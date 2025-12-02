# Find Experts

Find and profile domain experts for collaboration and learning.

## Usage

```
/find-experts <domain or topic>
```

## What This Does

1. Activates the Expert Finder Agent
2. Identifies thought leaders and influencers
3. Profiles experts with collaboration potential
4. Provides outreach templates

## Instructions for Claude

When this command is run:

1. Use the ExpertFinderAgent at `agents/research/expert_finder.py`
2. Call find_experts with the query
3. Present findings with:
   - Top experts by relevance
   - Collaboration opportunities
   - Outreach templates

```python
from agents.research.expert_finder import ExpertFinderAgent

agent = ExpertFinderAgent(domain="AI and automation")
report = agent.find_experts(
    query="$ARGUMENTS",
    min_followers=1000
)
```

## Output Format

### 👥 Expert Finder: [Domain]

**Top Experts:**

**👤 [Name]**
- Title: ... at ...
- Followers: X | Engagement: X%
- Expertise: topic1, topic2
- Collaboration potential: 🔥 High
- Best approach: ...

**Collaboration Opportunities:**
| Type | Expert | Opportunity | Priority |
|------|--------|-------------|----------|
| Guest Post | ... | ... | High |

**Outreach Template:**
```
Hi [Name],

I've been following your work on [topic]...
```

**Key Communities:**
- Community 1
- Community 2

**Events & Conferences:**
- Event 1
- Event 2
