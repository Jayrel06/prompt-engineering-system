# Root Cause Analysis Framework

## Purpose
Find the actual cause of a problem, not just symptoms. Solving symptoms without addressing root causes leads to recurring problems.

## When to Use
- When problems keep coming back
- After incidents or failures
- When symptoms are being treated but problem persists
- For process improvement

---

## The Process

### Stage 1: Define the Problem
What exactly happened?

**Be specific:**
- What was observed?
- When did it happen?
- Where did it happen?
- Who was involved?
- What was the impact?

### Stage 2: Five Whys
Ask "why" repeatedly until you reach a root cause.

```
Problem: [State the problem]
↓ Why?
Because: [First answer]
↓ Why?
Because: [Second answer]
↓ Why?
Because: [Third answer]
↓ Why?
Because: [Fourth answer]
↓ Why?
Because: [Root cause - can't meaningfully ask "why" again]
```

**Tips:**
- Stay focused on one causal chain at a time
- If multiple causes, branch and follow each
- Stop when you reach something actionable

### Stage 3: Categorize the Root Cause
What type of cause is this?

**Common categories:**
- **Process:** Missing or broken process
- **People:** Training, staffing, communication
- **Technology:** Tools, systems, infrastructure
- **Policy:** Rules that cause bad outcomes
- **Environment:** External factors
- **Design:** Fundamental architecture issues

### Stage 4: Verify the Root Cause
How do we know this is actually the root cause?

**Tests:**
- If we fix this, will the problem stop recurring?
- Can we explain the entire problem from this cause?
- Is this actionable (not just "human error")?
- Does the team agree this is the actual cause?

### Stage 5: Develop Countermeasures
How do we address the root cause?

| Root Cause | Countermeasure | Owner | Timeline |
|------------|----------------|-------|----------|
| | | | |

**Good countermeasures:**
- Address the root cause, not symptoms
- Prevent recurrence, not just fix this instance
- Are sustainable long-term
- Don't create new problems

---

## Output Format

1. **Problem Statement:** Clear, specific description
2. **Five Whys Chain:** Path to root cause
3. **Root Cause:** The actual underlying issue
4. **Verification:** Why we believe this is correct
5. **Countermeasures:** Actions to prevent recurrence
6. **Success Metrics:** How we'll know it's fixed

---

## Common Root Cause Traps

### "Human Error"
Never stop at "someone made a mistake."
Ask: Why was the mistake possible? What would prevent it?

### Multiple Causes
Most problems have multiple contributing factors.
Prioritize: Which cause, if fixed, prevents most recurrence?

### Treating Symptoms
If your solution is "be more careful" or "try harder," you haven't found the root cause.

### Going Too Deep
Stop when you reach something actionable.
"Laws of physics" is not a useful root cause.
