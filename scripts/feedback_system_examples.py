#!/usr/bin/env python3
"""
Feedback System Examples

Demonstrates various usage patterns for the feedback system including:
- Basic feedback capture
- Integration with prompt router
- Automated analysis and reporting
- Custom queries and visualizations
"""

import sys
from pathlib import Path
from datetime import datetime, timedelta
import json

# Add scripts to path
sys.path.insert(0, str(Path(__file__).parent))

from feedback_system import (
    FeedbackEntry,
    FeedbackDatabase,
    FeedbackAnalyzer,
    capture_feedback,
    analyze_patterns,
    generate_report,
    suggest_improvements
)
from prompt_router import route_prompt, build_enhanced_prompt


def example_1_basic_capture():
    """Example 1: Basic feedback capture workflow."""
    print("\n" + "=" * 80)
    print("EXAMPLE 1: Basic Feedback Capture")
    print("=" * 80)

    db = FeedbackDatabase()

    # Simulate a user interaction
    user_task = "Explain how blockchain works"
    llm_output = """
    Blockchain is a distributed ledger technology that records transactions across
    multiple computers. Each 'block' contains transaction data and is linked to the
    previous block, forming a 'chain'. This structure makes it extremely difficult
    to alter historical records, providing security and transparency.
    """

    # User provides feedback
    user_rating = 5
    user_likes_it = True
    user_tags = ["technical", "explanation", "blockchain"]

    # Capture the feedback
    entry = capture_feedback(
        prompt=user_task,
        output=llm_output.strip(),
        rating=user_rating,
        thumbs_up=user_likes_it,
        tags=user_tags,
        context={
            "model": "claude-sonnet-4",
            "framework": "direct-answer",
            "timestamp": datetime.now().isoformat()
        },
        notes="Clear and concise explanation",
        db=db
    )

    print(f"\nFeedback captured successfully!")
    print(f"Entry ID: {entry.feedback_id}")


def example_2_router_integration():
    """Example 2: Integration with prompt router."""
    print("\n" + "=" * 80)
    print("EXAMPLE 2: Router Integration")
    print("=" * 80)

    db = FeedbackDatabase()

    # User's task
    task = "Calculate the derivative of f(x) = 3x^2 + 2x + 1"

    # Step 1: Route the prompt
    print("\n1. Routing prompt...")
    routing = route_prompt(task)
    print(f"   Framework: {routing.primary_framework}")
    print(f"   Techniques: {', '.join(routing.techniques)}")
    print(f"   Confidence: {routing.confidence:.0%}")

    # Step 2: Build enhanced prompt
    print("\n2. Building enhanced prompt...")
    enhanced_prompt = build_enhanced_prompt(task, routing)
    print(f"   Enhanced prompt created ({len(enhanced_prompt)} chars)")

    # Step 3: Simulate LLM call
    print("\n3. Getting LLM response...")
    simulated_output = """
    Let me work through this step by step:

    Given: f(x) = 3x^2 + 2x + 1

    Step 1: Apply the power rule to each term
    - d/dx(3x^2) = 3 * 2x^(2-1) = 6x
    - d/dx(2x) = 2 * 1x^(1-1) = 2
    - d/dx(1) = 0 (constant)

    Step 2: Combine the derivatives
    f'(x) = 6x + 2

    Confidence: HIGH - This is a straightforward application of basic calculus rules.
    """

    # Step 4: User provides feedback
    print("\n4. Capturing user feedback...")
    entry = capture_feedback(
        prompt=enhanced_prompt,
        output=simulated_output.strip(),
        rating=5,
        thumbs_up=True,
        tags=["math", "calculus", "step-by-step"],
        context={
            "framework": routing.primary_framework,
            "model": routing.model_recommendation,
            "confidence": routing.confidence,
            "techniques": routing.techniques,
            "original_task": task
        },
        notes="Perfect step-by-step breakdown",
        db=db
    )

    print(f"   Feedback captured: {entry.feedback_id}")


