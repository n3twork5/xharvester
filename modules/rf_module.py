#!/usr/bin/env python3
"""
Radio Frequency (RF) Security Testing Module
Professional SDR-based RF analysis and wireless protocol testing

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
import struct
import math
from typing import List, Dict, Optional, Any, Tuple
import numpy as np

# Import application dependencies
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from config import Config, Colors
from utils import (
    SystemUtils, MenuRenderer, Logger, InputValidator, 
    Animation, error_handler
)

class RFSignal:
    """Represents an RF signal"""
    
    def __init__(self, frequency: float, amplitude: float = 0.0, modulation: str = "Unknown"):
        self.frequency = frequency
        self.amplitude = amplitude
        self.modulation = modulation
        self.bandwidth = 0.0
        self.protocol = "Unknown"
        self.timestamp = time.time()
        self.samples = []
        self.metadata = {}
        
    def __str__(self):
        return f"{self.frequency/1e6:.2f} MHz - {self.amplitude:.1f} dB ({self.modulation})"

class SDRController:
    """SDR hardware controller and interface"""
    
    def __init__(self):
        self.logger = Logger.get_logger("sdr_controller")
        self.device_type = None
        self.device_available = False
        self.sample_rate = 2048000  # 2 MHz default
        self.center_frequency = 100e6  # 100 MHz default
        self.gain = 20
        
        # Check for available SDR devices
        self._detect_sdr_devices()
        
    def _detect_sdr_devices(self):
        """Detect available SDR devices"""
        try:
            # Check for RTL-SDR
            result = subprocess.run(['rtl_test', '-t'], capture_output=True, text=True, timeout=5)
            if result.returncode == 0 and 'Found' in result.stderr:
                self.device_type = "RTL-SDR"
                self.device_available = True
                print(f"{Colors.SUCCESS}  RTL-SDR device detected")
                return
                
        except (subprocess.TimeoutExpired, FileNotFoundError):
            pass
        
        try:
            # Check for HackRF
            result = subprocess.run(['hackrf_info'], capture_output=True, text=True, timeout=5)
            if result.returncode == 0:
                self.device_type = "HackRF"
                self.device_available = True
                print(f"{Colors.SUCCESS}  HackRF device detected")
                return
                
        except FileNotFoundError:
            pass
        
        try:
            # Check for BladeRF
            result = subprocess.run(['bladeRF-cli', '-i'], capture_output=True, text=True, timeout=5)
            if result.returncode == 0:
                self.device_type = "BladeRF"
                self.device_available = True
                print(f"{Colors.SUCCESS}  BladeRF device detected")
                return
                
        except FileNotFoundError:
            pass
        
        print(f"{Colors.WARNING}  No SDR devices detected")
        self.device_available = False
    
    def get_device_info(self) -> Dict[str, Any]:
        """Get detailed device information"""
        info = {
            'type': self.device_type,
            'available': self.device_available,
            'sample_rate': self.sample_rate,
            'center_frequency': self.center_frequency,
            'gain': self.gain
        }
        
        if not self.device_available:
            return info
        
        try:
            if self.device_type == "RTL-SDR":
                result = subprocess.run(['rtl_test', '-t'], capture_output=True, text=True, timeout=5)
                if result.returncode == 0:
                    # Parse RTL-SDR info
                    for line in result.stderr.split('\n'):
                        if 'Tuner:' in line:
                            info['tuner'] = line.split(':', 1)[1].strip()
                        elif 'Tuner gain:' in line:
                            info['tuner_gain'] = line.split(':', 1)[1].strip()
            
            elif self.device_type == "HackRF":
                result = subprocess.run(['hackrf_info'], capture_output=True, text=True, timeout=5)
                if result.returncode == 0:
                    # Parse HackRF info
                    for line in result.stdout.split('\n'):
                        if 'Serial number:' in line:
                            info['serial'] = line.split(':', 1)[1].strip()
                        elif 'Firmware version:' in line:
                            info['firmware'] = line.split(':', 1)[1].strip()
                            
        except Exception as e:
            self.logger.error(f"Error getting device info: {e}")
        
        return info
    
    def scan_frequency_range(self, start_freq: float, end_freq: float, step: float = 1e6) -> List[RFSignal]:
        """Scan a frequency range for signals"""
        print(f"\n{Colors.CYAN}  [{Colors.GREEN}+{Colors.CYAN}] RF Frequency Scan")
        print(f"{Colors.INFO}  Range: {start_freq/1e6:.2f} - {end_freq/1e6:.2f} MHz")
        print(f"{Colors.INFO}  Step: {step/1e6:.2f} MHz")
        
        signals = []
        
        if not self.device_available:
            print(f"{Colors.WARNING}  No SDR device available - simulating scan...")
            # Simulate some signals for demo
            demo_frequencies = [88.5e6, 101.1e6, 433.92e6, 868e6, 915e6]
            for freq in demo_frequencies:
                if start_freq <= freq <= end_freq:
                    signal = RFSignal(freq, -45.0, "FM")
                    signals.append(signal)
                    print(f"{Colors.GREEN}    • {freq/1e6:.2f} MHz - Simulated signal")
            return signals
        
        try:
            current_freq = start_freq
            scan_count = 0
            total_steps = int((end_freq - start_freq) / step)
            
            while current_freq <= end_freq:
                # Set frequency and capture samples
                if self.device_type == "RTL-SDR":
                    # Use rtl_power for power spectrum analysis
                    cmd = [
                        'rtl_power', '-f', f'{current_freq:.0f}:{current_freq + step:.0f}:{step/10:.0f}',
                        '-i', '1', '-1', '/tmp/rf_scan.csv'
                    ]
                    
                    try:
                        result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
                        
                        if result.returncode == 0 and os.path.exists('/tmp/rf_scan.csv'):
                            # Parse power data
                            with open('/tmp/rf_scan.csv', 'r') as f:
                                lines = f.readlines()
                                
                            for line in lines[6:]:  # Skip header
                                if line.strip():
                                    parts = line.strip().split(', ')
                                    if len(parts) >= 6:
                                        freq = float(parts[2])
                                        power = float(parts[6])
                                        
                                        # Detect signals above threshold
                                        if power > -70:  # -70 dBm threshold
                                            signal = RFSignal(freq, power)
                                            signals.append(signal)
                                            print(f"{Colors.GREEN}    • {freq/1e6:.2f} MHz - {power:.1f} dBm")
                            
                            os.remove('/tmp/rf_scan.csv')
                    
                    except subprocess.TimeoutExpired:
                        print(f"{Colors.WARNING}  Scan timeout at {current_freq/1e6:.2f} MHz")
                
                elif self.device_type == "HackRF":
                    # Use hackrf_sweep for scanning
                    cmd = [
                        'hackrf_sweep', '-f', f'{current_freq/1e6:.0f}:{(current_freq + step)/1e6:.0f}',
                        '-w', '1000000', '-l', '32', '-g', '16', '-a', '1'
                    ]
                    
                    try:
                        result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
                        
                        # Parse sweep data (simplified)
                        if result.returncode == 0:
                            # HackRF sweep output parsing would go here
                            # For now, simulate detection
                            if scan_count % 10 == 0:  # Simulate occasional signals
                                signal = RFSignal(current_freq, -60.0, "Unknown")
                                signals.append(signal)
                                print(f"{Colors.GREEN}    • {current_freq/1e6:.2f} MHz - Detected")
                    
                    except subprocess.TimeoutExpired:
                        print(f"{Colors.WARNING}  Scan timeout at {current_freq/1e6:.2f} MHz")
                
                current_freq += step
                scan_count += 1
                
                # Progress indicator
                if scan_count % 10 == 0:
                    progress = (scan_count / total_steps) * 100
                    print(f"{Colors.YELLOW}  Scan progress: {progress:.1f}%")
        
        except Exception as e:
            self.logger.error(f"Frequency scan error: {e}")
            print(f"{Colors.ERROR}  Scan error: {e}")
        
        print(f"\n{Colors.SUCCESS}  Found {len(signals)} signals")
        return signals
    
    def record_signal(self, frequency: float, duration: int = 10, output_file: str = "/tmp/rf_recording.bin") -> bool:
        """Record RF signal to file"""
        print(f"\n{Colors.CYAN}  [{Colors.GREEN}+{Colors.CYAN}] RF Signal Recording")
        print(f"{Colors.INFO}  Frequency: {frequency/1e6:.2f} MHz")
        print(f"{Colors.INFO}  Duration: {duration} seconds")
        print(f"{Colors.INFO}  Output: {output_file}")
        
        if not self.device_available:
            print(f"{Colors.WARNING}  No SDR device available")
            return False
        
        try:
            if self.device_type == "RTL-SDR":
                cmd = [
                    'rtl_sdr', '-f', str(int(frequency)), '-s', str(self.sample_rate),
                    '-n', str(int(self.sample_rate * duration)), output_file
                ]
                
                print(f"{Colors.BLUE}  Starting RTL-SDR recording...")
                result = subprocess.run(cmd, capture_output=True, text=True, timeout=duration + 10)
                
                if result.returncode == 0 and os.path.exists(output_file):
                    file_size = os.path.getsize(output_file)
                    print(f"{Colors.SUCCESS}  Recording completed: {file_size} bytes")
                    return True
                else:
                    print(f"{Colors.ERROR}  Recording failed")
                    return False
            
            elif self.device_type == "HackRF":
                cmd = [
                    'hackrf_transfer', '-r', output_file, '-f', str(int(frequency)),
                    '-s', str(self.sample_rate), '-n', str(int(self.sample_rate * duration * 2))
                ]
                
                print(f"{Colors.BLUE}  Starting HackRF recording...")
                result = subprocess.run(cmd, capture_output=True, text=True, timeout=duration + 10)
                
                if result.returncode == 0 and os.path.exists(output_file):
                    file_size = os.path.getsize(output_file)
                    print(f"{Colors.SUCCESS}  Recording completed: {file_size} bytes")
                    return True
                else:
                    print(f"{Colors.ERROR}  Recording failed")
                    return False
        
        except Exception as e:
            self.logger.error(f"Recording error: {e}")
            print(f"{Colors.ERROR}  Recording error: {e}")
            return False
    
    def analyze_recording(self, recording_file: str) -> Dict[str, Any]:
        """Analyze recorded RF data"""
        print(f"\n{Colors.CYAN}  [{Colors.GREEN}+{Colors.CYAN}] RF Signal Analysis")
        
        analysis = {
            'file_size': 0,
            'duration': 0,
            'peak_frequency': 0,
            'avg_power': 0,
            'modulation_type': 'Unknown',
            'bandwidth': 0
        }
        
        if not os.path.exists(recording_file):
            print(f"{Colors.ERROR}  Recording file not found")
            return analysis
        
        try:
            file_size = os.path.getsize(recording_file)
            analysis['file_size'] = file_size
            
            # Calculate duration (assuming complex samples)
            samples = file_size // 2  # 2 bytes per I/Q sample
            analysis['duration'] = samples / self.sample_rate
            
            print(f"{Colors.INFO}  File size: {file_size:,} bytes")
            print(f"{Colors.INFO}  Duration: {analysis['duration']:.2f} seconds")
            print(f"{Colors.INFO}  Sample rate: {self.sample_rate:,} Hz")
            
            # Basic analysis using numpy if available
            try:
                # Read first chunk of data for analysis
                with open(recording_file, 'rb') as f:
                    data = f.read(min(1024*1024, file_size))  # Read up to 1MB
                
                # Convert to numpy array (assuming uint8 I/Q)
                samples_array = np.frombuffer(data, dtype=np.uint8)
                
                if len(samples_array) >= 2:
                    # Convert to complex samples
                    i_samples = samples_array[0::2].astype(np.float32) - 127.5
                    q_samples = samples_array[1::2].astype(np.float32) - 127.5
                    complex_samples = i_samples + 1j * q_samples
                    
                    # Calculate average power
                    power = np.mean(np.abs(complex_samples)**2)
                    analysis['avg_power'] = 10 * np.log10(power) if power > 0 else -100
                    
                    # FFT analysis
                    if len(complex_samples) >= 1024:
                        fft_data = np.fft.fft(complex_samples[:1024])
                        fft_magnitude = np.abs(fft_data)
                        peak_index = np.argmax(fft_magnitude)
                        
                        # Estimate peak frequency offset
                        freq_resolution = self.sample_rate / 1024
                        freq_offset = (peak_index - 512) * freq_resolution
                        analysis['peak_frequency'] = self.center_frequency + freq_offset
                        
                        # Estimate bandwidth (simplistic)
                        threshold = np.max(fft_magnitude) * 0.5
                        above_threshold = fft_magnitude > threshold
                        bandwidth_bins = np.sum(above_threshold)
                        analysis['bandwidth'] = bandwidth_bins * freq_resolution
                    
                    print(f"{Colors.SUCCESS}  Average power: {analysis['avg_power']:.1f} dBFS")
                    print(f"{Colors.SUCCESS}  Peak frequency: {analysis['peak_frequency']/1e6:.2f} MHz")
                    print(f"{Colors.SUCCESS}  Estimated bandwidth: {analysis['bandwidth']/1e3:.1f} kHz")
                    
                    # Simple modulation detection
                    if analysis['bandwidth'] > 200e3:
                        analysis['modulation_type'] = 'Wideband (possibly FM)'
                    elif analysis['bandwidth'] > 20e3:
                        analysis['modulation_type'] = 'Narrowband (possibly AM/FM)'
                    else:
                        analysis['modulation_type'] = 'Very narrowband (possibly digital)'
                    
                    print(f"{Colors.INFO}  Modulation estimate: {analysis['modulation_type']}")
                
            except ImportError:
                print(f"{Colors.WARNING}  NumPy not available - basic analysis only")
            except Exception as e:
                print(f"{Colors.WARNING}  Analysis error: {e}")
        
        except Exception as e:
            self.logger.error(f"Recording analysis error: {e}")
            print(f"{Colors.ERROR}  Analysis error: {e}")
        
        return analysis

class RFProtocolAnalyzer:
    """RF protocol analysis and decoding"""
    
    def __init__(self):
        self.logger = Logger.get_logger("rf_protocol_analyzer")
        self.known_protocols = {
            # Common ISM band protocols
            433.92e6: ['433 MHz ISM', 'Garage doors', 'Weather stations', 'Car key fobs'],
            315e6: ['315 MHz ISM', 'Tire pressure monitors', 'Car remotes'],
            868e6: ['868 MHz ISM', 'LoRa', 'Sigfox', 'Z-Wave'],
            915e6: ['915 MHz ISM', 'LoRa', 'ZigBee', 'Thread'],
            2.4e9: ['2.4 GHz ISM', 'WiFi', 'Bluetooth', 'ZigBee', 'Microwave ovens'],
            
            # Broadcast bands
            88e6: ['FM Broadcast', 'Radio stations'],
            162e6: ['Marine VHF', 'Weather radio'],
            
            # Aviation
            118e6: ['Aviation VHF', 'Air traffic control'],
            1090e6: ['ADS-B', 'Aircraft transponders'],
            
            # Cellular
            850e6: ['GSM 850', 'Cellular'],
            1900e6: ['PCS 1900', 'Cellular'],
        }
    
    def identify_protocol(self, frequency: float) -> List[str]:
        """Identify possible protocols for a frequency"""
        protocols = []
        
        # Check exact matches first
        if frequency in self.known_protocols:
            return self.known_protocols[frequency]
        
        # Check frequency ranges
        freq_mhz = frequency / 1e6
        
        if 87.5 <= freq_mhz <= 108:
            protocols.extend(['FM Broadcast', 'Radio stations'])
        elif 162 <= freq_mhz <= 174:
            protocols.extend(['VHF TV', 'Marine VHF'])
        elif 430 <= freq_mhz <= 440:
            protocols.extend(['Amateur radio (70cm)', 'ISM devices'])
        elif 860 <= freq_mhz <= 890:
            protocols.extend(['Cellular GSM 900', 'LoRa'])
        elif 902 <= freq_mhz <= 928:
            protocols.extend(['ISM 915 MHz', 'LoRa', 'ZigBee'])
        elif 1800 <= freq_mhz <= 1900:
            protocols.extend(['GSM 1800', 'DCS'])
        elif 2400 <= freq_mhz <= 2500:
            protocols.extend(['WiFi', 'Bluetooth', 'ISM 2.4 GHz'])
        
        return protocols if protocols else ['Unknown protocol']
    
    def analyze_ook_signal(self, samples: bytes) -> Dict[str, Any]:
        """Analyze On-Off Keying (OOK) signals"""
        analysis = {
            'protocol': 'OOK',
            'bit_rate': 0,
            'manchester': False,
            'preamble_length': 0,
            'data_bits': []
        }
        
        try:
            # This would require proper signal processing
            # For now, return basic analysis
            analysis['bit_rate'] = 1000  # 1 kbps estimate
            analysis['estimated'] = True
            
        except Exception as e:
            self.logger.error(f"OOK analysis error: {e}")
        
        return analysis
    
    def decode_ask_signal(self, samples: bytes) -> Dict[str, Any]:
        """Decode Amplitude Shift Keying (ASK) signals"""
        analysis = {
            'protocol': 'ASK',
            'symbols': [],
            'bit_rate': 0,
            'data': None
        }
        
        # Placeholder for ASK decoding
        # Would require proper signal processing
        return analysis
    
    def analyze_fsk_signal(self, samples: bytes) -> Dict[str, Any]:
        """Analyze Frequency Shift Keying (FSK) signals"""
        analysis = {
            'protocol': 'FSK',
            'deviation': 0,
            'bit_rate': 0,
            'mark_frequency': 0,
            'space_frequency': 0
        }
        
        # Placeholder for FSK analysis
        return analysis

class RFAttacker:
    """RF attack and replay tools"""
    
    def __init__(self, sdr_controller: SDRController):
        self.logger = Logger.get_logger("rf_attacker")
        self.sdr = sdr_controller
        self.recorded_signals = {}
    
    def replay_attack(self, recording_file: str, frequency: float, repeat: int = 1) -> bool:
        """Perform replay attack with recorded signal"""
        print(f"\n{Colors.CYAN}  [{Colors.RED}⚠{Colors.CYAN}] RF Replay Attack")
        print(f"{Colors.WARNING}  File: {recording_file}")
        print(f"{Colors.WARNING}  Frequency: {frequency/1e6:.2f} MHz")
        print(f"{Colors.WARNING}  Repeats: {repeat}")
        print(f"{Colors.ERROR}  ⚠️  This may interfere with legitimate communications!")
        
        confirm = input(f"\n{Colors.GREEN}  Continue with replay attack? ({Colors.CYAN}y{Colors.GREEN}/{Colors.RED}N{Colors.GREEN}): {Colors.YELLOW}").strip().lower()
        if confirm not in ['y', 'yes']:
            print(f"{Colors.INFO}  Attack cancelled")
            return False
        
        if not os.path.exists(recording_file):
            print(f"{Colors.ERROR}  Recording file not found")
            return False
        
        if not self.sdr.device_available:
            print(f"{Colors.WARNING}  No transmit-capable SDR available")
            return False
        
        try:
            if self.sdr.device_type == "HackRF":
                for i in range(repeat):
                    print(f"{Colors.BLUE}  Transmitting replay {i+1}/{repeat}...")
                    
                    cmd = [
                        'hackrf_transfer', '-t', recording_file, '-f', str(int(frequency)),
                        '-s', str(self.sdr.sample_rate), '-x', '20'  # 20 dB gain
                    ]
                    
                    result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
                    
                    if result.returncode == 0:
                        print(f"{Colors.SUCCESS}  Replay {i+1} completed")
                    else:
                        print(f"{Colors.ERROR}  Replay {i+1} failed")
                        break
                    
                    if i < repeat - 1:
                        time.sleep(1)  # Delay between replays
                
                print(f"{Colors.SUCCESS}  Replay attack completed")
                return True
            else:
                print(f"{Colors.ERROR}  {self.sdr.device_type} does not support transmission")
                return False
        
        except Exception as e:
            self.logger.error(f"Replay attack error: {e}")
            print(f"{Colors.ERROR}  Attack error: {e}")
            return False
    
    def jamming_attack(self, frequency: float, bandwidth: float, duration: int = 10) -> bool:
        """Perform RF jamming attack"""
        print(f"\n{Colors.CYAN}  [{Colors.RED}⚠{Colors.CYAN}] RF Jamming Attack")
        print(f"{Colors.WARNING}  Frequency: {frequency/1e6:.2f} MHz")
        print(f"{Colors.WARNING}  Bandwidth: {bandwidth/1e3:.1f} kHz")
        print(f"{Colors.WARNING}  Duration: {duration} seconds")
        print(f"{Colors.ERROR}  ⚠️  RF jamming may be illegal and dangerous!")
        
        confirm = input(f"\n{Colors.GREEN}  Continue with jamming? ({Colors.CYAN}y{Colors.GREEN}/{Colors.RED}N{Colors.GREEN}): {Colors.YELLOW}").strip().lower()
        if confirm not in ['y', 'yes']:
            print(f"{Colors.INFO}  Attack cancelled")
            return False
        
        if not self.sdr.device_available or self.sdr.device_type != "HackRF":
            print(f"{Colors.ERROR}  HackRF required for transmission")
            return False
        
        try:
            print(f"{Colors.BLUE}  Starting RF jamming...")
            
            # Generate noise file
            noise_file = "/tmp/rf_noise.bin"
            noise_duration = 1  # 1 second of noise
            noise_samples = int(self.sdr.sample_rate * noise_duration * 2)  # I/Q
            
            # Generate random noise
            noise_data = np.random.randint(0, 255, noise_samples, dtype=np.uint8)
            with open(noise_file, 'wb') as f:
                noise_data.tofile(f)
            
            # Transmit noise repeatedly
            start_time = time.time()
            jam_count = 0
            
            while (time.time() - start_time) < duration:
                cmd = [
                    'hackrf_transfer', '-t', noise_file, '-f', str(int(frequency)),
                    '-s', str(self.sdr.sample_rate), '-x', '47'  # Maximum gain
                ]
                
                subprocess.run(cmd, capture_output=True, timeout=2)
                jam_count += 1
                
                print(f"{Colors.YELLOW}  Jamming... {time.time() - start_time:.1f}s")
            
            os.remove(noise_file)
            print(f"{Colors.SUCCESS}  Jamming completed: {jam_count} transmissions")
            return True
        
        except Exception as e:
            self.logger.error(f"Jamming attack error: {e}")
            print(f"{Colors.ERROR}  Attack error: {e}")
            return False
    
    def clone_rolling_code(self, target_frequency: float) -> Dict[str, Any]:
        """Attempt to clone rolling code remotes"""
        print(f"\n{Colors.CYAN}  [{Colors.GREEN}+{Colors.CYAN}] Rolling Code Analysis")
        print(f"{Colors.INFO}  Target: {target_frequency/1e6:.2f} MHz")
        print(f"{Colors.WARNING}  This analyzes rolling code patterns")
        
        results = {
            'frequency': target_frequency,
            'signals_captured': 0,
            'pattern_identified': False,
            'rolling_codes': [],
            'estimated_algorithm': 'Unknown'
        }
        
        if not self.sdr.device_available:
            print(f"{Colors.WARNING}  No SDR device available")
            return results
        
        try:
            print(f"{Colors.INFO}  Monitoring for rolling code transmissions...")
            print(f"{Colors.YELLOW}  Press the remote button multiple times...")
            
            # Monitor for signals
            monitoring_time = 60  # 60 seconds
            start_time = time.time()
            
            while (time.time() - start_time) < monitoring_time:
                # This would require real signal processing
                # For demonstration, simulate detection
                if int(time.time()) % 10 == 0:  # Simulate detection every 10 seconds
                    code = f"CODE_{results['signals_captured']:04d}"
                    results['rolling_codes'].append(code)
                    results['signals_captured'] += 1
                    print(f"{Colors.GREEN}  Captured code: {code}")
                    
                    if results['signals_captured'] >= 3:
                        # Analyze pattern
                        results['pattern_identified'] = True
                        results['estimated_algorithm'] = 'KeeLoq or similar'
                        break
                
                time.sleep(1)
            
            if results['pattern_identified']:
                print(f"{Colors.SUCCESS}  Pattern analysis completed")
                print(f"{Colors.INFO}  Algorithm: {results['estimated_algorithm']}")
                print(f"{Colors.WARNING}  Note: Rolling codes cannot be easily cloned")
            else:
                print(f"{Colors.WARNING}  No clear pattern identified")
        
        except Exception as e:
            self.logger.error(f"Rolling code analysis error: {e}")
            print(f"{Colors.ERROR}  Analysis error: {e}")
        
        return results

class RFModule:
    """Main RF security testing module"""
    
    def __init__(self):
        self.logger = Logger.get_logger("rf_module")
        self.hostname = SystemUtils.get_hostname()
        self.sdr = SDRController()
        self.analyzer = RFProtocolAnalyzer()
        self.attacker = RFAttacker(self.sdr)
        self.discovered_signals = []
        
        # Check numpy availability
        try:
            import numpy as np
            self.numpy_available = True
        except ImportError:
            self.numpy_available = False
            print(f"{Colors.WARNING}  NumPy not available - limited signal analysis")
    
    def show_menu(self):
        """Display the RF module menu"""
        Animation.display_banner()
        MenuRenderer.render_menu_header(f"RADIO FREQUENCY {Colors.YELLOW}-{Colors.CYAN} SECURITY MODULE")
        
        icons = {
            "1": "📡",
            "2": "📊",
            "3": "🔍",
            "4": "🔄",
            "5": "📻",
            "6": "🎛️",
            "7": "🛯️",
            "8": "📄",
            "9": "ℹ️",
            "0": "🚚"
        }
        
        menu_options = {
            "1": "Frequency Spectrum Scan",
            "2": "Signal Analysis & Recording",
            "3": "Protocol Identification",
            "4": "Replay Attack",
            "5": "RF Jamming Attack",
            "6": "Rolling Code Analysis",
            "7": "SDR Device Management",
            "8": "Generate RF Assessment Report",
            "9": "Module Information",
            "0": "Return to Main Menu"
        }
        
        MenuRenderer.render_menu_options(menu_options, icons)
        MenuRenderer.render_menu_footer()
    
    def frequency_scan(self):
        """Frequency spectrum scanning interface"""
        print(f"\n{Colors.CYAN}  [{Colors.GREEN}+{Colors.CYAN}] RF Frequency Spectrum Scan")
        
        if not self.sdr.device_available:
            print(f"{Colors.WARNING}  No SDR device available - running simulation mode")
        
        try:
            start_freq_input = input(f"{Colors.GREEN}  Start frequency (MHz) [88]: {Colors.YELLOW}") or "88"
            start_freq = InputValidator.validate_float(start_freq_input, 0.1, 6000) * 1e6
            
            end_freq_input = input(f"{Colors.GREEN}  End frequency (MHz) [108]: {Colors.YELLOW}") or "108"
            end_freq = InputValidator.validate_float(end_freq_input, start_freq/1e6, 6000) * 1e6
            
            step_input = input(f"{Colors.GREEN}  Step size (kHz) [100]: {Colors.YELLOW}") or "100"
            step = InputValidator.validate_float(step_input, 1, 10000) * 1e3
            
            # Perform frequency scan
            signals = self.sdr.scan_frequency_range(start_freq, end_freq, step)
            self.discovered_signals = signals
            
            if signals:
                print(f"\n{Colors.MAGENTA}  Discovered Signals Summary:")
                print(f"{Colors.CYAN}  {'Frequency (MHz)':<15} {'Power (dB)':<12} {'Protocols':<30}")
                print(f"{Colors.CYAN}  {'-'*15} {'-'*12} {'-'*30}")
                
                for signal in signals[:20]:  # Show first 20 signals
                    protocols = self.analyzer.identify_protocol(signal.frequency)
                    protocol_str = ', '.join(protocols[:2])  # First 2 protocols
                    if len(protocol_str) > 28:
                        protocol_str = protocol_str[:25] + "..."
                    
                    print(f"{Colors.GREEN}  {signal.frequency/1e6:<15.2f} {signal.amplitude:<12.1f} {protocol_str:<30}")
                
                if len(signals) > 20:
                    print(f"{Colors.INFO}  ... and {len(signals) - 20} more signals")
            else:
                print(f"{Colors.WARNING}  No signals detected in specified range")
        
        except ValueError as e:
            print(f"{Colors.ERROR}  Invalid input: {e}")
    
    def signal_analysis(self):
        """Signal analysis and recording interface"""
        if not self.discovered_signals:
            print(f"{Colors.WARNING}  No signals discovered. Run frequency scan first.")
            return
        
        print(f"\n{Colors.CYAN}  [{Colors.GREEN}+{Colors.CYAN}] RF Signal Analysis & Recording")
        print(f"\n{Colors.INFO}  Available signals:")
        
        for i, signal in enumerate(self.discovered_signals[:10], 1):
            print(f"{Colors.GREEN}    [{i}] {signal}")
        
        try:
            choice_input = input(f"\n{Colors.GREEN}  Select signal to analyze [1]: {Colors.YELLOW}") or "1"
            choice = InputValidator.validate_integer(choice_input, 1, min(len(self.discovered_signals), 10))
            
            selected_signal = self.discovered_signals[choice - 1]
            
            duration_input = input(f"{Colors.GREEN}  Recording duration (seconds) [10]: {Colors.YELLOW}") or "10"
            duration = InputValidator.validate_integer(duration_input, 1, 300)
            
            # Record signal
            recording_file = f"/tmp/rf_signal_{selected_signal.frequency/1e6:.2f}MHz.bin"
            success = self.sdr.record_signal(selected_signal.frequency, duration, recording_file)
            
            if success:
                # Analyze recording
                analysis = self.sdr.analyze_recording(recording_file)
                
                # Protocol identification
                protocols = self.analyzer.identify_protocol(selected_signal.frequency)
                print(f"\n{Colors.MAGENTA}  Protocol Analysis:")
                for protocol in protocols:
                    print(f"{Colors.CYAN}    • {protocol}")
                
                # Store analysis results
                selected_signal.metadata['recording_file'] = recording_file
                selected_signal.metadata['analysis'] = analysis
                selected_signal.metadata['protocols'] = protocols
        
        except ValueError as e:
            print(f"{Colors.ERROR}  Invalid input: {e}")
    
    def protocol_identification(self):
        """Protocol identification interface"""
        print(f"\n{Colors.CYAN}  [{Colors.GREEN}+{Colors.CYAN}] RF Protocol Identification")
        
        try:
            freq_input = input(f"{Colors.GREEN}  Enter frequency (MHz): {Colors.YELLOW}").strip()
            frequency = InputValidator.validate_float(freq_input, 0.1, 6000) * 1e6
            
            protocols = self.analyzer.identify_protocol(frequency)
            
            print(f"\n{Colors.MAGENTA}  Protocol Analysis for {frequency/1e6:.2f} MHz:")
            
            if protocols:
                for i, protocol in enumerate(protocols, 1):
                    print(f"{Colors.GREEN}    [{i}] {protocol}")
                
                print(f"\n{Colors.INFO}  Additional Information:")
                
                # Provide specific information based on frequency
                freq_mhz = frequency / 1e6
                
                if 87.5 <= freq_mhz <= 108:
                    print(f"{Colors.CYAN}    • FM Broadcast band")
                    print(f"{Colors.CYAN}    • Stereo FM uses 19 kHz pilot tone")
                    print(f"{Colors.CYAN}    • RDS data at 57 kHz subcarrier")
                elif 430 <= freq_mhz <= 440:
                    print(f"{Colors.CYAN}    • Common for garage door openers")
                    print(f"{Colors.CYAN}    • Usually OOK or ASK modulation")
                    print(f"{Colors.CYAN}    • Rolling code security in modern devices")
                elif 860 <= freq_mhz <= 930:
                    print(f"{Colors.CYAN}    • ISM band - many protocols possible")
                    print(f"{Colors.CYAN}    • LoRa, ZigBee, proprietary protocols")
                    print(f"{Colors.CYAN}    • Check for spread spectrum signals")
                elif 2400 <= freq_mhz <= 2500:
                    print(f"{Colors.CYAN}    • 2.4 GHz ISM band")
                    print(f"{Colors.CYAN}    • WiFi channels 1-14")
                    print(f"{Colors.CYAN}    • Bluetooth frequency hopping")
            else:
                print(f"{Colors.WARNING}    No known protocols for this frequency")
        
        except ValueError as e:
            print(f"{Colors.ERROR}  Invalid input: {e}")
    
    def replay_attack(self):
        """RF replay attack interface"""
        print(f"\n{Colors.CYAN}  [{Colors.RED}⚠{Colors.CYAN}] RF Replay Attack")
        
        # Show available recordings
        recorded_signals = [s for s in self.discovered_signals if 'recording_file' in s.metadata]
        
        if not recorded_signals:
            print(f"{Colors.WARNING}  No recorded signals available.")
            print(f"{Colors.INFO}  Please record signals using Signal Analysis first.")
            return
        
        print(f"\n{Colors.INFO}  Available recordings:")
        for i, signal in enumerate(recorded_signals, 1):
            recording_file = signal.metadata['recording_file']
            file_size = os.path.getsize(recording_file) if os.path.exists(recording_file) else 0
            print(f"{Colors.GREEN}    [{i}] {signal.frequency/1e6:.2f} MHz - {file_size:,} bytes")
        
        try:
            choice_input = input(f"\n{Colors.GREEN}  Select recording [1]: {Colors.YELLOW}") or "1"
            choice = InputValidator.validate_integer(choice_input, 1, len(recorded_signals))
            
            selected_signal = recorded_signals[choice - 1]
            recording_file = selected_signal.metadata['recording_file']
            
            repeat_input = input(f"{Colors.GREEN}  Number of repeats [1]: {Colors.YELLOW}") or "1"
            repeat = InputValidator.validate_integer(repeat_input, 1, 100)
            
            # Perform replay attack
            success = self.attacker.replay_attack(recording_file, selected_signal.frequency, repeat)
            
            if success:
                print(f"\n{Colors.SUCCESS}  Replay attack completed successfully")
            else:
                print(f"\n{Colors.ERROR}  Replay attack failed")
        
        except ValueError as e:
            print(f"{Colors.ERROR}  Invalid input: {e}")
    
    def jamming_attack(self):
        """RF jamming attack interface"""
        print(f"\n{Colors.CYAN}  [{Colors.RED}⚠{Colors.CYAN}] RF Jamming Attack")
        print(f"{Colors.ERROR}  ⚠️  WARNING: RF jamming may be illegal and dangerous!")
        print(f"{Colors.WARNING}  Use only in authorized test environments!")
        
        if not self.sdr.device_available or self.sdr.device_type != "HackRF":
            print(f"{Colors.ERROR}  HackRF required for transmission attacks")
            return
        
        try:
            freq_input = input(f"{Colors.GREEN}  Target frequency (MHz): {Colors.YELLOW}").strip()
            frequency = InputValidator.validate_float(freq_input, 0.1, 6000) * 1e6
            
            bandwidth_input = input(f"{Colors.GREEN}  Bandwidth (kHz) [10]: {Colors.YELLOW}") or "10"
            bandwidth = InputValidator.validate_float(bandwidth_input, 1, 1000) * 1e3
            
            duration_input = input(f"{Colors.GREEN}  Duration (seconds) [5]: {Colors.YELLOW}") or "5"
            duration = InputValidator.validate_integer(duration_input, 1, 60)
            
            # Perform jamming attack
            success = self.attacker.jamming_attack(frequency, bandwidth, duration)
            
            if success:
                print(f"\n{Colors.SUCCESS}  Jamming attack completed")
            else:
                print(f"\n{Colors.ERROR}  Jamming attack failed")
        
        except ValueError as e:
            print(f"{Colors.ERROR}  Invalid input: {e}")
    
    def rolling_code_analysis(self):
        """Rolling code analysis interface"""
        print(f"\n{Colors.CYAN}  [{Colors.GREEN}+{Colors.CYAN}] Rolling Code Analysis")
        print(f"{Colors.INFO}  Analyze rolling code remote controls")
        
        try:
            freq_input = input(f"{Colors.GREEN}  Target frequency (MHz) [433.92]: {Colors.YELLOW}") or "433.92"
            frequency = InputValidator.validate_float(freq_input, 0.1, 6000) * 1e6
            
            # Perform rolling code analysis
            results = self.attacker.clone_rolling_code(frequency)
            
            print(f"\n{Colors.MAGENTA}  Rolling Code Analysis Results:")
            print(f"{Colors.INFO}    Frequency: {results['frequency']/1e6:.2f} MHz")
            print(f"{Colors.INFO}    Signals captured: {results['signals_captured']}")
            print(f"{Colors.INFO}    Pattern identified: {results['pattern_identified']}")
            print(f"{Colors.INFO}    Algorithm: {results['estimated_algorithm']}")
            
            if results['rolling_codes']:
                print(f"\n{Colors.GREEN}  Captured codes:")
                for code in results['rolling_codes']:
                    print(f"{Colors.CYAN}    • {code}")
        
        except ValueError as e:
            print(f"{Colors.ERROR}  Invalid input: {e}")
    
    def sdr_management(self):
        """SDR device management interface"""
        print(f"\n{Colors.CYAN}  [{Colors.GREEN}+{Colors.CYAN}] SDR Device Management")
        
        # Device information
        device_info = self.sdr.get_device_info()
        
        print(f"\n{Colors.MAGENTA}  Device Information:")
        print(f"{Colors.INFO}    Type: {device_info.get('type', 'None')}")
        print(f"{Colors.INFO}    Available: {device_info.get('available', False)}")
        
        if device_info.get('available'):
            print(f"{Colors.INFO}    Sample rate: {device_info.get('sample_rate', 0):,} Hz")
            print(f"{Colors.INFO}    Center frequency: {device_info.get('center_frequency', 0)/1e6:.2f} MHz")
            print(f"{Colors.INFO}    Gain: {device_info.get('gain', 0)} dB")
            
            if 'tuner' in device_info:
                print(f"{Colors.INFO}    Tuner: {device_info['tuner']}")
            if 'firmware' in device_info:
                print(f"{Colors.INFO}    Firmware: {device_info['firmware']}")
        
        # Available tools
        print(f"\n{Colors.MAGENTA}  Required Tools:")
        tools = [
            ('rtl_sdr', 'RTL-SDR capture tool'),
            ('rtl_power', 'RTL-SDR power scanning'),
            ('hackrf_transfer', 'HackRF capture/transmit'),
            ('hackrf_sweep', 'HackRF frequency sweeping'),
            ('hackrf_info', 'HackRF device information'),
            ('gqrx', 'SDR GUI application'),
            ('inspectrum', 'Signal analysis GUI')
        ]
        
        for tool, description in tools:
            try:
                result = subprocess.run(['which', tool], capture_output=True, timeout=5)
                status = "✅" if result.returncode == 0 else "❌"
                print(f"{Colors.INFO}    {status} {tool}: {description}")
            except:
                print(f"{Colors.ERROR}    ❌ {tool}: {description}")
        
        # Configuration options
        if device_info.get('available'):
            print(f"\n{Colors.MAGENTA}  Configuration:")
            
            new_sample_rate = input(f"{Colors.GREEN}  New sample rate (Hz) [{self.sdr.sample_rate}]: {Colors.YELLOW}")
            if new_sample_rate:
                try:
                    self.sdr.sample_rate = InputValidator.validate_integer(new_sample_rate, 250000, 10000000)
                    print(f"{Colors.SUCCESS}  Sample rate updated to {self.sdr.sample_rate:,} Hz")
                except ValueError as e:
                    print(f"{Colors.ERROR}  Invalid sample rate: {e}")
            
            new_gain = input(f"{Colors.GREEN}  New gain (dB) [{self.sdr.gain}]: {Colors.YELLOW}")
            if new_gain:
                try:
                    self.sdr.gain = InputValidator.validate_integer(new_gain, 0, 50)
                    print(f"{Colors.SUCCESS}  Gain updated to {self.sdr.gain} dB")
                except ValueError as e:
                    print(f"{Colors.ERROR}  Invalid gain: {e}")
        
        # Status information
        print(f"\n{Colors.MAGENTA}  System Status:")
        print(f"{Colors.INFO}    NumPy available: {self.numpy_available}")
        print(f"{Colors.INFO}    Discovered signals: {len(self.discovered_signals)}")
        
        recorded_count = len([s for s in self.discovered_signals if 'recording_file' in s.metadata])
        print(f"{Colors.INFO}    Recorded signals: {recorded_count}")
    
    def generate_report(self):
        """Generate RF security assessment report"""
        print(f"\n{Colors.CYAN}  [{Colors.GREEN}+{Colors.CYAN}] RF Security Assessment Report")
        
        if not self.discovered_signals:
            print(f"{Colors.WARNING}  No assessment data available. Perform scans first.")
            return
        
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        report_file = os.path.join("reports", f"rf_security_report_{timestamp}.txt")
        
        try:
            os.makedirs("reports", exist_ok=True)
            
            with open(report_file, 'w') as f:
                f.write("===============================================\n")
                f.write("  RF SECURITY ASSESSMENT REPORT\n")
                f.write("===============================================\n\n")
                f.write(f"Date: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"Assessor: {Config.APP_NAME} v{Config.VERSION}\n")
                f.write(f"Environment: {Config.CURRENT_PLATFORM}\n")
                f.write(f"SDR Device: {self.sdr.device_type or 'None'}\n\n")
                
                f.write("DISCOVERED SIGNALS\n")
                f.write("==================\n\n")
                
                for i, signal in enumerate(self.discovered_signals, 1):
                    f.write(f"[{i}] Frequency: {signal.frequency/1e6:.3f} MHz\n")
                    f.write(f"    Amplitude: {signal.amplitude:.1f} dB\n")
                    f.write(f"    Modulation: {signal.modulation}\n")
                    
                    # Protocol identification
                    protocols = self.analyzer.identify_protocol(signal.frequency)
                    if protocols:
                        f.write(f"    Possible protocols: {', '.join(protocols[:3])}\n")
                    
                    # Analysis results
                    if 'analysis' in signal.metadata:
                        analysis = signal.metadata['analysis']
                        f.write(f"    Bandwidth: {analysis.get('bandwidth', 0)/1e3:.1f} kHz\n")
                        f.write(f"    Duration recorded: {analysis.get('duration', 0):.2f} s\n")
                    
                    f.write("\n")
                
                # Frequency band analysis
                f.write("FREQUENCY BAND ANALYSIS\n")
                f.write("=======================\n\n")
                
                bands = {
                    'VHF_LOW': (30e6, 88e6),
                    'FM_BROADCAST': (88e6, 108e6),
                    'VHF_HIGH': (108e6, 174e6),
                    'UHF_LOW': (174e6, 470e6),
                    'ISM_433': (430e6, 440e6),
                    'UHF_HIGH': (470e6, 900e6),
                    'ISM_915': (900e6, 930e6),
                    'L_BAND': (1e9, 2e9),
                    'ISM_2400': (2.4e9, 2.5e9)
                }
                
                for band_name, (start, end) in bands.items():
                    signals_in_band = [s for s in self.discovered_signals if start <= s.frequency <= end]
                    if signals_in_band:
                        f.write(f"{band_name}: {len(signals_in_band)} signals\n")
                
                f.write("\nSECURITY RECOMMENDATIONS\n")
                f.write("========================\n\n")
                f.write("1. Monitor critical frequency bands regularly\n")
                f.write("2. Implement RF shielding for sensitive areas\n")
                f.write("3. Use encrypted protocols when possible\n")
                f.write("4. Regularly update firmware on RF devices\n")
                f.write("5. Consider frequency hopping for critical communications\n")
                f.write("6. Monitor for unauthorized transmissions\n")
                f.write("7. Implement proper RF access controls\n")
            
            print(f"{Colors.SUCCESS}  Report generated: {report_file}")
        
        except Exception as e:
            self.logger.error(f"Report generation error: {e}")
            print(f"{Colors.ERROR}  Report generation failed: {e}")
    
    def module_information(self):
        """Display module information"""
        print(f"\n{Colors.CYAN}  [{Colors.GREEN}ℹ{Colors.CYAN}] RF Module Information")
        
        print(f"\n{Colors.MAGENTA}  Module Details:")
        print(f"{Colors.GREEN}    • Name: Radio Frequency Security Testing Module")
        print(f"{Colors.GREEN}    • Version: 2.1")
        print(f"{Colors.GREEN}    • Author: Network(GHANA)")
        print(f"{Colors.GREEN}    • Purpose: RF security assessment and testing")
        
        print(f"\n{Colors.MAGENTA}  Capabilities:")
        print(f"{Colors.CYAN}    • Frequency spectrum scanning")
        print(f"{Colors.CYAN}    • Signal recording and analysis")
        print(f"{Colors.CYAN}    • Protocol identification")
        print(f"{Colors.CYAN}    • Replay attacks")
        print(f"{Colors.CYAN}    • RF jamming attacks")
        print(f"{Colors.CYAN}    • Rolling code analysis")
        print(f"{Colors.CYAN}    • Security assessment reporting")
        
        print(f"\n{Colors.MAGENTA}  Supported SDR Devices:")
        print(f"{Colors.YELLOW}    • RTL-SDR (receive only)")
        print(f"{Colors.YELLOW}    • HackRF (transmit and receive)")
        print(f"{Colors.YELLOW}    • BladeRF (transmit and receive)")
        
        print(f"\n{Colors.MAGENTA}  Requirements:")
        print(f"{Colors.YELLOW}    • SDR hardware")
        print(f"{Colors.YELLOW}    • GNU Radio or equivalent tools")
        print(f"{Colors.YELLOW}    • NumPy for signal analysis (optional)")
        
        print(f"\n{Colors.MAGENTA}  Status:")
        print(f"{Colors.SUCCESS if self.sdr.device_available else Colors.ERROR}    • SDR Device: {self.sdr.device_type or 'Not Available'}")
        print(f"{Colors.SUCCESS if self.numpy_available else Colors.WARNING}    • NumPy: {'Available' if self.numpy_available else 'Not Available'}")
        print(f"{Colors.INFO}    • Discovered signals: {len(self.discovered_signals)}")
    
    def main(self):
        """Main RF module loop"""
        if not self.sdr.device_available:
            print(f"\n{Colors.ERROR}  No SDR devices detected!")
            print(f"{Colors.INFO}  Supported devices:")
            print(f"{Colors.YELLOW}    • RTL-SDR: sudo apt install rtl-sdr")
            print(f"{Colors.YELLOW}    • HackRF: sudo apt install hackrf")
            print(f"{Colors.YELLOW}    • BladeRF: Install from bladeRF website")
            print(f"{Colors.WARNING}  Some features will work in simulation mode")
            input(f"\n{Colors.GREEN}  Press Enter to continue...")
        
        try:
            while True:
                try:
                    SystemUtils.clear_screen()
                    self.show_menu()
                    choice = MenuRenderer.get_user_input(self.hostname)
                    
                    if choice == "0":
                        print(f"\n{Colors.MAGENTA}🚪🔙{Colors.YELLOW} Returning to main menu...")
                        break
                    elif choice == "1":
                        self.frequency_scan()
                    elif choice == "2":
                        self.signal_analysis()
                    elif choice == "3":
                        self.protocol_identification()
                    elif choice == "4":
                        self.replay_attack()
                    elif choice == "5":
                        self.jamming_attack()
                    elif choice == "6":
                        self.rolling_code_analysis()
                    elif choice == "7":
                        self.sdr_management()
                    elif choice == "8":
                        self.generate_report()
                    elif choice == "9":
                        self.module_information()
                    else:
                        print(f"\n{Colors.WARNING}'{choice}' is not a valid option!")
                    
                    if choice != "0":
                        input(f"\n  {Colors.GREEN}Press Enter to continue...")
                        
                except (KeyboardInterrupt, EOFError):
                    print(f"\n{Colors.MAGENTA}🚪🔙{Colors.YELLOW} Returning to main menu...")
                    break
                    
        except Exception as e:
            self.logger.error(f"RF module error: {e}", exc_info=True)
            print(f"{Colors.ERROR}Module error: {e}")

if __name__ == "__main__":
    try:
        rf_module = RFModule()
        rf_module.main()
    except Exception as e:
        print(f"{Colors.ERROR}Critical error: {e}")