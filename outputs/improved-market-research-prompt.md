# Visual-First Design Research Prompt

## The Core Problem
**Your websites are visually empty** - all text, no imagery, illustrations, or visual elements that create emotional impact and credibility.

This prompt focuses specifically on finding and implementing **visual assets** that transform plain text pages into premium, conversion-focused experiences.

---

## The Improved Prompt

```xml
<context>
<role>
You are a visual design researcher specializing in high-converting B2B SaaS websites.
Your expertise is finding and cataloging visual assets, imagery patterns, and design
inspiration that transforms text-heavy pages into visually compelling experiences.
</role>

<core_problem>
The client's websites are visually impoverished:
- Hero sections with only headlines and buttons (no visuals)
- Service sections that are text blocks without supporting imagery
- No illustrations, 3D elements, abstract graphics, or photography
- Result: Sites look cheap, untrustworthy, and fail to convert

Goal: Find specific visual solutions with implementation sources.
</core_problem>

<project>
Client: CoreReceptionAI - AI workflow automation for physical therapy clinics
Need: Premium visual identity that signals trust, innovation, and professionalism
Budget tier: Mid-to-high (willing to pay for quality assets)
</project>
</context>

<action>

<phase id="1" name="Visual Inspiration Sources">
<objective>Catalog the BEST places to find design inspiration with visual-heavy examples</objective>

<sources_to_document>

<category name="Curated Design Galleries">
| Source | URL | Best For | How to Search |
|--------|-----|----------|---------------|
| Dribbble | dribbble.com | UI/hero concepts, illustrations | "SaaS landing page", "hero section", "B2B website" |
| Behance | behance.net | Full case studies with process | "SaaS website design", "landing page concept" |
| Awwwards | awwwards.com | Award-winning live sites | Filter: "Corporate", "Technology" |
| Mobbin | mobbin.com | Mobile + web patterns | Browse "Marketing" category |
| Land-book | land-book.com | Landing page specific | Filter by industry |
| Lapa Ninja | lapa.ninja | Landing pages only | Browse categories |
| SaaS Landing Page | saaslandingpage.com | SaaS-specific examples | Browse all |
| Godly | godly.website | Cutting-edge designs | Browse featured |
| Dark Mode Design | darkmodedesign.com | Dark theme inspiration | Browse all |
| One Page Love | onepagelove.com | Single page sites | Filter by industry |
</category>

<category name="Component-Specific Inspiration">
| Source | URL | Best For |
|--------|-----|----------|
| Hero Patterns | heropatterns.com | SVG background patterns |
| UI Patterns | ui-patterns.com | Specific UI solutions |
| Page Collective | pagecollective.com | Full page screenshots |
| Refero Design | refero.design | Searchable design database |
| Screenlane | screenlane.com | Specific UI patterns |
</category>

</sources_to_document>

<task>
For each source, find 3-5 examples relevant to CoreReceptionAI and document:
- Screenshot/URL of example
- What visual element makes it work
- How to replicate or source similar assets
</task>

<deliverable>/workspace/research/visual-inspiration-sources.md</deliverable>
</phase>

<phase id="2" name="Hero Visual Patterns">
<objective>Document the 7 most effective hero visual types for B2B SaaS</objective>

<hero_visual_types>

<type id="1" name="3D Abstract Objects">
<description>Floating geometric shapes, abstract 3D renders</description>
<examples>Linear.app, Stripe.com, Vercel.com</examples>
<where_to_get>
- Spline (spline.design) - Free 3D design tool
- Three.js + React Three Fiber - Code your own
- Sketchfab - 3D model marketplace
- Blender + free models from Poly Haven
</where_to_get>
<implementation>React Three Fiber component or Spline embed</implementation>
</type>

<type id="2" name="Product Screenshots/Mockups">
<description>Dashboard previews, app interfaces in device frames</description>
<examples>Notion.so, Figma.com, Slack.com</examples>
<where_to_get>
- Mockup World (mockupworld.co) - Free mockups
- Angle (angle.sh) - Premium device mockups
- Screely (screely.com) - Browser mockups
- Cleanmock (cleanmock.com) - Simple mockups
</where_to_get>
<implementation>PNG/SVG with CSS animations on scroll</implementation>
</type>

<type id="3" name="Custom Illustrations">
<description>Brand-specific illustrated scenes, isometric graphics</description>
<examples>Mailchimp.com, Dropbox.com, Intercom.com</examples>
<where_to_get>
- unDraw (undraw.co) - Free customizable SVGs
- Storyset (storyset.com) - Animated illustrations
- Blush (blush.design) - Mix-and-match illustrations
- Humaaans (humaaans.com) - People illustrations
- DrawKit (drawkit.com) - Free illustration packs
- Icons8 Illustrations (icons8.com/illustrations)
- IRA Design (iradesign.io) - Gradient illustrations
</where_to_get>
<implementation>SVG with CSS/Framer Motion animations</implementation>
</type>

<type id="4" name="Abstract Gradient Backgrounds">
<description>Mesh gradients, aurora effects, animated color flows</description>
<examples>Stripe.com, Apple.com, Arc Browser</examples>
<where_to_get>
- Mesh Gradient (meshgradient.in) - Generate mesh gradients
- Haikei (haikei.app) - SVG background generator
- Coolors Gradient (coolors.co/gradient-maker)
- CSS Gradient (cssgradient.io)
- Gradienta (gradienta.io) - Free gradient backgrounds
</where_to_get>
<implementation>CSS gradients with animation keyframes</implementation>
</type>

<type id="5" name="Lifestyle/Contextual Photography">
<description>Real photos showing product in use, target audience</description>
<examples>Zoom.us, Calendly.com, HubSpot.com</examples>
<where_to_get>
- Unsplash (unsplash.com) - Free high-quality photos
- Pexels (pexels.com) - Free stock photos
- Burst (burst.shopify.com) - Free business photos
- Nappy (nappy.co) - Diverse stock photos
- PREMIUM: Shutterstock, Getty, Adobe Stock
</where_to_get>
<implementation>Optimized WebP with lazy loading</implementation>
</type>

<type id="6" name="Animated Data Visualizations">
<description>Live charts, metrics, flowing data representations</description>
<examples>Plausible.io, Fathom Analytics, Segment.com</examples>
<where_to_get>
- Chart.js - Animated charts
- Recharts - React chart library
- Framer Motion - Custom animations
- Lottie (lottiefiles.com) - After Effects animations
</where_to_get>
<implementation>React component with live/mock data</implementation>
</type>

<type id="7" name="Video Backgrounds/Loops">
<description>Subtle looping video, product demos, ambient motion</description>
<examples>Apple.com, Tesla.com, Webflow.com</examples>
<where_to_get>
- Coverr (coverr.co) - Free stock video
- Pexels Video (pexels.com/videos)
- Mixkit (mixkit.co) - Free video clips
- PREMIUM: Artgrid, Storyblocks
</where_to_get>
<implementation>HTML5 video with autoplay, muted, loop</implementation>
</type>

</hero_visual_types>

<task>
1. Visit each example site listed
2. Screenshot the hero section
3. Identify which visual type they use
4. Document the exact implementation approach
5. Recommend which type fits CoreReceptionAI best (with reasoning)
</task>

<deliverable>/workspace/research/hero-visual-patterns.md</deliverable>
</phase>

<phase id="3" name="Visual Asset Marketplace Research">
<objective>Create a sourcing guide for every type of visual asset needed</objective>

<asset_categories>

<category name="Illustrations & Graphics">
| Resource | URL | Price | Quality | Best For |
|----------|-----|-------|---------|----------|
| unDraw | undraw.co | Free | High | Concept illustrations |
| Storyset | storyset.com | Free | High | Animated scenes |
| Blush | blush.design | Free/Paid | High | Customizable people |
| DrawKit | drawkit.com | Free/Paid | High | SaaS illustrations |
| Absurd Design | absurd.design | Free | Unique | Quirky illustrations |
| Open Peeps | openpeeps.com | Free | Good | Hand-drawn people |
| Stubborn | stubborn.fun | Free | Good | Character generator |
| Pixeltrue | pixeltrue.com | Free | High | Modern illustrations |
</category>

<category name="3D Assets">
| Resource | URL | Price | Best For |
|----------|-----|-------|----------|
| Spline | spline.design | Free | Interactive 3D for web |
| Sketchfab | sketchfab.com | Free/Paid | 3D model marketplace |
| Poly Haven | polyhaven.com | Free | 3D models, HDRIs |
| Renderforest | renderforest.com | Paid | 3D mockups |
| Vectary | vectary.com | Free/Paid | 3D design tool |
| Three.js Journey | threejs-journey.com | Course | Learn 3D web |
</category>

<category name="Icons">
| Resource | URL | Price | Style |
|----------|-----|-------|-------|
| Lucide | lucide.dev | Free | Clean line icons |
| Heroicons | heroicons.com | Free | Tailwind-optimized |
| Phosphor | phosphoricons.com | Free | Flexible weights |
| Feather | feathericons.com | Free | Minimal |
| Tabler Icons | tabler-icons.io | Free | 3000+ icons |
| Lordicon | lordicon.com | Free/Paid | Animated icons |
</category>

<category name="Background Patterns & Textures">
| Resource | URL | Price | Type |
|----------|-----|-------|------|
| Hero Patterns | heropatterns.com | Free | SVG patterns |
| Haikei | haikei.app | Free | Generated backgrounds |
| Pattern Monster | pattern.monster | Free | Customizable patterns |
| Subtle Patterns | subtlepatterns.com | Free | Texture overlays |
| SVG Backgrounds | svgbackgrounds.com | Free | Ready-made SVGs |
| Trianglify | trianglify.io | Free | Geometric patterns |
</category>

<category name="Stock Photography">
| Resource | URL | Price | Focus |
|----------|-----|-------|-------|
| Unsplash | unsplash.com | Free | High-quality general |
| Pexels | pexels.com | Free | Diverse, searchable |
| Burst | burst.shopify.com | Free | Business/commerce |
| Nappy | nappy.co | Free | Diversity-focused |
| Reshot | reshot.com | Free | Unique, non-stocky |
| PREMIUM | shutterstock.com | $29+/mo | Largest selection |
| PREMIUM | adobe.stock.com | $29+/mo | Adobe integration |
</category>

<category name="Animation Resources">
| Resource | URL | Price | Type |
|----------|-----|-------|------|
| LottieFiles | lottiefiles.com | Free/Paid | After Effects → Web |
| Rive | rive.app | Free/Paid | Interactive animations |
| Motion One | motion.dev | Free | JS animation library |
| Framer Motion | framer.com/motion | Free | React animations |
| GSAP | gsap.com | Free/Paid | Professional animations |
| Animate.css | animate.style | Free | CSS animations |
</category>

</asset_categories>

<deliverable>/workspace/research/visual-asset-sources.md</deliverable>
</phase>

<phase id="4" name="Competitor Visual Audit">
<objective>Analyze what visuals competitors use (and where yours fall short)</objective>

<audit_framework>
For each competitor, document:

```markdown
## [Competitor Name]
**URL**:
**Overall Visual Score**: /10

