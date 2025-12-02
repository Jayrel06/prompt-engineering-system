# Unified Prompt Improver

**The ONE command to automatically improve any prompt.**

## Overview

`prompt_improver.py` is the single entry point that automatically chains together all prompt improvement tools:

1. **Diagnose** - Identifies issues using `prompt_doctor.py`
2. **Route** - Finds the best framework using `prompt_router.py`
3. **Apply Best Practices** - Loads relevant guidance from `prompting-best-practices.md`
4. **Optimize** - Generates improved variations using `prompt_optimizer.py`
5. **Report** - Returns comprehensive before/after comparison with explanations

## Quick Start

```bash
# Basic usage - improve any prompt
python prompt_improver.py "Write a summary of this article"

# From file
python prompt_improver.py --file prompt.txt

# Save improved version
python prompt_improver.py "your prompt" --output improved.txt

# JSON output for automation
python prompt_improver.py "your prompt" --json
```

## Features

### Automatic Everything

- No need to run multiple tools separately
- Automatic issue detection and diagnosis
- Automatic framework selection
- Automatic best practices application
- Automatic variation generation (with API)
- Comprehensive before/after reporting

### Two Modes

**1. API-Based Mode (Recommended)**
- Requires Anthropic or OpenAI API key
- Generates multiple optimized variations
- Uses LLM to apply sophisticated improvements
- Provides quality scores and rankings

**2. Rule-Based Mode (Fallback)**
- Works without API keys
- Uses pattern matching and rules
- Applies structural improvements
- Good for basic fixes

### Smart Integration

- Handles tool failures gracefully
- Falls back to rule-based if API unavailable
- Works even if individual tools are missing
- Clear error messages and warnings

## Installation

```bash
# Install dependencies
pip install anthropic  # For Anthropic API
# OR
pip install openai     # For OpenAI API

# Set API key (optional, for API mode)
export ANTHROPIC_API_KEY="your-key-here"
# OR
export OPENAI_API_KEY="your-key-here"
```

## Usage

### Basic Commands

```bash
# Simple improvement (rule-based, no API needed)
python prompt_improver.py "Analyze this data" --no-api

# With API (generates better variations)
python prompt_improver.py "Analyze this data"

# Read from file
python prompt_improver.py --file my_prompt.txt

# Verbose mode (shows progress)
python prompt_improver.py "prompt" --verbose

# Generate more variations (default: 3)
python prompt_improver.py "prompt" --num-variations 5
```

### Output Options

```bash
# Human-readable report (default)
python prompt_improver.py "prompt"

# JSON output for scripts
python prompt_improver.py "prompt" --json

# Save improved prompt to file
python prompt_improver.py "prompt" --output improved.txt

# Both JSON and file
python prompt_improver.py "prompt" --json --output result.json
```

### Advanced Options

```bash
# Just diagnose and route (no fixes)
python prompt_improver.py "prompt" --no-fix

# Use OpenAI instead of Anthropic
python prompt_improver.py "prompt" --provider openai

# Specific model
python prompt_improver.py "prompt" --model claude-opus-4-20250514

# Combine options
python prompt_improver.py "prompt" --verbose --json --num-variations 5 --output result.json
```

## Output Structure

### Human-Readable Report

```
================================================================================
PROMPT IMPROVEMENT REPORT
================================================================================

ORIGINAL PROMPT:
--------------------------------------------------------------------------------
[Your original prompt]

DIAGNOSIS:
--------------------------------------------------------------------------------
Quality Score: 45/100
Health Status: FAIR
Issues Found: 5
  [HIGH] unclear_goal: Goal or desired outcome not clearly stated
  [MEDIUM] missing_format: No output format specification detected
  ...

RECOMMENDED FRAMEWORK:
--------------------------------------------------------------------------------
chain-of-thought
Techniques: zero-shot-cot, step-by-step

BEST PRACTICES APPLIED:
--------------------------------------------------------------------------------
  - Increased specificity and detail
  - Added concrete examples
  - Improved structure and organization
  - Added clear constraints

IMPROVED PROMPT:
--------------------------------------------------------------------------------
[Your improved prompt]

IMPROVEMENT METRICS:
--------------------------------------------------------------------------------
Improvement Score: 67.5%

WHAT CHANGED AND WHY:
--------------------------------------------------------------------------------
Generated 3 optimized variations
Winner technique: structured
Quality score improved from 4.5 to 7.6
Addressed 5 identified issues

ALTERNATIVE VARIATIONS (2 more):
--------------------------------------------------------------------------------
1. with_examples (Score: 7.2/10)
   [Preview of variation...]

2. role_based (Score: 6.9/10)
   [Preview of variation...]
```

