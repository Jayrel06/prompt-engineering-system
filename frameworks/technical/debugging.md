# Debugging Framework

## Purpose
Systematically isolate and fix problems. Avoid random guessing and wasted time.

## When to Use
- When something isn't working
- When behavior is unexpected
- When errors are occurring
- Before asking for help

---

## The Process

### Stage 1: Reproduce the Problem
Can you make it happen consistently?

**Document:**
- Exact steps to reproduce
- Environment (OS, versions, etc.)
- Input data
- Expected vs actual behavior

**If intermittent:**
- What's different when it works vs doesn't?
- Is it timing-related?
- Resource-related?
- Data-related?

### Stage 2: Gather Information

**Collect:**
- Error messages (exact text)
- Logs (before, during, after)
- System state
- Recent changes

**Questions:**
- When did this start happening?
- What changed recently?
- Does it happen in all environments?
- Are there related issues?

### Stage 3: Form Hypotheses
What could cause this behavior?

List possible causes ranked by:
- Likelihood (based on evidence)
- Ease of testing

| Hypothesis | Evidence For | Evidence Against | How to Test |
|------------|--------------|------------------|-------------|
| | | | |

### Stage 4: Isolate the Problem

**Techniques:**
- **Binary search:** Narrow down where the problem is
- **Simplify:** Remove components until problem disappears
- **Compare:** Working vs non-working cases
- **Log:** Add visibility at key points

**Goal:** Find the smallest reproduction case

### Stage 5: Fix and Verify

**Before fixing:**
- Write a test that fails (proves the bug)

**After fixing:**
- Test passes
- Original problem resolved
- No new problems introduced
- Root cause addressed (not just symptom)

### Stage 6: Prevent Recurrence

**Ask:**
- Why wasn't this caught earlier?
- Could we add monitoring/alerting?
- Should we add tests?
- Is documentation needed?

---

## Output Format

1. **Problem:** Clear description of what's wrong
2. **Reproduction:** Steps to make it happen
3. **Investigation:** What you found
4. **Root Cause:** Why it's happening
5. **Fix:** What you changed
6. **Prevention:** How to avoid in future

---

## Debugging Checklist

### Before Diving In
- [ ] Can I reproduce it?
- [ ] Do I understand expected behavior?
- [ ] Have I checked logs/errors?
- [ ] What changed recently?

### During Investigation
- [ ] Am I testing hypotheses, not guessing?
- [ ] Am I narrowing the scope?
- [ ] Am I documenting what I find?
- [ ] Should I ask for help?

### After Fixing
- [ ] Is the problem actually fixed?
- [ ] Did I address root cause?
- [ ] Any side effects?
- [ ] What can prevent recurrence?

---

## Common Debugging Traps

### Random Guessing
Making changes without hypotheses. Wastes time, can make things worse.

### Confirmation Bias
Only looking for evidence that supports your theory.

### Tunnel Vision
Assuming the problem is in one area without verifying.

### Not Reading Errors
The error message often tells you exactly what's wrong.

### Cargo Culting
Copying solutions without understanding why they work.
