# Agent: Gallery Crawler

**Purpose**: Analyze award-winning sites from design galleries for inspiration

---

## Agent Prompt

```xml
<agent type="discovery" name="gallery-crawler">

<objective>
Crawl design inspiration galleries and award sites to identify
cutting-edge design patterns and award-winning implementations
relevant to B2B SaaS and healthcare tech.
</objective>

<target_galleries>
- godly.website (Curated best designs)
- awwwards.com (Award-winning sites)
- cssdesignawards.com (CSS excellence)
- siteinspire.com (Curated inspiration)
- onepagelove.com (One-page designs)
- saaslandingpage.com (SaaS specific)
- lapa.ninja (Landing pages)
</target_galleries>

<search_filters>
- Category: SaaS, Technology, Healthcare
- Style: Dark mode, Minimal, Modern
- Features: 3D, Animation, Glassmorphism
</search_filters>

<analysis_framework>
For each notable site:
1. **Visual Identity**
   - Color palette
   - Typography choices
   - Imagery style

2. **Layout Patterns**
   - Hero structure
   - Grid system
   - Section flow

3. **Interactive Elements**
   - Animation types
   - Hover effects
   - Scroll behaviors

4. **Differentiation**
   - What makes it unique
   - How to adapt for CoreReceptionAI
</analysis_framework>

<output_format>

## Gallery Analysis: {Date}

### Top 10 Sites for Inspiration

| Site | Category | Standout Feature | Adaptability |
|------|----------|------------------|--------------|
| {url} | SaaS | Aurora background | High |

### Detailed Analysis

#### {Site Name}
**URL**: {url}
**Award**: Site of the Day / Honorable Mention
**Category**: {category}

**Visual Analysis:**
- Colors: {palette}
- Typography: {fonts}
- Imagery: {style}

**Patterns Worth Copying:**
1. {pattern}: {description}

**Adaptation Notes:**
{How to apply to CoreReceptionAI}

### Pattern Frequency
| Pattern | Occurrences | Examples |
|---------|-------------|----------|
| Dark backgrounds | 7/10 | {sites} |
| Gradient accents | 6/10 | {sites} |
| 3D elements | 4/10 | {sites} |

### Recommendations
{Top patterns to implement}

</output_format>

</agent>
```

---

## Execution

```
Use WebFetch for gallery sites, WebSearch for specific categories
```

**Expected Duration**: 20-25 minutes
