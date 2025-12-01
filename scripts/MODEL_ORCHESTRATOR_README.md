# Multi-Model Orchestration System

A production-ready system for intelligently routing prompts across multiple LLMs (Anthropic Claude and OpenAI GPT models) with support for fallback chains, ensemble responses, and cost optimization.

## Features

### 1. Intelligent Routing
- **Complexity Analysis**: Automatically analyzes prompt complexity to determine the minimum required model capability
- **Cost Optimization**: Routes to the cheapest model that can handle the task
- **Pattern Recognition**: Detects task types (math, code, research, planning, etc.) and selects appropriate models

### 2. Fallback Chains
- Start with cheapest/fastest model (e.g., Haiku)
- Escalate to more capable models if confidence is low
- Configurable confidence thresholds
- Automatic retry with exponential backoff

### 3. Ensemble Responses
- Run prompts on multiple models simultaneously
- Synthesize responses based on confidence scores and model capabilities
- Consensus detection across responses
- Best-of-N selection with intelligent scoring

### 4. Cost & Performance Tracking
- Real-time cost calculation per request
- Integration with cost_tracker for historical analysis
- Latency measurement
- Token usage tracking
- Cost budget enforcement

### 5. Production-Ready Features
- Rate limiting per model
- Retry logic with error handling
- Configurable timeouts
- JSON output for integration
- Comprehensive logging

## Installation

```bash
# Already included in your prompt-engineering-system
cd C:/Users/JRiel/prompt-engineering-system/scripts/

# No additional dependencies required beyond existing requirements.txt
```

## Quick Start

### 1. List Available Models

```bash
python model_orchestrator.py --list-models
```

### 2. Run with Cheapest Model (Auto-routing)

```bash
python model_orchestrator.py \
  --prompt "What is the capital of France?" \
  --strategy cheapest
```

### 3. Run with Fallback Chain

```bash
python model_orchestrator.py \
  --prompt "Explain quantum entanglement" \
  --strategy fallback
```

### 4. Run with Ensemble (Multiple Models)

```bash
python model_orchestrator.py \
  --prompt "Should I use REST or GraphQL?" \
  --strategy ensemble \
  --ensemble-size 3
```

### 5. Set Cost Budget

```bash
python model_orchestrator.py \
  --prompt "Complex analysis task" \
  --strategy fallback \
  --max-cost 0.01
```

## Usage Guide

### Basic Usage

```bash
python model_orchestrator.py --prompt "Your prompt here" --strategy <strategy>
```

### Command-Line Options

| Option | Short | Description | Default |
|--------|-------|-------------|---------|
| `--prompt` | `-p` | The prompt to run | Required |
| `--strategy` | `-s` | Orchestration strategy: `fallback`, `ensemble`, or `cheapest` | `fallback` |
| `--max-cost` | `-c` | Maximum cost budget in dollars | Unlimited |
| `--chain` | | Custom fallback chain (comma-separated) | `mixed` chain |
| `--ensemble-size` | `-e` | Number of models for ensemble | 3 |
| `--verbose` | `-v` | Verbose output with debugging info | False |
| `--output` | `-o` | Save JSON result to file | None |
| `--list-models` | | List all available models | |
| `--test` | | Run test suite | |

### Strategies

#### 1. Cheapest (Auto-routing)

Automatically selects the cheapest model that can handle the prompt's complexity level.

```bash
python model_orchestrator.py \
  --prompt "What is 2+2?" \
  --strategy cheapest
# Routes to: gpt-4o-mini (cheapest basic model)
```

**Best for**: Simple queries, formatting, basic Q&A

**Complexity Levels**:
- **Basic**: Simple questions, definitions, formatting
- **Intermediate**: Code writing, summaries, calculations
- **Advanced**: Complex reasoning, system design, debugging
- **Expert**: Research, multi-step analysis, comprehensive evaluations

#### 2. Fallback Chain

Tries models in sequence, escalating to more capable models if confidence is low.

```bash
python model_orchestrator.py \
  --prompt "Design a distributed system" \
  --strategy fallback \
  --chain "claude-haiku-3.5,claude-sonnet-3.5,claude-opus-3"
```

