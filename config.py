#!/usr/bin/env python3

import os
import sys
import platform
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


class PlatformDetector:
    """Platform detection utilities"""
    
    @staticmethod
    def get_platform() -> str:
        """Detect current platform"""
        system = platform.system().lower()
        
        # Check for Android/Termux
        if 'ANDROID_DATA' in os.environ or 'ANDROID_ROOT' in os.environ:
            return 'android'
        
        # Check for other platforms
        if system == 'linux':
            return 'linux'
        elif system == 'windows':
            return 'windows'
        elif system == 'darwin':
            return 'macos'
        else:
            return 'unknown'
    
    @staticmethod
    def is_termux() -> bool:
        """Check if running in Termux environment"""
        return ('TERMUX_VERSION' in os.environ or 
                'PREFIX' in os.environ and '/data/data/com.termux' in os.environ.get('PREFIX', ''))
    
    @staticmethod
    def is_root_required() -> bool:
        """Check if root privileges are required for current platform"""
        platform_name = PlatformDetector.get_platform()
        # Android/Termux usually doesn't need root for basic operations
        return platform_name not in ['android', 'windows']


class Config:
    """Main configuration class with cross-platform support"""
    
    # Application metadata
    APP_NAME = "xharvester"
    VERSION = "1.0"
    AUTHOR = f"N3twork({Colors.RED}G{Colors.YELLOW}H{Colors.GREEN}A{Colors.BLACK}N{Colors.RED}A{Colors.GREEN}) {Colors.YELLOW}- {Colors.RED}Computer Hacker {Colors.YELLOW}&{Colors.GREEN} Programmer"
    GITHUB = "@n3twork5"
    GITHUB_REPO = "n3twork5/xharvester"
    GITHUB_API_URL = f"https://api.github.com/repos/n3twork5/xharvester"
    GITHUB_REPO_URL = f"https://github.com/n3twork5/xharvester.git"
    DONATION_URL = "https://ko-fi.com/n3twork"
    
    # Platform detection
    CURRENT_PLATFORM = PlatformDetector.get_platform()
    IS_TERMUX = PlatformDetector.is_termux()
    
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
    
    # Platform-specific settings
    PLATFORM_SETTINGS = {
        'linux': {
            'can_interfaces': ["vcan0", "can0", "can1", "slcan0"],
            'require_root': True,
            'package_manager': 'apt',
            'shell_commands': True
        },
        'android': {
            'can_interfaces': ["vcan0"],  # Limited CAN support
            'require_root': False,  # Termux doesn't require root
            'package_manager': 'pkg',
            'shell_commands': True
        },
        'windows': {
            'can_interfaces': ["vcan0"],
            'require_root': False,  # Windows uses different privilege model
            'package_manager': None,
            'shell_commands': True
        },
        'macos': {
            'can_interfaces': ["vcan0", "can0"],
            'require_root': True,
            'package_manager': 'brew',
            'shell_commands': True
        }
    }
    
    # Security settings
    REQUIRE_ROOT = PLATFORM_SETTINGS.get(CURRENT_PLATFORM, {}).get('require_root', True)
    MAX_INPUT_LENGTH = 1024
    ALLOWED_CAN_INTERFACES = PLATFORM_SETTINGS.get(CURRENT_PLATFORM, {}).get('can_interfaces', ["vcan0"])
    
    # Update settings
    UPDATE_CHECK_INTERVAL = 86400  # 24 hours in seconds
    AUTO_UPDATE = False  # Disabled until first release is published
    BACKUP_COUNT = 3  # Number of backups to keep
    UPDATE_TIMEOUT = 300  # 5 minutes timeout for updates
    
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
            f"{Colors.WHITE}  Created by{Colors.GREEN} {cls.AUTHOR}\t\t\t\n"
            f"{Colors.RED} Use only for authorized security testing!{Colors.RESET}"
        )


class MenuConfig:
    """Menu configuration constants"""
    
    MAIN_MENU_OPTIONS = {
        "1": "BlueTooth",
        "2": "Wi-Fi",
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
        "0": "Return to Main Menu"
    }
    
    MENU_DECORATORS = {
        "top": f"{Colors.LIGHTCYAN_EX}  ⇇━━━━━━━━━━━━━━━━━━━━━━━━୨ৎ━━━━━━━━━━━━━━━━━━━━━━━━━⇉",
        "bottom": f"{Colors.LIGHTCYAN_EX}  ⇇━━━━━━━━━━━━━━━━━━━━━━━━୨ৎ━━━━━━━━━━━━━━━━━━━━━━━━━⇉",
        "title_prefix": f"{Colors.LIGHTCYAN_EX} ︻芫═─── {Colors.RED}💥 {Colors.YELLOW}(▀̿Ĺ̯▀̿ ̿)",
        "prompt_icon": f"{Colors.CYAN}[{Colors.MAGENTA}💀{Colors.CYAN}]"
    }


# Initialize directories on import
Config.ensure_directories()