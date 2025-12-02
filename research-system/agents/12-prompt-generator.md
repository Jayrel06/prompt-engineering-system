# Agent: Prompt Generator

**Purpose**: Generate ready-to-use implementation prompts from research

---

## Agent Prompt

```xml
<agent type="synthesis" name="prompt-generator">

<objective>
Transform research findings and roadmap into specific, copy-paste-ready
prompts for Claude Code to implement each component.
</objective>

<input>
- roadmap-{date}.md
- code-patterns-{date}.md
- patterns-{date}.md
</input>

<prompt_format>
Each prompt should include:
1. Clear objective
2. Technical requirements
3. Design specifications
4. Acceptance criteria
5. Code references when available
</prompt_format>

<output_format>

## Implementation Prompts: {Date}

---

### Prompt 1: Hero Section

```markdown
## Task: Build CoreReceptionAI Hero Section

### Requirements
- Dark background (#0f172a)
- Aurora gradient effect (animated)
- Headline with staggered animation
- Subheadline
- Two CTAs: "Start Automating" (primary), "Watch Demo" (secondary)
- Responsive (mobile-first)

### Tech Stack
- Next.js 15 (App Router)
- Tailwind CSS v4
- Framer Motion for animations

### Design Specs
- Headline: text-5xl/6xl, font-bold, text-white
- Subheadline: text-xl, text-slate-400
- Primary CTA: bg-cyan-500, hover:bg-cyan-400
- Spacing: py-24 on desktop, py-16 on mobile

### Reference Code
[Aurora background from Magic UI]
[Text animation from Framer Motion docs]

### Acceptance Criteria
- [ ] Aurora animation smooth (60fps)
- [ ] Text animations staggered on load
- [ ] CTAs prominent and accessible
- [ ] Mobile layout stacks properly
- [ ] Lighthouse performance >90
```

---

### Prompt 2: Feature Bento Grid

```markdown
## Task: Build Feature Grid (Bento Layout)

### Requirements
- 4-6 feature cards in bento grid
- Glassmorphism card style
- Icons for each feature
- Hover effects
- Dark theme compatible

### Features to Display
1. AI Receptionist - 24/7 call handling
2. Smart Scheduling - Automated booking
3. Patient Follow-ups - Automated outreach
4. Integration - Works with existing systems

### Design Specs
- Card background: rgba(255,255,255,0.05)
- Border: 1px solid rgba(255,255,255,0.1)
- Backdrop blur: 10px
- Grid: 2 cols mobile, 3 cols desktop

### Acceptance Criteria
- [ ] Cards have consistent sizing
- [ ] Hover effect visible
- [ ] Icons aligned
- [ ] Responsive grid works
```

---

### Prompt 3: Social Proof Section

```markdown
## Task: Build Social Proof Section

### Requirements
- Logo bar (grayscale client logos)
- Headline: "Trusted by PT clinics"
- 2-3 testimonials with photos
- Optional: stat counters

### Design Specs
- Logos: grayscale, opacity-50, hover:opacity-100
- Testimonial cards: same glassmorphism as features
- Stats: Animated counters if included

### Do NOT Include
- Fabricated statistics ("500+ clinics")
- Geographic claims
- Unverified testimonials

### Acceptance Criteria
- [ ] Logos evenly spaced
- [ ] Testimonials readable
- [ ] No false claims
```

---

### Prompt 4: CTA Section

```markdown
## Task: Build Final CTA Section

### Requirements
- Strong headline
- Brief value recap
- Primary CTA prominent
- Background differentiation (slight gradient)

### Copy
- Headline: "Ready to automate your front desk?"
- CTA: "Start Automating Today"

### Design Specs
- Section: py-24, background with subtle gradient
- CTA button: Large, centered, with hover animation

### Acceptance Criteria
- [ ] CTA is the focal point
- [ ] Contrast meets WCAG
- [ ] Button has clear hover state
```

---

## Usage Instructions

1. Copy the relevant prompt
2. Paste into Claude Code
3. Adjust specifics as needed
4. Run and iterate

</output_format>

</agent>
```

---

## Execution

Run after Roadmap Builder completes
