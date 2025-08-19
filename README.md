```
               _  _  _   _    __    ____  _  _  ____  ___  ____  _____  ____ 
              ( \/ )( )_( )  /__\  (  _ \( \/ )( ___)/ __)(_  _)(  _  )(  _ \
               )  (  ) _ (  /(__)\  )   / \  /  )__) \__ \  )(   )(_)(  )   /
              (_/\_)(_) (_)(__)(__)(_)\_)  \/  (____)(___/ (__) (_____)(_)\_)
```
xharvestor is a specialized, modular Python-based reconnaissance suite designed for security assessments of radio frequency (RF), wireless, industrial, and automotive systems. It integrates multiple tools and scripts into a unified workflow for probing, analyzing, and documenting findings from the physical and wireless world.
### Overview

Moving beyond traditional web OSINT, xHarvester RF allows security researchers, red teams, and penetration testers to interact with the electromagnetic spectrum. It provides a structured approach to discovering, fingerprinting, and assessing the security posture of devices ranging from WiFi routers and Bluetooth peripherals to critical Industrial Control Systems (ICS) and modern automobiles.

### Core Framework Features

Unified Command & Control: A single Python-based interface to orchestrate a wide array of specialized hardware and software tools.

Modular Architecture: Enables users to run specific reconnaissance modules (--rf, --wifi, --auto, --bt, --ics) independently or in combination for a full-spectrum assessment.

Automated Evidence Collection: Automatically saves all findings in structured, standardized formats:

Raw Data: PCAP files, IQ recordings (*.bin), CAN bus logs.

Structured Reports: Comprehensive reports in HTML, JSON, and Markdown for easy integration into deliverables.

Geotagging Integration: Correlates all discovered devices and signals with GPS coordinates (when a receiver is available) for mapping and analysis.

Hardware Abstraction Layer: Simplifies the use of complex hardware (SDRs, CAN interfaces) by handling driver communication and configuration automatically.

### Disclaimer
This tool is intended for authorized security testing and educational purposes only. Interfering with wireless signals, industrial processes, or vehicle systems without explicit permission is illegal, extremely dangerous, and can lead to physical harm, catastrophic failure, and severe legal consequences. Always operate within a controlled, legal environment.
