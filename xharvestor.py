#!/bin/env python3
import shlex
import subprocess
import argparse
import sys
import time
import csv
from typing import List, Dict, Any

# Color setup
try:
    import colorama
    colorama.init(autoreset=True)
    GREEN = colorama.Fore.GREEN
    YELLOW = colorama.Fore.YELLOW
    RED = colorama.Fore.RED
    BLUE = colorama.Fore.BLUE
    MAGENTA = colorama.Fore.MAGENTA
    CYAN = colorama.Fore.CYAN
    RESET = colorama.Fore.RESET
except ImportError:
    # Fallback if colorama is not installed
    GREEN = YELLOW = RED = BLUE = MAGENTA = CYAN = RESET = ""

def banner() -> None:
    """Banner"""
    print(f"""{MAGENTA}
 _  _  _   _    __    ____  _  _  ____  ___  ____  _____  ____ 
( \/ )( )_( )  /__\  (  _ \( \/ )( ___)/ __)(_  _)(  _  )(  _ \\
 )  (  ) _ (  /(__)\  )   / \  /  )__) \__ \  )(   )(_)(  )   /
(_/\_)(_) (_)(__)(__)(_)\_)  \/  (____)(___/ (__) (_____)(_)\_)
    {RESET}""")
    print(f"{CYAN}>>> Extented Reconnaissance Toolkit For Pentesters <<<{RESET}")
def print_status(message: str) -> None:
    """Print status messages"""
    print(f"{GREEN}[+]{RESET} {message}")

def print_warning(message: str) -> None:
    """Print warning messages"""
    print(f"{YELLOW}[!]{RESET} {message}")

def print_error(message: str) -> None:
    """Print error messages"""
    print(f"{RED}[-]{RESET} {message}")


class WiFiModule:
    """WiFi reconnaissance module"""
    
    def __init__(self, interface: str) -> None:
        self.interface = interface
        self.monitor_interface = f"{interface}mon"
        self.scan_results = []
    
    def setup_monitor_mode(self) -> str:
        """Put wireless interface into monitor mode"""
        print_status(f"{YELLOW}Setting up monitor mode on {self.interface}{RESET}") 
        cmd = f"sudo ifconfig {self.interface} down && sudo iwconfig {self.interface} mode monitor && sudo ifconfig {self.interface} up && sudo airmon-ng check kill"
        output = subprocess.check_output(cmd, shell=True, text=True)
        if output:
            print(f'{GREEN}[+] Successfully set to monitor mode: {self.interface}!{RESET}')
        else:
            print('An error occured during change of mode!')
    
    def setup_manage_mode(self) -> str:
        print_status(f"{YELLOW}Setting sup manage mode on {self.interface}{RESET}")
        cmd = f"sudo ifconfig {self.interface} down && sudo iwconfig {self.interface} mode manage && sudo ifconfig {self.interface} up && sudo service NetworkManager restart"
        output = subprocess.check_output(cmd, shell=True, text=True)
        if output:
            print_status(f'{YELLOW}[+] Successfully set to manage mode: {self.interface}!{RESET}')
        else:
            print_error('An error occured during set of mode!')
    

if __name__ == '__main__':
    wifi = WiFiModule('wlo1')
    wifi.setup_monitor_mode()
    banner()
    wifi.setup_manage_mode()