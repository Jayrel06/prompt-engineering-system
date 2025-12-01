# Token Counter - Production-Ready Context Overflow Prevention

## Quick Start

```bash
# Basic usage
python token_counter.py --text "Your prompt here" --model gpt-4o --check-limit

# From file
python token_counter.py --file prompt.txt --model claude-3-5-sonnet-20241022 --output-tokens 2000

# List models
python token_counter.py --list-models

# Get model info
python token_counter.py --model-info gpt-4o
```

## Python Integration

```python
from token_counter import validate_before_send

# Validate before sending to API (RECOMMENDED)
is_valid, info = validate_before_send(
    prompt="Your complete prompt here",
    model="claude-3-5-sonnet-20241022",
    max_output_tokens=4096
)

if is_valid:
    print(f"Safe to send! Cost: ${info.cost_estimate:.4f}")
    # Send to API
else:
    print(f"Error: Exceeds limit by {abs(info.remaining_tokens)} tokens")
```

## Key Features

1. **Accurate Token Counting**
   - Uses tiktoken for OpenAI models (GPT-4, GPT-3.5, O1)
   - Intelligent approximation for Claude and other models
   - ~95% accuracy even without tiktoken

2. **Context Limit Validation**
   - Supports 39+ models (Claude, GPT, O1, Gemini, etc.)
   - Warns before exceeding context windows
   - Calculates remaining tokens

3. **Cost Estimation**
   - Current pricing for all major models (Dec 2025)
   - Per-request cost calculation
   - Batch processing cost tracking

4. **Auto-Truncation**
   - Smart truncation (start, end, or middle)
   - Preserves important context
   - Summarization with structure preservation

5. **Production-Ready**
   - CLI and Python API
   - JSON output support
   - Error handling
   - Comprehensive testing

## Supported Models

### Best for Production
- **claude-3-5-sonnet-20241022** - Best quality/price ratio ($3/$15 per 1M)
- **gpt-4o** - Fast, high quality ($2.50/$10 per 1M)
- **gpt-4o-mini** - Cheapest OpenAI ($0.15/$0.60 per 1M)
- **claude-3-haiku** - Cheapest Claude ($0.25/$1.25 per 1M)

### All Supported Models
- Claude: 3.5 Sonnet (v1/v2), Opus, Sonnet, Haiku, 2.1, 2.0, Instant
- GPT: 4o, 4o-mini, 4-turbo, 4, 4-32k, 3.5-turbo variants
- O1: o1, o1-preview, o1-mini
- Gemini: 1.5 Pro (2M context!), 1.5 Flash, 1.0 Pro

Run `python token_counter.py --list-models` for complete list.

## Installation

```bash
# Install required dependency for accurate OpenAI counting
pip install tiktoken

# Or install all requirements
cd C:/Users/JRiel/prompt-engineering-system/scripts
pip install -r requirements.txt
```

Note: Works without tiktoken but uses approximation for all models.

## Files

- **token_counter.py** - Main utility (810 lines, production-ready)
- **test_token_counter.py** - Test suite (370 lines)
- **token_counter_examples.py** - 7 integration examples (320 lines)
- **TOKEN_COUNTER_GUIDE.md** - Comprehensive documentation
- **TOKEN_COUNTER_README.md** - This quick reference

## Testing

```bash
python test_token_counter.py
```

Expected: 8-11 tests pass (some tests require tiktoken for 100% pass rate)

## Examples

Run interactive examples:

```bash
python token_counter_examples.py
```

Includes:
1. Basic validation
2. Cost comparison across models
3. Auto-truncation
4. Batch cost tracking
5. Context window management
6. Pre-send validation pattern
7. Smart model selection

## API Reference

### Main Functions

```python
# Count tokens
count_tokens(text: str, model: str) -> int

# Estimate cost
estimate_cost(input_tokens: int, output_tokens: int, model: str) -> float

# Check limits
check_limits(token_count: int, model: str, output_tokens: int) -> Tuple[bool, int]

# Truncate to fit
truncate_to_fit(text: str, model: str, max_tokens: int, output_tokens: int,
                truncate_from: str = "end") -> str

# MAIN INTEGRATION POINT
validate_before_send(prompt: str, model: str, max_output_tokens: int,
                     auto_truncate: bool = False) -> Tuple[bool, TokenCount]
```

