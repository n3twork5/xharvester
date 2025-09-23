# Chapter 2: Bus Protocols 🚌

## Learning Objectives
By the end of this chapter, you will:
- Understand all major automotive communication protocols
- Know how to identify different bus types in vehicles
- Master CAN bus packet structure and signaling
- Learn about high-speed, mid-speed, and low-speed bus systems
- Understand protocol-specific vulnerabilities and attack surfaces

---

## 1. Introduction to Automotive Bus Protocols 📡

**Bus Protocol**: A set of rules governing data transfer between vehicle components

### Key Concepts:
- **High-Speed Bus**: Critical systems (RPM, braking) - 500Kbps+
- **Mid-Speed Bus**: Semi-critical systems - 125Kbps
- **Low-Speed Bus**: Non-critical systems (HVAC, doors) - 33Kbps

### Timeline:
- **1996**: CAN became standard on US vehicles
- **2008**: CAN made mandatory
- **2001**: Mandatory in Europe

---

## 2. CAN Bus (Controller Area Network) 🔧

### 2.1 Physical Layer

**Wiring**: Two twisted-pair wires
- **CANH (CAN High)**: Pin 6 on OBD-II
- **CANL (CAN Low)**: Pin 14 on OBD-II

**Voltage Levels**:
- **Rest State**: 2.5V on both lines
- **Signal**: ±1V differential (3.5V/1.5V)
- **Termination**: 120-ohm resistors at bus ends

**Differential Signaling Benefits**:
- Noise immunity
- Fault tolerance
- Electromagnetic compatibility

### 2.2 CAN Packet Structure

#### Standard CAN Packets (11-bit ID)

**Components**:
1. **Arbitration ID** (11-bit): Device identifier/message type
2. **IDE** (1-bit): Always 0 for standard CAN
3. **DLC** (4-bit): Data Length Code (0-8 bytes)
4. **Data** (0-64 bits): Actual payload

#### Extended CAN Packets (29-bit ID)

**Key Differences**:
- **IDE**: Set to 1
- **SRR**: Substitute Remote Request (replaces RTR)
- **18-bit Extended ID**: Additional identifier space
- **Backward Compatible**: Standard devices ignore extended packets

### 2.3 CAN Bus Characteristics

**Broadcast Nature**:
- All devices see all packets (like UDP)
- No source authentication
- Easy to simulate other devices

**Arbitration**:
- Lower ID wins in collision
- Non-destructive arbitration
- Real-time priority system

### 2.4 Finding CAN Connections

**Voltage Detection**:
- Use multimeter to find 2.5V resting voltage
- Look for ±1V fluctuations during activity
- Always found in dual-wire pairs

**OBD-II Standard Locations**:
- **Pin 6**: CANH
- **Pin 14**: CANL

---

## 3. ISO-TP Protocol (ISO 15765-2) 📦

### Purpose
Extend CAN's 8-byte limit to support up to 4095 bytes

### Implementation
- **First Byte**: Extended addressing
- **Remaining 7 Bytes**: Data payload
- **Packet Chaining**: Multiple CAN frames linked together

### Common Uses
- Diagnostic communications (UDS)
- KWP message transport
- Large data transfers

### Security Implications
- Can flood CAN bus with large transfers
- Used for diagnostic exploitation
- Bridge between network layers

---

## 4. CANopen Protocol 🏭

### Structure
**Communication Object Identifier (COB-ID)**:
- **4-bit Function Code**: Message type
- **7-bit Node ID**: Device identifier

### Key Characteristics
- **Broadcast**: Function code and node ID both 0x0
- **Heartbeat**: Format 0x700 + node ID
- **Industrial Focus**: More common in manufacturing

### Security Value
- Structured arbitration IDs make analysis easier
- Standardized message types
- Easier to reverse engineer than raw CAN

---

## 5. GMLAN (GM Local Area Network) 🚗

### Implementation
Based on ISO-TP with GM-specific extensions

### Bus Types
**Low-Speed Single-Wire**:
- **Speed**: 33.33Kbps
- **Max Nodes**: 32
- **Uses**: Infotainment, HVAC, doors, immobilizer

**High-Speed Dual-Wire**:
- **Speed**: 500Kbps
- **Max Nodes**: 16
- **Uses**: Critical vehicle systems

### Cost Reduction
Single-wire design reduces wiring costs for non-critical systems

---

## 6. SAE J1850 Protocol Family 🔌

### 6.1 PWM (Pulse Width Modulation)

**Physical**:
- **Pins**: 2 and 10 (differential)
- **Voltage**: 5V high
- **Speed**: 41.6Kbps
- **Manufacturer**: Primarily Ford

**Characteristics**:
- Fixed-bit signaling (1=high, 0=low)
- Dual-wire differential like CAN
- Older than CAN but still present

### 6.2 VPW (Variable Pulse Width)

