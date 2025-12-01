# Prompt Optimizer Guide

## Overview

The Prompt Optimizer is a production-ready tool for automatically improving prompts through systematic testing and optimization. It generates multiple variations using different techniques, evaluates them, and identifies the best performing version.

## Features

- **Automatic Variation Generation**: Creates 3-5 prompt variations using proven optimization techniques
- **Multi-Criteria Evaluation**: Scores prompts on clarity, specificity, format guidance, examples quality, and conciseness
- **A/B Testing**: Test variations with real inputs and expected outputs
- **Results Tracking**: Saves winning prompts to JSON for future reference
- **Multi-Provider Support**: Works with Anthropic (Claude) and OpenAI (GPT) APIs
- **Production Ready**: Comprehensive error handling, logging, and documentation

## Installation

### Prerequisites

```bash
pip install anthropic  # For Anthropic API
# OR
pip install openai     # For OpenAI API
```

### Environment Setup

Set your API key:

```bash
# Anthropic
export ANTHROPIC_API_KEY="your-api-key-here"

# OpenAI
export OPENAI_API_KEY="your-api-key-here"
```

## Optimization Techniques

The tool uses 8 different optimization techniques:

1. **MORE_SPECIFIC**: Adds details, constraints, and specific requirements
2. **MORE_CONCISE**: Removes verbosity while preserving key information
3. **STRUCTURED**: Reorganizes with sections, numbered steps, or bullet points
4. **WITH_EXAMPLES**: Adds concrete examples to clarify expectations
5. **ROLE_BASED**: Specifies a role or persona (e.g., "You are an expert...")
6. **STEP_BY_STEP**: Requests explicit step-by-step reasoning
7. **CONSTRAINED**: Adds output format, length, or style constraints
8. **CONTEXT_RICH**: Adds relevant context to improve understanding

## Usage Examples

### Basic Optimization

```bash
python prompt_optimizer.py --prompt "Summarize this article"
```

This will:
- Generate 5 variations using different techniques
- Evaluate each variation on multiple criteria
- Identify and display the winner
- Save results to `~/.prompt_optimizer/results/`

### Specify Number of Variations

```bash
python prompt_optimizer.py --prompt "Extract key points" --num-variations 3
```

### Use Specific Techniques

```bash
python prompt_optimizer.py \
  --prompt "Analyze sentiment" \
  --techniques more_specific with_examples structured
```

### With A/B Testing

```bash
python prompt_optimizer.py \
  --prompt "Extract the email address" \
  --test-input "Contact John at john@example.com" \
  --expected-output "john@example.com"
```

Multiple test cases:

```bash
python prompt_optimizer.py \
  --prompt "Extract emails" \
  --test-input "Email: alice@test.com" \
  --test-input "Contact bob@demo.org" \
  --expected-output "alice@test.com" \
  --expected-output "bob@demo.org"
```

### Interactive Mode

```bash
python prompt_optimizer.py --interactive
```

This starts an interactive session where you can:
- Enter prompts one at a time
- See optimization results immediately
- Iterate on different prompts

### Choose Provider/Model

```bash
# Use OpenAI
python prompt_optimizer.py \
  --prompt "Summarize" \
  --provider openai \
  --model gpt-4

# Use Anthropic with specific model
python prompt_optimizer.py \
  --prompt "Analyze" \
  --provider anthropic \
  --model claude-sonnet-4-20250514
```

### View Historical Winners

```bash
# Show all top performers
python prompt_optimizer.py --show-winners

# Filter by technique
python prompt_optimizer.py --show-winners --technique more_specific

# Set minimum score threshold
python prompt_optimizer.py --show-winners --min-score 8.0
```

### Save to Custom Location

```bash
python prompt_optimizer.py \
  --prompt "Generate code" \
  --output my_optimization.json
```

### Verbose Output

```bash
python prompt_optimizer.py --prompt "Explain" --verbose
```

Shows:
- Detailed logs during processing
- All variations with scores
- Full test results

## Python API Usage

### Basic Optimization

```python
from prompt_optimizer import PromptOptimizer

optimizer = PromptOptimizer(provider="anthropic")

result = optimizer.optimize(
    base_prompt="Summarize this article",
    num_variations=5
)

print(f"Winner: {result.winner.technique_used}")
print(f"Score: {result.winner.total_score():.2f}/10")
print(f"Optimized prompt: {result.winner.content}")

# Save results
optimizer.save_results(result)
```

### With Test Cases

```python
result = optimizer.optimize(
    base_prompt="Extract the main topic",
    num_variations=4,
    test_inputs=[
        "Article about climate change...",
        "Story about space exploration..."
    ],
    expected_outputs=[
        "climate change",
        "space exploration"
    ]
)

print(f"Test success rate: {result.winner.average_test_success_rate():.0%}")
```

