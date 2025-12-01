#!/usr/bin/env python3
"""
Prompt Optimizer Examples

Practical examples demonstrating various use cases of the prompt optimizer.
"""

from prompt_optimizer import (
    PromptOptimizer,
    OptimizationTechnique,
    PromptVariation,
    EvaluationCriteria
)
from pathlib import Path
import json


def example_1_basic_optimization():
    """Example 1: Basic prompt optimization."""
    print("\n" + "="*80)
    print("EXAMPLE 1: Basic Optimization")
    print("="*80)

    optimizer = PromptOptimizer(provider="anthropic")

    result = optimizer.optimize(
        base_prompt="Summarize this text",
        num_variations=3
    )

    print(f"\nOriginal: {result.original}")
    print(f"Winner: {result.winner.technique_used}")
    print(f"Score: {result.winner.total_score():.2f}/10")
    print(f"Improvement: {result.improvement_percentage:.1f}%")
    print(f"\nOptimized Prompt:\n{result.winner.content}")


def example_2_with_test_cases():
    """Example 2: Optimization with A/B testing."""
    print("\n" + "="*80)
    print("EXAMPLE 2: Optimization with Test Cases")
    print("="*80)

    optimizer = PromptOptimizer(provider="anthropic")

    # Define test cases for email extraction
    test_inputs = [
        "Contact us at support@company.com for help",
        "John Doe (john.doe@example.org) is the manager",
        "Email me at alice_smith123@test.co.uk"
    ]

    expected_outputs = [
        "support@company.com",
        "john.doe@example.org",
        "alice_smith123@test.co.uk"
    ]

    result = optimizer.optimize(
        base_prompt="Extract the email address from the text",
        num_variations=4,
        test_inputs=test_inputs,
        expected_outputs=expected_outputs
    )

    print(f"\nWinner: {result.winner.technique_used}")
    print(f"Score: {result.winner.total_score():.2f}/10")
    print(f"Test Success Rate: {result.winner.average_test_success_rate():.0%}")
    print(f"\nOptimized Prompt:\n{result.winner.content}")

    # Show test results
    print("\nTest Results:")
    for i, test in enumerate(result.winner.test_results, 1):
        status = "✓" if test.success else "✗"
        print(f"  {status} Test {i}: {test.test_input[:50]}...")


def example_3_specific_techniques():
    """Example 3: Using specific optimization techniques."""
    print("\n" + "="*80)
    print("EXAMPLE 3: Specific Techniques")
    print("="*80)

    optimizer = PromptOptimizer(provider="anthropic")

    # Use only specific techniques
    techniques = [
        OptimizationTechnique.MORE_SPECIFIC,
        OptimizationTechnique.WITH_EXAMPLES,
        OptimizationTechnique.STEP_BY_STEP
    ]

    result = optimizer.optimize(
        base_prompt="Analyze the sentiment of this review",
        techniques=techniques
    )

    print(f"\nTechniques used: {[t.value for t in techniques]}")
    print(f"\nWinner: {result.winner.technique_used}")
    print(f"Score: {result.winner.total_score():.2f}/10")

    print("\n--- All Variations ---")
    for i, var in enumerate(result.variations, 1):
        print(f"\n{i}. {var.technique_used} (Score: {var.total_score():.2f})")
        print(f"   Clarity: {var.scores.clarity:.1f} | "
              f"Specificity: {var.scores.specificity:.1f} | "
              f"Examples: {var.scores.examples_quality:.1f}")
        print(f"   Preview: {var.content[:100]}...")


def example_4_iterative_optimization():
    """Example 4: Iterative optimization (multi-round)."""
    print("\n" + "="*80)
    print("EXAMPLE 4: Iterative Optimization")
    print("="*80)

    optimizer = PromptOptimizer(provider="anthropic")

    base_prompt = "Generate a product description"
    current_prompt = base_prompt

    print(f"Starting prompt: {current_prompt}\n")

    # Round 1
    print("--- Round 1 ---")
    result1 = optimizer.optimize(current_prompt, num_variations=3)
    current_prompt = result1.winner.content
    print(f"Best technique: {result1.winner.technique_used}")
    print(f"Score: {result1.winner.total_score():.2f}/10")

    # Round 2 - optimize the winner
    print("\n--- Round 2 ---")
    result2 = optimizer.optimize(current_prompt, num_variations=3)
    current_prompt = result2.winner.content
    print(f"Best technique: {result2.winner.technique_used}")
    print(f"Score: {result2.winner.total_score():.2f}/10")

    print(f"\n--- Final Result ---")
    print(f"Original: {base_prompt}")
    print(f"\nFinal optimized prompt:\n{current_prompt}")