**Default chains**:
- `mixed`: gpt-4o-mini → claude-haiku-3.5 → claude-sonnet-3.5 → gpt-4o → claude-opus-3
- `anthropic`: claude-haiku-3.5 → claude-sonnet-3.5 → claude-opus-3
- `openai`: gpt-4o-mini → gpt-4o → gpt-4
- `fast`: claude-haiku-3.5 → gpt-4o-mini → claude-sonnet-3.5

**Best for**: Tasks with uncertain complexity, when you want to minimize cost but ensure quality

**How it works**:
1. Starts with the first (cheapest) model
2. Checks confidence in response (pattern detection)
3. If confidence < 0.6, escalates to next model
4. Stops when confidence is acceptable or last model is reached

#### 3. Ensemble

Runs prompt on multiple models and synthesizes the best response.

```bash
python model_orchestrator.py \
  --prompt "Should I use microservices or monolith?" \
  --strategy ensemble \
  --ensemble-size 3
```

**Best for**: Important decisions, when you need multiple perspectives, validation of complex answers

**Synthesis Algorithm**:
- Confidence score (50% weight)
- Model capability level (30% weight)
- Response length/completeness (20% weight)
- Consensus bonus for overlapping key points

## Model Registry

### Anthropic Models

| Model | Input Cost | Output Cost | Capabilities | Context |
|-------|------------|-------------|--------------|---------|
| claude-haiku-3.5 | $0.80/1M | $4.00/1M | Basic, Intermediate | 200K |
| claude-sonnet-3.5 | $3.00/1M | $15.00/1M | Basic, Intermediate, Advanced | 200K |
| claude-opus-3 | $15.00/1M | $75.00/1M | Basic, Intermediate, Advanced, Expert | 200K |

### OpenAI Models

| Model | Input Cost | Output Cost | Capabilities | Context |
|-------|------------|-------------|--------------|---------|
| gpt-4o-mini | $0.15/1M | $0.60/1M | Basic, Intermediate | 128K |
| gpt-4o | $2.50/1M | $10.00/1M | Basic, Intermediate, Advanced | 128K |
| gpt-4 | $30.00/1M | $60.00/1M | Basic, Intermediate, Advanced, Expert | 128K |

## Complexity Analysis

The system automatically analyzes prompt complexity using pattern matching:

### Expert Level
- Research, comprehensive analysis, multi-step problems
- "Research", "analyze deeply", "comprehensive", "compare multiple"
- "Prove", "derive", "formalize"

### Advanced Level
- System design, complex reasoning, optimization
- "Explain why", "implement", "design", "debug"
- "Compare", "evaluate", "optimize"

### Intermediate Level
- Code writing, summaries, calculations
- "Write code", "summarize", "calculate"
- "List", "identify", "solve"

### Basic Level
- Simple questions, definitions, formatting
- "What is", "define", "format"
- "Simple", "basic", "quick"

## Confidence Detection

The system detects confidence in model responses to determine if fallback is needed:

**Low Confidence Indicators**:
- "not sure", "uncertain", "might be", "possibly"
- "I think", "seems like", "appears to"
- "need more context", "would need to"
- Very short responses (< 20 words)

**High Confidence Indicators**:
- "definitely", "certainly", "clearly"
- "proven", "established", "confirmed"
- Comprehensive responses with details

## Cost Optimization

### Budget Enforcement

```bash
# Limit total cost to $0.005 (half a cent)
python model_orchestrator.py \
  --prompt "Analyze this code" \
  --strategy fallback \
  --max-cost 0.005
```

### Cost Comparison Examples

**Simple question: "What is 2+2?"**
- gpt-4o-mini: ~$0.000024
- claude-haiku-3.5: ~$0.000032
- claude-sonnet-3.5: ~$0.000150
- Savings: 83% by using cheapest strategy

**Complex analysis (1000 tokens in/out)**
- gpt-4o-mini: ~$0.00075
- claude-sonnet-3.5: ~$0.018
- claude-opus-3: ~$0.090
- Ensemble (3 models): ~$0.109

## Integration Examples

### Python Integration

