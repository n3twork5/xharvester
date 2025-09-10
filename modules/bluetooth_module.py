#!/usr/bin/env python
import os
import time
import socket
import asyncio
import platform
from typing import List, Dict, Any

# BLE imports
try:
    from bleak import BleakClient, BleakScanner, BleakError
    from bleak.backends.characteristic import BleakGATTCharacteristic
    from bleak.backends.service import BleakGATTService
    BLE_AVAILABLE = True
except ImportError:
    BLE_AVAILABLE = False
    BleakClient, BleakScanner, BleakError = None, None, None
    BleakGATTCharacteristic, BleakGATTService = None, None

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
IS_WINDOWS = platform.system() == "Windows"
IS_LINUX = platform.system() == "Linux"
IS_MACOS = platform.system() == "Darwin"

class BluetoothModule:
    def __init__(self):
        self.discovered_ble_devices = {}
        self.hostname = self.get_hostname()
        self.ble_available = BLE_AVAILABLE
        self.connected_ble_device = None
        
        print(f"{GREEN}  Bluetooth Low Energy available: {self.ble_available}")
        if not self.ble_available:
            print(f"{YELLOW}  Install bleak library for BLE support:{BLUE} pip install bleak")

    def clear_screen(self) -> None:
        os.system('cls' if os.name == 'nt' else 'clear')

    def get_hostname(self) -> str:
        try:
            return socket.gethostname()
        except:
            return "unknown"

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

    ### BLE Operations ###
    async def scan_ble_devices(self, timeout: float = 10.0) -> List[Dict[str, Any]]:
        """Scan for BLE devices"""
        if not self.ble_available:
            print(f"{RED}  BLE not available on this platform")
            return []
            
        print(f"{GREEN}  Scanning for BLE devices...")
        devices = []
        try:
            scanned_devices = await BleakScanner.discover(timeout=timeout)
            for i, d in enumerate(scanned_devices):
                device_info = {
                    "index": i,
                    "name": d.name or "Unknown",
                    "address": d.address,
                    "metadata": d.metadata,
                    "rssi": d.metadata.get("rssi", 0) if d.metadata else 0,
                    "details": d.details if hasattr(d, 'details') else None
                }
                devices.append(device_info)
                self.discovered_ble_devices[i] = device_info
                
                rssi_str = f"{YELLOW}RSSI: {CYAN}{device_info['rssi']} dBm" if device_info['rssi'] else ""
                print(f"  [{i}]{YELLOW} NAME: {CYAN}{device_info['name']} {YELLOW}ADDRESS: {CYAN}{device_info['address']} {rssi_str}")
                
            return devices
        except Exception as e:
            print(f"{RED}  BLE scan failed: {e}")
            return []

    async def explore_ble_services(self, address: str):
        """Explore services and characteristics of a BLE device"""
        if not self.ble_available:
            print(f"{RED}  BLE not available on this platform")
            return
            
        try:
            async with BleakClient(address) as client:
                print(f"{GREEN}  Connected to {address}")
                self.connected_ble_device = client
                
                services = await client.get_services()
                for service in services:
                    print(f"{GREEN}  Service: {service.uuid} - {service.description}")
                    for char in service.characteristics:
                        prop_str = ", ".join(char.properties)
                        print(f"  {YELLOW}Characteristic: {char.uuid} - Properties: {prop_str}")
                        
                        if "read" in char.properties:
                            try:
                                value = await client.read_gatt_char(char.uuid)
                                print(f"    {CYAN}Value: {value.hex()}")
                            except Exception as e:
                                print(f"    {RED}Read failed: {e}")
                        
        except Exception as e:
            print(f"{RED}  Failed to explore BLE device: {e}")
        finally:
            self.connected_ble_device = None

    def ble_services_flow(self):
        """Handle BLE service exploration workflow"""
        if not self.ble_available:
            print(f"{RED}  BLE not available on this platform")
            return
            
        print(f"{GREEN}  Starting BLE service exploration")
        
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        devices = loop.run_until_complete(self.scan_ble_devices())
        
        if not devices:
            return
            
        choice = input(f"{GREEN}  Select device index: {YELLOW}")
        try:
            selected = self.discovered_ble_devices[int(choice)]
            loop.run_until_complete(self.explore_ble_services(selected["address"]))
        except (ValueError, IndexError):
            print(f"{RED}  Invalid selection")
        except Exception as e:
            print(f"Error: {e}")
        finally:
            loop.close()

    def ble_spoofing_attack(self):
        """BLE spoofing attack implementation"""
        if not self.ble_available:
            print(f"{RED}  BLE not available")
            return
            
        print(f"{RED}  Starting BLE spoofing attack simulation")
        
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        devices = loop.run_until_complete(self.scan_ble_devices())
        
        if not devices:
            return
            
        choice = input(f"{GREEN}  Select device to spoof: {YELLOW}")
        if not choice.isdigit() or int(choice) not in self.discovered_ble_devices:
            print(f"{RED}  Invalid selection")
            return
            
        target = self.discovered_ble_devices[int(choice)]
        print(f"{BLUE}  Selected device: {target['name']} ({target['address']})")
        
        spoof_name = input(f"{GREEN}  Enter spoofed name [default: {target['name']}_spoof]: {YELLOW}")
        spoof_name = spoof_name or f"{target['name']}_spoof"
        
        print(f"{GREEN}  Simulating BLE spoofing attack as '{spoof_name}'")
        print(f"{YELLOW}  Actual BLE spoofing requires specialized hardware and software")
        
        impacts = [
            "Man-in-the-middle attacks",
            "Data interception",
            "Unauthorized access to BLE devices",
            "False data injection",
            "Device tracking and profiling"
        ]
        
        for impact in impacts:
            print(f"  {RED}• {impact}")
            time.sleep(0.5)
            
        print(f"{GREEN}  BLE spoofing simulation completed")

    ### Main Menu ###
    def main(self) -> None:
        time.sleep(0.05)
        active = True
        while active:
            self.clear_screen()
            self.text_animation()
            print(f"\n\t\t{LIGHTCYAN_EX} ︻芫═─── {RED}💥 {YELLOW}(▀̿Ĺ̯▀̿ ̿)\t\t\t\n")
            print(f"{LIGHTCYAN_EX}  ⇇━━━━━━━━━━━━━━━━━━━━━━━━୨ৎ━━━━━━━━━━━━━━━━━━━━━━━━━⇉")
            print(f"{GREEN}         {LIGHTCYAN_EX}🚀{RESET}{GREEN}   XHARVESTER -- BLUETOOTH MENU   {LIGHTCYAN_EX}🕷{GREEN}")
            print(f"{LIGHTCYAN_EX}  ⇇━━━━━━━━━━━━━━━━━━━━━━━━୨ৎ━━━━━━━━━━━━━━━━━━━━━━━━━⇉")
            
            # Show available BLE options
            options = [
                ("1", "🎭", "BLE Scanning", self.ble_available),
                ("2", "🔍", "List Services", self.ble_available),
                ("3", "👻", "BLE Spoofing", self.ble_available),
            ]
            
            for opt_num, icon, name, available in options:
                if available:
                    print(f"{GREEN}\t[{opt_num}]{MAGENTA} {icon}{CYAN} {name}")
                else:
                    print(f"{RED}\t[{opt_num}]{MAGENTA} {icon}{RED} {name} (Not Available)")
            
            print(f"{LIGHTCYAN_EX}  ⇇━━━━━━━━━━━━━━━━━━━━━━━━୨ৎ━━━━━━━━━━━━━━━━━━━━━━━━━⇉")
            print(f"{YELLOW}\t[0] 🚪🔙 Back")
            print(f"{LIGHTCYAN_EX}  ⇇━━━━━━━━━━━━━━━━━━━━━━━━୨ৎ━━━━━━━━━━━━━━━━━━━━━━━━━⇉")  

            try:
                choice = input(f"\n  [💀] {GREEN}xharvester{YELLOW}@{RESET}{CYAN}{self.hostname}{RESET}{RED}:{RESET}{GREEN}~{RESET}{YELLOW}$ ")
                    
                if choice == "0":
                    mesg = f"{MAGENTA}\n\t\t\t🚪🔙{YELLOW} Moving Back・・・\n\n"
                    for word in mesg:
                        print(word, end="", flush=True)
                        time.sleep(0.05)
                    active = False

                elif choice == "1":
                    if not self.ble_available:
                        self.print_error("BLE not available")
                    else:
                        print(f"\n{GREEN}  BLE Scanning:{CYAN} Passive reconnaissance to discover nearby BLE devices and their services.")
                        print(f"{GREEN}  Impact:{CYAN} Device tracking, profiling, and identifying vulnerabilities for further attacks.")
                        print(f"{GREEN}  Protection:{CYAN} Disable Bluetooth when not needed; use random MAC addresses for BLE.{RESET}")
                        loop = asyncio.new_event_loop()
                        asyncio.set_event_loop(loop)
                        loop.run_until_complete(self.scan_ble_devices())
                        loop.close()

                elif choice == "2":
                    if not self.ble_available:
                        self.print_error("BLE not available")
                    else:
                        print(f"\n{GREEN}  List Services:{CYAN} Enumerating supported services and profiles on a Bluetooth device.")
                        print(f"{GREEN}  Impact:{CYAN} Reveals potential attack surfaces and vulnerabilities in specific services.")
                        print(f"{GREEN}  Protection:{CYAN} Disable unnecessary Bluetooth services; use least-privilege principles on device features.{RESET}")
                        self.ble_services_flow()

                elif choice == "3":
                    if not self.ble_available:
                        self.print_error("BLE not available")
                    else:
                        print(f"\n{GREEN}  BLE Spoofing:{CYAN} Impersonating legitimate BLE devices to perform man-in-the-middle attacks.")
                        print(f"{GREEN}  Impact:{CYAN} Interception of sensitive data, unauthorized access, and false data injection.")
                        print(f"{GREEN}  Protection:{CYAN} Use BLE devices with secure pairing, validate device identities, and monitor for spoofed devices.{RESET}")
                        self.ble_spoofing_attack()

                else:
                    error = f"\n\t\t\t{YELLOW}{choice} is not a valid option!\n"
                    for word in error:
                        print(word, end="", flush=True)
                        time.sleep(0.05)

                if choice != "0":
                    input(f"\n  {GREEN}Press Enter to continue・・・")
            
            except (KeyboardInterrupt, EOFError):
                terminator = f"\n\n\t\t\t{MAGENTA}🚪🔙{YELLOW} Moving Back・・・\n\n"
                for word in terminator:
                    print(word, end="", flush=True)
                    time.sleep(0.05)
                active = False

if __name__ == "__main__":
    blue = BluetoothModule()
    blue.main()