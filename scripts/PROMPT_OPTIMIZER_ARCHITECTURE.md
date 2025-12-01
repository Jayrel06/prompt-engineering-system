# Prompt Optimizer Architecture

## System Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                    PROMPT OPTIMIZER SYSTEM                       │
│                                                                  │
│  Input: Base Prompt → Optimize → Evaluate → Test → Output      │
└─────────────────────────────────────────────────────────────────┘
```

## Core Components

### 1. Input Layer
```
┌──────────────────┐
│   User Input     │
│                  │
│ • Base Prompt    │
│ • Techniques     │
│ • Test Cases     │
│ • Criteria       │
└────────┬─────────┘
         │
         ▼
```

### 2. Optimization Engine
```
┌────────────────────────────────────────┐
│       PromptOptimizer Class            │
│                                        │
│  ┌──────────────────────────────┐    │
│  │  Variation Generation        │    │
│  │  • more_specific             │    │
│  │  • more_concise              │    │
│  │  • structured                │    │
│  │  • with_examples             │    │
│  │  • role_based                │    │
│  │  • step_by_step              │    │
│  │  • constrained               │    │
│  │  • context_rich              │    │
│  └──────────────────────────────┘    │
│                                        │
│  ┌──────────────────────────────┐    │
│  │  LLM Integration             │    │
│  │  • Anthropic API             │    │
│  │  • OpenAI API                │    │
│  │  • Error Handling            │    │
│  │  • Caching                   │    │
│  └──────────────────────────────┘    │
└────────────────────────────────────────┘
```

### 3. Evaluation System
```
┌────────────────────────────────────────┐
│      Evaluation Framework              │
│                                        │
│  ┌──────────────────────────────┐    │
│  │  Criteria Scoring (0-10)     │    │
│  │                              │    │
│  │  Clarity        (25%)        │    │
│  │  Specificity    (25%)        │    │
│  │  Format         (20%)        │    │
│  │  Examples       (15%)        │    │
│  │  Conciseness    (15%)        │    │
│  └──────────────────────────────┘    │
│                                        │
│  ┌──────────────────────────────┐    │
│  │  Overall Score Calculation   │    │
│  │                              │    │
│  │  Base Score × 0.6 +          │    │
│  │  Test Score × 0.4            │    │
│  └──────────────────────────────┘    │
└────────────────────────────────────────┘
```

### 4. Testing Framework
```
┌────────────────────────────────────────┐
│      A/B Testing System                │
│                                        │
│  ┌──────────────────────────────┐    │
│  │  Test Execution              │    │
│  │  • Run test inputs           │    │
│  │  • Compare outputs           │    │
│  │  • Calculate success rate    │    │
│  │  • Track execution time      │    │
│  └──────────────────────────────┘    │
│                                        │
│  ┌──────────────────────────────┐    │
│  │  Result Tracking             │    │
│  │  • TestResult objects        │    │
│  │  • Success/Failure           │    │
│  │  • Error logging             │    │
│  └──────────────────────────────┘    │
└────────────────────────────────────────┘
```

### 5. Storage Layer
```
┌────────────────────────────────────────┐
│      Results Management                │
│                                        │
│  ┌──────────────────────────────┐    │
│  │  Cache System                │    │
│  │  ~/.prompt_optimizer/cache/  │    │
│  │  • API response caching      │    │
│  └──────────────────────────────┘    │
│                                        │
│  ┌──────────────────────────────┐    │
│  │  Results Storage             │    │
│  │  ~/.prompt_optimizer/results/│    │
│  │  • JSON format               │    │
│  │  • Winner tracking           │    │
│  │  • Historical data           │    │
│  └──────────────────────────────┘    │
└────────────────────────────────────────┘
```

## Data Flow

```
┌─────────┐
│  User   │
└────┬────┘
     │
     ▼
┌─────────────────┐
│  Base Prompt    │
└────┬────────────┘
     │
     ▼
┌──────────────────────────┐
│  Generate Variations     │◄──── OptimizationTechnique enum
│  (3-5 variations)        │
└────┬─────────────────────┘
     │
     ▼
┌──────────────────────────┐
│  Evaluate Each           │
│  Variation               │◄──── EvaluationCriteria
│  • Clarity               │
│  • Specificity           │
│  • Format                │
│  • Examples              │
│  • Conciseness           │
└────┬─────────────────────┘
     │
     ▼