### Hero Section
- [ ] Has hero image/visual: Yes/No
- Visual type: [3D | Illustration | Photo | Video | Gradient | None]
- Visual source (if identifiable):
- Screenshot: [attach]

### Supporting Sections
- [ ] Service cards have icons: Yes/No
- [ ] Features have illustrations: Yes/No
- [ ] Testimonials have photos: Yes/No
- [ ] Data/stats visualized: Yes/No

### Visual Assets Used
| Asset Type | Present? | Quality | Source (if known) |
|------------|----------|---------|-------------------|
| Custom illustrations | | | |
| Stock photos | | | |
| Icons | | | |
| 3D elements | | | |
| Background patterns | | | |
| Animations | | | |

### What Makes It Work (or Not)
[Analysis]

### Visual Gap vs CoreReceptionAI
[What they have that you don't]
```
</audit_framework>

<competitors_to_audit>
1. Direct PT clinic automation competitors (5+)
2. Premium B2B SaaS benchmarks: Linear, Vercel, Stripe, Notion, Figma
</competitors_to_audit>

<deliverable>/workspace/research/competitor-visual-audit.md</deliverable>
</phase>

<phase id="5" name="Visual Implementation Roadmap">
<objective>Create prioritized list of visuals to add with exact sources</objective>

<output_format>
```markdown
# CoreReceptionAI Visual Implementation Roadmap

## Immediate Impact (Week 1)

### 1. Hero Visual
**Recommendation**: [Specific type]
**Why**: [Evidence from research]
**Source**: [Exact URL/tool]
**Implementation**:
```code
[Actual code snippet or embed method]
```
**Estimated time**: X hours

### 2. Service Section Icons
**Recommendation**: [Icon set]
**Source**: [URL]
**Icons needed**: [List with names]

### 3. Background Treatment
**Recommendation**: [Pattern/gradient type]
**Source**: [URL]
**CSS**:
```css
[Actual CSS]
```

## High Impact (Week 2)

### 4. Testimonial Section
**Add**: Client photos or company logos
**Source**: [Where to get/request]
**Fallback**: [If no real photos available]

### 5. Feature Illustrations
**Recommendation**: [Style]
**Source**: [URL]
**Illustrations needed**:
- Feature 1: [description]
- Feature 2: [description]
- Feature 3: [description]

## Polish (Week 3+)

### 6. Micro-animations
**Library**: [Framer Motion / GSAP / etc]
**Animations**:
- Hero entrance: [description]
- Scroll reveals: [description]
- Hover states: [description]

### 7. 3D Elements (Optional)
**Tool**: [Spline / Three.js]
**Concept**: [What to build]
**Fallback**: [For mobile/low-end]
```
</output_format>

<deliverable>/workspace/research/VISUAL_ROADMAP.md</deliverable>
</phase>

</action>

<result>
<primary_deliverable>
/workspace/research/VISUAL_ROADMAP.md containing:
- Prioritized list of visuals to implement
- Exact sources for each asset type
- Code snippets for implementation
- Estimated timeline
</primary_deliverable>

<supporting_files>
- /workspace/research/visual-inspiration-sources.md
- /workspace/research/hero-visual-patterns.md
- /workspace/research/visual-asset-sources.md
- /workspace/research/competitor-visual-audit.md
</supporting_files>
</result>

<evaluate>
<success_criteria>
- [ ] Minimum 10 design inspiration sources documented with search strategies
- [ ] All 7 hero visual types documented with real examples
- [ ] At least 30 visual asset sources cataloged across categories
- [ ] 5+ competitors audited for visual patterns
- [ ] Final roadmap includes specific URLs/tools for each recommended visual
- [ ] Code snippets provided for key implementations
- [ ] Every recommendation cites evidence from research
</success_criteria>

<the_test>
After implementing this roadmap, the website should:
1. Have a visually compelling hero (not just text + button)
2. Use icons/illustrations in service sections
3. Include real or styled testimonial photos
4. Have animated elements that guide attention
5. Feel "premium" at first glance
</the_test>
</evaluate>

<non_goals>
Do NOT:
- Recommend paid assets over $100 without free alternatives
- Suggest visuals that require custom illustration skills
- Focus on color/typography (separate research)
- Recommend complex 3D that hurts performance
- Include more than 3 options per category (decision paralysis)
</non_goals>
```

---

## Quick Reference: Best Visual Asset Sources

### For Immediate Use (Free, High Quality)

| Need | Go Here First |
|------|---------------|
| Hero illustration | undraw.co or storyset.com |
| Icons | lucide.dev or heroicons.com |
| Background pattern | haikei.app |
| Stock photos | unsplash.com |
| Animations | lottiefiles.com |
| 3D elements | spline.design |
| Gradients | meshgradient.in |
| Mockups | mockupworld.co |

### For Inspiration

| Need | Go Here First |
|------|---------------|
| Hero section ideas | godly.website |
| Full landing pages | land-book.com |
| SaaS-specific | saaslandingpage.com |
| Premium/award-winning | awwwards.com |
| Dark mode designs | darkmodedesign.com |

### Implementation Libraries

| Need | Use This |
|------|----------|
| React animations | framer-motion |
| 3D in React | react-three-fiber |
| Scroll animations | GSAP ScrollTrigger |
| Lottie animations | lottie-react |
| Image optimization | next/image or sharp |

---

## Why This Prompt Works Better

| Original Problem | This Prompt's Solution |
|------------------|------------------------|
| Focused on colors/typography | Focuses on **visual assets** (images, illustrations, 3D) |
| No specific sources | **50+ specific URLs** for assets |
| Abstract "design patterns" | **Concrete visual types** with examples |
| No implementation guidance | **Code snippets** and embed methods |
| Overwhelming scope | **Prioritized roadmap** (Week 1, 2, 3) |
| Generic "research" | **Audit framework** for competitors |

The output isn't "what makes good design" - it's **"here's exactly what to add and where to get it."**
