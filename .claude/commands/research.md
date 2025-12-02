# Research Topic

Run comprehensive research using the multi-agent research system.

## Usage

```
/research <topic>
```

## What This Does

1. Activates the Research Orchestrator
2. Runs multiple specialized agents in parallel:
   - Trend Scout: Find emerging trends
   - Keyword Researcher: SEO opportunities
   - Social Listener: Social media conversations
   - Audience Analyst: Target audience insights
   - Competitor Monitor: Market positioning
3. Combines insights into a unified report
4. Provides actionable recommendations

## Example

```
/research AI automation for small business
```

## Instructions for Claude

When this command is run:

1. Use the research orchestrator at `agents/research/orchestrator.py`
2. Run the quick_research method for fast results, or full_research for comprehensive analysis
3. Present findings in a clear, actionable format:
   - Key trends
   - Top keyword opportunities
   - Audience insights
   - Content recommendations
   - Next steps

```python
from agents.research.orchestrator import ResearchOrchestrator

orchestrator = ResearchOrchestrator()
report = orchestrator.quick_research("$ARGUMENTS")
```

## Output Format

Present results as:

### 📊 Research Summary: [Topic]

**Key Trends:**
- Trend 1 (growth rate, relevance)
- Trend 2

**Keyword Opportunities:**
- Keyword 1 (volume, difficulty)
- Keyword 2

**Audience Insights:**
- Segment information
- Channel preferences

**Recommendations:**
1. Action item 1
2. Action item 2

**Next Steps:**
- [ ] Step 1
- [ ] Step 2
