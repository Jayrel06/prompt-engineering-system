# Prompt Engineering System - Complete Overview

## The Unified System

This system provides a complete toolkit for prompt engineering, with **one unified entry point** that chains everything together automatically.

## The Tools

### 1. prompt_improver.py - THE ONE COMMAND

**The single entry point for all prompt improvements.**

```bash
python prompt_improver.py "your prompt here"
```

**What it does:**
- Automatically diagnoses issues
- Routes to best framework
- Applies best practices
- Generates optimized variations
- Provides comprehensive report

**When to use:**
- Always! This should be your default command
- Quick improvements (--no-api for instant results)
- Production optimization (with API for best quality)
- Learning what's wrong with prompts
- Automated workflows (--json output)

**Key features:**
- Works with or without API
- Graceful degradation
- Clear explanations
- Multiple output formats
- Programmatic API

---

### 2. prompt_doctor.py - The Diagnostician

**Analyzes prompts to identify issues.**

```bash
python prompt_doctor.py --diagnose prompt.txt
```

**What it does:**
- Detects vague instructions
- Finds missing elements
- Calculates quality scores
- Suggests specific fixes

**When to use:**
- When you want ONLY diagnosis (no fixes)
- Learning what makes a good prompt
- Debugging specific issues
- Quality auditing

**Integrated into:** prompt_improver.py (Step 1)

---

### 3. prompt_router.py - The Navigator

**Routes tasks to optimal frameworks.**

```bash
python prompt_router.py "Analyze this data"
```

**What it does:**
- Identifies task type
- Recommends framework
- Suggests techniques
- Recommends model

**When to use:**
- When you want ONLY framework recommendation
- Exploring different approaches
- Learning frameworks
- Strategic planning

**Integrated into:** prompt_improver.py (Step 2)

---

### 4. prompt_optimizer.py - The Enhancer

**Generates and tests variations.**

```bash
python prompt_optimizer.py --prompt "Summarize this" --num-variations 5
```

**What it does:**
- Generates multiple variations
- Applies different techniques
- Scores and ranks results
- A/B testing support

**When to use:**
- When you want ONLY variations (no diagnosis)
- Experimenting with techniques
- A/B testing prompts
- Building prompt libraries

**Integrated into:** prompt_improver.py (Step 4)

---

## The Workflow

### Manual Workflow (Using Individual Tools)

```bash
# Step 1: Diagnose
python prompt_doctor.py --diagnose prompt.txt

# Step 2: Route
python prompt_router.py "$(cat prompt.txt)"

# Step 3: Optimize
python prompt_optimizer.py --prompt "$(cat prompt.txt)" --num-variations 5

# Step 4: Review best practices
cat ../context/technical/prompting-best-practices.md

# Step 5: Apply learnings manually
```

### Automated Workflow (Using Unified Tool)

```bash
# One command does everything
python prompt_improver.py --file prompt.txt
```

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│                  prompt_improver.py                      │
│              (Unified Entry Point)                       │
└────────────────────┬────────────────────────────────────┘
                     │
          ┌──────────┼──────────┐
          │          │          │
          ▼          ▼          ▼
┌──────────────┐ ┌──────────────┐ ┌──────────────┐
│prompt_doctor │ │prompt_router │ │prompt_optimizer│
│  (Diagnose)  │ │  (Route)     │ │  (Optimize)  │
└──────────────┘ └──────────────┘ └──────────────┘
          │          │          │
          └──────────┼──────────┘
                     │
                     ▼
        ┌────────────────────────┐
        │   Best Practices       │
        │   (Knowledge Base)     │
        └────────────────────────┘
