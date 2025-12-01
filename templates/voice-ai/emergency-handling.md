# Emergency Handling Template

## Purpose
Comprehensive emergency detection and response for voice AI across industries.

---

## Universal Emergency Keywords

### Life Safety
- Fire
- Smoke (visible)
- Gas leak / smell gas
- Carbon monoxide / CO alarm
- Explosion
- Electrocution
- Someone injured / hurt

### Industry-Specific

#### HVAC
- No heat (when freezing outside)
- No AC (extreme heat, elderly, infants)
- Gas smell
- Carbon monoxide alarm
- Sparking from unit
- Burning smell from vents

#### Plumbing
- Flooding / water everywhere
- Sewage backup
- Gas smell (gas water heater)
- No water (entire house)
- Burst pipe
- Water main break

#### Electrical
- Sparking / arcing
- Burning smell from outlet/panel
- Smoke from electrical
- Shock / electrocution
- Power out entire house
- Buzzing from panel

#### Medical (PT Clinics)
- Patient fallen
- Difficulty breathing
- Chest pain
- Loss of consciousness
- Severe pain (beyond normal)

---

## Emergency Response Template

```
[DETECTION]
When caller mentions any emergency keyword:

[IMMEDIATE RESPONSE]
"This sounds like an emergency. [SAFETY_INSTRUCTION]"

[SAFETY_INSTRUCTIONS by type]
- Gas leak: "Please leave the house immediately and don't use any light switches or electronics."
- Fire/smoke: "Please evacuate immediately and call 911."
- Flooding: "If safe, try to shut off the main water valve."
- No heat (freezing): "Do you have a safe way to stay warm? Space heater or can you go somewhere warm?"
- Electrical sparking: "Please stay away from the area and don't touch anything."
- Medical: "Please call 911 immediately if this is a medical emergency."

[ESCALATION]
"I'm connecting you to our emergency line right now."
[TRANSFER TO EMERGENCY NUMBER]

[IF NO TRANSFER AVAILABLE]
"Our emergency number is [EMERGENCY_PHONE]. Please call them immediately. They're available twenty-four seven."
```

---

## Detection Logic

### Explicit Keywords (Immediate trigger)
These words alone trigger emergency response:
- Gas leak
- Carbon monoxide
- Flooding
- Electrocution
- Fire
- Smoke

### Contextual Keywords (Require context)
These need additional context:
- "No heat" + (temperature check)
- "No AC" + (vulnerable person or extreme heat)
- "Water" + (everywhere, flooding, emergency)
- "Smell" + (gas, burning, smoke)

### Context Questions
```
If unclear severity:
"Can you tell me more about what's happening right now?"
"Is anyone in immediate danger?"
"How long has this been going on?"
```

---

## Non-Emergency Similar Phrases

Train to distinguish from emergencies:

| Sounds Like Emergency | Actually |
|-----------------------|----------|
| "My AC died" | Equipment not working (urgent, not emergency) |
| "I have no hot water" | Inconvenient but not dangerous |
| "Something smells weird" | Needs follow-up questions |
| "My heater isn't working" | Check temperature context |

---

## Escalation Paths

### Primary: Transfer to Emergency Line
```
Transfer to: [EMERGENCY_PHONE]
Announce: "Emergency call from [caller name if known]"
```

### Secondary: Provide Emergency Number
```
"Our emergency line is [EMERGENCY_PHONE].
They're available around the clock.
Please call them right now."
```

### Tertiary: 911 Referral
```
"This sounds like it may require emergency services.
Please hang up and call nine one one immediately.
Your safety is the priority."
```

---

## Post-Emergency Logging

Capture for every emergency call:
- Timestamp
- Caller phone
- Emergency type detected
- Keywords that triggered
- Action taken
- Transfer successful (yes/no)

---

## Testing Checklist

Test each scenario before deployment:

- [ ] "I smell gas in my house"
- [ ] "My carbon monoxide detector is going off"
- [ ] "There's water flooding my basement"
- [ ] "I have no heat and it's below freezing"
- [ ] "There's sparking coming from my electrical panel"
- [ ] "I see smoke coming from my vents"
- [ ] "My elderly mother has no AC and it's 100 degrees"
- [ ] Edge case: "My gas stove won't light" (not emergency)
- [ ] Edge case: "I need my AC fixed" (not emergency)
