# Model Orchestrator - Quick Reference

## Overview

The Model Orchestrator is a production-ready system for intelligently routing LLM requests across multiple models with automatic cost optimization, fallback chains, and ensemble voting.

**Location**: `C:/Users/JRiel/prompt-engineering-system/scripts/model_orchestrator.py`

## Quick Commands

```bash
# List models
python model_orchestrator.py --list-models

# Auto-route to cheapest model
python model_orchestrator.py --prompt "Your prompt" --strategy cheapest

# Fallback chain (escalate if needed)
python model_orchestrator.py --prompt "Your prompt" --strategy fallback

# Ensemble (multiple models)
python model_orchestrator.py --prompt "Your prompt" --strategy ensemble --ensemble-size 3

# With cost limit
python model_orchestrator.py --prompt "Your prompt" --strategy fallback --max-cost 0.01

# Run tests
python model_orchestrator.py --test

# View costs
python cost_tracker.py report --category orchestration
```

## Three Strategies

### 1. Cheapest (Auto-routing)
**Use when**: You want minimum cost for unknown complexity
- Analyzes prompt complexity automatically
- Routes to cheapest model that can handle it
- Best for: Simple Q&A, formatting, basic tasks

**Example**:
```bash
python model_orchestrator.py --prompt "What is 2+2?" --strategy cheapest
# Routes to: gpt-4o-mini ($0.000024)
```

### 2. Fallback Chain
**Use when**: You want to minimize cost but ensure quality
- Starts with cheapest model
- Escalates to more capable models if confidence < 0.6
- Best for: Production workloads, uncertain complexity

**Example**:
```bash
python model_orchestrator.py --prompt "Explain quantum physics" --strategy fallback
# Tries: gpt-4o-mini → claude-haiku-3.5 → claude-sonnet-3.5 (stops when confident)
```

### 3. Ensemble
**Use when**: You need validation or multiple perspectives
- Runs on 2-3 models simultaneously
- Synthesizes best response
- Best for: Important decisions, validation

**Example**:
```bash
python model_orchestrator.py --prompt "Should I use REST or GraphQL?" --strategy ensemble
# Runs on: claude-haiku-3.5, gpt-4o-mini, claude-sonnet-3.5
# Selects best based on confidence + capability
```

## Model Costs (per 1M tokens)

| Model | Input | Output | Best For |
|-------|-------|--------|----------|
| gpt-4o-mini | $0.15 | $0.60 | Cheapest, basic tasks |
| claude-haiku-3.5 | $0.80 | $4.00 | Fast, intermediate |
| gpt-4o | $2.50 | $10.00 | Balanced performance |
| claude-sonnet-3.5 | $3.00 | $15.00 | Advanced reasoning |
| claude-opus-3 | $15.00 | $75.00 | Expert analysis |
| gpt-4 | $30.00 | $60.00 | Complex tasks |

## Complexity Detection

The system automatically detects task complexity:

- **Basic**: "What is...", "Define...", "Format..." → gpt-4o-mini
- **Intermediate**: "Explain...", "Write code..." → claude-haiku-3.5
- **Advanced**: "Design system...", "Analyze..." → claude-sonnet-3.5
- **Expert**: "Research...", "Comprehensive analysis..." → claude-opus-3

## Cost Examples

### Simple Query
```bash
python model_orchestrator.py --prompt "What is Python?" --strategy cheapest
```
- Model: gpt-4o-mini
- Cost: ~$0.000024
- Time: 0.2s

### Code Generation
```bash
python model_orchestrator.py --prompt "Write a binary search function" --strategy fallback
```
- Model: claude-haiku-3.5 (first try) or claude-sonnet-3.5 (if escalated)
- Cost: ~$0.000080 - $0.000150
- Time: 0.2-0.4s

### Complex Analysis
```bash
python model_orchestrator.py --prompt "Design distributed architecture" --strategy ensemble
```
- Models: 3 models (haiku, mini, sonnet)
- Cost: ~$0.001200
- Time: 0.6s

## Budget Control

```bash
# Set hard limit
python model_orchestrator.py \
  --prompt "Your prompt" \
  --strategy fallback \
  --max-cost 0.005

# System will:
# 1. Stop if cost exceeds budget
# 2. Skip expensive models in chain
# 3. Error if no model fits budget
```

## Integration

### Python
```python
from model_orchestrator import run_orchestration

result = run_orchestration(
    prompt="Explain Docker",
    strategy="cheapest"
)

print(f"Cost: ${result.cost}")
print(f"Model: {result.model_used}")
print(f"Response: {result.response}")
```

### Bash
```bash
#!/bin/bash
python model_orchestrator.py \
  --prompt "Analyze logs" \
  --strategy fallback \
  --output result.json

cost=$(jq -r '.cost' result.json)
echo "Analysis cost: \$$cost"
```

## Output Format

```json
{
  "response": "Model response here...",
  "model_used": "claude-sonnet-3.5",
  "cost": 0.0018,
  "latency": 0.23,
  "confidence": 0.85,
  "input_tokens": 50,
  "output_tokens": 100,
  "strategy": "ensemble",
  "fallback_chain": ["gpt-4o-mini", "claude-haiku-3.5", "claude-sonnet-3.5"],
  "ensemble_models": ["claude-haiku-3.5", "gpt-4o-mini", "claude-sonnet-3.5"],
  "metadata": {
    "ensemble_size": 3
  },
  "timestamp": "2025-12-01T14:30:00"
}
```

