# AI Video Creation Research & Implementation Prompt

## Optimized for Gemini Deep Research

**Created using:** Prompt Engineering System v1.0
**Techniques Applied:** CARE Framework, XML Structure, Chain-of-Thought, Few-Shot Examples, Task-First Ordering, Progressive Disclosure, Confidence Calibration, Multi-Path Verification

---

## THE PROMPT

```xml
<role>
You are a senior AI video production researcher and technical strategist. Your expertise spans AI-powered content creation tools, automation pipelines, and the practical workflows used by successful faceless content creators in 2024-2025.

Your characteristics:
- Deep knowledge of AI video generation tools (Sora, Runway, Kling, Veo, Pika)
- Experience with voice synthesis (ElevenLabs, Murf, Play.ht)
- Understanding of automation platforms (n8n, Make, Zapier)
- Data-driven approach to tool recommendations
- Focus on practical, implementable solutions over theoretical possibilities
</role>

<mission>
Execute comprehensive deep research on Reddit conversations and GitHub projects to identify the most effective AI video creation stacks, then create detailed implementation guides for 10 specific video formats that I can execute immediately.
</mission>

<context>
<my_situation>
- Creating faceless/semi-faceless AI video content for Instagram
- Format: 70% AI B-roll/stock footage, 30% screen recordings
- Audio: My real voice (not AI-generated) for authenticity
- Visual style: No face shown, occasional hands/monitor shots
- Goal: Build authority in AI niche without "young face" perception issues
</my_situation>

<previous_video_ideas>
You previously provided me 10 video concepts. Here they are for reference:

1. **AI Tool Ranking (Listicle)** - Fast-paced comparison of AI tools
2. **"Secret" Workflow Tutorial** - Screen recording of hidden features
3. **Aesthetic Desk Tour** - Cinematic B-roll, ASMR vibes
4. **Tribal Comparison** - Split-screen product battles
5. **Digital Documentary** - AI-generated imagery with storytelling
6. **Productivity Cheat Code** - Text overlay + stock footage
7. **Kinetic Motivation** - Typography + motivational audio
8. **Tech News Speedrun** - 60-second news recap
9. **Sensory Unboxing** - Hand-only ASMR product reveals
10. **Expectation vs Reality** - Contrast format for humor/trust
</previous_video_ideas>

<my_constraints>
- Budget: Prefer free/low-cost tools initially, willing to pay for proven ROI
- Timeline: Want to publish first video within 1 week
- Skills: Comfortable with basic video editing (CapCut), can learn new tools
- Equipment: iPhone 14, basic ring light, decent microphone
- Platform focus: Instagram Reels (vertical format, 15-60 seconds)
</my_constraints>
</context>

<research_instructions>
Execute deep research in two phases:

<phase_1_reddit>
Search these subreddits for AI video creation insights:
- r/LocalLLaMA (local AI models, optimization)
- r/ChatGPT (prompt engineering for video scripts)
- r/ClaudeAI (Claude-specific workflows)
- r/artificial (general AI tools)
- r/SideProject (indie creator tech stacks)
- r/Entrepreneur (monetization, growth strategies)
- r/contentcreation (creator workflows)
- r/InstagramReels (platform-specific tactics)

For each relevant thread, extract:
1. Specific tool combinations recommended
2. Step-by-step workflows shared
3. Cost breakdowns mentioned
4. Problems/limitations people encountered
5. Tips that improved results
6. Links to resources/tutorials

Search queries to use:
- "AI video generation workflow 2024"
- "faceless YouTube channel tools"
- "ElevenLabs video automation"
- "n8n video creation"
- "AI B-roll generation"
- "automated content pipeline"
- "Runway vs Kling vs Pika"
- "text to video workflow"
</phase_1_reddit>

<phase_2_github>
Search GitHub for:
- Repositories with 50+ stars related to AI video generation
- Automation pipelines for content creation
- Open-source alternatives to paid tools
- Integration examples (API combinations)

For each relevant repository, extract:
1. Repository name and URL
2. Star count and last update date
3. Core functionality
4. Technologies/APIs used
5. Setup complexity (easy/medium/hard)
6. Active maintenance status
7. Notable issues or limitations from Issues tab
</phase_2_github>
</research_instructions>

<output_requirements>
Provide your findings in this exact structure:

<section_1_tool_stack_analysis>
## Recommended Tool Stacks

For each category, provide:
- **Best Free Option**: [Tool] - [Why]
- **Best Paid Option**: [Tool] - [Why] - [Cost]
- **Reddit Consensus**: [What most creators recommend]
- **GitHub Evidence**: [Relevant projects/integrations]

Categories:
1. Video Generation (Sora, Runway, Kling, Veo, Pika, Luma)
2. Voice Synthesis (ElevenLabs, Murf, Play.ht, local TTS)
3. Script Generation (ChatGPT, Claude, local LLMs)
4. B-Roll/Stock (Pexels, AI generators, stock libraries)
5. Editing (CapCut, DaVinci, Descript)
6. Automation (n8n, Make, Zapier, custom scripts)
7. Thumbnail/Graphics (Canva, Midjourney, DALL-E)
</section_1_tool_stack_analysis>

<section_2_implementation_guides>
## Implementation Guides (One Per Video Concept)

For EACH of the 10 video ideas, create a guide with:

### Video [N]: [Concept Name]

**My Stack for This Format:**
| Component | Tool | Why This Tool | Cost |
|-----------|------|---------------|------|
| Video Gen | [X] | [Reason] | [$/mo] |
| Voice | [X] | [Reason] | [$/mo] |
| Editing | [X] | [Reason] | [$/mo] |
| Automation | [X] | [Reason] | [$/mo] |
| **Total** | | | **[$/mo]** |

**Step-by-Step Workflow:**
1. [Step] - [Time estimate] - [Tool used]
2. [Step] - [Time estimate] - [Tool used]
3. [Step] - [Time estimate] - [Tool used]
...

**Script Template:**
```
[0:00-0:03] HOOK: "[Exact hook text]"
[0:03-0:XX] BODY: "[Content structure]"
[0:XX-END] CTA: "[Call to action]"
```

**Visual Breakdown:**
- 0:00-0:03: [Visual type] - [Source/how to create]
- 0:03-0:10: [Visual type] - [Source/how to create]
...

**Reddit Tips for This Format:**
- [Tip 1 from Reddit discussion]
- [Tip 2 from Reddit discussion]
- [Common mistake to avoid]

**Time to Produce:** [X minutes/hours]
**Difficulty:** [Easy/Medium/Hard]
**Confidence Level:** [High/Medium/Low] - [Why]
</section_2_implementation_guides>

<section_3_google_sheet_data>
## Google Sheet Export Data

Provide data formatted for direct paste into Google Sheets:

**Tab 1: Tool Comparison**
| Tool Name | Category | Cost/mo | Free Tier | API Available | Reddit Rating | Best For |
|-----------|----------|---------|-----------|---------------|---------------|----------|
[10-15 rows of top tools]

**Tab 2: Implementation Guides**
| Video # | Concept | Tool Stack | Est. Cost | Production Time | Difficulty | Script Hook | First Step |
|---------|---------|------------|-----------|-----------------|------------|-------------|------------|
[10 rows, one per video concept]

**Tab 3: Workflow Checklist**
| Video # | Step 1 | Step 2 | Step 3 | Step 4 | Step 5 | Step 6 |
|---------|--------|--------|--------|--------|--------|--------|
[10 rows with checkable steps]

**Tab 4: Resources**
| Resource Type | Name | URL | Notes |
|---------------|------|-----|-------|
[15-20 rows of Reddit threads, GitHub repos, tutorials]
</section_3_google_sheet_data>

<section_4_prioritized_action_plan>
## Your First Week Action Plan

**Day 1: Setup**
- [ ] [Specific action with tool]
- [ ] [Specific action with tool]

**Day 2: First Video Prep**
- [ ] [Specific action]
- [ ] [Specific action]

**Day 3-4: Production**
- [ ] [Specific action]
- [ ] [Specific action]

**Day 5: Edit & Polish**
- [ ] [Specific action]

**Day 6: Publish & Analyze**
- [ ] [Specific action]

**Day 7: Iterate**
- [ ] [Specific action]

**Recommended First Video:** [Which of the 10 concepts to start with and why]
</section_4_prioritized_action_plan>
</output_requirements>

<success_criteria>
Your research is successful if:
1. ✅ Every tool recommendation includes source (Reddit thread or GitHub repo)
2. ✅ Each implementation guide is specific enough to execute without additional research
3. ✅ Cost estimates are current (2024-2025 pricing)
4. ✅ Workflows match my constraints (faceless, my voice, 70% AI B-roll)
5. ✅ Google Sheet data is copy-paste ready
6. ✅ Action plan is achievable in 7 days with my equipment/skills
7. ✅ Confidence levels are honest (don't oversell uncertain recommendations)
</success_criteria>

<reasoning_requirements>
Before finalizing each recommendation, work through:

<thinking>
1. What does Reddit consensus say about this tool/approach?
2. What GitHub evidence supports this?
3. Does this fit my specific constraints?
4. What could go wrong with this recommendation?
5. What's my confidence level and why?
</thinking>

Then provide your recommendation with this reasoning visible.
</reasoning_requirements>

<verification>
After completing the research, verify:
- [ ] All 10 video concepts have complete implementation guides
- [ ] Tool recommendations include both free and paid options
- [ ] Reddit sources are cited for major recommendations
- [ ] GitHub repos are linked where relevant
- [ ] Google Sheet format is consistent and complete
- [ ] Action plan accounts for my 1-week timeline
- [ ] No recommendations require skills/equipment I don't have
</verification>
```

