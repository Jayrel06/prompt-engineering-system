#!/usr/bin/env python3
"""
Prompt History Integration Examples

Demonstrates how to integrate prompt_history.py with other scripts in the system.
Shows both basic usage and advanced integration patterns.
"""

import sys
from pathlib import Path
from datetime import datetime
from typing import Optional

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from prompt_history import PromptHistory, HistoryEntry


class PromptHistoryIntegration:
    """Integration wrapper for automatic history tracking."""

    def __init__(self, db_path: Optional[Path] = None):
        """Initialize with optional custom database path."""
        self.history = PromptHistory(db_path)

    def track_prompt_execution(
        self,
        prompt: str,
        output: str,
        **kwargs
    ) -> int:
        """
        Track a prompt execution with automatic metadata extraction.

        Args:
            prompt: The prompt text
            output: The output/response
            **kwargs: Additional parameters (framework, model, tokens, etc.)

        Returns:
            Entry ID
        """
        return self.history.save(
            prompt=prompt,
            output=output,
            framework=kwargs.get('framework'),
            template=kwargs.get('template'),
            model=kwargs.get('model'),
            tokens=kwargs.get('tokens'),
            cost=kwargs.get('cost'),
            tags=kwargs.get('tags', []),
            metadata=kwargs.get('metadata', {})
        )


# Example 1: Basic Usage
def example_basic_usage():
    """Basic usage example."""
    print("\n" + "="*80)
    print("EXAMPLE 1: Basic Usage")
    print("="*80)

    history = PromptHistory()

    # Save a simple entry
    entry_id = history.save(
        prompt="What is the capital of France?",
        output="The capital of France is Paris.",
        tags=["geography", "education"],
        model="gpt-4"
    )

    print(f"Saved entry with ID: {entry_id}")

    # Retrieve recent entries
    recent = history.get_recent(limit=1)
    if recent:
        print(f"\nMost recent entry:")
        print(f"  Prompt: {recent[0].prompt}")
        print(f"  Output: {recent[0].output}")
        print(f"  Tags: {recent[0].tags}")


# Example 2: Integration with Chain-of-Thought
def example_chain_of_thought_integration():
    """Example of tracking chain-of-thought prompts."""
    print("\n" + "="*80)
    print("EXAMPLE 2: Chain-of-Thought Integration")
    print("="*80)

    history = PromptHistory()

    prompt = """
Let's solve this step by step:

Question: If a train travels 120 miles in 2 hours, what is its average speed?

Think through this carefully.
"""

    output = """
Step 1: Identify the given information
- Distance: 120 miles
- Time: 2 hours

Step 2: Recall the speed formula
Speed = Distance / Time

Step 3: Calculate
Speed = 120 miles / 2 hours = 60 miles per hour

Answer: The train's average speed is 60 mph.
"""

    entry_id = history.save(
        prompt=prompt,
        output=output,
        framework="chain-of-thought",
        model="gpt-4-turbo",
        tokens=150,
        cost=0.0045,
        tags=["math", "problem-solving", "education"],
        metadata={
            "difficulty": "easy",
            "steps": 3,
            "subject": "physics"
        }
    )

    print(f"Saved chain-of-thought entry: {entry_id}")


# Example 3: Integration with Few-Shot Learning
def example_few_shot_integration():
    """Example of tracking few-shot prompts."""
    print("\n" + "="*80)
    print("EXAMPLE 3: Few-Shot Learning Integration")
    print("="*80)

    history = PromptHistory()

    prompt = """
Classify the sentiment of the following text as positive, negative, or neutral.

Example 1:
Text: "I love this product!"
Sentiment: positive

Example 2:
Text: "This is the worst experience ever."
Sentiment: negative

Example 3:
Text: "The item arrived on time."
Sentiment: neutral

Now classify:
Text: "Amazing quality and fast shipping!"
Sentiment:
"""

    output = "positive"

    entry_id = history.save(
        prompt=prompt,
        output=output,
        framework="few-shot",
        template="sentiment-classification",
        model="claude-3-sonnet",
        tokens=125,
        cost=0.0025,
        tags=["sentiment-analysis", "classification", "few-shot"],
        metadata={
            "examples_count": 3,
            "task": "sentiment_classification",
            "accuracy": "high"
        }
    )

    print(f"Saved few-shot entry: {entry_id}")


