#!/usr/bin/env python3
"""
Quickstart Guide for Feedback System

Interactive tutorial that walks you through the feedback system features.
Run this first to understand how everything works.
"""

import sys
from pathlib import Path

# Add scripts to path
sys.path.insert(0, str(Path(__file__).parent))

from feedback_system import (
    FeedbackDatabase,
    capture_feedback,
    analyze_patterns,
    generate_report
)
from datetime import datetime


def print_header(title):
    """Print a section header."""
    print("\n" + "=" * 80)
    print(title.center(80))
    print("=" * 80)


def step_1_initialize():
    """Step 1: Initialize the database."""
    print_header("STEP 1: Initialize Database")

    print("\nFirst, we need to create the database to store feedback.")
    print("This only needs to be done once.\n")

    db = FeedbackDatabase()

    # Check if already initialized
    if db.db_path.exists():
        print(f"[OK] Database already exists at: {db.db_path}")
    else:
        print("Creating database...")
        db.init_database()
        print(f"[OK] Database created at: {db.db_path}")

    input("\nPress Enter to continue...")


def step_2_capture():
    """Step 2: Capture some feedback."""
    print_header("STEP 2: Capture Feedback")

    print("\nLet's capture some sample feedback entries.")
    print("In a real scenario, this happens after each LLM interaction.\n")

    db = FeedbackDatabase()

    # Sample interactions
    samples = [
        {
            "prompt": "Explain how neural networks learn from data",
            "output": "Neural networks learn through a process called backpropagation...",
            "rating": 5,
            "tags": ["technical", "explanation", "ai"],
            "notes": "Very clear explanation with good examples"
        },
        {
            "prompt": "Write Python code to reverse a list",
            "output": "def reverse_list(lst):\n    return lst[::-1]",
            "rating": 4,
            "tags": ["code", "python"],
            "notes": "Simple and effective"
        },
        {
            "prompt": "do something",
            "output": "I need more context to help you...",
            "rating": 1,
            "tags": ["vague"],
            "notes": "Prompt was too vague"
        },
        {
            "prompt": "Create a project plan for launching a mobile app",
            "output": "Phase 1: Planning...\nPhase 2: Development...\nPhase 3: Testing...",
            "rating": 5,
            "tags": ["planning", "project-management"],
            "notes": "Comprehensive and well-structured"
        },
        {
            "prompt": "Compare React and Vue for building web apps",
            "output": "React: Better for large teams...\nVue: Easier learning curve...",
            "rating": 4,
            "tags": ["technical", "comparison", "web"],
            "notes": "Good balanced comparison"
        }
    ]

    print(f"Capturing {len(samples)} sample feedback entries...\n")

    for i, sample in enumerate(samples, 1):
        entry = capture_feedback(
            prompt=sample["prompt"],
            output=sample["output"],
            rating=sample["rating"],
            thumbs_up=sample["rating"] >= 4,
            tags=sample["tags"],
            context={
                "model": "claude-sonnet-4",
                "framework": "demo",
                "sample_id": i
            },
            notes=sample.get("notes"),
            db=db
        )
        print()

    print(f"[OK] Successfully captured {len(samples)} feedback entries")

    input("\nPress Enter to continue...")


def step_3_query():
    """Step 3: Query the feedback."""
    print_header("STEP 3: Query Feedback")

    print("\nNow let's query the feedback we just captured.\n")

    db = FeedbackDatabase()

    # Query 1: Get all feedback
    all_feedback = db.get_feedback()
    print(f"1. Total feedback entries: {len(all_feedback)}")

    # Query 2: Get only positive feedback
    positive = db.get_feedback(min_rating=4)
    print(f"2. Positive feedback (rating >= 4): {len(positive)}")

    # Query 3: Get negative feedback
    negative = db.get_feedback(max_rating=2)
    print(f"3. Negative feedback (rating <= 2): {len(negative)}")

    # Query 4: Get statistics
    stats = db.get_statistics()
    print(f"\n4. Overall statistics:")
    print(f"   - Average rating: {stats['avg_rating']:.2f}/5")
    print(f"   - Success rate: {stats['success_rate']:.1%}")
    print(f"   - Thumbs up: {stats['thumbs_up_count']}")
    print(f"   - Thumbs down: {stats['thumbs_down_count']}")

    input("\nPress Enter to continue...")