### Use Specific Techniques

```python
from prompt_optimizer import OptimizationTechnique

result = optimizer.optimize(
    base_prompt="Analyze sentiment",
    techniques=[
        OptimizationTechnique.MORE_SPECIFIC,
        OptimizationTechnique.WITH_EXAMPLES,
        OptimizationTechnique.STRUCTURED
    ]
)
```

### Evaluate Single Prompt

```python
from prompt_optimizer import PromptVariation, EvaluationCriteria

variation = PromptVariation(
    id="test1",
    content="Your prompt here",
    technique_used="manual",
    scores=EvaluationCriteria()
)

criteria = optimizer.evaluate_prompt(variation)
print(f"Clarity: {criteria.clarity}/10")
print(f"Overall: {criteria.overall_score():.2f}/10")
```

### Load and Analyze Results

```python
# Load specific result
data = optimizer.load_results("optimization_more_specific_20241201_120000.json")

# Get top performers
winners = optimizer.get_winning_prompts(
    technique="with_examples",
    min_score=8.0,
    limit=5
)

for winner in winners:
    print(f"{winner['technique']}: {winner['score']:.2f}")
    print(f"Prompt: {winner['prompt']}")
```

## Data Classes

### PromptVariation

Represents a single prompt variation:

```python
@dataclass
class PromptVariation:
    id: str                      # Unique identifier
    content: str                 # Prompt text
    technique_used: str          # Optimization technique applied
    scores: EvaluationCriteria   # Quality scores
    test_results: List[TestResult]  # A/B test results
    metadata: Dict[str, Any]     # Additional metadata
```

### EvaluationCriteria

Scoring criteria for prompts:

```python
@dataclass
class EvaluationCriteria:
    clarity: float              # 0-10: Clarity and unambiguity
    specificity: float          # 0-10: Detail and specificity
    format_guidance: float      # 0-10: Output format specification
    examples_quality: float     # 0-10: Quality of examples
    conciseness: float          # 0-10: Conciseness vs completeness
```

### OptimizationResult

Complete optimization results:

```python
@dataclass
class OptimizationResult:
    original: str                      # Original prompt
    variations: List[PromptVariation]  # All variations (ranked)
    winner: PromptVariation           # Best performing variation
    improvement_percentage: float      # Improvement over baseline
    timestamp: str                     # ISO format timestamp
    metadata: Dict[str, Any]          # Additional metadata
```

### TestResult

Individual test execution result:

```python
@dataclass
class TestResult:
    test_input: str           # Input used for testing
    expected_output: str      # Expected output (optional)
    actual_output: str        # Actual LLM output
    success: bool             # Whether test passed
    execution_time: float     # Time taken (seconds)
    error: Optional[str]      # Error message if failed
```

## Scoring System

### Individual Criteria (0-10)

- **Clarity**: How clear and unambiguous are the instructions?
- **Specificity**: How detailed and specific are the requirements?
- **Format Guidance**: Does it specify the desired output format?
- **Examples Quality**: Quality of examples provided (0 if none)
- **Conciseness**: Is it concise while being complete?

### Overall Score Calculation

```
Overall Score = (
    Clarity × 0.25 +
    Specificity × 0.25 +
    Format Guidance × 0.20 +
    Examples Quality × 0.15 +
    Conciseness × 0.15
)
```

### Total Score (with tests)

```
Total Score = (Overall Score × 0.6) + (Test Success Rate × 10 × 0.4)
```

## Output Format

### Console Output

```
================================================================================
OPTIMIZATION RESULTS
================================================================================

Original Prompt:
Summarize this text

Winner: with_examples
Score: 8.45/10
Improvement: 23.5%

Optimized Prompt:
Summarize the following text in 2-3 concise sentences, capturing the main
points and key takeaways.

Example:
Input: "Long article about AI..."
Output: "The article discusses recent advances in AI..."

Detailed Scores:
  Clarity: 8.5/10
  Specificity: 8.8/10
  Format Guidance: 8.2/10
  Examples Quality: 9.0/10
  Conciseness: 7.8/10

================================================================================
Results saved to: /home/user/.prompt_optimizer/results/optimization_with_examples_20241201_120000.json
```

### JSON Output Format

```json
{
  "original": "Summarize this text",
  "variations": [
    {
      "id": "abc123def456",
      "content": "Optimized prompt content...",
      "technique_used": "with_examples",
      "scores": {
        "clarity": 8.5,
        "specificity": 8.8,
        "format_guidance": 8.2,
        "examples_quality": 9.0,
        "conciseness": 7.8
      },
      "test_results": [],
      "metadata": {
        "generation_timestamp": "2024-12-01T12:00:00"
      },
      "total_score": 8.45
    }
  ],
  "winner": {
    "id": "abc123def456",
    "content": "Optimized prompt content...",
    "technique_used": "with_examples",
    "total_score": 8.45
  },
  "improvement_percentage": 23.5,
  "timestamp": "2024-12-01T12:00:00",
  "metadata": {
    "num_variations": 5,
    "provider": "anthropic",
    "model": "claude-sonnet-4-20250514",
    "baseline_score": 6.84
  }
}
```