```

## Comparison Matrix

| Feature | doctor | router | optimizer | **improver** |
|---------|--------|--------|-----------|--------------|
| Diagnose Issues | ✓ | - | - | **✓** |
| Framework Selection | - | ✓ | - | **✓** |
| Generate Variations | - | - | ✓ | **✓** |
| Apply Best Practices | - | - | - | **✓** |
| Comprehensive Report | - | - | - | **✓** |
| Works Without API | ✓ | ✓ | - | **✓** |
| JSON Output | ✓ | ✓ | - | **✓** |
| File I/O | ✓ | - | - | **✓** |
| Verbose Mode | ✓ | - | ✓ | **✓** |
| Single Command | - | - | - | **✓** |
| Auto-Chain Tools | - | - | - | **✓** |
| Graceful Fallback | - | - | - | **✓** |
| **BEST FOR** | Auditing | Planning | Testing | **Everything** |

## Usage Recommendations

### For Daily Use

```bash
# Default: Use the unified tool
python prompt_improver.py "your prompt"
```

### For Learning

```bash
# Use verbose mode to see the process
python prompt_improver.py "your prompt" --verbose --no-api
```

### For Production

```bash
# Use API mode for best quality
python prompt_improver.py "your prompt" --num-variations 5
```

### For Automation

```bash
# JSON output for scripts
python prompt_improver.py "your prompt" --json
```

### For Deep Dive

```bash
# Use individual tools when you need specific insights
python prompt_doctor.py --diagnose prompt.txt --verbose
python prompt_router.py "$(cat prompt.txt)"
python prompt_optimizer.py --prompt "$(cat prompt.txt)" --num-variations 5
```

## File Structure

```
prompt-engineering-system/
├── scripts/
│   ├── prompt_improver.py           # ⭐ THE ONE COMMAND
│   ├── prompt_doctor.py             # Diagnosis tool
│   ├── prompt_router.py             # Routing tool
│   ├── prompt_optimizer.py          # Optimization tool
│   ├── README_PROMPT_IMPROVER.md    # Full documentation
│   ├── QUICK_START_IMPROVER.md      # Quick guide
│   └── SYSTEM_OVERVIEW.md           # This file
├── context/
│   └── technical/
│       └── prompting-best-practices.md  # Knowledge base
└── frameworks/
    └── [various framework definitions]
```

## Dependencies

### Core (No API)
- Python 3.8+
- Standard library only

### API Mode
- `anthropic` package (for Claude)
- OR `openai` package (for GPT)

### Installation

```bash
# For API mode (choose one)
pip install anthropic
# OR
pip install openai