def example_5_batch_optimization():
    """Example 5: Batch optimization of multiple prompts."""
    print("\n" + "="*80)
    print("EXAMPLE 5: Batch Optimization")
    print("="*80)

    optimizer = PromptOptimizer(provider="anthropic")

    # Collection of prompts to optimize
    prompts = [
        "Summarize the article",
        "Extract key entities",
        "Classify the topic",
        "Generate tags"
    ]

    results = []

    print("Optimizing multiple prompts...\n")

    for i, prompt in enumerate(prompts, 1):
        print(f"{i}. Optimizing: '{prompt}'")

        result = optimizer.optimize(
            base_prompt=prompt,
            num_variations=3
        )

        results.append({
            'original': prompt,
            'optimized': result.winner.content,
            'technique': result.winner.technique_used,
            'score': result.winner.total_score(),
            'improvement': result.improvement_percentage
        })

        print(f"   → {result.winner.technique_used} "
              f"(score: {result.winner.total_score():.2f}, "
              f"improvement: {result.improvement_percentage:.1f}%)")

    # Summary
    print("\n--- Summary ---")
    avg_score = sum(r['score'] for r in results) / len(results)
    avg_improvement = sum(r['improvement'] for r in results) / len(results)
    print(f"Average Score: {avg_score:.2f}/10")
    print(f"Average Improvement: {avg_improvement:.1f}%")

    # Most effective technique
    techniques = [r['technique'] for r in results]
    most_common = max(set(techniques), key=techniques.count)
    print(f"Most Effective Technique: {most_common}")


def example_6_custom_evaluation():
    """Example 6: Custom evaluation logic."""
    print("\n" + "="*80)
    print("EXAMPLE 6: Custom Evaluation")
    print("="*80)

    optimizer = PromptOptimizer(provider="anthropic")

    result = optimizer.optimize(
        base_prompt="Write a blog post",
        num_variations=3
    )

    print("Evaluating variations with custom criteria:\n")

    # Custom evaluation: prefer prompts with certain keywords
    priority_keywords = ['structure', 'example', 'format', 'specific']

    for i, var in enumerate(result.variations, 1):
        # Count priority keywords
        keyword_count = sum(
            1 for kw in priority_keywords
            if kw in var.content.lower()
        )

        # Custom score
        base_score = var.total_score()
        keyword_bonus = keyword_count * 0.5
        custom_score = base_score + keyword_bonus

        print(f"{i}. {var.technique_used}")
        print(f"   Base Score: {base_score:.2f}")
        print(f"   Keywords Found: {keyword_count} (+{keyword_bonus:.1f})")
        print(f"   Custom Score: {custom_score:.2f}")

    # Re-rank based on custom score
    custom_ranked = sorted(
        result.variations,
        key=lambda v: v.total_score() + sum(
            0.5 for kw in priority_keywords if kw in v.content.lower()
        ),
        reverse=True
    )

    print(f"\nCustom winner: {custom_ranked[0].technique_used}")


def example_7_save_and_load():
    """Example 7: Saving and loading results."""
    print("\n" + "="*80)
    print("EXAMPLE 7: Save and Load Results")
    print("="*80)

    optimizer = PromptOptimizer(provider="anthropic")

    # Optimize and save
    result = optimizer.optimize(
        base_prompt="Translate this text",
        num_variations=3
    )

    filepath = optimizer.save_results(result, filename="example_translation.json")
    print(f"Results saved to: {filepath}")

    # Load results
    loaded = optimizer.load_results("example_translation.json")
    print(f"\nLoaded results:")
    print(f"  Original: {loaded['original']}")
    print(f"  Winner: {loaded['winner']['technique_used']}")
    print(f"  Score: {loaded['winner']['total_score']:.2f}")

    # Get all winners
    print("\n--- Top Performers from History ---")
    winners = optimizer.get_winning_prompts(min_score=7.0, limit=5)

    for i, winner in enumerate(winners, 1):
        print(f"\n{i}. {winner['technique']} (Score: {winner['score']:.2f})")
        print(f"   Improvement: {winner['improvement']:.1f}%")
        print(f"   Prompt preview: {winner['prompt'][:80]}...")


def example_8_comparison_study():
    """Example 8: Technique comparison study."""
    print("\n" + "="*80)
    print("EXAMPLE 8: Technique Comparison Study")
    print("="*80)

    optimizer = PromptOptimizer(provider="anthropic")

    base_prompt = "Analyze customer feedback"

    # Test each technique individually
    techniques = [
        OptimizationTechnique.MORE_SPECIFIC,
        OptimizationTechnique.MORE_CONCISE,
        OptimizationTechnique.STRUCTURED,
        OptimizationTechnique.WITH_EXAMPLES,
        OptimizationTechnique.ROLE_BASED
    ]

    print(f"Testing techniques on: '{base_prompt}'\n")

    results = []

    for technique in techniques:
        variations = optimizer.generate_variations(
            base_prompt=base_prompt,
            num_variations=1,
            techniques=[technique]
        )

        if variations:
            var = variations[0]
            optimizer.evaluate_prompt(var)

            results.append({
                'technique': technique.value,
                'score': var.total_score(),
                'clarity': var.scores.clarity,
                'specificity': var.scores.specificity,
                'examples': var.scores.examples_quality,
                'content_length': len(var.content)
            })

    # Display comparison
    print("--- Technique Comparison ---")
    print(f"{'Technique':<20} {'Score':<10} {'Clarity':<10} {'Specific':<10} {'Examples':<10} {'Length':<10}")
    print("-" * 80)

    for r in sorted(results, key=lambda x: x['score'], reverse=True):
        print(f"{r['technique']:<20} "
              f"{r['score']:<10.2f} "
              f"{r['clarity']:<10.1f} "
              f"{r['specificity']:<10.1f} "
              f"{r['examples']:<10.1f} "
              f"{r['content_length']:<10}")

    best = max(results, key=lambda x: x['score'])
    print(f"\nBest Technique: {best['technique']} (Score: {best['score']:.2f})")


