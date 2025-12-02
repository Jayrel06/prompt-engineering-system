# Prompt Improver - Quick Start Guide

## One Command to Rule Them All

```bash
python prompt_improver.py "your prompt here"
```

That's it! This ONE command automatically:
- Diagnoses issues in your prompt
- Identifies the best framework to use
- Applies proven best practices
- Generates optimized variations
- Shows you what changed and why

## 5 Common Use Cases

### 1. Quick Improvement (No API Needed)

```bash
python prompt_improver.py "Summarize this article" --no-api
```

Perfect for:
- Quick fixes
- Learning what's wrong with your prompt
- When you don't have an API key
- Fast iterations

### 2. Best Quality (With API)

```bash
python prompt_improver.py "Summarize this article"
```

Requires: ANTHROPIC_API_KEY or OPENAI_API_KEY environment variable

Perfect for:
- Production prompts
- Complex tasks
- Maximum quality
- Multiple variations to choose from

### 3. From File

```bash
python prompt_improver.py --file my_prompt.txt
```

Perfect for:
- Long prompts
- Version control
- Batch processing
- Team collaboration

### 4. For Automation (JSON Output)

```bash
python prompt_improver.py "your prompt" --json > result.json
```

Perfect for:
- CI/CD pipelines
- Automated testing
- Programmatic use
- Integration with other tools

### 5. Learn What's Wrong

```bash
python prompt_improver.py "your prompt" --verbose --no-api
```

Perfect for:
- Learning prompt engineering
- Understanding issues
- Seeing the improvement process
- Educational purposes

## Understanding the Output

### The Report Sections

1. **ORIGINAL PROMPT** - Your starting point
2. **DIAGNOSIS** - What's wrong (scores and issues)
3. **RECOMMENDED FRAMEWORK** - Best approach for your task
4. **BEST PRACTICES APPLIED** - What techniques were used
5. **IMPROVED PROMPT** - The result (copy and use this!)
6. **IMPROVEMENT METRICS** - How much better it is
7. **WHAT CHANGED AND WHY** - Explanation of changes
8. **ALTERNATIVE VARIATIONS** - Other options to consider

### Quality Scores

- **80-100**: EXCELLENT - Your prompt is great!
- **60-79**: GOOD - Minor improvements possible
- **40-59**: FAIR - Significant room for improvement
- **20-39**: POOR - Major issues to fix
- **0-19**: CRITICAL - Complete rewrite needed

## Common Options

```bash
# Verbose (see progress)
python prompt_improver.py "prompt" --verbose

# More variations
python prompt_improver.py "prompt" --num-variations 5

# Save result
python prompt_improver.py "prompt" --output improved.txt

# Use OpenAI instead of Anthropic
python prompt_improver.py "prompt" --provider openai

# Combine options
python prompt_improver.py "prompt" -v --json --num-variations 5
```

## Quick Troubleshooting

### Error: "Could not initialize optimizer"

**Solution:** Either:
1. Set your API key: `export ANTHROPIC_API_KEY="your-key"`
2. Or use rule-based mode: `--no-api`

### Slow Performance

**Solution:**
- Use fewer variations: `--num-variations 2`
- Or use rule-based mode: `--no-api` (instant)

### No Improvement Detected

**Congratulations!** Your prompt is already high quality (score >80).

## Examples

### Bad Prompt

```
Write something about AI
```

**Issues:**
- Vague ("something")
- No specificity ("about AI")
- No format
- No constraints
- No context

### Good Prompt (After Improvement)

```
Create a 300-word blog post about AI in healthcare.

Target Audience: Healthcare professionals with limited technical knowledge

Requirements:
- Focus on practical applications currently in use
- Include 2-3 specific examples
- Explain benefits and limitations
- Use accessible language (no heavy jargon)

Format:
- Opening hook (1 sentence)
- Main content (3 paragraphs)
- Conclusion with call-to-action (1 paragraph)

Tone: Professional but conversational
```

