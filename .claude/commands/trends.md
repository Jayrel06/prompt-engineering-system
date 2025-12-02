# Analyze Trends

Scout for emerging trends across platforms relevant to your topic.

## Usage

```
/trends [topic] [--platforms twitter,linkedin,reddit]
```

## What This Does

1. Activates the Trend Scout Agent
2. Analyzes trends across specified platforms
3. Identifies opportunities with high relevance
4. Provides content angles and recommendations

## Instructions for Claude

When this command is run:

1. Use the TrendScoutAgent at `agents/research/trend_scout.py`
2. Call analyze_trends with the topic
3. Present findings focusing on:
   - Top trending topics
   - Growth rates and predictions
   - Content opportunities
   - Recommended actions

```python
from agents.research.trend_scout import TrendScoutAgent

agent = TrendScoutAgent(industry="AI consulting")
report = agent.analyze_trends(
    platforms=["twitter", "linkedin", "reddit", "youtube"],
    time_window="7d",
    min_relevance=0.6
)
```

## Output Format

### 🔥 Trend Analysis: [Topic]

**Hot Trends:**
| Trend | Platform | Growth | Relevance |
|-------|----------|--------|-----------|
| ... | ... | ... | ... |

**Top Opportunities:**
1. Opportunity with urgency level
2. ...

**Content Angles:**
- Angle 1
- Angle 2

**Recommended Actions:**
- [ ] Action 1
- [ ] Action 2