## Custom Chains

```bash
# Fast chain (cheap models only)
python model_orchestrator.py \
  --prompt "Quick question" \
  --strategy fallback \
  --chain "gpt-4o-mini,claude-haiku-3.5"

# Quality chain (skip cheap models)
python model_orchestrator.py \
  --prompt "Important analysis" \
  --strategy fallback \
  --chain "claude-sonnet-3.5,claude-opus-3"

# OpenAI only
python model_orchestrator.py \
  --prompt "Your prompt" \
  --strategy fallback \
  --chain "gpt-4o-mini,gpt-4o,gpt-4"

# Anthropic only
python model_orchestrator.py \
  --prompt "Your prompt" \
  --strategy fallback \
  --chain "claude-haiku-3.5,claude-sonnet-3.5,claude-opus-3"
```

## Cost Tracking

View orchestration statistics:

```bash
# Daily stats
python cost_tracker.py stats --period daily

# Monthly report with orchestration filter
python cost_tracker.py report --category orchestration --period monthly

# Export to CSV
python cost_tracker.py export --format csv --category orchestration --output orch_costs.csv
```

## Common Patterns

### Pattern 1: Development Workflow
```bash
# Quick exploration (cheapest)
python model_orchestrator.py --prompt "How does X work?" --strategy cheapest

# Detailed investigation (fallback)
python model_orchestrator.py --prompt "Design X system" --strategy fallback

# Critical decision (ensemble)
python model_orchestrator.py --prompt "Should we use X or Y?" --strategy ensemble
```

### Pattern 2: Cost-Conscious Pipeline
```bash
# Step 1: Quick classification (cheap)
python model_orchestrator.py \
  --prompt "Classify: $INPUT" \
  --strategy cheapest \
  --output step1.json

# Step 2: Detailed analysis (budget-limited fallback)
python model_orchestrator.py \
  --prompt "Analyze: $INPUT" \
  --strategy fallback \
  --max-cost 0.005 \
  --output step2.json
```

### Pattern 3: Quality Validation
```bash
# Generate with single model
python model_orchestrator.py \
  --prompt "Write documentation for $CODE" \
  --strategy cheapest \
  --output draft.json

# Validate with ensemble
python model_orchestrator.py \
  --prompt "Review this documentation: $(cat draft.json)" \
  --strategy ensemble \
  --output final.json
```

## Troubleshooting

### Problem: Costs too high
**Solution**:
```bash
# Use cheapest strategy
python model_orchestrator.py --prompt "..." --strategy cheapest

# Set budget limit
python model_orchestrator.py --prompt "..." --strategy fallback --max-cost 0.01

# Use smaller ensemble
python model_orchestrator.py --prompt "..." --strategy ensemble --ensemble-size 2
```

### Problem: Low confidence responses
**Solution**:
```bash
# Use fallback (auto-escalates)
python model_orchestrator.py --prompt "..." --strategy fallback

# Use ensemble for validation
python model_orchestrator.py --prompt "..." --strategy ensemble

# Start with better model in custom chain
python model_orchestrator.py --prompt "..." --strategy fallback --chain "claude-sonnet-3.5,claude-opus-3"
```

### Problem: Rate limiting
**Solution**:
- Built-in rate limiter automatically waits
- Reduce concurrent requests
- Use models with higher limits (haiku, gpt-4o-mini)

## Best Practices

1. **Start with cheapest** for new tasks
2. **Use fallback** for production
3. **Reserve ensemble** for critical decisions
4. **Set budgets** on all production calls
5. **Monitor costs** regularly with cost_tracker
6. **Custom chains** for specific domains
7. **Test first** with `--test` flag

## Performance Characteristics

| Strategy | Latency | Cost | Reliability |
|----------|---------|------|-------------|
| Cheapest | 0.15s | $ | Medium |
| Fallback (1 hop) | 0.20s | $$ | High |
| Fallback (2 hops) | 0.40s | $$$ | Very High |
| Ensemble | 0.60s | $$$$ | Highest |

## Files

- **Main Script**: `model_orchestrator.py`
- **Documentation**: `MODEL_ORCHESTRATOR_README.md`
- **Examples**: `model_orchestrator_examples.sh`
- **This File**: `MODEL_ORCHESTRATOR_SUMMARY.md`

## Testing

```bash
# Run full test suite
python model_orchestrator.py --test

# Tests include:
# - Complexity scoring
# - Model routing
# - Fallback chains
# - Ensemble synthesis
```

## Next Steps

1. Read full documentation: `MODEL_ORCHESTRATOR_README.md`
2. Run examples: `./model_orchestrator_examples.sh`
3. Run tests: `python model_orchestrator.py --test`
4. Try on your prompts: `python model_orchestrator.py --prompt "..."`

---

**Quick Links**:
- Full docs: `MODEL_ORCHESTRATOR_README.md`
- Cost tracker: `cost_tracker.py`
- Integration: Import functions from `model_orchestrator.py`