**Physical**:
- **Pin**: 2 only (single-wire)
- **Voltage**: 7V high
- **Speed**: 10.4Kbps
- **Manufacturers**: GM and Chrysler

**Time-Dependent Signaling**:
- Bit value determined by signal duration
- High = ~7V for specific time
- Low = ground level for specific time
- Rest state = near-ground (up to 3V)

**Packet Format**:
- **Data**: Always 11 bits
- **CRC**: 1-bit validity check
- **Headers**: Priority, size, response mode, addressing

---

## 7. Keyword Protocols 🔑

### 7.1 KWP2000 (ISO 14230)

**Physical**:
- **Pin**: 7 on OBD-II
- **Data Size**: Up to 255 bytes per message
- **Common**: US vehicles post-2003

**Variants**:
- **5-baud init**: 10.4Kbaud (ISO 14230-4)
- **Fast init**: 10.4Kbaud (ISO 14230-4)

### 7.2 K-Line (ISO 9141-2)

**Physical**:
- **Primary**: Pin 7
- **Optional**: Pin 15
- **Type**: UART-like serial protocol

**Characteristics**:
- **Start/Stop Bits**: Like modem communication
- **Source/Destination**: Unlike broadcast CAN
- **PID Support**: Similar to CAN parameter IDs
- **Common**: European vehicles

---

## 8. LIN (Local Interconnect Network) 💰

### Purpose
Cheapest vehicle protocol, designed to complement CAN

### Architecture
- **Master**: Single node controlling all transmission
- **Slaves**: Up to 16 nodes, primarily listeners
- **Integration**: Master often connected to CAN bus

### Specifications
- **Speed**: Maximum 20Kbps
- **Wiring**: Single wire at 12V
- **Access**: Not exposed on OBD-II connector

### Message Structure
**Header** (Master sends):
- **SYNC**: Clock synchronization
- **ID**: Message content type (64 possibilities)

**Response** (Master or slave):
- **Data**: Up to 8 bytes
- **Checksum**: Error detection

**Diagnostic IDs**:
- **ID 60**: Master diagnostic requests
- **ID 61**: Slave diagnostic responses
- **NAD**: Node Address for Diagnostics (first byte)

---

## 9. MOST (Media Oriented Systems Transport) 🎵

### Purpose
Designed specifically for multimedia devices

### Network Topology
- **Layout**: Ring or virtual star
- **Devices**: Maximum 64 MOST devices
- **Timing Master**: Feeds frames continuously into ring
- **Network Master**: Assigns addresses (plug-and-play)

### Speed Variants

**MOST25** (Standard):
- **Speed**: ~23Mbaud
- **Medium**: Plastic Optical Fiber (POF)
- **Light**: Red LED at 650nm wavelength
- **Audio**: 15 uncompressed CD channels or MPEG1

**MOST50**:
- **Speed**: Double bandwidth of MOST25
- **Frame**: 1025 bits
- **Medium**: Unshielded Twisted Pair (UTP)

**MOST150**:
- **Speed**: 150Mbps
- **Frame**: 3072 bits
- **Technology**: Implements Ethernet
- **Bandwidth**: 6x MOST25

### Channel Types
1. **Synchronous**: Streamed audio/video data
2. **Asynchronous**: Packet data (TCP/IP)
3. **Control**: Low-speed control data (768Kbaud)

### Security Considerations
- Ring topology creates single points of failure
- Optical fiber difficult to tap
- Ethernet implementation (MOST150) brings IP vulnerabilities

---

## 10. FlexRay Bus ⚡

### Purpose
High-speed, time-critical communications for safety systems

### Applications
- **Drive-by-wire systems**
- **Steer-by-wire**
- **Brake-by-wire**
- **Advanced safety features**

### Specifications
- **Speed**: Up to 10Mbps
- **Medium**: Twisted-pair wiring
- **Dual-Channel**: Optional for fault tolerance/bandwidth

### Network Topologies

**Bus Topology**:
- Similar to CAN bus
- Multiple ECUs on twisted-pair
- Requires termination resistors

**Star Topology**:
- Central FlexRay hub
- Longer segment support
- Active central device required

**Hybrid**: Combination of bus and star

### Time Division Multiple Access (TDMA)
- **Deterministic**: Always same timing
- **Pre-configured**: Devices know network layout
- **Collision-Free**: Time slots prevent conflicts
- **Complex Setup**: More configuration than CAN

### Security Implications
- Time-critical nature makes DoS attacks severe
- Deterministic timing aids in traffic analysis
- Complex configuration increases attack surface

---

## 11. Automotive Ethernet 🌐

### Evolution
Modern vehicles adopting standard Ethernet for:
- **High bandwidth needs**
- **IP-based services**
- **Infotainment connectivity**
- **Over-the-air updates**

### Security Concerns
- **Standard IP vulnerabilities**
- **Network-based attacks**
- **Remote exploitation potential**
- **Integration with safety systems**

---

## 12. OBD-II Connector Pinout Reference 🔌

