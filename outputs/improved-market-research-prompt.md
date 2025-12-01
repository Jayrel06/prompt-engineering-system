# Improved Market & Design Research Prompt

## Analysis of Original Prompt Issues

Based on the prompt engineering system frameworks, the original prompt had these issues:

| Issue | Framework Reference | Impact |
|-------|---------------------|--------|
| Over-long (~4000+ words) | `what-doesnt.md`: "After ~2000 words, effectiveness drops" | Model loses focus on key instructions |
| No XML structure | `structured-prompting.md`: "XML tags help Claude parse" | Unclear section boundaries |
| Redundant instructions | `few-shot.md`: Quality > quantity | Wasted tokens, diluted focus |
| Missing success criteria | `claude-code-handoff.md`: Testable checkboxes | No way to verify completion |
| No non-goals | `claude-code-handoff.md`: Prevents scope creep | Risk of unnecessary work |
| Too many phases (6) | `chain-of-thought.md`: Break into chains | Cognitive overload |

---

## Improved Prompt (Using CARE + XML Structure)

```xml
<context>
<role>
You are a senior market research analyst with expertise in B2B SaaS positioning,
competitive intelligence, and design systems. You have 10+ years experience in
healthcare technology markets.
</role>

<project>
Client: CoreReceptionAI - Premium AI workflow automation consultancy
Target Market: Physical therapy clinics seeking operational efficiency
Goal: Create an evidence-based design system and market positioning strategy
</project>

<constraints>
- Output all files to /workspace/research/
- Every recommendation must cite source evidence
- Design decisions must be implementable in Tailwind CSS + React
- Time budget: Focus on highest-impact research first
</constraints>
</context>

<action>
Execute a systematic research operation across four domains. Complete each phase
before proceeding to the next.

<phase id="1" name="Competitive Intelligence">
<objective>Map the competitive landscape and identify positioning opportunities</objective>

<tasks>
1. Search for direct competitors:
   - "AI automation physical therapy clinic"
   - "AI receptionist physical therapy practice"
   - "workflow automation PT EMR integration"

2. For each competitor (minimum 5), extract:
</tasks>

<output_format>
```json
{
  "company_name": "",
  "url": "",
  "hero_message": "",
  "pricing_model": "",
  "design_quality": "premium|standard|basic",
  "key_differentiators": [],
  "weaknesses": [],
  "cta_strategy": ""
}
```
</output_format>

<deliverable>/workspace/research/competitors.json</deliverable>
</phase>

<phase id="2" name="Premium SaaS Benchmarks">
<objective>Extract visual and messaging patterns from successful B2B SaaS</objective>

<benchmark_companies>
Rippling, WorkOS, Vanta, Linear, Superhuman, Clay
</benchmark_companies>

<tasks>
For each company, document:
1. Hero section structure and copy
2. Color palette (hex values)
3. Typography choices
4. Animation patterns
5. Social proof strategy
</tasks>

<output_format>
```markdown
## [Company Name]
**Hero Message**: [Exact copy]
**Color System**: Primary: #XXX, Accent: #XXX, Background: #XXX
**Typography**: [Font family, weights]
**What Works**: [2-3 specific patterns to adapt]
```
</output_format>

<deliverable>/workspace/research/benchmarks.md</deliverable>
</phase>

<phase id="3" name="Design Pattern Mining">
<objective>Find production-ready code patterns from successful implementations</objective>

<github_searches>
- `"landing page" "saas" "tailwind" stars:>500`
- `"glassmorphism" "tailwind" "framer-motion"`
- `"design system" "react" stars:>1000`
</github_searches>

<extract_for_each_repo>
1. Tailwind config (color system, spacing, typography)
2. Animation implementations (framer-motion patterns)
3. Component structure (hero, pricing cards, CTAs)
</extract_for_each_repo>

<output_format>
```typescript
// Pattern: [Name]
// Source: [repo URL]
// Use case: [Where to apply]

const pattern = {
  // Actual code snippet
}
```
</output_format>

<deliverable>/workspace/research/code-patterns.md</deliverable>
</phase>

<phase id="4" name="Customer Pain Points">
<objective>Understand real PT clinic problems in their own language</objective>

<reddit_searches>
Subreddits: r/physicaltherapy, r/healthcare
Queries: "practice management software", "no-show patients", "administrative burden"
</reddit_searches>

<extract>
- Exact quotes describing pain points
- Frustrations with current solutions
- Language they use to describe problems
</extract>

<deliverable>/workspace/research/pain-points.md</deliverable>
</phase>
</action>

<result>
<primary_deliverable>
/workspace/research/DESIGN_SYSTEM.md - Complete design specification containing:

```markdown
# CoreReceptionAI Design System

## Evidence Summary
- [X] competitors analyzed
- [X] benchmark companies studied
- [X] GitHub repos reviewed
- [X] pain points documented

## Color System
```typescript
const colors = {
  background: { value: "#XXX", rationale: "[Evidence]" },
  primary: { value: "#XXX", rationale: "[Evidence]" },
  accent: { value: "#XXX", rationale: "[Evidence]" },
}
```

## Typography
- Heading: [Font] - Used by [X] of benchmarks
- Body: [Font] - Rationale: [Evidence]
- Scale: [Values with reasoning]

## Component Specifications

### Hero Section
- Layout: [Evidence-based structure]
- Animation: [Specific pattern from GitHub]
- Copy framework: [Based on pain point research]

### Glassmorphism Cards
```typescript
// From: [source repo]
const glassCard = { /* exact values */ }
```

### Pricing Cards
[Specification with evidence]

