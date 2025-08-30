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

class ICSModule:
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
            print(f"{GREEN}         🚀   XHARVESTER -- ICS MENU")
            print(f"{LIGHTCYAN_EX}  ⇇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━⇉")
            print(f"{CYAN}\t[1] ⚡ Unauthorized Command Injection")
            print(f"{CYAN}\t[2] 💣 ICS Malware (e.g., Triton)")
            print(f"{CYAN}\t[3] 🔁 ICS Replay Attack")
            print(f"{CYAN}\t[4] 🚫 ICS DoS Attack")
            print(f"{CYAN}\t[5] 📦 Supply Chain Attack")
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
                print(f"\n{GREEN}  Unauthorized Command Injection:{CYAN} Sending malicious commands to ICS devices like PLCs or RTUs.")
                print(f"{GREEN}  Impact:{CYAN} Can cause physical damage to machinery, unsafe operations, and production downtime.")
                print(f"{GREEN}  Protection:{CYAN} Implement strict access control, network segmentation, and use application whitelisting.{RESET}")
            
            elif choice == "2":
                print(f"\n{GREEN}  ICS Malware (e.g., Triton):{CYAN} Malicious software specifically designed to target and disrupt industrial control systems.")
                print(f"{GREEN}  Impact:{CYAN} Safety system disablement, equipment hijacking, and potential physical destruction.")
                print(f"{GREEN}  Protection:{CYAN} Secure HMIs and workstations, use specialized ICS antivirus, and enforce air-gapping where possible.{RESET}")

            elif choice == "3":
                print(f"\n{GREEN}  ICS Replay Attack:{CYAN} Capturing and retransmitting legitimate operational commands to disrupt processes.")
                print(f"{GREEN}  Impact:{CYAN} Causes unexpected machine behavior, process anomalies, and potential safety incidents.")
                print(f"{GREEN}  Protection:{CYAN} Use protocols with sequence numbers or timestamps to prevent command replay.{RESET}")

            elif choice == "4":
                print(f"\n{GREEN}  ICS DoS Attack:{CYAN} Flooding controllers or network channels to cripple operational technology (OT) networks.")
                print(f"{GREEN}  Impact:{CYAN} Halts production, disrupts critical monitoring, and can lead to unsafe plant conditions.")
                print(f"{GREEN}  Protection:{CYAN} Segment networks rigorously, prioritize ICS traffic, and deploy OT-specific intrusion detection systems.{RESET}")

            elif choice == "5":
                print(f"\n{GREEN}  Supply Chain Attack:{CYAN} Introducing vulnerabilities into ICS systems through compromised firmware or vendor software.")
                print(f"{GREEN}  Impact:{CYAN} Provides a hidden backdoor for attackers, leading to widespread system compromise and data manipulation.")
                print(f"{GREEN}  Protection:{CYAN} Vet suppliers rigorously, verify firmware checksums, and maintain an isolated patch management network.{RESET}")

            else:
                error = f"\n\t\t\t{YELLOW}{choice} is not a valid option!\n"
                for word in error:
                    print(word, end="", flush=True)
                    time.sleep(0.05)
                
            if choice != "0":
                
                input(f"\n  {GREEN}Press Enter to continue...")

if __name__ == "__main__":
    ics = ICSModule()
    ics.main()