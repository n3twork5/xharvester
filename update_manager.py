#!/usr/bin/env python3
"""
Update Manager for xharvester
Handles automatic updates from GitHub with cross-platform support

Author: Network(GHANA)
Version: 2.1
"""

import os
import sys
import json
import shutil
import tempfile
import subprocess
import zipfile
from pathlib import Path
from datetime import datetime, timedelta
from typing import Optional, Dict, Any, Tuple
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from config import Config, Colors, PlatformDetector
from utils import Animation, Logger, error_handler, InputValidator


class GitHubAPI:
    """GitHub API interface for update checking"""
    
    def __init__(self):
        self.logger = Logger.get_logger("update_manager")
        self.session = self._create_session()
    
    def _create_session(self) -> requests.Session:
        """Create a configured requests session with retry logic"""
        session = requests.Session()
        
        # Configure retry strategy
        retry_strategy = Retry(
            total=3,
            backoff_factor=1,
            status_forcelist=[429, 500, 502, 503, 504],
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        session.mount("http://", adapter)
        session.mount("https://", adapter)
        
        # Set user agent
        session.headers.update({
            'User-Agent': f'{Config.APP_NAME}/{Config.VERSION}',
            'Accept': 'application/vnd.github.v3+json'
        })
        
        return session
    
    def get_latest_release(self) -> Optional[Dict[str, Any]]:
        """Get latest release information from GitHub"""
        try:
            url = f"{Config.GITHUB_API_URL}/releases/latest"
            response = self.session.get(url, timeout=30)
            
            # Handle 404 specifically for no releases scenario
            if response.status_code == 404:
                self.logger.info("No releases found for this repository")
                return None
            
            response.raise_for_status()
            return response.json()
            
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Failed to fetch latest release: {e}")
            return None
        except json.JSONDecodeError as e:
            self.logger.error(f"Failed to parse GitHub API response: {e}")
            return None
    
    def download_release(self, download_url: str, destination: Path) -> bool:
        """Download release archive"""
        try:
            with self.session.get(download_url, stream=True, timeout=Config.UPDATE_TIMEOUT) as response:
                response.raise_for_status()
                
                total_size = int(response.headers.get('content-length', 0))
                downloaded = 0
                
                with open(destination, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        if chunk:
                            f.write(chunk)
                            downloaded += len(chunk)
                            
                            if total_size > 0:
                                progress = (downloaded / total_size) * 100
                                print(f"\r{Colors.CYAN}  Downloading... {progress:.1f}%{Colors.RESET}", end="", flush=True)
                
                print()  # New line after progress
                return True
                
        except Exception as e:
            self.logger.error(f"Failed to download release: {e}")
            return False


class VersionManager:
    """Version comparison and management"""
    
    @staticmethod
    def parse_version(version_str: str) -> Tuple[int, ...]:
        """Parse version string into comparable tuple"""
        # Remove 'v' prefix if present
        clean_version = version_str.lstrip('v')
        
        # Split and convert to integers
        try:
            return tuple(int(x) for x in clean_version.split('.'))
        except ValueError:
            # Fallback for non-standard version formats
            return (0, 0, 0)
    
    @staticmethod
    def compare_versions(current: str, latest: str) -> int:
        """Compare version strings. Returns: -1 (older), 0 (same), 1 (newer)"""
        current_tuple = VersionManager.parse_version(current)
        latest_tuple = VersionManager.parse_version(latest)
        
        if current_tuple < latest_tuple:
            return -1  # Current is older
        elif current_tuple > latest_tuple:
            return 1   # Current is newer
        else:
            return 0   # Same version
    
    @staticmethod
    def is_update_available(current: str, latest: str) -> bool:
        """Check if an update is available"""
        return VersionManager.compare_versions(current, latest) == -1


class BackupManager:
    """Backup and restore functionality"""
    
    def __init__(self):
        self.logger = Logger.get_logger("backup_manager")
        self.project_root = Config.PROJECT_ROOT
        self.backup_dir = self.project_root / "backups"
        self.backup_dir.mkdir(exist_ok=True)
    
    def create_backup(self) -> Optional[Path]:
        """Create a backup of current installation"""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_name = f"xharvester_backup_{Config.VERSION}_{timestamp}"
            backup_path = self.backup_dir / f"{backup_name}.zip"
            
            print(f"{Colors.CYAN}  Creating backup: {backup_name}")
            
            with zipfile.ZipFile(backup_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                for root, dirs, files in os.walk(self.project_root):
                    # Skip backup directory and git directory
                    dirs[:] = [d for d in dirs if d not in ['backups', '.git', '__pycache__', 'venv']]
                    
                    for file in files:
                        if not file.endswith('.pyc'):
                            file_path = Path(root) / file
                            arc_path = file_path.relative_to(self.project_root)
                            zipf.write(file_path, arc_path)
            
            self.logger.info(f"Backup created: {backup_path}")
            return backup_path
            
        except Exception as e:
            self.logger.error(f"Failed to create backup: {e}")
            return None
    
    def cleanup_old_backups(self) -> None:
        """Remove old backup files, keeping only the most recent ones"""
        try:
            backups = sorted(self.backup_dir.glob("xharvester_backup_*.zip"), 
                           key=lambda x: x.stat().st_mtime, reverse=True)
            
            for backup in backups[Config.BACKUP_COUNT:]:
                backup.unlink()
                self.logger.info(f"Removed old backup: {backup.name}")
                
        except Exception as e:
            self.logger.error(f"Failed to cleanup old backups: {e}")
    
    def restore_backup(self, backup_path: Path) -> bool:
        """Restore from backup"""
        try:
            print(f"{Colors.YELLOW}  Restoring from backup...")
            
            # Create temporary directory for extraction
            with tempfile.TemporaryDirectory() as temp_dir:
                temp_path = Path(temp_dir)
                
                # Extract backup
                with zipfile.ZipFile(backup_path, 'r') as zipf:
                    zipf.extractall(temp_path)
                
                # Copy files back
                for item in temp_path.iterdir():
                    dest_path = self.project_root / item.name
                    if item.is_file():
                        shutil.copy2(item, dest_path)
                    elif item.is_dir():
                        if dest_path.exists():
                            shutil.rmtree(dest_path)
                        shutil.copytree(item, dest_path)
            
            print(f"{Colors.SUCCESS}  Backup restored successfully!")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to restore backup: {e}")
            print(f"{Colors.ERROR}  Failed to restore backup: {e}")
            return False


class UpdateManager:
    """Main update manager class"""
    
    def __init__(self):
        self.logger = Logger.get_logger("update_manager")
        self.github_api = GitHubAPI()
        self.version_manager = VersionManager()
        self.backup_manager = BackupManager()
        self.project_root = Config.PROJECT_ROOT
    
    def check_for_updates(self) -> Optional[Dict[str, Any]]:
        """Check if updates are available"""
        print(f"{Colors.CYAN}  [{Colors.GREEN}+{Colors.CYAN}] Checking for updates...")
        
        release_info = self.github_api.get_latest_release()
        if not release_info:
            print(f"{Colors.WARNING}  No releases available yet - you're using the development version!")
            return None
        
        latest_version = release_info.get('tag_name', '').lstrip('v')
        current_version = Config.VERSION
        
        print(f"{Colors.INFO}  Current version: {Colors.YELLOW}v{current_version}")
        print(f"{Colors.INFO}  Latest version:  {Colors.YELLOW}v{latest_version}")
        
        if self.version_manager.is_update_available(current_version, latest_version):
            print(f"{Colors.SUCCESS}  🎉 New version available!")
            return release_info
        else:
            print(f"{Colors.SUCCESS}  ✅ You have the latest version!")
            return None
    
    def get_platform_download_url(self, release_info: Dict[str, Any]) -> Optional[str]:
        """Get appropriate download URL for current platform"""
        # For now, we'll use the source code archive since the tool is Python-based
        # In the future, platform-specific releases could be added
        return release_info.get('zipball_url')
    
    def perform_update(self) -> bool:
        """Perform the actual update process"""
        with error_handler("performing update", self.logger):
            print(f"\n{Colors.CYAN}  [{Colors.GREEN}+{Colors.CYAN}] Starting update process...")
            
            # Step 1: Check for updates
            release_info = self.check_for_updates()
            if not release_info:
                return False
            
            # Step 2: Confirm update
            latest_version = release_info.get('tag_name', '').lstrip('v')
            print(f"\n{Colors.YELLOW}  Update Details:")
            print(f"  - Version: {Colors.CYAN}v{latest_version}")
            print(f"  - Published: {Colors.CYAN}{release_info.get('published_at', 'Unknown')}")
            print(f"  - Description: {Colors.CYAN}{release_info.get('name', 'No description')}")
            
            confirm = input(f"\n{Colors.GREEN}  Do you want to update? ({Colors.CYAN}y{Colors.GREEN}/{Colors.RED}N{Colors.GREEN}): {Colors.YELLOW}").strip().lower()
            if confirm not in ['y', 'yes']:
                print(f"{Colors.WARNING}  Update cancelled by user.")
                return False
            
            # Step 3: Create backup
            print(f"\n{Colors.CYAN}  [{Colors.GREEN}+{Colors.CYAN}] Creating backup...")
            backup_path = self.backup_manager.create_backup()
            if not backup_path:
                print(f"{Colors.ERROR}  Failed to create backup! Update aborted.")
                return False
            
            try:
                # Step 4: Download update
                download_url = self.get_platform_download_url(release_info)
                if not download_url:
                    print(f"{Colors.ERROR}  No download URL found for your platform!")
                    return False
                
                print(f"\n{Colors.CYAN}  [{Colors.GREEN}+{Colors.CYAN}] Downloading update...")
                
                with tempfile.TemporaryDirectory() as temp_dir:
                    temp_path = Path(temp_dir)
                    archive_path = temp_path / "update.zip"
                    
                    if not self.github_api.download_release(download_url, archive_path):
                        raise Exception("Download failed")
                    
                    # Step 5: Extract and install
                    print(f"{Colors.CYAN}  [{Colors.GREEN}+{Colors.CYAN}] Installing update...")
                    
                    extract_path = temp_path / "extracted"
                    with zipfile.ZipFile(archive_path, 'r') as zipf:
                        zipf.extractall(extract_path)
                    
                    # Find the extracted directory (GitHub creates a folder with repo name)
                    extracted_dirs = [d for d in extract_path.iterdir() if d.is_dir()]
                    if not extracted_dirs:
                        raise Exception("No extracted directory found")
                    
                    source_dir = extracted_dirs[0]
                    
                    # Copy new files (excluding certain directories)
                    self._install_update(source_dir)
                
                # Step 6: Cleanup old backups
                self.backup_manager.cleanup_old_backups()
                
                print(f"\n{Colors.SUCCESS}  ✅ Update completed successfully!")
                print(f"{Colors.INFO}  Backup saved as: {Colors.CYAN}{backup_path.name}")
                print(f"{Colors.WARNING}  Please restart xharvester to use the new version.")
                
                return True
                
            except Exception as e:
                print(f"\n{Colors.ERROR}  Update failed: {e}")
                
                # Attempt to restore from backup
                if backup_path and backup_path.exists():
                    print(f"{Colors.WARNING}  Attempting to restore from backup...")
                    if self.backup_manager.restore_backup(backup_path):
                        print(f"{Colors.SUCCESS}  Successfully restored from backup!")
                    else:
                        print(f"{Colors.ERROR}  Failed to restore from backup!")
                
                return False
    
    def _install_update(self, source_dir: Path) -> None:
        """Install update files from source directory"""
        exclude_dirs = {'.git', '__pycache__', 'venv', 'backups', 'logs'}
        exclude_files = {'*.pyc', '*.pyo', '*.pyd'}
        
        for item in source_dir.iterdir():
            if item.name in exclude_dirs:
                continue
            
            dest_path = self.project_root / item.name
            
            if item.is_file():
                if not any(item.name.endswith(ext.lstrip('*')) for ext in exclude_files):
                    shutil.copy2(item, dest_path)
                    print(f"  Updated: {item.name}")
            elif item.is_dir():
                if dest_path.exists() and dest_path.name not in {'logs', 'backups'}:
                    shutil.rmtree(dest_path)
                if not dest_path.exists():
                    shutil.copytree(item, dest_path)
                    print(f"  Updated: {item.name}/")
    
    def show_update_info(self) -> None:
        """Show current update information"""
        print(f"\n{Colors.CYAN}  [{Colors.GREEN}ℹ{Colors.CYAN}] Update Information:")
        print(f"  Current version: {Colors.YELLOW}v{Config.VERSION}")
        print(f"  Platform: {Colors.YELLOW}{Config.CURRENT_PLATFORM}")
        if Config.IS_TERMUX:
            print(f"  Environment: {Colors.YELLOW}Termux/Android")
        print(f"  GitHub: {Colors.YELLOW}{Config.GITHUB_REPO_URL}")
        print(f"  Auto-update: {Colors.YELLOW}{'Enabled' if Config.AUTO_UPDATE else 'Disabled'}")


def main():
    """Test the update manager"""
    try:
        update_manager = UpdateManager()
        update_manager.show_update_info()
        
        choice = input(f"\n{Colors.GREEN}Check for updates? (y/N): {Colors.YELLOW}").strip().lower()
        if choice in ['y', 'yes']:
            update_manager.perform_update()
            
    except KeyboardInterrupt:
        print(f"\n{Colors.WARNING}Update check cancelled by user.")
    except Exception as e:
        print(f"{Colors.ERROR}Update manager error: {e}")


if __name__ == "__main__":
    main()