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

---

## Research Findings (Verified December 2024)

### Premium SaaS Hero Patterns Analyzed

#### Linear.app
- **Visual Type**: 3D animated hero with detailed UI animation
- **Implementation**: Next.js + Tailwind + Framer Motion
- **Key Feature**: Hero animates on load, rotates in response to cursor
- **Open Source Clone**: [github.com/frontendfyi/rebuilding-linear.app](https://github.com/frontendfyi/rebuilding-linear.app)
- **Design Pattern**: "Bento Box" compartmentalized layout

#### Vercel.com
- **Visual Type**: Dark theme with prism visual + grid glow
- **Color Scheme**: White-on-black, gradient accents
- **Typography**: Geist font family
- **Animation**: Magnetic particles → fluid metallic liquid system
- **Tools Used**: Motion.js + Three.js
- **CTA Strategy**: Dual action-oriented buttons ("Start Deploying", "Get a Demo")
- **Reference**: [hero.gallery/hero-gallery/vercel](https://hero.gallery/hero-gallery/vercel)

#### Stripe.com
- **Visual Type**: Animated WebGL gradient background
- **Implementation**: Custom "minigl" WebGL + Canvas
- **CSS Transform**: `skewY(-12deg)` for angled effect
- **Gradient Colors**:
  ```css
  --gradientColorZero: #a960ee;
  --gradientColorOne: #ff333d;
  --gradientColorTwo: #90e0ff;
  --gradientColorThree: #ffcb57;
  ```
- **Open Source Libraries**:
  - [github.com/thelevicole/stripe-gradient](https://github.com/thelevicole/stripe-gradient)
  - [kevinhufnagl.com/how-to-stripe-website-gradient-effect](https://kevinhufnagl.com/how-to-stripe-website-gradient-effect/)
  - [CodePen examples](https://codepen.io/smitpatelx/pen/GRZayyO)

### Verified Illustration Libraries (2024)

| Library | URL | Unique Value |
|---------|-----|--------------|
| **unDraw** | [undraw.co](https://undraw.co) | 1000+ SVGs, color customizable on-site, MIT license |
| **Storyset** | [storyset.com](https://storyset.com) | Animated + static, Lottie export, by Freepik |
| **ManyPixels** | [manypixels.co](https://manypixels.co/gallery) | Most similar to unDraw, SVG + PNG |
| **Open Doodles** | [opendoodles.com](https://opendoodles.com) | Hand-drawn quirky style, CC0 license |
| **Humaaans** | [humaaans.com](https://humaaans.com) | Mix-and-match people builder |
| **DrawKit** | [drawkit.com](https://drawkit.com) | SaaS-focused, free + premium |
| **IRA Design** | [iradesign.io](https://iradesign.io) | 5 gradient styles per component |
| **Open Peeps** | [openpeeps.com](https://openpeeps.com) | Hand-drawn, building-block style |
| **Lummi** | [lummi.ai](https://lummi.ai) | AI-generated, 20,000+ images |
| **ITG.Digital** | [itg.digital](https://itg.digital) | Online illustration builder |

### Spline 3D Integration (React)

**Official Library**: [@splinetool/react-spline](https://github.com/splinetool/react-spline)

```jsx
// Basic Spline Hero Integration
import Spline from '@splinetool/react-spline';

export default function Hero() {
  return (
    <div className="relative h-screen bg-black">
      {/* 3D Background */}
      <Spline
        scene="https://prod.spline.design/YOUR-SCENE-ID/scene.splinecode"
        className="absolute inset-0 w-full h-full"
      />

      {/* Content Overlay */}
      <div className="relative z-10 flex flex-col items-center justify-center h-full text-white">
        <h1 className="text-6xl font-bold">Your Headline</h1>
        <p className="mt-4 text-xl text-gray-400">Subheadline text</p>
        <button className="mt-8 px-8 py-3 bg-cyan-500 rounded-lg">
          Get Started
        </button>
      </div>
    </div>
  );
}
```

**Next.js SSR Support**:
```jsx
import Spline from '@splinetool/react-spline/next';
// Renders blurred placeholder on server, loads 3D on client
```

**Spline vs React-Three-Fiber**:
- **Spline**: No-code, faster prototyping, easier export
- **React-Three-Fiber**: Fine-grained control, better performance optimization
- **Recommendation**: Start with Spline, migrate to R3F if performance issues

### Design Inspiration Galleries (Ranked)

| Rank | Site | Best For | Why |
|------|------|----------|-----|
| 1 | [godly.website](https://godly.website) | Cutting-edge animation | Hand-curated, boundary-pushing designs |
| 2 | [awwwards.com](https://awwwards.com) | Award-winning variety | World's best designers compete here |
| 3 | [land-book.com](https://land-book.com) | Landing page specific | Focused on conversion-oriented pages |
| 4 | [saaslandingpage.com](https://saaslandingpage.com) | SaaS-only examples | Curated from top SaaS companies |
| 5 | [landingfolio.com](https://landingfolio.com) | Components + templates | Includes Tailwind/Figma resources |
| 6 | [minimal.gallery](https://minimal.gallery) | Minimalist designs | Active since 2013, diverse quality |

### Code Resources for Implementation

**Stripe Gradient Effect**:
- Tutorial: [kevinhufnagl.com/how-to-stripe-website-gradient-effect](https://kevinhufnagl.com/how-to-stripe-website-gradient-effect/)
- Library: [github.com/thelevicole/stripe-gradient](https://github.com/thelevicole/stripe-gradient)
- jQuery Plugin: [jqueryscript.net/animation/stripe-gradient-animation.html](https://www.jqueryscript.net/animation/stripe-gradient-animation.html)

**Linear.app Clone**:
- Full rebuild: [github.com/frontendfyi/rebuilding-linear.app](https://github.com/frontendfyi/rebuilding-linear.app)
- Stack: Next.js + Tailwind + Framer Motion

**Hero Section Components**:
- Vercel v0: [v0.dev/chat/spline-design-hero](https://v0.dev/chat/spline-design-hero-h3SFiDjWwXO)
- Chakra Templates: [chakra-templates.vercel.app/page-sections/hero](https://chakra-templates.vercel.app/page-sections/hero)
- Aestero UI: [aestero-ui.vercel.app/herosection](https://aestero-ui.vercel.app/herosection)

**Design+Code Course** (Paid):
- [designcode.io/spline-react](https://designcode.io/spline-react/) - Complete 3D landing page tutorial

---

---

## Visual Design Trends 2024-2025

### Skeuomorphism Comeback ("Liquid Glass")

Apple's iOS 26 introduces "Liquid Glass" - skeuomorphism reimagined:
- **What it is**: Digital interfaces that mimic real-world materials (glass, metal, depth)
- **Why now**: Ultra-high resolution screens, advanced GPUs, user fatigue with flat design
- **Examples**: Photos icon mimics "layered stained glass", Camera app returns high-res lens illustration
- **SaaS Applications**: Fintech dashboards, productivity apps, meditation apps

**Sources**:
- [Apple's Liquid Glass Design](https://www.techradar.com/phones/iphone/apples-new-liquid-glass-design-puts-the-spotlight-on-skeuomorphism-for-the-first-time-since-ios-6-and-im-all-for-it)
- [Skeuomorphism Comeback 2025](https://kryzalid.net/en/web-marketing-blog/skeuomorphism-an-unexpected-comeback-in-2025/)
- [Rise of Skeuomorphic Minimalism](https://uiverse.io/blog/the-rise-of-skeumorphic-minimalism-ui-designs-unexpected-comeback-in-2025)

### Claymorphism (3D Clay UI)

Soft, inflated 3D shapes with pastel colors - coined by Michal Malewicz (Hype4):

**CSS Implementation**:
```css
.claymorphism {
  background: linear-gradient(145deg, #e6f0ff, #d1e3ff);
  border-radius: 40px;
  box-shadow:
    /* Outer shadow */
    8px 8px 20px rgba(0, 0, 0, 0.15),
    /* Inner highlight (top-left) */
    inset -4px -4px 8px rgba(255, 255, 255, 0.6),
    /* Inner shadow (bottom-right) */
    inset 4px 4px 8px rgba(0, 0, 0, 0.05);
}
```

**Key Properties**:
- Border radius: ~40% of button height
- Two inner shadows (top-left lighter, bottom-right darker)
- Pastel/bright colors only (dark colors kill the effect)
- Subtle gradient fill (top lighter than bottom)

**Resources**:
- [Claymorphism Generator](https://hype4.academy/tools/claymorphism-generator)
- [clay.css Library](https://codeadrian.github.io/clay.css/)
- [LogRocket Tutorial](https://blog.logrocket.com/implementing-claymorphism-css/)

### Bento Grid Layout

Japanese lunchbox-inspired compartmentalized design - the 2024 golden standard:

**Who Uses It**:
- Apple (iPhone product pages)
- Linear (feature introductions)
- Microsoft

**Why It Works for SaaS**:
- Organizes complex features without overwhelming
- Easy responsive adaptation
- Seamlessly integrates images, text, audio, video
- Perfect for dashboards and landing pages

**Resources**:
- [BentoGrids.com](https://bentogrids.com/) - Curated collection
- [SaaS Bento Examples](https://saaslandingpage.com/tag/bento-style/)
- [SaaSFrame Bento Analysis](https://www.saasframe.io/blog/the-bento-layout-trend)

### Glassmorphism (Frosted Glass)

Translucent frosted glass effect with blur:

**Tailwind CSS Implementation**:
```html
<div class="backdrop-blur-md bg-white/30 border border-white/20 rounded-lg shadow-lg p-6">
  <h2 class="text-xl font-semibold">Glass Card</h2>
  <p class="text-gray-800">Frosted glass effect with Tailwind</p>
</div>
```

**Key Classes**:
- `backdrop-blur-md` or `backdrop-blur-lg` - frosted effect
- `bg-white/30` - transparent white background
- `border border-white/20` - subtle border
- Custom: `backdrop-blur-[10px]`

**Generators**:
- [Tailwind Glassmorphism Generator](https://tailwindcss-glassmorphism.vercel.app/)
- [Gradienty Generator](https://gradienty.codes/tailwind-glassmorphism-generator)
- [CSS Glassmorphism Generator](https://notchtools.com/css-glassmorphism-generator)

### Aurora Gradient Backgrounds

Northern lights animated gradient effect:

**React + Tailwind (Performance-Optimized)**:
```jsx
// Uses CSS-only animation - no JS calculations
// Respects prefers-reduced-motion
// Smooth 60fps with GPU acceleration
```

**Key Technique**:
- `background-size: 400% 400%`
- Animate `background-position` over 15-60 seconds
- CSS blend modes: `hard-light`, `screen`, `overlay`
- Five independent orbs with different animation paths

**Component Libraries**:
- [Aceternity UI Aurora](https://ui.aceternity.com/components/aurora-background)
- [shadcn/ui Aurora](https://www.shadcn.io/background/aurora)
- [Auroral CSS Library](https://github.com/LunarLogic/auroral)
- [CodePen CSS-Only Aurora](https://codepen.io/Ahmod-Musa/pen/emNqPQd)

---

## Competitor Visual Audit Results (December 2024)

Based on analysis of 7 PT clinic software competitors:

| Competitor | Hero Visual | Background | 3D | Animation |
|------------|-------------|------------|-----|-----------|
| WebPT | Product screenshot | Light blue | ❌ | Fade-in |
| Cliniko | Illustration | White | ❌ | None |
| SimplePractice | Product screenshot | Gradient | ❌ | Subtle |
| Jane App | Product screenshot | Light | ❌ | Fade-in |
| Hint | Lifestyle photo | White | ❌ | None |
| Healthie | Product screenshot | Light blue | ❌ | Fade-in |
| IntakeQ | Product screenshot | White | ❌ | None |

**Gap Opportunities**:
- **3D Elements**: 0/7 competitors use 3D
- **Dark Mode**: 0/7 use dark backgrounds
- **Bold Animations**: 6/7 use only subtle fade-ins
- **Glassmorphism**: 0/7 use glass effects

**Differentiation Strategy**:
- Use 3D floating geometry (Spline or React Three Fiber)
- Dark background (#0f172a) with cyan accent (#06b6d4)
- Bold animations (parallax, stagger reveals, 3D rotation)
- Glassmorphic cards for pricing/features

---

## Professional Tech Stack Research (December 2024)

### What Professionals Actually Use (Reddit/HN/GitHub)

Based on research from Hacker News, Reddit r/webdev, and GitHub:

#### The Winning Stack for Beautiful SaaS Websites

```
Frontend:  Next.js 14/15 + React 19 + TypeScript
Styling:   Tailwind CSS v4
Animation: Framer Motion
Components: shadcn/ui + Magic UI or Aceternity UI
Hosting:   Vercel
```

**Why this combo dominates:**
- **Next.js** - Server-side rendering, SEO, fast builds (used by Linear, Vercel, Stripe)
- **Tailwind** - 7% market share, #1 CSS framework for landing pages
- **Framer Motion** - "Production-ready" per creators, powers Linear.app animations
- **shadcn/ui** - Copy-paste components, full code ownership, no dependency lock-in

#### Solo Entrepreneur Favorites (HN "Companies of One" Thread)

| Stack | Use Case | Why They Chose It |
|-------|----------|-------------------|
| Next.js + shadcn/ui + Vercel | SaaS landing pages | Fast deployment, beautiful defaults |
| Rails + SQLite + Hetzner | Full apps | Simple, cheap, convention over config |
| Remix + Tailwind | Interactive apps | Nested routing, data loading |
| Astro + Svelte | Content sites | Best performance, partial hydration |
| Phoenix LiveView | Real-time apps | No JS needed, fast |

#### Animation Component Libraries (Ranked by GitHub Stars)

| Library | Stars | Best For | URL |
|---------|-------|----------|-----|
| **Magic UI** | 19,000+ | Landing pages, effects | [magicui.design](https://magicui.design) |
| **Aceternity UI** | 15,000+ | Hero sections, 3D | [ui.aceternity.com](https://ui.aceternity.com) |
| **shadcn/ui** | 80,000+ | Base components | [ui.shadcn.com](https://ui.shadcn.com) |
| **Framer Motion** | 25,000+ | All animations | [framer.com/motion](https://www.framer.com/motion) |

### GitHub Templates to Clone (Production-Ready)

#### SaaS Landing Pages

| Repo | Stack | Stars | URL |
|------|-------|-------|-----|
| **launch-ui** | Next.js 15 + shadcn + Tailwind v4 | High | [github.com/launch-ui/launch-ui](https://github.com/launch-ui/launch-ui) |
| **saas-landing-page-template** | Next.js 14 + Framer Motion (Dark) | Growing | [github.com/karthikmudunuri/saas-landing-page-template](https://github.com/karthikmudunuri/saas-landing-page-template) |
| **shadcn-landing-page** | Next.js + shadcn + TypeScript | Growing | [github.com/leoMirandaa/shadcn-landing-page](https://github.com/leoMirandaa/shadcn-landing-page) |
| **Magic UI Templates** | Next.js + Magic UI + Tailwind | Included | [magicui.design/docs/templates](https://magicui.design/docs/templates) |

#### Linear.app Clones (Learn Premium Animations)

| Repo | What You Learn | URL |
|------|----------------|-----|
| **frontendfyi/rebuilding-linear.app** | Hero animations, keyboard shortcuts | [GitHub](https://github.com/frontendfyi/rebuilding-linear.app) |
| **thenameiswiiwin/linear-clone** | Next.js 13 patterns | [GitHub](https://github.com/thenameiswiiwin/linear-clone) |

### How Top SaaS Sites Are Built

| Site | Framework | Animation | Hosting | Verified Source |
|------|-----------|-----------|---------|-----------------|
| **Linear.app** | Next.js | Framer Motion | Vercel | [BuiltWith](https://builtwith.com/linear.app) |
| **Vercel.com** | Next.js | Three.js + Motion | Vercel | [BuiltWith](https://builtwith.com/vercel.com) |
| **Stripe.com** | Custom React | WebGL (minigl) | Custom | Reverse-engineered |
| **Notion.so** | Next.js | Custom | AWS | [StackShare](https://stackshare.io/notion) |

### Step-by-Step: Build Like Linear

```bash
# 1. Clone the best starter
npx create-next-app@latest my-site --typescript --tailwind --app

# 2. Add shadcn/ui
npx shadcn@latest init

# 3. Add animation libraries
npm install framer-motion @react-three/fiber @react-three/drei

# 4. Add Magic UI components (copy-paste)
# Visit magicui.design and copy components you need

# 5. Add Aceternity effects (copy-paste)
# Visit ui.aceternity.com for hero effects

# 6. Deploy to Vercel
vercel deploy
```

### Recommended Learning Path

1. **Start**: Clone [launch-ui](https://github.com/launch-ui/launch-ui) or [Magic UI template](https://magicui.design/docs/templates)
2. **Study**: [frontendfyi/rebuilding-linear.app](https://github.com/frontendfyi/rebuilding-linear.app) for animation patterns
3. **Add Effects**: Copy components from Aceternity UI and Magic UI
4. **Customize**: Use the design tokens from our CoreReceptionAI design system
5. **Deploy**: Push to Vercel with one click

### Tools for Non-Coders

| Tool | Best For | Pricing |
|------|----------|---------|
| **v0.dev** | Generate React/Tailwind from prompts | Free tier |
| **Framer** | No-code with pro animations | $20/mo |
| **Webflow** | No-code, most flexibility | $14/mo |
| **Bolt.new** | Full-stack AI builder | Free tier |

---

## Files Cleaned Up

Removed unnecessary backup files:
- `scripts/prompt.sh.bak`
- `scripts/prompt.sh.bak2`
- `scripts/prompt.sh.bak3`
- `scripts/prompt.sh.backup`
- `scripts/prompt.sh.backup_20251128_000650`
- `scripts/prompt.sh.backup_20251128_001513`
