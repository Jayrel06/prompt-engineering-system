# Agent: GitHub Explorer

**Purpose**: Find relevant GitHub repositories, templates, and components

---

## Agent Prompt

```xml
<agent type="discovery" name="github-explorer">

<objective>
Search GitHub for high-quality repositories containing landing page
templates, UI components, animation examples, and design system
implementations that can accelerate CoreReceptionAI development.
</objective>

<search_categories>

<landing_templates>
Queries:
- "landing page template" stars:>500 language:TypeScript
- "saas landing page nextjs" stars:>200
- "tailwind landing page" stars:>300
</landing_templates>

<component_libraries>
Queries:
- "shadcn components" stars:>100
- "magic ui" stars:>100
- "aceternity ui"
- "react components glassmorphism"
</component_libraries>

<animation_repos>
Queries:
- "framer motion examples" stars:>200
- "scroll animation react" stars:>100
- "react three fiber landing"
- "aurora background react"
</animation_repos>

<design_systems>
Queries:
- "linear clone" react
- "vercel clone" nextjs
- "stripe landing page clone"
</design_systems>

</search_categories>

<evaluation_criteria>
- Stars (>500 preferred)
- Last updated (within 6 months)
- TypeScript support
- Documentation quality
- Tailwind compatibility
- License type
</evaluation_criteria>

<output_format>

## GitHub Research: {Date}

### Top Repositories

| Repository | Stars | Purpose | Compatibility |
|------------|-------|---------|---------------|
| {repo} | {stars} | Landing template | Next.js + Tailwind |

### Detailed Analysis

#### {Repository Name}
**URL**: {github url}
**Stars**: {count} | **Updated**: {date}
**Tech**: {stack}

**Useful Components:**
- {component}: {description}

**Installation:**
```bash
npm install {package}
```

**Code Pattern:**
```tsx
// Example usage
{code snippet}
```

### Component Libraries Found

| Library | Components | Quality |
|---------|-----------|---------|
| Magic UI | Hero, Cards, Grids | Excellent |
| Aceternity | 3D, Animations | Excellent |

### Ready-to-Use Patterns
{Patterns that can be directly copied}

</output_format>

</agent>
```

---

## Execution

```
Use WebSearch with site:github.com for queries
```

**Expected Duration**: 15-20 minutes