┌──────────────────────────┐
│  Run A/B Tests           │
│  (if test cases          │◄──── Test inputs/outputs
│   provided)              │
└────┬─────────────────────┘
     │
     ▼
┌──────────────────────────┐
│  Rank Variations         │
│  by Total Score          │
└────┬─────────────────────┘
     │
     ▼
┌──────────────────────────┐
│  Select Winner           │
│  (highest score)         │
└────┬─────────────────────┘
     │
     ▼
┌──────────────────────────┐
│  OptimizationResult      │
│  • Winner                │
│  • All variations        │
│  • Scores                │
│  • Improvement %         │
└────┬─────────────────────┘
     │
     ▼
┌──────────────────────────┐
│  Save to JSON            │
└────┬─────────────────────┘
     │
     ▼
┌──────────────────────────┐
│  Return to User          │
└──────────────────────────┘
```

## Class Hierarchy

```
OptimizationTechnique (Enum)
├── MORE_SPECIFIC
├── MORE_CONCISE
├── STRUCTURED
├── WITH_EXAMPLES
├── ROLE_BASED
├── STEP_BY_STEP
├── CONSTRAINED
└── CONTEXT_RICH

EvaluationCriteria (Dataclass)
├── clarity: float
├── specificity: float
├── format_guidance: float
├── examples_quality: float
├── conciseness: float
└── overall_score() → float

TestResult (Dataclass)
├── test_input: str
├── expected_output: Optional[str]
├── actual_output: str
├── success: bool
├── execution_time: float
└── error: Optional[str]

PromptVariation (Dataclass)
├── id: str
├── content: str
├── technique_used: str
├── scores: EvaluationCriteria
├── test_results: List[TestResult]
├── metadata: Dict
├── average_test_success_rate() → float
└── total_score() → float

OptimizationResult (Dataclass)
├── original: str
├── variations: List[PromptVariation]
├── winner: PromptVariation
├── improvement_percentage: float
├── timestamp: str
├── metadata: Dict
└── to_dict() → Dict

PromptOptimizer (Class)
├── __init__(provider, model, api_key, cache_dir, results_dir)
├── _default_model() → str
├── _call_llm(prompt, system, temperature, max_tokens) → str
├── generate_variations(base_prompt, num_variations, techniques) → List[PromptVariation]
├── _apply_technique(base_prompt, technique) → str
├── evaluate_prompt(variation, reference_prompt) → EvaluationCriteria
├── run_ab_test(variations, test_inputs, expected_outputs, auto_evaluate) → List[PromptVariation]
├── _evaluate_output_match(expected, actual) → bool
├── optimize(base_prompt, num_variations, test_inputs, expected_outputs, techniques) → OptimizationResult
├── save_results(result, filename) → Path
├── load_results(filename) → Dict
└── get_winning_prompts(technique, min_score, limit) → List[Dict]
```

## Workflow Diagram

```
                    ┌──────────────┐
                    │   CLI Args   │
                    │      or      │
                    │  Python API  │
                    └──────┬───────┘
                           │
                           ▼
                ┌──────────────────────┐
                │  PromptOptimizer     │
                │  Initialization      │
                └──────┬───────────────┘
                       │
         ┌─────────────┼─────────────┐
         │             │             │
         ▼             ▼             ▼
    ┌────────┐   ┌─────────┐   ┌────────┐
    │Anthropic│  │ OpenAI  │   │ Config │
    │  API    │  │   API   │   │  Load  │
    └────┬────┘  └────┬────┘   └───┬────┘
         │            │            │
         └────────────┼────────────┘
                      │
                      ▼
          ┌───────────────────────┐
          │  Generate Variations  │
          │                       │
          │  For each technique:  │
          │  1. Build prompt      │
          │  2. Call LLM          │
          │  3. Parse response    │
          │  4. Create variation  │
          └───────┬───────────────┘
                  │
                  ▼
          ┌───────────────────────┐
          │  Evaluate Variations  │
          │                       │
          │  For each variation:  │
          │  1. Score criteria    │
          │  2. Calculate overall │
          │  3. Update scores     │
          └───────┬───────────────┘
                  │
                  ▼
          ┌───────────────────────┐
          │    Run Tests          │
          │    (optional)         │
          │                       │
          │  For each test:       │
          │  1. Execute prompt    │
          │  2. Compare output    │
          │  3. Track success     │
          └───────┬───────────────┘
                  │
                  ▼
          ┌───────────────────────┐
          │  Rank & Select Winner │
          │                       │
          │  1. Sort by score     │
          │  2. Pick highest      │
          │  3. Calculate improve │
          └───────┬───────────────┘
                  │
                  ▼
          ┌───────────────────────┐
          │  Create Result Object │
          │                       │
          │  • Winner             │
          │  • All variations     │
          │  • Metadata           │
          └───────┬───────────────┘
                  │
         ┌────────┼────────┐
         │                 │
         ▼                 ▼
    ┌─────────┐      ┌──────────┐
    │  Save   │      │  Return  │
    │  JSON   │      │  Result  │
    └─────────┘      └──────────┘
