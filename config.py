#!/usr/bin/env python3
"""
Configuration management for xharvester
Centralizes all settings, colors, and constants
"""

import os
from pathlib import Path
from typing import Dict, Any

class Colors:
    """ANSI color codes for terminal output"""
    WHITE = '\033[37m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    RED = '\033[31m'
    BLUE = '\033[34m'
    MAGENTA = '\033[35m'
    CYAN = '\033[36m'
    LIGHTCYAN_EX = '\033[96m'
    BLACK = '\x1b[30m'
    RESET = '\033[0m'
    
    # Semantic colors for better code readability
    SUCCESS = GREEN
    WARNING = YELLOW
    ERROR = RED
    INFO = CYAN
    HIGHLIGHT = MAGENTA


class Config:
    """Main configuration class"""
    
    # Application metadata
    APP_NAME = "xharvester"
    VERSION = "2.0"
    AUTHOR = "Network(GHANA)"
    GITHUB = "@n3tworkh4x"
    DONATION_URL = "https://ko-fi.com/n3twork"
    
    # Animation settings
    ANIMATION_SPEED = 0.005
    MENU_ANIMATION_SPEED = 0.05
    
    # CAN Bus settings
    DEFAULT_CAN_INTERFACE = "vcan0"
    CAN_TIMEOUT = 0.08
    DEFAULT_FLOOD_DURATION = 5
    DEFAULT_MONITOR_DURATION = 0  # 0 for continuous
    
    # ICSim CAN IDs - Instrument Cluster Simulator specific
    ICSIM_CAN_IDS = {
        "Speed": 0x244,
        "RPM": 0x201,
        "Turn_Signals": 0x2C0,
        "Doors": 0x19B,
        "Lights": 0x2E0,
        "Engine": 0x2D0
    }
    
    # Flood attack settings
    FLOOD_RATES = {
        "high": 1000,
        "medium": 100,
        "low": 10
    }
    
    # Input validation limits
    MAX_SPEED = 255
    MAX_RPM = 8000
    MIN_FLOOD_DURATION = 1
    MAX_FLOOD_DURATION = 60
    
    # File paths
    PROJECT_ROOT = Path(__file__).parent
    LOGS_DIR = PROJECT_ROOT / "logs"
    MODULES_DIR = PROJECT_ROOT / "modules"
    
    # Logging configuration
    LOG_LEVEL = "INFO"
    LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    MAX_LOG_SIZE = 10 * 1024 * 1024  # 10MB
    LOG_BACKUP_COUNT = 5
    
    # Security settings
    REQUIRE_ROOT = True
    MAX_INPUT_LENGTH = 1024
    ALLOWED_CAN_INTERFACES = ["vcan0", "can0", "can1", "slcan0"]
    
    @classmethod
    def ensure_directories(cls):
        """Create necessary directories if they don't exist"""
        cls.LOGS_DIR.mkdir(exist_ok=True)
        cls.MODULES_DIR.mkdir(exist_ok=True)
    
    @classmethod
    def validate_can_interface(cls, interface: str) -> bool:
        """Validate CAN interface name"""
        return interface in cls.ALLOWED_CAN_INTERFACES
    
    @classmethod
    def get_banner_text(cls) -> str:
        """Return the ASCII banner"""
        return f"""{Colors.MAGENTA}
 _  _  _   _    __    ____  _  _  ____  ___  ____  ____  ____ {Colors.RED}
( \\/ )( )_( )  /__\\  (  _ \\( \\/ )( ___)/ __)(_  _)( ___)(  _ \\{Colors.MAGENTA}
 )  (  ) _ (  /(__)\\  )   / \\  /  )__) \\__ \\  )(   )__)  )   /{Colors.RED}
(_/\\_)(_) (_)(__)(__)(_)\\_)  \\/  (____)(___/ (__) (____)(_)\\_)
    {Colors.RESET}"""
    
    @classmethod
    def get_tagline(cls) -> str:
        """Return the application tagline"""
        return f"{Colors.CYAN} >>> Extended Reconnaissance & Exploitation Toolkit For Newbies <<<{Colors.RESET}"
    
    @classmethod
    def get_credits(cls) -> str:
        """Return credits information"""
        return (
            f"{Colors.GREEN}| GitHub:{Colors.RESET}{Colors.YELLOW} {cls.GITHUB} |{Colors.RESET}"
            f"{Colors.MAGENTA} Ko-fi{Colors.YELLOW}(Donation):{Colors.RESET}{Colors.GREEN} {cls.DONATION_URL} |\n"
            f"\t\t{Colors.WHITE}Created by{Colors.GREEN} {cls.AUTHOR}\t\t\t\n"
            f"{Colors.RED} Use only for authorized security testing!{Colors.RESET}"
        )


class MenuConfig:
    """Menu configuration constants"""
    
    MAIN_MENU_OPTIONS = {
        "1": "BlueTooth",
        "2": "Wifi", 
        "3": "Automobile",
        "4": "Radio Frequency",
        "5": "Industrial Control System - SCADA",
        "6": "About",
        "0": "Exit",
        "99": "Update XHARVESTER"
    }
    
    AUTOMOBILE_MENU_OPTIONS = {
        "1": "CAN Message Injection",
        "2": "ECU Firmware Attack",
        "3": "Wireless Gateway Exploit", 
        "4": "Sensor Spoofing",
        "5": "CAN Bus Flood",
        "6": "Real-time CAN Monitor",
        "0": "Back"
    }
    
    MENU_DECORATORS = {
        "top": f"{Colors.LIGHTCYAN_EX}  ⇇━━━━━━━━━━━━━━━━━━━━━━━━୨ৎ━━━━━━━━━━━━━━━━━━━━━━━━━⇉",
        "bottom": f"{Colors.LIGHTCYAN_EX}  ⇇━━━━━━━━━━━━━━━━━━━━━━━━୨ৎ━━━━━━━━━━━━━━━━━━━━━━━━━⇉",
        "title_prefix": f"{Colors.LIGHTCYAN_EX} ︻芫═─── {Colors.RED}💥 {Colors.YELLOW}(▀̿Ĺ̯▀̿ ̿)",
        "prompt_icon": f"{Colors.CYAN}[{Colors.MAGENTA}💀{Colors.CYAN}]"
    }


# Initialize directories on import
Config.ensure_directories()