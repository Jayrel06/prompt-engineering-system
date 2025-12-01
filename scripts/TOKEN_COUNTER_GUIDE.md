# Token Counter and Context Overflow Prevention Guide

## Overview

The `token_counter.py` utility provides accurate token counting, cost estimation, and context limit validation for various LLM models. It's designed to integrate seamlessly with your prompt engineering pipeline to prevent context overflow errors and manage API costs.

## Installation

```bash
# Install required dependencies
pip install tiktoken

# Or install all requirements
cd C:/Users/JRiel/prompt-engineering-system/scripts
pip install -r requirements.txt
```

## Quick Start

### Command Line Usage

```bash
# Count tokens in text
python token_counter.py --text "Hello, world!" --model gpt-4

# Count tokens in a file
python token_counter.py --file prompt.txt --model claude-3-5-sonnet-20241022

# Check if prompt fits within context limits
python token_counter.py --file large_prompt.txt --check-limit --output-tokens 2000

# Get cost estimate
python token_counter.py --text "Your prompt here" --model gpt-4o --output-tokens 1000

# Show truncated version if over limit
python token_counter.py --file large.txt --check-limit --truncate --model gpt-4

# List all supported models
python token_counter.py --list-models

# Get model information
python token_counter.py --model-info claude-3-5-sonnet-20241022

# Output as JSON
python token_counter.py --text "Hello" --model gpt-4 --json
```

### Python API Usage

```python
from token_counter import (
    count_tokens,
    estimate_cost,
    check_limits,
    validate_before_send,
    truncate_to_fit,
    summarize_to_fit,
    get_model_info
)

# Count tokens
tokens = count_tokens("Your text here", model="gpt-4o")
print(f"Token count: {tokens}")

# Estimate cost
cost = estimate_cost(
    input_tokens=10000,
    output_tokens=2000,
    model="claude-3-5-sonnet-20241022"
)
print(f"Estimated cost: ${cost:.4f}")

# Check limits
within_limit, remaining = check_limits(
    token_count=5000,
    model="gpt-4",
    output_tokens=1000
)
print(f"Within limit: {within_limit}, Remaining: {remaining}")

# Validate before sending (RECOMMENDED)
prompt = "Your complete prompt here..."
is_valid, info = validate_before_send(
    prompt=prompt,
    model="claude-3-5-sonnet-20241022",
    max_output_tokens=4096
)

if not is_valid:
    print(f"⚠️ Warning: Prompt exceeds limit by {abs(info.remaining_tokens)} tokens!")
    print(f"Cost would be: ${info.cost_estimate:.4f}")
else:
    print(f"✓ Prompt is valid. Cost: ${info.cost_estimate:.4f}")
    # Safe to send to API
```

## Integration with Prompt Assembly Pipeline

### Example 1: Basic Integration

```python
from token_counter import validate_before_send

def assemble_and_validate_prompt(system_msg, user_msg, context="", model="gpt-4o"):
    """Assemble prompt and validate before sending."""

    # Assemble full prompt
    full_prompt = f"{system_msg}\n\n{context}\n\nUser: {user_msg}\n\nAssistant:"

    # Validate
    is_valid, info = validate_before_send(
        prompt=full_prompt,
        model=model,
        max_output_tokens=2000
    )

    if not is_valid:
        print(f"⚠️ Warning: Prompt too long!")
        print(f"  Input tokens: {info.input_tokens}")
        print(f"  Over limit by: {abs(info.remaining_tokens)} tokens")
        return None

    print(f"✓ Prompt validated")
    print(f"  Tokens: {info.input_tokens}")
    print(f"  Estimated cost: ${info.cost_estimate:.4f}")

    return full_prompt

# Usage
prompt = assemble_and_validate_prompt(
    system_msg="You are a helpful assistant.",
    user_msg="Explain quantum physics.",
    model="gpt-4o"
)

if prompt:
    # Send to API
    pass
```

### Example 2: Auto-Truncation

```python
from token_counter import validate_before_send, truncate_to_fit

def safe_prompt_assembly(system_msg, user_msg, context="", model="gpt-4"):
    """Assemble prompt with auto-truncation if needed."""

    # Assemble
    full_prompt = f"{system_msg}\n\n{context}\n\nUser: {user_msg}\n\nAssistant:"

    # Validate with auto-truncate
    is_valid, info = validate_before_send(
        prompt=full_prompt,
        model=model,
        max_output_tokens=1000,
        auto_truncate=True,
        truncate_from="middle"  # Keep beginning and end
    )

    if not info.within_limit:
        # Context was too large, truncate it
        truncated = truncate_to_fit(
            full_prompt,
            model=model,
            output_tokens=1000,
            truncate_from="middle"
        )
        print(f"⚠️ Context truncated from {info.input_tokens} to ~{count_tokens(truncated, model)} tokens")
        return truncated

    return full_prompt
```

