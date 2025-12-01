#!/usr/bin/env python3
"""
Smart Context Selection - Practical Examples

Demonstrates various usage patterns for the smart context system.
"""

import sys
from pathlib import Path

# Add parent to path
sys.path.insert(0, str(Path(__file__).parent))

from smart_context import (
    ContextChunk,
    SemanticScorer,
    EmbeddingCache,
    discover_context_files,
    score_relevance,
    select_context,
    get_dynamic_context,
    format_output,
    compress_context,
    estimate_tokens,
    keyword_similarity
)


def example_1_basic_usage():
    """Example 1: Basic context selection for a task."""
    print("=" * 80)
    print("EXAMPLE 1: Basic Context Selection")
    print("=" * 80)

    # Define task
    task = "Design a new n8n workflow for processing customer emails"

    # Initialize scorer
    scorer = SemanticScorer(use_cache=True)

    # Discover and score context
    chunks = discover_context_files()
    print(f"\nDiscovered {len(chunks)} context files")

    scored = score_relevance(task, chunks, scorer)

    # Select top 5 most relevant
    selected = select_context(scored, top_n=5, max_tokens=5000)

    print(f"Selected {len(selected)} most relevant chunks:")
    for i, chunk in enumerate(selected, 1):
        source_name = Path(chunk.source).name
        print(f"  {i}. {source_name} (score: {chunk.relevance_score:.3f}, "
              f"tokens: {chunk.token_count})")

    print()


def example_2_token_budget():
    """Example 2: Strict token budget management."""
    print("=" * 80)
    print("EXAMPLE 2: Token Budget Management")
    print("=" * 80)

    task = "Debug authentication issues in the API integration"

    # Set strict token budget (e.g., for API cost control)
    max_tokens = 3000

    scorer = SemanticScorer(use_cache=True)
    chunks = discover_context_files()
    scored = score_relevance(task, chunks, scorer)

    # Select within budget
    selected = select_context(scored, max_tokens=max_tokens)

    total_tokens = sum(c.token_count for c in selected)

    print(f"\nToken Budget: {max_tokens}")
    print(f"Tokens Used: {total_tokens}")
    print(f"Tokens Remaining: {max_tokens - total_tokens}")
    print(f"Chunks Selected: {len(selected)}")

    print("\nSelected chunks:")
    for chunk in selected:
        source_name = Path(chunk.source).name
        print(f"  - {source_name}: {chunk.token_count} tokens "
              f"(score: {chunk.relevance_score:.3f})")

    print()


def example_3_category_boosting():
    """Example 3: Boost specific categories for better relevance."""
    print("=" * 80)
    print("EXAMPLE 3: Category Boosting")
    print("=" * 80)

    task = "Implement OAuth2 authentication flow"

    # We know we need technical context, so boost it
    boost_categories = {
        "technical": 0.5,      # 50% boost for technical content
        "framework": 0.3,      # 30% boost for frameworks
    }

    scorer = SemanticScorer(use_cache=True)
    chunks = discover_context_files()

    # Score with boosts
    scored = score_relevance(task, chunks, scorer, boost_categories)

    selected = select_context(scored, top_n=8, max_tokens=6000)

    print(f"\nBoosted categories: {boost_categories}")
    print(f"Selected {len(selected)} chunks:\n")

    for chunk in selected:
        source_name = Path(chunk.source).name
        print(f"  {source_name}")
        print(f"    Category: {chunk.category}")
        print(f"    Score: {chunk.relevance_score:.3f}")
        print()


def example_4_dynamic_context():
    """Example 4: Include dynamic context from environment."""
    print("=" * 80)
    print("EXAMPLE 4: Dynamic Context")
    print("=" * 80)

    task = "Continue development from where we left off yesterday"

    # Get dynamic context
    dynamic = get_dynamic_context()

    print("\nDynamic Context Gathered:")
    for key, value in dynamic.items():
        print(f"\n  {key}:")
        # Truncate long values
        value_str = str(value)
        if len(value_str) > 100:
            value_str = value_str[:100] + "..."
        print(f"    {value_str}")

    # Regular context selection
    scorer = SemanticScorer(use_cache=True)
    chunks = discover_context_files()
    scored = score_relevance(task, chunks, scorer)
    selected = select_context(scored, top_n=3, max_tokens=4000)

    print(f"\nSelected {len(selected)} context chunks + dynamic context")
    print()


