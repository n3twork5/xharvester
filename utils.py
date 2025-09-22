#!/usr/bin/env python3
"""
Utilities module for xharvester
Common functions, animations, input validation, and helper utilities
"""

import os
import re
import sys
import time
import socket
import logging
import logging.handlers
from datetime import datetime
from typing import Optional, Union, List, Any
from contextlib import contextmanager

from config import Colors, Config


class SecurityError(Exception):
    """Custom exception for security-related errors"""
    pass


class InputValidator:
    """Input validation utilities"""
    
    @staticmethod
    def validate_integer(value: str, min_val: int = 0, max_val: int = float('inf')) -> int:
        """
        Validate and convert string to integer within specified range
        
        Args:
            value: Input string to validate
            min_val: Minimum allowed value
            max_val: Maximum allowed value
            
        Returns:
            Validated integer value
            
        Raises:
            ValueError: If validation fails
        """
        if len(value) > Config.MAX_INPUT_LENGTH:
            raise ValueError("Input too long")
        
        try:
            int_val = int(value)
            if not (min_val <= int_val <= max_val):
                raise ValueError(f"Value must be between {min_val} and {max_val}")
            return int_val
        except ValueError as e:
            raise ValueError(f"Invalid integer: {e}")
    
    @staticmethod
    def validate_hex(value: str) -> int:
        """
        Validate hexadecimal input
        
        Args:
            value: Input string (can start with 0x or not)
            
        Returns:
            Integer value of hex
            
        Raises:
            ValueError: If not valid hex
        """
        if len(value) > Config.MAX_INPUT_LENGTH:
            raise ValueError("Input too long")
        
        try:
            # Remove 0x prefix if present
            clean_value = value.strip().lower()
            if clean_value.startswith('0x'):
                clean_value = clean_value[2:]
            
            return int(clean_value, 16)
        except ValueError:
            raise ValueError("Invalid hexadecimal value")
    
    @staticmethod
    def validate_can_interface(interface: str) -> str:
        """
        Validate CAN interface name
        
        Args:
            interface: Interface name to validate
            
        Returns:
            Validated interface name
            
        Raises:
            SecurityError: If interface not allowed
        """
        if not Config.validate_can_interface(interface):
            raise SecurityError(f"CAN interface '{interface}' not allowed")
        return interface
    
    @staticmethod
    def sanitize_input(value: str) -> str:
        """
        Sanitize user input by removing potentially dangerous characters
        
        Args:
            value: Input to sanitize
            
        Returns:
            Sanitized input
        """
        if len(value) > Config.MAX_INPUT_LENGTH:
            raise ValueError("Input too long")
        
        # Remove control characters and limit to printable ASCII
        sanitized = re.sub(r'[^\x20-\x7e]', '', value.strip())
        return sanitized


class Animation:
    """Animation utilities for terminal output"""
    
    @staticmethod
    def typewriter_text(text: str, speed: float = Config.ANIMATION_SPEED) -> None:
        """
        Display text with typewriter animation
        
        Args:
            text: Text to display
            speed: Animation speed (delay between characters)
        """
        for char in text:
            print(char, end='', flush=True)
            time.sleep(speed)
    
    @staticmethod
    def typewriter_line(text: str, speed: float = Config.MENU_ANIMATION_SPEED) -> None:
        """
        Display text line with typewriter animation and newline
        
        Args:
            text: Text to display
            speed: Animation speed
        """
        Animation.typewriter_text(text + '\n', speed)
    
    @staticmethod
    def display_banner() -> None:
        """Display the application banner with animation"""
        Animation.typewriter_text(Config.get_banner_text())
        print(Config.get_tagline())
        print(Config.get_credits())
    
    @staticmethod
    def show_loading(message: str, duration: int = 3) -> None:
        """
        Show loading animation with message
        
        Args:
            message: Loading message
            duration: Duration in seconds
        """
        print(f"{Colors.INFO}{message}", end="")
        for _ in range(duration):
            for dot in "...":
                print(dot, end="", flush=True)
                time.sleep(0.3)
            print("\b\b\b   \b\b\b", end="", flush=True)
        print(f"{Colors.SUCCESS} Done!{Colors.RESET}")