def example_3_batch_feedback():
    """Example 3: Capture feedback for multiple interactions."""
    print("\n" + "=" * 80)
    print("EXAMPLE 3: Batch Feedback Capture")
    print("=" * 80)

    db = FeedbackDatabase()

    # Simulate multiple user interactions
    interactions = [
        {
            "prompt": "Write a Python function to reverse a string",
            "output": "def reverse_string(s):\n    return s[::-1]",
            "rating": 4,
            "thumbs_up": True,
            "tags": ["code", "python", "simple"],
            "framework": "code-generation-chain"
        },
        {
            "prompt": "Explain recursion",
            "output": "Recursion is when a function calls itself...",
            "rating": 3,
            "thumbs_up": False,
            "tags": ["explanation", "technical"],
            "framework": "direct-answer"
        },
        {
            "prompt": "Create a project plan for a website redesign",
            "output": "Phase 1: Discovery...\nPhase 2: Design...",
            "rating": 5,
            "thumbs_up": True,
            "tags": ["planning", "project-management"],
            "framework": "first-principles"
        },
        {
            "prompt": "Compare React vs Vue",
            "output": "React: ...\nVue: ...\nConclusion: ...",
            "rating": 5,
            "thumbs_up": True,
            "tags": ["technical", "comparison", "frameworks"],
            "framework": "decision-matrix"
        },
        {
            "prompt": "fix bug",
            "output": "Need more information...",
            "rating": 1,
            "thumbs_up": False,
            "tags": ["vague", "code"],
            "framework": "direct-answer"
        }
    ]

    print(f"\nCapturing {len(interactions)} feedback entries...")

    for i, interaction in enumerate(interactions, 1):
        entry = capture_feedback(
            prompt=interaction["prompt"],
            output=interaction["output"],
            rating=interaction["rating"],
            thumbs_up=interaction["thumbs_up"],
            tags=interaction["tags"],
            context={
                "framework": interaction["framework"],
                "model": "claude-sonnet-4",
                "batch_id": "example_3"
            },
            db=db
        )
        print(f"  {i}. {entry.feedback_id} - Rating: {entry.rating}/5")

    print(f"\nAll feedback captured successfully!")


def example_4_pattern_analysis():
    """Example 4: Analyze feedback patterns."""
    print("\n" + "=" * 80)
    print("EXAMPLE 4: Pattern Analysis")
    print("=" * 80)

    # First, ensure we have enough data
    example_3_batch_feedback()

    # Now analyze
    print("\nAnalyzing feedback patterns...")
    try:
        analysis = analyze_patterns(days=7, min_samples=3)

        print(f"\nKey Insights:")
        print(f"- Success Rate: {analysis.success_rate:.1%}")
        print(f"- Best Performing Tags:")

        # Sort tags by success rate
        sorted_tags = sorted(
            analysis.tag_performance.items(),
            key=lambda x: x[1]['success_rate'],
            reverse=True
        )

        for tag, perf in sorted_tags[:5]:
            print(f"  • {tag}: {perf['success_rate']:.0%} success ({perf['count']} samples)")

    except ValueError as e:
        print(f"\nNote: {e}")
        print("Run example_3_batch_feedback() first to generate sample data")


def example_5_weekly_report():
    """Example 5: Generate weekly improvement report."""
    print("\n" + "=" * 80)
    print("EXAMPLE 5: Weekly Report Generation")
    print("=" * 80)

    # Ensure we have data
    db = FeedbackDatabase()
    stats = db.get_statistics()

    if stats['total_count'] < 5:
        print("\nGenerating sample data first...")
        example_3_batch_feedback()

    # Generate report
    print("\nGenerating weekly report...")
    report = generate_report(
        period="weekly",
        output_file=None,
        db=db
    )

    print("\nReport Summary:")
    print(f"- Period: {report.period}")
    print(f"- Total Prompts: {report.total_prompts}")
    print(f"- Average Rating: {report.avg_rating:.2f}/5")
    print(f"- Success Rate: {report.success_rate:.1%}")

    if report.improvement_vs_previous:
        direction = "improved" if report.improvement_vs_previous > 0 else "declined"
        print(f"- Trend: {direction} by {abs(report.improvement_vs_previous):.1f}%")