---

## TECHNIQUES APPLIED

### 1. CARE Framework
- **Context**: My situation, constraints, previous video ideas
- **Action**: Deep research on Reddit + GitHub
- **Result**: Implementation guides + Google Sheet data
- **Evaluate**: 7 success criteria + verification checklist

### 2. XML Structure (Claude/Gemini Optimized)
- Clear semantic tags for each section
- Nested structure for complex requirements
- Easy parsing and reference

### 3. Task-First Ordering
- Mission stated immediately after role
- Context provided AFTER task is clear
- Details follow in logical progression

### 4. Chain-of-Thought
- `<thinking>` tags force explicit reasoning
- Step-by-step verification process
- Confidence calibration required

### 5. Few-Shot via Structure
- Output format shows exactly what's expected
- Table structures demonstrate desired format
- Script template shows timing pattern

### 6. Progressive Disclosure
- Phase 1 (Reddit) → Phase 2 (GitHub) → Output
- Simple structure → complex implementation guides

### 7. Specificity Over Vagueness
- Exact subreddits listed
- Specific search queries provided
- Table columns defined precisely
- Time estimates required for each step

### 8. Multi-Path Verification
- Reddit consensus + GitHub evidence
- Free AND paid options for comparison
- Multiple success criteria

### 9. Confidence Calibration
- Explicit confidence levels required
- "Why" reasoning mandatory
- Honest uncertainty encouraged

### 10. Constraint Integration
- Budget constraints stated upfront
- Equipment limitations noted
- Timeline (1 week) drives action plan

---

## HOW TO USE THIS PROMPT

1. **Copy the entire XML block** (between the triple backticks)
2. **Paste into Gemini** with Deep Research enabled
3. **Let it run** the full research cycle
4. **Export results** to your Google Sheet

### Expected Output Size
- ~3,000-5,000 words of research synthesis
- 10 detailed implementation guides
- 4 Google Sheet tabs worth of data
- 7-day action plan

### Follow-Up Prompts
After receiving results, you can ask:
- "Expand on the workflow for Video #3"
- "Compare [Tool A] vs [Tool B] in more detail"
- "What if my budget is $0 for the first month?"
- "Show me the exact prompts for generating B-roll with [Tool]"

---

## VERSION HISTORY

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2024-12-01 | Initial creation using prompt engineering system |

---

*Generated by Prompt Engineering System*
*Location: C:/Users/JRiel/prompt-engineering-system/*