class SystemUtils:
    """System utilities and checks"""
    
    @staticmethod
    def check_root_privileges() -> bool:
        """Check if running with root privileges"""
        return os.geteuid() == 0
    
    @staticmethod
    def get_hostname() -> str:
        """Get system hostname safely"""
        try:
            return socket.gethostname()
        except Exception:
            return "unknown"
    
    @staticmethod
    def clear_screen() -> None:
        """Clear terminal screen"""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    @staticmethod
    def ensure_root() -> None:
        """Ensure application is running with root privileges"""
        if Config.REQUIRE_ROOT and not SystemUtils.check_root_privileges():
            error_msg = f"{Colors.WARNING}Please run {Config.APP_NAME} with administrator/root privileges!{Colors.RESET}"
            Animation.typewriter_line(error_msg)
            sys.exit(1)
    
    @staticmethod
    def safe_exit(message: str = "Exiting...", code: int = 0) -> None:
        """Safe application exit with message"""
        Animation.typewriter_line(f"{Colors.INFO}{message}{Colors.RESET}")
        sys.exit(code)


class MenuRenderer:
    """Menu rendering utilities"""
    
    @staticmethod
    def render_menu_header(title: str) -> None:
        """
        Render menu header with decorations
        
        Args:
            title: Menu title
        """
        from config import MenuConfig
        
        print(f"\n\t\t{MenuConfig.MENU_DECORATORS['title_prefix']}\t\t\t\n")
        print(MenuConfig.MENU_DECORATORS['top'])
        print(f"{Colors.GREEN}         {Colors.LIGHTCYAN_EX}🚀{Colors.GREEN}   {title}   {Colors.LIGHTCYAN_EX}🕷{Colors.GREEN}")
        print(MenuConfig.MENU_DECORATORS['bottom'])
    
    @staticmethod
    def render_menu_options(options: dict, icons: dict = None) -> None:
        """
        Render menu options with optional icons
        
        Args:
            options: Dictionary of option_key: option_name
            icons: Optional dictionary of option_key: icon
        """
        if icons is None:
            icons = {}
        
        for key, name in options.items():
            icon = icons.get(key, "")
            if key == "0":
                print(f"{Colors.CYAN}\t [{Colors.RED}{key}{Colors.CYAN}]{Colors.RED} ✗ {name}")
            elif key == "99":
                print(f"{Colors.CYAN}\t[{Colors.YELLOW}{key}{Colors.CYAN}]{Colors.YELLOW} 🎁 {name}")
            else:
                print(f"{Colors.CYAN}\t[{Colors.WHITE}{key}{Colors.CYAN}]{Colors.BLUE} {icon} {Colors.CYAN}{name}")
    
    @staticmethod
    def render_menu_footer() -> None:
        """Render menu footer"""
        from config import MenuConfig
        print(MenuConfig.MENU_DECORATORS['bottom'])
    
    @staticmethod
    def get_user_input(hostname: str) -> str:
        """
        Get user input with styled prompt
        
        Args:
            hostname: System hostname for prompt
            
        Returns:
            User input string
        """
        from config import MenuConfig
        
        prompt = (
            f"\n  {MenuConfig.MENU_DECORATORS['prompt_icon']} "
            f"{Colors.GREEN}{Config.APP_NAME}{Colors.YELLOW}@{Colors.CYAN}{hostname}{Colors.RED}:"
            f"{Colors.GREEN}~{Colors.YELLOW}$ {Colors.RESET}"
        )
        return input(prompt)


class Logger:
    """Enhanced logging utilities"""
    
    _loggers = {}
    
    @classmethod
    def get_logger(cls, name: str) -> logging.Logger:
        """
        Get or create logger instance
        
        Args:
            name: Logger name
            
        Returns:
            Configured logger instance
        """
        if name not in cls._loggers:
            logger = logging.getLogger(name)
            logger.setLevel(getattr(logging, Config.LOG_LEVEL))
            
            # Console handler
            console_handler = logging.StreamHandler()
            console_handler.setLevel(logging.WARNING)
            console_formatter = logging.Formatter('%(levelname)s: %(message)s')
            console_handler.setFormatter(console_formatter)
            
            # File handler
            file_handler = logging.handlers.RotatingFileHandler(
                Config.LOGS_DIR / f"{name}.log",
                maxBytes=Config.MAX_LOG_SIZE,
                backupCount=Config.LOG_BACKUP_COUNT
            )
            file_handler.setLevel(getattr(logging, Config.LOG_LEVEL))
            file_formatter = logging.Formatter(Config.LOG_FORMAT)
            file_handler.setFormatter(file_formatter)
            
            logger.addHandler(console_handler)
            logger.addHandler(file_handler)
            cls._loggers[name] = logger
        
        return cls._loggers[name]