## Competitive Positioning
Based on competitor analysis:
- Gap: [What competitors miss]
- Our angle: [How we differentiate]
- Messaging: [Pain point language to use]

## Implementation Priority
1. [Highest impact item] - Why: [Evidence]
2. [Second priority] - Why: [Evidence]
3. [Third priority] - Why: [Evidence]
```
</primary_deliverable>

<supporting_files>
- /workspace/research/competitors.json
- /workspace/research/benchmarks.md
- /workspace/research/code-patterns.md
- /workspace/research/pain-points.md
</supporting_files>
</result>

<evaluate>
<success_criteria>
- [ ] Minimum 5 competitors analyzed with complete data extraction
- [ ] All 6 benchmark companies documented
- [ ] At least 5 GitHub repos with extractable code patterns
- [ ] Minimum 10 pain point quotes from real PT professionals
- [ ] Every design decision in final spec cites evidence source
- [ ] Color palette includes contrast ratios for accessibility
- [ ] Typography scale is implementable in Tailwind
- [ ] At least 3 ready-to-use code snippets included
</success_criteria>

<quality_checks>
- No design decision without evidence citation
- All hex values verified as valid
- Code snippets are syntactically correct
- Pain points use actual user language, not paraphrased
</quality_checks>

<anti_patterns>
Avoid these common mistakes:
- Generic "best practices" without specific sources
- Design opinions without competitive evidence
- Recommending tools/libraries without seeing production use
- Pain points that sound like marketing copy
</anti_patterns>
</evaluate>

<non_goals>
Explicitly do NOT:
- Build any actual components (research only)
- Create visual mockups or wireframes
- Analyze more than 10 competitors (diminishing returns)
- Deep dive into technical SEO
- Research pricing strategy (separate task)
- Evaluate hosting/infrastructure options
</non_goals>

<execution_notes>
<priority_order>
If time is limited, prioritize in this order:
1. Competitor analysis (foundation for positioning)
2. Pain points (drives messaging)
3. Benchmark design patterns (visual direction)
4. GitHub code patterns (implementation details)
</priority_order>

<output_format_preference>
- JSON for structured data (competitors)
- Markdown for analysis (benchmarks, patterns)
- TypeScript for code snippets (implementation-ready)
</output_format_preference>
</execution_notes>
```

---

## Key Improvements Made

### 1. Applied CARE Framework
- **C**ontext: Role, project, constraints clearly defined upfront
- **A**ction: Phased tasks with specific instructions
- **R**esult: Explicit deliverables with format specifications
- **E**valuate: Testable success criteria with checkboxes

### 2. XML Structure for Clarity
Per `structured-prompting.md`, XML tags help Claude:
- Distinguish sections clearly
- Follow hierarchical instructions
- Parse complex requirements without confusion

### 3. Reduced Length (~60% shorter)
Original: ~4000+ words
Improved: ~1500 words
Per `what-doesnt.md`: "After ~2000 words, prompt effectiveness drops"

### 4. Added Non-Goals
Per `claude-code-handoff.md`: Prevents scope creep and clarifies boundaries

### 5. Testable Success Criteria
Per `claude-code-handoff.md`:
- Specific, measurable outcomes
- Checkbox format for verification
- Minimum thresholds defined

### 6. Evidence-Based Requirements
Every design decision must cite source, preventing:
- Opinion-based recommendations
- Unverifiable claims
- Generic "best practices"

### 7. Priority Order
Per `what-works.md` "Ship small, iterate":
- Phased approach with clear priorities
- Graceful degradation if time-limited

### 8. Anti-Patterns Section
Per `what-doesnt.md`: Explicitly call out what to avoid

---

## Alternative: Chained Prompts Approach

For even better results, break into 4 separate prompts:

### Prompt Chain 1: Competitive Intelligence
```xml
<role>Competitive intelligence analyst</role>
<task>Analyze 5-7 direct competitors in PT clinic automation</task>
<output>/workspace/research/competitors.json</output>
<format>[JSON schema]</format>
```

### Prompt Chain 2: Design Benchmarking
```xml
<role>Design systems researcher</role>
<input>Read /workspace/research/competitors.json first</input>
<task>Analyze 6 premium B2B SaaS sites for design patterns</task>
<output>/workspace/research/benchmarks.md</output>
```

### Prompt Chain 3: Code Pattern Mining
```xml
<role>Frontend architecture researcher</role>
<input>Read benchmarks.md for context</input>
<task>Find production code patterns from GitHub</task>
<output>/workspace/research/code-patterns.md</output>
```

### Prompt Chain 4: Synthesis
```xml
<role>Design system architect</role>
<input>Read all files in /workspace/research/</input>
<task>Synthesize into complete design system specification</task>
<output>/workspace/research/DESIGN_SYSTEM.md</output>
<requirement>Every decision must cite evidence from inputs</requirement>
```

**Why chaining works better:**
- Each prompt stays under 500 words (optimal)
- Model focuses on one task at a time
- Outputs build on each other
- Easier to debug/iterate individual phases

---

## Quick Reference: Prompt Engineering Principles Applied

| Principle | How Applied |
|-----------|-------------|
| Role definition first | `<role>` tag at start |
| Task-first ordering | Main action before supporting details |
| Clear delimiters | XML tags throughout |
| Output format specification | JSON/Markdown templates provided |
| Testable success criteria | Checkbox list with minimums |
| Non-goals | Explicit exclusions |
| Evidence requirement | "Must cite source" throughout |
| Priority ordering | Numbered phases with fallback guidance |
| Anti-patterns | Explicit "avoid" section |
| Reasonable length | ~1500 words vs ~4000 original |
