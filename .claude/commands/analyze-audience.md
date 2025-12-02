# Analyze Audience

Analyze and segment your target audience for better content and messaging.

## Usage

```
/analyze-audience <target description>
```

## What This Does

1. Activates the Audience Analyst Agent
2. Creates audience segments with demographics and psychographics
3. Builds detailed buyer personas
4. Provides channel and messaging recommendations

## Instructions for Claude

When this command is run:

1. Use the AudienceAnalystAgent at `agents/research/audience_analyst.py`
2. Call analyze_audience with the target description
3. Present findings with:
   - Audience segments
   - Buyer personas
   - Channel strategy
   - Messaging guidelines

```python
from agents.research.audience_analyst import AudienceAnalystAgent

agent = AudienceAnalystAgent(business_type="AI consulting")
analysis = agent.analyze_audience(
    target_description="$ARGUMENTS",
    depth="detailed"
)
```

## Output Format

### 👥 Audience Analysis

**Segments:**

**1. [Segment Name]**
- Size: X
- Demographics: ...
- Pain points: ...
- Goals: ...
- Preferred channels: ...

**Buyer Personas:**

**👤 [Persona Name]**
- Role: ...
- Challenge: ...
- Goal: ...
- Messaging tone: ...
- Quote: "..."

**Channel Strategy:**
| Channel | Priority | Content Type | Frequency |
|---------|----------|--------------|-----------|
| LinkedIn | High | ... | Daily |

**Messaging Guidelines:**
1. Guideline 1
2. Guideline 2
