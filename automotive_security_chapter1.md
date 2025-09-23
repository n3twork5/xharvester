# Chapter 1: Understanding Threat Models 🎯

## Learning Objectives
By the end of this chapter, you will:
- Understand automotive attack surfaces and entry points
- Know how to create structured threat models for vehicles
- Be able to identify and categorize automotive threats
- Learn to use DREAD and CVSS rating systems for risk assessment

---

## 1. Finding Attack Surfaces 🔍

**Attack Surface Definition**: All possible ways to attack a target, from individual component vulnerabilities to entire vehicle weaknesses.

### Key Concept: Risk vs Value Ratio
- **Surface Area** = Exposure to risk
- **Volume** = Value of the asset
- **Goal**: Create a low ratio of risk to value through security hardening

### External Attack Surface Analysis
When examining a vehicle's perimeter, consider:

**Exterior Signals & Inputs:**
- Radio waves and communication signals
- Key fobs and remote entry systems
- Distance sensors and proximity detection
- Physical keypad access points
- Touch or motion sensors
- Electric vehicle charging interfaces

**Interior Access Points:**
- Audio inputs: CD, USB, Bluetooth
- Diagnostic ports (OBD-II, manufacturer-specific)
- Dashboard capabilities: GPS, Bluetooth, Internet
- Infotainment system interfaces

---

## 2. Threat Modeling Framework 📋

Threat modeling is a structured approach to:
1. Collect information about vehicle architecture
2. Create diagrams showing component communication
3. Identify high-risk inputs and prioritize them
4. Maintain living documents that evolve with the target

### Level 0: Bird's-Eye View 🦅

**Purpose**: High-level overview of all vehicle inputs

**Components**:
- **Vehicle** (center circle) = Complex process (1.0)
- **Inputs** (rectangular boxes) = External/internal data sources
- **Trust Boundaries** (dotted lines) = External vs internal threats

**Key Inputs to Document**:
- Cellular, Wi-Fi, Bluetooth
- Key fob (KES), TPMS
- USB, CD, Audio
- OBD-II diagnostic port
- Immobilizer system

### Level 1: Receivers 📡

**Purpose**: Identify what each input connects to inside the vehicle

**Numbering System**: X.Y (Process.Receiver)
- Process 1.0 → Receivers 1.1, 1.2, 1.3...

**Key Receivers**:
- **1.1**: Infotainment unit (complex process)
- **1.2**: Immobilizer system
- **1.3**: Engine Control Unit (ECU)
- **1.4**: TPMS Receiver

**Trust Boundary Analysis**:
- More boundaries crossed = Higher risk
- External → Internal → Device-specific

### Level 2: Receiver Breakdown 🔬

**Purpose**: Examine internal communication within complex receivers

**Example - Infotainment Console (1.1)**:
- **Kernel Space** (higher risk): Direct kernel access
  - udev (USB device loading)
  - HSI (cellular communication driver)
  - Kvaser (vehicle network driver)
- **User Space** (lower risk): Application-level access
  - WPA supplicant (Wi-Fi management)
  - Media players, apps

**Numbering**: X.X.X format (Process.Receiver.Subcomponent)

---

## 3. Threat Identification 🚨

### Level 0 Threats (High-Level)
Potential attacker capabilities:
- **Remote vehicle takeover**
- **Vehicle shutdown/disabling**
- **Occupant surveillance**
- **Unauthorized access/theft**
- **Vehicle tracking**
- **Safety system compromise**
- **Malware installation**
- **Ransomware deployment**

### Level 1 Threats (Receiver-Specific)

**By Input Type:**
- **Cellular**: Remote code execution, data interception
- **Wi-Fi**: Network-based attacks, man-in-the-middle
- **Bluetooth**: Unauthorized pairing, protocol exploits
- **Key Fob**: Signal replay, rolling code attacks
- **TPMS**: Sensor spoofing, tracking
- **USB**: Malicious device attacks, data extraction
- **CAN Bus**: Message injection, DoS attacks

---

## 4. Threat Rating Systems ⚖️

### DREAD Rating System

**Scale**: 1-3 for each category (1=Low, 2=Medium, 3=High)

**Categories**:
- **D**amage potential: How great is the damage?
- **R**eproducibility: How easy is it to reproduce?
- **E**xploitability: How easy is it to attack?
- **A**ffected users: How many users are affected?
- **D**iscoverability: How easy is it to find the vulnerability?

**Rating Examples**:
- **High Damage (3)**: Could subvert security system and gain full control
- **Medium Damage (2)**: Could leak sensitive information
- **Low Damage (1)**: Limited impact, minimal information disclosure

**Risk Score**: Sum of all categories ÷ 5 = Overall risk rating

### CVSS (Common Vulnerability Scoring System)
Alternative to DREAD with more detailed scoring:
- **Base Score**: Vulnerability characteristics
- **Temporal Score**: Time-based factors
- **Environmental Score**: Local environment impact

---

## 5. Working with Threat Model Results 📊

### Documentation Best Practices
1. **Living Documents**: Update as you learn more
2. **Version Control**: Track changes over time
3. **Cross-Reference**: Link threats to specific components
4. **Priority Matrix**: Risk score vs. attack feasibility

### Risk Prioritization
**High Priority**:
- Remote attack vectors
- Safety-critical systems
- High DREAD scores
- Multiple trust boundary crossings

**Medium Priority**:
- Local attack vectors
- Non-safety systems
- Medium DREAD scores

**Low Priority**:
- Physical access required
- Low impact potential
- Single trust boundary

---

## 🛠️ Practical Exercise

### DIY Threat Model Creation

**Step 1**: Choose a vehicle (your own or a specific model)

**Step 2**: Create Level 0 diagram
- Draw vehicle in center
- List all inputs you can identify
- Mark trust boundaries

**Step 3**: Develop Level 1 map
- Research what each input connects to
- Number each receiver
- Identify complex processes

**Step 4**: Threat identification
- Brainstorm Level 0 threats
- List receiver-specific threats
- Be creative - think "James Bond villain"

**Step 5**: Apply DREAD scoring
- Rate each identified threat
- Calculate risk scores
- Prioritize for testing

---

## 🎯 Key Takeaways

1. **Attack Surface**: Document ALL possible data entry points
2. **Layered Modeling**: Start high-level, dive deeper progressively
3. **Trust Boundaries**: More boundaries = Higher risk
4. **Threat Brainstorming**: Include unrealistic scenarios initially
5. **Risk Scoring**: Use structured approaches (DREAD/CVSS)
6. **Living Process**: Update models as you learn more

---

## 📚 Next Steps

After mastering threat modeling, you'll move to:
- **Chapter 2**: Bus Protocols (CAN, OBD-II, etc.)
- **Chapter 3**: SocketCAN practical implementation
- **Chapter 4**: Diagnostics and logging techniques

**Practice Recommendation**: Create a threat model for your own vehicle or a popular car model before proceeding to technical protocols.

---

## 🔗 Related Resources
- Microsoft Threat Modeling Tool
- OWASP Threat Modeling Guide
- NIST Cybersecurity Framework
- ISO 21434 (Automotive Cybersecurity)

Remember: Threat modeling is the foundation of all automotive security work. Take time to master these concepts!