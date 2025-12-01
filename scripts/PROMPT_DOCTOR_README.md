# Prompt Doctor

A comprehensive diagnostic tool for analyzing and improving prompt quality across multiple dimensions.

## Features

- **Multi-Dimensional Analysis**: Evaluates clarity, specificity, completeness, and complexity
- **Pattern-Based Detection**: Identifies common anti-patterns and issues
- **Severity Scoring**: Categorizes issues as HIGH/MEDIUM/LOW priority
- **Actionable Feedback**: Provides specific, implementable suggestions
- **Auto-Fix Capability**: Basic automatic fixes for common issues
- **Multiple Output Formats**: Human-readable reports or JSON for automation

## Installation

No external dependencies required - uses only Python standard library.

```bash
# Make executable (Unix/Mac)
chmod +x prompt_doctor.py

# Or run with Python
python prompt_doctor.py --help
```

## Usage

### Basic Diagnosis

```bash
# Diagnose a prompt from file
python prompt_doctor.py --diagnose my_prompt.txt

# Diagnose from stdin
echo "Write a story" | python prompt_doctor.py --diagnose -

# With verbose output
python prompt_doctor.py --diagnose my_prompt.txt --verbose
```

### Auto-Fix Mode

```bash
# Show fixes in terminal
python prompt_doctor.py --diagnose my_prompt.txt --fix

# Save fixed version to file
python prompt_doctor.py --diagnose my_prompt.txt --fix --output fixed_prompt.txt
```

### JSON Output (for automation)

```bash
# Get machine-readable results
python prompt_doctor.py --diagnose my_prompt.txt --json

# Use in pipelines
python prompt_doctor.py --diagnose - --json < prompt.txt | jq '.quality_score'
```

## What It Checks

### 1. Clarity (30% weight)
- Vague verbs (handle, process, deal with)
- Ambiguous language (maybe, perhaps, might)
- Question-heavy prompts without instructions
- Clear goal statements

### 2. Specificity (25% weight)
- Prompt length and detail level
- Pronoun overuse
- Concrete vs abstract language
- Actionable instructions

### 3. Completeness (25% weight)
- Output format specification
- Examples and demonstrations
- Context and background
- Constraints and requirements

### 4. Complexity (20% weight, inverted)
- Sentence length and structure
- Multiple simultaneous tasks
- Nested conditional logic
- Overall readability

## Issue Types

| Type | Description | Example |
|------|-------------|---------|
| `VAGUE_INSTRUCTION` | Unclear or non-specific instructions | "Handle the data" |
| `MISSING_CONTEXT` | Lacks background information | No audience or purpose specified |
| `MISSING_FORMAT` | No output format specified | Doesn't say JSON, markdown, etc. |
| `MISSING_EXAMPLES` | No examples provided | Complex task without demonstration |
| `OVERLY_COMPLEX` | Too many tasks or conditions | Multiple goals in one prompt |
| `AMBIGUOUS_LANGUAGE` | Uncertain or hedging language | "Maybe write something" |
| `MISSING_CONSTRAINTS` | No requirements specified | No length, tone, or style limits |
| `UNCLEAR_GOAL` | Desired outcome not stated | Questions without clear ask |

## Severity Levels

- **HIGH**: Critical issues that will likely produce poor results
- **MEDIUM**: Important issues that should be addressed
- **LOW**: Minor improvements that would enhance quality

## Quality Scoring

### Overall Health Assessment
- **EXCELLENT** (80-100): Well-crafted prompt, ready to use
- **GOOD** (60-79): Solid prompt, minor improvements possible
- **FAIR** (40-59): Needs improvement in several areas
- **POOR** (20-39): Significant issues, major revision needed
- **CRITICAL** (0-19): Fundamental problems, complete rewrite recommended

### Exit Codes
- `0`: Good prompt (score >= 60)
- `1`: Needs improvement (score 40-59)
- `2`: Critical issues (score < 40)

## Examples