@contextmanager
def error_handler(operation: str, logger: logging.Logger = None):
    """
    Context manager for graceful error handling
    
    Args:
        operation: Description of operation being performed
        logger: Optional logger instance
    """
    try:
        yield
    except KeyboardInterrupt:
        message = f"\n{Colors.WARNING}Operation '{operation}' cancelled by user{Colors.RESET}"
        if logger:
            logger.info(f"Operation '{operation}' cancelled by user")
        Animation.typewriter_line(message)
    except Exception as e:
        message = f"\n{Colors.ERROR}Error in '{operation}': {str(e)}{Colors.RESET}"
        if logger:
            logger.error(f"Error in '{operation}': {str(e)}", exc_info=True)
        Animation.typewriter_line(message)


def get_current_timestamp() -> str:
    """Get formatted current timestamp"""
    return datetime.now().strftime(f"%d/%m/%Y {Colors.WHITE}Time:{Colors.RESET}{Colors.MAGENTA} %H:%M")


def create_about_text() -> str:
    """Create the about section text"""
    return f"""
{Colors.RED}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
{Colors.WHITE}Bio: {Colors.RESET}
{Colors.MAGENTA}     I am a 19-year-old skilled hacker and programmer with expertise in ICS/SCADA security,
{Colors.MAGENTA}     Wireless exploitation (Wi-Fi/Bluetooth/RF) & Automotive systems hacking.
{Colors.RED}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
{Colors.WHITE}Tag Lines: {Colors.RESET}
{Colors.LIGHTCYAN_EX}    * {Colors.MAGENTA}Coding Is My Weapon, Hacking Is My Art
{Colors.LIGHTCYAN_EX}    * {Colors.MAGENTA}I Craft Backdoors & Close Loopholes
{Colors.LIGHTCYAN_EX}    * {Colors.MAGENTA}I Hack To Protect, Not To Destroy
{Colors.LIGHTCYAN_EX}    * {Colors.MAGENTA}I Love Crafting Backdoors{Colors.CYAN} 🚪
{Colors.LIGHTCYAN_EX}    * {Colors.MAGENTA}Breaking Systems, Building Knowledge  
{Colors.LIGHTCYAN_EX}    * {Colors.MAGENTA}Pseudo Code: Print 'Our Democracy Has Been Hacked'
{Colors.LIGHTCYAN_EX}    * {Colors.MAGENTA}Plant Backdoors, Gain Power
{Colors.LIGHTCYAN_EX}    * {Colors.MAGENTA}When We Lose Our Principles, We Invite Chaos
{Colors.LIGHTCYAN_EX}    * {Colors.MAGENTA}The Quieter You Become, The More You Are Able To Hear
{Colors.RED}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
{Colors.WHITE}About: {Colors.RESET}
{Colors.MAGENTA}      {Config.APP_NAME} is a specialized,{Colors.RESET}
{Colors.MAGENTA}      modular Python-based reconnaissance and exploitation suite designed for security assessments of radio frequency (RF),{Colors.RESET}
{Colors.MAGENTA}      wireless (bluetooth & wifi), industrial control system (SCADA), and automotive systems.{Colors.RESET}
{Colors.MAGENTA}      It integrates multiple tools and scripts into a unified workflow for probing,{Colors.RESET}
{Colors.MAGENTA}      analyzing, and documenting findings from the physical and wireless world.{Colors.RESET}
{Colors.RED}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
{Colors.WHITE}Version: {Colors.RESET}{Colors.MAGENTA}{Config.VERSION}{Colors.RESET}
{Colors.WHITE}Date: {Colors.RESET}{Colors.MAGENTA}{get_current_timestamp()}
{Colors.RED}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""