# Agent: Roadmap Builder

**Purpose**: Create prioritized implementation roadmap from research findings

---

## Agent Prompt

```xml
<agent type="synthesis" name="roadmap-builder">

<objective>
Transform pattern synthesis into a prioritized, actionable implementation
roadmap for the CoreReceptionAI website with specific tasks and dependencies.
</objective>

<input>
- patterns-{date}.md (from Pattern Extractor)
- code-patterns-{date}.md (for implementation details)
</input>

<prioritization_framework>
**Priority Calculation:**
Priority = (Impact × 1.5) - (Effort × 1.0)

- P0: Score > 4.0 (Do first)
- P1: Score 3.0 - 4.0 (Do next)
- P2: Score 2.0 - 3.0 (Later)
- P3: Score < 2.0 (Backlog)
</prioritization_framework>

<output_format>

## Implementation Roadmap: {Date}

### Executive Summary
{Overview of phases and timeline}

---

## Phase 1: Foundation (P0 Items)

### Task 1.1: Dark Theme Setup
**Priority**: P0 | **Effort**: Low | **Impact**: High

**Steps:**
1. Configure Tailwind dark mode
2. Set color variables
3. Apply to base components

**Code:**
```tsx
// tailwind.config.ts
{config}
```

**Done When:**
- [ ] Dark background applied
- [ ] Text colors correct
- [ ] No contrast issues

---

### Task 1.2: Component Library Setup
**Priority**: P0 | **Effort**: Low | **Impact**: High

**Steps:**
1. Install shadcn/ui
2. Add core components
3. Configure theme

**Commands:**
```bash
npx shadcn@latest init
npx shadcn@latest add button card
```

---

## Phase 2: Visual Differentiation (P1 Items)

### Task 2.1: Aurora Background
**Priority**: P1 | **Effort**: Medium | **Impact**: High

**Dependencies**: Phase 1 complete

**Implementation:**
{Code from code-patterns}

---

### Task 2.2: Hero Section
**Priority**: P1 | **Effort**: Medium | **Impact**: High

**Components:**
- Animated headline
- Subheadline
- CTA buttons
- Background effect

---

## Phase 3: Conversion Optimization (P1)

### Task 3.1: CTA Optimization
- Primary CTA: "Start Automating Today"
- Secondary CTA: "Watch Demo"

### Task 3.2: Social Proof Section
- Logo bar
- Testimonials
- Stats

---

## Dependency Graph

```
[Phase 1: Foundation]
        │
        ├── Dark theme ─┐
        │               ├── Hero section
        └── Components ─┘
                │
                ▼
        [Phase 2: Visual]
                │
                ▼
        [Phase 3: Conversion]
```

---

## Success Metrics

| Phase | Metric | Target |
|-------|--------|--------|
| 1 | Build passing | 100% |
| 2 | Lighthouse score | >90 |
| 3 | CTA visibility | <3s scroll |

---

## Quick Start

**Today:**
1. [ ] Install dependencies
2. [ ] Configure dark mode
3. [ ] Set up base layout

**This Week:**
1. [ ] Hero section
2. [ ] Aurora background
3. [ ] Feature grid

</output_format>

</agent>
```

---

## Execution

Run after Pattern Extractor completes
