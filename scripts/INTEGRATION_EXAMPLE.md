# Integration Examples

How to integrate the Prompt Optimizer with other tools in the prompt engineering system.

## Integration with Cost Tracker

Track costs while optimizing prompts:

```python
from prompt_optimizer import PromptOptimizer
from cost_tracker import CostTracker

# Initialize both
optimizer = PromptOptimizer(provider="anthropic")
tracker = CostTracker()

# Optimize with cost tracking
with tracker.track_operation("prompt_optimization"):
    result = optimizer.optimize(
        base_prompt="Summarize articles",
        num_variations=5
    )

print(f"Winner: {result.winner.technique_used}")
print(f"Total cost: ${tracker.get_total_cost():.4f}")
```

## Integration with Reflection System

Use reflection to analyze optimization results:

```python
from prompt_optimizer import PromptOptimizer
from reflection import ReflectionEngine

optimizer = PromptOptimizer(provider="anthropic")
reflection = ReflectionEngine()

# Optimize
result = optimizer.optimize(
    base_prompt="Analyze customer feedback",
    num_variations=5
)

# Reflect on results
analysis = reflection.analyze({
    'original_prompt': result.original,
    'winner_technique': result.winner.technique_used,
    'score': result.winner.total_score(),
    'improvement': result.improvement_percentage,
    'all_techniques': [v.technique_used for v in result.variations]
})

print("Reflection insights:")
print(analysis)
```

## Integration with Self-Consistency

Optimize a prompt then test with self-consistency:

```python
from prompt_optimizer import PromptOptimizer
from self_consistency import run_self_consistency

# First optimize the prompt
optimizer = PromptOptimizer(provider="anthropic")
result = optimizer.optimize(
    base_prompt="Solve this math problem",
    num_variations=4
)

optimized_prompt = result.winner.content

# Then test with self-consistency
consistency_result = run_self_consistency(
    prompt=f"{optimized_prompt}\n\nProblem: What is 15% of 240?",
    num_samples=5,
    provider="anthropic"
)

print(f"Optimized prompt: {optimized_prompt}")
print(f"Final answer: {consistency_result.final_answer}")
print(f"Confidence: {consistency_result.confidence:.0%}")
```

## Integration with Prompt Router

Route prompts based on optimization technique:

```python
from prompt_optimizer import PromptOptimizer
from prompt_router import PromptRouter

optimizer = PromptOptimizer(provider="anthropic")
router = PromptRouter()

# Optimize multiple prompts
prompts = [
    "Summarize text",
    "Extract entities",
    "Classify sentiment"
]

optimized_prompts = {}

for prompt in prompts:
    result = optimizer.optimize(prompt, num_variations=3)

    # Store with routing metadata
    optimized_prompts[prompt] = {
        'optimized': result.winner.content,
        'technique': result.winner.technique_used,
        'score': result.winner.total_score(),
        'route_to': 'fast_model' if result.winner.scores.conciseness > 8 else 'powerful_model'
    }

# Use router with optimized prompts
for original, data in optimized_prompts.items():
    print(f"{original} → {data['route_to']}")
    print(f"  Technique: {data['technique']}")
    print(f"  Score: {data['score']:.2f}")
```

## Batch Optimization Pipeline

Create a pipeline for batch prompt optimization:

