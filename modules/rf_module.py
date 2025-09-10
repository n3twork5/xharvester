#!/usr/bin/env python
import os
import time
import socket
import subprocess
import platform
from typing import List, Dict, Any, Optional

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

# Try to import RF/SDR libraries
try:
    import numpy as np
except ImportError:
    np = None

try:
    from rtlsdr import RtlSdr
except ImportError:
    RtlSdr = None

try:
    from scapy.all import *
    from scapy.layers.dot15d4 import *
    from scapy.layers.zigbee import *
except ImportError:
    pass

class RFModule:
    def __init__(self):
        self.hostname = self.get_hostname()
        self.sdr_available = RtlSdr is not None
        self.numpy_available = np is not None
        self.supported_protocols = ["Zigbee", "Z-Wave", "LoRa", "433MHz", "315MHz", "GSM", "Bluetooth"]
        self.recorded_signals = {}
        
        self.print_status(f"SDR support available: {self.sdr_available}")
        self.print_status(f"NumPy available: {self.numpy_available}")
        
        if not self.sdr_available:
            self.print_warning("For full RF functionality, install pyrtlsdr (pip install pyrtlsdr)")
        
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
        print(f"{YELLOW} RF Module with SDR Support{RESET}")

    ### RF Operations ###
    def check_rf_dependencies(self) -> bool:
        """Check if required RF dependencies are available"""
        missing = []
        
        if not self.sdr_available:
            missing.append("pyrtlsdr (install with: pip install pyrtlsdr)")
        
        if not self.numpy_available:
            missing.append("numpy (install with: pip install numpy)")
        
        # Check for GNU Radio
        try:
            subprocess.run(["gnuradio-companion", "--version"], capture_output=True, timeout=5)
        except (subprocess.TimeoutExpired, FileNotFoundError):
            missing.append("GNU Radio (install from your package manager)")
        
        if missing:
            self.print_warning("Missing RF dependencies:")
            for dep in missing:
                print(f"  - {dep}")
            return False
        
        self.print_status("All RF dependencies are available")
        return True

    def scan_rf_spectrum(self, start_freq: float = 400, end_freq: float = 900, sample_rate: float = 2.4e6) -> Optional[List[float]]:
        """Scan RF spectrum for signals (requires RTL-SDR)"""
        if not self.sdr_available:
            self.print_error("RTL-SDR not available")
            return None
            
        self.print_status(f"Scanning RF spectrum from {start_freq}MHz to {end_freq}MHz...")
        
        try:
            # This is a simplified simulation - real implementation would use the SDR
            # to capture and analyze signals across the frequency range
            with RtlSdr() as sdr:
                sdr.sample_rate = sample_rate
                sdr.center_freq = (start_freq + end_freq) / 2 * 1e6
                sdr.gain = 'auto'
                
                # Simulate finding some signals
                signals = []
                for freq in np.linspace(start_freq, end_freq, 20):
                    if np.random.random() > 0.7:  # 30% chance of finding a signal
                        signals.append(round(freq, 2))
                        self.print_status(f"Found signal at {freq}MHz")
                
                if not signals:
                    self.print_warning("No strong signals detected in the scanned range")
                
                return signals
                
        except Exception as e:
            self.print_error(f"RF scan failed: {e}")
            return None

    def record_signal(self, frequency: float, duration: int = 5, name: str = "") -> bool:
        """Record a signal at a specific frequency"""
        if not self.sdr_available:
            self.print_error("RTL-SDR not available")
            return False
            
        if not name:
            name = f"signal_{frequency}MHz"
            
        self.print_status(f"Recording signal at {frequency}MHz for {duration} seconds...")
        
        try:
            # Simulate recording - real implementation would capture I/Q samples
            time.sleep(duration)  # Simulate recording time
            
            # Generate simulated signal data
            signal_data = {
                "frequency": frequency,
                "duration": duration,
                "timestamp": time.time(),
                "sample_count": duration * 1000  # Simulated sample count
            }
            
            self.recorded_signals[name] = signal_data
            self.print_status(f"Signal recorded as '{name}'")
            return True
            
        except Exception as e:
            self.print_error(f"Signal recording failed: {e}")
            return False

    def replay_signal(self, signal_name: str, frequency: float, repeat: int = 1) -> bool:
        """Replay a recorded signal"""
        if signal_name not in self.recorded_signals:
            self.print_error(f"Signal '{signal_name}' not found")
            return False
            
        self.print_status(f"Replaying signal '{signal_name}' at {frequency}MHz (x{repeat})...")
        
        try:
            signal = self.recorded_signals[signal_name]
            
            # Simulate replay - real implementation would transmit the signal
            for i in range(repeat):
                self.print_status(f"Transmission {i+1}/{repeat}...")
                time.sleep(1)  # Simulate transmission time
                
            self.print_status("Replay completed")
            return True
            
        except Exception as e:
            self.print_error(f"Signal replay failed: {e}")
            return False

    def detect_protocols(self, frequency: float) -> List[str]:
        """Attempt to detect protocols at a specific frequency"""
        self.print_status(f"Analyzing protocols at {frequency}MHz...")
        
        # Simulate protocol detection based on frequency
        protocols = []
        
        if 2400 <= frequency <= 2483.5:
            protocols.append("Bluetooth/802.15.1")
            protocols.append("Zigbee/802.15.4")
            protocols.append("Wi-Fi")
            
        elif 902 <= frequency <= 928:
            protocols.append("ISM Band Devices")
            protocols.append("Some LoRa implementations")
            
        elif 433 <= frequency <= 434:
            protocols.append("433MHz Devices (garage doors, sensors)")
            
        elif 315 <= frequency <= 316:
            protocols.append("315MHz Devices (car key fobs, remotes)")
            
        else:
            protocols.append("Unknown protocol -可能需要进一步分析")
            
        for protocol in protocols:
            self.print_status(f"Detected possible protocol: {protocol}")
            
        return protocols

    def rf_jamming_simulation(self, frequency: float, duration: int = 10) -> bool:
        """Simulate RF jamming (for educational purposes only)"""
        self.print_warning("RF Jamming Simulation - FOR EDUCATIONAL PURPOSES ONLY")
        self.print_warning("Actual jamming is illegal in most countries!")
        
        self.print_status(f"Simulating jamming at {frequency}MHz for {duration} seconds...")
        
        try:
            # Simulate jamming - this doesn't actually transmit anything
            for i in range(duration):
                print(f"{RED}JAMMING [{'#' * (i+1)}{' ' * (duration-i-1)}] {i+1}/{duration} seconds{RESET}", end='\r')
                time.sleep(1)
                
            print()  # New line after progress bar
            self.print_status("Jamming simulation completed")
            return True
            
        except Exception as e:
            self.print_error(f"Jamming simulation failed: {e}")
            return False

    def list_recorded_signals(self) -> None:
        """List all recorded signals"""
        if not self.recorded_signals:
            self.print_warning("No signals recorded yet")
            return
            
        self.print_status("Recorded signals:")
        for i, (name, signal) in enumerate(self.recorded_signals.items()):
            print(f"  [{i}] {name}: {signal['frequency']}MHz, {signal['duration']}s")

    ### Main Menu Handlers ###
    def handle_eavesdropping(self):
        """Handle RF eavesdropping workflow"""
        print(f"\n{GREEN}  RF Eavesdropping:{CYAN} Intercepting and monitoring unencrypted wireless transmissions.")
        print(f"{GREEN}  Impact:{CYAN} Loss of confidentiality, exposing sensitive data and commands.")
        print(f"{GREEN}  Protection:{CYAN} Implement strong end-to-end encryption (AES) for all transmitted data.{RESET}")
        
        # Check dependencies
        if not self.check_rf_dependencies():
            self.print_error("Cannot perform eavesdropping without required hardware/software")
            return
            
        # Scan for signals
        start_freq = input(f"{GREEN}  Enter start frequency in MHz [default: 400]: {YELLOW}").strip()
        end_freq = input(f"{GREEN}  Enter end frequency in MHz [default: 900]: {YELLOW}").strip()
        
        start_freq = float(start_freq) if start_freq else 400
        end_freq = float(end_freq) if end_freq else 900
        
        signals = self.scan_rf_spectrum(start_freq, end_freq)
        
        if signals:
            freq_choice = input(f"{GREEN}  Select frequency to monitor or leave blank to cancel: {YELLOW}").strip()
            if freq_choice:
                try:
                    frequency = float(freq_choice)
                    duration = input(f"{GREEN}  Enter monitoring duration in seconds [default: 10]: {YELLOW}").strip()
                    duration = int(duration) if duration.isdigit() else 10
                    
                    name = input(f"{GREEN}  Enter a name for this recording or leave blank for automatic: {YELLOW}").strip()
                    
                    self.record_signal(frequency, duration, name)
                    self.detect_protocols(frequency)
                    
                except ValueError:
                    self.print_error("Invalid frequency")

    def handle_replay_attack(self):
        """Handle RF replay attack workflow"""
        print(f"\n{GREEN}  RF Replay Attack:{CYAN} Capturing and retransmitting valid RF signals to trigger unauthorized actions.")
        print(f"{GREEN}  Impact:{CYAN} Unauthorized control of devices, such as unlocking doors or activating systems.")
        print(f"{GREEN}  Protection:{CYAN} Use cryptographic nonces or rolling codes in messages to prevent reuse.{RESET}")
        
        # List recorded signals
        self.list_recorded_signals()
        
        if not self.recorded_signals:
            return
            
        # Select signal to replay
        signal_choice = input(f"{GREEN}  Select signal to replay: {YELLOW}").strip()
        if not signal_choice.isdigit() or int(signal_choice) >= len(self.recorded_signals):
            self.print_error("Invalid selection")
            return
            
        signal_name = list(self.recorded_signals.keys())[int(signal_choice)]
        signal = self.recorded_signals[signal_name]
        
        # Get replay parameters
        frequency = input(f"{GREEN}  Enter frequency to transmit on [default: {signal['frequency']}MHz]: {YELLOW}").strip()
        frequency = float(frequency) if frequency else signal['frequency']
        
        repeat = input(f"{GREEN}  Enter number of times to repeat transmission [default: 1]: {YELLOW}").strip()
        repeat = int(repeat) if repeat.isdigit() else 1
        
        self.replay_signal(signal_name, frequency, repeat)

    def handle_jamming(self):
        """Handle RF jamming workflow"""
        print(f"\n{GREEN}  RF Jamming:{CYAN} Flooding a frequency with noise to create a denial-of-service condition.")
        print(f"{GREEN}  Impact:{CYAN} Disrupts critical communications, causing operational failure and system unavailability.")
        print(f"{GREEN}  Protection:{CYAN} Deploy frequency-hopping spread spectrum (FHSS) and monitor for jamming signals.{RESET}")
        
        self.print_warning("This is a simulation only. Actual RF jamming is illegal in most countries!")
        
        frequency = input(f"{GREEN}  Enter frequency to simulate jamming on (MHz): {YELLOW}").strip()
        if not frequency:
            self.print_error("Frequency required")
            return
            
        try:
            frequency = float(frequency)
            duration = input(f"{GREEN}  Enter simulation duration in seconds [default: 10]: {YELLOW}").strip()
            duration = int(duration) if duration.isdigit() else 10
            
            self.rf_jamming_simulation(frequency, duration)
            
        except ValueError:
            self.print_error("Invalid frequency")

    def handle_spoofing(self):
        """Handle RF spoofing workflow"""
        print(f"\n{GREEN}  RF Spoofing:{CYAN} Impersonating a legitimate device to inject malicious commands into a network.")
        print(f"{GREEN}  Impact:{CYAN} Enables unauthorized control and manipulation of devices, leading to potential physical damage.")
        print(f"{GREEN}  Protection:{CYAN} Enforce mutual authentication between all devices and use cryptographically signed commands.{RESET}")
        
        self.print_status("RF Spoofing requires a recorded signal to modify")
        self.list_recorded_signals()
        
        if not self.recorded_signals:
            return
            
        signal_choice = input(f"{GREEN}  Select signal to use as base for spoofing: {YELLOW}").strip()
        if not signal_choice.isdigit() or int(signal_choice) >= len(self.recorded_signals):
            self.print_error("Invalid selection")
            return
            
        signal_name = list(self.recorded_signals.keys())[int(signal_choice)]
        self.print_status(f"Selected '{signal_name}' for spoofing")
        
        # In a real implementation, we would modify the signal here
        new_name = input(f"{GREEN}  Enter name for spoofed signal: {YELLOW}").strip()
        if not new_name:
            new_name = f"spoofed_{signal_name}"
            
        # Create a modified version of the signal
        original_signal = self.recorded_signals[signal_name]
        spoofed_signal = original_signal.copy()
        spoofed_signal["spoofed"] = True
        spoofed_signal["original"] = signal_name
        
        self.recorded_signals[new_name] = spoofed_signal
        self.print_status(f"Created spoofed signal '{new_name}'")
        
        # Option to immediately replay the spoofed signal
        replay = input(f"{GREEN}  Replay spoofed signal now? (y/N): {YELLOW}").strip().lower()
        if replay == 'y':
            frequency = input(f"{GREEN}  Enter frequency to transmit on [default: {original_signal['frequency']}MHz]: {YELLOW}").strip()
            frequency = float(frequency) if frequency else original_signal['frequency']
            
            self.replay_signal(new_name, frequency)

    def handle_mitm(self):
        """Handle RF Man-in-the-Middle workflow"""
        print(f"\n{GREEN}  RF Man-in-the-Middle (MITM):{CYAN} Intercepting and potentially altering two-way RF communication between devices.")
        print(f"{GREEN}  Impact:{CYAN} Loss of data integrity, stolen credentials, and complete compromise of the communication channel.")
        print(f"{GREEN}  Protection:{CYAN} Utilize strong encryption and secure key management to prevent interception and tampering.{RESET}")
        
        self.print_status("RF MITM attack simulation")
        self.print_status("This would require two SDRs: one to receive and one to transmit")
        
        # Check if we have the capability
        if not self.sdr_available:
            self.print_error("MITM attack requires SDR hardware")
            return
            
        frequency = input(f"{GREEN}  Enter frequency to monitor for MITM (MHz): {YELLOW}").strip()
        if not frequency:
            self.print_error("Frequency required")
            return
            
        try:
            frequency = float(frequency)
            self.print_status(f"Simulating MITM on {frequency}MHz")
            self.print_status("Monitoring for signals...")
            
            # Simulate detecting a communication
            time.sleep(2)
            self.print_status("Detected communication between two devices")
            self.print_status("Intercepting and analyzing...")
            time.sleep(1)
            
            # Simulate modifying the communication
            modify = input(f"{GREEN}  Attempt to modify intercepted communication? (y/N): {YELLOW}").strip().lower()
            if modify == 'y':
                self.print_status("Creating modified version of intercepted signal...")
                time.sleep(1)
                self.print_status("Replaying modified signal to target device...")
                time.sleep(2)
                self.print_status("MITM attack simulation completed")
            else:
                self.print_status("Passive interception only - no modifications made")
                
        except ValueError:
            self.print_error("Invalid frequency")

    ### Main Menu ###
    def main(self) -> None:
        # Check dependencies
        self.check_rf_dependencies()
        
        time.sleep(0.05)
        active = True
        while active:
            self.clear_screen()
            self.text_animation()
            print(f"\n\t\t{LIGHTCYAN_EX} ︻芫═─── {RED}💥 {YELLOW}(▀̿Ĺ̯▀̿ ̿)\t\t\t\n")
            print(f"{LIGHTCYAN_EX}  ⇇━━━━━━━━━━━━━━━━━━━━━━━━୨ৎ━━━━━━━━━━━━━━━━━━━━━━━━━⇉")
            print(f"{GREEN}         {LIGHTCYAN_EX}🚀{RESET}{GREEN}   XHARVESTER -- RF MENU   {LIGHTCYAN_EX}🕷{GREEN}")
            print(f"{LIGHTCYAN_EX}  ⇇━━━━━━━━━━━━━━━━━━━━━━━━୨ৎ━━━━━━━━━━━━━━━━━━━━━━━━━⇉")
            
            # Show available options based on capabilities
            options = [
                ("1", "👂", "RF Eavesdropping", self.sdr_available),
                ("2", "⟲", "RF Replay Attack", len(self.recorded_signals) > 0),
                ("3", "🚫", "RF Jamming", True),  # Simulation only, always available
                ("4", "📡", "RF Spoofing", len(self.recorded_signals) > 0),
                ("5", "👨🏿", "RF Man-in-the-Middle", self.sdr_available),
                ("6", "📊", "Scan RF Spectrum", self.sdr_available),
                ("7", "📝", "List Recorded Signals", True),
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
                self.handle_eavesdropping()
                    
            elif choice == "2":
                self.handle_replay_attack()

            elif choice == "3":
                self.handle_jamming()

            elif choice == "4":
                self.handle_spoofing()

            elif choice == "5":
                self.handle_mitm()
                
            elif choice == "6":
                if not self.sdr_available:
                    self.print_error("SDR hardware not available")
                else:
                    self.scan_rf_spectrum()
                    
            elif choice == "7":
                self.list_recorded_signals()

            else:
                error = f"\n\t\t\t{YELLOW}{choice} is not a valid option!\n"
                for word in error:
                    print(word, end="", flush=True)
                    time.sleep(0.05)
                
            if choice != "0":
                input(f"\n  {GREEN}Press Enter to continue・・・")

if __name__ == "__main__":
    rf = RFModule()
    rf.main()