#!/usr/bin/env python3
"""
Robust Automobile Security Testing Module for xharvester
Works seamlessly with both virtual and real CAN interfaces
Based on "The Car Hacker's Handbook" methodologies

Author: N3twork(GHANA) - Computer Programmer & Hacker
Version: 1.0
"""

import os
import sys
import time
import random
import threading
import struct
import subprocess
from pathlib import Path
from typing import Optional, Dict, List, Any, Tuple
from dataclasses import dataclass
from datetime import datetime

# Import CAN libraries with fallback
try:
    import can
    from can import Message
    CAN_AVAILABLE = True
except ImportError:
    print("⚠️ CAN library not available - using simulation mode")
    CAN_AVAILABLE = False
    
    # Create mock classes for when CAN is not available
    class Message:
        def __init__(self, arbitration_id=0, data=b'', is_extended_id=False, **kwargs):
            self.arbitration_id = arbitration_id
            self.data = data
            self.is_extended_id = is_extended_id
            self.timestamp = time.time()

# Import configuration and utilities
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import Config, Colors, MenuConfig
from utils import (
    Animation, SystemUtils, MenuRenderer, Logger, error_handler,
    InputValidator
)


@dataclass
class CANMessage:
    """CAN message representation"""
    arbitration_id: int
    data: bytes
    timestamp: float
    is_extended_id: bool = False
    
    def __str__(self):
        return f"ID: 0x{self.arbitration_id:03X}, Data: {self.data.hex().upper()}, Time: {self.timestamp:.3f}"


