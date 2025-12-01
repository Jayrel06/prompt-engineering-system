# Research to Action Chain

A 4-stage prompt chain that transforms research questions into actionable plans.

## Overview

```
[Research Question] → Stage 1: Deep Research → Stage 2: Synthesis → Stage 3: Planning → Stage 4: Action Items → [Executable Plan]
```

## Stage 1: Deep Research

**Purpose:** Gather comprehensive information on the topic.

```xml
<role>You are a thorough research analyst specializing in {{domain}}.</role>

<task>
Conduct comprehensive research on: {{research_question}}

Structure your research as follows:
1. **Key Concepts** - Define core terminology and concepts
2. **Current State** - What exists today, major players, approaches
3. **Best Practices** - What experts recommend
4. **Common Pitfalls** - What to avoid
5. **Emerging Trends** - What's changing or coming next
6. **Data Points** - Relevant statistics, benchmarks, case studies
</task>

<output_format>
Use headers for each section. Include sources where possible.
End with: "Research complete. Key themes: [list 3-5 themes]"
</output_format>
```

**Pass to Stage 2:** Full research output

---

## Stage 2: Synthesis

**Purpose:** Distill research into actionable insights.

```xml
<role>You are a strategic analyst who transforms research into insights.</role>

<context>
{{stage_1_output}}
</context>

<task>
Synthesize this research into actionable insights:

1. **Core Findings** (3-5 bullet points)
   - What are the most important discoveries?

2. **Implications for {{user_context}}**
   - How does this apply to my specific situation?

3. **Opportunities Identified**
   - What can I capitalize on?

4. **Risks to Mitigate**
   - What should I be careful about?

5. **Knowledge Gaps**
   - What do we still not know?
</task>

<output_format>
Be concise. Each bullet should be actionable, not just informational.
End with: "Synthesis complete. Top opportunity: [one sentence]"
</output_format>
```

**Pass to Stage 3:** Synthesis output

---

## Stage 3: Planning

**Purpose:** Create a strategic plan based on insights.

```xml
<role>You are a strategic planner who creates executable plans.</role>

<context>
Research synthesis:
{{stage_2_output}}

Constraints:
- Timeline: {{timeline}}
- Resources: {{resources}}
- Priority: {{priority_focus}}
</context>

<task>
Create a strategic plan with:

1. **Objective** - Clear, measurable goal

2. **Strategy** - High-level approach (2-3 sentences)

3. **Phases**
   - Phase 1: [Quick wins, 1-2 weeks]
   - Phase 2: [Foundation building, 2-4 weeks]
   - Phase 3: [Scale/optimize, ongoing]

4. **Success Metrics**
   - How will we know this worked?

5. **Dependencies & Risks**
   - What could block us?
</task>

<output_format>
Keep phases concrete. Each phase should have clear deliverables.
End with: "Plan complete. First action: [specific next step]"
</output_format>
```

**Pass to Stage 4:** Strategic plan

---

## Stage 4: Action Items

**Purpose:** Convert plan into specific, assignable tasks.

```xml
<role>You are a project manager who creates clear, executable task lists.</role>

<context>
Strategic plan:
{{stage_3_output}}
</context>

<task>
Break down into specific action items:

For each phase, create tasks with:
- **Task**: Specific action (start with verb)
- **Owner**: Who does this (or "Self" if solo)
- **Duration**: Estimated time
- **Dependencies**: What must happen first
- **Definition of Done**: How we know it's complete

Format as a checklist that can be imported into a task manager.
</task>

<output_format>
## Phase 1: [Name]
- [ ] Task 1 | Owner: X | Duration: Y | Depends on: Z
      Done when: [criteria]

## Phase 2: [Name]
...

End with: 
**Confidence:** [HIGH/MEDIUM/LOW]
**First task to start today:** [specific task]
</output_format>
```

---

## Usage Example

```bash
# Using the CLI
prompt chain research-to-action \
  --question "How should I implement AI-powered lead scoring?" \
  --domain "B2B SaaS sales" \
  --context "Small team, limited budget, using HubSpot" \
  --timeline "Q1 2024" \
  --resources "1 developer, marketing data available"
```

## Chain Configuration

```json
{
  "name": "research-to-action",
  "stages": 4,
  "variables": {
    "research_question": "required",
    "domain": "required",
    "user_context": "optional",
    "timeline": "optional, default: '3 months'",
    "resources": "optional, default: 'standard'",
    "priority_focus": "optional, default: 'balanced'"
  },
  "pass_full_context": true,
  "model_recommendations": {
    "stage_1": "claude-sonnet-4-20250514",
    "stage_2": "claude-sonnet-4-20250514",
    "stage_3": "claude-sonnet-4-20250514",
    "stage_4": "claude-haiku"
  }
}
```