### Poor Prompt
```
Input: "Write something about dogs."

Output:
Overall Health: POOR (25.0/100)
Issues Found: 6 total (3 high, 2 medium, 1 low)

[HIGH] unclear_goal: Goal or desired outcome not clearly stated
  → Start with or include a clear statement of what you want as output

[HIGH] vague_instruction [overall]: Very short prompt (4 words)
  → Add more specific details about what you want, how you want it, and why

[MEDIUM] missing_format: No output format specification detected
  → Specify the desired output format (e.g., JSON, markdown, bullet points)
```

### Good Prompt
```
Input: "Generate a product description for an ergonomic wireless mouse.
Target: Office professionals. Length: 150-200 words. Format: 2 paragraphs
+ bullet points. Must highlight ergonomic benefits and battery life.
Example: 'Transform your workday with...' Tone: Professional but friendly."

Output:
Overall Health: EXCELLENT (87.5/100)
Issues Found: 0 total

No issues found! This is a well-structured prompt.
```

## API Usage

```python
from prompt_doctor import PromptDoctor, format_report

# Create doctor instance
doctor = PromptDoctor(verbose=False)

# Diagnose a prompt
result = doctor.diagnose_prompt("Write a story about robots")

# Access scores
print(f"Quality: {result.quality_score}")
print(f"Clarity: {result.clarity_score}")
print(f"Health: {result.overall_health}")

# Iterate through issues
for issue in result.issues:
    print(f"{issue.severity.value}: {issue.description}")
    print(f"Suggestion: {issue.suggestion}")

# Generate report
report = format_report(result, verbose=True)
print(report)

# Auto-fix
fixed_prompt = doctor.auto_fix(original_prompt, result)

# JSON export
import json
print(json.dumps(result.to_dict(), indent=2))
```

## Testing

Run the test suite to see examples across different quality levels:

```bash
python test_prompt_doctor.py
```

This will demonstrate:
- Poor prompts (vague, minimal)
- Fair prompts (basic but incomplete)
- Good prompts (clear with details)
- Excellent prompts (complete, well-structured)
- Complex prompts (too many tasks)
- Ambiguous prompts (unclear instructions)

## Best Practices

### Quick Prompt Template
Use this structure for consistently high-quality prompts:

```
Task: [Clear, specific instruction]

Context:
- [Background information]
- [Target audience]
- [Purpose/use case]

Format:
- [Desired output structure]
- [Length requirements]

Requirements:
- [Must-have elements]
- [Constraints]
- [What to avoid]

Example:
[Sample input/output]

Tone/Style:
- [Voice and style guidelines]
```

### Common Fixes

1. **Vague → Specific**
   - Before: "Handle the data"
   - After: "Extract email addresses from the CSV file"

2. **Missing Format → Clear Format**
   - Before: "Analyze the results"
   - After: "Analyze the results and provide JSON with keys: summary, insights, recommendations"

3. **Complex → Focused**
   - Before: "Write a story and create characters and develop plot and..."
   - After: [Separate prompts for each task]

4. **Ambiguous → Definitive**
   - Before: "Maybe write something fairly good"
   - After: "Write a 500-word article about..."

## Advanced Features (Coming Soon)

- **LLM-Powered Deep Analysis**: Use AI to provide sophisticated suggestions
- **Template Detection**: Identify and suggest appropriate prompt frameworks
- **A/B Comparison**: Compare multiple prompt versions
- **Benchmark Mode**: Test against known high-quality prompts
- **Custom Rule Sets**: Define organization-specific quality standards

## Contributing

To add new detection patterns:

1. Add pattern list to `PromptDoctor` class (e.g., `VAGUE_VERBS`)
2. Create or extend check method (e.g., `check_clarity()`)
3. Return `Issue` objects with appropriate type and severity
4. Update scoring calculations if needed

## License

MIT License - feel free to use and modify for your needs.

## Support

For issues, suggestions, or contributions, please open an issue in the repository.
