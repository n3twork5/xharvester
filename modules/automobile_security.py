#!/usr/bin/env python3
"""
Professional Automotive Security Testing Module for xharvester
Based on methodologies from "The Car Hacker's Handbook" by Craig Smith
Comprehensive vehicle security assessment framework

Author: Network(GHANA)
Version: 2.1 - Professional Edition
"""

import os
import sys
import time
import random
import threading
import struct
import binascii
from pathlib import Path
from typing import Optional, Dict, List, Any, Tuple, Union
from datetime import datetime, timedelta
from dataclasses import dataclass
from enum import Enum

import can
from can import CanError, Message

# Import configuration and utilities
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import Config, Colors, MenuConfig
from utils import (
    Animation, SystemUtils, MenuRenderer, Logger, error_handler,
    InputValidator, SecurityError
)


class CANBusProtocol(Enum):
    """CAN Bus protocol types"""
    CAN_20A = "CAN 2.0A (11-bit)"
    CAN_20B = "CAN 2.0B (29-bit)"  
    CAN_FD = "CAN FD"
    ISO_TP = "ISO-TP"
    UDS = "UDS (ISO 14229)"


class VehicleNetwork(Enum):
    """Vehicle network types"""
    CAN_HIGH_SPEED = "High-Speed CAN (ISO 11898-2)"
    CAN_LOW_SPEED = "Low-Speed CAN (ISO 11898-3)"
    LIN = "Local Interconnect Network"
    MOST = "Media Oriented Systems Transport"
    FLEXRAY = "FlexRay"
    ETHERNET = "Automotive Ethernet"


class OBD2Mode(Enum):
    """OBD-II service modes"""
    SHOW_CURRENT_DATA = 0x01
    SHOW_FREEZE_FRAME = 0x02
    SHOW_STORED_DTC = 0x03
    CLEAR_DTC = 0x04
    TEST_RESULTS = 0x05
    TEST_RESULTS_OTHER = 0x06
    SHOW_PENDING_DTC = 0x07
    CONTROL_OPERATION = 0x08
    REQUEST_VEHICLE_INFO = 0x09
    PERMANENT_DTC = 0x0A


@dataclass
class CANMessage:
    """CAN message structure"""
    arbitration_id: int
    data: bytes
    timestamp: float
    is_extended_id: bool = False
    is_error_frame: bool = False
    is_remote_frame: bool = False
    
    def __str__(self):
        return f"ID: 0x{self.arbitration_id:X}, Data: {self.data.hex().upper()}, Time: {self.timestamp:.6f}"


@dataclass
class ECUInfo:
    """ECU identification information"""
    ecu_id: str
    name: str
    supplier: str
    part_number: str
    software_version: str
    hardware_version: str
    can_ids: List[int]
    services: List[str]


class CANDatabase:
    """CAN message database and analysis"""
    
    def __init__(self):
        self.logger = Logger.get_logger("can_database")
        self.messages: List[CANMessage] = []
        self.unique_ids: Dict[int, List[CANMessage]] = {}
        self.id_frequencies: Dict[int, int] = {}
        
        # Known automotive CAN IDs (based on common implementations)
        self.known_ids = {
            # Engine Management
            0x7E0: {"name": "Engine ECU", "service": "UDS", "type": "Request"},
            0x7E8: {"name": "Engine ECU", "service": "UDS", "type": "Response"},
            0x7E1: {"name": "Transmission ECU", "service": "UDS", "type": "Request"},
            0x7E9: {"name": "Transmission ECU", "service": "UDS", "type": "Response"},
            
            # Body Control
            0x760: {"name": "Body Control Module", "service": "UDS", "type": "Request"},
            0x768: {"name": "Body Control Module", "service": "UDS", "type": "Response"},
            
            # Instrument Cluster
            0x720: {"name": "Instrument Cluster", "service": "UDS", "type": "Request"},
            0x728: {"name": "Instrument Cluster", "service": "UDS", "type": "Response"},
            
            # Common broadcast IDs
            0x100: {"name": "Engine RPM/Speed", "service": "Broadcast", "type": "Data"},
            0x200: {"name": "Vehicle Speed", "service": "Broadcast", "type": "Data"},
            0x300: {"name": "Steering Wheel", "service": "Broadcast", "type": "Data"},
            0x400: {"name": "Brake System", "service": "Broadcast", "type": "Data"},
            
            # ICSim specific IDs
            0x244: {"name": "ICSim Speed", "service": "Simulation", "type": "Data"},
            0x201: {"name": "ICSim RPM", "service": "Simulation", "type": "Data"},
            0x2C0: {"name": "ICSim Turn Signals", "service": "Simulation", "type": "Data"},
            0x19B: {"name": "ICSim Doors", "service": "Simulation", "type": "Data"},
            0x2E0: {"name": "ICSim Lights", "service": "Simulation", "type": "Data"},
        }
    
    def add_message(self, msg: CANMessage):
        """Add a CAN message to the database"""
        self.messages.append(msg)
        
        if msg.arbitration_id not in self.unique_ids:
            self.unique_ids[msg.arbitration_id] = []
        self.unique_ids[msg.arbitration_id].append(msg)
        
        self.id_frequencies[msg.arbitration_id] = self.id_frequencies.get(msg.arbitration_id, 0) + 1
    
    def get_id_info(self, can_id: int) -> Dict[str, str]:
        """Get information about a CAN ID"""
        return self.known_ids.get(can_id, {
            "name": "Unknown",
            "service": "Unknown", 
            "type": "Unknown"
        })
    
    def analyze_traffic(self) -> Dict[str, Any]:
        """Analyze captured CAN traffic"""
        if not self.messages:
            return {"error": "No messages to analyze"}
        
        total_messages = len(self.messages)
        unique_ids = len(self.unique_ids)
        time_span = self.messages[-1].timestamp - self.messages[0].timestamp if total_messages > 1 else 0
        avg_rate = total_messages / time_span if time_span > 0 else 0
        
        # Top 10 most frequent IDs
        top_ids = sorted(self.id_frequencies.items(), key=lambda x: x[1], reverse=True)[:10]
        
        return {
            "total_messages": total_messages,
            "unique_ids": unique_ids,
            "time_span": time_span,
            "avg_rate": avg_rate,
            "top_ids": top_ids
        }


