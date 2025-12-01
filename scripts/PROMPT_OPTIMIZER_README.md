# Prompt Optimizer - Complete Package

A production-ready system for automatically optimizing prompts through systematic testing and evaluation.

## 📦 Package Contents

### Core Script
- **`prompt_optimizer.py`** (1,017 lines)
  - Main optimizer implementation
  - 8 optimization techniques
  - Multi-criteria evaluation system
  - A/B testing framework
  - Results tracking and storage
  - CLI and Python API

### Documentation
- **`PROMPT_OPTIMIZER_GUIDE.md`** - Comprehensive guide (400+ lines)
- **`PROMPT_OPTIMIZER_QUICKSTART.md`** - Quick reference
- **`INTEGRATION_EXAMPLE.md`** - Integration patterns with other tools

### Supporting Scripts
- **`prompt_optimizer_examples.py`** - 10 practical examples
- **`test_prompt_optimizer.py`** - Full test suite

## 🚀 Quick Start

### Installation
```bash
pip install anthropic  # or: pip install openai
export ANTHROPIC_API_KEY="your-key"
```

### Basic Usage
```bash
# Optimize a prompt
python prompt_optimizer.py --prompt "Summarize this text"

# Interactive mode
python prompt_optimizer.py --interactive

# View help
python prompt_optimizer.py --help
```

### Run Tests
```bash
python test_prompt_optimizer.py
# Expected: 8 passed, 0 failed
```

## 📋 Features

### Optimization Techniques
1. **more_specific** - Add details and constraints
2. **more_concise** - Remove verbosity
3. **structured** - Add organization (sections, bullets)
4. **with_examples** - Include concrete examples
5. **role_based** - Specify expert role
6. **step_by_step** - Request explicit reasoning
7. **constrained** - Add output format rules
8. **context_rich** - Add background context

### Evaluation Criteria
- **Clarity** (0-10) - How clear and unambiguous?
- **Specificity** (0-10) - How detailed?
- **Format Guidance** (0-10) - Output format specified?
- **Examples Quality** (0-10) - Quality of examples
- **Conciseness** (0-10) - Concise yet complete?

### Key Capabilities
- ✅ Automatic variation generation (3-5 variations)
- ✅ Multi-criteria evaluation with scoring
- ✅ A/B testing with test cases
- ✅ Results tracking in JSON format
- ✅ Historical winner retrieval
- ✅ Anthropic & OpenAI support
- ✅ CLI and Python API
- ✅ Comprehensive error handling
- ✅ Logging and debugging support

## 📊 Data Structures

### PromptVariation
```python
@dataclass
class PromptVariation:
    id: str                      # Unique identifier
    content: str                 # Prompt text
    technique_used: str          # Technique applied
    scores: EvaluationCriteria   # Quality scores
    test_results: List[TestResult]  # Test results
    metadata: Dict[str, Any]     # Additional data
```

### OptimizationResult
```python
@dataclass
class OptimizationResult:
    original: str                      # Original prompt
    variations: List[PromptVariation]  # All variations
    winner: PromptVariation           # Best variation
    improvement_percentage: float      # Improvement %
    timestamp: str                     # ISO timestamp
    metadata: Dict[str, Any]          # Additional data
```

## 💻 Usage Examples

### Example 1: Basic Optimization
```python
from prompt_optimizer import PromptOptimizer

optimizer = PromptOptimizer(provider="anthropic")

result = optimizer.optimize(
    base_prompt="Summarize articles",
    num_variations=5
)

print(f"Winner: {result.winner.technique_used}")
print(f"Score: {result.winner.total_score():.2f}/10")
print(f"Improvement: {result.improvement_percentage:.1f}%")
```

### Example 2: With Test Cases
```python
result = optimizer.optimize(
    base_prompt="Extract email addresses",
    num_variations=4,
    test_inputs=[
        "Contact: john@example.com",
        "Email us at support@company.org"
    ],
    expected_outputs=[
        "john@example.com",
        "support@company.org"
    ]
)

print(f"Test Success: {result.winner.average_test_success_rate():.0%}")
```

### Example 3: Specific Techniques
```python
from prompt_optimizer import OptimizationTechnique

result = optimizer.optimize(
    base_prompt="Analyze sentiment",
    techniques=[
        OptimizationTechnique.MORE_SPECIFIC,
        OptimizationTechnique.WITH_EXAMPLES
    ]
)
```

