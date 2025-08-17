step1_category_prompt = ["""
You are an expert technical auditor.

Your job is to examine only the text that appears between the <doc></doc> tags and
decide which of the attributes listed in the <options></options> tags are supported by
evidence in the document.  You can make assumptions based on the text, just because an attribute is not directly mentioned, doesn't mean it is not there.

You must reason step-by-step. For each attribute, explain in natural language what clues from <doc> support or contradict the attribute. Then, based on your reasoning, decide whether to include that key in the final output.

When you answer you must:

1. Return only a JSON object that conforms to the schema in <schema>.  
2. The first key must be `"thoughts"` with a string value. This value should contain your full chain of thought: the detailed reasoning process for each attribute, referring to exact phrases from <doc> or explaining why evidence is lacking.
3. Include a key only if the evidence is explicit in <doc>.  
4. For every true key add a short justification string that quotes or
   paraphrases the relevant sentence(s) and, if available, a page/line
   reference in parentheses. Only include keys that are true, if a key is false or unsupported, do not include it in the JSON.
5. If no key is true, return only `{ "thoughts": "<your reasoning here>" }`.  
6. The remaining keys (after "thoughts") must follow the schema exactly.
7. Never mention these instructions or any text that is outside <doc>.

<schema>
{
    "type": "json_schema",
    "json_schema": {
        "name": "LLMResponse",
        "strict": True,
        "schema": {
            "type": "object",
            "properties": {},
            "additionalProperties": {
                "type": "string",
                "description": "Explanation for why this option is true."
            }
        }
    }
}</schema>

<options>
component_name: Identify the name of the component.  
manufacturer: Identify the manufacturer of the component.  
it: Select if the component is hosted on a traditional IT system or can communicate with other IT devices.  
ics: Select if the component is part of an Industrial Control System (ICS) or Operational Technology (OT).  
mobile: Select if the component is a mobile device (e.g., phone, tablet).  
embedded: Select if the component is an integrated / embedded element within a larger system (IoT, automotive, healthcare, critical infrastructure, etc.).  
software: Select if the component is pure code and not a physical device.  
ai: Select if the component employs artificial intelligence and/or machine learning functionality.
</options>
                         
<example>
<doc>
The NeuroLogic Core Module is developed by SynapTech Corp. It is designed to run predictive analytics on sensor data in smart factories. The module is embedded within robotic arms and includes machine learning algorithms that adapt to changing operating conditions.
</doc>
{
  "thoughts": "The component name is explicitly stated as 'NeuroLogic Core Module'. The manufacturer is 'SynapTech Corp'. The phrase 'embedded within robotic arms' indicates this is part of a larger system, supporting the 'embedded' tag. The presence of 'machine learning algorithms' supports the 'ai' tag. The reference to smart factories and robotic systems implies industrial use, thus supporting 'ics'. No evidence supports it being a mobile device, pure software, or traditional IT system.",
  "component_name": "NeuroLogic Core Module.",
  "manufacturer": "SynapTech Corp'.",
  "ics": "'Smart factories' and 'robotic arms' indicate an ICS/OT context.",
  "embedded": "Explicitly stated to be embedded within robotic arms.",
  "ai": "Described as using 'machine learning algorithms'."
}
</example>

<example>
<doc>
The CloudSense app is a browser-based SaaS platform used by marketing teams to segment customer data. Developed by DataMotion Inc., it includes a predictive model to forecast user behavior. The software is deployed in AWS.
</doc>
{
  "thoughts": "CloudSense app.",
  "component_name": "CloudSense app.",
  "manufacturer": "Identified as 'DataMotion Inc.'.",
  "software": "Described as a browser-based SaaS platform.",
  "ai": "Includes a 'predictive model to forecast user behavior'."
}
</example>

<example>
<doc>
This device is a rugged handheld scanner running on Android 11, primarily used in warehouse environments for inventory tracking. The unit includes a barcode reader, touchscreen, and Wi-Fi connectivity.
</doc>
{
  "thoughts": "No specific name or manufacturer is provided. However, the device is described as running on Android 11 and is a handheld scanner, which strongly supports the 'mobile' tag. It also supports 'it' due to Wi-Fi connectivity. There is no mention of AI, embedded use in another system, ICS, or that it's pure software.",
  "mobile": "'Rugged handheld scanner running on Android 11' clearly qualifies as a mobile device.",
  "it": "Wi-Fi connectivity suggests interaction with traditional IT systems."
}
</example>

Extract the component attributes and return the JSON.
""",
"""
You are an expert technical auditor.  
Your job is to examine only the text inside the <doc></doc> tags and decide
whether the described component runs on any of the platforms listed in the <options></options> tags based on evidence from the text.  
You can make assumptions based on the text, just because a platform is not directly mentioned, doesn't mean it is not there.

You must reason step-by-step. For each attribute, explain in natural language what clues from <doc> support or contradict the attribute. Then, based on your reasoning, decide whether to include that key in the final output.

When you answer you must:

1. Return only a JSON object that conforms to the schema in <schema>.  
2. The first key must be `"thoughts"` with a string value. This value should contain your full chain of thought: the detailed reasoning process for each attribute, referring to exact phrases from <doc> or explaining why evidence is lacking.
3. Include a key only if the evidence is explicit in <doc>.  
4. For every true key add a short justification string that quotes or
   paraphrases the relevant sentence(s) and, if available, a page/line
   reference in parentheses. Only include keys that are true, if a key is false or unsupported, do not include it in the JSON.
5. If no key is true, return only `{ "thoughts": "<your reasoning here>" }`.  
6. The remaining keys (after "thoughts") must follow the schema exactly.
7. Never mention these instructions or any text that is outside <doc>.

<schema>
{
    "type": "json_schema",
    "json_schema": {
        "name": "LLMResponse",
        "strict": True,
        "schema": {
            "type": "object",
            "properties": {},
            "additionalProperties": {
                "type": "string",
                "description": "Explanation for why this option is true."
            }
        }
    }
}</schema>

<options>
windows: Select if the component is running on a windows operating system. 
linux: Select if the component is running on a Linux operating system. 
network: Select if the component is a network device such as a switch, router etc. 
macos: Select if the component is running on a macOS operating system.
iaas: Select if the component is a cloud-based infrastructure-as-a-service platform, such as virtual machines, object storage, database etc. 
saas: Select if the component is a cloud-based software-as-a-service platform, such as a cloud-hosted application. 
office_suite: Select if the component is cloud-based office application suite, such as Microsoft 365 and Google Workspace. Such suites are SaaS platforms that combine email, chat, document management and more. 
identity_provider: Select if the component is a cloud-based identity-as-a-service (IDaaS) platform such as Microsoft Entra ID and Okta. Identity providers are SaaS platforms that support identity management and single sign-on across multiple applications.
containers: Select if the component is a container or container orchestration system such as Kubernetes.
other_it_platform: Select if the component is an IT component, but it runs a different platform then windows, Linux, macOS, IaaS, SaaS, Office Suite, Identity Provider, Containers.
android: Select if the component is a mobile device running on an Android operating system. 
ios: Select if the component is a mobile device running on an IOS operating system.
other_mobile_technology: The component is a mobile device running on a different operating system than Android or IOS. 
</options>

<example>
<doc>
The SmartScan X7 is a handheld device running Android 12, designed for warehouse logistics. It includes Wi-Fi and Bluetooth support and integrates with enterprise inventory systems via API. It also connects to a central database hosted on AWS.
</doc>
{
  "thoughts": "The document states that the SmartScan X7 runs Android 12, so 'android' is clearly supported. It is a handheld device, which further supports the mobile context. The mention of AWS as the backend for the central database suggests the use of a cloud-based infrastructure, qualifying 'iaas'. Wi-Fi and Bluetooth support reinforce that it is an IT-connected device, but no mention of Linux, Windows, macOS, or containerized environments.",
  "android": "Explicitly stated to run 'Android 12'.",
  "iaas": "Mentions that the device connects to a 'central database hosted on AWS', indicating IaaS.",
  "other_it_platform": "The device integrates with enterprise inventory systems via API and uses common IT protocols like Wi-Fi and Bluetooth."
}
</example>

<example>
<doc>
CloudReports Pro is a browser-based software suite used for corporate reporting and analytics. It is accessed through Google Workspace and includes features for document collaboration, chat integration, and automated data aggregation.
</doc>
{
  "thoughts": "The system is described as browser-based and integrated with Google Workspace, which qualifies it as an 'office_suite'. Since it runs entirely in the cloud and provides SaaS-like features (chat, document collaboration), it also qualifies as 'saas'. There's no evidence of it being tied to specific operating systems or containers.",
  "office_suite": "Google Workspace is explicitly mentioned, which is a cloud-based office suite.",
  "saas": "Described as 'browser-based' and used for corporate reporting and analytics, with typical SaaS features like collaboration and automation."
}
</example>

<example>
<doc>
This component is a network switch that supports VLAN tagging, SNMP, and redundant uplinks. It is installed in a data center to manage routing between subnetworks and offers a web-based admin panel. It can be connected to Windows or MacOS computers.
</doc>
{
  "thoughts": "The document describes the component as a 'network switch', and includes features typical of networking equipment such as VLAN, SNMP, and routing functions. It is clearly a 'network' device. Even though it says it can be connected to windows and MacOS computers, there's no indication of an operating system of the device itself, cloud platform, or mobile context.",
  "network": "Described explicitly as a 'network switch' and includes networking features like VLAN tagging and SNMP."
}
</example>


Extract the platform information and return the JSON.
""",
"""
You are an expert technical auditor.  
Your job is to examine only the text inside the <doc></doc> tags and decide
which of the MITRE ICS asset categories listed in the <options></options> tags below that the component fits into.
You can make assumptions based on the text, just because the asset category is not directly mentioned, doesn't mean it is not there.

You must reason step-by-step. For each category, explain in natural language what clues from <doc> support or contradict the option. Then, based on your reasoning, decide whether to include that key in the final output.

When you answer you must:

1. Return only a JSON object that conforms to the schema in <schema>.  
2. The first key must be `"thoughts"` with a string value. This value should contain your full chain of thought: the detailed reasoning process for each option, referring to exact phrases from <doc> or explaining why evidence is lacking.
3. Include a key only if the evidence is explicit in <doc>.  
4. For every true key add a short justification string that quotes or
   paraphrases the relevant sentence(s) and, if available, a page/line
   reference in parentheses. Only include keys that are true, if a key is false or unsupported, do not include it in the JSON.
5. If no key is true, return only `{ "thoughts": "<your reasoning here>" }`.  
6. The remaining keys (after "thoughts") must follow the schema exactly.
7. Never mention these instructions or any text that is outside <doc>.

<schema>
{
  "type": "json_schema",
  "json_schema": {
    "name": "LLMResponse",
    "strict": true,
    "schema": {
      "type": "object",
      "properties": {},
      "additionalProperties": {
        "type": "string",
        "description": "Explanation for why this option is true."
      }
    }
  }
}
</schema>

<options>
a0008: Select if the component is an application server. Application servers are used across many different sectors to host various diverse software applications necessary to supporting the system. Example functions can include data analytics and reporting, alarm management, and the management/coordination of different control servers. The application server typically runs on a modern server operating system (e.g., MS Windows Server).
a0007: Select if the component is a control server. Control servers are typically a software platform that runs on a modern server operating system (e.g., MS Windows Server). The server typically uses one or more automation protocols (e.g., Modbus, DNP3) to communicate with the various low-level control devices such as Remote Terminal Units (RTUs) and Programmable Logic Controllers (PLCs). The control server also usually provides an interface/network service to connect with an HMI.
a0009: Select if the component is a data gateway. Data Gateway is a device that supports the communication and exchange of data between different systems, networks, or protocols within the ICS. Different types of data gateways are used to perform various functions, including: Protocol Translation that enables communication to devices that support different or incompatible protocols by translating information from one protocol to another. Media Converter that converts data across different Layer 1 and 2 network protocols / mediums, for example, converting from Serial to Ethernet. Data Aggregation that collects and combines data from different devices into one consistent format and protocol interface. Data gateways are often critical to the forwarding/transmission of critical control or monitoring data within the ICS. Further, these devices often have remote various network services that are used to communicate across different zones or networks. These assets may focus on a single function listed or combinations of these functions to best fit the industry use-case.
a0006: Select if the component is a data historian. Data historians, or historian, are systems used to collect and store data, including telemetry, events, alerts, and alarms about the operational process and supporting devices. The historian typically utilizes a database to store this data, and commonly provide tools and interfaces to support the analysis of the data. Data historians are often used to support various engineering or business analysis functions and therefore commonly needs access from the corporate network. Data historians often work in a hierarchical paradigm where lower/site level historians collect and store data which is then aggregated into a site/plant level historian. Therefore, data historians often have remote services that can be accessed externally from the ICS network.
a0013: Select if the component is a field I/O device. Field I/O are devices that communicate with a controller or data aggregator to either send input data or receive output data. Input data may include readings about a given environment/device state from sensors, while output data may include data sent back to actuators for them to either undertake actions or change parameter values. These devices are frequently embedded devices running on lightweight embedded operating systems or RTOSes.
a0002: Select if the component is a Human-Machine Interface (HMI).Human-Machine Interfaces (HMIs) are systems used by an operator to monitor the real-time status of an operational process and to perform necessary control functions, including the adjustment of device parameters. An HMI can take various forms, including a dedicated screen or control panel integrated with a specific device/controller, or a customizable software GUI application running on a standard operating system (e.g., MS Windows) that interfaces with a control/SCADA server. The HMI is critical to ensuring operators have sufficient visibility and control over the operational process.
a0005: Select if the component is an Intelligent Electronic Device (IED). An Intelligent Electronic Device (IED) is a type of specialized field device that is designed to perform specific operational functions, frequently for protection, monitoring, or control within the electric sector. IEDs are typically used to both acquire telemetry and execute tailored control algorithms/actions based on customizable parameters/settings. An IED is usually implemented as a dedicated embedded device and supports various network automation protocols to communicate with RTUs and Control Servers.
a0012: Select if the component is a jump host. Jump hosts are devices used to support remote management sessions into ICS networks or devices. The system is used to access the ICS environment securely from external networks, such as the corporate network. The user must first remote into the jump host before they can access ICS devices. The jump host may be a customized Windows server using common remote access protocols (e.g., RDP) or a dedicated access management device. The jump host typically performs various security functions to ensure the authenticity of remote sessions, including authentication, enforcing access controls/permissions, and auditing all access attempts.
a0003: Select if the component is a Programmable Logic Controller (PLC). A Programmable Logic Controller (PLC) is an embedded programmable control device. PLCs typically utilize a modular architecture with separate modules used to support its processing capabilities, communication mediums, and I/O interfaces. PLCs allow for the deployment of customized programs/logic to control or monitor an operational process. This logic is defined using industry specific programming languages, such as IEC 61131 , which define the set of tasks and program organizational units (POUs) included in the device's programs. PLCs also typically have distinct operating modes (e.g., Remote, Run, Program, Stop) which are used to determine when the device can be programmed or whether it should execute the custom logic.
a0004: Select if the component is a Remote Terminal Unit (RTU). A Remote Terminal Unit (RTU) is a device that typically resides between field devices (e.g., PLCs, IEDs) and control/SCADA servers and supports various communication interfacing and data aggregation functions. RTUs are typically responsible for forwarding commands from the control server and the collection of telemetry, events, and alerts from the field devices. An RTU can be implemented as a dedicated embedded device, as software platform that runs on a hardened/ruggedized computer, or using a custom application program on a PLC.
a0014: Select if the component is a router. A computer that is a gateway between two networks at OSI layer 3 and that relays and directs data packets through that inter-network. The most common form of router operates on IP packets.
a0010: Select if the component is a safety controller. Safety controllers are typically a type of field device used to perform the safety critical function. Safety controllers often support the deployment of custom programs/logic, similar to a PLC, but can also be tailored for sector specific functions/applications. The safety controllers typically utilize redundant hardware and processors to ensure they operate reliably if a component fails.
a0011: Select if the component is a VPN server. A Virtual Private Network (VPN) server is a device that is used to establish a secure network tunnel between itself and other remote VPN devices, including field VPNs. VPN servers can be used to establish a secure connection with a single remote device, or to securely bridge all traffic between two separate networks together by encapsulating all data between those networks. VPN servers typically support remote network services that are used by field VPNs to initiate the establishment of the secure VPN tunnel between the field device and server.
a0001: Select if the component is a workstation. Workstations are devices used by human operators or engineers to perform various configuration, programming, maintenance, diagnostic, or operational tasks. Workstations typically utilize standard desktop or laptop hardware and operating systems (e.g., MS Windows), but run dedicated control system applications or diagnostic/management software to support interfacing with the control servers or field devices. Some workstations have a fixed location within the network architecture, while others are transient devices that are directly connected to various field devices to support local management activities.
   </options>

<example>
<doc>
The system includes a ruggedized touchscreen panel mounted in the control room that allows operators to adjust system parameters and visualize real-time metrics. The interface is built on Windows Server and connects to the SCADA control network.
</doc>
{
  "thoughts": "The text describes a 'touchscreen panel' used by operators to monitor and adjust system parameters, which clearly supports it being a Human-Machine Interface (HMI). The fact that it is 'mounted in the control room' and runs on 'Windows Server' further supports this. It also connects to the SCADA control network, a common integration point for HMIs. No mention is made of functions specific to historians, PLCs, RTUs, or other categories.",
  "a0002": "Operators use the touchscreen panel to 'adjust system parameters and visualize real-time metrics'. It runs on 'Windows Server' and interfaces with the SCADA control network, supporting the HMI classification."
}
</example>

<example>
<doc>
The Protego SecureLink unit is installed at the boundary between the corporate and ICS network. All external connections must first authenticate through the SecureLink, which logs all sessions, applies access policies, and then allows users to connect to internal systems.
</doc>
{
  "thoughts": "The system is located between the corporate and ICS networks and handles remote session access, enforces access policies, and logs activity. These characteristics clearly identify it as a jump host. There is no indication that this component performs control logic, interacts directly with field devices, or acts as a VPN server.",
  "a0012": "The SecureLink 'authenticates sessions', 'logs all sessions', and mediates external access to the ICS network, which is consistent with the definition of a jump host."
}
</example>

<example>
<doc>
This controller manages actuator timing and motor feedback in a robotic welding station. It uses redundant logic circuits and is certified for safety-critical operations. The device runs its own firmware and accepts IEC 61131 logic uploaded via engineering tools.
</doc>
{
  "thoughts": "The controller is responsible for timing and motor control in a welding station and is described as 'certified for safety-critical operations' with 'redundant logic circuits'. These are clear indicators of a safety controller. Additionally, it uses IEC 61131 logic, which supports its similarity to a PLC, but the safety focus makes 'a0010' more appropriate. No mention is made of historian, HMI, RTU, or network gateway functionality.",
  "a0010": "Performs 'safety-critical operations' and uses 'redundant logic circuits', which are defining features of a safety controller."
}
</example>

Extract the asset categories and return the JSON.
""",
"""
You are an expert technical auditor.  
Your job is to examine only the text inside the <doc></doc> tags and decide
whether the described component has any of the MITRE EMB3D hardware properties listed
in the <options></options> tags based on evidence from the text.  
You can make assumptions based on the text, just because a property is not directly mentioned, doesn't mean it is not there.

You must reason step-by-step. For each property, explain in natural language what clues from <doc> support or contradict the property. Then, based on your reasoning, decide whether to include that key in the final output.

When you answer you must:

1. Return only a JSON object that conforms to the schema in <schema>.  
2. The first key must be `"thoughts"` with a string value. This value should contain your full chain of thought: the detailed reasoning process for each option, referring to exact phrases from <doc> or explaining why evidence is lacking.
3. Include a key only if the evidence is explicit in <doc>.  
4. For every true key add a short justification string that quotes or
   paraphrases the relevant sentence(s) and, if available, a page/line
   reference in parentheses. Only include keys that are true, if a key is false or unsupported, do not include it in the JSON.
5. If no key is true, return only `{ "thoughts": "<your reasoning here>" }`.  
6. The remaining keys (after "thoughts") must follow the schema exactly.
7. Never mention these instructions or any text that is outside <doc>.

<schema>
{
  "type": "json_schema",
  "json_schema": {
    "name": "LLMResponse",
    "strict": true,
    "schema": {
      "type": "object",
      "properties": {},
      "additionalProperties": {
        "type": "string",
        "description": "Explanation for why this option is true."
      }
    }
  }
}
</schema>

<options>
pid11: Select if the device includes a microprocessor (CPU).
If the product supports firmware updates, displays boot or diagnostic messages, references an OS/RTOS, or lists a clock rate in MHz, assume a CPU is present—even if the word processor never appears. Virtually every modern connected gadget, sensor hub, or smart peripheral conceals at least one microcontroller.

pid12: Select if the device includes external memory or storage components.
Mark this when stated flash/RAM capacities exceed the SoC's on-die limits, or teardown photos show separate flash, EEPROM, eMMC, or SRAM parts. Any mention of “8 MB flash,” “32 GB eMMC,” or an SD-card slot is an automatic yes.

pid121: Select if the device includes buses for external memory/storage.
Whenever pid12 is true, this property is almost certainly true as well. Explicit references to SPI, QSPI, I²C, SDIO, DDR, PCIe, or a memory controller confirm it; length-matched trace bundles between the CPU and memory devices offer visual proof.

pid122: Select if multiple chips/devices share access to the same physical memory.
Tick this box when block diagrams show GPUs, radios, DMA engines, or accelerators touching system RAM. Buzzwords like shared DDR, heterogeneous SoC, zero-copy, or any mention of DMA masters indicate that more than one device reads or writes the memory.

pid123: Select if the device includes non-volatile memory such as ROM, NVRAM, or removable storage.
Evidence includes boot ROM, eFuse, configuration NAND, FRAM, or field-replaceable media (SD/TF card, USB mass-storage, M.2/NVMe). If firmware or configuration survives power loss, qualifying NVM is almost certainly present.

pid124: Select if the device includes discrete RAM (volatile memory) chips.
Specifications showing hundreds of megabytes of RAM, or PCB photos with multiple identical DRAM/SRAM BGAs flanking the CPU, satisfy this property. Part numbers beginning MT41, K4B, or similar DRAM families strengthen the case.

pid1241: Select if the RAM is DDR DRAM.
Look for “DDR,” “DDR2,” “DDR3,” “DDR4,” “LPDDR,” or speeds in MT/s (e.g., 1600 MT/s). Tightly matched differential pairs and fly-by routing between CPU and memory packages also imply DDR technology.

pid13: Select if the device includes peripheral chips and internal buses for component communication.
Auxiliary ICs—Ethernet PHYs, Wi-Fi/Bluetooth modules, audio codecs, sensor hubs—connected over I²C, SPI, CAN, or similar on-board links qualify. Bills of materials or block diagrams listing -PHY, -ADC, sensor hub, or bridge components are clear indicators.

pid14: Select if the device provides external peripheral interfaces such as USB, Serial, HDMI, or Ethernet.
Visible connectors (USB-C, Micro-USB, RJ-45, DB-9, HDMI) or manual sections labeled I/O, Connectivity, or “connect to PC” constitute sufficient evidence.

pid15: Select if the device exposes a hardware access/debug port (e.g., JTAG, UART, SWD).
Unpopulated headers, tag-connect pads, or test points marked TCK, TMS, RX, TX reveal such ports. Documentation mentioning “debug,” “factory console,” or boot logs that say “Press any key to stop autoboot” further substantiate this property.
</options>

<example>
<doc>
The TrackerBoard v2 includes a 32-bit microcontroller running at 120 MHz with 512 KB flash and 64 KB SRAM. External SPI flash of 2 MB is used to store logs. It also includes a USB-C port for data transfer, a JTAG header for firmware debugging, and a Wi-Fi module for wireless communication.
</doc>
{
  "thoughts": "The mention of a '32-bit microcontroller running at 120 MHz' confirms the presence of a CPU (pid11). The '512 KB flash and 64 KB SRAM' refer to internal memory, while the 'external SPI flash of 2 MB' confirms external memory (pid12) and a memory bus (pid121). The JTAG header confirms a debug port (pid15), and the USB-C port satisfies the requirement for external interfaces (pid14). The presence of a Wi-Fi module and SPI connection supports the presence of peripheral chips and buses (pid13).",
  "pid11": "120 MHz 32-bit microcontroller confirms the presence of a CPU.",
  "pid12": "External 2 MB SPI flash qualifies as external memory.",
  "pid121": "SPI connection implies a memory/storage bus is used.",
  "pid13": "Wi-Fi module connected via SPI indicates peripheral chip and communication bus.",
  "pid14": "USB-C port qualifies as an external peripheral interface.",
  "pid15": "JTAG header is explicit evidence of a debug port."
}
</example>

<example>
<doc>
The CoreVision-X uses an embedded SoC with 8 MB of LPDDR4 RAM and 16 GB eMMC flash. Boot code is stored in an internal ROM. Communication with the main processor and memory is done over a high-speed DDR bus. The device includes Bluetooth, I²C-connected sensors, and supports USB and HDMI output. Debugging is possible via a UART console.
</doc>
{
  "thoughts": "The SoC has LPDDR4 RAM and 16 GB eMMC flash, indicating external memory (pid12), DDR RAM (pid1241), and discrete RAM (pid124). The use of DDR confirms the presence of a memory bus (pid121). Internal ROM and large flash meet the criteria for non-volatile memory (pid123). Communication over a high-speed DDR bus and the presence of connected sensors over I²C confirm peripheral buses (pid13). USB and HDMI qualify for peripheral interfaces (pid14), and the UART console qualifies as a debug port (pid15).",
  "pid12": "16 GB eMMC flash and LPDDR4 RAM exceed on-die limits.",
  "pid121": "High-speed DDR bus confirms a memory bus.",
  "pid123": "Internal ROM and eMMC flash qualify as non-volatile memory.",
  "pid124": "LPDDR4 RAM implies discrete volatile memory.",
  "pid1241": "LPDDR4 explicitly confirms DDR DRAM.",
  "pid13": "Bluetooth and I²C-connected sensors imply internal peripheral buses.",
  "pid14": "USB and HDMI outputs qualify as external interfaces.",
  "pid15": "UART console provides debug access."
}
</example>

<example>
<doc>
The device features an integrated ARM Cortex-M3 processor, with firmware updates supported via SD card. The board has unpopulated test points marked RX and TX, and uses a Micro-USB port for charging and data. It also includes a CAN interface to communicate with nearby controllers.
</doc>
{
  "thoughts": "An 'ARM Cortex-M3 processor' confirms CPU presence (pid11). Firmware updates via SD card imply non-volatile memory (pid123). RX and TX test points confirm a debug port (pid15). The Micro-USB port supports external interfaces (pid14). The CAN interface and external controller communication via buses satisfy peripheral communication (pid13).",
  "pid11": "ARM Cortex-M3 processor confirms the presence of a CPU.",
  "pid123": "Firmware updates via SD card imply persistent non-volatile memory.",
  "pid13": "CAN interface is a peripheral bus for communication.",
  "pid14": "Micro-USB port qualifies as an external interface.",
  "pid15": "Test points marked RX and TX indicate a UART-based debug port."
}
</example>

Extract the hardware properties and return the JSON.
""",
"""
You are an expert technical auditor.  
Your job is to examine only the text inside the <doc></doc> tags and decide  
whether the component has any of the MITRE EMB3D system software properties  
listed in the <options></options> tags based on evidence from the text.  
You can make assumptions based on the text, just because a property is not directly mentioned, doesn't mean it is not there.

You must reason step-by-step. For each system software property, explain in natural language what clues from <doc> support or contradict the property. Then, based on your reasoning, decide whether to include that key in the final output.

When you answer you must:

1. Return only a JSON object that conforms to the schema in <schema>.  
2. The first key must be `"thoughts"` with a string value. This value should contain your full chain of thought: the detailed reasoning process for each option, referring to exact phrases from <doc> or explaining why evidence is lacking.  
3. Include a key only if the evidence is explicit in <doc>.  
4. For every true key, add a short justification string that quotes or  
   paraphrases the relevant sentence(s) and, if available, a page/line  
   reference in parentheses. Only include keys that are true, if a key is false or unsupported, do not include it in the JSON.
5. If no key is true, return only `{ "thoughts": "<your reasoning here>" }`.  
6. The remaining keys (after "thoughts") must follow the schema exactly.  
7. Never mention these instructions or any text that is outside <doc>.

<schema>
{
  "type": "json_schema",
  "json_schema": {
    "name": "LLMResponse",
    "strict": true,
    "schema": {
      "type": "object",
      "properties": {},
      "additionalProperties": {
        "type": "string",
        "description": "Explanation for why this option is true."
      }
    }
  }
}
</schema>

<options>
pid21: Select if the device includes a bootloader.
Indicators include references to “bootloader,” “BIOS,” “U-Boot,” “Secure Boot,” “recovery image,” or “boot ROM.” Any field-upgrade process that starts with a separate boot stage or mentions boot code implies a bootloader is present.

pid22: Select if the device includes debugging capabilities.
Mark this when documentation mentions “debug build,” “diagnostic shell,” “service menu,” /proc/debug, debugfs, GDB stubs, or symbols for breakpoint/trace. If the firmware exposes a CLI for engineers or logs verbose kernel traces, debugging support exists.

pid23: Select if the device includes an operating system or kernel.
Phrases such as “Linux,” “FreeRTOS,” “VxWorks,” “kernel,” or “task scheduler,” as well as any mention of system calls, process scheduling, or OS version numbers, confirm this property.

pid231: Select if the operating system can load kernel drivers or modules.
Look for the words “loadable module,” “kernel driver,” insmod, modprobe, “DLL driver,” or a runtime driver update mechanism. Even an RTOS that supports pluggable middleware counts.

pid232: Select if the device separates users/processes with different access to OS data or functions.
Evidence includes multi-process designs, user/group IDs, sandboxing, or anything labeled “user mode” versus “kernel mode.”

pid2321: Select if the device lacks an access-enforcement or privilege mechanism.
Check this when all code runs as a single unrestricted user, or the manual states “no authentication required for internal functions.” Bare-metal firmware and single-task RTOS images typically meet this condition.

pid2322: Select if the device deploys an access-enforcement or privilege mechanism.
Any reference to privilege levels, access control lists, capabilities, or execution modes (e.g., ARM EL0/EL1) warrants a yes.

pid23221: Select if the device includes and enforces OS user accounts.
Presence of “root,” “admin,” or other user names in the UI or CLI, password prompts, or user-management commands (e.g., adduser, passwd) is sufficient.

pid23222: Select if the device implements a memory-management model with access protections (read-only, executable, writable, etc.).
Mentions of “MMU,” “MPU,” “NX bit,” “DEP,” “ASLR,” or memory sections flagged as RO/RX/RW indicate active protection.

pid24: Select if the device supports virtualization or containers.
Confirm with terms like “hypervisor,” “virtual machine,” “container,” “namespace isolation,” or “KVM/VMware/QEMU.”

pid241: Select if the device uses containers.
References to Docker, Podman, LXC, OCI images, or a container runtime show this property is present.

pid242: Select if the device runs a hypervisor.
Look for Xen, KVM, ESXi, Jailhouse, or proprietary hypervisor branding, or diagrams showing guest VMs on top of a host OS.

pid25: Select if the device includes a hardware or software root of trust.
Indicators include TPM, Secure Element, TrustZone, secure enclave, fuses storing boot keys, or language about “chain of trust.”

pid251: Select if the root of trust is physically accessible or not immutable.
If the secure element is socketed, firmware keys are stored in writable flash, or the documentation notes “keys can be re-provisioned,” mark this.

pid252: Select if the root of trust is immutable.
One-time-programmable (OTP) fuses, mask ROM, or “hardware-burned keys that cannot be changed” qualify.

pid26: Select if the device lacks firmware or software update support.
Absence of any documented update mechanism, or explicit statements that updates are not supported, meets this property.

pid27: Select if the device supports firmware or software updates.
Any mention of OTA, field upgrade, USB update, or maintenance firmware packages confirms.

pid271: Select if firmware/software updates are not cryptographically validated.
Mark this when updates rely solely on checksums, version numbers, or no integrity check at all. Phrases like “copy file to SD card and reboot” without signing steps are a clue.

pid272: Select if the device uses cryptographic integrity protection for firmware/software.
Look for “signed firmware,” “secure hash verification,” “public-key check,” or “secure boot validation” to select this.

pid2721: Select if firmware integrity relies on a shared key.
Words such as “symmetric key,” “shared secret,” or use of HMAC/CMAC with a single device-wide key indicate this scenario.

pid2722: Select if firmware is digitally signed with a private key (public-key scheme).
Confirm with statements about RSA/ECC signatures, certificate chains, or separate public/private keys for firmware validation.

pid273: Select if firmware updates are unencrypted.
If update images are distributed in plain binary or zip form with no encryption layer, choose this option.

pid274: Select if the user can select firmware/software versions during updates.
Menus offering “choose image,” “rollback,” or version pick-lists demonstrate this capability.

pid275: Select if firmware/software updates can be initiated remotely.
Any remote OTA service, cloud push, or API command that triggers an update qualifies.
</options>

<example>
<doc>
The SecureEdge IoT Gateway runs a hardened Linux kernel with SELinux enforced. It supports OTA firmware updates signed using RSA-2048 and allows administrators to rollback to previous versions. Firmware updates are distributed via a cloud API, and the system also includes a TPM for root-of-trust enforcement.
</doc>
{
  "thoughts": "The presence of a 'hardened Linux kernel' confirms an operating system (pid23), and SELinux implies access control enforcement (pid2322). The RSA-signed OTA updates confirm support for cryptographic integrity (pid272), use of a public-key scheme (pid2722), and remote update initiation (pid275). The ability to rollback shows support for version selection (pid274). The mention of TPM confirms a root of trust (pid25).",
  "pid23": "'Hardened Linux kernel' confirms the presence of an operating system.",
  "pid2322": "SELinux provides a privilege enforcement mechanism.",
  "pid25": "TPM is a hardware root of trust.",
  "pid272": "OTA firmware updates are 'signed using RSA-2048', confirming integrity protection.",
  "pid2722": "RSA-2048 signatures confirm a public-key-based scheme.",
  "pid274": "Firmware rollback feature confirms version selection during updates.",
  "pid275": "Firmware updates are 'distributed via a cloud API', indicating remote update support."
}
</example>

<example>
<doc>
The system firmware for the controller is updated via USB stick. The process does not require any authentication and involves placing a binary image on the stick and rebooting the device. There is no mention of checks, signatures, or encryption. Debug messages can be seen through a serial console.
</doc>
{
  "thoughts": "Firmware updates are clearly supported via USB (pid27), but the lack of checks or signatures and the ability to update with just a binary image confirms that no cryptographic validation is used (pid271). No encryption is mentioned for the firmware (pid273). Debug messages over a serial console suggest debugging capabilities (pid22).",
  "pid22": "Serial console displays debug messages, indicating debugging support.",
  "pid27": "Firmware update via USB stick indicates update support.",
  "pid271": "No authentication or signing confirms absence of cryptographic validation.",
  "pid273": "Update is a plain binary image with no encryption mentioned."
}
</example>

<example>
<doc>
The AirSecure Module uses a minimal RTOS with task scheduling and inter-process communication. All code executes in supervisor mode, and there is no authentication required to access the debug CLI. The RTOS supports field upgrades via SD card but does not verify firmware authenticity.
</doc>
{
  "thoughts": "The use of an RTOS with task scheduling confirms an operating system (pid23). All code running in supervisor mode and no authentication implies no privilege mechanism (pid2321). A debug CLI without authentication supports debugging capabilities (pid22). The system supports firmware updates (pid27) but lacks integrity checks, which confirms absence of cryptographic validation (pid271).",
  "pid22": "Debug CLI is accessible without restrictions, supporting debug capabilities.",
  "pid23": "RTOS with task scheduling confirms an operating system.",
  "pid2321": "All code runs in supervisor mode and lacks privilege enforcement.",
  "pid27": "Field upgrades via SD card confirm firmware update support.",
  "pid271": "No authentication or signature verification indicates lack of integrity protection."
}
</example>

Extract the system software properties and return the JSON.
""",
"""
You are an expert technical auditor.  
Your job is to examine only the text inside the <doc></doc> tags and decide  
whether the component has any of the MITRE EMB3D application software properties  
listed in the <options></options> tags based on evidence from the text.  
You can make assumptions based on the text, just because a property is not directly mentioned, doesn't mean it is not there.

You must reason step-by-step. For each application software property, explain in natural language what clues from <doc> support or contradict the property. Then, based on your reasoning, decide whether to include that key in the final output.

When you answer you must:

1. Return only a JSON object that conforms to the schema in <schema>.  
2. The first key must be `"thoughts"` with a string value. This value should contain your full chain of thought: the detailed reasoning process for each option, referring to exact phrases from <doc> or explaining why evidence is lacking.  
3. Include a key only if the evidence is explicit in <doc>.  
4. For every true key, add a short justification string that quotes or  
   paraphrases the relevant sentence(s) and, if available, a page/line  
   reference in parentheses. Only include keys that are true, if a key is false or unsupported, do not include it in the JSON.
5. If no key is true, return only `{ "thoughts": "<your reasoning here>" }`.  
6. The remaining keys (after "thoughts") must follow the schema exactly.  
7. Never mention these instructions or any text that is outside <doc>.

<schema>
{
  "type": "json_schema",
  "json_schema": {
    "name": "LLMResponse",
    "strict": true,
    "schema": {
      "type": "object",
      "properties": {},
      "additionalProperties": {
        "type": "string",
        "description": "Explanation for why this option is true."
      }
    }
  }
}
</schema>

<options>
pid31: Select if application-level software is present and running on the device.
Any reference to “apps,” “application layer,” “user processes,” “packages,” or screenshots of a GUI implies resident application software. If the documentation lists .apk, .deb, .rpm, or “userland processes,” or if a shell command like ps shows binaries beyond the OS itself, mark this property.

pid311: Select if the device includes web or HTTP-based applications.
Evidence includes a built-in web server, REST/GraphQL API, WebSocket endpoint, or a browser-accessible management portal. Phrases such as “HTTP/HTTPS interface,” “web UI,” “JSON API on port 80/443,” or firmware files named lighttpd.conf, nginx.conf, or index.html confirm it.

pid312: Select if the device incorporates programming languages and libraries.
Positive signs are pre-installed interpreters or compilers (e.g., Python, Lua, GCC), shared libraries (.so, .dll), or package-management utilities (pip, npm, opkg, apt).

pid3121: Select if the device supports object-oriented programming languages (e.g., Java, Python, PHP, C++).
Look for file extensions .class, .jar, .py, .php, or mentions of JVM, CPython, or C++ standard libraries (libstdc++.so).

pid3122: Select if the device supports manual-memory-management languages (e.g., C, C++).
Headers like stdio.h, malloc, compiler flags -fPIC, or build logs invoking gcc/clang indicate this capability.

pid32: Select if the device can deploy custom or external programs.
Any OTA app store, scripting console, container loader, or engineering tool that uploads binaries or logic diagrams (e.g., PLC ladder logic) qualifies.

pid321: Select if custom programs can be deployed from engineering software or an IDE.
PLC/RTU manuals referencing “Studio 5000,” “TIA Portal,” “Codesys,” or vendor IDE push-button downloads are clear indicators.

pid322: Select if the device provides a runtime environment for custom or external programs.
Examples include a Java VM, Python interpreter, Node.js runtime, or a vendor-specific script engine that executes uploaded code.

pid323: Select if the device supports program executable formats.
Look for acceptance of .exe, .elf, .bin, .hex, or architecture-specific binaries described in developer guides.

pid3231: Select if custom/external programs run as native binaries without confinement.
If uploaded code executes directly under the main OS with standard privileges (e.g., chmod +x then ./myapp), choose this.

pid3232: Select if custom/external programs execute within a sandboxed environment.
Indicators include references to “container,” “jail,” “AppArmor,” “seccomp-filtered runtime,” or a proprietary sandbox that restricts syscalls.

pid324: Select if the device supports “program uploads” that let an engineering workstation retrieve code from the device.
Functions named “download program from controller,” “backup logic,” or “export firmware binary” satisfy this property.

pid33: Select if the device offers interactive applications, services, or user interfaces.
CLI shells, graphical HMI panels, touchscreen menus, or voice-assistant skills are all evidence.

pid331: Select if the device exposes unauthenticated services.
Open Telnet/HTTP endpoints with no login, SNMP v1/v2c community “public,” or default-open MQTT topics count here.

pid332: Select if the device exposes authenticated services.
Any service that asks for credentials, certificates, API keys, tokens, or multifactor codes meets this criterion.

pid3321: Select if the device uses passwords for user authentication.
Presence of a login prompt, passwd file, web-form password field, or parameter like --password confirms this.

pid3322: Select if the device employs cryptographic mechanisms to authenticate users or sessions.
Evidence includes TLS client certificates, OAuth/JWT tokens, SSH keys, or signed challenge-response handshakes.
</options>

<example>
<doc>
The VisionEdge Pro device provides a touchscreen GUI for monitoring and configuration, with a built-in web dashboard accessible via HTTPS. It runs a Python-based application layer that utilizes Flask to serve a JSON API. The device also supports uploading custom logic scripts written in Python, which are executed using an internal interpreter. Login is required to access the web dashboard, and credentials are checked against a hashed password file. 
</doc>
{
  "thoughts": "The mention of a 'Python-based application layer' and 'touchscreen GUI' confirms the presence of application software (pid31) and interactive user interfaces (pid33). The use of Flask and a 'web dashboard accessible via HTTPS' confirms web-based application support (pid311). Running Python scripts confirms both support for object-oriented languages (pid3121) and a runtime environment (pid322). The presence of a password-verified login mechanism supports both authenticated services (pid332) and password-based authentication (pid3321).",
  "pid31": "Described as running a 'Python-based application layer' and providing a touchscreen GUI.",
  "pid311": "A 'web dashboard accessible via HTTPS' served by Flask implies HTTP-based application functionality.",
  "pid3121": "Python language and Flask framework confirm object-oriented language support.",
  "pid322": "Python interpreter executes uploaded scripts, confirming runtime environment support.",
  "pid33": "Touchscreen GUI confirms interactive application presence.",
  "pid332": "Login required to access the web dashboard supports authenticated services.",
  "pid3321": "Password-based access control using a hashed password file confirms password authentication."
}
</example>

<example>
<doc>
The AutoFlex controller integrates with engineering tools like Codesys and supports the upload of ladder logic programs. Uploaded logic runs directly on the embedded system and can be downloaded or backed up to an engineering workstation. It uses compiled binaries in .hex format and offers a USB-based serial CLI with no authentication required. 
</doc>
{
  "thoughts": "Integration with Codesys confirms custom program deployment via IDE (pid321). The use of .hex binaries and direct execution confirms support for executable formats (pid323) and native binary execution (pid3231). Mention of backup functionality implies program uploads (pid324). The unauthenticated USB CLI implies an exposed unauthenticated interface (pid331).",
  "pid321": "Support for Codesys confirms engineering software deployment capability.",
  "pid323": "Uses '.hex' binaries, confirming executable format support.",
  "pid3231": "Programs run 'directly on the embedded system', confirming native execution without sandboxing.",
  "pid324": "Programs can be 'downloaded or backed up' to an engineering workstation.",
  "pid331": "CLI via USB is accessible with 'no authentication', confirming unauthenticated service exposure."
}
</example>

<example>
<doc>
This device features an application framework with built-in support for REST APIs and MQTT. It provides TLS-based authentication and requires a token for API access. It includes a Node.js runtime, and applications can be deployed using NPM packages. The firmware includes system services for telemetry and diagnostics, all confined by seccomp filters.
</doc>
{
  "thoughts": "REST APIs and MQTT interfaces confirm application software (pid31) and web/HTTP-based services (pid311). The use of Node.js and NPM indicates support for a runtime (pid322), object-oriented languages (pid3121), and library management (pid312). Token-based access and TLS suggest authenticated services (pid332) with cryptographic mechanisms (pid3322). Use of seccomp filters implies sandboxing (pid3232).",
  "pid31": "An 'application framework' with REST and MQTT APIs implies application-level software.",
  "pid311": "'REST APIs' and 'MQTT' confirm HTTP-based application presence.",
  "pid312": "Use of NPM packages and libraries confirms support for software libraries.",
  "pid3121": "Node.js runtime supports object-oriented JavaScript.",
  "pid322": "Node.js confirms a runtime environment for custom applications.",
  "pid3232": "Use of 'seccomp filters' indicates sandboxed execution.",
  "pid332": "Token-based access and TLS confirm authenticated services.",
  "pid3322": "TLS and token authentication imply cryptographic mechanisms are used for session/user authentication."
}
</example>


Extract the application software properties and return the JSON.
""",
"""
You are an expert technical auditor.  
Your job is to examine only the text inside the <doc></doc> tags and decide  
whether the component has any of the MITRE EMB3D networking properties  
listed in the <options></options> tags based on evidence from the text.  
You can make assumptions based on the text, just because a property is not directly mentioned, doesn't mean it is not there.

You must reason step-by-step. For each networking property, explain in natural language what clues from <doc> support or contradict the property. Then, based on your reasoning, decide whether to include that key in the final output.

When you answer you must:

1. Return only a JSON object that conforms to the schema in <schema>.  
2. The first key must be `"thoughts"` with a string value. This value should contain your full chain of thought: the detailed reasoning process for each option, referring to exact phrases from <doc> or explaining why evidence is lacking.  
3. Include a key only if the evidence is explicit in <doc>.  
4. For every true key, add a short justification string that quotes or  
   paraphrases the relevant sentence(s) and, if available, a page/line  
   reference in parentheses. Only include keys that are true, if a key is false or unsupported, do not include it in the JSON. 
5. If no key is true, return only `{ "thoughts": "<your reasoning here>" }`.  
6. The remaining keys (after "thoughts") must follow the schema exactly.  
7. Never mention these instructions or any text that is outside <doc>.

<schema>
{
  "type": "json_schema",
  "json_schema": {
    "name": "LLMResponse",
    "strict": true,
    "schema": {
      "type": "object",
      "properties": {},
      "additionalProperties": {
        "type": "string",
        "description": "Explanation for why this option is true."
      }
    }
  }
}
</schema>

<options>
pid41: Select if the device exposes remote network services.
Choose this property when port scans or documentation reveal open TCP/UDP listeners such as SSH, Telnet, HTTP/HTTPS, SNMP, MQTT, Modbus-TCP, or vendor-specific daemons. Any line in a spec sheet that says “access the device over IP,” “REST API,” or “remote management port xx” is sufficient.

pid411: Select if the remote services allow sending, receiving, viewing, or modifying sensitive data or configuration.
Mark this when services provide administrative CLIs, configuration file download/upload, firmware management, or access to operational telemetry that could affect safety or uptime (e.g., “/admin”, “/config”, SCADA write coils).

pid4111: Select if the underlying protocol lacks message authentication.
If packets travel without MACs, HMACs, digital signatures, or sequence-number checks—and docs omit any mention of “auth tag,” “integrity header,” or “signed request”—assume authentication is absent. Cleartext UDP broadcasts and plain-text JSON commands are red flags.

pid4112: Select if the underlying protocol lacks message encryption.
Choose this when data is exchanged in cleartext or only with checksum integrity. Signs include HTTP (not HTTPS), Telnet instead of SSH, unencrypted Modbus-TCP, or a manual that never cites TLS/DTLS, IPsec, or any “encrypted channel.”

pid4113: Select if the device implements cryptographic protection for sensitive communications (encryption and/or authentication).
Evidence includes TLS/DTLS, SSH, IPsec, MACsec, or custom protocols that specify AES, ChaCha20-Poly1305, HMAC, certificate chains, or mutual authentication handshakes. Log entries such as “Starting OpenSSL” or configuration fields for certificates/keys also qualify.

pid42: Select if the device can forward or route network messages.
Indicators are routing tables, NAT/firewall rules, bridge or switch modes, IP-forwarding kernel parameters, or language like “acts as gateway/edge router.” CLI commands such as route add, ip forward 1, or references to BGP/OSPF/RIP confirm this capability.</options>

<example>
<doc>
The NetMon-300 device supports remote configuration via HTTP and exposes an administrative dashboard accessible at port 8080. It allows operators to modify network parameters, view traffic logs, and upload firmware images. Communication is unencrypted and conducted over plain HTTP. No documentation references TLS, certificates, or encryption settings.
</doc>
{
  "thoughts": "The phrase 'supports remote configuration via HTTP' and 'administrative dashboard accessible at port 8080' confirms that remote services are exposed (pid41). The ability to 'modify network parameters' and 'upload firmware images' shows access to sensitive configuration (pid411). Since the communication is explicitly described as 'unencrypted' and over 'plain HTTP', the device lacks message encryption (pid4112). The absence of mention of MACs, HMACs, or signatures suggests no message authentication (pid4111). There is no evidence for cryptographic protection (pid4113) or forwarding behavior (pid42).",
  "pid41": "Device exposes HTTP service at port 8080 for remote configuration.",
  "pid411": "Allows modifying network parameters and uploading firmware—sensitive operations.",
  "pid4111": "No mention of MACs or signed messages implies no message authentication.",
  "pid4112": "Uses plain HTTP; no evidence of encryption like TLS or IPsec."
}
</example>

<example>
<doc>
The controller uses HTTPS to provide a REST API for telemetry retrieval and configuration updates. TLS certificates are used for mutual authentication between the client and device. The API supports operations like reading process status and updating device thresholds.
</doc>
{
  "thoughts": "Use of HTTPS and TLS confirms remote network services (pid41). The API allows configuration updates and status reads, indicating access to sensitive data (pid411). Mutual TLS and certificates confirm cryptographic protection (pid4113). Since the protocol uses TLS, encryption (pid4112) and authentication (pid4111) are handled securely. There is no indication that the device routes or forwards traffic (pid42).",
  "pid41": "REST API over HTTPS is a remote network service.",
  "pid411": "Configuration updates and telemetry access indicate sensitive operations.",
  "pid4113": "Mutual TLS and certificate-based authentication confirm encryption and authentication."
}
</example>

<example>
<doc>
This embedded bridge device supports packet forwarding between two Ethernet interfaces. It operates in Layer 2 bridge mode and can be configured with VLAN tagging rules. There are no remote access protocols enabled.
</doc>
{
  "thoughts": "The text confirms that the device performs 'packet forwarding' between interfaces and operates in 'Layer 2 bridge mode', which supports the routing/forwarding property (pid42). No remote services are exposed, so pid41 and its subproperties do not apply.",
  "pid42": "Described as forwarding packets in Layer 2 bridge mode between Ethernet interfaces."
}
</example>

Extract the networking properties and return the JSON.
"""
]

step1_example_response = {
"component_name": "Component 1", 
"manufacturer": "ABC Company", 
"pid11": "Explanation for why this property is true.", 
"pid122": "Explanation for why this property is true.", 
"pid1241": "Explanation for why this property is true."
}