class OBD2Scanner:
    """OBD-II diagnostic scanner implementation"""
    
    def __init__(self, can_bus):
        self.logger = Logger.get_logger("obd2_scanner")
        self.can_bus = can_bus
        
        # Standard OBD-II PIDs
        self.pids = {
            0x00: "Supported PIDs [01-20]",
            0x01: "Monitor status since DTCs cleared",
            0x02: "Freeze frame DTC",
            0x03: "Fuel system status",
            0x04: "Calculated engine load",
            0x05: "Engine coolant temperature",
            0x06: "Short term fuel trim—Bank 1",
            0x07: "Long term fuel trim—Bank 1",
            0x08: "Short term fuel trim—Bank 2",
            0x09: "Long term fuel trim—Bank 2",
            0x0A: "Fuel pressure",
            0x0B: "Intake manifold absolute pressure",
            0x0C: "Engine RPM",
            0x0D: "Vehicle speed",
            0x0E: "Timing advance",
            0x0F: "Intake air temperature",
            0x10: "MAF air flow rate",
            0x11: "Throttle position",
            0x12: "Commanded secondary air status",
            0x13: "Oxygen sensors present",
            0x14: "Bank 1, Sensor 1 Oxygen sensor voltage",
            0x15: "Bank 1, Sensor 2 Oxygen sensor voltage",
            0x1C: "OBD standards this vehicle conforms to",
            0x1F: "Run time since engine start",
            0x20: "PIDs supported [21-40]",
            0x21: "Distance traveled with malfunction indicator lamp (MIL) on",
            0x2F: "Fuel level input",
            0x33: "Barometric pressure",
            0x40: "PIDs supported [41-60]",
            0x42: "Control module voltage",
            0x43: "Absolute load value",
            0x44: "Command equivalence ratio",
            0x45: "Relative throttle position",
            0x46: "Ambient air temperature",
            0x47: "Absolute throttle position B",
            0x48: "Absolute throttle position C",
            0x4C: "Commanded throttle actuator",
            0x4D: "Time run with MIL on",
            0x4E: "Time since trouble codes cleared",
        }
        
        # Common DTC categories
        self.dtc_categories = {
            'P': "Powertrain",
            'B': "Body", 
            'C': "Chassis",
            'U': "Network Communication"
        }
    
    def send_obd2_request(self, mode: int, pid: int = 0x00) -> Optional[bytes]:
        """Send OBD-II request and return response"""
        try:
            # Standard OBD-II request format
            request_data = bytes([mode, pid])
            request_msg = Message(
                arbitration_id=0x7DF,  # Functional addressing
                data=request_data,
                is_extended_id=False
            )
            
            if self.can_bus:
                self.can_bus.send(request_msg)
                
                # Wait for response (simplified)
                time.sleep(0.1)
                response = self.can_bus.recv(timeout=1.0)
                
                if response and response.arbitration_id in range(0x7E8, 0x7EF + 1):
                    return response.data
            
            return None
            
        except Exception as e:
            self.logger.error(f"OBD-II request failed: {e}")
            return None
    
    def scan_supported_pids(self) -> List[int]:
        """Scan for supported PIDs"""
        supported_pids = []
        
        # Check PID support in ranges
        for base_pid in [0x00, 0x20, 0x40, 0x60, 0x80, 0xA0, 0xC0]:
            response = self.send_obd2_request(0x01, base_pid)
            if response and len(response) >= 6:
                # Response format: [mode+0x40, pid, data1, data2, data3, data4]
                pid_bitmap = int.from_bytes(response[2:6], 'big')
                
                for i in range(32):
                    if pid_bitmap & (1 << (31 - i)):
                        pid = base_pid + i + 1
                        if pid <= 0xFF:
                            supported_pids.append(pid)
        
        return supported_pids
    
    def read_dtcs(self) -> List[str]:
        """Read Diagnostic Trouble Codes"""
        dtcs = []
        
        response = self.send_obd2_request(0x03)  # Show stored DTCs
        if response and len(response) >= 2:
            num_dtcs = response[1]
            
            for i in range(num_dtcs):
                if len(response) >= 4 + (i * 2):
                    dtc_bytes = response[2 + (i * 2):4 + (i * 2)]
                    if len(dtc_bytes) == 2:
                        dtc_code = self._decode_dtc(dtc_bytes)
                        dtcs.append(dtc_code)
        
        return dtcs
    
    def _decode_dtc(self, dtc_bytes: bytes) -> str:
        """Decode DTC from bytes"""
        if len(dtc_bytes) != 2:
            return "Invalid DTC"
        
        first_byte = dtc_bytes[0]
        second_byte = dtc_bytes[1]
        
        # Extract category from first 2 bits
        category_bits = (first_byte >> 6) & 0x03
        categories = ['P', 'C', 'B', 'U']
        category = categories[category_bits]
        
        # Extract digits
        digit1 = (first_byte >> 4) & 0x03
        digit2 = first_byte & 0x0F
        digit3 = (second_byte >> 4) & 0x0F
        digit4 = second_byte & 0x0F
        
        return f"{category}{digit1}{digit2:X}{digit3:X}{digit4:X}"


