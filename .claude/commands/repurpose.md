# Repurpose Content

Adapt content for multiple platforms and formats.

## Usage

```
/repurpose <content or file path> [--formats twitter,linkedin,email]
```

## What This Does

1. Activates the Format Adapter Agent
2. Adapts content for specified platforms
3. Provides platform-specific versions
4. Creates a posting calendar

## Instructions for Claude

When this command is run:

1. Use the FormatAdapterAgent at `agents/research/format_adapter.py`
2. Call adapt_content with the source content
3. Present adapted versions for each platform with:
   - Formatted content
   - Hashtags and CTAs
   - Media suggestions
   - Posting tips

```python
from agents.research.format_adapter import FormatAdapterAgent

agent = FormatAdapterAgent()
bundle = agent.adapt_content(
    content="...",
    source_format="blog",
    target_formats=["twitter_thread", "linkedin", "email"]
)
```

## Output Format

### 🔄 Content Repurposing

**Source:** [Original format]
**Efficiency:** X%

---

**📱 TWITTER THREAD**
```
1/ [Hook]

2/ [Point 1]
...
```
🏷️ #hashtag1 #hashtag2
📣 CTA: ...
🖼️ Media: Infographic suggestion
💡 Best time: 9am

---

**💼 LINKEDIN**
```
[Formatted for LinkedIn]
```
🏷️ #hashtag1 #hashtag2
📣 CTA: Comment question
💡 Best time: 8am Tuesday

---

**📅 Posting Calendar:**
| Day | Platform | Content | Time |
|-----|----------|---------|------|
| 1 | Twitter | Thread | 9am |
| 2 | LinkedIn | Post | 8am |