def example_5_compression():
    """Example 5: Context compression when needed."""
    print("=" * 80)
    print("EXAMPLE 5: Context Compression")
    print("=" * 80)

    # Create a large chunk
    large_content = """# Large Document

## Introduction

This is a very long document with lots of content that we might need to compress.

## Section 1: Details

Here are many details about the first topic. This includes lots of information
that might not all be necessary.

More paragraphs here...

## Section 2: More Details

Additional content here.

```python
# Code block that will be removed
def example():
    pass
```

## Section 3: Even More

Final section with concluding remarks.
"""

    chunk = ContextChunk(
        source="large_document.md",
        content=large_content,
        category="example"
    )

    print(f"Original chunk:")
    print(f"  Tokens: {chunk.token_count}")
    print(f"  Length: {len(chunk.content)} characters")

    # Compress to fit in 100 tokens
    compressed = compress_context(chunk, max_tokens=100)

    if compressed:
        print(f"\nCompressed chunk:")
        print(f"  Tokens: {compressed.token_count}")
        print(f"  Length: {len(compressed.content)} characters")
        print(f"  Reduction: {((1 - compressed.token_count / chunk.token_count) * 100):.1f}%")
        print(f"\nCompressed content preview:")
        print("  " + compressed.content[:200] + "...")

    print()


def example_6_custom_chunks():
    """Example 6: Add custom context chunks."""
    print("=" * 80)
    print("EXAMPLE 6: Custom Context Chunks")
    print("=" * 80)

    task = "Analyze recent API changes"

    # Create custom chunks (e.g., from external sources)
    custom_chunks = [
        ContextChunk(
            source="recent_api_changes.txt",
            content="API v2.0 introduced OAuth2 support and deprecated basic auth. "
                   "New endpoints for user management added.",
            category="dynamic",
            metadata={"type": "changelog", "version": "2.0"}
        ),
        ContextChunk(
            source="performance_metrics.txt",
            content="Recent monitoring shows 15% improvement in response time "
                   "after database index optimization.",
            category="dynamic",
            metadata={"type": "metrics", "date": "2024-12-01"}
        ),
    ]

    # Discover existing context
    existing_chunks = discover_context_files()

    # Combine all chunks
    all_chunks = existing_chunks + custom_chunks

    print(f"\nTotal chunks: {len(all_chunks)}")
    print(f"  - Existing: {len(existing_chunks)}")
    print(f"  - Custom: {len(custom_chunks)}")

    # Score and select
    scorer = SemanticScorer(use_cache=True)
    scored = score_relevance(task, all_chunks, scorer)
    selected = select_context(scored, top_n=5, max_tokens=3000)

    print(f"\nSelected chunks:")
    for chunk in selected:
        source_name = Path(chunk.source).name
        chunk_type = chunk.metadata.get('type', 'standard')
        print(f"  - {source_name} ({chunk_type}, score: {chunk.relevance_score:.3f})")

    print()


def example_7_similarity_comparison():
    """Example 7: Compare semantic vs keyword similarity."""
    print("=" * 80)
    print("EXAMPLE 7: Similarity Comparison")
    print("=" * 80)

    text1 = "machine learning model training and deployment in production"
    text2 = "ML algorithms for training neural networks in production environment"
    text3 = "cooking recipes and kitchen management techniques"

    print("\nText 1:", text1)
    print("Text 2:", text2)
    print("Text 3:", text3)

    # Keyword similarity
    print("\n--- Keyword Similarity ---")
    score_1_2_kw = keyword_similarity(text1, text2)
    score_1_3_kw = keyword_similarity(text1, text3)

    print(f"Text1 vs Text2: {score_1_2_kw:.3f}")
    print(f"Text1 vs Text3: {score_1_3_kw:.3f}")

    # Semantic similarity (if available)
    try:
        scorer = SemanticScorer(use_cache=False)
        if scorer.use_embeddings:
            print("\n--- Semantic Similarity ---")
            score_1_2_sem = scorer.score_similarity(text1, text2)
            score_1_3_sem = scorer.score_similarity(text1, text3)

            print(f"Text1 vs Text2: {score_1_2_sem:.3f}")
            print(f"Text1 vs Text3: {score_1_3_sem:.3f}")

            print("\n--- Improvement ---")
            print(f"Related texts (1-2): {((score_1_2_sem - score_1_2_kw) * 100):.1f}% better")
            print(f"Unrelated texts (1-3): {((score_1_3_kw - score_1_3_sem) * 100):.1f}% better")
    except Exception as e:
        print(f"\nSemantic similarity not available: {e}")

    print()


