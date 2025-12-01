# Prompt Optimizer Quick Start

## Installation

```bash
pip install anthropic  # or: pip install openai
export ANTHROPIC_API_KEY="your-api-key"
```

## Basic Usage

### 1. Optimize a Simple Prompt

```bash
python prompt_optimizer.py --prompt "Summarize this article"
```

Output:
```
Winner: with_examples
Score: 8.45/10
Improvement: 23.5%

Optimized Prompt:
Summarize the following article in 2-3 concise sentences...
```

### 2. Interactive Mode

```bash
python prompt_optimizer.py --interactive
```

### 3. With Test Cases

```bash
python prompt_optimizer.py \
  --prompt "Extract the email address" \
  --test-input "Contact us at support@company.com" \
  --expected-output "support@company.com"
```

### 4. View Historical Winners

```bash
python prompt_optimizer.py --show-winners
```

## Common Options

| Option | Description | Example |
|--------|-------------|---------|
| `--prompt` | Base prompt to optimize | `--prompt "Analyze sentiment"` |
| `--num-variations` | Number of variations (3-5) | `--num-variations 4` |
| `--provider` | anthropic or openai | `--provider anthropic` |
| `--techniques` | Specific techniques to use | `--techniques more_specific with_examples` |
| `--test-input` | Test case input | `--test-input "Sample text"` |
| `--expected-output` | Expected test output | `--expected-output "Expected result"` |
| `--interactive` | Interactive mode | `--interactive` |
| `--verbose` | Detailed output | `--verbose` |

## Optimization Techniques

1. **more_specific** - Adds details, constraints, requirements
2. **more_concise** - Removes verbosity, keeps essentials
3. **structured** - Adds sections, numbered steps, bullets
4. **with_examples** - Includes concrete examples
5. **role_based** - Specifies expert role/persona
6. **step_by_step** - Requests explicit reasoning steps
7. **constrained** - Adds output format/length/style rules
8. **context_rich** - Adds relevant background context

## Python API

```python
from prompt_optimizer import PromptOptimizer

optimizer = PromptOptimizer(provider="anthropic")

result = optimizer.optimize(
    base_prompt="Summarize articles",
    num_variations=5
)

print(f"Winner: {result.winner.technique_used}")
print(f"Score: {result.winner.total_score():.2f}/10")
print(f"Optimized: {result.winner.content}")

# Save results
optimizer.save_results(result)
```

## File Locations

- **Results**: `~/.prompt_optimizer/results/`
- **Cache**: `~/.prompt_optimizer/cache/`

## Examples

See `prompt_optimizer_examples.py` for 10 detailed examples:

```bash
# Run specific example
python prompt_optimizer_examples.py --example 1

# Run all examples
python prompt_optimizer_examples.py --all
```

## Troubleshooting

**Error: "anthropic package not installed"**
```bash
pip install anthropic
```

**Error: "API call failed"**
```bash
# Check API key is set
echo $ANTHROPIC_API_KEY
```

**Low scores?**
- Try different techniques
- Make base prompt more specific
- Add test cases
- Use `--verbose` to see details

## Full Documentation

See `PROMPT_OPTIMIZER_GUIDE.md` for comprehensive documentation.

## Quick Tips

1. Start with clear, specific base prompts
2. Use test cases for critical prompts
3. Choose techniques based on your use case:
   - Data extraction: `more_specific`, `constrained`
   - Creative tasks: `with_examples`, `role_based`
   - Reasoning: `step_by_step`, `structured`
4. Build a library of winning prompts with `--show-winners`
5. Iterate: optimize winners again for incremental improvements

## Test Script

Run tests to verify installation:

```bash
python test_prompt_optimizer.py
```

Expected output:
```
RESULTS: 8 passed, 0 failed
[OK] All tests passed!
```
