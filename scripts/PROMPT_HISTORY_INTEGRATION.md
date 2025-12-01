# Prompt History Integration Guide

This guide shows how to integrate `prompt_history.py` with other scripts in the prompt engineering system.

## Table of Contents

1. [Basic Integration](#basic-integration)
2. [Integration with Existing Scripts](#integration-with-existing-scripts)
3. [Auto-Tracking Patterns](#auto-tracking-patterns)
4. [Advanced Use Cases](#advanced-use-cases)
5. [Best Practices](#best-practices)

## Basic Integration

### Simple Import and Use

```python
from prompt_history import PromptHistory

# Initialize once
history = PromptHistory()

# Use in your code
def process_prompt(prompt_text):
    # Your existing logic
    response = call_ai_api(prompt_text)

    # Add history tracking
    history.save(
        prompt=prompt_text,
        output=response,
        model="gpt-4",
        tags=["processed"]
    )

    return response
```

## Integration with Existing Scripts

### 1. Integration with prompt_optimizer.py

```python
from prompt_optimizer import PromptOptimizer
from prompt_history import PromptHistory

class TrackedPromptOptimizer:
    def __init__(self):
        self.optimizer = PromptOptimizer()
        self.history = PromptHistory()

    def optimize_and_track(self, prompt, target="clarity"):
        # Optimize
        result = self.optimizer.optimize(prompt, target=target)

        # Track both original and optimized
        self.history.save(
            prompt=prompt,
            output=result['optimized_prompt'],
            framework="optimization",
            template=f"optimize-{target}",
            tags=["optimization", target],
            metadata={
                "original_score": result.get('original_score'),
                "optimized_score": result.get('optimized_score'),
                "improvements": result.get('improvements')
            }
        )

        return result

# Usage
optimizer = TrackedPromptOptimizer()
result = optimizer.optimize_and_track("my prompt", target="clarity")
```

### 2. Integration with model_orchestrator.py

```python
from model_orchestrator import ModelOrchestrator
from prompt_history import PromptHistory

class TrackedOrchestrator:
    def __init__(self):
        self.orchestrator = ModelOrchestrator()
        self.history = PromptHistory()

    def execute_and_track(self, prompt, requirements):
        # Execute through orchestrator
        result = self.orchestrator.execute(prompt, requirements)

        # Track with full orchestration metadata
        self.history.save(
            prompt=prompt,
            output=result['output'],
            framework="model-orchestration",
            model=result['model_used'],
            tokens=result.get('tokens'),
            cost=result.get('cost'),
            tags=["orchestrated"] + list(requirements.keys()),
            metadata={
                "requirements": requirements,
                "selected_model": result['model_used'],
                "selection_reason": result.get('reason'),
                "alternatives": result.get('alternatives_considered', [])
            }
        )

        return result

# Usage
orchestrator = TrackedOrchestrator()
result = orchestrator.execute_and_track(
    prompt="Analyze this data",
    requirements={"quality": "high", "speed": "medium"}
)
```

### 3. Integration with feedback_system.py

```python
from feedback_system import FeedbackSystem
from prompt_history import PromptHistory

class IntegratedFeedbackHistory:
    def __init__(self):
        self.feedback = FeedbackSystem()
        self.history = PromptHistory()

    def evaluate_and_track(self, prompt, output, context=None):
        # Get feedback
        feedback = self.feedback.evaluate(output, context)

        # Save to history with feedback scores
        self.history.save(
            prompt=prompt,
            output=output,
            tags=["evaluated"],
            metadata={
                "quality_score": feedback.get('quality_score'),
                "relevance_score": feedback.get('relevance_score'),
                "feedback": feedback,
                "context": context
            }
        )

        return feedback

# Usage
integrated = IntegratedFeedbackHistory()
feedback = integrated.evaluate_and_track(
    prompt="Explain AI",
    output="AI is...",
    context={"audience": "beginners"}
)
```

### 4. Integration with cache_manager.py

```python
from cache_manager import CacheManager
from prompt_history import PromptHistory

class CachedHistoryManager:
    def __init__(self):
        self.cache = CacheManager()
        self.history = PromptHistory()

    def get_or_generate(self, prompt, generator_func, **kwargs):
        # Try cache first
        cached = self.cache.get(prompt)

        if cached:
            # Track cache hit
            self.history.save(
                prompt=prompt,
                output=cached,
                tags=["cache-hit"],
                metadata={"source": "cache"}
            )
            return cached

        # Generate new
        output = generator_func(prompt)

        # Cache it
        self.cache.set(prompt, output)

        # Track generation
        self.history.save(
            prompt=prompt,
            output=output,
            tags=["cache-miss", "generated"],
            metadata={"source": "generated"},
            **kwargs
        )

        return output

# Usage
manager = CachedHistoryManager()
result = manager.get_or_generate(
    prompt="What is ML?",
    generator_func=lambda p: call_ai(p),
    model="gpt-4",
    tokens=100
)
```

## Auto-Tracking Patterns

### Pattern 1: Decorator

```python
from functools import wraps
from prompt_history import PromptHistory

history = PromptHistory()

def track_prompt(framework=None, template=None, tags=None):
    """Decorator to automatically track prompt executions."""
    def decorator(func):
        @wraps(func)
        def wrapper(prompt, *args, **kwargs):
            # Execute function
            result = func(prompt, *args, **kwargs)

            # Extract output (handle different return types)
            if isinstance(result, dict):
                output = result.get('output', str(result))
                metadata = {k: v for k, v in result.items() if k != 'output'}
            else:
                output = str(result)
                metadata = {}

            # Track execution
            history.save(
                prompt=prompt,
                output=output,
                framework=framework,
                template=template,
                tags=tags or ["auto-tracked"],
                metadata=metadata
            )

            return result
        return wrapper
    return decorator

# Usage
@track_prompt(framework="chain-of-thought", tags=["math"])
def solve_math_problem(prompt):
    return {"output": "Solution...", "steps": 3}

result = solve_math_problem("2 + 2 = ?")
```

### Pattern 2: Context Manager

```python
from contextlib import contextmanager
from prompt_history import PromptHistory
import time

history = PromptHistory()

@contextmanager
def track_execution(prompt, **kwargs):
    """Context manager for tracking prompt execution with timing."""
    start_time = time.time()
    result = {"output": None, "error": None}

    try:
        yield result

        # Success - save with timing
        if result["output"]:
            kwargs["metadata"] = kwargs.get("metadata", {})
            kwargs["metadata"]["duration"] = time.time() - start_time
            kwargs["metadata"]["status"] = "success"

            history.save(
                prompt=prompt,
                output=result["output"],
                **kwargs
            )
    except Exception as e:
        # Error - save with error info
        result["error"] = str(e)
        history.save(
            prompt=prompt,
            output=f"ERROR: {str(e)}",
            tags=["error"] + kwargs.get("tags", []),
            metadata={
                "error_type": type(e).__name__,
                "duration": time.time() - start_time,
                "status": "failed"
            }
        )
        raise

# Usage
with track_execution("Explain AI", model="gpt-4", tags=["education"]) as result:
    result["output"] = call_ai_api("Explain AI")
```

### Pattern 3: Callback Class

```python
from prompt_history import PromptHistory

class PromptHistoryCallback:
    """Callback class for integration with event-driven systems."""

    def __init__(self, db_path=None):
        self.history = PromptHistory(db_path)

    def on_prompt_start(self, prompt, **kwargs):
        """Called when prompt execution starts."""
        self.current_prompt = prompt
        self.start_time = time.time()
        self.metadata = kwargs

    def on_prompt_complete(self, output, **kwargs):
        """Called when prompt execution completes."""
        duration = time.time() - self.start_time

        metadata = self.metadata.copy()
        metadata.update(kwargs)
        metadata["duration"] = duration

        self.history.save(
            prompt=self.current_prompt,
            output=output,
            **metadata
        )

    def on_prompt_error(self, error, **kwargs):
        """Called when prompt execution fails."""
        self.history.save(
            prompt=self.current_prompt,
            output=f"ERROR: {str(error)}",
            tags=["error"],
            metadata={
                "error_type": type(error).__name__,
                "error_message": str(error),
                **kwargs
            }
        )

# Usage with an event system
callback = PromptHistoryCallback()

# Register callbacks
ai_client.on("prompt_start", callback.on_prompt_start)
ai_client.on("prompt_complete", callback.on_prompt_complete)
ai_client.on("prompt_error", callback.on_prompt_error)
```

### Pattern 4: Wrapper Class

```python
from prompt_history import PromptHistory

class HistoryTrackedAI:
    """Wrapper that adds history tracking to any AI client."""

    def __init__(self, ai_client, db_path=None):
        self.client = ai_client
        self.history = PromptHistory(db_path)

    def __call__(self, prompt, **kwargs):
        """Make the instance callable."""
        return self.generate(prompt, **kwargs)

    def generate(self, prompt, track=True, **kwargs):
        """Generate with automatic tracking."""
        # Call underlying client
        response = self.client.generate(prompt, **kwargs)

        # Track if enabled
        if track:
            self.history.save(
                prompt=prompt,
                output=response.text,
                model=kwargs.get('model', self.client.model),
                tokens=getattr(response, 'tokens', None),
                cost=getattr(response, 'cost', None),
                framework=kwargs.get('framework'),
                tags=kwargs.get('tags', []),
                metadata=kwargs.get('metadata', {})
            )

        return response

    def search_history(self, query):
        """Search past interactions."""
        return self.history.search(query)

    def get_stats(self):
        """Get usage statistics."""
        return self.history.stats()

# Usage
tracked_ai = HistoryTrackedAI(your_ai_client)

# Use like normal
response = tracked_ai("Explain quantum computing")

# Or disable tracking
response = tracked_ai("Test", track=False)

# Search history
similar = tracked_ai.search_history("quantum")
```

## Advanced Use Cases

### A/B Testing Framework

```python
from prompt_history import PromptHistory
import random

class ABTestingFramework:
    def __init__(self):
        self.history = PromptHistory()

    def test_variants(self, variants, test_prompt, num_runs=10):
        """Test multiple prompt variants."""
        results = {v['name']: [] for v in variants}

        for i in range(num_runs):
            for variant in variants:
                # Execute variant
                output = call_ai(variant['prompt'])

                # Track with A/B metadata
                self.history.save(
                    prompt=variant['prompt'],
                    output=output,
                    framework="ab-testing",
                    tags=["ab-test", variant['name']],
                    metadata={
                        "experiment": test_prompt,
                        "variant": variant['name'],
                        "run": i,
                        "variant_params": variant.get('params', {})
                    }
                )

                results[variant['name']].append(output)

        return results

    def analyze_test(self, test_name):
        """Analyze A/B test results."""
        # Get all test entries
        entries = self.history.search(test_name)

        # Group by variant
        by_variant = {}
        for entry in entries:
            variant = entry.metadata.get('variant')
            if variant not in by_variant:
                by_variant[variant] = []
            by_variant[variant].append(entry)

        return by_variant

# Usage
tester = ABTestingFramework()
variants = [
    {"name": "direct", "prompt": "Explain AI"},
    {"name": "detailed", "prompt": "Explain AI in detail with examples"}
]
results = tester.test_variants(variants, "AI explanation test")
```

### Template Performance Tracking

```python
from prompt_history import PromptHistory

class TemplatePerformanceTracker:
    def __init__(self):
        self.history = PromptHistory()

    def use_template(self, template_name, variables, **kwargs):
        """Use a template and track performance."""
        # Load template
        template = load_template(template_name)
        prompt = template.format(**variables)

        # Execute
        start_time = time.time()
        output = call_ai(prompt)
        duration = time.time() - start_time

        # Track with template metadata
        self.history.save(
            prompt=prompt,
            output=output,
            template=template_name,
            tags=["templated", template_name],
            metadata={
                "template_name": template_name,
                "variables": variables,
                "duration": duration,
                **kwargs
            }
        )

        return output

    def analyze_template(self, template_name):
        """Analyze template performance."""
        entries = self.history.db.get_recent(limit=1000)
        template_entries = [e for e in entries if e.template_used == template_name]

        if not template_entries:
            return None

        total_tokens = sum(e.tokens for e in template_entries if e.tokens)
        total_cost = sum(e.cost for e in template_entries if e.cost)
        avg_duration = sum(
            e.metadata.get('duration', 0)
            for e in template_entries
        ) / len(template_entries)

        return {
            "template": template_name,
            "uses": len(template_entries),
            "total_tokens": total_tokens,
            "total_cost": total_cost,
            "avg_duration": avg_duration
        }

# Usage
tracker = TemplatePerformanceTracker()
output = tracker.use_template(
    "code-review",
    {"code": "def foo(): pass"},
    model="gpt-4"
)
stats = tracker.analyze_template("code-review")
```

### Progressive Prompt Refinement

```python
from prompt_history import PromptHistory

class PromptRefiner:
    def __init__(self):
        self.history = PromptHistory()

    def refine_iteratively(self, initial_prompt, iterations=3):
        """Iteratively refine a prompt based on outputs."""
        current_prompt = initial_prompt
        session_id = f"refine_{int(time.time())}"

        for i in range(iterations):
            # Execute current version
            output = call_ai(current_prompt)

            # Track iteration
            self.history.save(
                prompt=current_prompt,
                output=output,
                framework="iterative-refinement",
                tags=["refinement", f"iteration-{i}"],
                metadata={
                    "session_id": session_id,
                    "iteration": i,
                    "is_final": i == iterations - 1
                }
            )

            if i < iterations - 1:
                # Refine prompt based on output
                current_prompt = self.refine_based_on_output(
                    current_prompt,
                    output
                )

        return output

    def get_refinement_history(self, session_id):
        """Get all iterations for a refinement session."""
        all_entries = self.history.db.get_recent(limit=1000)
        return [
            e for e in all_entries
            if e.metadata.get('session_id') == session_id
        ]

# Usage
refiner = PromptRefiner()
final_output = refiner.refine_iteratively("Explain AI")
```

## Best Practices

### 1. Consistent Tagging

```python
# Define tag constants
TAGS = {
    "PRODUCTION": "production",
    "TESTING": "testing",
    "EXPERIMENT": "experiment",
    "ERROR": "error",
    "HIGH_QUALITY": "high-quality",
}

# Use consistently
history.save(
    prompt=prompt,
    output=output,
    tags=[TAGS["PRODUCTION"], TAGS["HIGH_QUALITY"]]
)
```

### 2. Structured Metadata

```python
# Define metadata structure
def create_metadata(
    experiment_id=None,
    version=None,
    environment=None,
    **kwargs
):
    return {
        "experiment_id": experiment_id,
        "version": version,
        "environment": environment,
        "timestamp": datetime.now().isoformat(),
        **kwargs
    }

# Use consistently
history.save(
    prompt=prompt,
    output=output,
    metadata=create_metadata(
        experiment_id="exp-001",
        version="1.0",
        environment="production"
    )
)
```

### 3. Error Handling

```python
def safe_track(prompt, output, **kwargs):
    """Safely track with error handling."""
    try:
        return history.save(
            prompt=prompt,
            output=output,
            **kwargs
        )
    except Exception as e:
        # Log error but don't fail the main operation
        logger.error(f"Failed to track history: {e}")
        return None
```

### 4. Batch Processing

```python
def process_batch(prompts):
    """Process and track batch of prompts."""
    batch_id = f"batch_{int(time.time())}"

    for i, prompt in enumerate(prompts):
        output = call_ai(prompt)

        history.save(
            prompt=prompt,
            output=output,
            tags=["batch"],
            metadata={
                "batch_id": batch_id,
                "batch_index": i,
                "batch_size": len(prompts)
            }
        )
```

### 5. Regular Exports

```python
import schedule

def export_daily():
    """Export history daily."""
    date_str = datetime.now().strftime("%Y%m%d")
    history.export_json(f"backups/history_{date_str}.json")

# Schedule daily exports
schedule.every().day.at("00:00").do(export_daily)
```

## Summary

The prompt history system integrates seamlessly with existing scripts through:

1. **Simple API**: Easy to add tracking to any function
2. **Flexible Patterns**: Decorators, context managers, callbacks, wrappers
3. **Rich Metadata**: Track anything relevant to your use case
4. **Powerful Search**: Find relevant prompts quickly
5. **Analytics**: Understand usage patterns and performance

Start with simple tracking and expand as needed!
