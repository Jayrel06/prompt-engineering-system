# Social Listening

Monitor social media for relevant conversations and opportunities.

## Usage

```
/social-listen [keywords] [--platforms twitter,linkedin,reddit]
```

## What This Does

1. Activates the Social Listener Agent
2. Monitors platforms for relevant mentions and conversations
3. Identifies engagement opportunities
4. Extracts content ideas from discussions

## Instructions for Claude

When this command is run:

1. Use the SocialListenerAgent at `agents/research/social_listener.py`
2. Call listen with specified keywords
3. Present findings with:
   - Recent mentions with sentiment
   - Active conversations
   - Engagement opportunities
   - Content ideas from conversations

```python
from agents.research.social_listener import SocialListenerAgent

agent = SocialListenerAgent(keywords=["AI consulting", "automation"])
report = agent.listen(
    platforms=["twitter", "linkedin", "reddit"],
    time_period="24h"
)
```

## Output Format

### 👂 Social Listening Report

**Overview:**
- Total mentions: X
- Sentiment: X% positive, X% negative

**Recent Mentions:**

😊 [@user on Twitter]
"Quote..."
- Engagement: X likes
- Opportunity: engagement

**Active Conversations:**

🔗 [Reddit] "Thread Title"
- Participants: X
- Key questions asked
- Engagement opportunity

**Engagement Opportunities:**
1. 🔴 [High] Platform - Description
2. 🟡 [Medium] Platform - Description

**Content Ideas from Conversations:**
- Idea 1
- Idea 2