# Example 4: Integration with Prompt Templates
def example_template_integration():
    """Example of tracking template-based prompts."""
    print("\n" + "="*80)
    print("EXAMPLE 4: Template Integration")
    print("="*80)

    history = PromptHistory()

    # Simulate using a template
    template_name = "code-review"

    prompt = """
Please review the following code:

```python
def calculate_sum(numbers):
    total = 0
    for num in numbers:
        total += num
    return total
```

Provide feedback on:
1. Code quality
2. Performance
3. Best practices
4. Suggestions for improvement
"""

    output = """
Code Review:

1. Code Quality: The code is clear and readable.

2. Performance: Good for small lists. For very large lists, consider using sum().

3. Best practices:
   - Add docstring
   - Add type hints
   - Handle edge cases (empty list, non-numeric values)

4. Suggestions:
```python
def calculate_sum(numbers: list[float]) -> float:
    '''Calculate the sum of numbers in a list.'''
    if not numbers:
        return 0.0
    return sum(numbers)
```
"""

    entry_id = history.save(
        prompt=prompt,
        output=output,
        framework="structured-output",
        template=template_name,
        model="gpt-4",
        tokens=320,
        cost=0.0096,
        tags=["code-review", "python", "quality"],
        metadata={
            "language": "python",
            "review_aspects": ["quality", "performance", "best-practices"],
            "template_version": "1.0"
        }
    )

    print(f"Saved template-based entry: {entry_id}")


# Example 5: Search and Retrieval
def example_search_and_retrieval():
    """Example of searching and retrieving history."""
    print("\n" + "="*80)
    print("EXAMPLE 5: Search and Retrieval")
    print("="*80)

    history = PromptHistory()

    # Search for entries
    results = history.search("code review", limit=5)
    print(f"\nFound {len(results)} entries matching 'code review'")

    # Get entries by tag
    python_entries = history.get_by_tag("python", limit=5)
    print(f"Found {len(python_entries)} entries with tag 'python'")

    # Get today's entries
    today_entries = history.get_today()
    print(f"Found {len(today_entries)} entries from today")

    # Get statistics
    stats = history.stats()
    print(f"\nTotal entries in database: {stats['total_entries']}")
    print(f"Total tokens used: {stats['total_tokens']:,}")
    print(f"Total cost: ${stats['total_cost']:.2f}")


# Example 6: Automatic Integration Wrapper
def example_auto_tracking():
    """Example of automatic prompt tracking."""
    print("\n" + "="*80)
    print("EXAMPLE 6: Automatic Tracking Wrapper")
    print("="*80)

    integration = PromptHistoryIntegration()

    # Simulate an AI call with automatic tracking
    def call_ai_with_tracking(prompt, model="gpt-4", framework=None):
        """Simulate AI call with automatic history tracking."""
        # This would be your actual AI API call
        output = f"Response to: {prompt[:50]}..."

        # Automatically track
        entry_id = integration.track_prompt_execution(
            prompt=prompt,
            output=output,
            model=model,
            framework=framework,
            tokens=len(prompt.split()) + len(output.split()),  # Simplified
            tags=["auto-tracked"],
            metadata={
                "auto_tracked": True,
                "timestamp": datetime.now().isoformat()
            }
        )

        return output, entry_id

    # Use it
    response, entry_id = call_ai_with_tracking(
        "Explain machine learning in simple terms",
        framework="zero-shot"
    )

    print(f"Response tracked with ID: {entry_id}")


# Example 7: Batch Analysis
def example_batch_analysis():
    """Example of analyzing multiple entries."""
    print("\n" + "="*80)
    print("EXAMPLE 7: Batch Analysis")
    print("="*80)

    history = PromptHistory()

    # Get entries from this week
    week_entries = history.get_this_week()

    if not week_entries:
        print("No entries from this week")
        return

    # Analyze by framework
    framework_counts = {}
    total_tokens = 0
    total_cost = 0.0

    for entry in week_entries:
        # Count frameworks
        framework = entry.framework_used or "unknown"
        framework_counts[framework] = framework_counts.get(framework, 0) + 1

        # Sum tokens and cost
        if entry.tokens:
            total_tokens += entry.tokens
        if entry.cost:
            total_cost += entry.cost

    print(f"\nThis Week's Summary:")
    print(f"  Total entries: {len(week_entries)}")
    print(f"  Total tokens: {total_tokens:,}")
    print(f"  Total cost: ${total_cost:.2f}")
    print(f"\nFrameworks used:")
    for framework, count in sorted(framework_counts.items(), key=lambda x: -x[1]):
        print(f"  {framework}: {count}")


