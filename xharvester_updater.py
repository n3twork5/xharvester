#!/usr/bin/env python3
import os
import sys
import stat
import shutil
import platform
import subprocess

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
            if hasattr(os, 'getppid') and "termux" in os.readlink(f"/proc/{os.getppid()}/exe"):
                # Android/Termux
                return Path.home() / "xharvester"
            else:
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
            except subprocess.CalledProcessError:
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
                else:
                    self.print_error("Could not detect package manager. Please install git manually.")
                    return False
            except subprocess.CalledProcessError:
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
        if requirements_file.exists():
            try:
                subprocess.run([sys.executable, "-m", "pip", "install", "-r", str(requirements_file)], check=True)
                self.print_status("Dependencies installed successfully!")
                return True
            except subprocess.CalledProcessError:
                self.print_error("Failed to install dependencies from requirements.txt")
        
        # Fallback to specific packages
        try:
            subprocess.run([sys.executable, "-m", "pip", "install", "colorama", "requests"], check=True)
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
                bin_dir = Path(os.environ.get('APPDATA', str(Path.home()))) / "Local" / "Microsoft" / "WindowsApps"
                if not bin_dir.exists():
                    bin_dir = Path.home() / "AppData" / "Local" / "Programs" / "Python" / "Scripts"
                    if not bin_dir.exists():
                        bin_dir = Path(os.environ.get('USERPROFILE', str(Path.home()))) / "AppData" / "Roaming" / "Python" / "Scripts"
                
                if bin_dir.exists():
                    batch_file = bin_dir / "xharvester.bat"
                    with open(batch_file, 'w') as f:
                        f.write(f'@echo off\npython "{script_path}" %*\n')
                    self.print_status(f"Created batch file at {batch_file}")
                else:
                    self.print_warning("Could not find suitable directory for batch file")
                    
            else:
                # Unix-like systems (Linux, Android, macOS)
                bin_dir = Path.home() / ".local" / "bin"
                if not bin_dir.exists():
                    bin_dir.mkdir(parents=True)
                
                # Make script executable
                script_path.chmod(script_path.stat().st_mode | stat.S_IEXEC)
                
                # Create symlink
                symlink_path = bin_dir / "xharvester"
                if symlink_path.exists():
                    symlink_path.unlink()
                
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
        possible_names = ["xharvester.py", "xharvester", "main.py", "tool.py"]
        for name in possible_names:
            script_path = self.repo_path / name
            if script_path.exists():
                return script_path
        return None

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
oLink.Description = "XHarvester - Extended Reconnaissance Toolkit"
oLink.Save
'''
                    with open(vbs_script, 'w') as f:
                        f.write(vbs_content)
                    
                    # Run the VBS script to create the shortcut
                    subprocess.run(["cscript", "//Nologo", str(vbs_script)], check=True)
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
                    f.write(f'python "{script_path}"\n')
                    f.write('read -p "Press enter to continue"\n')
                
                shortcut_script.chmod(0o755)
                self.print_status("Created Android/Termux shortcut in ~/.shortcuts/")
                self.print_info("Add a Termux widget to your home screen to access XHarvester")
                
            else:
                # Linux and other Unix-like systems
                desktop_file = Path.home() / ".local" / "share" / "applications" / "xharvester.desktop"
                desktop_file.parent.mkdir(parents=True, exist_ok=True)
                
                desktop_content = f'''[Desktop Entry]
Version=1.0
Type=Application
Name=XHarvester
Comment=Extended Reconnaissance Toolkit
Exec=gnome-terminal --window -- python3 "{script_path}"
Icon=utilities-terminal
Terminal=false
Categories=Network;Security;
'''
                with open(desktop_file, 'w') as f:
                    f.write(desktop_content)
                
                # Make it executable
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
if __name__ == "__main__":
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