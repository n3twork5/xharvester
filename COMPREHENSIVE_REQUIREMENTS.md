# xharvester v1.0 - Comprehensive Requirements Guide
## Cross-Platform Security Testing Requirements & Hardware Tools

> **⚠️ LEGAL DISCLAIMER**: This tool is for authorized security testing and educational purposes only. Using these tools and techniques without explicit permission is illegal and can result in severe legal consequences.

---

## 📋 Table of Contents

1. [Platform-Specific Requirements](#platform-specific-requirements)
2. [Module-Specific Hardware Requirements](#module-specific-hardware-requirements)
3. [Software Dependencies](#software-dependencies)
4. [Hardware Tools for Professional Testing](#hardware-tools-for-professional-testing)
5. [Installation Commands by Platform](#installation-commands-by-platform)
6. [Attack Scenarios & Required Equipment](#attack-scenarios--required-equipment)

---

## 🖥️ Platform-Specific Requirements

### 🐧 **Linux (Recommended: Kali Linux, Ubuntu, Debian)**
**Minimum System Requirements:**
- CPU: 2+ cores, 2.0 GHz
- RAM: 4GB minimum, 8GB recommended
- Storage: 20GB free space
- USB 3.0 ports for hardware tools

**Required System Packages:**
```bash
# Core utilities
sudo apt update && sudo apt install -y \
    python3 python3-pip python3-venv git build-essential \
    libdbus-1-dev libgirepository1.0-dev libcairo2-dev \
    libbluetooth-dev bluez bluez-tools

# WiFi testing tools
sudo apt install -y aircrack-ng hostapd dnsmasq iptables \
    hcxdumptool hcxtools reaver pixiewps wifite

# Bluetooth tools
sudo apt install -y bluez-hcidump bluez-tools btscanner \
    bluetoothctl spooftooph l2ping

# RF/SDR tools
sudo apt install -y rtl-sdr hackrf bladerf gqrx \
    rtl-433 multimon-ng dump1090-fa

# CAN tools (Automotive)
sudo apt install -y can-utils linux-modules-extra-$(uname -r)

# Industrial/SCADA tools
sudo apt install -y nmap python3-scapy wireshark
```

### 🍎 **macOS**
**Minimum System Requirements:**
- macOS 10.15+ (Catalina or newer)
- 8GB RAM, 16GB recommended
- 30GB free space
- Thunderbolt/USB-C ports

**Required Dependencies:**
```bash
# Install Homebrew first
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# System dependencies
brew install python3 git dbus bluez pkg-config cairo gobject-introspection

# Python dependencies
pip3 install pyobjc>=9.2
```

### 🪟 **Windows**
**Minimum System Requirements:**
- Windows 10/11 (64-bit)
- 8GB RAM
- 30GB free space
- Administrator privileges

**Required Software:**
- Python 3.8+ from microsoft store or python.org
- Git for Windows
- Visual Studio Build Tools
- Windows Subsystem for Linux (WSL2) for advanced features

### 🤖 **Android (Termux)**
**Requirements:**
- Android 7.0+ (API 24+)
- 4GB RAM minimum
- 8GB free storage
- Root access (recommended)

**Installation:**
```bash
# Update Termux
pkg update && pkg upgrade -y

# Install dependencies
pkg install git python tsu root-repo -y
pkg install nmap aircrack-ng -y
```

### 🍏 **iOS/iPadOS (a-Shell/iSH)**
**Requirements:**
- iOS 13+ or iPadOS 13+
- a-Shell or iSH app from App Store
- 4GB device storage
- Limited functionality (no root access)

---

## 🔧 Module-Specific Hardware Requirements

### 📱 **Bluetooth Module Hardware**

**Required Hardware:**
- **Built-in Bluetooth adapter** (minimum)
- **USB Bluetooth dongles** (recommended for multiple adapters):
  - CSR8510 chipset dongles (€5-15)
  - Asus USB-BT400 (€15-25)
  - Intel AX200 (€20-30)

**Professional Hardware:**
- **Ubertooth One** (€100-150): Bluetooth Low Energy (BLE) monitoring
- **HackRF One** (€300-400): Wide-spectrum Bluetooth analysis
- **BladeRF 2.0 micro** (€500-600): Advanced RF analysis
- **Flipper Zero** (€150-200): Multi-protocol device testing

**Attack Capabilities:**
- Device discovery and enumeration
- Service fingerprinting
- BlueBorne vulnerability testing
- PIN/key attacks
- Proximity-based attacks

### 🛜 **WiFi Module Hardware**

**Required Hardware:**
- **USB WiFi adapter with monitor mode support**:
  - **Alfa AWUS036ACS** (€30-50): Dual-band, excellent range
  - **Alfa AWUS036NHA** (€25-40): 2.4GHz, high power
  - **Panda PAU09** (€15-25): Budget option
  - **TP-Link AC600 T2U Plus** (€20-30): Dual-band

**Professional Hardware:**
- **WiFi Pineapple Mark VII** (€200-300): Automated pentest platform
- **Hak5 Packet Squirrel** (€60-80): Network implant
- **Directional antennas** (€50-200): Long-range attacks
- **High-gain omni antennas** (€30-100): 360° coverage

**Attack Capabilities:**
- WPA/WPA2/WPA3 handshake capture
- Evil twin access points
- Deauthentication attacks
- KRACK vulnerability testing
- Captive portal attacks

### 🚗 **Automotive Module Hardware**

**Required Hardware:**
- **OBD-II Interface**:
  - **ELM327 Bluetooth/WiFi** (€10-30): Basic diagnostics
  - **CANtact Pro** (€200-300): Professional CAN analysis
  - **ValueCAN 4-1** (€800-1200): Multi-protocol interface

**Professional Hardware:**
- **CANbus Triple** (€150-250): Multi-CAN interface
- **Red Pitaya** (€400-600): Automotive signal analysis
- **ChipWhisperer** (€300-500): ECU security analysis
- **J2534 Pass-Thru Device** (€500-1500): OEM-level access

**Vehicle Requirements:**
- CAN bus access (OBD-II port)
- Modern vehicle (2008+)
- Safe, controlled environment
- **Legal authorization required**

**Attack Capabilities:**
- CAN bus monitoring and injection
- ECU fingerprinting
- Diagnostic protocol fuzzing
- Instrument cluster manipulation
- Engine control attacks (DANGEROUS)

### 📡 **Radio Frequency (RF) Module Hardware**

**Required Hardware (Choose One):**
- **RTL-SDR dongles** (€20-40):
  - RTL-SDR Blog V3 (recommended)
  - NooElec NESDR series
  - Frequency range: 500 kHz - 1.7 GHz

**Professional Hardware:**
- **HackRF One** (€300-400): TX/RX, 1 MHz - 6 GHz
- **BladeRF 2.0** (€500-600): High-performance SDR
- **USRP B200mini** (€700-900): Research-grade SDR
- **LimeSDR** (€300-500): Open-source SDR

**Antennas & Accessories:**
- **Discone antenna** (€50-150): Wideband receiving
- **Yagi antennas** (€30-200): Directional, various frequencies
- **Telescopic whip antennas** (€10-30): Portable
- **SMA/BNC adapters** (€20-50): Connector compatibility

**Attack Capabilities:**
- ISM band analysis (433/868/915 MHz)
- Garage door/car key attacks
- RFID/NFC analysis
- Cellular protocol monitoring
- Emergency services monitoring (legal restrictions apply)

### 🏭 **Industrial/SCADA Module Hardware**

**Network Hardware:**
- **Ethernet adapters** (built-in sufficient)
- **Serial-to-USB converters** (€10-30): RS232/RS485 access
- **Industrial network taps** (€500-2000): Professional monitoring

**Professional Hardware:**
- **Modbus RTU/TCP analyzers** (€300-1000)
- **PLC programming cables** (€50-300): Vendor-specific
- **Industrial HMI devices** (€1000-5000): Full system testing
- **Network packet brokers** (€2000-10000): Advanced analysis

**Attack Capabilities:**
- Modbus device discovery
- PLC program analysis
- HMI credential attacks
- Industrial protocol fuzzing
- SCADA system reconnaissance

---

## 📦 Software Dependencies

### Core Python Requirements
```txt
# Essential packages (from requirements.txt)
requests>=2.31.0
numpy>=1.24.3
urllib3>=2.0.0
bleak>=0.20.0          # Bluetooth Low Energy
scapy>=2.5.0           # Packet manipulation
python-snap7>=1.0      # SCADA/PLC communication
pymodbus>=3.5.4        # Modbus protocol
can>=0.0.0             # CAN bus interface
pyrtlsdr>=0.3.0        # RTL-SDR interface
colorama>=0.4.0        # Terminal colors
netifaces>=0.11.0      # Network interfaces

# Platform-specific (Linux)
dbus-python==1.3.2
pydbus==0.6.0
PyGObject==3.48.1
pycairo==1.26.0

# Platform-specific (macOS)
pyobjc>=9.2
```

### System-Level Tools by Platform

#### Kali Linux (Complete Suite)
```bash
# Already includes most tools, additional packages:
sudo apt install -y \
    gr-osmosdr gr-fosphor gqrx-sdr \
    chirp hackrf bladerf \
    can-utils cansniffer canutils-dev
```

#### Ubuntu/Debian
```bash
# Full installation command
sudo apt update && sudo apt install -y \
    aircrack-ng hostapd dnsmasq iptables \
    bluez bluez-tools bluez-hcidump \
    rtl-sdr hackrf bladerf \
    can-utils python3-can \
    nmap wireshark python3-scapy \
    git python3-pip python3-venv
```

#### Arch Linux
```bash
# AUR packages required
yay -S rtl-sdr-git hackrf bladerf \
       aircrack-ng bluez-tools \
       python-can can-utils
```

---

## 💰 Hardware Budget Guide

### 🎯 **Beginner Setup** (€100-200)
- USB WiFi adapter with monitor mode: €30-50
- RTL-SDR dongle with antennas: €25-40
- Basic Bluetooth dongle: €10-20
- ELM327 OBD-II adapter: €15-30
- **Total: ~€150**

### 🔧 **Intermediate Setup** (€500-800)
- Alfa AWUS036ACS WiFi adapter: €40
- HackRF One SDR: €350
- Ubertooth One: €120
- CANtact Pro: €200
- Professional antennas: €100
- **Total: ~€810**

### 🏆 **Professional Setup** (€2000-5000)
- WiFi Pineapple Mark VII: €250
- BladeRF 2.0 micro: €600
- ValueCAN 4-1: €1000
- Professional antenna array: €500
- Industrial testing equipment: €1500+
- **Total: €3850+**

---

## 🎯 Attack Scenarios & Required Equipment

### **WiFi Penetration Testing**
**Equipment:** Monitor-mode WiFi adapter, directional antenna
**Attacks:** WPA handshake capture, evil twin AP, deauth attacks
**Legal:** Requires written authorization

### **Bluetooth Security Assessment**
**Equipment:** Multiple BT adapters, Ubertooth One (for BLE)
**Attacks:** Device enumeration, service exploitation, proximity attacks
**Legal:** Only test owned/authorized devices

### **Automotive Security Testing**
**Equipment:** OBD-II interface, CAN analysis tools
**Attacks:** ECU fingerprinting, CAN injection, diagnostic fuzzing
**Legal:** Only on owned vehicles in controlled environment

### **RF Security Analysis**
**Equipment:** SDR (HackRF/RTL-SDR), appropriate antennas
**Attacks:** Signal analysis, replay attacks, protocol reverse engineering
**Legal:** Strong regulations - monitor only authorized frequencies

### **Industrial System Assessment**
**Equipment:** Network access, Modbus analyzers
**Attacks:** Device discovery, protocol analysis, credential attacks
**Legal:** Critical infrastructure - requires explicit authorization

---

## 🚨 Important Safety & Legal Considerations

1. **🏛️ Legal Authorization Required**: Never test systems you don't own or lack explicit written permission to test
2. **🚗 Automotive Safety**: Vehicle testing must be performed in safe, controlled environments
3. **📡 RF Regulations**: Respect local RF transmission laws and frequency allocations
4. **🏭 Industrial Safety**: Industrial system testing can affect critical infrastructure
5. **📝 Documentation**: Always document testing activities and maintain proper evidence

---

## 📞 Support & Community

- **GitHub Issues**: Report bugs and feature requests
- **Documentation**: Refer to module-specific README files
- **Legal Questions**: Consult with cybersecurity legal experts
- **Hardware Support**: Check manufacturer specifications and compatibility

**Remember**: With great power comes great responsibility. Use these tools ethically and legally! 🛡️