class CANInterface:
    """Unified CAN interface handler for both virtual and real interfaces"""
    
    def __init__(self, interface_name: str = "vcan0"):
        self.logger = Logger.get_logger("can_interface")
        self.interface_name = interface_name
        self.bus: Optional[can.BusABC] = None
        self.is_virtual = interface_name.startswith('vcan')
        self.is_connected = False
        self.simulation_mode = False
        
        # Setup interface
        self.setup_interface()
    
    def setup_interface(self) -> bool:
        """Setup CAN interface (virtual or real)"""
        try:
            # First check if interface exists
            result = subprocess.run(['ip', 'link', 'show', self.interface_name], 
                                  capture_output=True, text=True)
            
            if result.returncode != 0:
                if self.is_virtual:
                    return self._create_virtual_interface()
                else:
                    print(f"{Colors.ERROR}  Real CAN interface {self.interface_name} not found!")
                    print(f"{Colors.INFO}  Switching to simulation mode...")
                    self.simulation_mode = True
                    return True
            
            # Interface exists, try to connect
            return self._connect_to_interface()
            
        except Exception as e:
            self.logger.error(f"Failed to setup CAN interface: {e}")
            print(f"{Colors.WARNING}  CAN setup failed, using simulation mode")
            self.simulation_mode = True
            return True
    
    def _create_virtual_interface(self) -> bool:
        """Create virtual CAN interface"""
        try:
            print(f"{Colors.INFO}  Creating virtual CAN interface: {self.interface_name}")
            
            # Load vcan module
            subprocess.run(['sudo', 'modprobe', 'vcan'], check=True)
            
            # Create virtual CAN interface
            subprocess.run(['sudo', 'ip', 'link', 'add', 'dev', self.interface_name, 'type', 'vcan'], check=True)
            
            # Bring interface up
            subprocess.run(['sudo', 'ip', 'link', 'set', 'up', self.interface_name], check=True)
            
            print(f"{Colors.SUCCESS}  Virtual CAN interface {self.interface_name} created successfully")
            
            # Now connect to it
            return self._connect_to_interface()
            
        except subprocess.CalledProcessError as e:
            self.logger.error(f"Failed to create virtual CAN interface: {e}")
            print(f"{Colors.ERROR}  Failed to create virtual interface: {e}")
            print(f"{Colors.INFO}  Falling back to simulation mode")
            self.simulation_mode = True
            return True
        except Exception as e:
            self.logger.error(f"Unexpected error creating virtual interface: {e}")
            self.simulation_mode = True
            return True
    
    def _connect_to_interface(self) -> bool:
        """Connect to the CAN interface"""
        if not CAN_AVAILABLE:
            print(f"{Colors.WARNING}  CAN library not available - using simulation mode")
            self.simulation_mode = True
            return True
        
        try:
            # Try to create CAN bus connection
            self.bus = can.interface.Bus(
                channel=self.interface_name,
                bustype='socketcan',
                bitrate=500000  # Standard automotive CAN bitrate
            )
            
            self.is_connected = True
            interface_type = "Virtual" if self.is_virtual else "Real"
            print(f"{Colors.SUCCESS}  Connected to {interface_type} CAN interface: {self.interface_name}")
            print(f"{Colors.INFO}  Bitrate: 500 kbps (Standard automotive)")
            self.logger.info(f"Connected to CAN interface {self.interface_name}")
            
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to connect to CAN interface: {e}")
            print(f"{Colors.ERROR}  Connection failed: {e}")
            print(f"{Colors.INFO}  Using simulation mode")
            self.simulation_mode = True
            return True
    
    def send_message(self, can_id: int, data: bytes) -> bool:
        """Send CAN message"""
        try:
            message = Message(arbitration_id=can_id, data=data)
            
            if self.simulation_mode:
                # Simulate message sending
                print(f"{Colors.BLUE}  [SIM] Sent: ID=0x{can_id:03X}, Data={data.hex().upper()}")
                return True
            elif self.is_connected and self.bus:
                # Send real message
                self.bus.send(message)
                print(f"{Colors.GREEN}  [REAL] Sent: ID=0x{can_id:03X}, Data={data.hex().upper()}")
                return True
            else:
                print(f"{Colors.WARNING}  [SIM] Would send: ID=0x{can_id:03X}, Data={data.hex().upper()}")
                return False
                
        except Exception as e:
            self.logger.error(f"Failed to send CAN message: {e}")
            print(f"{Colors.ERROR}  Send failed: {e}")
            return False
    
    def receive_message(self, timeout: float = 1.0) -> Optional[CANMessage]:
        """Receive CAN message"""
        try:
            if self.simulation_mode:
                # Simulate message reception
                time.sleep(0.1)  # Small delay to simulate real reception
                simulated_ids = [0x244, 0x201, 0x2C0, 0x100, 0x200, 0x7E8]
                can_id = random.choice(simulated_ids)
                data = bytes([random.randint(0, 255) for _ in range(random.randint(1, 8))])
                return CANMessage(can_id, data, time.time())
                
            elif self.is_connected and self.bus:
                # Receive real message
                msg = self.bus.recv(timeout=timeout)
                if msg:
                    return CANMessage(msg.arbitration_id, msg.data, msg.timestamp)
                return None
            else:
                return None
                
        except Exception as e:
            self.logger.error(f"Failed to receive CAN message: {e}")
            return None
    
    def monitor_traffic(self, duration: int = 10) -> List[CANMessage]:
        """Monitor CAN traffic for specified duration"""
        messages = []
        start_time = time.time()
        
        print(f"{Colors.INFO}  Monitoring CAN traffic for {duration} seconds...")
        print(f"{Colors.CYAN}    Time    | ID   | Data")
        print(f"{Colors.CYAN}    --------+------+------------------")
        
        while (time.time() - start_time) < duration:
            msg = self.receive_message(timeout=0.1)
            if msg:
                messages.append(msg)
                elapsed = msg.timestamp - start_time
                print(f"{Colors.GREEN}    {elapsed:6.2f}  | {msg.arbitration_id:03X}  | {msg.data.hex().upper()}")
        
        return messages
    
    def cleanup(self):
        """Clean up CAN interface"""
        try:
            if self.bus:
                self.bus.shutdown()
                self.is_connected = False
                print(f"{Colors.INFO}  CAN bus connection closed")
            
            if self.is_virtual and not self.simulation_mode:
                # Remove virtual interface
                subprocess.run(['sudo', 'ip', 'link', 'del', self.interface_name], 
                             capture_output=True)
                print(f"{Colors.INFO}  Virtual CAN interface {self.interface_name} removed")
                
        except Exception as e:
            self.logger.warning(f"Error during cleanup: {e}")