### Example 3: Cost Budgeting

```python
from token_counter import validate_before_send, estimate_cost

class CostBudgetedPromptManager:
    """Manage prompts with cost budgeting."""

    def __init__(self, max_cost_per_request=0.10):
        self.max_cost_per_request = max_cost_per_request
        self.total_spent = 0.0

    def validate_and_send(self, prompt, model="gpt-4o", max_output=2000):
        """Validate prompt against cost budget."""

        is_valid, info = validate_before_send(
            prompt=prompt,
            model=model,
            max_output_tokens=max_output
        )

        if not is_valid:
            raise ValueError(f"Prompt exceeds context limit by {abs(info.remaining_tokens)} tokens")

        if info.cost_estimate > self.max_cost_per_request:
            raise ValueError(
                f"Cost ${info.cost_estimate:.4f} exceeds budget "
                f"${self.max_cost_per_request:.4f}"
            )

        print(f"✓ Validated. Cost: ${info.cost_estimate:.4f}")
        self.total_spent += info.cost_estimate

        return prompt

    def get_total_spent(self):
        return self.total_spent

# Usage
manager = CostBudgetedPromptManager(max_cost_per_request=0.05)

try:
    prompt = manager.validate_and_send(
        "Your prompt here",
        model="gpt-4o-mini",  # Use cheaper model
        max_output=1000
    )
    # Send to API
except ValueError as e:
    print(f"Error: {e}")
```

### Example 4: Batch Processing with Cost Tracking

```python
from token_counter import count_tokens, estimate_cost
from typing import List, Dict

def batch_process_with_cost_tracking(
    prompts: List[str],
    model: str = "claude-3-5-sonnet-20241022",
    max_output_per_prompt: int = 1000
) -> Dict:
    """Process multiple prompts with cost tracking."""

    results = {
        'total_input_tokens': 0,
        'total_output_tokens': 0,
        'total_cost': 0.0,
        'prompts': []
    }

    for i, prompt in enumerate(prompts):
        input_tokens = count_tokens(prompt, model)
        cost = estimate_cost(input_tokens, max_output_per_prompt, model)

        results['total_input_tokens'] += input_tokens
        results['total_output_tokens'] += max_output_per_prompt
        results['total_cost'] += cost

        results['prompts'].append({
            'index': i,
            'input_tokens': input_tokens,
            'estimated_output_tokens': max_output_per_prompt,
            'estimated_cost': cost
        })

        print(f"Prompt {i+1}: {input_tokens} tokens, ${cost:.4f}")

    print(f"\nTotal estimated cost: ${results['total_cost']:.4f}")
    return results

# Usage
prompts = [
    "Explain AI",
    "What is machine learning?",
    "Describe neural networks"
]

summary = batch_process_with_cost_tracking(prompts, model="gpt-4o-mini")
```

### Example 5: Smart Context Window Management

```python
from token_counter import count_tokens, check_limits, truncate_to_fit

class ContextWindowManager:
    """Manage context window with conversation history."""

    def __init__(self, model="claude-3-5-sonnet-20241022", max_output=4000):
        self.model = model
        self.max_output = max_output
        self.conversation_history = []

    def add_message(self, role: str, content: str):
        """Add message to conversation history."""
        self.conversation_history.append({"role": role, "content": content})

    def get_prompt_with_history(self, system_prompt: str) -> str:
        """Get full prompt with as much history as fits."""

        # Start with system prompt and latest message
        latest_msg = self.conversation_history[-1]
        base_prompt = f"{system_prompt}\n\n{latest_msg['role']}: {latest_msg['content']}"

        base_tokens = count_tokens(base_prompt, self.model)

        # Check if we can fit history
        within_limit, remaining = check_limits(
            base_tokens,
            self.model,
            self.max_output
        )

        if not within_limit:
            # Even base prompt is too long, truncate it
            return truncate_to_fit(
                base_prompt,
                model=self.model,
                output_tokens=self.max_output
            )

        # Add history messages from most recent to oldest
        full_prompt = base_prompt
        for msg in reversed(self.conversation_history[:-1]):
            msg_text = f"\n\n{msg['role']}: {msg['content']}"
            test_prompt = msg_text + full_prompt

            test_tokens = count_tokens(test_prompt, self.model)
            within_limit, _ = check_limits(test_tokens, self.model, self.max_output)

            if within_limit:
                full_prompt = test_prompt
            else:
                break

        return full_prompt

# Usage
manager = ContextWindowManager(model="gpt-4", max_output=2000)
manager.add_message("user", "Hello!")
manager.add_message("assistant", "Hi! How can I help?")
manager.add_message("user", "Tell me about Python")

prompt = manager.get_prompt_with_history("You are a helpful coding assistant.")
print(f"Generated prompt with history:\n{prompt}")
```