**Improvements:**
- Specific task and length
- Clear audience
- Detailed requirements
- Explicit format
- Defined tone
- Measurable criteria

## Best Practices

1. **Start with the tool** - Let it show you issues first
2. **Use --verbose** - Learn from the process
3. **Try both modes** - Compare rule-based vs API results
4. **Review variations** - Don't just accept the winner
5. **Test the result** - Always validate with real use
6. **Iterate** - Use improved prompt as input for further refinement
7. **Save versions** - Use --output to track changes

## Integration Examples

### Shell Script

```bash
#!/bin/bash
# improve_all_prompts.sh

for file in prompts/*.txt; do
    echo "Improving $file..."
    python prompt_improver.py --file "$file" --output "improved_$(basename $file)"
done
```

### Python Script

```python
from prompt_improver import PromptImprover

improver = PromptImprover(use_api=True)

prompts = [
    "Summarize this",
    "Extract emails",
    "Write code"
]

for prompt in prompts:
    result = improver.improve_prompt(prompt)
    print(f"Original: {result.original}")
    print(f"Improved: {result.improved}")
    print(f"Score: +{result.improvement_score:.1f}%")
    print("-" * 80)
```

### Git Hook (Pre-Commit)

```bash
#!/bin/bash
# .git/hooks/pre-commit

if git diff --cached --name-only | grep -q "prompts/"; then
    for file in $(git diff --cached --name-only | grep "prompts/"); do
        python prompt_improver.py --file "$file" --json > "${file}.analysis.json"
        git add "${file}.analysis.json"
    done
fi
```

## Keyboard Shortcuts (Bash)

Add to your `.bashrc` or `.zshrc`:

```bash
# Quick improve
alias improve='python ~/prompt-engineering-system/scripts/prompt_improver.py'

# Quick improve with verbose
alias improveq='python ~/prompt-engineering-system/scripts/prompt_improver.py --verbose --no-api'

# Improve from clipboard (macOS)
alias improveclip='pbpaste | python ~/prompt-engineering-system/scripts/prompt_improver.py'

# Improve and copy to clipboard (macOS)
alias improvecopy='python ~/prompt-engineering-system/scripts/prompt_improver.py "$1" --no-api | tail -n +50 | pbcopy'
```

Usage:
```bash
improve "your prompt"
improveq "your prompt"
improveclip
improvecopy "your prompt"
```

## When NOT to Use

- Your prompt is already scoring 90+ (diminishing returns)
- You need domain-specific expertise (tool is general-purpose)
- You're exploring creative/experimental approaches (tool optimizes for effectiveness)
- Your prompt is part of a larger system (consider full system context)

## Next Steps

1. Read the full README: `README_PROMPT_IMPROVER.md`
2. Learn individual tools: `prompt_doctor.py`, `prompt_router.py`, `prompt_optimizer.py`
3. Study best practices: `../context/technical/prompting-best-practices.md`
4. Explore frameworks: `../frameworks/`
5. Join the community: Share your improvements!

## Cheat Sheet

```bash
# Basic
python prompt_improver.py "prompt"

# From file
python prompt_improver.py --file prompt.txt

# No API (free)
python prompt_improver.py "prompt" --no-api

# More variations
python prompt_improver.py "prompt" -n 5

# JSON output
python prompt_improver.py "prompt" --json

# Save result
python prompt_improver.py "prompt" -o improved.txt

# Verbose
python prompt_improver.py "prompt" -v

# Full power
python prompt_improver.py "prompt" -v --json -n 5 -o result.json
```

## Remember

**The goal isn't perfect prompts - it's BETTER prompts.**

Even a 20% improvement can mean:
- Faster responses
- More accurate results
- Fewer retries needed
- Better consistency
- Lower costs

Start improving your prompts today with ONE simple command:

```bash
python prompt_improver.py "your prompt here"
```

Happy prompting!