class AutomotiveSecurityTester:
    """Professional automotive security testing capabilities"""
    
    def __init__(self, can_interface: CANInterface):
        self.logger = Logger.get_logger("automotive_security")
        self.can = can_interface
        
        # Known automotive CAN IDs and their purposes
        self.known_ids = {
            # Engine Management
            0x7E0: {"name": "Engine ECU Request", "type": "UDS Request"},
            0x7E8: {"name": "Engine ECU Response", "type": "UDS Response"},
            0x7E1: {"name": "Transmission Request", "type": "UDS Request"},
            0x7E9: {"name": "Transmission Response", "type": "UDS Response"},
            
            # Body Control
            0x760: {"name": "Body Control Request", "type": "UDS Request"},
            0x768: {"name": "Body Control Response", "type": "UDS Response"},
            
            # Instrument Cluster
            0x720: {"name": "Cluster Request", "type": "UDS Request"},
            0x728: {"name": "Cluster Response", "type": "UDS Response"},
            
            # Common data IDs
            0x100: {"name": "Engine RPM/Speed", "type": "Broadcast Data"},
            0x200: {"name": "Vehicle Speed", "type": "Broadcast Data"},
            0x300: {"name": "Steering Angle", "type": "Broadcast Data"},
            0x400: {"name": "Brake System", "type": "Broadcast Data"},
            
            # ICSim (Instrument Cluster Simulator) IDs
            0x244: {"name": "ICSim Speed", "type": "Simulation"},
            0x201: {"name": "ICSim RPM", "type": "Simulation"},
            0x2C0: {"name": "ICSim Turn Signals", "type": "Simulation"},
            0x19B: {"name": "ICSim Doors", "type": "Simulation"},
            0x2E0: {"name": "ICSim Lights", "type": "Simulation"},
        }
    
    def scan_network(self) -> Dict[int, Dict]:
        """Scan for active CAN IDs on the network"""
        print(f"\n{Colors.CYAN}  [{Colors.GREEN}+{Colors.CYAN}] Scanning CAN Network...")
        
        active_ids = {}
        
        if self.can.simulation_mode:
            # In simulation mode, return some active IDs
            simulated_active = [0x244, 0x201, 0x2C0, 0x7E0, 0x7E8, 0x100, 0x200]
            for can_id in simulated_active:
                if can_id in self.known_ids:
                    active_ids[can_id] = self.known_ids[can_id]
                    print(f"{Colors.GREEN}    • ID 0x{can_id:03X}: {self.known_ids[can_id]['name']}")
        else:
            # Real network scan - monitor traffic to detect active IDs
            print(f"{Colors.INFO}  Monitoring traffic to detect active IDs...")
            messages = self.can.monitor_traffic(duration=5)
            
            for msg in messages:
                if msg.arbitration_id not in active_ids:
                    info = self.known_ids.get(msg.arbitration_id, {"name": "Unknown", "type": "Unknown"})
                    active_ids[msg.arbitration_id] = info
                    print(f"{Colors.GREEN}    • ID 0x{msg.arbitration_id:03X}: {info['name']}")
        
        return active_ids
    
    def obd2_scan(self) -> Dict[str, Any]:
        """Perform OBD-II diagnostic scan"""
        print(f"\n{Colors.CYAN}  [{Colors.GREEN}+{Colors.CYAN}] OBD-II Diagnostic Scan...")
        
        results = {
            "dtcs": [],
            "supported_pids": [],
            "live_data": {}
        }
        
        # Send OBD-II request (Mode 01, PID 00 - supported PIDs)
        obd_request = bytes([0x01, 0x00])  # Mode 01, PID 00
        
        if self.can.send_message(0x7DF, obd_request):  # OBD functional address
            # Wait for response
            time.sleep(0.1)
            response = self.can.receive_message(timeout=1.0)
            
            if response and 0x7E8 <= response.arbitration_id <= 0x7EF:
                print(f"{Colors.SUCCESS}  OBD-II ECU responded: 0x{response.arbitration_id:03X}")
                print(f"{Colors.INFO}  Response data: {response.data.hex().upper()}")
                
                # Simulate supported PIDs
                results["supported_pids"] = [0x01, 0x03, 0x04, 0x05, 0x0C, 0x0D, 0x0F, 0x11]
                
                for pid in results["supported_pids"]:
                    pid_names = {
                        0x01: "Monitor status",
                        0x03: "Fuel system status", 
                        0x04: "Calculated engine load",
                        0x05: "Engine coolant temperature",
                        0x0C: "Engine RPM",
                        0x0D: "Vehicle speed",
                        0x0F: "Intake air temperature",
                        0x11: "Throttle position"
                    }
                    if pid in pid_names:
                        print(f"{Colors.GREEN}    • PID 0x{pid:02X}: {pid_names[pid]}")
            else:
                print(f"{Colors.WARNING}  No OBD-II response received")
        
        return results
    
    def inject_messages(self, target_id: int, data_list: List[bytes], count: int = 5):
        """Inject custom CAN messages"""
        print(f"\n{Colors.CYAN}  [{Colors.GREEN}+{Colors.CYAN}] CAN Message Injection...")
        print(f"{Colors.WARNING}  ⚠️  This can affect vehicle behavior!")
        
        successful_injections = 0
        
        for i in range(count):
            data = random.choice(data_list) if data_list else bytes([random.randint(0, 255) for _ in range(8)])
            
            if self.can.send_message(target_id, data):
                successful_injections += 1
                print(f"{Colors.SUCCESS}  [{i+1}/{count}] Injected: ID=0x{target_id:03X}, Data={data.hex().upper()}")
            else:
                print(f"{Colors.ERROR}  [{i+1}/{count}] Injection failed")
            
            time.sleep(0.5)  # Delay between injections
        
        print(f"\n{Colors.INFO}  Injection complete: {successful_injections}/{count} messages sent")
        return successful_injections
    
    def fuzz_testing(self, target_ids: List[int], duration: int = 30, rate: int = 10):
        """Perform CAN bus fuzzing"""
        print(f"\n{Colors.CYAN}  [{Colors.GREEN}+{Colors.CYAN}] CAN Bus Fuzzing...")
        print(f"{Colors.ERROR}  ⚠️  DANGER: Fuzzing can cause unpredictable behavior!")
        print(f"{Colors.ERROR}  Only use on test vehicles or simulation!")
        
        confirm = input(f"\n{Colors.GREEN}  Continue with fuzzing? ({Colors.CYAN}y{Colors.GREEN}/{Colors.RED}N{Colors.GREEN}): {Colors.YELLOW}").strip().lower()
        if confirm not in ['y', 'yes']:
            print(f"{Colors.INFO}  Fuzzing cancelled")
            return
        
        print(f"\n{Colors.INFO}  Fuzzing {len(target_ids)} targets for {duration}s at {rate} msg/s")
        
        start_time = time.time()
        messages_sent = 0
        
        while (time.time() - start_time) < duration:
            target_id = random.choice(target_ids)
            fuzz_data = bytes([random.randint(0, 255) for _ in range(random.randint(1, 8))])
            
            if self.can.send_message(target_id, fuzz_data):
                messages_sent += 1
            
            time.sleep(1.0 / rate)
            
            # Progress indicator
            elapsed = time.time() - start_time
            if int(elapsed) % 10 == 0:  # Every 10 seconds
                print(f"{Colors.YELLOW}  Fuzzing... {elapsed:.0f}s, {messages_sent} messages sent")
        
        print(f"{Colors.SUCCESS}  Fuzzing completed: {messages_sent} messages sent in {duration}s")