def example_6_custom_queries():
    """Example 6: Custom database queries."""
    print("\n" + "=" * 80)
    print("EXAMPLE 6: Custom Database Queries")
    print("=" * 80)

    db = FeedbackDatabase()

    # Query 1: Get all high-rated feedback
    print("\n1. High-rated feedback (4-5 stars):")
    high_rated = db.get_feedback(min_rating=4, limit=5)
    print(f"   Found {len(high_rated)} entries")

    for entry in high_rated[:3]:
        print(f"\n   - Rating: {entry.rating}/5")
        print(f"     Prompt: {entry.prompt[:60]}...")
        print(f"     Tags: {', '.join(entry.tags)}")

    # Query 2: Get failed prompts (low rating or thumbs down)
    print("\n2. Failed prompts (rating <= 2):")
    failed = db.get_feedback(max_rating=2)
    print(f"   Found {len(failed)} entries")

    for entry in failed[:3]:
        print(f"\n   - Rating: {entry.rating}/5")
        print(f"     Prompt: {entry.prompt[:60]}...")
        if entry.notes:
            print(f"     Notes: {entry.notes}")

    # Query 3: Get feedback by tag
    print("\n3. Code-related feedback:")
    code_feedback = db.get_feedback(tags=["code"])
    print(f"   Found {len(code_feedback)} entries")

    # Query 4: Get recent feedback (last 24 hours)
    print("\n4. Recent feedback (last 24 hours):")
    yesterday = (datetime.now() - timedelta(days=1)).isoformat()
    recent = db.get_feedback(start_date=yesterday)
    print(f"   Found {len(recent)} entries")


def example_7_ai_suggestions():
    """Example 7: Get AI-powered improvement suggestions."""
    print("\n" + "=" * 80)
    print("EXAMPLE 7: AI-Powered Suggestions")
    print("=" * 80)

    # Ensure we have data
    db = FeedbackDatabase()
    stats = db.get_statistics()

    if stats['total_count'] < 5:
        print("\nGenerating sample data first...")
        example_3_batch_feedback()

    print("\nGenerating AI suggestions...")
    print("(Note: Requires ANTHROPIC_API_KEY environment variable)")

    try:
        suggestions = suggest_improvements(
            framework="chain-of-thought",
            days=7,
            limit=3,
            db=db
        )

        print(f"\nReceived {len(suggestions)} suggestions")

    except Exception as e:
        print(f"\nNote: AI suggestions unavailable ({e})")
        print("Falling back to rule-based suggestions")


def example_8_performance_tracking():
    """Example 8: Track performance over time."""
    print("\n" + "=" * 80)
    print("EXAMPLE 8: Performance Tracking Over Time")
    print("=" * 80)

    db = FeedbackDatabase()

    # Get statistics for different time periods
    periods = [
        ("Today", 0, 1),
        ("Yesterday", 1, 2),
        ("This Week", 0, 7),
        ("Last Week", 7, 14),
    ]

    print("\nPerformance Metrics:")
    print(f"{'Period':<15} {'Count':>8} {'Avg Rating':>12} {'Success Rate':>15}")
    print("-" * 55)

    for label, days_back_start, days_back_end in periods:
        start = (datetime.now() - timedelta(days=days_back_end)).isoformat()
        end = (datetime.now() - timedelta(days=days_back_start)).isoformat()

        stats = db.get_statistics(start_date=start, end_date=end)

        if stats['total_count'] > 0:
            print(f"{label:<15} {stats['total_count']:>8} "
                  f"{stats['avg_rating']:>12.2f} "
                  f"{stats['success_rate']:>14.1%}")
        else:
            print(f"{label:<15} {'N/A':>8} {'N/A':>12} {'N/A':>15}")


def example_9_export_data():
    """Example 9: Export feedback data."""
    print("\n" + "=" * 80)
    print("EXAMPLE 9: Export Feedback Data")
    print("=" * 80)

    db = FeedbackDatabase()

    # Get all feedback
    all_feedback = db.get_feedback(limit=100)

    if not all_feedback:
        print("\nNo feedback data to export")
        return

    # Export to JSON
    output_file = Path(__file__).parent.parent / "data" / "feedback_export.json"
    output_file.parent.mkdir(exist_ok=True)

    export_data = {
        "exported_at": datetime.now().isoformat(),
        "total_entries": len(all_feedback),
        "entries": [entry.to_dict() for entry in all_feedback]
    }

    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(export_data, f, indent=2)

    print(f"\nExported {len(all_feedback)} entries to:")
    print(f"  {output_file}")

    # Print summary statistics
    positive = sum(1 for e in all_feedback if e.is_positive())
    negative = sum(1 for e in all_feedback if e.is_negative())
    avg_rating = sum(e.rating for e in all_feedback) / len(all_feedback)

    print(f"\nExport Summary:")
    print(f"  Total: {len(all_feedback)}")
    print(f"  Positive: {positive} ({positive/len(all_feedback):.1%})")
    print(f"  Negative: {negative} ({negative/len(all_feedback):.1%})")
    print(f"  Avg Rating: {avg_rating:.2f}/5")


