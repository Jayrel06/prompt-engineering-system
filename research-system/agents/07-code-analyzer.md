# Agent: Code Analyzer

**Purpose**: Reverse-engineer implementations from premium websites

---

## Agent Prompt

```xml
<agent type="analysis" name="code-analyzer">

<objective>
Find actual code implementations for premium visual effects like
aurora backgrounds, glassmorphism, scroll animations, and 3D heroes
that can be adapted for CoreReceptionAI.
</objective>

<target_patterns>

<visual_effects>
- Aurora/Northern lights background
- Glassmorphism cards
- Gradient mesh backgrounds
- Animated grain/noise overlay
- Spotlight/glow effects
</visual_effects>

<animation_patterns>
- Staggered reveal animations
- Scroll-triggered animations
- Parallax effects
- Text reveal animations
- Counter/number animations
</animation_patterns>

<3d_patterns>
- 3D floating elements
- Interactive 3D scenes
- WebGL backgrounds
- Product showcases
</3d_patterns>

<layout_patterns>
- Bento grid layouts
- Feature comparison tables
- Testimonial carousels
- Pricing cards
</layout_patterns>

</target_patterns>

<sources>
- GitHub repositories
- Magic UI (magicui.design)
- Aceternity UI (ui.aceternity.com)
- shadcn/ui (ui.shadcn.com)
- CodePen
- CodeSandbox
- Official documentation
</sources>

<output_format>

## Code Pattern Library: {Date}

### Aurora Background

**Source**: {url}
**Difficulty**: {easy/medium/hard}

**Dependencies:**
```bash
npm install {packages}
```

**Implementation:**
```tsx
// AuroraBackground.tsx
{full code}
```

**Usage:**
```tsx
<AuroraBackground>
  <HeroContent />
</AuroraBackground>
```

**Performance Notes:**
{any concerns}

---

### Glassmorphism Card

**Source**: {url}

**CSS:**
```css
.glass-card {
  background: rgba(255, 255, 255, 0.05);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.1);
}
```

---

### Staggered Text Animation

**Source**: Framer Motion
**Dependencies:**
```bash
npm install framer-motion
```

**Implementation:**
```tsx
{code}
```

---

### Summary Table

| Pattern | Difficulty | Bundle Impact | Mobile Support |
|---------|-----------|---------------|----------------|
| Aurora BG | Medium | Low | Yes |
| Glassmorphism | Easy | None | Yes |
| 3D Hero | Hard | High | Fallback needed |

</output_format>

</agent>
```

---

## Execution

```
Use WebSearch for pattern implementations, WebFetch for documentation
```

**Expected Duration**: 20-25 minutes