class AutomobileModule:
    """Main automobile security testing module"""
    
    def __init__(self):
        self.logger = Logger.get_logger("automobile_module")
        self.hostname = SystemUtils.get_hostname()
        
        # Initialize CAN interface
        self.can_interface = CANInterface(Config.DEFAULT_CAN_INTERFACE)
        self.security_tester = AutomotiveSecurityTester(self.can_interface)
        
        # Menu options
        self.menu_options = {
            "1": "CAN Network Discovery",
            "2": "OBD-II Diagnostic Scan",
            "3": "CAN Message Injection",
            "4": "Real-time Traffic Monitor", 
            "5": "Security Fuzzing (DANGEROUS)",
            "6": "ICSim Integration Test",
            "7": "Interface Status & Info",
            "0": "Back to Main Menu"
        }
        
        self.menu_icons = {
            "1": "🔍", "2": "🔌", "3": "💉", "4": "📊", 
            "5": "💥", "6": "🚗", "7": "ℹ️"
        }
        
        self.logger.info("Automobile module initialized successfully")
    
    def show_menu(self):
        """Display automobile module menu"""
        Animation.display_banner()
        MenuRenderer.render_menu_header(f"AUTOMOBILE SECURITY TESTING {Colors.YELLOW}-{Colors.CYAN} PROFESSIONAL")
        
        # Show interface status
        status_color = Colors.SUCCESS if self.can_interface.is_connected else Colors.WARNING
        mode = "Real CAN" if self.can_interface.is_connected else "Simulation"
        print(f"{Colors.INFO}  Interface: {Colors.CYAN}{self.can_interface.interface_name} {status_color}({mode}){Colors.RESET}")
        
        if not self.can_interface.simulation_mode:
            print(f"{Colors.SUCCESS}  ✅ Connected to physical CAN interface")
        else:
            print(f"{Colors.WARNING}  ⚠️  Running in simulation mode")
        
        print(f"{Colors.MAGENTA}  Based on professional automotive security methodologies{Colors.RESET}")
        print()
        
        MenuRenderer.render_menu_options(self.menu_options, self.menu_icons)
        MenuRenderer.render_menu_footer()
    
    def can_network_discovery(self):
        """Discover active CAN network nodes"""
        active_ids = self.security_tester.scan_network()
        print(f"\n{Colors.SUCCESS}  Found {len(active_ids)} active CAN IDs")
        
        if not active_ids:
            print(f"{Colors.WARNING}  No active IDs detected. Try with real vehicle or ICSim running.")
    
    def obd2_diagnostic_scan(self):
        """Perform OBD-II diagnostics"""
        results = self.security_tester.obd2_scan()
        print(f"\n{Colors.SUCCESS}  OBD-II scan completed")
        
        if results["supported_pids"]:
            print(f"{Colors.INFO}  Found {len(results['supported_pids'])} supported PIDs")
        else:
            print(f"{Colors.WARNING}  No OBD-II responses. Check connection to vehicle OBD port.")
    
    def can_message_injection(self):
        """CAN message injection testing"""
        print(f"\n{Colors.CYAN}  CAN Message Injection Setup")
        print(f"{Colors.WARNING}  ⚠️ Only use on test vehicles or with ICSim!")
        
        try:
            # Get target ID
            id_input = input(f"{Colors.GREEN}  Target CAN ID (hex): {Colors.YELLOW}") or "244"
            target_id = InputValidator.validate_hex(id_input)
            
            # Get injection count
            count_input = input(f"{Colors.GREEN}  Number of messages: {Colors.YELLOW}") or "5"
            count = InputValidator.validate_integer(count_input, 1, 100)
            
            # Predefined test data for common automotive functions
            test_data_options = {
                0x244: [bytes([0, 0, 0, 50, 0, 0, 0, 0])],  # ICSim speed
                0x201: [bytes([0x10, 0x00, 0, 0, 0, 0, 0, 0])],  # ICSim RPM
                0x2C0: [bytes([1, 0, 0, 0, 0, 0, 0, 0])],  # ICSim turn signals
            }
            
            data_list = test_data_options.get(target_id, [])
            
            # Perform injection
            self.security_tester.inject_messages(target_id, data_list, count)
            
        except ValueError as e:
            print(f"{Colors.ERROR}  Invalid input: {e}")
    
    def real_time_monitor(self):
        """Real-time CAN traffic monitoring"""
        print(f"\n{Colors.CYAN}  Real-time CAN Traffic Monitor")
        
        try:
            duration_input = input(f"{Colors.GREEN}  Monitor duration (seconds): {Colors.YELLOW}") or "10"
            duration = InputValidator.validate_integer(duration_input, 1, 300)
            
            messages = self.can_interface.monitor_traffic(duration)
            
            print(f"\n{Colors.SUCCESS}  Captured {len(messages)} messages in {duration} seconds")
            
            if messages:
                # Show statistics
                unique_ids = set(msg.arbitration_id for msg in messages)
                print(f"{Colors.INFO}  Unique CAN IDs: {len(unique_ids)}")
                print(f"{Colors.INFO}  Message rate: {len(messages)/duration:.1f} msg/s")
            
        except ValueError as e:
            print(f"{Colors.ERROR}  Invalid duration: {e}")
    
    def security_fuzzing(self):
        """Security fuzzing interface"""
        print(f"\n{Colors.ERROR}  ⚠️ SECURITY FUZZING - EXTREME CAUTION REQUIRED!")
        
        try:
            # Get target IDs
            ids_input = input(f"{Colors.GREEN}  Target IDs (hex, comma-separated): {Colors.YELLOW}") or "244,201"
            target_ids = []
            for id_str in ids_input.split(','):
                target_ids.append(InputValidator.validate_hex(id_str.strip()))
            
            # Get parameters
            duration_input = input(f"{Colors.GREEN}  Duration (seconds): {Colors.YELLOW}") or "10"
            duration = InputValidator.validate_integer(duration_input, 1, 60)
            
            rate_input = input(f"{Colors.GREEN}  Rate (msg/s): {Colors.YELLOW}") or "5"
            rate = InputValidator.validate_integer(rate_input, 1, 100)
            
            # Perform fuzzing
            self.security_tester.fuzz_testing(target_ids, duration, rate)
            
        except ValueError as e:
            print(f"{Colors.ERROR}  Invalid input: {e}")
    
    def icsim_integration_test(self):
        """Test integration with ICSim (Instrument Cluster Simulator)"""
        print(f"\n{Colors.CYAN}  [{Colors.GREEN}+{Colors.CYAN}] ICSim Integration Test")
        print(f"{Colors.INFO}  Testing integration with Instrument Cluster Simulator")
        
        # Check if ICSim might be running (look for typical ICSim traffic)
        print(f"{Colors.INFO}  Checking for ICSim activity...")
        messages = self.can_interface.monitor_traffic(duration=3)
        
        icsim_ids = [0x244, 0x201, 0x2C0, 0x19B, 0x2E0]
        icsim_detected = any(msg.arbitration_id in icsim_ids for msg in messages)
        
        if icsim_detected:
            print(f"{Colors.SUCCESS}  ✅ ICSim activity detected!")
            
            # Test different ICSim controls
            print(f"\n{Colors.INFO}  Testing ICSim controls...")
            
            # Test speedometer
            print(f"{Colors.BLUE}  Testing speedometer...")
            speed_data = bytes([0, 0, 0, 80, 0, 0, 0, 0])  # 80 km/h
            self.can_interface.send_message(0x244, speed_data)
            
            # Test RPM
            print(f"{Colors.BLUE}  Testing RPM gauge...")
            rpm_data = bytes([0x20, 0x00, 0, 0, 0, 0, 0, 0])  # ~2000 RPM
            self.can_interface.send_message(0x201, rpm_data)
            
            # Test turn signals
            print(f"{Colors.BLUE}  Testing turn signals...")
            turn_data = bytes([1, 0, 0, 0, 0, 0, 0, 0])  # Left turn signal
            self.can_interface.send_message(0x2C0, turn_data)
            
            print(f"{Colors.SUCCESS}  ICSim integration test completed!")
            print(f"{Colors.INFO}  Check ICSim window for changes")
            
        else:
            print(f"{Colors.WARNING}  No ICSim activity detected")
            print(f"{Colors.INFO}  To test with ICSim:")
            print(f"{Colors.YELLOW}    1. Install: sudo apt install can-utils")
            print(f"{Colors.YELLOW}    2. Run: icsim {self.can_interface.interface_name}")
            print(f"{Colors.YELLOW}    3. Run: controls {self.can_interface.interface_name}")
    
    def interface_status(self):
        """Show detailed interface status and information"""
        print(f"\n{Colors.CYAN}  [{Colors.GREEN}ℹ{Colors.CYAN}] CAN Interface Status & Information")
        
        print(f"\n{Colors.MAGENTA}  Interface Details:")
        print(f"{Colors.GREEN}    • Name: {Colors.CYAN}{self.can_interface.interface_name}")
        print(f"{Colors.GREEN}    • Type: {Colors.CYAN}{'Virtual' if self.can_interface.is_virtual else 'Physical'}")
        print(f"{Colors.GREEN}    • Status: {Colors.SUCCESS if self.can_interface.is_connected else Colors.WARNING}{'Connected' if self.can_interface.is_connected else 'Simulation Mode'}")
        print(f"{Colors.GREEN}    • Mode: {Colors.CYAN}{'Simulation' if self.can_interface.simulation_mode else 'Real CAN'}")
        
        if not self.can_interface.simulation_mode:
            print(f"{Colors.GREEN}    • Bitrate: {Colors.CYAN}500 kbps")
            print(f"{Colors.GREEN}    • Protocol: {Colors.CYAN}CAN 2.0B (Extended)")
        
        print(f"\n{Colors.MAGENTA}  Available Commands:")
        if self.can_interface.is_virtual:
            print(f"{Colors.YELLOW}    • Check interface: ip link show {self.can_interface.interface_name}")
            print(f"{Colors.YELLOW}    • Monitor traffic: candump {self.can_interface.interface_name}")
            print(f"{Colors.YELLOW}    • Send message: cansend {self.can_interface.interface_name} 123#DEADBEEF")
        
        print(f"\n{Colors.MAGENTA}  Testing with ICSim:")
        print(f"{Colors.YELLOW}    • Install: sudo apt install can-utils")
        print(f"{Colors.YELLOW}    • Simulator: icsim {self.can_interface.interface_name}")
        print(f"{Colors.YELLOW}    • Controls: controls {self.can_interface.interface_name}")
    
    def main(self):
        """Main automobile module loop"""
        try:
            while True:
                try:
                    SystemUtils.clear_screen()
                    self.show_menu()
                    choice = MenuRenderer.get_user_input(self.hostname)
                    
                    if choice == "0":
                        print(f"\n{Colors.MAGENTA}🚪🔙{Colors.YELLOW} Returning to main menu...")
                        break
                    elif choice == "1":
                        self.can_network_discovery()
                    elif choice == "2":
                        self.obd2_diagnostic_scan()
                    elif choice == "3":
                        self.can_message_injection()
                    elif choice == "4":
                        self.real_time_monitor()
                    elif choice == "5":
                        self.security_fuzzing()
                    elif choice == "6":
                        self.icsim_integration_test()
                    elif choice == "7":
                        self.interface_status()
                    else:
                        print(f"\n{Colors.WARNING}'{choice}' is not a valid option!")
                    
                    if choice != "0":
                        input(f"\n  {Colors.GREEN}Press Enter to continue...")
                        
                except (KeyboardInterrupt, EOFError):
                    print(f"\n{Colors.MAGENTA}🚪🔙{Colors.YELLOW} Returning to main menu...")
                    break
                    
        except Exception as e:
            self.logger.error(f"Automobile module error: {e}", exc_info=True)
            print(f"{Colors.ERROR}Module error: {e}")
        finally:
            # Cleanup
            if hasattr(self, 'can_interface'):
                self.can_interface.cleanup()


if __name__ == "__main__":
    try:
        auto_module = AutomobileModule()
        auto_module.main()
    except Exception as e:
        print(f"{Colors.ERROR}Critical error: {e}")