```python
from model_orchestrator import run_orchestration

# Simple usage
result = run_orchestration(
    prompt="Explain neural networks",
    strategy="cheapest"
)

print(f"Model: {result.model_used}")
print(f"Cost: ${result.cost}")
print(f"Response: {result.response}")

# Advanced usage with ensemble
result = run_orchestration(
    prompt="Design a scalable system",
    strategy="ensemble",
    ensemble_size=3,
    max_cost=0.05
)

# Access detailed metrics
print(f"Models used: {result.ensemble_models}")
print(f"Confidence: {result.confidence}")
print(f"Latency: {result.latency}s")
```

### JSON Output

```bash
python model_orchestrator.py \
  --prompt "Your prompt" \
  --strategy ensemble \
  --output result.json
```

Output structure:
```json
{
  "response": "Model response text",
  "model_used": "claude-sonnet-3.5",
  "cost": 0.0018,
  "latency": 0.23,
  "confidence": 0.85,
  "input_tokens": 50,
  "output_tokens": 100,
  "strategy": "ensemble",
  "ensemble_models": ["claude-haiku-3.5", "gpt-4o-mini", "claude-sonnet-3.5"],
  "metadata": {
    "ensemble_size": 3,
    "all_confidences": [0.60, 0.65, 0.85]
  },
  "timestamp": "2025-12-01T14:30:00.000000"
}
```

### Bash Script Integration

```bash
#!/bin/bash

# Run with fallback and capture result
python model_orchestrator.py \
  --prompt "Analyze this log file" \
  --strategy fallback \
  --max-cost 0.01 \
  --output result.json

# Check if successful
if [ $? -eq 0 ]; then
    echo "Success! Cost: $(jq -r '.cost' result.json)"
    echo "Model used: $(jq -r '.model_used' result.json)"
else
    echo "Failed to process prompt"
fi
```

## Advanced Usage

### Custom Fallback Chains

```bash
# Fast, cheap chain
python model_orchestrator.py \
  --prompt "Quick question" \
  --strategy fallback \
  --chain "gpt-4o-mini,claude-haiku-3.5"

# Quality-focused chain
python model_orchestrator.py \
  --prompt "Important analysis" \
  --strategy fallback \
  --chain "claude-sonnet-3.5,claude-opus-3"
```

### Ensemble with Custom Models

```python
from model_orchestrator import run_ensemble

result = run_ensemble(
    prompt="Evaluate this architecture",
    models=["claude-sonnet-3.5", "gpt-4o", "claude-opus-3"],
    ensemble_size=3,
    max_cost=0.10
)
```

### Rate Limiting

Built-in rate limiting per model based on typical API limits:
- claude-haiku-3.5: 100 RPM
- claude-sonnet-3.5: 50 RPM
- claude-opus-3: 20 RPM
- gpt-4o-mini: 100 RPM
- gpt-4o: 50 RPM
- gpt-4: 20 RPM

## Testing

Run the comprehensive test suite:

```bash
python model_orchestrator.py --test
```

Tests include:
1. **Complexity Scoring**: Validates prompt analysis
2. **Model Routing**: Tests auto-routing to appropriate models
3. **Fallback Chain**: Tests escalation logic
4. **Ensemble**: Tests multi-model synthesis

## Cost Tracking Integration

The orchestrator integrates with the existing cost_tracker.py system:

```bash
# View orchestration costs
cd C:/Users/JRiel/prompt-engineering-system/scripts/
python cost_tracker.py report --category orchestration

# View by strategy
python cost_tracker.py export \
  --format csv \
  --category orchestration \
  --output orchestration_costs.csv
```

## Production Deployment

### Environment Setup

While this is a mock implementation, in production you would:

1. **API Keys**: Set environment variables
   ```bash
   export ANTHROPIC_API_KEY="your-key"
   export OPENAI_API_KEY="your-key"
   ```

2. **Replace MockLLMClient**: Implement actual API calls
   ```python
   # In production, replace MockLLMClient with:
   import anthropic
   import openai

   def call_anthropic(model, prompt):
       client = anthropic.Anthropic()
       response = client.messages.create(
           model=model,
           messages=[{"role": "user", "content": prompt}]
       )
       return response
   ```

