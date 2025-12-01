# Content Creation Chain

A 4-stage prompt chain that transforms ideas into polished content.

## Overview

```
[Topic/Idea] → Stage 1: Research & Outline → Stage 2: Draft → Stage 3: Critique → Stage 4: Polish → [Final Content]
```

## Stage 1: Research & Outline

**Purpose:** Build foundation and structure before writing.

```xml
<role>You are a content strategist who creates compelling, well-structured content.</role>

<task>
Create a research-backed outline for: {{topic}}

Content type: {{content_type}}
Target audience: {{audience}}
Goal: {{content_goal}}
Tone: {{tone}}

Produce:
1. **Audience Analysis**
   - What do they already know?
   - What do they need to learn?
   - What objections might they have?

2. **Key Messages** (3-5 points)
   - What must readers remember?

3. **Research Points**
   - Statistics or data to include
   - Examples or case studies
   - Quotes or expert opinions

4. **Detailed Outline**
   - Hook/Opening
   - Section 1: [title] - [purpose]
   - Section 2: [title] - [purpose]
   - ...
   - Call to Action/Conclusion

5. **SEO Considerations** (if applicable)
   - Primary keyword: {{keyword}}
   - Secondary keywords
   - Search intent alignment
</task>

<output_format>
Outline should be detailed enough that writing becomes execution, not ideation.
End with: "Outline complete. Estimated length: [X words]"
</output_format>
```

---

## Stage 2: Draft

**Purpose:** Write the first complete draft.

```xml
<role>You are a skilled writer who creates engaging, clear content.</role>

<context>
{{stage_1_output}}
</context>

<task>
Write the full first draft following the outline.

Guidelines:
- Write in {{tone}} tone
- Use active voice
- Vary sentence length for rhythm
- Include transitions between sections
- Add specific examples, not generic statements
- For {{content_type}}, follow format conventions

Structure:
- Hook that addresses reader's pain point or curiosity
- Body that delivers on the promise
- Conclusion with clear next step

Do NOT:
- Use clichés ("In today's fast-paced world...")
- Pad with filler words
- Make claims without support
</task>

<output_format>
Write the complete draft with headers.
End with: "Draft complete. Word count: [X]"
</output_format>
```

---

## Stage 3: Critique

**Purpose:** Identify weaknesses and improvements.

```xml
<role>You are a harsh but constructive editor who makes content better.</role>

<context>
{{stage_2_output}}
</context>

<task>
Critique this draft ruthlessly but constructively:

1. **Engagement Score: [1-10]**
   - Would the target audience read past the first paragraph?
   - Is the hook strong enough?

2. **Clarity Score: [1-10]**
   - Any confusing sections?
   - Jargon that needs explaining?

3. **Structure Score: [1-10]**
   - Does it flow logically?
   - Are transitions smooth?

4. **Value Score: [1-10]**
   - Does it deliver on its promise?
   - Would readers share this?

5. **Specific Issues**
   For each problem:
   - Location: [quote or section]
   - Issue: [what's wrong]
   - Suggestion: [how to fix]

6. **What's Working**
   - Highlight 2-3 strengths to preserve
</task>

<output_format>
Be specific. Vague feedback like "make it better" is not allowed.
End with: "Critique complete. Priority fixes: [top 3]"
</output_format>
```

---

## Stage 4: Polish

**Purpose:** Apply feedback and finalize.

```xml
<role>You are a senior editor producing publish-ready content.</role>

<context>
Original draft:
{{stage_2_output}}

Critique:
{{stage_3_output}}
</context>

<task>
Produce the final, polished version:

1. Address all issues from critique
2. Tighten prose (remove unnecessary words)
3. Strengthen weak sections
4. Ensure consistent tone throughout
5. Check for:
   - Grammar and spelling
   - Formatting consistency
   - Link/reference accuracy
   - Call-to-action clarity

Final checks:
- Read aloud - does it flow?
- First sentence - would you keep reading?
- Last sentence - is the CTA clear?
</task>

<output_format>
Produce the final content, ready to publish.

End with:
---
**Final Word Count:** [X]
**Reading Time:** [X minutes]
**Confidence:** [HIGH/MEDIUM/LOW]
**Best for:** [where to publish/use this]
</output_format>
```

---

## Usage Examples

```bash
# Blog post
prompt chain content-creation \
  --topic "Why AI voice agents outperform human receptionists" \
  --content-type "blog post" \
  --audience "small business owners" \
  --goal "drive demo requests" \
  --tone "professional but conversational" \
  --keyword "AI receptionist"

# LinkedIn post
prompt chain content-creation \
  --topic "Lessons from scaling to 100 clients" \
  --content-type "LinkedIn post" \
  --audience "B2B founders" \
  --goal "thought leadership" \
  --tone "authentic, slightly vulnerable"

# Email sequence
prompt chain content-creation \
  --topic "Onboarding sequence for new trial users" \
  --content-type "email sequence (5 emails)" \
  --audience "SaaS trial users" \
  --goal "convert to paid" \
  --tone "helpful, not pushy"
```

## Chain Configuration

```json
{
  "name": "content-creation",
  "stages": 4,
  "variables": {
    "topic": "required",
    "content_type": "required",
    "audience": "required",
    "content_goal": "required",
    "tone": "optional, default: 'professional'",
    "keyword": "optional"
  },
  "pass_full_context": false,
  "pass_previous_stage": true,
  "model_recommendations": {
    "stage_1": "claude-sonnet-4-20250514",
    "stage_2": "claude-sonnet-4-20250514",
    "stage_3": "claude-sonnet-4-20250514",
    "stage_4": "claude-sonnet-4-20250514"
  }
}
```

## Content Type Templates

### Blog Post
- 1500-2500 words
- H2/H3 headers every 200-300 words
- Include 1-2 images/diagrams
- End with CTA

### LinkedIn Post
- 150-300 words
- Hook in first line
- Line breaks for readability
- End with question or CTA

### Email
- Subject line + preview text
- 100-200 words per email
- Single CTA per email
- P.S. line for secondary message
