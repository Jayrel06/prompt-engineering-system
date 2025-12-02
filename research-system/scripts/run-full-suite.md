# Run Full Research Suite

**Execute all research agents in optimal order**

---

## Quick Start Prompt

Copy and paste this into Claude Code:

```markdown
## Research Mission: Full Website Design Suite

Execute the following research agents, storing outputs in
./research-system/outputs/{today's date}/

### Phase 1: Discovery (Run in Parallel)

**Agent 1: Trend Scout**
Research emerging web design trends for SaaS landing pages.
Search: "web design trends 2025", "SaaS landing page trends", "dark mode design"
Focus: Dark mode, 3D, glassmorphism, animation patterns
Output: trends-{date}.md

**Agent 2: Tech Stack Hunter**
Research what professionals use to build premium websites.
Analyze: linear.app, vercel.com, stripe.com tech stacks
Search: Reddit/HN discussions on best stacks
Output: tech-stacks-{date}.md

**Agent 3: Community Researcher**
Mine Reddit, HN, Twitter for design insights.
Find: What gets praised, what gets criticized
Output: community-{date}.md

**Agent 4: Gallery Crawler**
Analyze award-winning sites from godly.website, awwwards.com
Document: Visual patterns, animations, layouts
Output: gallery-{date}.md

**Agent 5: GitHub Explorer**
Find landing page templates and component libraries
Search: shadcn components, framer motion examples, aurora backgrounds
Output: github-{date}.md

### Phase 2: Analysis (Run in Parallel)

**Agent 6: Competitor Auditor**
Audit PT clinic competitors: webpt.com, cliniko.com, simplepractice.com,
jane.app, gethealthie.com
And benchmarks: linear.app, vercel.com, stripe.com
Document: Visual gaps, opportunities
Output: competitors-{date}.md

**Agent 7: Code Analyzer**
Find implementation code for: Aurora backgrounds, glassmorphism cards,
staggered animations, 3D heroes, scroll reveals
Search: GitHub repos, Magic UI, Aceternity UI
Output: code-patterns-{date}.md

**Agent 8: UX Auditor**
Analyze user flows and interaction patterns
Document: Navigation, forms, CTAs
Output: ux-patterns-{date}.md

**Agent 9: Conversion Researcher**
Research CTA, social proof, form optimization
Find: Evidence-based best practices
Output: conversion-{date}.md

### Phase 3: Synthesis (Run Sequentially)

**Agent 10: Pattern Extractor**
Read all Phase 1 and Phase 2 outputs.
Extract: Validated patterns (3+ sources), priority matrix
Output: patterns-{date}.md

**Agent 11: Roadmap Builder**
Create implementation roadmap from patterns
Output: roadmap-{date}.md

**Agent 12: Prompt Generator**
Generate ready-to-use implementation prompts
Output: prompts-{date}.md

### Constraints
- No fabricated statistics
- No geographic claims
- Include confidence levels
- Credit sources
```

---

## Manual Execution

### Step 1: Create Output Directory
```bash
mkdir -p ./research-system/outputs/$(date +%Y-%m-%d)/{raw,synthesized,actionable}
```

### Step 2: Run Discovery Agents
Use Task tool with agent prompts from ./agents/01-05

### Step 3: Run Analysis Agents
Use Task tool with agent prompts from ./agents/06-09

### Step 4: Run Synthesis Agents
Use Task tool with agent prompts from ./agents/10-12 (in order)

---

## Expected Outputs

```
research-system/outputs/{date}/
├── raw/
│   ├── trends-{date}.md
│   ├── tech-stacks-{date}.md
│   ├── community-{date}.md
│   ├── gallery-{date}.md
│   ├── github-{date}.md
│   ├── competitors-{date}.md
│   ├── code-patterns-{date}.md
│   ├── ux-patterns-{date}.md
│   └── conversion-{date}.md
├── synthesized/
│   └── patterns-{date}.md
└── actionable/
    ├── roadmap-{date}.md
    └── prompts-{date}.md
```
