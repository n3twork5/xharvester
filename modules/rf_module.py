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

class RFModule:
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
            print(f"{GREEN}         🚀   XHARVESTER -- RF MENU")
            print(f"{LIGHTCYAN_EX}  ⇇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━⇉")
            print(f"{CYAN}\t[1] 👂 RF Eavesdropping")
            print(f"{CYAN}\t[2] 🔁 RF Replay Attack")
            print(f"{CYAN}\t[3] 🚫 RF Jamming")
            print(f"{CYAN}\t[4] 📡 RF Spoofing")
            print(f"{CYAN}\t[5] 🕵️  RF Man-in-the-Middle (MITM)")
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
                print(f"\n{GREEN}  RF Eavesdropping:{CYAN} Intercepting and monitoring unencrypted wireless transmissions.")
                print(f"{GREEN}  Impact:{CYAN} Loss of confidentiality, exposing sensitive data and commands.")
                print(f"{GREEN}  Protection:{CYAN} Implement strong end-to-end encryption (AES) for all transmitted data.{RESET}")
            
            elif choice == "2":
                print(f"\n{GREEN}  RF Replay Attack:{CYAN} Capturing and retransmitting valid RF signals to trigger unauthorized actions.")
                print(f"{GREEN}  Impact:{CYAN} Unauthorized control of devices, such as unlocking doors or activating systems.")
                print(f"{GREEN}  Protection:{CYAN} Use cryptographic nonces or rolling codes in messages to prevent reuse.{RESET}")

            elif choice == "3":
                print(f"\n{GREEN}  RF Jamming:{CYAN} Flooding a frequency with noise to create a denial-of-service condition.")
                print(f"{GREEN}  Impact:{CYAN} Disrupts critical communications, causing operational failure and system unavailability.")
                print(f"{GREEN}  Protection:{CYAN} Deploy frequency-hopping spread spectrum (FHSS) and monitor for jamming signals.{RESET}")

            elif choice == "4":
                print(f"\n{GREEN}  RF Spoofing:{CYAN} Impersonating a legitimate device to inject malicious commands into a network.")
                print(f"{GREEN}  Impact:{CYAN} Enables unauthorized control and manipulation of devices, leading to potential physical damage.")
                print(f"{GREEN}  Protection:{CYAN} Enforce mutual authentication between all devices and use cryptographically signed commands.{RESET}")

            elif choice == "5":
                print(f"\n{GREEN}  RF Man-in-the-Middle (MITM):{CYAN} Intercepting and potentially altering two-way RF communication between devices.")
                print(f"{GREEN}  Impact:{CYAN} Loss of data integrity, stolen credentials, and complete compromise of the communication channel.")
                print(f"{GREEN}  Protection:{CYAN} Utilize strong encryption and secure key management to prevent interception and tampering.{RESET}")

            else:
                error = f"\n\t\t\t{YELLOW}{choice} is not a valid option!\n"
                for word in error:
                    print(word, end="", flush=True)
                    time.sleep(0.05)
                
            if choice != "0":
                input(f"\n  {GREEN}Press Enter to continue...")

if __name__ == "__main__":
    rf = RFModule()
    rf.main()