class UDSScanner:
    """Unified Diagnostic Services (ISO 14229) scanner"""
    
    def __init__(self, can_bus):
        self.logger = Logger.get_logger("uds_scanner")
        self.can_bus = can_bus
        
        # UDS service identifiers
        self.services = {
            0x10: "Diagnostic Session Control",
            0x11: "ECU Reset", 
            0x14: "Clear Diagnostic Information",
            0x19: "Read DTC Information",
            0x22: "Read Data By Identifier",
            0x23: "Read Memory By Address",
            0x24: "Read Scaling Data By Identifier", 
            0x27: "Security Access",
            0x28: "Communication Control",
            0x2A: "Read Data By Periodic Identifier",
            0x2C: "Dynamically Define Data Identifier",
            0x2E: "Write Data By Identifier",
            0x2F: "Input Output Control By Identifier",
            0x31: "Routine Control",
            0x34: "Request Download",
            0x35: "Request Upload",
            0x36: "Transfer Data",
            0x37: "Request Transfer Exit",
            0x3D: "Write Memory By Address",
            0x3E: "Tester Present",
            0x83: "Access Timing Parameter",
            0x84: "Secured Data Transmission",
            0x85: "Control DTC Setting",
            0x86: "Response On Event",
            0x87: "Link Control"
        }
        
        # Common Data Identifiers
        self.data_identifiers = {
            0xF010: "Active Diagnostic Session",
            0xF011: "ECU Manufacturing Date",
            0xF012: "ECU Serial Number", 
            0xF013: "Supported Functional Units",
            0xF015: "VM identifier",
            0xF018: "Application Software Identification",
            0xF019: "Application Software Version Number",
            0xF01A: "System Supplier Identifier",
            0xF01B: "ECU Manufacturing Date",
            0xF01C: "ECU Serial Number",
            0xF040: "Vehicle Identification Number",
            0xF050: "Vehicle Manufacturer Specific",
            0xF0F0: "Boot Software Identification",
            0xF0F1: "Application Software Identification",
            0xF0F2: "Application Data Identification",
            0xF0F3: "Boot Software Fingerprint",
            0xF0F4: "Application Software Fingerprint",
            0xF0F5: "Application Data Fingerprint"
        }
    
    def send_uds_request(self, target_id: int, service: int, data: bytes = b'') -> Optional[bytes]:
        """Send UDS request to specific ECU"""
        try:
            request_data = bytes([service]) + data
            request_msg = Message(
                arbitration_id=target_id,
                data=request_data,
                is_extended_id=False
            )
            
            if self.can_bus:
                self.can_bus.send(request_msg)
                
                # Wait for response
                time.sleep(0.1)
                response = self.can_bus.recv(timeout=1.0)
                
                if response and response.arbitration_id == target_id + 8:
                    return response.data
            
            return None
            
        except Exception as e:
            self.logger.error(f"UDS request failed: {e}")
            return None
    
    def scan_ecu_info(self, ecu_id: int) -> Dict[str, Any]:
        """Scan ECU information using UDS"""
        ecu_info = {
            "ecu_id": ecu_id,
            "response_id": ecu_id + 8,
            "services": [],
            "data_identifiers": {},
            "session_active": False
        }
        
        # Try to establish diagnostic session
        response = self.send_uds_request(ecu_id, 0x10, bytes([0x01]))  # Default session
        if response and len(response) >= 2 and response[0] == 0x50:
            ecu_info["session_active"] = True
            
            # Read common data identifiers
            for did, description in self.data_identifiers.items():
                data = self.send_uds_request(ecu_id, 0x22, struct.pack('>H', did))
                if data and len(data) >= 3 and data[0] == 0x62:
                    ecu_info["data_identifiers"][did] = {
                        "description": description,
                        "data": data[3:].hex().upper()
                    }
        
        return ecu_info


