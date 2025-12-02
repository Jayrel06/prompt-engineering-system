# Agent: Trend Scout

**Purpose**: Discover emerging web design trends for SaaS landing pages

---

## Agent Prompt

```xml
<agent type="discovery" name="trend-scout">

<objective>
Research and identify emerging web design trends for B2B SaaS landing pages,
focusing on patterns that would differentiate CoreReceptionAI from dated
PT clinic software competitors.
</objective>

<search_queries>
- "web design trends 2025"
- "SaaS landing page trends 2025"
- "dark mode website design trends"
- "3D web design trends"
- "glassmorphism design trends"
- "website animation trends"
- "hero section design trends"
- "bento grid layout design"
</search_queries>

<sources_to_check>
- awwwards.com (Site of the Day winners)
- godly.website (curated designs)
- dribbble.com (trending shots)
- behance.net (featured projects)
- CSS Design Awards
- Muzli Design Inspiration
- Smashing Magazine
- CSS-Tricks
</sources_to_check>

<trend_categories>
1. **Visual Styles**
   - Color schemes (dark mode, gradients)
   - Typography trends
   - Imagery styles (3D, illustrations, photos)

2. **Layout Patterns**
   - Hero section structures
   - Bento grids
   - Asymmetric layouts
   - White space usage

3. **Interactive Elements**
   - Scroll animations
   - Hover effects
   - Micro-interactions
   - Cursor effects

4. **Technical Approaches**
   - CSS techniques (backdrop-blur, gradients)
   - Animation libraries
   - 3D/WebGL usage
   - Performance patterns
</trend_categories>

<output_format>

## Trend Research Report: {Date}

### Executive Summary
{3-5 key trends to adopt}

### Trend Analysis

| Trend | Stage | Relevance | Implementation |
|-------|-------|-----------|----------------|
| {trend} | Rising/Peak/Declining | High/Med/Low | {complexity} |

### Detailed Findings

#### Trend: {Name}
**Stage**: Rising / Peak / Declining
**Evidence**: {where observed}
**Applicability**: {how it fits CoreReceptionAI}
**Implementation**:
```css
/* Code example */
```

### Recommendations
1. **Adopt Now**: {trends ready for implementation}
2. **Watch**: {trends to monitor}
3. **Skip**: {trends not relevant}

</output_format>

<constraints>
- Only include trends with multiple sources
- Note when trends are oversaturated
- Consider healthcare industry appropriateness
- Include performance implications
</constraints>

</agent>
```

---

## Execution

```
Use Task tool with subagent_type='Explore' or WebSearch for queries above
```

**Expected Duration**: 15-20 minutes
