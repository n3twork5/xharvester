#!/bin/env python3
import os
import time
import socket
import sys
import platform
from datetime import datetime

try:
    from xharvester_updater import XHarvesterUpdater
    UPDATER_AVAILABLE = True
except ImportError:
    UPDATER_AVAILABLE = False
    # Create a minimal stub for the updater
    class XHarvesterUpdater:
        def __init__(self):
            print("Update functionality is not available. Please ensure xharvester_updater.py is in the same directory.")
        
        def run(self, create_launchers=True):
            print("Update functionality is not available.")
            return False

# Use proper ANSI escape sequences for all systems with platform compatibility
if platform.system() == "Windows":
    # Enable ANSI support on Windows 10+
    os.system("")  # This enables ANSI escape sequences on Windows

# Color codes
GREEN = '\033[32m'
YELLOW = '\033[33m'
RED = '\033[31m'
BLUE = '\033[34m'
MAGENTA = '\033[35m'
CYAN = '\033[36m'
LIGHTCYAN_EX = '\033[96m'
RESET = '\033[0m'

# Configuration
ANIMATION_SPEED = 0.005

### Color Status ###
def print_status(message: str) -> None:
    """Print status messages"""
    print(f"{GREEN}[+]{RESET} {message}")

def print_warning(message: str) -> None:
    """Print warning messages"""
    print(f"{YELLOW}[!]{RESET} {message}")

def print_error(message: str) -> None:
    """Print error messages"""
    print(f"{RED}[-]{RESET} {message}")

### Text Animation ###
def text_animation():
    banner_text = f"""{MAGENTA}
 _  _  _   _    __    ____  _  _  ____  ___  ____  ____  ____ {RED}
( \/ )( )_( )  /__\  (  _ \( \/ )( ___)/ __)(_  _)( ___)(  _ \\{MAGENTA}
 )  (  ) _ (  /(__)\  )   / \  /  )__) \__ \  )(   )__)  )   /{RED}
(_/\_)(_) (_)(__)(__)(_)\_)  \/  (____)(___/ (__) (____)(_)\_)
    {RESET}"""
    for char in banner_text:
        print(char, end='', flush=True)
        time.sleep(ANIMATION_SPEED)
    print(f"\n{CYAN}>>> Extended Reconnaissance Toolkit For Pentesters <<<{RESET}")
    print(f"{GREEN}| GitHub:{RESET}{YELLOW} @n3tworkh4x |{RESET}{MAGENTA} Ko-fi{YELLOW}(Donation):{RESET}{GREEN} https://ko-fi.com/n3twork |")
    print(f"{RED}Use only for authorized security testing!{RESET}")

### Display Menu ###
def show_menu() -> None:
    text_animation()
    print(f"\n\t\t\t(▀̿Ĺ̯▀̿ ̿)\t\t\t\n")
    print(f"{LIGHTCYAN_EX}  ⇇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━⇉")
    print(f"{GREEN}         🚀   XHARVESTER -- MAIN MENU")
    print(f"{LIGHTCYAN_EX}  ⇇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━⇉")
    print(f"{CYAN}\t[1] 🔀 BlueTooth")
    print(f"{CYAN}\t[2] 📶 Wifi")
    print(f"{CYAN}\t[3] 🚖 Automobile")
    print(f"{CYAN}\t[4] 📡 Radio Frequency")
    print(f"{CYAN}\t[5] 🏙️  Industrial Control System - SCADA")
    print(f"{CYAN}\t[6] 🤘 About")
    print(f"{LIGHTCYAN_EX}  ⇇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━⇉")
    print(f"{RED}\t [0] ❌ Exit")
    print(f"{YELLOW}\t[99] 🎁 Update XHARVESTER")
    print(f"{LIGHTCYAN_EX}  ⇇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━⇉")  

### Display About ###
def about() -> None:
    description = f"""
{RED}\t\t\t━━━━━━━━━━\t\t\t
{YELLOW}Bio: {RESET}{GREEN}I am a 19-year-old skilled hacker and programmer with expertise in ICS/SCADA security,
{GREEN}Wireless exploitation (Wi-Fi/Bluetooth/RF) & Automotive systems hacking.
{RED}\t\t\t━━━━━━━━━━\t\t\t
{YELLOW}About: {RESET}{CYAN}xharvester is a specialized,{RESET}
{CYAN}modular Python-based reconnaissance suite designed for security assessments of radio frequency (RF),{RESET}
{CYAN}wireless (bluetooth & wifi),{RESET}
{CYAN}industrial control system (SCADA),{RESET}
{CYAN}and automotive systems.{RESET}
{CYAN}It integrates multiple tools and scripts into a unified workflow for probing,{RESET}
{CYAN}analyzing, and documenting findings from the physical and wireless world.{RESET}

{YELLOW}Version: {RESET}{GREEN}1.0.0{RESET}
{YELLOW}Last Updated: {RESET}{GREEN}2023-11-15{RESET}
"""
    print(description)