class CANFuzzer:
    """CAN bus fuzzing implementation"""
    
    def __init__(self, can_bus):
        self.logger = Logger.get_logger("can_fuzzer")
        self.can_bus = can_bus
        self.fuzzing_active = False
        self._lock = threading.Lock()
    
    def random_fuzz(self, target_ids: List[int], duration: int = 60, rate: int = 100):
        """Random CAN message fuzzing"""
        print(f"{Colors.CYAN}  [{Colors.GREEN}+{Colors.CYAN}] Starting random fuzzing")
        print(f"{Colors.INFO}  Target IDs: {[hex(x) for x in target_ids]}")
        print(f"{Colors.INFO}  Duration: {duration}s, Rate: {rate} msg/s")
        
        with self._lock:
            self.fuzzing_active = True
        
        start_time = time.time()
        messages_sent = 0
        
        try:
            while self.fuzzing_active and (time.time() - start_time) < duration:
                # Generate random message
                target_id = random.choice(target_ids)
                data_length = random.randint(1, 8)
                data = bytes([random.randint(0, 255) for _ in range(data_length)])
                
                msg = Message(
                    arbitration_id=target_id,
                    data=data,
                    is_extended_id=False
                )
                
                if self.can_bus:
                    try:
                        self.can_bus.send(msg)
                        messages_sent += 1
                    except Exception as e:
                        self.logger.warning(f"Failed to send fuzz message: {e}")
                
                time.sleep(1.0 / rate)
                
                # Progress update
                elapsed = time.time() - start_time
                if int(elapsed) % 10 == 0:  # Update every 10 seconds
                    print(f"{Colors.YELLOW}  Fuzzing... {elapsed:.0f}s, {messages_sent} messages sent{Colors.RESET}")
        
        finally:
            with self._lock:
                self.fuzzing_active = False
            
            print(f"{Colors.SUCCESS}  Fuzzing completed: {messages_sent} messages sent in {elapsed:.1f}s")
    
    def stop_fuzzing(self):
        """Stop fuzzing operation"""
        with self._lock:
            self.fuzzing_active = False
    
    def intelligent_fuzz(self, baseline_messages: List[CANMessage], mutation_rate: float = 0.1):
        """Intelligent fuzzing based on captured traffic"""
        print(f"{Colors.CYAN}  [{Colors.GREEN}+{Colors.CYAN}] Starting intelligent fuzzing")
        print(f"{Colors.INFO}  Baseline messages: {len(baseline_messages)}")
        print(f"{Colors.INFO}  Mutation rate: {mutation_rate * 100}%")
        
        mutations = 0
        
        for base_msg in baseline_messages:
            if not self.fuzzing_active:
                break
            
            # Mutate message
            if random.random() < mutation_rate:
                mutated_data = bytearray(base_msg.data)
                
                # Random bit flip
                if mutated_data:
                    byte_idx = random.randint(0, len(mutated_data) - 1)
                    bit_idx = random.randint(0, 7)
                    mutated_data[byte_idx] ^= (1 << bit_idx)
                
                msg = Message(
                    arbitration_id=base_msg.arbitration_id,
                    data=bytes(mutated_data),
                    is_extended_id=base_msg.is_extended_id
                )
                
                if self.can_bus:
                    try:
                        self.can_bus.send(msg)
                        mutations += 1
                        print(f"{Colors.BLUE}  Sent mutation: ID=0x{msg.arbitration_id:X}, Data={msg.data.hex()}")
                    except Exception as e:
                        self.logger.warning(f"Failed to send mutated message: {e}")
                
                time.sleep(0.01)  # Small delay between mutations
        
        print(f"{Colors.SUCCESS}  Intelligent fuzzing completed: {mutations} mutations sent")


