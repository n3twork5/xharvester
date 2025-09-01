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

class WifiModule:
    def __init__(self):
        #self.socket = socket.gethostname()
        pass

    ### Color Status ###
    def print_status(message: str) -> None:
        """Print status messages"""
        print(f"{GREEN}[✚]{RESET} {message}")

    def print_warning(message: str) -> None:
        """Print warning messages"""
        print(f"{YELLOW}[❕️]{RESET} {message}")

    def print_error(message: str) -> None:
        """Print error messages"""
        print(f"{RED}[━]{RESET} {message}")

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
            print(f"\n\t\t{LIGHTCYAN_EX} ︻芫═─── {RED}💥 {YELLOW}(▀̿Ĺ̯▀̿ ̿)\t\t\t\n")
            print(f"{LIGHTCYAN_EX}  ⇇━━━━━━━━━━━━━━━━━━━━━━━━୨ৎ━━━━━━━━━━━━━━━━━━━━━━━━━⇉")
            print(f"{GREEN}         {LIGHTCYAN_EX}🚀{RESET}{GREEN}   XHARVESTER -- WIFI MENU   {LIGHTCYAN_EX}🕷{GREEN}")
            print(f"{LIGHTCYAN_EX}  ⇇━━━━━━━━━━━━━━━━━━━━━━━━୨ৎ━━━━━━━━━━━━━━━━━━━━━━━━━⇉")
            print(f"{GREEN}\t[1]{MAGENTA} 😈 {CYAN} Captive Portal")
            print(f"{GREEN}\t[2]{MAGENTA} 🤝 {CYAN} Handshake Sniffer")
            print(f"{GREEN}\t[3]{MAGENTA}👨🏿 {CYAN}MITM & ARP Spoofing")
            print(f"{GREEN}\t[4]{MAGENTA} 🚫 {CYAN} Deauth (DOS Attack)")
            print(f"{GREEN}\t[5]{MAGENTA} 🗝 {CYAN}  KRACK (Key Reinstallation Attack)")
            print(f"{GREEN}\t[6]{MAGENTA} 📍 {CYAN} WPS Attacks")
            print(f"{GREEN}\t[7]{MAGENTA} 👥 {CYAN} Evil Twin")
            print(f"{LIGHTCYAN_EX}  ⇇━━━━━━━━━━━━━━━━━━━━━━━━୨ৎ━━━━━━━━━━━━━━━━━━━━━━━━━⇉")
            print(f"{YELLOW}\t[0] 🚪🔙 Back")
            print(f"{LIGHTCYAN_EX}  ⇇━━━━━━━━━━━━━━━━━━━━━━━━୨ৎ━━━━━━━━━━━━━━━━━━━━━━━━━⇉") 

            try:
                choice = input(f"\n  [💀] {GREEN}xharvester{YELLOW}@{RESET}{CYAN}{self.get_hostname()}{RESET}{RED}:{RESET}{GREEN}~{RESET}{YELLOW}$ ")
            except (KeyboardInterrupt, EOFError):
                terminator = f"\n\n\t\t\t{MAGENTA}[💀]{RESET}{RED} Exiting・・・\n\n"
                for word in terminator:
                    print(word, end="", flush=True)
                    time.sleep(0.05)
                break
                    
            if choice == "0":
                mesg = f"{MAGENTA}\n\t\t\t🚪🔙{YELLOW} Moving Back・・・\n\n"
                for word in mesg:
                    print(word, end="", flush=True)
                    time.sleep(0.05)
                active = False

            elif choice == "1":
                print(f"\n{GREEN}  Captive Portal:{CYAN} A fake login page used to steal user credentials.")
                print(f"{GREEN}  Impact:{CYAN} Can lead to compromised accounts and identity theft.")
                print(f"{GREEN}  Protection:{CYAN} Verify the URL is legitimate, look for HTTPS encryption, and avoid entering sensitive information on public networks.{RESET}")

            elif choice == "2":
                print(f"\n{GREEN}  Handshake Sniffer:{CYAN} Intercepts unencrypted wireless traffic to steal sensitive information.")
                print(f"{GREEN}  Impact:{CYAN} Can lead to loss of privacy and data leaks.")
                print(f"{GREEN}  Protection:{CYAN} Ensure you use HTTPS instead of HTTP, and shut down servers to disconnect attackers.{RESET}")

            elif choice == "3":
                print(f"\n{GREEN}  Man-in-the-Middle (MITM) & ARP Spoofing:{CYAN} Redirecting and intercepting unencrypted network traffic by poisoning the ARP cache.")
                print(f"{GREEN}  Impact:{CYAN} Leads to a loss of privacy, data leaks, and the theft of sensitive information like login credentials.")
                print(f"{GREEN}  Protection:{CYAN} Always use HTTPS instead of HTTP, employ a VPN, and configure your network to use ARP spoofing detection tools.{RESET}")

            elif choice == "4":
                print(f"\n{GREEN}  Deauth Attack (DoS):{CYAN} Broadcasting forged deauthentication frames to forcibly disconnect devices from a Wi-Fi network.")
                print(f"{GREEN}  Impact:{CYAN} Causes service disruption, network unavailability, and can be used to capture handshakes for password cracking.")
                print(f"{GREEN}  Protection:{CYAN} Upgrade to WPA3, which provides management frame protection (802.11w), making deauth attacks significantly harder.{RESET}")

            elif choice == "5":
                print(f"\n{GREEN}  KRACK (Key Reinstallation Attack):{CYAN} Exploiting WPA2 handshake vulnerabilities to reinstall encryption keys and decrypt traffic.")
                print(f"{GREEN}  Impact:{CYAN} Decryption of WPA2 traffic, data theft.")
                print(f"{GREEN}  Protection:{CYAN} Apply firmware/OS patches, upgrade to WPA3, use VPNs.{RESET}")

            elif choice == "6":
                print(f"\n{GREEN}  WPS Attacks:{CYAN} Exploiting WPA2 handshake vulnerabilities to reinstall encryption keys and decrypt traffic.")
                print(f"{GREEN}  Impact:{CYAN} Unauthorized network access via WPS PIN brute force attack.")
                print(f"{GREEN}  Protection:{CYAN} Unauthorized network access via WPS PIN brute force attack.{RESET}")

            elif choice == "7":
                print(f"\n{GREEN}  AP Spoofing (Evil Twin):{CYAN} Creating a rogue access point that mimics a legitimate network.")
                print(f"{GREEN}  Impact:{CYAN} Users unknowingly connect to malicious networks, enabling traffic interception.")
                print(f"{GREEN}  Protection:{CYAN} Verify network names carefully, use VPNs on public networks, and avoid auto-connecting to open Wi-Fi.{RESET}")

            else:
                error = f"\n\t\t\t{YELLOW}{choice} is not a valid option!\n"
                for word in error:
                    print(word, end="", flush=True)
                    time.sleep(0.05)
                time.sleep(3)

            if choice != "0":
                input(f"\n  {GREEN}Press Enter to continue・・・")

if __name__ == "__main__":
    wifi = WifiModule()
    wifi.main()