```

## Integration Points

```
┌─────────────────────────────────────────────────────────┐
│            Prompt Engineering System                     │
│                                                          │
│  ┌──────────────┐      ┌──────────────────────┐       │
│  │   Prompt     │◄────►│  Prompt Optimizer    │       │
│  │   Router     │      │                      │       │
│  └──────────────┘      └──────────┬───────────┘       │
│                                   │                    │
│  ┌──────────────┐                │                    │
│  │    Cost      │◄───────────────┤                    │
│  │   Tracker    │                │                    │
│  └──────────────┘                │                    │
│                                   │                    │
│  ┌──────────────┐                │                    │
│  │  Reflection  │◄───────────────┤                    │
│  │   Engine     │                │                    │
│  └──────────────┘                │                    │
│                                   │                    │
│  ┌──────────────┐                │                    │
│  │     Self     │◄───────────────┤                    │
│  │ Consistency  │                │                    │
│  └──────────────┘                │                    │
│                                   │                    │
│  ┌──────────────┐                │                    │
│  │   Version    │◄───────────────┤                    │
│  │   Manager    │                │                    │
│  └──────────────┘                │                    │
│                                   │                    │
│  ┌──────────────┐                │                    │
│  │  Knowledge   │◄───────────────┘                    │
│  │     Base     │                                     │
│  └──────────────┘                                     │
└─────────────────────────────────────────────────────────┘
```

## File Organization

```
prompt-engineering-system/
└── scripts/
    ├── prompt_optimizer.py          # Main implementation
    ├── prompt_optimizer_examples.py # Usage examples
    ├── test_prompt_optimizer.py     # Test suite
    │
    ├── PROMPT_OPTIMIZER_README.md        # Overview
    ├── PROMPT_OPTIMIZER_GUIDE.md         # Full docs
    ├── PROMPT_OPTIMIZER_QUICKSTART.md    # Quick ref
    ├── PROMPT_OPTIMIZER_ARCHITECTURE.md  # This file
    └── INTEGRATION_EXAMPLE.md            # Integration

~/.prompt_optimizer/
├── cache/
│   └── api_responses_*.json
└── results/
    ├── optimization_*.json
    └── prompt_library.json
```

## API Structure

### CLI Interface
```
prompt_optimizer.py
├── --prompt              (required*)
├── --num-variations      (default: 5)
├── --provider            (default: anthropic)
├── --model               (auto)
├── --test-input          (multiple)
├── --expected-output     (multiple)
├── --techniques          (multiple)
├── --show-winners        (flag)
├── --technique           (filter)
├── --min-score           (default: 7.0)
├── --interactive         (flag)
├── --output              (filename)
└── --verbose             (flag)

* or --show-winners or --interactive
```

### Python API
```python
# Initialize
optimizer = PromptOptimizer(
    provider="anthropic",
    model=None,
    api_key=None,
    cache_dir=None,
    results_dir=None
)

# Generate variations
variations = optimizer.generate_variations(
    base_prompt="...",
    num_variations=5,
    techniques=[...]
)

# Evaluate
criteria = optimizer.evaluate_prompt(
    variation=...,
    reference_prompt=None
)

# A/B test
tested_variations = optimizer.run_ab_test(
    variations=[...],
    test_inputs=[...],
    expected_outputs=[...],
    auto_evaluate=True
)