def step_4_analyze():
    """Step 4: Analyze patterns."""
    print_header("STEP 4: Analyze Patterns")

    print("\nNow let's analyze the feedback to find patterns.\n")

    try:
        analysis = analyze_patterns(days=1, min_samples=3)

        print("\n[OK] Analysis complete!")
        print("\nKey insights:")
        print(f"  - Success rate: {analysis.success_rate:.1%}")
        print(f"  - Positive patterns found: {len(analysis.common_positive_patterns)}")
        print(f"  - Negative patterns found: {len(analysis.common_negative_patterns)}")

        print("\nTop recommendations:")
        for i, rec in enumerate(analysis.recommendations[:3], 1):
            print(f"  {i}. {rec}")

        # Show tag performance
        if analysis.tag_performance:
            print("\nTag performance:")
            sorted_tags = sorted(
                analysis.tag_performance.items(),
                key=lambda x: x[1]['success_rate'],
                reverse=True
            )
            for tag, perf in sorted_tags[:5]:
                print(f"  - {tag}: {perf['success_rate']:.0%} success ({perf['count']} samples)")

    except ValueError as e:
        print(f"\n[\!] {e}")

    input("\nPress Enter to continue...")


def step_5_report():
    """Step 5: Generate a report."""
    print_header("STEP 5: Generate Report")

    print("\nLet's generate a weekly improvement report.\n")

    report = generate_report(period="weekly", output_file=None)

    print("\n[OK] Report generated!")
    print("\nKey metrics:")
    print(f"  - Period: {report.period}")
    print(f"  - Total prompts: {report.total_prompts}")
    print(f"  - Avg rating: {report.avg_rating:.2f}/5")
    print(f"  - Success rate: {report.success_rate:.1%}")

    if report.improvement_vs_previous:
        print(f"  - Change: {report.improvement_vs_previous:+.1f}%")

    input("\nPress Enter to continue...")


def step_6_next_steps():
    """Step 6: What's next."""
    print_header("STEP 6: Next Steps")

    print("\nGreat! You've completed the quickstart tutorial.")
    print("\nHere's what you can do next:\n")

    print("1. Integrate into Your Workflow")
    print("   - See: FEEDBACK_INTEGRATION_GUIDE.md")
    print("   - Add feedback capture after each LLM call")
    print()

    print("2. Run More Examples")
    print("   - python feedback_system_examples.py --all")
    print("   - Learn advanced usage patterns")
    print()

    print("3. Set Up Automated Reports")
    print("   - Schedule weekly analysis")
    print("   - Monitor success rate trends")
    print()

    print("4. Use CLI Commands")
    print("   - Capture: python feedback_system.py --capture --prompt '...' --output '...' --rating 5")
    print("   - Analyze: python feedback_system.py --analyze --days 7")
    print("   - Report:  python feedback_system.py --report --period weekly")
    print()

    print("5. Read Documentation")
    print("   - Full guide: FEEDBACK_SYSTEM_README.md")
    print("   - Integration: FEEDBACK_INTEGRATION_GUIDE.md")
    print()

    print("=" * 80)
    print("\nYou're all set! Start capturing feedback to improve your prompts.")
    print("=" * 80)


def run_quickstart():
    """Run the complete quickstart tutorial."""

    print("\n" + "=" * 80)
    print("FEEDBACK SYSTEM QUICKSTART".center(80))
    print("=" * 80)

    print("\nWelcome! This interactive tutorial will guide you through the")
    print("feedback system in 6 easy steps.\n")

    print("You'll learn how to:")
    print("  1. Initialize the database")
    print("  2. Capture feedback")
    print("  3. Query feedback data")
    print("  4. Analyze patterns")
    print("  5. Generate reports")
    print("  6. Next steps for integration")

    input("\nPress Enter to begin...")

    # Run all steps
    steps = [
        step_1_initialize,
        step_2_capture,
        step_3_query,
        step_4_analyze,
        step_5_report,
        step_6_next_steps
    ]

    for step_func in steps:
        try:
            step_func()
        except KeyboardInterrupt:
            print("\n\nQuickstart interrupted. You can resume anytime!")
            sys.exit(0)
        except Exception as e:
            print(f"\n\n[\!] Error in step: {e}")
            import traceback
            traceback.print_exc()
            print("\nContinuing to next step...")


if __name__ == "__main__":
    try:
        run_quickstart()
    except KeyboardInterrupt:
        print("\n\nGoodbye!")
        sys.exit(0)
