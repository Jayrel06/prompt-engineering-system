# Build Case Study

Create a compelling case study from project data.

## Usage

```
/case-study <project description or data>
```

## What This Does

1. Activates the Case Study Builder Agent
2. Creates structured outline
3. Writes full draft
4. Generates format variations (LinkedIn, email, etc.)

## Instructions for Claude

When this command is run:

1. Use the CaseStudyBuilderAgent at `agents/research/case_study_builder.py`
2. Create ProjectData from the input
3. Generate outline, draft, and variations
4. Present with:
   - Structured outline
   - Full draft sections
   - Platform-specific versions

```python
from agents.research.case_study_builder import CaseStudyBuilderAgent, ProjectData

agent = CaseStudyBuilderAgent()

project = ProjectData(
    client_industry="...",
    client_size="...",
    challenge="...",
    solution="...",
    timeline="...",
    results=[{"metric": "...", "value": "..."}],
    testimonial="...",
    technologies=["..."]
)

outline = agent.create_outline(project, style="success_story")
draft = agent.write_draft(outline)
variations = agent.generate_variations(draft, ["linkedin", "email"])
```

## Output Format

### 📋 Case Study: [Title]

**Executive Summary:**
[2-3 sentence summary]

**Key Metrics:**
| Metric | Result |
|--------|--------|
| ... | ... |

**Outline:**
1. The Challenge
2. The Solution
3. The Results
4. Key Learnings

**Draft Sections:**

## The Challenge
[Content]

## The Solution
[Content]

## The Results
[Content]

---

**LinkedIn Version:**
```
[LinkedIn-formatted post]
```

**Email Version:**
```
Subject: [Subject line]
[Email content]
```