# Set API key
export ANTHROPIC_API_KEY="your-key"
# OR
export OPENAI_API_KEY="your-key"
```

## Performance Comparison

### Speed

| Tool | Mode | Time | Quality |
|------|------|------|---------|
| prompt_doctor | - | <1s | Diagnostic |
| prompt_router | - | <1s | Advisory |
| prompt_optimizer | API | 30-60s | High |
| **prompt_improver** | **Rule-based** | **<2s** | **Good** |
| **prompt_improver** | **API** | **30-60s** | **Excellent** |

### Cost (API Mode)

| Provider | Model | Cost per Run |
|----------|-------|--------------|
| Anthropic | Haiku | ~$0.001 |
| Anthropic | Sonnet 4 | ~$0.02-0.05 |
| OpenAI | GPT-4 | ~$0.05-0.10 |
| **Rule-based** | **N/A** | **$0.00** |

## Common Workflows

### Workflow 1: Quick Fix

```bash
# Fast, free, good enough
python prompt_improver.py "prompt" --no-api
```

### Workflow 2: Production Optimization

```bash
# Slower, costs money, excellent quality
python prompt_improver.py "prompt" --num-variations 5
```

### Workflow 3: Batch Processing

```bash
# Process multiple prompts
for file in prompts/*.txt; do
    python prompt_improver.py --file "$file" --output "improved_$file"
done
```

### Workflow 4: CI/CD Integration

```bash
# Automated testing
python prompt_improver.py --file prompt.txt --json > result.json
python validate_quality.py result.json  # Your validation script
```

### Workflow 5: Learning & Exploration

```bash
# Understand what makes prompts better
python prompt_improver.py "prompt" --verbose --no-api
python prompt_doctor.py --diagnose improved_prompt.txt
```

## Exit Codes

All tools use consistent exit codes:

- `0` - Success
- `1` - Warning or needs improvement
- `2` - Critical issues

## Error Handling

The system handles errors gracefully:

1. **Missing tool** - Warning, continues with available tools
2. **API failure** - Falls back to rule-based mode
3. **Invalid input** - Clear error message, exits cleanly
4. **File not found** - Helpful suggestion

## Best Practices

1. **Start with unified tool** - `prompt_improver.py` should be your default
2. **Use --verbose** - Learn from the process
3. **Test both modes** - Compare rule-based vs API results
4. **Review all variations** - Don't blindly accept winner
5. **Iterate** - Use output as input for refinement
6. **Version control** - Track prompt changes over time
7. **Measure results** - Test improved prompts in production

## Integration Examples

### Shell Function

```bash
# Add to ~/.bashrc or ~/.zshrc
improve() {
    python ~/prompt-engineering-system/scripts/prompt_improver.py "$@"
}

# Usage
improve "your prompt"
improve --file prompt.txt
improve "prompt" --json
```

### Python Library

```python
from prompt_improver import PromptImprover

improver = PromptImprover(use_api=True)
result = improver.improve_prompt("your prompt")
print(result.improved)
```

### API Endpoint (Future)

```bash
curl -X POST http://localhost:8000/improve \
  -H "Content-Type: application/json" \
  -d '{"prompt": "your prompt", "use_api": true}'
```

## Roadmap

### v1.1 (Current)
- ✓ Unified entry point
- ✓ Rule-based mode
- ✓ API mode
- ✓ JSON output
- ✓ File I/O

### v1.2 (Planned)
- [ ] Batch processing
- [ ] Interactive mode
- [ ] Custom best practices
- [ ] Template library

### v2.0 (Future)
- [ ] Web UI
- [ ] API server
- [ ] Prompt versioning
- [ ] A/B testing framework
- [ ] Analytics dashboard

## Support & Resources

### Documentation
- **Quick Start**: `QUICK_START_IMPROVER.md`
- **Full Guide**: `README_PROMPT_IMPROVER.md`
- **This Overview**: `SYSTEM_OVERVIEW.md`
- **Best Practices**: `../context/technical/prompting-best-practices.md`

### Individual Tools
- `python prompt_doctor.py --help`
- `python prompt_router.py --help`
- `python prompt_optimizer.py --help`
- `python prompt_improver.py --help`

### Examples
See documentation for 20+ real-world examples

## Philosophy

### Design Principles

1. **Simplicity** - One command should do everything
2. **Flexibility** - Individual tools for specific needs
3. **Resilience** - Graceful degradation when things fail
4. **Transparency** - Always explain what changed and why
5. **Pragmatism** - Rule-based fallback when API unavailable

### The Improver Advantage

Instead of:
```bash
python prompt_doctor.py --diagnose prompt.txt
python prompt_router.py "$(cat prompt.txt)"
python prompt_optimizer.py --prompt "$(cat prompt.txt)"
# Review output, apply fixes manually...
```

Just do:
```bash
python prompt_improver.py --file prompt.txt
```

**Less typing. More improving. Better results.**

## Summary

- **USE**: `prompt_improver.py` for 95% of use cases
- **USE**: Individual tools when you need specific functionality
- **USE**: `--no-api` for fast, free improvements
- **USE**: API mode for production-quality optimization
- **USE**: `--verbose` to learn and understand
- **USE**: `--json` for automation and integration

## The Bottom Line

You now have ONE command that does EVERYTHING:

```bash
python prompt_improver.py "your prompt here"
```

It's that simple. No need to remember multiple tools or run multiple commands.

**Start improving your prompts today!**