### JSON Output

```json
{
  "original": "Write a summary",
  "improved": "[Improved prompt]",
  "diagnosis": {
    "quality_score": 45.0,
    "overall_health": "FAIR",
    "issues": [...]
  },
  "framework_used": "chain-of-thought",
  "techniques_applied": ["structured", "zero-shot-cot"],
  "improvement_score": 67.5,
  "explanation": "Generated 3 optimized variations...",
  "all_variations": [...],
  "best_practices_applied": [...],
  "metadata": {
    "mode": "api_based",
    "provider": "anthropic",
    "model": "claude-sonnet-4-20250514"
  },
  "timestamp": "2025-12-02T10:00:00"
}
```

## ImprovementResult Object

The core data structure returned by `improve_prompt()`:

```python
@dataclass
class ImprovementResult:
    original: str                          # Original prompt
    improved: str                          # Best improved version
    diagnosis: Optional[Dict[str, Any]]    # Diagnostic results
    framework_used: Optional[str]          # Recommended framework
    techniques_applied: List[str]          # Techniques used
    improvement_score: float               # Percentage improvement
    explanation: str                       # What changed and why
    all_variations: List[Dict]             # All generated variations
    best_practices_applied: List[str]      # Best practices used
    metadata: Dict[str, Any]               # Additional info
    timestamp: str                         # ISO timestamp
```

## Python API

Use programmatically in your own scripts:

```python
from prompt_improver import PromptImprover, ImprovementResult

# Initialize
improver = PromptImprover(
    use_api=True,              # Use API mode (requires key)
    provider="anthropic",      # or "openai"
    model=None,                # Auto-select model
    verbose=False
)

# Improve a prompt
result: ImprovementResult = improver.improve_prompt(
    prompt="Analyze this data",
    auto_fix=True,             # Apply automatic fixes
    num_variations=3,          # Number of variations
    verbose=False
)

# Access results
print(f"Original: {result.original}")
print(f"Improved: {result.improved}")
print(f"Score: {result.improvement_score}%")
print(f"Techniques: {result.techniques_applied}")

# Get as dict for JSON
result_dict = result.to_dict()

# Get as formatted report
report = result.format_report()
print(report)
```

## Examples

### Example 1: Simple Prompt

**Input:**
```
Summarize this
```

**Output (Rule-Based):**
```
Task: Summarize this

Format: Please provide output in a clear, structured format.

Constraints:
- [Define boundaries and requirements]
```

**Techniques Applied:**
- Add format specification
- Add constraints
- Lead with task

### Example 2: Code Request

**Input:**
```
Write code to process files
```

**Output (API-Based):**
```
You are an expert Python developer. Create a Python script that processes files
with the following requirements:

Task: Write a file processing utility

Requirements:
- Accept file path as command-line argument
- Read file contents safely
- Process each line
- Handle errors gracefully
- Output results to console

Format: Provide complete, runnable Python code with:
- Proper error handling
- Clear comments
- Example usage

Example Input: data.txt
Example Output: Processed 42 lines successfully

Constraints:
- Use Python 3.8+ features
- Follow PEP 8 style
- Include docstrings
```

**Techniques Applied:**
- Role-based prompting
- Structured format
- Added examples
- Defined constraints
- Specified output format

### Example 3: Complex Analysis

**Input:**
```
What are the pros and cons?
```

**Output (API-Based):**
```
Analyze the pros and cons of [subject] using this structure:

Step 1: Identify key aspects to evaluate
Step 2: List advantages with supporting evidence
Step 3: List disadvantages with supporting evidence
Step 4: Provide balanced conclusion

Format:
**Pros:**
- [Pro 1]: [Evidence and reasoning]
- [Pro 2]: [Evidence and reasoning]

**Cons:**
- [Con 1]: [Evidence and reasoning]
- [Con 2]: [Evidence and reasoning]

**Conclusion:**
[Balanced assessment considering all factors]

Requirements:
- Minimum 3 pros and 3 cons
- Cite specific evidence
- Consider multiple perspectives
- Acknowledge limitations
```

**Techniques Applied:**
- Step-by-step reasoning
- Structured format
- Explicit requirements
- Context provision
- Clear delimiters

## Integration with Other Tools

### With prompt_doctor.py

```bash
# Just diagnose (no improvements)
python prompt_doctor.py --diagnose prompt.txt

# Diagnose AND improve
python prompt_improver.py --file prompt.txt
```

### With prompt_router.py

```bash
# Just route (framework recommendation)
python prompt_router.py "Analyze this data"

# Route AND improve
python prompt_improver.py "Analyze this data"
```

### With prompt_optimizer.py

