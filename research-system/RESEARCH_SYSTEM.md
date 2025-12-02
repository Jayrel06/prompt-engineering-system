# CoreReceptionAI Website Design Research System

**Multi-agent research framework for website design intelligence**

This system uses Claude Code agents to conduct comprehensive research on web design trends, tech stacks, competitor analysis, and implementation patterns for the CoreReceptionAI landing page.

---

## System Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                        RESEARCH ORCHESTRATOR                         │
│                    (Coordinates all research agents)                 │
└─────────────────────────────────────────────────────────────────────┘
                                    │
        ┌───────────────────────────┼───────────────────────────┐
        │                           │                           │
        ▼                           ▼                           ▼
┌───────────────┐         ┌───────────────┐         ┌───────────────┐
│   DISCOVERY   │         │   ANALYSIS    │         │  SYNTHESIS    │
│    AGENTS     │         │    AGENTS     │         │    AGENTS     │
├───────────────┤         ├───────────────┤         ├───────────────┤
│ • Trend Scout │         │ • Competitor  │         │ • Pattern     │
│ • Tech Stack  │         │   Auditor     │         │   Extractor   │
│ • Community   │         │ • Code        │         │ • Roadmap     │
│   Research    │         │   Analyzer    │         │   Builder     │
│ • Gallery     │         │ • UX Auditor  │         │ • Prompt      │
│   Crawler     │         │ • Conversion  │         │   Generator   │
│ • GitHub      │         │   Researcher  │         │               │
│   Explorer    │         │               │         │               │
└───────────────┘         └───────────────┘         └───────────────┘
```

---

## Quick Start

### Run Full Research Suite
```bash
/research-design-full
```

### Run Individual Agents
```bash
/research-design-trends      # Web design trends
/research-design-tech        # Tech stack analysis
/research-design-competitors # Competitor audit
/research-design-code        # Code pattern hunt
```

---

## Agent Catalog

### Phase 1: Discovery Agents

| Agent | Purpose | Output |
|-------|---------|--------|
| **Trend Scout** | Find emerging web design trends | trends-{date}.md |
| **Tech Stack Hunter** | Research professional tech stacks | tech-stacks-{date}.md |
| **Community Researcher** | Mine Reddit/HN for design insights | community-{date}.md |
| **Gallery Crawler** | Analyze award-winning sites | gallery-{date}.md |
| **GitHub Explorer** | Find UI components/templates | github-{date}.md |

### Phase 2: Analysis Agents

| Agent | Purpose | Output |
|-------|---------|--------|
| **Competitor Auditor** | Deep-dive PT clinic competitors | competitors-{date}.md |
| **Code Analyzer** | Reverse-engineer implementations | code-patterns-{date}.md |
| **UX Auditor** | Analyze user flows/patterns | ux-patterns-{date}.md |
| **Conversion Researcher** | Research CRO best practices | conversion-{date}.md |

### Phase 3: Synthesis Agents

| Agent | Purpose | Output |
|-------|---------|--------|
| **Pattern Extractor** | Consolidate findings into patterns | patterns-{date}.md |
| **Roadmap Builder** | Create prioritized action plans | roadmap-{date}.md |
| **Prompt Generator** | Create implementation prompts | prompts-{date}.md |

---

## Research Domains

### Domain 1: Visual Design Intelligence
- Current design trends (2024-2025)
- Dark mode implementations
- Glassmorphism, Aurora backgrounds
- 3D/WebGL hero sections
- Animation patterns (Framer Motion)
- Bento grid layouts
- Color psychology for healthcare

### Domain 2: Technical Implementation
- Next.js 15 + React 19 patterns
- Tailwind CSS v4 features
- shadcn/ui component patterns
- Framer Motion animations
- React Three Fiber for 3D
- Performance optimization
- SEO implementation

### Domain 3: Competitor Analysis
**PT Clinic Software:**
- webpt.com
- cliniko.com
- simplepractice.com
- jane.app
- gethealthie.com
- intakeq.com

**Premium Benchmarks:**
- linear.app
- vercel.com
- stripe.com
- notion.so
- figma.com

### Domain 4: Conversion Optimization
- CTA placement and copy
- Social proof patterns
- Trust signals for healthcare
- Form optimization
- Pricing page layouts

---

## File Structure

```
research-system/
├── RESEARCH_SYSTEM.md          # This file
├── agents/
│   ├── 01-trend-scout.md
│   ├── 02-tech-stack-hunter.md
│   ├── 03-community-researcher.md
│   ├── 04-gallery-crawler.md
│   ├── 05-github-explorer.md
│   ├── 06-competitor-auditor.md
│   ├── 07-code-analyzer.md
│   ├── 08-ux-auditor.md
│   ├── 09-conversion-researcher.md
│   ├── 10-pattern-extractor.md
│   ├── 11-roadmap-builder.md
│   └── 12-prompt-generator.md
├── prompts/
│   ├── research-templates.md
│   ├── analysis-frameworks.md
│   └── synthesis-patterns.md
├── scripts/
│   ├── run-full-suite.md
│   ├── run-targeted.md
│   └── schedule.md
└── outputs/
    ├── templates/
    └── {date}/
        ├── raw/
        ├── synthesized/
        └── actionable/
```

---

## Target Design: CoreReceptionAI

### Visual Direction
- **Theme**: Dark mode (#0f172a slate-900)
- **Accent**: Cyan (#06b6d4)
- **Style**: Premium SaaS like Linear/Vercel
- **Elements**: Aurora backgrounds, 3D hero, glassmorphism cards

### Tech Stack
- Next.js 15 (App Router)
- React 19
- TypeScript
- Tailwind CSS v4
- shadcn/ui + Magic UI
- Framer Motion
- React Three Fiber

### Differentiation Goal
Stand out from clinical/dated PT software competitors with modern, premium design that conveys trust and innovation.