# Example 8: Export and Backup
def example_export():
    """Example of exporting history."""
    print("\n" + "="*80)
    print("EXAMPLE 8: Export and Backup")
    print("="*80)

    history = PromptHistory()

    # Export to JSON
    json_path = Path(__file__).parent.parent / "data" / "exports" / "history_backup.json"
    json_path.parent.mkdir(parents=True, exist_ok=True)

    history.export_json(json_path)
    print(f"Exported to JSON: {json_path}")

    # Export to CSV
    csv_path = Path(__file__).parent.parent / "data" / "exports" / "history_backup.csv"
    history.export_csv(csv_path)
    print(f"Exported to CSV: {csv_path}")


# Example 9: Integration with Model Orchestrator
def example_model_orchestrator_integration():
    """Example of integration with model orchestrator."""
    print("\n" + "="*80)
    print("EXAMPLE 9: Model Orchestrator Integration")
    print("="*80)

    history = PromptHistory()

    # Simulate model orchestrator choosing and executing
    def orchestrate_with_history(prompt, requirements):
        """Simulate model orchestration with history tracking."""
        # Model selection logic would go here
        selected_model = "claude-3-opus"  # Example

        # Execute (simulated)
        output = f"High-quality response from {selected_model}"

        # Track with orchestrator metadata
        entry_id = history.save(
            prompt=prompt,
            output=output,
            framework="model-orchestration",
            model=selected_model,
            tokens=500,
            cost=0.025,
            tags=["orchestrated", "high-quality"],
            metadata={
                "requirements": requirements,
                "selection_reason": "High quality needed",
                "alternatives_considered": ["gpt-4", "claude-3-sonnet"]
            }
        )

        return output, entry_id

    result, entry_id = orchestrate_with_history(
        "Write a comprehensive analysis of quantum computing",
        {"quality": "high", "length": "long"}
    )

    print(f"Orchestrated prompt tracked: {entry_id}")


# Example 10: Error Tracking
def example_error_tracking():
    """Example of tracking failed prompts."""
    print("\n" + "="*80)
    print("EXAMPLE 10: Error Tracking")
    print("="*80)

    history = PromptHistory()

    prompt = "Generate a summary of [invalid input]"
    error_output = "ERROR: Invalid input format. Please provide valid text."

    entry_id = history.save(
        prompt=prompt,
        output=error_output,
        model="gpt-4",
        tags=["error", "invalid-input"],
        metadata={
            "status": "failed",
            "error_type": "validation_error",
            "error_message": "Invalid input format"
        }
    )

    print(f"Error tracked with ID: {entry_id}")
    print("\nThis allows you to:")
    print("  - Analyze common failure patterns")
    print("  - Debug prompt issues")
    print("  - Track error rates by framework/model")


def run_all_examples():
    """Run all examples."""
    print("\n" + "#"*80)
    print("# PROMPT HISTORY INTEGRATION EXAMPLES")
    print("#"*80)

    examples = [
        ("Basic Usage", example_basic_usage),
        ("Chain-of-Thought", example_chain_of_thought_integration),
        ("Few-Shot Learning", example_few_shot_integration),
        ("Template Integration", example_template_integration),
        ("Search & Retrieval", example_search_and_retrieval),
        ("Auto Tracking", example_auto_tracking),
        ("Batch Analysis", example_batch_analysis),
        ("Export & Backup", example_export),
        ("Model Orchestrator", example_model_orchestrator_integration),
        ("Error Tracking", example_error_tracking),
    ]

    for name, example_func in examples:
        try:
            example_func()
        except Exception as e:
            print(f"\nError in {name}: {e}")

    print("\n" + "#"*80)
    print("# Examples complete!")
    print("#"*80)


if __name__ == '__main__':
    run_all_examples()
