step4_complete_prompt = """You are a threat modelling assistant.
Your task is to analyse a component described inside the <doc> tags.
Assume that this component has completely failed.
Your objective is to assign a numeric criticality value for each of the six risk categories defined in the <categories> tags below.
The criticality ratings must be floating-point numbers between 0 and 1 (inclusive).
You are allowed to use any number between 0.0 and 1.0 based on your judgment.
You must reason step by step and provide a detailed explanation of your thinking for each category under the "thoughts" key.
You must return only valid JSON matching the exact structure below.
Do not rename or add any keys. Do not include any additional output.

<JSON Structure>
{
  "thoughts": "[step-by-step reasoning for all six categories]",
  "dc": {
“rating”: <float between 0 and 1>,
“explanation” “[Justification of the rating]”
},
  "ipc": {
“rating”: <float between 0 and 1>,
“explanation” “[Justification of the rating]”
},
  "lic": {
“rating”: <float between 0 and 1>,
“explanation” “[Justification of the rating]”
},
  "sc": {
“rating”: <float between 0 and 1>,
“explanation” “[Justification of the rating]”
},
  "fc": {
“rating”: <float between 0 and 1>,
“explanation” “[Justification of the rating]”
},
  "fc2": {
“rating”: <float between 0 and 1>,
“explanation” “[Justification of the rating]”
}
}
</JSON Structure>
<categories>
Data Criticality (DC)  
None (0): Component does not store or process sensitive personal data (example: GNSS system)  
Low (0.01-0.33): Only forwards encoded sensitive personal data (example: network device)  Medium (0.33-0.66): Processes sensitive personal data (example: video camera)  
High (0.66-1): Stores sensitive personal data (example: data historian)
Intellectual Property Criticality (IPC)  
None (0): Hosts processes with no intellectual-property value  
Low (0.01-0.33): Hosts low-value IP (common proprietary software) (example: network devices)
Medium (0.33-0.66): Hosts medium-value IP (rare proprietary software) (example: DP system)  
High (0.66-1): Hosts high-value IP (innovative proprietary software) (example: ANS)
Location Information Criticality (LIC)  
None (0): Does not store, process, or advertise location-sensitive information  
High (1): Stores, processes, or advertises location-sensitive information
Safety Criticality (SC)  
None (0): A failure in the component may cause no injuries  
Minor (0.01-0.25): A failure in the component may cause single or minor injuries  
Significant (0.25-0.5): A failure in the component may cause multiple minor injuries or one severe injury  
Severe (0.5-0.75): A failure in the component may cause a single fatality or multiple severe injuries  
Catastrophic (1): A failure in the component may cause multiple fatalities and severe injuries
Financial Criticality (FC) — damage to equipment, property, or income  
None (0): A failure in the component may cause no damage to equipment or other property  
Minor (0.01-0.25): A failure in the component may cause local equipment damage, small property damage, or minor income loss  
Significant (0.25-0.5): A failure in the component may cause damage to CPS or other property, or significant income loss  
Severe (0.5-0.75): A failure in the component may cause severe damage to CPS or other property, or income loss equal to several days of operation  
Catastrophic (1): A failure in the component may cause total loss of CPS or other properties
Financial Criticality 2 (FC2) — unexpected SMS billing  
None (0): No unexpected billing for SMS-enabled devices  
Low (0.01-0.33): Minor unexpected billing  
Medium (0.33-0.66): Moderate unexpected billing  
High (0.66-1): Large unexpected billing
</categories>
<example>
<doc> 
This device is used to store the phone numbers of the users. It supports basic CRUD operations on contact entries, allowing administrators to add, remove, or update user phone numbers.
</doc>
{
  "thoughts": "The device is described as storing user phone numbers, which qualifies as sensitive personal data and results in a high Data Criticality (DC) score. There is no mention of any intellectual property being hosted or processed by this device, so IPC is none. There is no indication that the device handles or advertises location-sensitive information, so LIC is rated none. A failure in this device would not result in any physical harm or injury, so Safety Criticality (SC) is none. From a financial standpoint, losing access to phone numbers could cause operational disruption or minor income loss, so FC is rated minor. Since phone numbers may be used in SMS-capable systems, there could be some risk of unexpected messaging activity if compromised, but without clear evidence of SMS integration, FC2 is rated low.",
  "dc": {
    "rating": 0.8,
    "explanation": "The device stores user phone numbers, which are considered sensitive personal data. Storing this type of information corresponds to a high data criticality rating."
  },
  "ipc": {
    "rating": 0.0,
    "explanation": "The device is not described as containing or processing any form of intellectual property."
  },
  "lic": {
    "rating": 0.0,
    "explanation": "There is no indication that the device stores, processes, or advertises any location-sensitive data."
  },
  "sc": {
    "rating": 0.0,
    "explanation": "Failure of the device would not result in physical harm or injury to any individual."
  },
  "fc": {
    "rating": 0.2,
    "explanation": "A failure of the device could lead to the loss of phone numbers, which could cause some operational inconvenience or minor business disruption, resulting in minor financial impact."
  },
  "fc2": {
    "rating": 0,
    "explanation": "Although phone numbers could be linked to SMS communication, there is no evidence that the device itself triggers or manages SMS billing."
  }
}
</example>

<example>
<doc>
This system is a GPS receiver installed on board a vessel. It receives satellite signals, processes them, and provides location and timing data to other navigation systems. It does not store user data but continuously broadcasts vessel position.
</doc>
{
  "thoughts": "The GPS receiver processes and provides location data, but does not store sensitive personal data, so Data Criticality (DC) is none. It does not host any intellectual property, so IPC is none. Since it directly provides location-sensitive information, Location Information Criticality (LIC) is high. If this device fails, the vessel could lose accurate navigation input, leading to navigational hazards that could result in collisions or groundings, so Safety Criticality (SC) is significant to severe depending on context. Financially, damage caused by navigational errors can be severe, involving equipment/property damage or operational downtime, so FC is severe. The GPS itself is not SMS-enabled, so Financial Criticality 2 (FC2) is none.",
  "dc": {
    "rating": 0.0,
    "explanation": "The device does not store or process sensitive personal data."
  },
  "ipc": {
    "rating": 0.0,
    "explanation": "No intellectual property is stored or processed by the GPS receiver."
  },
  "lic": {
    "rating": 1.0,
    "explanation": "The GPS receiver continuously provides vessel position data, which is highly location-sensitive."
  },
  "sc": {
    "rating": 0.6,
    "explanation": "Failure could lead to navigational hazards, potentially causing accidents that result in severe injuries or fatalities."
  },
  "fc": {
    "rating": 0.7,
    "explanation": "Loss of GPS accuracy could cause major accidents at sea, leading to severe equipment damage and operational disruption."
  },
  "fc2": {
    "rating": 0.0,
    "explanation": "The device does not trigger SMS-related activities."
  }
}
</example>

<example>
<doc>
This is a data historian server that collects, stores, and archives process data from multiple sensors and control systems across the plant. It is used for analytics, reporting, and long-term data retention.
</doc>
{
  "thoughts": "The historian server stores large amounts of process data, which may include sensitive operational details and potentially personal data in logs, so DC is high. The historian software and stored datasets may represent valuable intellectual property (e.g., unique operational data, proprietary processes), so IPC is medium to high. The server does not inherently advertise or provide location-specific data, so LIC is none. If it fails, plant safety is not directly impacted in real time (other systems continue to operate), so SC is low to none. Financially, the historian is crucial for compliance, optimization, and troubleshooting; its failure could result in significant business and operational losses, so FC is significant. There is no SMS capability, so FC2 is none.",
  "dc": {
    "rating": 0.85,
    "explanation": "The historian stores process data, some of which may include sensitive or personal data, giving it high data criticality."
  },
  "ipc": {
    "rating": 0.5,
    "explanation": "The historian contains unique operational datasets and proprietary processes, which have medium intellectual property value."
  },
  "lic": {
    "rating": 0.0,
    "explanation": "The historian does not handle or advertise location-sensitive information."
  },
  "sc": {
    "rating": 0.1,
    "explanation": "Its failure would not immediately cause injuries, though it could indirectly reduce situational awareness. Thus, safety criticality is minor."
  },
  "fc": {
    "rating": 0.45,
    "explanation": "Loss of the historian could disrupt compliance, analytics, and reporting, leading to significant financial and operational impacts."
  },
  "fc2": {
    "rating": 0.0,
    "explanation": "The historian has no SMS-related functions."
  }
}
</example>

Estimate the criticality ratings and return the JSON.
"""

step4_example_response = """{"dc":{"rating": "0.3","explanation": "Explanation for why this rating was given."},
"ipc":{"rating": "0.3","explanation": "Explanation for why this rating was given."},
"lic":{"rating": "0.0","explanation": "Explanation for why this rating was given."},
"sc":{"rating": "0.5","explanation": "Explanation for why this rating was given."},
"fc":{"rating": "0.3","explanation": "Explanation for why this rating was given."},
"fc2":{"rating": "0.0","explanation": "Explanation for why this rating was given."}}"""