## Configuration

### Default Directories

- **Cache**: `~/.prompt_optimizer/cache/` - API response caching
- **Results**: `~/.prompt_optimizer/results/` - Optimization results

### Custom Configuration

```python
optimizer = PromptOptimizer(
    provider="anthropic",
    model="claude-sonnet-4-20250514",
    api_key="your-key",  # Optional, uses env var if not provided
    cache_dir=Path("/custom/cache"),
    results_dir=Path("/custom/results")
)
```

## Error Handling

The tool includes comprehensive error handling:

- **API Failures**: Retries with exponential backoff
- **Invalid Prompts**: Clear error messages
- **Missing Dependencies**: Helpful installation instructions
- **File I/O Errors**: Graceful fallbacks
- **Parsing Errors**: Default scoring on evaluation failures

All errors are logged with appropriate severity levels.

## Best Practices

### 1. Start with Clear Base Prompts

Good starting prompt:
```
"Summarize the key points from this article"
```

Too vague:
```
"Do something with this"
```

### 2. Use Test Cases for Critical Prompts

For production prompts, always include test cases:

```bash
python prompt_optimizer.py \
  --prompt "Extract entities" \
  --test-input "Apple Inc. CEO Tim Cook..." \
  --expected-output "Company: Apple Inc., Person: Tim Cook"
```

### 3. Choose Appropriate Techniques

- **Data extraction**: Use `more_specific`, `constrained`
- **Creative tasks**: Use `with_examples`, `role_based`
- **Complex reasoning**: Use `step_by_step`, `structured`
- **Concise outputs**: Use `more_concise`, `constrained`

### 4. Iterate on Winners

```bash
# First optimization
python prompt_optimizer.py --prompt "Your prompt" --output round1.json

# Extract winner and optimize again
python prompt_optimizer.py --prompt "<winner from round1>" --output round2.json
```

### 5. Build a Library

Keep track of winning prompts:

```bash
# Regularly check your best performers
python prompt_optimizer.py --show-winners --min-score 8.5
```

## Troubleshooting

### "anthropic package not installed"

```bash
pip install anthropic
```

### "API call failed"

Check your API key:
```bash
echo $ANTHROPIC_API_KEY  # Should show your key
```

### Low Scores

Try:
- Different techniques
- More specific base prompt
- Add test cases
- Increase temperature for variation generation

### Slow Execution

- Reduce `--num-variations`
- Use caching (enabled by default)
- Use faster models (claude-haiku, gpt-3.5-turbo)

## Performance Tips

1. **Caching**: API responses are automatically cached
2. **Batch Processing**: Use Python API to optimize multiple prompts
3. **Model Selection**: Use faster models for initial testing
4. **Parallel Evaluation**: Test cases run sequentially but variations are independent

## Advanced Usage

### Custom Evaluation Function

```python
def custom_evaluator(variation, reference):
    # Your custom logic
    score = calculate_custom_score(variation.content)
    return score

# Use in optimization workflow
result = optimizer.optimize(base_prompt="...")
# Post-process with custom evaluation
```

### Batch Optimization

```python
prompts = [
    "Summarize articles",
    "Extract entities",
    "Classify sentiment"
]

results = []
for prompt in prompts:
    result = optimizer.optimize(prompt, num_variations=3)
    results.append(result)
    optimizer.save_results(result)
```

### Integration with Existing Systems

```python
# Load your prompts
with open('prompts.json') as f:
    prompts = json.load(f)

# Optimize each
for prompt_data in prompts:
    result = optimizer.optimize(
        base_prompt=prompt_data['prompt'],
        test_inputs=prompt_data['test_cases']
    )

    # Update with optimized version
    prompt_data['optimized'] = result.winner.content
    prompt_data['score'] = result.winner.total_score()

# Save updated prompts
with open('prompts_optimized.json', 'w') as f:
    json.dump(prompts, f, indent=2)
```

## Contributing

To extend the tool:

1. Add new optimization techniques to `OptimizationTechnique` enum
2. Implement technique in `_apply_technique()` method
3. Add custom evaluation criteria to `EvaluationCriteria`
4. Update scoring weights in `overall_score()`

## License

Part of the Prompt Engineering System toolkit.

## Support

For issues or questions:
- Check the examples in this guide
- Review error logs with `--verbose` flag
- Ensure API keys are properly configured