### Standard Pin Assignments

| Pin | Function | Protocol |
|-----|----------|----------|
| 1   | Manufacturer specific | Various |
| 2   | Bus positive (VPW/PWM) | SAE J1850 |
| 3   | Manufacturer specific | Various |
| 4   | Chassis ground | All |
| 5   | Signal ground | All |
| 6   | CAN high (CANH) | CAN |
| 7   | K-Line | ISO 9141-2/KWP2000 |
| 8   | Manufacturer specific | Various |
| 9   | Manufacturer specific | Various |
| 10  | Bus negative (PWM) | SAE J1850 |
| 11  | Manufacturer specific | Various |
| 12  | Manufacturer specific | Various |
| 13  | Manufacturer specific | Various |
| 14  | CAN low (CANL) | CAN |
| 15  | L-Line (optional) | ISO 9141-2 |
| 16  | Battery positive | All |

---

## 13. Protocol Comparison Matrix 📊

| Protocol | Speed | Wires | Primary Use | Security Risk |
|----------|--------|-------|-------------|---------------|
| **CAN** | 125K-1Mbps | 2 | General vehicle | High |
| **LIN** | 20Kbps | 1 | Low-cost devices | Low |
| **FlexRay** | 10Mbps | 2-4 | Safety-critical | Very High |
| **MOST** | 23-150Mbps | Fiber/UTP | Multimedia | Medium |
| **K-Line** | 10.4Kbps | 1-2 | Diagnostics | Medium |
| **J1850** | 10.4-41.6Kbps | 1-2 | Legacy systems | Low |

---

## 14. Security Implications by Protocol 🛡️

### High Risk Protocols
**CAN Bus**:
- Broadcast nature allows eavesdropping
- No authentication enables spoofing
- Direct access to critical systems
- Easy to flood with malicious traffic

**FlexRay**:
- Controls safety-critical systems
- Time-sensitive makes DoS effective
- Complex configuration creates attack surface

### Medium Risk Protocols
**MOST**:
- Multimedia focus limits impact
- Network complexity provides opportunities
- Ethernet variants bring IP vulnerabilities

**K-Line/KWP2000**:
- Diagnostic access
- Less widespread than CAN
- Source/destination addressing provides some structure

### Lower Risk Protocols
**LIN**:
- Master-slave architecture limits attack vectors
- Low speed reduces impact
- Not exposed on OBD-II

**J1850 (PWM/VPW)**:
- Legacy protocol
- Limited modern implementation
- Slower speeds reduce impact

---

## 15. Practical Protocol Identification 🔍

### Voltage-Based Detection

**2.5V Rest Voltage**: CAN bus (differential ±1V)
**12V**: LIN protocol
**5V**: PWM variant of J1850
**7V**: VPW variant of J1850

### OBD-II Pin Analysis
1. Check pins 6 & 14 for CAN
2. Check pin 2 for VPW or PWM
3. Check pin 7 for K-Line
4. Check pin 10 for PWM negative

### Traffic Analysis
**Regular Patterns**: Likely CAN with periodic messages
**Master-Slave**: Probably LIN
**Deterministic Timing**: FlexRay
**Multimedia Data**: MOST
**Diagnostic Requests**: K-Line/KWP2000

---

## 🛠️ Hands-On Exercises

### Exercise 1: OBD-II Pin Identification
1. Locate your vehicle's OBD-II connector
2. Use multimeter to test pin voltages
3. Identify active protocols
4. Document findings

### Exercise 2: Protocol Research
1. Research your vehicle's specific protocols
2. Find wiring diagrams online
3. Identify internal bus connections
4. Map protocol usage by system

### Exercise 3: Packet Analysis Preparation
1. Understand packet structures for identified protocols
2. Calculate theoretical bandwidth usage
3. Identify potential monitoring points
4. Plan sniffing strategy

---

## 🎯 Key Takeaways

1. **CAN Dominance**: Most important protocol to master
2. **Multi-Protocol Reality**: Modern vehicles use multiple protocols
3. **Speed Hierarchy**: Different speeds for different criticality levels
4. **Evolution**: Trend toward higher speeds and Ethernet adoption
5. **Security Varies**: Risk level depends on protocol characteristics
6. **Physical Access**: Most protocols require OBD-II or internal access

---

## 📚 Next Steps

After mastering bus protocols, you'll move to:
- **Chapter 3**: SocketCAN practical implementation
- **Chapter 4**: Diagnostics and logging
- **Chapter 5**: CAN bus reverse engineering

**Preparation**: Install can-utils and practice with virtual CAN networks before working with real vehicles.

---

## 🔗 Related Standards
- ISO 11898 (CAN)
- ISO 15765-2 (ISO-TP)
- ISO 14230 (KWP2000)
- ISO 9141-2 (K-Line)
- SAE J1850 (PWM/VPW)
- FlexRay Specification
- MOST Specification

Understanding these protocols is fundamental to all automotive security work!