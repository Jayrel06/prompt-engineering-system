# Generate Content Ideas

Generate content ideas based on trends, audience, and strategic goals.

## Usage

```
/content-ideas <topic> [--count 10] [--formats blog,linkedin,twitter]
```

## What This Does

1. Activates the Content Ideator Agent
2. Generates content ideas across specified formats
3. Provides outlines and hooks for each idea
4. Creates a content calendar

## Instructions for Claude

When this command is run:

1. Use the ContentIdeatorAgent at `agents/research/content_ideator.py`
2. Call generate_ideas with the topic
3. Present ideas with:
   - Title and hook
   - Format and effort level
   - Target audience and goal
   - Content outline

```python
from agents.research.content_ideator import ContentIdeatorAgent

agent = ContentIdeatorAgent()
session = agent.generate_ideas(
    topic="$ARGUMENTS",
    count=10,
    formats=["blog_post", "linkedin_post", "twitter_thread"]
)
```

## Output Format

### 💡 Content Ideas: [Topic]

**Top Ideas:**

1. **[Title]**
   - Format: blog_post | Effort: medium
   - Hook: "..."
   - Goal: awareness
   - Outline:
     - Point 1
     - Point 2

2. **[Title]**
   ...

**Quick Wins (< 1 hour):**
- [ ] Idea 1
- [ ] Idea 2

**Evergreen Content:**
- Idea that stays relevant

**4-Week Calendar:**
| Week | Day | Content | Platform |
|------|-----|---------|----------|
| 1 | Mon | ... | ... |