class AutomotiveSecurityModule:
    """Professional automotive security testing module"""
    
    def __init__(self):
        self.logger = Logger.get_logger("automotive_security")
        self.can_interface = Config.DEFAULT_CAN_INTERFACE
        self.can_bus: Optional[can.BusABC] = None
        self.hostname = SystemUtils.get_hostname()
        self._lock = threading.Lock()
        
        # Initialize components
        self.can_db = CANDatabase()
        self.obd2_scanner: Optional[OBD2Scanner] = None
        self.uds_scanner: Optional[UDSScanner] = None
        self.can_fuzzer: Optional[CANFuzzer] = None
        
        self.logger.info("Professional automotive security module initialized")
        self.setup_can_interface()
    
    def setup_can_interface(self) -> bool:
        """Setup CAN interface with professional configuration"""
        with error_handler("setting up CAN interface", self.logger):
            try:
                # Validate CAN interface
                InputValidator.validate_can_interface(self.can_interface)
                
                # Check and create virtual CAN interface if needed
                if os.system(f"ip link show {self.can_interface} > /dev/null 2>&1") != 0:
                    print(f"\n{Colors.WARNING}  CAN interface {Colors.CYAN}{self.can_interface}{Colors.WARNING} not found!")
                    print(f"{Colors.INFO}  Creating virtual CAN interface for testing...")
                    
                    cmd = f"sudo modprobe vcan && sudo ip link add dev {self.can_interface} type vcan && sudo ip link set up {self.can_interface}"
                    result = os.system(cmd)
                    
                    if result != 0:
                        raise RuntimeError("Failed to create virtual CAN interface")
                
                # Initialize CAN bus with professional settings
                self.can_bus = can.interface.Bus(
                    channel=self.can_interface,
                    bustype='socketcan',
                    bitrate=500000,  # Standard automotive CAN bitrate
                    receive_own_messages=False
                )
                
                # Initialize scanners
                self.obd2_scanner = OBD2Scanner(self.can_bus)
                self.uds_scanner = UDSScanner(self.can_bus)
                self.can_fuzzer = CANFuzzer(self.can_bus)
                
                print(f"{Colors.SUCCESS}  Connected to CAN interface: {Colors.CYAN}{self.can_interface}")
                print(f"{Colors.INFO}  Bitrate: 500 kbps (Standard automotive)")
                self.logger.info(f"CAN interface {self.can_interface} setup successful")
                return True
                
            except Exception as e:
                error_msg = f"Failed to setup CAN interface: {e}"
                print(f"{Colors.ERROR}  {error_msg}")
                print(f"{Colors.WARNING}  Some features will work in simulation mode only")
                self.logger.error(error_msg)
                return False
    
    def cleanup(self):
        """Clean up resources"""
        with self._lock:
            if self.can_fuzzer:
                self.can_fuzzer.stop_fuzzing()
            
            if self.can_bus:
                try:
                    self.can_bus.shutdown()
                    self.logger.info("CAN bus connection closed")
                except Exception as e:
                    self.logger.warning(f"Error closing CAN bus: {e}")
        
        # Clean up CAN interface
        try:
            if os.system(f"ip link show {self.can_interface} > /dev/null 2>&1") == 0:
                print(f"{Colors.INFO}  Cleaning up CAN interface...")
                os.system(f"sudo ip link del dev {self.can_interface} 2>/dev/null")
        except:
            pass
    
    def __del__(self):
        """Destructor"""
        self.cleanup()


# Continue with the rest of the professional automotive module...
# Due to length constraints, I'll create this as a separate module with proper menu integration

if __name__ == "__main__":
    try:
        auto_security = AutomotiveSecurityModule()
        print("Automotive security module initialized successfully")
    except Exception as e:
        print(f"Error: {e}")