def example_10_learning_router():
    """Example 10: Router that learns from feedback."""
    print("\n" + "=" * 80)
    print("EXAMPLE 10: Adaptive Router with Learning")
    print("=" * 80)

    class AdaptiveRouter:
        """Router that adapts based on feedback."""

        def __init__(self):
            self.db = FeedbackDatabase()
            self.analyzer = FeedbackAnalyzer(self.db)

        def route_with_learning(self, task, days_to_analyze=7):
            """Route and incorporate feedback insights."""
            # Standard routing
            routing = route_prompt(task)

            print(f"\nInitial routing:")
            print(f"  Framework: {routing.primary_framework}")
            print(f"  Confidence: {routing.confidence:.1%}")

            # Try to learn from feedback
            try:
                analysis = self.analyzer.analyze_patterns(
                    days=days_to_analyze,
                    min_samples=3
                )

                # Check if this framework is performing well
                if routing.primary_framework in analysis.framework_performance:
                    perf = analysis.framework_performance[routing.primary_framework]

                    print(f"\nFramework performance:")
                    print(f"  Success rate: {perf['success_rate']:.1%}")
                    print(f"  Sample size: {perf['count']}")

                    # Adjust confidence
                    if perf['success_rate'] > 0.8:
                        routing.confidence = min(1.0, routing.confidence * 1.1)
                        print(f"  ✓ Boosted confidence to {routing.confidence:.1%}")
                    elif perf['success_rate'] < 0.5:
                        routing.confidence *= 0.9
                        print(f"  ⚠ Lowered confidence to {routing.confidence:.1%}")

            except ValueError:
                print("\nInsufficient feedback data for learning (yet)")

            return routing

    # Demonstrate adaptive routing
    router = AdaptiveRouter()

    tasks = [
        "Calculate the sum of 1 to 100",
        "Write a function to sort a list",
        "Explain the concept of inheritance"
    ]

    for task in tasks:
        print(f"\nTask: {task}")
        routing = router.route_with_learning(task)


def run_all_examples():
    """Run all examples in sequence."""
    examples = [
        ("Basic Capture", example_1_basic_capture),
        ("Router Integration", example_2_router_integration),
        ("Batch Feedback", example_3_batch_feedback),
        ("Pattern Analysis", example_4_pattern_analysis),
        ("Weekly Report", example_5_weekly_report),
        ("Custom Queries", example_6_custom_queries),
        ("AI Suggestions", example_7_ai_suggestions),
        ("Performance Tracking", example_8_performance_tracking),
        ("Export Data", example_9_export_data),
        ("Learning Router", example_10_learning_router),
    ]

    print("\n" + "=" * 80)
    print("FEEDBACK SYSTEM EXAMPLES")
    print("=" * 80)
    print("\nAvailable examples:")
    for i, (name, _) in enumerate(examples, 1):
        print(f"  {i}. {name}")

    print("\nRunning all examples...")

    for name, example_func in examples:
        try:
            example_func()
        except Exception as e:
            print(f"\n⚠ Example '{name}' failed: {e}")
            import traceback
            traceback.print_exc()

    print("\n" + "=" * 80)
    print("All examples completed!")
    print("=" * 80)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Feedback System Examples")
    parser.add_argument(
        "--example",
        type=int,
        choices=range(1, 11),
        help="Run specific example (1-10)"
    )
    parser.add_argument(
        "--all",
        action="store_true",
        help="Run all examples"
    )

    args = parser.parse_args()

    examples = {
        1: example_1_basic_capture,
        2: example_2_router_integration,
        3: example_3_batch_feedback,
        4: example_4_pattern_analysis,
        5: example_5_weekly_report,
        6: example_6_custom_queries,
        7: example_7_ai_suggestions,
        8: example_8_performance_tracking,
        9: example_9_export_data,
        10: example_10_learning_router,
    }

    if args.all:
        run_all_examples()
    elif args.example:
        examples[args.example]()
    else:
        parser.print_help()
        print("\nExamples:")
        print("  python feedback_system_examples.py --example 1")
        print("  python feedback_system_examples.py --all")
