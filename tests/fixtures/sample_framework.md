# Sample Decision Framework

## Purpose
Help make structured decisions when facing multiple viable options.

## When to Use
- Choosing between build vs buy
- Evaluating vendor options
- Prioritizing feature development
- Resource allocation decisions

## Context Injection Points
<!-- System injects relevant context here -->
[INJECT: business context]
[INJECT: current constraints]
[INJECT: past similar decisions]

---

## The Process

### Step 1: Define Success Criteria
What makes this decision successful?

**Categories to consider:**
- Speed: How quickly can we execute?
- Cost: What's the total investment?
- Quality: What standard must we meet?
- Risk: What can we afford to lose?
- Learning: What capabilities do we gain?

### Step 2: Generate Options
List all viable approaches (minimum 3):

| Option | Description | Pros | Cons |
|--------|-------------|------|------|
| Option A | | | |
| Option B | | | |
| Option C | | | |

### Step 3: Score Against Criteria
Rate each option 1-10 against success criteria:

| Option | Speed | Cost | Quality | Risk | Learning | Total |
|--------|-------|------|---------|------|----------|-------|
| A | | | | | | |
| B | | | | | | |
| C | | | | | | |

### Step 4: Test Assumptions
For the leading option, identify risks:

**Questions to answer:**
- What could go wrong?
- What assumptions are we making?
- What would we need to learn?
- What's reversible vs irreversible?

### Step 5: Define Decision Point
When will we commit?

**Commitment plan:**
- **Pilot phase:** Small test (1-2 weeks)
- **Evaluation:** What metrics prove success?
- **Go/No-Go:** When do we fully commit or pivot?

---

## Output Format

After working through this framework, provide:

1. **Recommended Option**
   - Clear choice with rationale

2. **Key Tradeoffs**
   - What we're giving up
   - What we're gaining

3. **Risk Mitigation**
   - Top 3 risks and how to address them

4. **Next Action**
   - Specific first step to validate decision

---

## Meta-Instructions for Claude

When applying this framework:
- Push for 3+ options even if one seems obvious
- Challenge optimistic assumptions
- Highlight irreversible decisions
- Suggest small experiments before big commitments
- Be direct about what we don't know
