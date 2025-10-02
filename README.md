```
 _  _  _   _    __    ____  _  _  ____  ___  ____  ____  ____ 
( \/ )( )_( )  /__\  (  _ \( \/ )( ___)/ __)(_  _)( ___)(  _ \
 )  (  ) _ (  /(__)\  )   / \  /  )__) \__ \  )(   )__)  )   /
(_/\_)(_) (_)(__)(__)(_)\_)  \/  (____)(___/ (__) (____)(_)\_)
```
⚡ **xharvester v1.0** is a cross-platform enhanced Python-based reconnaissance and exploitation suite designed for security assessments of radio frequency (RF), wireless (Bluetooth & WiFi), industrial control systems (SCADA), and automotive systems with **automatic GitHub updates** and **full Android/Termux & IOS/a-Shell support**!

### Features
- **🔄 Auto-Update System**: Option 99 now downloads latest version from GitHub automatically.
- **Preventing Attacks**: **Generate Security Report** option gives a brief knowledage of **rules to protect individuals against the threat module(Wi-Fi MODULE)**.
- **🤖 Android/Termux Support**: Full compatibility with Android devices using Termux.
- **🍏 iOS/iPadOS Support**: Native support for a-Shell and iSH apps with Shortcuts integration.
- **🌍 Cross-Platform Detection**: Automatic platform detection (Linux/Windows/macOS/iOS/Android).
- **Platform-Specific Security**: Adaptive security based on platform capabilities.
- **💾 Backup & Restore**: Automatic backup creation during updates with rollback support.
- **🚗 Professional Automotive Module**: Based on "The Car Hacker's Handbook" by Craig Smith, Go search and learn more and unlock the hidden feautures of your vehicle.
- **5 Complete Security Modules**: Bluetooth, WiFi, Automotive, RF, and SCADA/ICS testing.

## Overview
Moving beyond traditional web OSINT & exploitations, xharvester allows security researchers, red teams, and penetration testers to interact with the electromagnetic spectrum. It provides a structured approach to discovering, fingerprinting, exploiting and assessing the security posture of devices ranging from WiFi routers and Bluetooth peripherals to critical Industrial Control Systems (ICS), modern automotive vehicles and radio frequency(RF).

## ✨ Core Framework Features
Unified Command & Control: A single Python-based interface to orchestrate a wide array of specialized hardware and software tools.

Modular Architecture: Enables users to run xharvestor in full-spectrum with a key.

Automated Evidence Collection: Automatically saves all findings in structured, standardized formats:

Raw Data Format: PCAP files, IQ recordings (*.bin), CAN bus logs, & etc.

Structured Reports: Comprehensive reports in HTML, JSON, and Markdown for easy integration into deliverables.

Geotagging Integration: Correlates all discovered devices and signals with GPS coordinates (when a receiver is available) for mapping and analysis.

Hardware Abstraction Layer: Simplifies the use of complex hardware (SDRs, CAN interfaces) by handling driver communication and configuration automatically.

## 🛠️ Installation Guide
### **Clone the Repository**
```bash
git clone https://github.com/n3twork5/xharvester.git
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
#In termux terminal:

pkg update && pkg upgrade -y
pkg install git python tsu aircrack-ng iptables hostapd dnsmasq -y 
git clone https://github.com/n3twork5/xharvester.git
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

###### Upgrade, Installation & Execution
```
# In a-Shell or iSH terminal:

pkg update && pkg upgrade -y
pkg install git python tsu aircrack-ng iptables hostapd dnsmasq -y
git clone https://github.com/n3twork5/xharvester.git
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

### Simulation for Automobile Network
Instrument Cluster Simulator for SocketCAN
------------------------------------------

By: OpenGarages <agent.craig@gmail.com>

Compiling
---------
You will need:
* SDL2
* SDL2_Image
* can-utils

You can get can-utils from github or on Ubuntu you may run the following

```
  sudo apt-get install libsdl2-dev libsdl2-image-dev can-utils  
```

With dependencies installed, you may use the [Meson build system](https://mesonbuild.com/) to build the project:

```
  meson setup builddir && cd builddir
  meson compile
```

Testing on a virtual CAN interface
----------------------------------
You can run the following commands to setup a virtual can interface

```
  sudo modprobe can
  sudo modprobe vcan
  sudo ip link add dev vcan0 type vcan
  sudo ip link set up vcan0
```

If you type ifconfig vcan0 you should see a vcan0 interface. A setup_vcan.sh file has also been provided with this
repo.

Usage
-----
Default operations:

Start the Instrument Cluster (IC) simulator:

```
  ./icsim vcan0
```

Then startup the controls

```
  ./controls vcan0
```

The hard coded defaults should be in sync and the controls should control the IC.  Ideally use a controller similar to
an XBox controller to interact with the controls interface.  The controls app will generate corrosponding CAN packets
based on the buttons you press.  The IC Sim sniffs the CAN and looks for relevant CAN packets that would change the
display.

Troubleshooting
---------------
* If you get an error about canplayer then you may not have can-utils properly installed and in your path.
* If the controller does not seem to be responding make sure the controls window is selected and active

## lib.o not linking
If lib.o doesn't link it's probably because it's the wrong arch for your platform.  To fix this you will
want to compile can-utils and copy the newly compiled lib.o to the icsim directory.  You can get can-utils
from: https://github.com/linux-can/can-utils

## read: Bad address
When running `./icsim vcan0` you end up getting a `read: Bad Address` message,
this is typically a result of needing to recompile with updated SDL libraries.
Make sure you have the recommended latest SDL2 libraries.  Some users have
reported fixing this problem by creating symlinks to the SDL.h files manually
or you could edit the Makefile and change the CFLAGS to point to wherever your
distro installs the SDL.h header, ie: /usr/include/x86_64-linux-gnu/SDL2

There was also a report that on Arch linux needed sdl2_gfx library.

CAN Hacking Training Usage
--------------------------
To *safely* train on CAN hacking you can play back a sample recording included in this repo of generic CAN traffic.  This will
create something similar to normal CAN "noise".  Then start the IC Sim with the -r (randomize) switch.

```
  ./icsim -r vcan0
  Using CAN interface vcan0
  Seed: 1401717026
```

Now copy the seed number and paste it as the -s (seed) option for the controls.

```
  ./controls -s 1401717026 vcan0
```

This will randomize what CAN packets the IC needs and by passing the seed to the controls they will sync.  Randomizing
changes the arbitration IDs as well as the byte position of the packets used.  This will give you experience in hunting down
different types of CAN packets on the CAN Bus.

For the most realistic training you can change the difficulty levels.  Set the difficulty to 2 with the controls:

```
  ./controls -s 1401717026 -l 2 vcan0
```

This will add additional randomization to the target packets, simulating other data stored in the same arbitration id.




### 💝 Support Xharvester's Growth
**🚀 If xharvester helps you, consider [sponsoring](https://n3twork5.github.io/BoostBond/) -- 100% of support goes to keeping it free forever.**

### Feedback & Suggestions
**Any Feedback and Suggestions? Consider contacting: [Me](mailto:networkmandaean@gmail.com)  --  Make sure you get the tools in need for yourself as well, because most complex attacks will require specific hardware tool to support it functionalities.**

#### **📌 Disclaimer**
This tool is intended for authorized security testing and educational purposes only. Interfering with wireless signals, industrial processes, or vehicle systems without explicit permission is illegal, extremely dangerous, and can lead to physical harm, and severe legal consequences. Always operate within a controlled and legal environment.
#### 💡 One Of My Best Taglines  
**%% The  Quieter  You  Become,  The  More  You  Are  Able  To  Hear %%**