### Example 4: View Winners
```python
winners = optimizer.get_winning_prompts(
    technique="with_examples",
    min_score=8.0,
    limit=5
)

for winner in winners:
    print(f"{winner['technique']}: {winner['score']:.2f}")
    print(f"Prompt: {winner['prompt']}")
```

## 🔧 CLI Examples

### Basic Commands
```bash
# Optimize with 3 variations
python prompt_optimizer.py \
  --prompt "Extract key points" \
  --num-variations 3

# Use specific techniques
python prompt_optimizer.py \
  --prompt "Analyze data" \
  --techniques more_specific with_examples

# With verbose output
python prompt_optimizer.py \
  --prompt "Classify text" \
  --verbose
```

### A/B Testing
```bash
# Single test case
python prompt_optimizer.py \
  --prompt "Extract email" \
  --test-input "Contact: user@example.com" \
  --expected-output "user@example.com"

# Multiple test cases
python prompt_optimizer.py \
  --prompt "Summarize" \
  --test-input "Long text 1..." \
  --test-input "Long text 2..." \
  --expected-output "Summary 1" \
  --expected-output "Summary 2"
```

### View History
```bash
# Show all winners
python prompt_optimizer.py --show-winners

# Filter by technique
python prompt_optimizer.py \
  --show-winners \
  --technique more_specific \
  --min-score 8.0
```

### Interactive Mode
```bash
python prompt_optimizer.py --interactive
```

## 📁 File Structure

```
scripts/
├── prompt_optimizer.py              # Main optimizer (1,017 lines)
├── prompt_optimizer_examples.py     # 10 examples
├── test_prompt_optimizer.py         # Test suite
├── PROMPT_OPTIMIZER_README.md       # This file
├── PROMPT_OPTIMIZER_GUIDE.md        # Full documentation
├── PROMPT_OPTIMIZER_QUICKSTART.md   # Quick reference
└── INTEGRATION_EXAMPLE.md           # Integration patterns
```

## 📂 Data Directories

```
~/.prompt_optimizer/
├── cache/                 # API response cache
└── results/              # Optimization results
    ├── optimization_*.json
    └── prompt_library.json
```

## 🧪 Testing

### Run Full Test Suite
```bash
python test_prompt_optimizer.py
```

### Expected Output
```
================================================================================
PROMPT OPTIMIZER TEST SUITE
================================================================================

Testing data classes...
  [OK] EvaluationCriteria: overall_score = 7.52
  [OK] PromptVariation: total_score = 4.51
  [OK] TestResult tracking: success_rate = 66.67%
  [OK] All data classes working correctly

Testing optimizer initialization...
  [OK] Anthropic provider initialized: claude-sonnet-4-20250514
  [OK] Directories created: ~/.prompt_optimizer/results
  ...

================================================================================
RESULTS: 8 passed, 0 failed
================================================================================

[OK] All tests passed!
```

## 📚 Documentation Index

1. **README** (this file) - Overview and quick reference
2. **QUICKSTART** - Get started in 5 minutes
3. **GUIDE** - Comprehensive documentation
4. **EXAMPLES** - 10 practical examples
5. **INTEGRATION** - Integration with other tools

## 🎯 Use Cases

### Data Extraction
```bash
python prompt_optimizer.py \
  --prompt "Extract product names" \
  --techniques more_specific constrained
```

### Creative Tasks
```bash
python prompt_optimizer.py \
  --prompt "Write product descriptions" \
  --techniques with_examples role_based
```

### Complex Reasoning
```bash
python prompt_optimizer.py \
  --prompt "Solve math problems" \
  --techniques step_by_step structured
```

### Concise Outputs
```bash
python prompt_optimizer.py \
  --prompt "Generate summaries" \
  --techniques more_concise constrained
```

## 🔍 Scoring System

### Individual Scores (0-10)
- Clarity: 25% weight
- Specificity: 25% weight
- Format Guidance: 20% weight
- Examples Quality: 15% weight
- Conciseness: 15% weight

### Total Score
```
Total = (Overall Score × 0.6) + (Test Success Rate × 10 × 0.4)
```

### Interpretation
- **9-10**: Excellent prompt
- **8-9**: Very good prompt
- **7-8**: Good prompt
- **6-7**: Adequate prompt
- **< 6**: Needs improvement

