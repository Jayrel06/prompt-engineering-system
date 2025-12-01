# Prompt Doctor - Quick Start Guide

## Installation & Setup

```bash
# No installation needed - just Python 3.6+
cd C:/Users/JRiel/prompt-engineering-system/scripts

# Make sure it works
python prompt_doctor.py --help
```

## Quick Examples

### 1. Test with Provided Examples

```bash
# Diagnose a poor prompt
python prompt_doctor.py --diagnose examples/poor_prompt.txt

# Diagnose a fair prompt
python prompt_doctor.py --diagnose examples/fair_prompt.txt

# Diagnose an excellent prompt
python prompt_doctor.py --diagnose examples/excellent_prompt.txt
```

### 2. Run Full Test Suite

```bash
python test_prompt_doctor.py
```

This will show you 6 different prompt quality levels with detailed analysis.

### 3. Try Your Own Prompts

```bash
# From a file
echo "Write a story about robots" > my_prompt.txt
python prompt_doctor.py --diagnose my_prompt.txt

# From command line
echo "Summarize the document" | python prompt_doctor.py --diagnose -

# Get auto-fix suggestions
python prompt_doctor.py --diagnose my_prompt.txt --fix
```

### 4. Get JSON Output

```bash
# For automation/scripting
python prompt_doctor.py --diagnose examples/poor_prompt.txt --json
```

## Understanding the Output

### Scores (0-100)

- **Quality Score**: Overall prompt health (weighted average)
- **Clarity Score**: How clear and unambiguous the instructions are
- **Specificity Score**: Level of detail and precision
- **Completeness Score**: Presence of format, examples, constraints
- **Complexity Score**: Structural complexity (lower is better)

### Health Ratings

- **EXCELLENT (80-100)**: Ready to use, well-crafted
- **GOOD (60-79)**: Minor tweaks could improve it
- **FAIR (40-59)**: Several improvements needed
- **POOR (20-39)**: Major revision required
- **CRITICAL (0-19)**: Complete rewrite recommended

### Issue Severity

- **HIGH**: Fix immediately - will significantly impact results
- **MEDIUM**: Should fix - noticeable improvement
- **LOW**: Nice to have - minor enhancement

## Common Issues & Fixes

### Issue: "Vague verbs detected"
```
❌ "Handle the customer data"
✅ "Extract email addresses from the customer CSV file"
```

### Issue: "No output format specification"
```
❌ "Analyze the sales data"
✅ "Analyze the sales data and return JSON with keys: total_revenue, top_products, growth_rate"
```

### Issue: "No examples provided for complex prompt"
```
❌ "Convert timestamps to readable dates"
✅ "Convert timestamps to readable dates
Example: 1638360000 → December 1, 2021, 10:00 AM EST"
```

### Issue: "Multiple distinct tasks detected"
```
❌ "Write a story AND create character profiles AND generate dialogue AND develop plot outline"
✅ Split into 4 separate prompts, one per task
```

### Issue: "Ambiguous language detected"
```
❌ "Maybe write something that could possibly be good"
✅ "Write a 300-word article about renewable energy"
```

## Pro Tips

### 1. Use the Template Structure
```
Task: [What you want]
Context: [Why/who/where]
Format: [How you want it]
Requirements: [Must-haves]
Example: [Show don't tell]
```

### 2. Be Specific with Verbs
- Vague: handle, process, deal with, manage
- Specific: extract, transform, generate, analyze, validate

### 3. Always Specify Format
- JSON with schema
- Markdown with structure
- Bullet points vs paragraphs
- Table with columns

### 4. Include at Least One Example
- Shows expected input/output
- Clarifies edge cases
- Demonstrates format

### 5. Add Constraints
- Length limits
- Tone/style requirements
- What to avoid
- Required elements

## Integration Examples

### Python Script
```python
from prompt_doctor import PromptDoctor

doctor = PromptDoctor()
result = doctor.diagnose_prompt(user_prompt)

if result.quality_score < 50:
    print("Please improve your prompt:")
    for suggestion in result.suggestions:
        print(f"- {suggestion}")
```

### Shell Script
```bash
#!/bin/bash
quality=$(python prompt_doctor.py --diagnose prompt.txt --json | jq '.quality_score')

if (( $(echo "$quality < 60" | bc -l) )); then
    echo "Prompt quality too low: $quality/100"
    exit 1
fi
```

### Pre-commit Hook
```bash
# .git/hooks/pre-commit
for file in prompts/*.txt; do
    python prompt_doctor.py --diagnose "$file" --json > /dev/null || {
        echo "Prompt quality check failed for $file"
        exit 1
    }
done
```

## Troubleshooting

### "ImportError: No module named..."
- No external dependencies needed
- Just requires Python 3.6+

### "FileNotFoundError"
- Check file path is correct
- Use absolute paths if relative paths fail

### Low Score on Good Prompt
- Tool uses pattern matching
- Some domain-specific prompts may score lower
- Use --verbose to see specific issues

## Next Steps

1. Try the test suite: `python test_prompt_doctor.py`
2. Analyze your existing prompts
3. Use --fix to get improvement suggestions
4. Integrate into your workflow
5. Track quality scores over time

## Quick Reference Card

```
Common Commands:
  --diagnose FILE       Analyze prompt file
  --fix                 Show auto-fix suggestions
  --output FILE         Save fixed prompt
  --json                JSON output
  --verbose             Detailed analysis

Exit Codes:
  0   Good (score >= 60)
  1   Fair (score 40-59)
  2   Poor (score < 40)

File Location:
  C:/Users/JRiel/prompt-engineering-system/scripts/prompt_doctor.py
```
