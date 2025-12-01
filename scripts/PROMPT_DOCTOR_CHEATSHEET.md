# Prompt Doctor - Quick Reference Card

## Installation
```bash
cd C:/Users/JRiel/prompt-engineering-system/scripts
# No dependencies needed - pure Python 3.6+
```

## Common Commands

### Basic Usage
```bash
# Diagnose a file
python prompt_doctor.py --diagnose prompt.txt

# Diagnose from stdin
echo "Write a story" | python prompt_doctor.py --diagnose -

# Get detailed analysis
python prompt_doctor.py --diagnose prompt.txt --verbose

# Get JSON output
python prompt_doctor.py --diagnose prompt.txt --json

# Auto-fix issues
python prompt_doctor.py --diagnose prompt.txt --fix

# Save fixed version
python prompt_doctor.py --diagnose prompt.txt --fix --output fixed.txt
```

### Pipeline Examples
```bash
# Check quality threshold
python prompt_doctor.py --diagnose prompt.txt --json | jq '.quality_score'

# Batch process
for file in prompts/*.txt; do
    python prompt_doctor.py --diagnose "$file"
done

# Quality gate
python prompt_doctor.py --diagnose prompt.txt
if [ $? -eq 0 ]; then echo "PASS"; else echo "FAIL"; fi
```

## Python API

### Basic
```python
from prompt_doctor import PromptDoctor

doctor = PromptDoctor()
result = doctor.diagnose_prompt("Your prompt here")

print(f"Quality: {result.quality_score}/100")
print(f"Health: {result.overall_health}")
```

### Access Issues
```python
for issue in result.issues:
    print(f"{issue.severity.value}: {issue.description}")
    print(f"Fix: {issue.suggestion}")
```

### Filter by Severity
```python
from prompt_doctor import Severity

high = [i for i in result.issues if i.severity == Severity.HIGH]
print(f"Critical issues: {len(high)}")
```

### Auto-Fix
```python
fixed = doctor.auto_fix(original_prompt, result)
print(fixed)
```

### JSON Export
```python
import json
print(json.dumps(result.to_dict(), indent=2))
```

## Scoring Guide

| Score | Health | Meaning |
|-------|--------|---------|
| 80-100 | EXCELLENT | Ready to use |
| 60-79 | GOOD | Minor improvements |
| 40-59 | FAIR | Needs work |
| 20-39 | POOR | Major revision |
| 0-19 | CRITICAL | Rewrite needed |

## Issue Severity

| Level | Meaning | Action |
|-------|---------|--------|
| HIGH | Critical | Fix immediately |
| MEDIUM | Important | Should fix |
| LOW | Minor | Nice to have |

## Common Issues & Quick Fixes

### "Vague verbs detected"
❌ `Handle the data`
✅ `Extract email addresses from CSV file`

### "No output format"
❌ `Analyze the results`
✅ `Analyze results and return JSON with: {summary, insights}`

### "No examples"
❌ `Convert timestamps`
✅ `Convert timestamps. Example: 1638360000 → Dec 1, 2021`

### "Multiple tasks"
❌ `Write story AND create characters AND develop plot`
✅ Split into 3 separate prompts

### "Ambiguous language"
❌ `Maybe write something good`
✅ `Write a 500-word article about AI`

## Prompt Template

```
Task: [Specific instruction with action verb]

Context:
- [Target audience]
- [Purpose/use case]
- [Background information]

Format:
- [Output structure]
- [Length requirements]
- [Style/tone]

Requirements:
- [Must-have elements]
- [Constraints]
- [What to avoid]

Example:
[Input/output demonstration]
```

## Exit Codes

| Code | Meaning | Score Range |
|------|---------|-------------|
| 0 | Good | 60-100 |
| 1 | Needs improvement | 40-59 |
| 2 | Critical issues | 0-39 |

## Dimension Scores

**Quality** = Weighted average
**Clarity** = Clear, unambiguous (30%)
**Specificity** = Detailed, precise (25%)
**Completeness** = All elements present (25%)
**Complexity** = Simple structure (20%, inverted)

## File Locations

```
scripts/
├── prompt_doctor.py              # Main tool (808 lines)
├── test_prompt_doctor.py         # Test suite
├── PROMPT_DOCTOR_README.md       # Full documentation
├── PROMPT_DOCTOR_SUMMARY.md      # Implementation summary
└── examples/
    ├── QUICK_START.md            # Getting started
    ├── ADVANCED_USAGE.md         # API & integrations
    ├── poor_prompt.txt           # Example: poor
    ├── fair_prompt.txt           # Example: fair
    └── excellent_prompt.txt      # Example: excellent
```

## Integration Snippets

### Pre-commit Hook
```bash
#!/bin/bash
python prompt_doctor.py --diagnose prompts/*.txt || exit 1
```

### Flask API
```python
@app.route('/diagnose', methods=['POST'])
def diagnose():
    result = doctor.diagnose_prompt(request.json['prompt'])
    return jsonify(result.to_dict())
```

### Quality Check Script
```python
def validate_prompt(prompt: str, min_score: float = 70):
    result = doctor.diagnose_prompt(prompt)
    if result.quality_score < min_score:
        raise ValueError(f"Quality too low: {result.quality_score}")
    return result
```

## Pattern Detection

**Vague Verbs**: handle, process, manage, deal with, improve, enhance, fix
**Ambiguous**: maybe, perhaps, possibly, might, could, somewhat
**Good Verbs**: extract, generate, transform, analyze, validate, create

## Tips

1. **Start Clear**: Use specific action verbs
2. **Add Format**: Always specify output structure
3. **Include Example**: At least one input/output pair
4. **Set Constraints**: Length, tone, requirements
5. **Provide Context**: Audience, purpose, background
6. **Keep Simple**: One main task per prompt
7. **Avoid Hedging**: No "maybe", "perhaps", "possibly"

## Troubleshooting

**Q: Low score on good prompt?**
A: Pattern matching may not catch domain terms. Check --verbose.

**Q: Unicode errors?**
A: Should auto-handle. If not, use --json output.

**Q: Slow on large files?**
A: Analysis is fast (< 100ms). Check file I/O.

## Help & Support

```bash
python prompt_doctor.py --help
python test_prompt_doctor.py  # See examples
```

## Quick Test

```bash
# Test installation
echo "Write a story" | python prompt_doctor.py --diagnose -

# Expected output: Shows diagnostic report with scores
```

---

**Version**: 1.0
**Location**: `C:/Users/JRiel/prompt-engineering-system/scripts/prompt_doctor.py`
**Dependencies**: None (Python 3.6+ stdlib only)
