#!/usr/bin/env python
import os
import time
import socket

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

class BluetoothModule:
    def __init__(self):
        #self.socket = socket.gethostname()
        pass

    ### Color Status ###
    def print_status(message: str) -> None:
        """Print status messages"""
        print(f"{GREEN}[+]{RESET} {message}")

    def print_warning(message: str) -> None:
        """Print warning messages"""
        print(f"{YELLOW}[!]{RESET} {message}")

    def print_error(message: str) -> None:
        """Print error messages"""
        print(f"{RED}[-]{RESET} {message}")

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
        print(f"\t\t\t{RED}DEVELOPED{YELLOW} BY{GREEN} N3TWORK({RED}G{YELLOW}H{GREEN}A{BLACK}N{RED}A)\t\t\t")
        print(f"{RED} Use only for authorized security testing!{RESET}")


    def clear_screen(self) -> None:
        os.system('cls' if os.name == 'nt' else 'clear')

    def get_hostname(self) -> str:
        try:
            return socket.gethostname()
        except:
            return "unknown"
        
    def discover_classic_devices(self) -> None:
        pass

    def list_services(self, address) -> None:
        pass
    
    def main(self) -> None:
        time.sleep(0.05)
        active = True
        while active:
            self.clear_screen()
            self.text_animation()
            print(f"\n\t\t\t{LIGHTCYAN_EX}(▀̿Ĺ̯▀̿ ̿)\t\t\t\n")
            print(f"{LIGHTCYAN_EX}  ⇇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━⇉")
            print(f"{GREEN}         🚀   XHARVESTER -- BLUETOOTH MENU")
            print(f"{LIGHTCYAN_EX}  ⇇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━⇉")
            print(f"{CYAN}\t[1] 📱 BlueJacking")
            print(f"{CYAN}\t[2] 📝 BlueSnarfing")
            print(f"{CYAN}\t[3] 🕵️  BlueBugging")
            print(f"{CYAN}\t[4] 💣 BlueBorne Attack")
            print(f"{CYAN}\t[5] 🔑 KNOB Attack")
            print(f"{CYAN}\t[6] 🎭 BLE Scanning")
            print(f"{CYAN}\t[7] 📡 Classic BT Scanning")
            print(f"{CYAN}\t[8] 🔍 List Services")
            print(f"{CYAN}\t[9] 💥 BlueSmacking")
            print(f"{LIGHTCYAN_EX}  ⇇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━⇉")
            print(f"{YELLOW}\t[0] ⇇ Back")
            print(f"{LIGHTCYAN_EX}  ⇇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━⇉")  

            try:
                choice = input(f"\n  [💀] {GREEN}xharvester{YELLOW}@{RESET}{CYAN}{self.get_hostname()}{RESET}{RED}:{RESET}{GREEN}~{RESET}{YELLOW}$ ")
            except (KeyboardInterrupt, EOFError):
                terminator = f"\n\n\t\t\t{MAGENTA}[💀]{RESET}{RED} Exiting...\n\n"
                for word in terminator:
                    print(word, end="", flush=True)
                    time.sleep(0.05)
                break
                    
            if choice == "0":
                mesg = f"{MAGENTA}\n\t\t\t[⇇]{YELLOW} Moving Back...\n\n"
                for word in mesg:
                    print(word, end="", flush=True)
                    time.sleep(0.05)
                active = False

            elif choice == "1":
                print(f"\n{GREEN}  BlueJacking:{CYAN} Sending unsolicited messages to Bluetooth devices.")
                print(f"{GREEN}  Impact:{CYAN} Annoyance and social engineering; no data theft or device control.")
                print(f"{GREEN}  Protection:{CYAN} Set Bluetooth to non-discoverable mode; ignore pairing requests from unknown devices.{RESET}")

            elif choice == "2":
                print(f"\n{GREEN}  BlueSnarfing:{CYAN} Unauthorized access and theft of data from a Bluetooth device.")
                print(f"{GREEN}  Impact:{CYAN} Theft of contacts, calendars, emails, and other personal information.")
                print(f"{GREEN}  Protection:{CYAN} Disable Bluetooth when not in use; use strong pairing PINs; keep devices updated.{RESET}")

            elif choice == "3":
                print(f"\n{GREEN}  BlueBugging:{CYAN} Establishing a secret backdoor connection to take full control of a device.")
                print(f"{GREEN}  Impact:{CYAN} Full device takeover: making calls, sending messages, and eavesdropping.")
                print(f"{GREEN}  Protection:{CYAN} Patch old devices; be wary of unknown pairing requests; disable BT visibility.{RESET}")
        
            elif choice == "4":
                print(f"\n{GREEN}  BlueBorne Attacks:{CYAN} Exploiting Bluetooth protocols to spread malware without user interaction.")
                print(f"{GREEN}  Impact:{CYAN} Remote code execution, device compromise, and network propagation.")
                print(f"{GREEN}  Protection:{CYAN} Apply the latest security patches; turn off Bluetooth when unused.{RESET}\n")

            elif choice == "5":
                print(f"\n{GREEN}  KNOB Atack:{CYAN} Forcing a weak encryption key during Bluetooth pairing.")
                print(f"{GREEN}  Impact:{CYAN} Eavesdropping on encrypted connections and man-in-the-middle attacks.")
                print(f"{GREEN}  Protection:{CYAN} Update device firmware; avoid pairing in public areas; use BLE with strong security.{RESET}\n")

            elif choice == "6":
                print(f"\n{GREEN}  BLE Scanning:{CYAN} Passive reconnaissance to discover nearby BLE devices and their services.")
                print(f"{GREEN}  Impact:{CYAN} Device tracking, profiling, and identifying vulnerabilities for further attacks.")
                print(f"{GREEN}  Protection:{CYAN} Disable Bluetooth when not needed; use random MAC addresses for BLE.{RESET}")

            elif choice == "7":
                print(f"\n{GREEN}  Classic BT Scanning:{CYAN} Actively scanning for discoverable classic Bluetooth devices.")
                print(f"{GREEN}  Impact:{CYAN} Identifying targets for more advanced attacks like BlueSnarfing or BlueBugging.")
                print(f"{GREEN}  Protection:{CYAN} Set Bluetooth to non-discoverable; use 'hidden' mode in OS settings.{RESET}")

            elif choice == "8":
                print(f"\n{GREEN}  List Services:{CYAN} Enumerating supported services and profiles on a Bluetooth device.")
                print(f"{GREEN}  Impact:{CYAN} Reveals potential attack surfaces and vulnerabilities in specific services (e.g., OBEX, A2DP).")
                print(f"{GREEN}  Protection:{CYAN} Disable unnecessary Bluetooth services; use least-privilege principles on device features.{RESET}")
            
            elif choice == "9":
                print(f"\n{GREEN}  BlueSmacking:{CYAN} Flooding a Bluetooth device with oversized packets causing a Denial-of-Service (DoS).")
                print(f"{GREEN}  Impact:{CYAN} Crashes the Bluetooth stack, rendering the device's radio unresponsive.")
                print(f"{GREEN}  Protection:{CYAN} Use updated Bluetooth stacks with DoS protections; power cycle BT to recover.{RESET}")

            else:
                error = f"\n\t\t\t{YELLOW}{choice} is not a valid option!\n"
                for word in error:
                    print(word, end="", flush=True)
                    time.sleep(0.05)

            if choice != "0":
                input(f"\n  {GREEN}Press Enter to continue...")

if __name__ == "__main__":
    blue = BluetoothModule()
    blue.main()