```bash
# Just optimize (needs API)
python prompt_optimizer.py --prompt "Summarize this" --num-variations 5

# Full pipeline (diagnose, route, optimize)
python prompt_improver.py "Summarize this" --num-variations 5
```

## Exit Codes

- `0` - Success with good improvement
- `1` - Success with minimal improvement
- `2` - Degradation (rare)

## Troubleshooting

### "Could not import prompt_doctor"

**Solution:** Tools are in the same directory, this should auto-resolve. Check that all scripts are present.

### "Could not initialize optimizer"

**Cause:** Missing API key or package

**Solution:**
```bash
# Install package
pip install anthropic  # or openai

# Set API key
export ANTHROPIC_API_KEY="your-key"

# Or use rule-based mode
python prompt_improver.py "prompt" --no-api
```

### "No improvement detected"

**Cause:** Prompt is already high quality

**Solution:** Check the diagnosis section - if quality score is >80, your prompt is already good!

### Slow performance

**Cause:** API calls take time with multiple variations

**Solution:**
```bash
# Reduce variations
python prompt_improver.py "prompt" --num-variations 2

# Or use rule-based mode (instant)
python prompt_improver.py "prompt" --no-api
```

## Best Practices for Using the Tool

1. **Start Simple**: Begin with default settings
2. **Use Rule-Based First**: Test without API to see structural issues
3. **Then Use API**: Get sophisticated improvements with API mode
4. **Compare Variations**: Review all variations, not just winner
5. **Iterate**: Use improved prompt as input for further refinement
6. **Save Results**: Use `--output` to track versions
7. **Test Results**: Always test improved prompts with real use cases

## Configuration

### Environment Variables

```bash
# API Keys (for API mode)
export ANTHROPIC_API_KEY="sk-ant-..."
export OPENAI_API_KEY="sk-..."

# Default provider (optional)
export PROMPT_IMPROVER_PROVIDER="anthropic"

# Default model (optional)
export PROMPT_IMPROVER_MODEL="claude-sonnet-4-20250514"
```

### Config File (Future)

Create `~/.prompt_improver/config.json`:

```json
{
  "provider": "anthropic",
  "model": "claude-sonnet-4-20250514",
  "default_variations": 3,
  "verbose": false,
  "use_api": true
}
```

## Performance

### Speed

| Mode | Speed | Quality |
|------|-------|---------|
| Rule-Based | Instant | Good |
| API (3 variations) | 15-30s | Excellent |
| API (5 variations) | 30-60s | Excellent |

### Cost

| Provider | Model | Cost per improvement (3 variations) |
|----------|-------|-------------------------------------|
| Anthropic | Claude Sonnet 4 | ~$0.02-0.05 |
| Anthropic | Claude Haiku | ~$0.001-0.01 |
| OpenAI | GPT-4 | ~$0.05-0.10 |
| Rule-Based | N/A | $0.00 (free) |

## Comparison with Individual Tools

| Feature | prompt_doctor | prompt_router | prompt_optimizer | prompt_improver |
|---------|--------------|---------------|------------------|-----------------|
| Diagnose Issues | ✓ | - | - | ✓ |
| Route Framework | - | ✓ | - | ✓ |
| Generate Variations | - | - | ✓ | ✓ |
| Apply Best Practices | - | - | - | ✓ |
| Works Without API | ✓ | ✓ | - | ✓ |
| Comprehensive Report | - | - | - | ✓ |
| Single Command | - | - | - | ✓ |

## Roadmap

- [ ] Support for custom best practices files
- [ ] Interactive mode with feedback loops
- [ ] Support for prompt libraries/templates
- [ ] Batch processing of multiple prompts
- [ ] Web UI interface
- [ ] Prompt version history tracking
- [ ] A/B testing integration
- [ ] Custom evaluation criteria
- [ ] Export to prompt management platforms

## Contributing

To add new improvement techniques:

1. Add technique to `OptimizationTechnique` enum
2. Implement in `prompt_optimizer.py`
3. Map in `prompt_improver.py` technique_mapping
4. Update documentation

## License

Same as parent project.

## Support

Issues? Check:
1. This README
2. Individual tool READMEs
3. Best practices guide: `context/technical/prompting-best-practices.md`
4. GitHub issues

## Summary

**Use `prompt_improver.py` as your ONE command for all prompt improvements.**

```bash
# That's it - one command does everything
python prompt_improver.py "your prompt here"
```

No need to remember multiple tools or run multiple commands. It automatically:
- Diagnoses issues
- Selects the best framework
- Applies best practices
- Generates optimized variations
- Shows you exactly what changed and why

**Simple. Powerful. Automatic.**