def example_9_domain_specific():
    """Example 9: Domain-specific optimization."""
    print("\n" + "="*80)
    print("EXAMPLE 9: Domain-Specific Optimization")
    print("="*80)

    optimizer = PromptOptimizer(provider="anthropic")

    # Different domains
    domains = {
        "Code Generation": "Write a Python function",
        "Creative Writing": "Write a short story",
        "Data Analysis": "Analyze this dataset",
        "Customer Support": "Respond to customer inquiry"
    }

    print("Optimizing prompts for different domains:\n")

    for domain, prompt in domains.items():
        print(f"--- {domain} ---")

        result = optimizer.optimize(
            base_prompt=prompt,
            num_variations=3
        )

        print(f"Original: {prompt}")
        print(f"Best technique: {result.winner.technique_used}")
        print(f"Score: {result.winner.total_score():.2f}/10")
        print(f"Optimized: {result.winner.content[:100]}...")
        print()


def example_10_export_library():
    """Example 10: Build a prompt library."""
    print("\n" + "="*80)
    print("EXAMPLE 10: Build Prompt Library")
    print("="*80)

    optimizer = PromptOptimizer(provider="anthropic")

    # Common prompt types to optimize and save
    prompt_library = {
        "summarization": "Summarize the following text",
        "entity_extraction": "Extract named entities",
        "sentiment_analysis": "Analyze sentiment",
        "translation": "Translate this text",
        "classification": "Classify this content"
    }

    library_results = {}

    print("Building optimized prompt library...\n")

    for task, prompt in prompt_library.items():
        print(f"Optimizing: {task}")

        result = optimizer.optimize(
            base_prompt=prompt,
            num_variations=4
        )

        library_results[task] = {
            'original': prompt,
            'optimized': result.winner.content,
            'technique': result.winner.technique_used,
            'score': result.winner.total_score(),
            'metadata': {
                'timestamp': result.timestamp,
                'improvement': result.improvement_percentage
            }
        }

        # Save individual result
        optimizer.save_results(result, filename=f"library_{task}.json")

    # Export complete library
    library_path = optimizer.results_dir / "prompt_library.json"
    with open(library_path, 'w', encoding='utf-8') as f:
        json.dump(library_results, f, indent=2, ensure_ascii=False)

    print(f"\n✓ Library saved to: {library_path}")

    # Display library
    print("\n--- Prompt Library ---")
    for task, data in library_results.items():
        print(f"\n{task.upper()}")
        print(f"  Technique: {data['technique']}")
        print(f"  Score: {data['score']:.2f}/10")
        print(f"  Improvement: {data['metadata']['improvement']:.1f}%")
        print(f"  Prompt: {data['optimized'][:80]}...")


def main():
    """Run all examples."""
    import argparse

    parser = argparse.ArgumentParser(description="Prompt Optimizer Examples")
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
        1: example_1_basic_optimization,
        2: example_2_with_test_cases,
        3: example_3_specific_techniques,
        4: example_4_iterative_optimization,
        5: example_5_batch_optimization,
        6: example_6_custom_evaluation,
        7: example_7_save_and_load,
        8: example_8_comparison_study,
        9: example_9_domain_specific,
        10: example_10_export_library
    }

    try:
        if args.all:
            print("\nRunning all examples...")
            for i in range(1, 11):
                examples[i]()
                input("\nPress Enter to continue to next example...")
        elif args.example:
            examples[args.example]()
        else:
            print("\nAvailable Examples:")
            print("  1. Basic Optimization")
            print("  2. Optimization with Test Cases")
            print("  3. Specific Techniques")
            print("  4. Iterative Optimization")
            print("  5. Batch Optimization")
            print("  6. Custom Evaluation")
            print("  7. Save and Load Results")
            print("  8. Technique Comparison Study")
            print("  9. Domain-Specific Optimization")
            print("  10. Build Prompt Library")
            print("\nUsage:")
            print("  python prompt_optimizer_examples.py --example N")
            print("  python prompt_optimizer_examples.py --all")

    except KeyboardInterrupt:
        print("\n\nInterrupted by user")
    except Exception as e:
        print(f"\nError: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
