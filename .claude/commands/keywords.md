# Keyword Research

Research SEO keywords and content opportunities for a topic.

## Usage

```
/keywords <seed topic> [--intent informational|commercial|transactional]
```

## What This Does

1. Activates the Keyword Researcher Agent
2. Finds keyword clusters around your topic
3. Identifies high-opportunity keywords (high volume, low difficulty)
4. Creates content recommendations and calendar

## Instructions for Claude

When this command is run:

1. Use the KeywordResearcherAgent at `agents/research/keyword_researcher.py`
2. Call research_keywords with the seed topic
3. Present findings focusing on:
   - Keyword clusters
   - Top opportunities
   - Quick wins
   - Content calendar suggestions

```python
from agents.research.keyword_researcher import KeywordResearcherAgent

agent = KeywordResearcherAgent(domain="AI consulting")
report = agent.research_keywords(
    seed_topic="$ARGUMENTS",
    depth="comprehensive"
)
```

## Output Format

### 🔍 Keyword Research: [Topic]

**Keyword Clusters:**

**Cluster 1: [Name]**
| Keyword | Volume | Difficulty | Intent |
|---------|--------|------------|--------|
| ... | ... | ... | ... |

**Top Opportunities:**
1. "keyword" - Volume: X, Difficulty: low
2. ...

**Quick Wins:**
- [ ] Quick win 1
- [ ] Quick win 2

**Content Calendar:**
| Week | Content | Target Keywords |
|------|---------|----------------|
| 1 | ... | ... |