```python
import json
from pathlib import Path
from prompt_optimizer import PromptOptimizer

class PromptOptimizationPipeline:
    """Pipeline for batch prompt optimization."""

    def __init__(self, provider="anthropic"):
        self.optimizer = PromptOptimizer(provider=provider)

    def optimize_library(self, prompts_file: str, output_file: str):
        """Optimize all prompts in a library file."""

        # Load prompts
        with open(prompts_file) as f:
            prompts = json.load(f)

        optimized = {}

        for category, prompt_data in prompts.items():
            print(f"Optimizing {category}...")

            result = self.optimizer.optimize(
                base_prompt=prompt_data['prompt'],
                num_variations=4,
                test_inputs=prompt_data.get('test_inputs'),
                expected_outputs=prompt_data.get('expected_outputs')
            )

            optimized[category] = {
                'original': result.original,
                'optimized': result.winner.content,
                'technique': result.winner.technique_used,
                'score': result.winner.total_score(),
                'improvement': result.improvement_percentage,
                'test_success_rate': result.winner.average_test_success_rate()
            }

            # Save individual result
            self.optimizer.save_results(
                result,
                filename=f"optimized_{category}.json"
            )

        # Save complete library
        with open(output_file, 'w') as f:
            json.dump(optimized, f, indent=2)

        print(f"\nOptimized library saved to: {output_file}")
        return optimized

# Usage
pipeline = PromptOptimizationPipeline()

# Example prompts library
prompts_library = {
    'summarization': {
        'prompt': 'Summarize this text',
        'test_inputs': ['Long article about AI...', 'News story about...'],
        'expected_outputs': ['Brief summary...', 'Short summary...']
    },
    'extraction': {
        'prompt': 'Extract key entities',
        'test_inputs': ['Document with names...'],
        'expected_outputs': ['List of entities...']
    }
}

# Save to file
with open('prompts_to_optimize.json', 'w') as f:
    json.dump(prompts_library, f, indent=2)

# Run pipeline
results = pipeline.optimize_library(
    'prompts_to_optimize.json',
    'optimized_prompts_library.json'
)

# Display results
for category, data in results.items():
    print(f"\n{category.upper()}")
    print(f"  Technique: {data['technique']}")
    print(f"  Score: {data['score']:.2f}/10")
    print(f"  Improvement: {data['improvement']:.1f}%")
```

## Integration with Version Manager

Track prompt optimization history:

```python
from prompt_optimizer import PromptOptimizer
from version_manager import VersionManager

optimizer = PromptOptimizer(provider="anthropic")
version_manager = VersionManager(repo_dir="./prompt_versions")

# Optimize
result = optimizer.optimize(
    base_prompt="Analyze financial data",
    num_variations=5
)

# Create version entry
version_manager.create_version(
    name="financial_analysis_prompt",
    content=result.winner.content,
    metadata={
        'optimization_technique': result.winner.technique_used,
        'score': result.winner.total_score(),
        'improvement': result.improvement_percentage,
        'original': result.original
    },
    tags=['optimized', result.winner.technique_used]
)

print("Version created with optimization metadata")
```

## A/B Testing Integration

Compare optimized vs original in production:

```python
from prompt_optimizer import PromptOptimizer
import random
import time

class ABTestOptimizer:
    """A/B test optimized prompts against originals."""

    def __init__(self):
        self.optimizer = PromptOptimizer(provider="anthropic")
        self.results = {'original': [], 'optimized': []}

    def optimize_and_test(self, base_prompt, test_cases):
        """Optimize prompt and run A/B test."""

        # Optimize
        result = self.optimizer.optimize(
            base_prompt=base_prompt,
            num_variations=5
        )

        optimized = result.winner.content

        print(f"A/B Testing: {result.winner.technique_used}")

        # Run A/B test
        for test_input in test_cases:
            # Randomly choose version (50/50 split)
            use_optimized = random.choice([True, False])
            prompt = optimized if use_optimized else base_prompt

            # Execute (mock - replace with actual LLM call)
            start = time.time()
            response = f"Response for: {test_input[:30]}"
            duration = time.time() - start

            # Track results
            version = 'optimized' if use_optimized else 'original'
            self.results[version].append({
                'input': test_input,
                'response': response,
                'duration': duration
            })

        # Analyze results
        return self.analyze_results()

    def analyze_results(self):
        """Analyze A/B test results."""

        orig_avg_time = sum(r['duration'] for r in self.results['original']) / len(self.results['original'])
        opt_avg_time = sum(r['duration'] for r in self.results['optimized']) / len(self.results['optimized'])

        return {
            'original_count': len(self.results['original']),
            'optimized_count': len(self.results['optimized']),
            'original_avg_time': orig_avg_time,
            'optimized_avg_time': opt_avg_time,
            'improvement': (orig_avg_time - opt_avg_time) / orig_avg_time * 100
        }

# Usage
ab_tester = ABTestOptimizer()

test_cases = [
    "Sample input 1",
    "Sample input 2",
    "Sample input 3"
]

results = ab_tester.optimize_and_test(
    base_prompt="Analyze sentiment",
    test_cases=test_cases
)

print("\nA/B Test Results:")
print(f"Original: {results['original_count']} requests")
print(f"Optimized: {results['optimized_count']} requests")
print(f"Time improvement: {results['improvement']:.1f}%")
```