### Clear screen function with platform detection ###
def clear_screen() -> None:
    """Clear the terminal screen based on the operating system"""
    os.system('cls' if os.name == 'nt' else 'clear')

### Get hostname with error handling ###
def get_hostname() -> str:
    """Get hostname with proper error handling"""
    try:
        return socket.gethostname()
    except:
        return "unknown"

### Check for root privileges ###
def check_root() -> bool:
    """Check if the script is running with root privileges"""
    if platform.system() == "Windows":
        # On Windows, we need to check for administrator privileges
        try:
            import ctypes
            return ctypes.windll.shell32.IsUserAnAdmin() != 0
        except:
            return False
    else:
        # On Unix-like systems, check for root UID
        return os.geteuid() == 0

### Module placeholder functions ###
def bluetooth_module():
    """Placeholder for Bluetooth functionality"""
    print_status("Initializing Bluetooth module...")
    # Add actual Bluetooth scanning/exploitation code here
    time.sleep(2)
    print_warning("Bluetooth module is a placeholder - actual functionality not implemented")

def wifi_module():
    """Placeholder for WiFi functionality"""
    print_status("Initializing WiFi module...")
    # Add actual WiFi scanning/exploitation code here
    time.sleep(2)
    print_warning("WiFi module is a placeholder - actual functionality not implemented")

def automobile_module():
    """Placeholder for Automobile functionality"""
    print_status("Initializing Automobile module...")
    # Add actual automobile hacking code here
    time.sleep(2)
    print_warning("Automobile module is a placeholder - actual functionality not implemented")

def rf_module():
    """Placeholder for Radio Frequency functionality"""
    print_status("Initializing Radio Frequency module...")
    # Add actual RF scanning/exploitation code here
    time.sleep(2)
    print_warning("RF module is a placeholder - actual functionality not implemented")

def scada_module():
    """Placeholder for SCADA functionality"""
    print_status("Initializing SCADA module...")
    # Add actual SCADA scanning/exploitation code here
    time.sleep(2)
    print_warning("SCADA module is a placeholder - actual functionality not implemented")

### Main Program ###
def main():
    # Check for root privileges
    if not check_root():
        warning = "[!] Please run xharvester with administrator/root privileges\n"
        for word in warning:
            print(word, end='', flush=True)
            time.sleep(0.05)
        sys.exit(1)
    
    # ========== MAIN LOOP ========== #
    active = True
    while active:
        clear_screen()
        show_menu()
        
        try:
            choice = input(f"\n{GREEN}root@{get_hostname()}:~$ {RESET}")
        except (KeyboardInterrupt, EOFError):
            print("\n\nExiting...")
            break
            
        if choice == "0":
            skull = f"{MAGENTA}[💀]{RESET}"
            closing_text = f"{RED}Closing The Program...{RESET}"
            time.sleep(0.10)
            
            print(f"\n{skull} {closing_text}\n")
            active = False
            
        elif choice == "1":
            bluetooth_module()
            input(f"\n{GREEN}Press Enter to continue...{RESET}")
            
        elif choice == "2":
            wifi_module()
            input(f"\n{GREEN}Press Enter to continue...{RESET}")

        elif choice == "3":
            automobile_module()
            input(f"\n{GREEN}Press Enter to continue...{RESET}")

        elif choice == '4':
            rf_module()
            input(f"\n{GREEN}Press Enter to continue...{RESET}")

        elif choice == '5':
            scada_module()
            input(f"\n{GREEN}Press Enter to continue...{RESET}")

        elif choice == '6':
            try:
                time_choice = input(f'{GREEN}[?] Choose time stamps [Read Bio & About][default = 10]>>> {RESET}')
                if not time_choice:
                    about()
                    time.sleep(10)
                else:
                    about()
                    time.sleep(int(time_choice))
            except ValueError:
                print_error("Invalid input. Using default time of 10 seconds.")
                time.sleep(10)
            except (KeyboardInterrupt, EOFError):
                print("\n\nReturning to menu...")
                time.sleep(1)

        elif choice == '99':
            clear_screen()
            try:
                if UPDATER_AVAILABLE:
                    updater = XHarvesterUpdater()
                    # Ask about creating launchers
                    response = input("Create desktop/launcher shortcuts? (Y/n): ")
                    create_launchers = response.lower() not in ['n', 'no']
                    
                    success = updater.run(create_launchers=create_launchers)
                    if success:
                        print_status("Update completed successfully!")
                    else:
                        print_error("Update failed!")
                else:
                    print_error("Update functionality is not available. Please ensure xharvester_updater.py is in the same directory.")
            except Exception as e:
                print_error(f"Update failed: {str(e)}")
            input(f"\n{GREEN}Press Enter to continue...{RESET}")

        else:
            warning = f"\n\t'{choice}' is not a valid menu option!\n"
            print(warning)
            time.sleep(2)

if __name__ == '__main__':
    main()