## Supported Models

### Claude Models (Anthropic)
- `claude-3-5-sonnet-20241022` - 200K context, $3/$15 per 1M tokens (latest)
- `claude-3-opus-20240229` - 200K context, $15/$75 per 1M tokens
- `claude-3-sonnet-20240229` - 200K context, $3/$15 per 1M tokens
- `claude-3-haiku-20240307` - 200K context, $0.25/$1.25 per 1M tokens

### GPT Models (OpenAI)
- `gpt-4o` - 128K context, $2.50/$10 per 1M tokens
- `gpt-4o-mini` - 128K context, $0.15/$0.60 per 1M tokens
- `gpt-4-turbo` - 128K context, $10/$30 per 1M tokens
- `gpt-4` - 8K context, $30/$60 per 1M tokens

### O1 Models (OpenAI)
- `o1` - 200K context, $15/$60 per 1M tokens
- `o1-mini` - 128K context, $3/$12 per 1M tokens

### Gemini Models (Google)
- `gemini-1.5-pro` - 2M context, $1.25/$5 per 1M tokens
- `gemini-1.5-flash` - 1M context, $0.075/$0.30 per 1M tokens

See full list with: `python token_counter.py --list-models`

## API Reference

### Core Functions

#### `count_tokens(text: str, model: str) -> int`
Count tokens in text for a specific model.

#### `estimate_cost(input_tokens: int, output_tokens: int, model: str) -> float`
Estimate cost based on token counts.

#### `check_limits(token_count: int, model: str, output_tokens: int) -> Tuple[bool, int]`
Check if token count is within model limits. Returns (within_limit, remaining_tokens).

#### `truncate_to_fit(text: str, model: str, max_tokens: Optional[int], output_tokens: int, truncate_from: str) -> str`
Truncate text to fit within limits. `truncate_from` can be "end", "start", or "middle".

#### `summarize_to_fit(text: str, model: str, max_tokens: Optional[int], output_tokens: int) -> str`
Intelligently reduce text size while preserving structure and key information.

#### `validate_before_send(prompt: str, model: str, max_output_tokens: int, auto_truncate: bool, truncate_from: str) -> Tuple[bool, TokenCount]`
**Main integration function.** Validate prompt before sending to API. Returns (is_valid, token_info).

### Data Classes

#### `TokenCount`
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

### Helper Functions

#### `get_model_info(model: str) -> Dict`
Get comprehensive information about a model.

#### `list_supported_models() -> List[str]`
Get list of all supported models.

## Best Practices

1. **Always validate before sending**: Use `validate_before_send()` in production code to prevent API errors.

2. **Budget for output tokens**: Always reserve tokens for the expected output length.

3. **Use auto-truncate carefully**: When using auto-truncate, ensure truncation doesn't remove critical context.

4. **Monitor costs**: Track token usage and costs, especially in batch processing.

5. **Choose appropriate models**: Use cheaper models (gpt-4o-mini, claude-haiku) for simple tasks.

6. **Test with realistic data**: Test your prompts with realistic input sizes.

7. **Handle edge cases**: Plan for very long inputs and implement graceful degradation.

## Testing

Run the test suite:

```bash
python test_token_counter.py
```

Expected output:
```
================================================================================
Token Counter Test Suite
================================================================================

Testing token counting...
  'Hello, world!' -> 4 tokens
  Empty string -> 0 tokens
  1000 words -> 750 tokens
  ✓ Token counting tests passed

Testing cost estimation...
  GPT-4o: 1000 input + 500 output = $0.007500
  Claude 3.5 Sonnet: 10000 input + 2000 output = $0.060000
  Zero tokens = $0.000000
  ✓ Cost estimation tests passed

...

All tests passed! ✓
================================================================================
```

## Troubleshooting

### `tiktoken` not installed
If you see warnings about tiktoken, install it:
```bash
pip install tiktoken
```

The utility will fall back to approximation but may be less accurate for OpenAI models.

### Inaccurate counts for Claude
Claude uses a proprietary tokenizer. The utility uses character-based approximation which is reasonably accurate (~95%) but not perfect.

### Unknown model warnings
If you use a model not in the database, the utility will use default limits (128K tokens) and won't provide cost estimates.

## Integration Checklist

- [ ] Install tiktoken for accurate OpenAI token counting
- [ ] Import validation functions into your prompt pipeline
- [ ] Add `validate_before_send()` calls before API requests
- [ ] Implement error handling for over-limit prompts
- [ ] Set up cost tracking for budget management
- [ ] Test with realistic prompt sizes
- [ ] Add logging for token usage and costs
- [ ] Configure auto-truncation settings if needed
- [ ] Update model pricing data periodically

## License

Part of the Prompt Engineering System.
Author: JRiel
Date: 2025-12-01
