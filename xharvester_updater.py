#!/usr/bin/env python3
import os
import sys
import stat
import shutil
import platform
import subprocess
import time
from pathlib import Path

class XHarvesterUpdater:
    """XHarvester updater scripts"""
    
    # Configuration
    REPO_URL = "https://github.com/n3tworkh4x/xharvester.git"
    BRANCH = "main"
    DIR_NAME = "xharvester"
    
    # Colors for output
    class Colors:
        RED = '\033[0;31m'
        GREEN = '\033[0;32m'
        YELLOW = '\033[1;33m'
        BLUE = '\033[0;34m'
        CYAN = '\033[0;36m'
        MAGENTA = '\033[0;35m'
        NC = '\033[0m'  # No Color

    def __init__(self, install_dir=None):
        """Initialize the updater with optional custom install directory"""
        self.install_dir = install_dir or self.get_install_dir()
        self.repo_path = self.install_dir / self.DIR_NAME
        
    @staticmethod
    def print_status(msg):
        print(f"{XHarvesterUpdater.Colors.GREEN}[+]{XHarvesterUpdater.Colors.NC} {msg}")

    @staticmethod
    def print_warning(msg):
        print(f"{XHarvesterUpdater.Colors.YELLOW}[!]{XHarvesterUpdater.Colors.NC} {msg}")

    @staticmethod
    def print_error(msg):
        print(f"{XHarvesterUpdater.Colors.RED}[-]{XHarvesterUpdater.Colors.NC} {msg}")

    @staticmethod
    def print_info(msg):
        print(f"{XHarvesterUpdater.Colors.BLUE}[*]{XHarvesterUpdater.Colors.NC} {msg}")

    def get_install_dir(self):
        """Determine the appropriate installation directory based on platform"""
        system = platform.system().lower()
        
        if system == "windows":
            # Use AppData on Windows
            appdata = os.environ.get('APPDATA', '')
            if appdata:
                return Path(appdata) / "xharvester"
            return Path.home() / "xharvester"
        
        elif "android" in system or "linux" in system:
            # Check if we're on Android (Termux)
            try:
                if "termux" in os.readlink(f"/proc/{os.getppid()}/exe"):
                    # Android/Termux
                    return Path.home() / "xharvester"
            except (FileNotFoundError, AttributeError, OSError):
                pass
            
            # Regular Linux
            return Path.home() / ".local" / "share" / "xharvester"
        
        else:
            # macOS or other Unix-like
            return Path.home() / ".local" / "share" / "xharvester"

    def check_git(self):
        """Check if git is available"""
        try:
            subprocess.run(["git", "--version"], check=True, 
                          stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            return False

    def install_git(self):
        """Attempt to install git based on platform"""
        system = platform.system().lower()
        
        if system == "windows":
            self.print_info("Please install Git for Windows from: https://git-scm.com/download/win")
            return False
            
        elif "android" in system:
            # Android (Termux)
            try:
                subprocess.run(["pkg", "install", "git", "-y"], check=True)
                return True
            except (subprocess.CalledProcessError, FileNotFoundError):
                self.print_error("Failed to install git on Android. Try: pkg install git")
                return False
                
        elif system == "linux":
            # Try to detect package manager
            try:
                if shutil.which("apt-get"):
                    subprocess.run(["sudo", "apt-get", "install", "git", "-y"], check=True)
                    return True
                elif shutil.which("yum"):
                    subprocess.run(["sudo", "yum", "install", "git", "-y"], check=True)
                    return True
                elif shutil.which("pacman"):
                    subprocess.run(["sudo", "pacman", "-S", "git", "--noconfirm"], check=True)
                    return True
                elif shutil.which("dnf"):
                    subprocess.run(["sudo", "dnf", "install", "git", "-y"], check=True)
                    return True
                else:
                    self.print_error("Could not detect package manager. Please install git manually.")
                    return False
            except (subprocess.CalledProcessError, FileNotFoundError):
                self.print_error("Failed to install git. Please install it manually.")
                return False
                
        else:
            self.print_error(f"Please install git manually on {system}")
            return False

    def update_repo(self):
        """Update or clone the repository"""
        if (self.repo_path / ".git").exists():
            # Update existing repository
            self.print_info("Updating existing repository...")
            try:
                subprocess.run(["git", "pull", "origin", self.BRANCH], cwd=self.repo_path, check=True)
                self.print_status("Update completed successfully!")
                return True
            except subprocess.CalledProcessError:
                self.print_warning("Git pull failed. Trying fresh clone...")
                try:
                    shutil.rmtree(self.repo_path)
                except OSError:
                    self.print_error(f"Could not remove directory {self.repo_path}")
                    return False
        
        # Clone repository
        self.print_info("Cloning repository...")
        try:
            subprocess.run(["git", "clone", "-b", self.BRANCH, self.REPO_URL, str(self.repo_path)], check=True)
            self.print_status("Installation completed successfully!")
            return True
        except subprocess.CalledProcessError:
            self.print_error("Git clone failed")
            return False

    def install_dependencies(self):
        """Install Python dependencies"""
        self.print_info("Installing Python dependencies...")
        
        requirements_file = self.repo_path / "requirements.txt"
        pip_command = [sys.executable, "-m", "pip", "install", "--upgrade"]
        
        # Add --break-system-packages only if supported (Python 3.10+)
        try:
            python_version = sys.version_info
            if python_version.major == 3 and python_version.minor >= 10:
                pip_command.append("--break-system-packages")
        except AttributeError:
            pass
            
        if requirements_file.exists():
            try:
                subprocess.run(pip_command + ["-r", str(requirements_file)], check=True)
                self.print_status("Dependencies installed successfully!")
                return True
            except subprocess.CalledProcessError:
                self.print_error("Failed to install dependencies from requirements.txt")
        
        # Fallback to specific packages
        try:
            subprocess.run(pip_command + ["colorama", "requests"], check=True)
            self.print_status("Dependencies installed successfully!")
            return True
        except subprocess.CalledProcessError:
            self.print_error("Failed to install dependencies")
            return False

    def create_symlink(self):
        """Create a symlink or batch file for easy execution"""
        system = platform.system().lower()
        script_path = self.find_main_script()
        
        if not script_path:
            self.print_warning("Main script not found, skipping symlink creation")
            return False
        
        try:
            if system == "windows":
                # Create a batch file
                bin_dirs = [
                    Path(os.environ.get('APPDATA', '')) / "Local" / "Microsoft" / "WindowsApps",
                    Path.home() / "AppData" / "Local" / "Programs" / "Python" / "Scripts",
                    Path(os.environ.get('USERPROFILE', '')) / "AppData" / "Roaming" / "Python" / "Scripts",
                    Path.home() / "Desktop"
                ]
                
                bin_dir = None
                for candidate in bin_dirs:
                    if candidate.exists():
                        bin_dir = candidate
                        break
                
                if bin_dir is None:
                    bin_dir = Path.home()
                
                batch_file = bin_dir / "xharvester.bat"
                with open(batch_file, 'w') as f:
                    f.write(f'@echo off\n"{sys.executable}" "{script_path}" %*\n')
                self.print_status(f"Created batch file at {batch_file}")
                return True
                    
            else:
                # Unix-like systems (Linux, Android, macOS)
                bin_dir = Path.home() / ".local" / "bin"
                if not bin_dir.exists():
                    bin_dir.mkdir(parents=True, exist_ok=True)
                
                # Make script executable
                script_path.chmod(script_path.stat().st_mode | stat.S_IEXEC)
                
                # Create symlink
                symlink_path = bin_dir / "xharvester"
                if symlink_path.exists():
                    if symlink_path.is_symlink():
                        symlink_path.unlink()
                    else:
                        self.print_warning(f"{symlink_path} exists but is not a symlink, skipping")
                        return False
                
                os.symlink(script_path, symlink_path)
                self.print_status(f"Created symlink at {symlink_path}")
                
                # Add to PATH if not already there
                if str(bin_dir) not in os.environ.get('PATH', ''):
                    self.print_warning(f"Add {bin_dir} to your PATH to run xharvester from anywhere")
                
                return True
            
        except Exception as e:
            self.print_error(f"Failed to create symlink/batch file: {e}")
            return False

    def find_main_script(self):
        """Find the main script in the repository"""
        # First, check for common entry points
        possible_names = ["xharvester.py", "xharvester", "main.py", "tool.py", "__main__.py"]
        
        for name in possible_names:
            script_path = self.repo_path / name
            if script_path.exists():
                return script_path
        
        # If not found, look for any Python file that might be the main script
        for file_path in self.repo_path.glob("*.py"):
            try:
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                    # Check if it looks like a main script
                    if "if __name__ == '__main__':" in content or "def main()" in content:
                        return file_path
            except Exception:
                continue
        
        # Last resort: check for any executable file
        for file_path in self.repo_path.iterdir():
            if file_path.is_file() and (os.access(file_path, os.X_OK) or file_path.suffix == ''):
                return file_path
        
        return None

    def verify_installation(self):
        """Verify that the installation was successful and the command is accessible"""
        self.print_info("Verifying installation...")
        
        system = platform.system().lower()
        
        if system == "windows":
            # Check for batch file on Windows
            bin_dirs = [
                Path(os.environ.get('APPDATA', '')) / "Local" / "Microsoft" / "WindowsApps",
                Path.home() / "AppData" / "Local" / "Programs" / "Python" / "Scripts",
                Path(os.environ.get('USERPROFILE', '')) / "AppData" / "Roaming" / "Python" / "Scripts",
                Path.home() / "Desktop"
            ]
            
            batch_file = None
            for bin_dir in bin_dirs:
                potential_batch = bin_dir / "xharvester.bat"
                if potential_batch.exists():
                    batch_file = potential_batch
                    break
            
            if batch_file:
                self.print_status(f"Batch file exists at {batch_file}")
                # Check if it's in PATH
                path_dirs = [Path(p) for p in os.environ.get('PATH', '').split(';')]
                if batch_file.parent in path_dirs:
                    self.print_status("Batch file directory is in PATH")
                    return True
                else:
                    self.print_warning(f"Batch file directory {batch_file.parent} is not in PATH")
                    return False
            else:
                self.print_error("Batch file was not created successfully")
                return False
        else:
            # Check if symlink exists and is valid on Unix systems
            bin_dir = Path.home() / ".local" / "bin"
            symlink_path = bin_dir / "xharvester"
            
            if symlink_path.exists() and symlink_path.is_symlink():
                self.print_status(f"Symlink exists at {symlink_path}")
                
                # Check if it's in PATH
                path_dirs = [Path(p) for p in os.environ.get('PATH', '').split(':')]
                if bin_dir in path_dirs:
                    self.print_status("Symlink directory is in PATH")
                    
                    # Test if the command works
                    try:
                        result = subprocess.run(["which", "xharvester"], capture_output=True, text=True, timeout=5)
                        if result.returncode == 0:
                            self.print_status("Command 'xharvester' is available in PATH")
                            return True
                        else:
                            self.print_warning("Command 'xharvester' not found in PATH")
                    except (subprocess.TimeoutExpired, FileNotFoundError, Exception):
                        self.print_warning("Could not verify command availability")
                else:
                    self.print_warning(f"Symlink directory {bin_dir} is not in PATH")
                    
                    # Offer to add it to PATH
                    response = input("Would you like to add it to your PATH? (Y/n): ")
                    if response.lower() not in ['n', 'no']:
                        self.add_to_path(bin_dir)
            else:
                self.print_error("Symlink was not created successfully")
            
            return False

    def add_to_path(self, bin_dir):
        """Add a directory to the user's PATH"""
        system = platform.system().lower()
        
        if system == "windows":
            self.print_info(f"Please add {bin_dir} to your PATH manually on Windows")
            self.print_info("Instructions:")
            self.print_info("1. Right-click on 'This PC' or 'My Computer' and select 'Properties'")
            self.print_info("2. Click on 'Advanced system settings'")
            self.print_info("3. Click on 'Environment Variables'")
            self.print_info("4. Under 'User variables', find and select the 'Path' variable")
            self.print_info("5. Click 'Edit' and add the path to the directory")
            return False
        else:
            # Unix-like systems
            shell_configs = [
                Path.home() / ".bashrc",
                Path.home() / ".bash_profile", 
                Path.home() / ".profile",
                Path.home() / ".zshrc"
            ]
            
            for shell_config in shell_configs:
                if shell_config.exists():
                    path_line = f'\nexport PATH="$PATH:{bin_dir}"\n'
                    
                    try:
                        with open(shell_config, 'a') as f:
                            f.write(path_line)
                        self.print_status(f"Added {bin_dir} to PATH in {shell_config}")
                        self.print_info(f"Please run 'source {shell_config.name}' or restart your terminal")
                        return True
                    except Exception as e:
                        self.print_error(f"Failed to add to PATH in {shell_config}: {e}")
            
            self.print_error("Could not find a shell configuration file to modify")
            return False

    def create_desktop_launcher(self):
        """Create a desktop launcher for GUI environments"""
        system = platform.system().lower()
        script_path = self.find_main_script()
        
        if not script_path:
            self.print_warning("Main script not found, skipping desktop launcher creation")
            return False
        
        try:
            if system == "windows":
                # Create Windows shortcut
                desktop = Path.home() / "Desktop"
                if not desktop.exists():
                    desktop = Path.home() / "OneDrive" / "Desktop"
                    if not desktop.exists():
                        desktop = Path(os.environ.get('USERPROFILE', '')) / "Desktop"
                
                if desktop.exists():
                    vbs_script = desktop / "create_xharvester_shortcut.vbs"
                    shortcut_path = desktop / "XHarvester.lnk"
                    
                    vbs_content = f'''
Set oWS = WScript.CreateObject("WScript.Shell")
sLinkFile = "{shortcut_path}"
Set oLink = oWS.CreateShortcut(sLinkFile)
oLink.TargetPath = "cmd.exe"
oLink.Arguments = "/k python \"{script_path}\" && pause"
oLink.WorkingDirectory = "{self.repo_path}"
oLink.Description = "Extended Reconnaissance Toolkit Developed By N3TWORK@(GHANA)"
oLink.Save
'''
                    with open(vbs_script, 'w') as f:
                        f.write(vbs_content)
                    
                    # Run the VBS script to create the shortcut
                    subprocess.run(["cscript", str(vbs_script)], check=True)
                    vbs_script.unlink()  # Clean up
                    
                    self.print_status(f"Created desktop shortcut at {shortcut_path}")
                else:
                    self.print_warning("Could not find desktop directory")
                    
            elif "android" in system:
                # Android - create a Termux widget script
                termux_shortcut_dir = Path.home() / ".shortcuts"
                termux_shortcut_dir.mkdir(exist_ok=True)
                
                shortcut_script = termux_shortcut_dir / "XHarvester"
                with open(shortcut_script, 'w') as f:
                    f.write('#!/bin/bash\n')
                    f.write(f'cd "{self.repo_path}"\n')
                    f.write('termux-toast "Starting XHarvester..."\n')
                    f.write(f'python "{script_path.name}"\n')
                    f.write('read -p "Press enter to continue"\n')
                
                shortcut_script.chmod(0o755)
                self.print_status("Created Android/Termux shortcut in ~/.shortcuts/")
                self.print_info("Add a Termux widget to your home screen to access XHarvester")
                
            else:
                # Linux and other Unix-like systems
                desktop_file = Path.home() / ".local" / "share" / "applications" / "xharvester.desktop"
                desktop_file.parent.mkdir(parents=True, exist_ok=True)
                
                # Use absolute path for the icon or remove it if not available
                icon_path = self.repo_path / "icons" / "jenkins_logo_icon_247972.png"
                icon_line = f"Icon={icon_path}" if icon_path.exists() else "Icon=terminal"
                
                desktop_content = f'''[Desktop Entry]
Version=1.0.0
Type=Application
Name=xharvester
Comment=Extended Reconnaissance Toolkit Developed By N3TWORK@(GHANA)
Exec=python3 "{script_path}"
{icon_line}
Terminal=true
Categories=Network;Security;
'''
                with open(desktop_file, 'w') as f:
                    f.write(desktop_content)
                
                # Make the desktop file executable
                desktop_file.chmod(desktop_file.stat().st_mode | stat.S_IEXEC)
                
                self.print_status(f"Created desktop launcher at {desktop_file}")
                
            return True
            
        except Exception as e:
            self.print_error(f"Failed to create desktop launcher: {e}")
            return False

    def create_mobile_launcher(self):
        """Create a mobile-friendly launcher for Android"""
        system = platform.system().lower()
        
        if "android" not in system:
            self.print_info("Mobile launcher is only applicable to Android")
            return False
        
        try:
            # Create a simple HTML launcher page that can be opened in a browser
            html_launcher = self.install_dir / "xharvester_launcher.html"
            
            html_content = '''<!DOCTYPE html>
<html>
<head>
    <title>XHarvester Launcher</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        body {
            font-family: Arial, sans-serif;
            max-width: 600px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f0f0f0;
        }
        .button {
            display: block;
            width: 100%;
            padding: 15px;
            margin: 10px 0;
            background-color: #4CAF50;
            color: white;
            text-align: center;
            text-decoration: none;
            border-radius: 5px;
            font-size: 18px;
        }
    </style>
</head>
<body>
    <h1>XHarvester Launcher</h1>
    <p>Click the button below to launch XHarvester in Termux:</p>
    <a class="button" href="intent://run/#Intent;scheme=termux;package=com.termux;S.org.freedesktop.intent.extra.EXECUTE_SCRIPT=python3 /data/data/com.termux/files/home/xharvester/xharvester.py;end">Launch XHarvester</a>
    <p>Note: This requires Termux to be installed and the Termux API app for intent handling.</p>
</body>
</html>
'''
            with open(html_launcher, 'w') as f:
                f.write(html_content)
            
            self.print_status(f"Created mobile launcher at {html_launcher}")
            self.print_info("Open this HTML file in your mobile browser to launch XHarvester")
            
            return True
            
        except Exception as e:
            self.print_error(f"Failed to create mobile launcher: {e}")
            return False

    def run(self, create_launchers=True):
        """Run the complete update process"""
        self.print_info(f"Installation directory: {self.install_dir}")
        
        # Create directory if it doesn't exist
        self.install_dir.mkdir(parents=True, exist_ok=True)
        
        # Check for git
        if not self.check_git():
            self.print_warning("Git is not installed")
            if not self.install_git():
                return False
        
        # Update repository
        if not self.update_repo():
            return False
        
        # Install dependencies
        if not self.install_dependencies():
            self.print_warning("Dependency installation had issues, but continuing...")
        
        # Create symlink
        if not self.create_symlink():
            self.print_warning("Symlink creation failed, but installation completed")
        
        # Verify installation
        self.verify_installation()
        
        # Create launchers if requested
        if create_launchers:
            if not self.create_desktop_launcher():
                self.print_warning("Desktop launcher creation failed")
            
            # For Android, create mobile launcher
            system = platform.system().lower()
            if "android" in system:
                if not self.create_mobile_launcher():
                    self.print_warning("Mobile launcher creation failed")
        
        self.print_status("XHARVESTER has been successfully updated/installed!")
        script_path = self.find_main_script()
        if script_path:
            self.print_info(f"You can run it with: python {script_path}")
        
        return True


# Standalone execution
def main():
    try:
        # Color codes
        GREEN = '\033[32m'
        YELLOW = '\033[33m'
        RED = '\033[31m'
        BLUE = '\033[34m'
        MAGENTA = '\033[35m'
        CYAN = '\033[36m'
        LIGHTCYAN_EX = '\033[96m'
        RESET = '\033[0m'

        print(f"{XHarvesterUpdater.Colors.CYAN}")
        print("┌─────────────────────────────────────────────────────┐")
        print("│              XHARVESTER UPDATER                     │")
        print("└─────────────────────────────────────────────────────┘")
        print(f"{XHarvesterUpdater.Colors.NC}")
        
        # Check if running as root (not recommended)
        if hasattr(os, 'getuid') and os.getuid() == 0:
            XHarvesterUpdater.print_warning("Running as root - this is not recommended for security reasons")
            response = input("Continue anyway? (y/N): ")
            if response.lower() not in ['y', 'yes']:
                sys.exit(1)
        
        # Create updater instance
        updater = XHarvesterUpdater()
        
        # Ask about creating launchers
        response = input("Create desktop/launcher shortcuts? (Y/n): ")
        create_launchers = response.lower() not in ['n', 'no']
        
        # Run the update
        success = updater.run(create_launchers=create_launchers)
        
        # Exit with appropriate code
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        msg = f"\n\n\t\t\t{MAGENTA}[💀] {RESET}{RED}Process Terminated by User\n\n"
        for word in msg:
            print(word, end="", flush=True)
            time.sleep(0.05)
        sys.exit(1)

# Allow the script to be imported without running
if __name__ == "__main__":
    main()