def example_8_cache_performance():
    """Example 8: Demonstrate cache performance improvement."""
    print("=" * 80)
    print("EXAMPLE 8: Cache Performance")
    print("=" * 80)

    import time

    task = "How to implement secure authentication in web applications"

    # First run (no cache for this task)
    print("\nFirst run (computing embeddings)...")
    scorer_no_cache = SemanticScorer(use_cache=False)

    start = time.time()
    chunks = discover_context_files()[:10]  # Limit to 10 for speed
    scored = score_relevance(task, chunks, scorer_no_cache)
    time_no_cache = time.time() - start

    print(f"Time: {time_no_cache:.3f} seconds")

    # Second run (with cache)
    print("\nSecond run (using cache)...")
    scorer_cache = SemanticScorer(use_cache=True)

    start = time.time()
    scored = score_relevance(task, chunks, scorer_cache)
    time_cache = time.time() - start

    print(f"Time: {time_cache:.3f} seconds")

    if time_no_cache > time_cache:
        speedup = time_no_cache / time_cache
        print(f"\nSpeedup: {speedup:.1f}x faster with cache")
    else:
        print("\nCache may not be warmed up yet (first run)")

    print()


def example_9_full_pipeline():
    """Example 9: Complete end-to-end pipeline."""
    print("=" * 80)
    print("EXAMPLE 9: Full Pipeline (End-to-End)")
    print("=" * 80)

    # Define task
    task = "Create a comprehensive plan for implementing a new feature"

    print(f"\nTask: {task}")

    # Configure parameters
    config = {
        "max_tokens": 6000,
        "top_n": 10,
        "min_score": 0.15,
        "boost_categories": {
            "identity": 0.3,
            "framework/planning": 0.4,
        },
        "include_dynamic": True
    }

    print(f"\nConfiguration:")
    for key, value in config.items():
        print(f"  {key}: {value}")

    # Execute pipeline
    print("\nExecuting pipeline...")

    # 1. Initialize
    scorer = SemanticScorer(use_cache=True)

    # 2. Discover context
    chunks = discover_context_files()
    print(f"  ✓ Discovered {len(chunks)} context files")

    # 3. Score relevance
    scored = score_relevance(
        task,
        chunks,
        scorer,
        config["boost_categories"]
    )
    print(f"  ✓ Scored all chunks for relevance")

    # 4. Select best context
    selected = select_context(
        scored,
        max_tokens=config["max_tokens"],
        top_n=config["top_n"],
        min_score=config["min_score"]
    )

    total_tokens = sum(c.token_count for c in selected)
    print(f"  ✓ Selected {len(selected)} chunks ({total_tokens} tokens)")

    # 5. Get dynamic context
    dynamic = None
    if config["include_dynamic"]:
        dynamic = get_dynamic_context()
        print(f"  ✓ Gathered dynamic context ({len(dynamic)} items)")

    # 6. Format output
    output = format_output(task, selected, dynamic, include_scores=True)

    print(f"\nOutput generated ({len(output)} characters)")
    print("\nPreview:")
    print("-" * 80)
    print(output[:500] + "\n[...truncated...]")
    print("-" * 80)

    print()


def run_all_examples():
    """Run all examples."""
    examples = [
        ("Basic Usage", example_1_basic_usage),
        ("Token Budget", example_2_token_budget),
        ("Category Boosting", example_3_category_boosting),
        ("Dynamic Context", example_4_dynamic_context),
        ("Compression", example_5_compression),
        ("Custom Chunks", example_6_custom_chunks),
        ("Similarity Comparison", example_7_similarity_comparison),
        ("Cache Performance", example_8_cache_performance),
        ("Full Pipeline", example_9_full_pipeline),
    ]

    print("\n" + "=" * 80)
    print("SMART CONTEXT SELECTION - PRACTICAL EXAMPLES")
    print("=" * 80)
    print("\nAvailable examples:")

    for i, (name, _) in enumerate(examples, 1):
        print(f"  {i}. {name}")

    print()

    choice = input("Enter example number (1-9) or 'all' to run all: ").strip()

    print()

    if choice.lower() == 'all':
        for name, func in examples:
            try:
                func()
            except Exception as e:
                print(f"Error in {name}: {e}\n")
    elif choice.isdigit() and 1 <= int(choice) <= len(examples):
        name, func = examples[int(choice) - 1]
        func()
    else:
        print("Invalid choice. Running all examples...")
        print()
        for name, func in examples:
            try:
                func()
            except Exception as e:
                print(f"Error in {name}: {e}\n")


if __name__ == '__main__':
    # Check if running with argument
    if len(sys.argv) > 1:
        example_num = sys.argv[1]
        if example_num.isdigit():
            examples = [
                example_1_basic_usage,
                example_2_token_budget,
                example_3_category_boosting,
                example_4_dynamic_context,
                example_5_compression,
                example_6_custom_chunks,
                example_7_similarity_comparison,
                example_8_cache_performance,
                example_9_full_pipeline,
            ]
            idx = int(example_num) - 1
            if 0 <= idx < len(examples):
                examples[idx]()
            else:
                print(f"Invalid example number. Choose 1-{len(examples)}")
        else:
            print("Usage: python smart_context_example.py [1-9]")
    else:
        run_all_examples()