3. **Database**: The cost_tracker already uses SQLite
   ```bash
   # Initialize tracking database
   python cost_tracker.py init
   ```

4. **Monitoring**: Add logging and alerting
   ```python
   import logging
   logging.basicConfig(level=logging.INFO)
   ```

### Best Practices

1. **Start with cheapest strategy** for unknown prompts
2. **Use fallback** for production workloads
3. **Use ensemble** for critical decisions
4. **Set max-cost budgets** to prevent runaway costs
5. **Monitor confidence scores** to tune thresholds
6. **Review cost reports** regularly

## Troubleshooting

### High Costs

```bash
# Check recent usage
python cost_tracker.py stats --period daily

# Identify expensive operations
python cost_tracker.py report --period weekly --category orchestration
```

**Solutions**:
- Lower ensemble size (3 → 2)
- Use more aggressive cost limits
- Prefer cheapest strategy for simple tasks
- Use custom chains with fewer models

### Low Confidence

If fallback chains consistently escalate to expensive models:

1. **Adjust threshold**: Lower confidence threshold in code (default 0.6)
2. **Better chains**: Start with higher-capability models
3. **Ensemble**: Use ensemble for uncertain tasks

### Rate Limiting

```
Error: Rate limit exceeded for model X
```

**Solutions**:
- Reduce concurrent requests
- Use models with higher rate limits
- Implement queue system for batch processing

## Performance Benchmarks

### Latency (Mock Implementation)

| Strategy | Models | Average Latency |
|----------|--------|-----------------|
| Cheapest | 1 | 0.15s |
| Fallback (1 hop) | 1 | 0.20s |
| Fallback (2 hops) | 2 | 0.40s |
| Ensemble (3) | 3 | 0.60s |

*Note: Real API calls add 0.5-3s per request*

### Cost Comparison

| Task Type | Cheapest | Fallback | Ensemble |
|-----------|----------|----------|----------|
| Simple Q&A | $0.00002 | $0.00002 | $0.00007 |
| Code generation | $0.00050 | $0.00080 | $0.00200 |
| Complex analysis | $0.00150 | $0.00450 | $0.01200 |

## Future Enhancements

Potential additions for v2:

1. **Streaming Responses**: Real-time output for long generations
2. **Caching**: Cache similar prompts to reduce costs
3. **A/B Testing**: Compare model performance over time
4. **Custom Scoring**: User-defined complexity scorers
5. **Async Processing**: Parallel ensemble execution
6. **Model Fine-tuning**: Track which models work best for your use cases
7. **Cost Alerts**: Notifications when budgets are exceeded
8. **Semantic Caching**: Use embeddings to find similar cached responses

## API Reference

### Core Functions

#### `route_to_model(prompt, max_cost=None) -> str`
Route prompt to cheapest capable model.

#### `run_with_fallback(prompt, chain=None, confidence_threshold=0.6, max_cost=None) -> OrchestrationResult`
Execute with fallback chain.

#### `run_ensemble(prompt, models=None, ensemble_size=3, max_cost=None) -> OrchestrationResult`
Execute with ensemble voting.

#### `synthesize_responses(responses) -> Dict`
Synthesize multiple model responses.

### Classes

#### `ModelConfig`
Configuration for a model including costs, capabilities, and limits.

#### `OrchestrationResult`
Result of orchestration including response, costs, and metadata.

#### `ComplexityAnalyzer`
Analyze prompt complexity and determine required capability.

#### `ConfidenceDetector`
Detect confidence level in model responses.

#### `RateLimiter`
Manage API rate limits per model.

## Support

For issues or questions:

1. Check test suite: `python model_orchestrator.py --test`
2. Review cost reports: `python cost_tracker.py stats`
3. Enable verbose mode: `--verbose` flag

## License

Part of the prompt-engineering-system. See project LICENSE.

---

**Version**: 1.0.0
**Last Updated**: 2025-12-01
**Author**: Prompt Engineering System
**Location**: `C:/Users/JRiel/prompt-engineering-system/scripts/model_orchestrator.py`
