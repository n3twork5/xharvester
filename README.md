```
 _  _  _   _    __    ____  _  _  ____  ___  ____  ____  ____ 
( \/ )( )_( )  /__\  (  _ \( \/ )( ___)/ __)(_  _)( ___)(  _ \
 )  (  ) _ (  /(__)\  )   / \  /  )__) \__ \  )(   )__)  )   /
(_/\_)(_) (_)(__)(__)(_)\_)  \/  (____)(___/ (__) (____)(_)\_)
```

# xharvester v1.0 - Cross-Platform Edition

⚡ **xharvester v1.0** is a cross-platform enhanced Python-based reconnaissance and exploitation suite designed for security assessments of radio frequency (RF), wireless (Bluetooth & WiFi), industrial control systems (SCADA), and automotive systems with **automatic GitHub updates** and **full Android/Termux & IOS/a-Shell support**!

### 🆕 Features
- **🔄 Auto-Update System**: Option 99 now downloads latest version from GitHub automatically
- **📱 Android/Termux Support**: Full compatibility with Android devices using Termux
- **🍏 iOS/iPadOS Support**: Native support for a-Shell and iSH apps with Shortcuts integration
- **🖥️ Desktop Integration**: Click-to-launch desktop shortcuts for all platforms (Linux/macOS/Windows/iOS/Android)
- **🌍 Cross-Platform Detection**: Automatic platform detection (Linux/Windows/macOS/iOS/Android)
- **Platform-Specific Security**: Adaptive security based on platform capabilities
- **💾 Backup & Restore**: Automatic backup creation during updates with rollback support
- **📋 Version Management**: Smart version comparison and update notifications
- **🚗 Professional Automotive Module**: Based on "The Car Hacker's Handbook" by Craig Smith, Go search and learn more and unlock the hidden feautures of your vehicle
- **🍎 App Bundle Integration**: Native macOS app bundles with Spotlight and Dock support
- **📡 5 Complete Security Modules**: Bluetooth, WiFi, Automotive, RF, and SCADA/ICS testing

## Overview
Moving beyond traditional web OSINT, xharvester allows security researchers, red teams, and penetration testers to interact with the electromagnetic spectrum. It provides a structured approach to discovering, fingerprinting, exploiting and assessing the security posture of devices ranging from WiFi routers and Bluetooth peripherals to critical Industrial Control Systems (ICS) and modern automotive vehicles.

## 📁 Project Structure

```
xharvester/
├── config.py                     # Centralized configuration management
├── utils.py                      # Shared utilities and helper functions
├── update_manager.py             # GitHub auto-update system
├── xharvester                    # Main application (cross-platform)
├── install_android.sh            # Android/Termux installation script
├── install_ios.sh                # iOS/a-Shell installation script
├── install_desktop_integration   # Universal desktop integration installer
├── modules/
│   ├── automobile_module.py       # Professional automotive security testing
│   ├── bluetooth_module.py        # Bluetooth security testing
│   ├── wifi_module.py             # WiFi security testing
│   ├── rf_module.py               # Radio frequency security testing
│   └── scada_module.py            # SCADA/ICS security testing
├── icons/                        # Desktop integration icons and installers
│   ├── linux/                    # Linux desktop integration
│   ├── macos/                     # macOS app bundle integration
│   ├── windows/                   # Windows shortcuts integration
│   ├── android/                   # Android/Termux integration
│   └── *.png, *.ico               # Platform-specific icons
├── logs/                         # Application logs directory
├── reports/                      # Security assessment reports
├── backups/                      # Update backups directory
├── requirements.txt              # Python dependencies
└── README.md                     # This file
```

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
### Installing Requirements
```
pip install -r requirements.txt
```

### 🖥️ Desktop Integration (Optional)

**Launch xharvester from your desktop environment with a single click!**

```bash
# Universal installer (auto-detects OS)
./install_desktop_integration

# Creates desktop shortcuts, application menu entries, and command-line integration
# Supports: Linux, macOS, Windows, iOS, Android
```

**What gets installed:**
- 🐧 **Linux**: Application launcher entry, desktop integration, "Run as Root" option
- 🍎 **macOS**: Native app bundle, Spotlight search, Dock integration
- 🦾 **Windows**: Start Menu shortcuts, desktop icon, "Run as Administrator" option
- 🍏 **iOS**: a-Shell integration, Shortcuts app support, home screen widget
- 🤖 **Android**: Termux widget, command-line integration, root mode support

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

##### 🍎 iOS/iPadOS (a-Shell/iSH)
###### Installation of a-Shell from App Store
```
Install a-Shell or a-Shell mini from App Store:

    1. Open the App Store on your iOS/iPadOS device
    
    2. Search for "a-Shell" or "a-Shell mini"
    
    3. Install the app by Nicolas Holzschuch
    
    4. Alternative: Install iSH (Alpine Linux terminal)
```

###### Installation & Execution
```
# In a-Shell or iSH terminal:
git clone https://github.com/n3tworkh4x/xharvester.git
cd xharvester

# Run iOS-specific installer
./install_ios.sh

# Launch xharvester
xharvester

# Or use iOS-optimized version
xharvester-ios
```

###### iOS Shortcuts Integration
```
For home screen access:

    1. Run the iOS installer: ./install_ios.sh
    
    2. Install "Shortcuts" app (if not already installed)
    
    3. Import the generated shortcut file
    
    4. Add xharvester widget to home screen
```

### 💝 Support Xharvester's Growth
**🚀 If Xharvester helps you, consider [sponsoring](https://ko-fi.com/n3twork) -- 100% of support goes to keeping it free forever.**

- **$5/month**: Coffie Tier ☕
- **$25/month**: 

Any Feedback and Suggestions? Consider Gmailing Me: [networkmandaean@gmail.com](mailto:networkmandaean@gmail.com)

#### **📌 Disclaimer**
This tool is intended for authorized security testing and educational purposes only. Interfering with wireless signals, industrial processes, or vehicle systems without explicit permission is illegal, extremely dangerous, and can lead to physical harm, and severe legal consequences. Always operate within a controlled and legal environment.
#### **💡 One Of My Best Taglines ** 
**** The Quieter You Become, The More You Are Able To Hear ****