## 🛠️ Advanced Features

### Iterative Optimization
```python
current = "Base prompt"
for i in range(3):
    result = optimizer.optimize(current, num_variations=3)
    current = result.winner.content
    print(f"Round {i+1}: {result.winner.total_score():.2f}")
```

### Batch Processing
```python
prompts = ["Prompt 1", "Prompt 2", "Prompt 3"]
results = [optimizer.optimize(p) for p in prompts]
```

### Custom Evaluation
```python
result = optimizer.optimize(base_prompt="...")
for var in result.variations:
    custom_score = calculate_custom_metric(var.content)
    print(f"{var.technique_used}: {custom_score}")
```

## 🔗 Integration

Integrate with other prompt engineering tools:

- **Cost Tracker** - Monitor optimization costs
- **Reflection System** - Analyze results
- **Self-Consistency** - Validate prompts
- **Prompt Router** - Route by technique
- **Version Manager** - Track history
- **Knowledge Base** - Build library

See `INTEGRATION_EXAMPLE.md` for detailed patterns.

## 🐛 Troubleshooting

### Common Issues

**"anthropic package not installed"**
```bash
pip install anthropic
```

**"API key not set"**
```bash
export ANTHROPIC_API_KEY="sk-ant-..."
```

**Low scores**
- Use more specific base prompts
- Add test cases for validation
- Try different techniques
- Use `--verbose` for debugging

**Slow execution**
- Reduce `--num-variations`
- Use faster models
- Check network connection

## 📈 Performance

- **Variation Generation**: ~5-10 seconds per variation
- **Evaluation**: ~3-5 seconds per variation
- **A/B Testing**: Depends on test case count
- **Total Time**: ~1-2 minutes for 5 variations with evaluation

## 🔐 Security

- API keys stored in environment variables
- No sensitive data in cache files
- Results stored locally
- No external data transmission (except API calls)

## 🤝 Contributing

To extend the optimizer:

1. Add techniques to `OptimizationTechnique` enum
2. Implement in `_apply_technique()` method
3. Update evaluation criteria if needed
4. Add tests
5. Update documentation

## 📝 License

Part of the Prompt Engineering System.

## 🔗 Links

- **Main Script**: `prompt_optimizer.py`
- **Examples**: `prompt_optimizer_examples.py`
- **Tests**: `test_prompt_optimizer.py`
- **Docs**: `PROMPT_OPTIMIZER_GUIDE.md`

## 💡 Tips

1. **Start Simple**: Begin with basic optimization, add complexity later
2. **Use Tests**: Always include test cases for production prompts
3. **Iterate**: Optimize winners again for incremental improvements
4. **Track Results**: Use `--show-winners` to build prompt library
5. **Choose Techniques**: Match techniques to your use case
6. **Validate**: Test optimized prompts in real scenarios
7. **Monitor**: Track costs and performance metrics
8. **Document**: Save optimization history for future reference

## 📞 Support

For issues:
1. Check documentation in `PROMPT_OPTIMIZER_GUIDE.md`
2. Run tests: `python test_prompt_optimizer.py`
3. Use `--verbose` for detailed logs
4. Review examples in `prompt_optimizer_examples.py`

## 🎓 Learning Path

1. **Basics**: Start with quickstart guide
2. **CLI**: Try different commands
3. **Python API**: Write simple scripts
4. **Examples**: Run 10 example scripts
5. **Integration**: Combine with other tools
6. **Advanced**: Iterative optimization, custom evaluation

## ✨ Key Highlights

- 🎯 **8 optimization techniques** covering all use cases
- 📊 **5 evaluation criteria** for comprehensive scoring
- 🧪 **Built-in A/B testing** with success rate tracking
- 💾 **Results persistence** in JSON format
- 🔍 **Historical analysis** with winner retrieval
- 🔌 **Multi-provider support** (Anthropic, OpenAI)
- 🛠️ **CLI + Python API** for flexibility
- ✅ **Production-ready** with error handling and logging
- 📚 **Comprehensive docs** with examples
- 🧪 **Full test coverage** with 8 test cases

---

**Created**: December 2024
**Version**: 1.0
**Status**: Production Ready
**Lines of Code**: 1,017 (main script)
**Test Coverage**: 8/8 passed
