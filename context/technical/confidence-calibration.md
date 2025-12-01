# Confidence Calibration Guide

Explicit confidence levels improve response reliability and help you know when to verify or dig deeper.

## Why Confidence Matters

- **HIGH confidence** → Trust the answer, proceed quickly
- **MEDIUM confidence** → Consider verification or second opinion
- **LOW confidence** → Definitely verify, may need expert input

## Standard Confidence Format

Always end responses with:

```
---
**Confidence:** [HIGH/MEDIUM/LOW]
**Reasoning:** [1-2 sentences explaining why]
**Verification suggested:** [Yes/No] - [what to verify if Yes]
```

## Confidence Criteria

### HIGH Confidence (85-100%)
Use when:
- Task is within clear expertise area
- Answer is based on established facts/patterns
- Similar problems solved successfully before
- Clear documentation/examples exist
- No significant ambiguity in requirements

Example:
```
Confidence: HIGH
Reasoning: Standard Python dict comprehension syntax, well-documented pattern.
Verification suggested: No
```

### MEDIUM Confidence (50-84%)
Use when:
- Some uncertainty about edge cases
- Multiple valid approaches exist
- Based on reasoning rather than direct knowledge
- Requirements have some ambiguity
- Solution works but may not be optimal

Example:
```
Confidence: MEDIUM
Reasoning: Architecture should work but hasn't been tested at this scale. May need tuning.
Verification suggested: Yes - load test before production deployment
```

### LOW Confidence (0-49%)
Use when:
- Outside primary expertise area
- Information may be outdated
- Significant assumptions made
- Complex domain with many unknowns
- First attempt at this type of problem

Example:
```
Confidence: LOW
Reasoning: Tax implications vary by jurisdiction and I may not have current regulations.
Verification suggested: Yes - consult with a tax professional for your specific situation
```

## Calibration by Task Type

### Code Generation
| Scenario | Typical Confidence |
|----------|-------------------|
| Standard library usage | HIGH |
| Common patterns (CRUD, auth) | HIGH |
| Complex algorithms | MEDIUM |
| Unfamiliar framework | MEDIUM |
| Performance optimization | MEDIUM-LOW |
| Security-critical code | MEDIUM (always review) |

### Technical Advice
| Scenario | Typical Confidence |
|----------|-------------------|
| Best practices (well-documented) | HIGH |
| Architecture decisions | MEDIUM |
| Technology recommendations | MEDIUM |
| Future predictions | LOW |
| Pricing/cost estimates | LOW |

### Business/Strategy
| Scenario | Typical Confidence |
|----------|-------------------|
| Framework application | MEDIUM-HIGH |
| Market analysis | MEDIUM |
| Competitor insights | MEDIUM-LOW |
| ROI predictions | LOW |
| Legal/compliance | LOW (not qualified) |

## Prompt Template with Confidence

Use this wrapper for any task requiring reliability:

```xml
<task>
{{your_task_here}}
</task>

<output_requirements>
1. Complete the task thoroughly
2. Show your reasoning process
3. End with confidence assessment:

---
**Confidence:** [HIGH/MEDIUM/LOW]
**Reasoning:** [Why this confidence level]
**Key assumptions:** [List any assumptions made]
**Verification suggested:** [Yes/No and what to verify]
</output_requirements>
```

## Self-Calibration Questions

Before assigning confidence, ask:
1. How certain am I about the core answer?
2. What could make this wrong?
3. Have I solved similar problems successfully?
4. What am I assuming that might not be true?
5. Would I bet money on this answer?

## Confidence Tracking

Over time, track your calibration accuracy:

```markdown
| Date | Task | Stated Confidence | Actual Outcome | Calibration |
|------|------|------------------|----------------|-------------|
| 2024-01-15 | API design | HIGH | Worked perfectly | Accurate |
| 2024-01-16 | Performance estimate | MEDIUM | 2x slower than predicted | Over-confident |
| 2024-01-17 | Security review | LOW | Caught 2/3 issues | Accurate |
```

## Integration with Prompt Router

The prompt router automatically adds confidence requirements when:
- Task involves reasoning or analysis
- Multiple approaches are possible
- Domain has high uncertainty

## Common Calibration Mistakes

### Over-confidence
- Assuming recent info is current
- Not accounting for edge cases
- Trusting pattern matching too much
- Underestimating domain complexity

### Under-confidence
- Doubting well-established patterns
- Over-weighting unlikely failure modes
- Not trusting successful past experience
- Excessive hedging on straightforward tasks

## Templates Updated with Confidence

All templates in `/templates/` should end with the confidence block. Check:
- `templates/development/claude-code-handoff.md`
- `templates/prompting/system-prompt-template.md`
- `templates/voice-ai/receptionist-base.md`
