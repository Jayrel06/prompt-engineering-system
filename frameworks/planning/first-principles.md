# First Principles Analysis Framework

## Purpose
Break down complex problems to their fundamental truths and rebuild understanding from the ground up.

## When to Use
- Starting projects with unclear requirements
- Questioning existing approaches
- Designing systems from scratch
- Making major strategic decisions

## Context Injection Points
<!-- System injects relevant context here -->
[INJECT: relevant project context]
[INJECT: domain expertise]
[INJECT: past similar problems]

---

## The Process

### Stage 1: Define the Ultimate Goal
What are we actually trying to achieve?

**Answer these questions:**
- If this succeeds perfectly, what changes in the world?
- Who benefits and how specifically?
- What would make this a complete waste of time?
- What's the simplest version of success?

### Stage 2: Surface All Assumptions
List every assumption—explicit and implicit.

**Categories to examine:**
- **Technical:** What technology can/can't do
- **Resource:** Time, money, people available
- **Market:** What customers want/need
- **Competitive:** What others will do
- **Personal:** What I'm capable of
- **Environmental:** External factors assumed stable

### Stage 3: Identify Load-Bearing Assumptions
Which assumptions, if wrong, would completely change our approach?

**For each critical assumption, evaluate:**
| Assumption | Evidence For | Evidence Against | Confidence (1-10) | Cost if Wrong |
|------------|--------------|------------------|-------------------|---------------|
| | | | | |

### Stage 4: Blank Slate Design
If starting fresh with unlimited resources, what would we build?

**Consider:**
- Ideal architecture (no constraints)
- Optimal user experience
- Perfect outcome state
- What would a 10x solution look like?

### Stage 5: Reintroduce Constraints
Add back real-world constraints one at a time:

**For each constraint:**
1. What does this eliminate from the ideal?
2. What's the minimum viable alternative?
3. Is this constraint actually immutable?
4. What would it take to remove this constraint?

**Common constraints:**
- Time (deadline, urgency)
- Budget (money available)
- Technical (existing systems, skills)
- People (team size, expertise)
- External (regulations, dependencies)

### Stage 6: Minimum Viable Test
What's the smallest thing we can build to test the core hypothesis?

**Define:**
- One clear hypothesis to test
- One experiment to validate/invalidate
- Timeline under 1 week
- Clear success/failure criteria
- What we'll learn either way

---

## Output Format

After working through this framework, provide:

1. **Restated Goal** (1-2 sentences)
   - The actual objective, clearly stated

2. **Critical Assumptions** (top 3)
   - Each with confidence level and evidence

3. **Non-Obvious Insights**
   - What surprised you in this analysis

4. **Recommended Approach**
   - With explicit rationale

5. **First Action**
   - Specific next step to take

---

## Meta-Instructions for Claude

When applying this framework:
- Challenge my framing if it seems limiting
- Point out blind spots given my background (technical founder, solo operator)
- Suggest approaches I wouldn't naturally consider
- Be direct about weak assumptions
- Don't just validate my thinking—improve it
- Ask clarifying questions if the problem is ambiguous
