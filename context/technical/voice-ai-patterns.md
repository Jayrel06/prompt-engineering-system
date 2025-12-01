# Voice AI Patterns

## Core Design Principles

### One Question at a Time
- Never ask multiple questions in one turn
- Wait for answer before proceeding
- Reduces confusion and abandonment

### Spell Out Numbers
- "two to four hours" not "2-4 hours"
- "eight thousand dollars" not "$8,000"
- Exception: phone numbers, addresses

### Natural Pauses
- Don't rush
- Allow processing time
- Match human conversation rhythm

### Clear Confirmations
- Repeat back key information
- "So that's Tuesday at 3pm, correct?"
- Prevents misunderstandings

---

## Conversation Flow Patterns

### Opening
```
"Good [morning/afternoon], thank you for calling [Business].
This is [Name], how can I help you today?"
```
- Warm, professional
- Identify business
- Open-ended question

### Intent Classification
```
Listen → Classify Intent [
  Schedule Appointment → Booking Flow
  Service Question → FAQ Flow
  Emergency → Emergency Flow
  Transfer Request → Transfer Flow
  Unknown → Clarification
]
```

### Information Gathering
```
1. Name → "May I have your name?"
2. Phone → "Best phone number to reach you?"
3. Address → "Address where service is needed?"
4. Details → "Can you tell me more about [issue]?"
```
- One field at a time
- Acknowledge each answer

### Closing
```
"Great, you're all set for [summary].
You'll receive a confirmation [method].
Is there anything else I can help with today?"
```

---

## Emergency Handling

### Detection Keywords
- Gas leak/smell gas
- Carbon monoxide
- Flooding/water emergency
- No heat (freezing weather)
- Electrical sparking/smoke
- Fire

### Response Pattern
```
Detect Emergency → Immediate Response:
"This sounds like an emergency. For your safety,
[specific instruction]. I'm connecting you to
our emergency line right now."
```

### Always
- Prioritize safety instructions
- Connect to human immediately
- Never continue normal flow

---

## Objection Handling

### Price Concerns
```
"I understand budget is important. Our technicians
can provide options that fit different budgets
when they assess your situation."
```

### Time Concerns
```
"I hear you. Let me see what we can do to
accommodate your schedule..."
```

### Trust Concerns
```
"That's a fair question. [Business] has been
serving [area] for [years], and we [trust builder]."
```

### Want to Think About It
```
"Of course. Would you like me to send you
some information to review? What's a good email?"
```

---

## Data Collection Standards

### Required Fields
| Field | Prompt | Format |
|-------|--------|--------|
| Name | "May I have your name?" | Full name |
| Phone | "Best number to reach you?" | E.164 (+1XXXXXXXXXX) |
| Address | "Address for service?" | Full with city/state/zip |
| Service | (from conversation) | Predefined category |
| Urgency | (from conversation) | emergency/urgent/standard/flexible |

### Optional Fields
- Email (for confirmation)
- Best callback time
- How they found us
- Additional notes

---

## Prompt Structure

### Identity Block
```
You are [NAME], the [warm/professional/energetic]
receptionist for [BUSINESS]. You speak at a
[measured/natural/upbeat] pace.
```

### Rules Block
```
CRITICAL RULES:
1. One question at a time
2. Spell out numbers
3. Never reveal AI nature
4. Emergency detection
5. Information boundaries
```

### Business Info Block
```
Hours: [HOURS]
Services: [SERVICES]
Emergency: [PROTOCOL]
FAQ: [Q&A PAIRS]
```

### Flows Block
```
For [INTENT], follow this flow:
1. [Step 1]
2. [Step 2]
...
```

---

## Testing Checklist

### Happy Path
- [ ] Normal appointment booking
- [ ] Service inquiry
- [ ] Basic FAQ

### Edge Cases
- [ ] Caller says only one word
- [ ] Caller speaks very fast
- [ ] Background noise
- [ ] Multiple questions at once

### Emergency
- [ ] Each emergency type detected
- [ ] Proper escalation triggered

### Objections
- [ ] Price objection handled
- [ ] Time objection handled
- [ ] "Let me think about it" handled

### Failure Modes
- [ ] Unable to understand caller
- [ ] System can't answer question
- [ ] Graceful transfer to human

---

## Platform-Specific Notes

### VAPI
- Custom functions for CRM integration
- Webhook for real-time updates
- Voice cloning available

### Retell
- Simpler setup
- Good for standard use cases
- Less customization

### Common Integrations
- Calendar (Google, Calendly)
- CRM (HubSpot, Salesforce)
- SMS (Twilio)
- n8n webhooks
