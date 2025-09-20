```
 _  _  _   _    __    ____  _  _  ____  ___  ____  ____  ____ 
( \/ )( )_( )  /__\  (  _ \( \/ )( ___)/ __)(_  _)( ___)(  _ \
 )  (  ) _ (  /(__)\  )   / \  /  )__) \__ \  )(   )__)  )   /
(_/\_)(_) (_)(__)(__)(_)\_)  \/  (____)(___/ (__) (____)(_)\_)
```
⚡ xharvester is a specialized, Python-based reconnaissance and exploitation suite designed for security assessments of radio frequency (RF), wireless(bluetooth & wifi), industrial control system(scada), and automotive systems. It integrates multiple tools and scripts into a unified workflow for probing, analyzing, and documenting findings from the physical and wireless world.

## Overview
Moving beyond traditional web OSINT, xHarvester allows security researchers, red teams, and penetration testers to interact with the electromagnetic spectrum. It provides a structured approach to discovering, fingerprinting, exploiting and assessing the security posture of devices ranging from WiFi routers and Bluetooth peripherals to critical Industrial Control Systems (ICS) and modern automobiles vehicles.

## ✨ Core Framework Features
Unified Command & Control: A single Python-based interface to orchestrate a wide array of specialized hardware and software tools.

Modular Architecture: Enables users to run xharvestor in full-spectrum.

Automated Evidence Collection: Automatically saves all findings in structured, standardized formats:

Raw Data Format: PCAP files, IQ recordings (*.bin), CAN bus logs, & etc.

Structured Reports: Comprehensive reports in HTML, JSON, and Markdown for easy integration into deliverables.

Geotagging Integration: Correlates all discovered devices and signals with GPS coordinates (when a receiver is available) for mapping and analysis.

Hardware Abstraction Layer: Simplifies the use of complex hardware (SDRs, CAN interfaces) by handling driver communication and configuration automatically.

🛠️ Installation Guide
### **Clone the Repository**
```bash
git clone https://github.com/n3tworkh4x/xharvester.git
cd xharvester
```
### **Virtual Environment Setup**
##### **🍎 MacOS/ 🐧 Linux**
```
python3 -m venv venv
source venv/bin/activate
```
#### **🪟 Windows**
```
###### Powershell ######
python -m venv venv
.\venv\Scripts\Activate.ps1
```
```
###### Command Prompt ######
python -m venv venv
.\venv\Scripts\activate.bat
```
### **Installing Requirements**
```
pip install -r requirements.txt
```
***External Requirements***
#### 🍎 macOS
``` 
brew install dbus bluez
pip install pyobjc==9.2
```
#### 🐧 Ubuntu/Debian
```
sudo apt update
sudo apt install libdbus-1-dev libgirepository1.0-dev libcairo2-dev \
libbluetooth-dev bluez
pip install PyBluez==0.30 dbus-python==1.3.2 pydbus==0.6.0 PyGObject==3.48.1 pycairo==1.26.0
sudo apt update
sudo apt install aircrack-ng hostapd dnsmasq iptables
```

#### **⚡ Usage Notes**
#### Multi OS CLI Base Tool For Recon & Exploitation
##### 🍎 MacOS/ 🐧 Linux
```
sudo ./xharvester 
```
##### 🪟 Windows
**Open Git or Command Prompt with Administration & Type:```python xharvester``` in the location of the tool.**

##### 🤖 Android (Termux)
###### Installation Of Termux From Play Store
```
Install from Google Play Store (Recommended)

    1. Open the Google Play Store app on your Android device.

    2. Search for Termux.

    3. Select the app published by Fredrik Fornwall.

    4. Tap Install.

    5. Once installed, open Termux from your app drawer
```

###### Upgrade, Installation & Execution
```
pkg update && pkg upgrade -y
pkg install git python tsu -y 
git clone https://github.com/n3tworkh4x/xharvester.git
cd xharvester
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
tsu ./xharvester
```

### 💝 Support Xharvester's Growth
**🚀 If Xharvester helps you, consider [sponsoring](https://ko-fi.com/n3twork) -- 100% of support goes to keeping it free forever.**

- **$5/month**: Coffie Tier ☕
- **$25/month**: Bug Prioritizer 🐛


#### **📌 Disclaimer**
This tool is intended for authorized security testing and educational purposes only. Interfering with wireless signals, industrial processes, or vehicle systems without explicit permission is illegal, extremely dangerous, and can lead to physical harm, catastrophic failure, and severe legal consequences. Always operate within a controlled, legal environment.