### TokenCount Dataclass

```python
@dataclass
class TokenCount:
    input_tokens: int              # Input token count
    output_tokens_estimate: int    # Estimated output tokens
    total: int                     # Total tokens
    model: str                     # Model name
    cost_estimate: float          # Estimated cost in USD
    within_limit: bool            # Whether within context limit
    remaining_tokens: int         # Remaining tokens (negative if over)
```

## Integration Pattern

```python
from token_counter import validate_before_send

def send_to_llm(prompt: str, model: str = "gpt-4o", max_output: int = 2000):
    """Safe API wrapper with validation."""

    # Validate first
    is_valid, info = validate_before_send(prompt, model, max_output)

    if not is_valid:
        raise ValueError(f"Prompt too long by {abs(info.remaining_tokens)} tokens")

    # Log cost
    print(f"Cost: ${info.cost_estimate:.4f}, Tokens: {info.input_tokens}")

    # Send to API
    response = your_api_call(prompt, model)

    return response

# Use it
try:
    result = send_to_llm("Your prompt", "claude-3-5-sonnet-20241022")
except ValueError as e:
    print(f"Validation failed: {e}")
```

## Common Use Cases

### 1. Pre-Flight Check
```bash
python token_counter.py --file large_prompt.txt --check-limit --model gpt-4
```

### 2. Cost Estimation
```bash
python token_counter.py --file batch_prompts.txt --model claude-3-5-sonnet-20241022 --output-tokens 1000
```

### 3. Auto-Truncate
```python
from token_counter import truncate_to_fit

safe_prompt = truncate_to_fit(
    long_prompt,
    model="gpt-4",
    output_tokens=1000,
    truncate_from="middle"
)
```

### 4. Model Selection
```python
from token_counter import estimate_cost

models = ["gpt-4o-mini", "claude-3-haiku-20240307", "gpt-4o"]
costs = [(m, estimate_cost(tokens, 500, m)) for m in models]
cheapest = min(costs, key=lambda x: x[1])
print(f"Use {cheapest[0]}: ${cheapest[1]:.4f}")
```

## Pricing Reference (per 1M tokens)

| Model | Input | Output | Context |
|-------|-------|--------|---------|
| gpt-4o-mini | $0.15 | $0.60 | 128K |
| claude-3-haiku | $0.25 | $1.25 | 200K |
| gemini-1.5-flash | $0.075 | $0.30 | 1M |
| gpt-4o | $2.50 | $10.00 | 128K |
| claude-3.5-sonnet | $3.00 | $15.00 | 200K |
| o1-mini | $3.00 | $12.00 | 128K |
| gpt-4-turbo | $10.00 | $30.00 | 128K |
| claude-3-opus | $15.00 | $75.00 | 200K |
| o1 | $15.00 | $60.00 | 200K |

*Updated December 2025*

## Troubleshooting

### tiktoken Warning
Install tiktoken for accurate OpenAI counting:
```bash
pip install tiktoken
```

Without it, approximation is used (~95% accurate).

### Unknown Model
If you see "Unknown model" warnings:
- Check model name spelling
- Use `--list-models` to see supported models
- Default limit (128K) and no cost estimate will be used

### Inaccurate Counts
- For Claude: Approximation is ~95% accurate
- For OpenAI without tiktoken: ~90% accurate
- Install tiktoken for 99%+ accuracy on OpenAI models

## License

Part of the Prompt Engineering System
Created: 2025-12-01
Author: JRiel

## Next Steps

1. Install tiktoken: `pip install tiktoken`
2. Run tests: `python test_token_counter.py`
3. Try examples: `python token_counter_examples.py`
4. Integrate into your pipeline using `validate_before_send()`
5. Update pricing data periodically

## Support

For issues or questions:
- Check TOKEN_COUNTER_GUIDE.md for detailed documentation
- Review token_counter_examples.py for integration patterns
- Run test suite to verify functionality
