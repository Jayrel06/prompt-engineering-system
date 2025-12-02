# Agent: Tech Stack Hunter

**Purpose**: Research professional tech stacks for premium website development

---

## Agent Prompt

```xml
<agent type="discovery" name="tech-stack-hunter">

<objective>
Research what technologies professional developers use to build
premium SaaS websites like Linear, Vercel, and Stripe.
</objective>

<target_stacks>
<site name="linear.app">
Research: Framework, styling, animations, 3D elements
</site>
<site name="vercel.com">
Research: Framework (likely Next.js), styling approach, animation library
</site>
<site name="stripe.com">
Research: Animations, scroll effects, interactive elements
</site>
</target_stacks>

<search_queries>
- "linear.app tech stack"
- "how was vercel.com built"
- "stripe website animation library"
- "best tech stack for SaaS landing page 2025"
- "next.js vs remix for marketing site"
- "framer motion vs gsap react"
- "shadcn ui vs radix ui"
- "tailwind css v4 features"
- "react three fiber examples landing page"
</search_queries>

<community_sources>
- Reddit: r/webdev, r/reactjs, r/nextjs
- Hacker News discussions
- Dev.to articles
- GitHub discussions
</community_sources>

<evaluation_criteria>
1. **Developer Experience**
   - Learning curve
   - Documentation quality
   - Community support

2. **Performance**
   - Bundle size
   - Runtime performance
   - Core Web Vitals impact

3. **Ecosystem**
   - Component libraries available
   - Integration ease
   - Long-term maintenance

4. **Production Readiness**
   - Used by major companies
   - Stability
   - Update frequency
</evaluation_criteria>

<output_format>

## Tech Stack Research: {Date}

### Recommended Stack for CoreReceptionAI

| Layer | Technology | Why |
|-------|-----------|-----|
| Framework | Next.js 15 | {rationale} |
| Styling | Tailwind CSS v4 | {rationale} |
| Components | shadcn/ui | {rationale} |
| Animations | Framer Motion | {rationale} |
| 3D | React Three Fiber | {rationale} |

### Detailed Analysis

#### {Technology}
**Category**: Framework / Styling / Animation / 3D
**Used By**: {companies}
**Pros**: {benefits}
**Cons**: {drawbacks}
**Verdict**: Adopt / Consider / Skip

### What Premium Sites Use

| Site | Framework | Styling | Animations | 3D |
|------|-----------|---------|------------|-----|
| linear.app | | | | |
| vercel.com | | | | |
| stripe.com | | | | |

### Community Consensus
{What Reddit/HN says about each technology}

</output_format>

</agent>
```

---

## Execution

```
Use WebSearch for queries, WebFetch for specific articles
```

**Expected Duration**: 15-20 minutes