# Full optimize
result = optimizer.optimize(
    base_prompt="...",
    num_variations=5,
    test_inputs=[...],
    expected_outputs=[...],
    techniques=[...]
)

# Save/Load
path = optimizer.save_results(result, filename="...")
data = optimizer.load_results(filename="...")

# Get winners
winners = optimizer.get_winning_prompts(
    technique="...",
    min_score=7.0,
    limit=10
)
```

## Scoring Algorithm

```
┌────────────────────────────────────┐
│  Individual Criterion Scoring      │
│  (LLM evaluates 0-10 for each)     │
└─────────┬──────────────────────────┘
          │
          ▼
┌────────────────────────────────────┐
│  Weighted Overall Score            │
│                                    │
│  Clarity       × 0.25              │
│  Specificity   × 0.25              │
│  Format        × 0.20              │
│  Examples      × 0.15              │
│  Conciseness   × 0.15              │
│  ─────────────────────             │
│  Overall Score (0-10)              │
└─────────┬──────────────────────────┘
          │
          ▼
┌────────────────────────────────────┐
│  Test Success Rate                 │
│  (if tests provided)               │
│                                    │
│  Successes / Total × 10            │
└─────────┬──────────────────────────┘
          │
          ▼
┌────────────────────────────────────┐
│  Total Score                       │
│                                    │
│  (Overall × 0.6) + (Tests × 0.4)   │
└────────────────────────────────────┘
```

## Technique Application Flow

```
Base Prompt
     │
     ▼
┌─────────────────────────────────────┐
│  Technique-Specific Prompt          │
│  Template                           │
│                                     │
│  "Take this prompt and make it      │
│   [TECHNIQUE_INSTRUCTION]"          │
└─────────┬───────────────────────────┘
          │
          ▼
┌─────────────────────────────────────┐
│  LLM API Call                       │
│  • System: "You are prompt expert"  │
│  • Temperature: 0.7                 │
│  • Max tokens: 2048                 │
└─────────┬───────────────────────────┘
          │
          ▼
┌─────────────────────────────────────┐
│  Parse Response                     │
│  • Extract optimized prompt         │
│  • Strip meta-commentary            │
└─────────┬───────────────────────────┘
          │
          ▼
┌─────────────────────────────────────┐
│  Create PromptVariation             │
│  • Generate ID                      │
│  • Store content                    │
│  • Tag technique                    │
└─────────────────────────────────────┘
```

## Error Handling

```
┌─────────────────────┐
│  User Input         │
└──────┬──────────────┘
       │
       ▼
┌─────────────────────┐
│  Input Validation   │
│  • Check required   │
│  • Validate types   │
└──────┬──────────────┘
       │
       ▼
┌─────────────────────┐
│  API Call           │
│  • Try/except       │
│  • Retry logic      │
│  • Timeout handling │
└──────┬──────────────┘
       │
       ├─ Success ──────────► Continue
       │
       └─ Error ──┐
                  │
                  ▼
         ┌────────────────┐
         │  Log Error     │
         │  • Logger.error│
         │  • Stack trace │
         └────────┬───────┘
                  │
                  ▼
         ┌────────────────┐
         │  Graceful Fail │
         │  • Skip variant│
         │  • Continue    │
         │  • Or raise    │
         └────────────────┘
```

## Performance Characteristics

```
Operation              Time Complexity    Space Complexity
─────────────────────  ─────────────────  ─────────────────
Generate Variation     O(1) + API_TIME    O(n) prompts
Evaluate Variation     O(1) + API_TIME    O(1)
Run A/B Test          O(n×m) + API_TIME  O(n×m) results
Rank Variations       O(n log n)         O(n)
Save Results          O(n)               O(n) disk
Load Results          O(n)               O(n) memory

where:
  n = number of variations
  m = number of test cases
  API_TIME = LLM response time (5-10s avg)
```

## Summary

The Prompt Optimizer is designed as a modular, extensible system with:

- **Clear separation of concerns** (generation, evaluation, testing)
- **Flexible integration points** with other tools
- **Robust error handling** and logging
- **Comprehensive data structures** for tracking results
- **Multiple interfaces** (CLI, Python API)
- **Persistent storage** for historical analysis
- **Production-ready** implementation

The architecture supports both simple single-prompt optimization and complex batch processing workflows, making it suitable for various use cases from experimentation to production deployment.