## Knowledge Base Integration

Build searchable database of optimized prompts:

```python
from prompt_optimizer import PromptOptimizer
from search_knowledge import KnowledgeBase

optimizer = PromptOptimizer(provider="anthropic")
kb = KnowledgeBase()

# Optimize prompts and add to knowledge base
domains = ['summarization', 'extraction', 'classification']

for domain in domains:
    # Optimize
    result = optimizer.optimize(
        base_prompt=f"Perform {domain}",
        num_variations=4
    )

    # Add to knowledge base
    kb.add_entry(
        title=f"Optimized {domain} Prompt",
        content=result.winner.content,
        category='optimized_prompts',
        tags=[domain, result.winner.technique_used],
        metadata={
            'score': result.winner.total_score(),
            'technique': result.winner.technique_used,
            'improvement': result.improvement_percentage
        }
    )

# Search optimized prompts
search_results = kb.search("summarization with_examples")
for entry in search_results:
    print(f"\n{entry['title']}")
    print(f"Technique: {entry['metadata']['technique']}")
    print(f"Score: {entry['metadata']['score']:.2f}")
```

## Continuous Optimization Loop

Automatically re-optimize prompts based on usage patterns:

```python
from prompt_optimizer import PromptOptimizer
import time
from datetime import datetime

class ContinuousOptimizer:
    """Continuously optimize prompts based on feedback."""

    def __init__(self, provider="anthropic"):
        self.optimizer = PromptOptimizer(provider=provider)
        self.prompt_history = {}

    def optimize_iteratively(self, base_prompt, iterations=3):
        """Optimize prompt iteratively."""

        current = base_prompt
        history = []

        for i in range(iterations):
            print(f"\nIteration {i+1}/{iterations}")

            result = self.optimizer.optimize(
                base_prompt=current,
                num_variations=3
            )

            history.append({
                'iteration': i+1,
                'prompt': result.winner.content,
                'technique': result.winner.technique_used,
                'score': result.winner.total_score(),
                'timestamp': datetime.now().isoformat()
            })

            # Use winner as base for next iteration
            current = result.winner.content

            print(f"  Technique: {result.winner.technique_used}")
            print(f"  Score: {result.winner.total_score():.2f}")

        # Save history
        self.prompt_history[base_prompt] = history

        return current, history

    def get_optimization_trajectory(self, base_prompt):
        """Get optimization improvement over iterations."""

        history = self.prompt_history.get(base_prompt, [])

        if not history:
            return None

        scores = [h['score'] for h in history]
        techniques = [h['technique'] for h in history]

        return {
            'initial_score': scores[0] if scores else 0,
            'final_score': scores[-1] if scores else 0,
            'improvement': scores[-1] - scores[0] if scores else 0,
            'techniques_used': techniques,
            'iterations': len(history)
        }

# Usage
continuous = ContinuousOptimizer()

final_prompt, history = continuous.optimize_iteratively(
    base_prompt="Generate product descriptions",
    iterations=3
)

trajectory = continuous.get_optimization_trajectory("Generate product descriptions")

print("\n=== Optimization Trajectory ===")
print(f"Initial Score: {trajectory['initial_score']:.2f}")
print(f"Final Score: {trajectory['final_score']:.2f}")
print(f"Total Improvement: {trajectory['improvement']:.2f}")
print(f"Techniques: {' → '.join(trajectory['techniques_used'])}")
```

## Summary

These integration examples demonstrate how the Prompt Optimizer can be combined with other tools in the prompt engineering system to create powerful workflows:

1. **Cost Tracking** - Monitor optimization costs
2. **Reflection** - Analyze why techniques work
3. **Self-Consistency** - Validate optimized prompts
4. **Routing** - Direct prompts to appropriate models
5. **Batch Processing** - Optimize prompt libraries
6. **Version Control** - Track optimization history
7. **A/B Testing** - Compare performance in production
8. **Knowledge Base** - Build searchable prompt library
9. **Continuous Improvement** - Iterative optimization loops

Use these patterns as starting points for building your own integrated prompt engineering workflows.
