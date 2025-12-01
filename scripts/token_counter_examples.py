#!/usr/bin/env python3
"""
Token Counter Integration Examples

Demonstrates how to integrate token_counter.py into your prompt engineering pipeline.

Usage:
    python token_counter_examples.py
"""

from token_counter import (
    count_tokens,
    estimate_cost,
    check_limits,
    validate_before_send,
    truncate_to_fit,
    get_model_info,
    TokenCount
)


def example_1_basic_validation():
    """Example 1: Basic prompt validation before API call."""
    print("=" * 80)
    print("Example 1: Basic Prompt Validation")
    print("=" * 80)

    prompt = "You are a helpful AI assistant.\n\nUser: Explain quantum computing.\n\nAssistant:"

    # Validate before sending
    is_valid, info = validate_before_send(
        prompt=prompt,
        model="gpt-4o",
        max_output_tokens=2000
    )

    print(f"Prompt: {prompt[:50]}...")
    print(f"Model: {info.model}")
    print(f"Input tokens: {info.input_tokens}")
    print(f"Output tokens (estimate): {info.output_tokens_estimate}")
    print(f"Total tokens: {info.total}")
    print(f"Cost estimate: ${info.cost_estimate:.4f}")
    print(f"Within limit: {info.within_limit}")
    print(f"Remaining tokens: {info.remaining_tokens}")

    if is_valid:
        print("\n✓ Safe to send to API!")
    else:
        print(f"\n✗ ERROR: Exceeds limit by {abs(info.remaining_tokens)} tokens")

    print()


def example_2_cost_comparison():
    """Example 2: Compare costs across different models."""
    print("=" * 80)
    print("Example 2: Cost Comparison Across Models")
    print("=" * 80)

    prompt = "Analyze this dataset and provide insights: " + ("data point, " * 100)
    input_tokens = count_tokens(prompt, "gpt-4o")
    output_tokens = 1000

    models = [
        "gpt-4o",
        "gpt-4o-mini",
        "claude-3-5-sonnet-20241022",
        "claude-3-haiku-20240307",
        "gemini-1.5-flash"
    ]

    print(f"Prompt length: {input_tokens} tokens")
    print(f"Expected output: {output_tokens} tokens\n")

    print(f"{'Model':<35} {'Cost':<15} {'Context Limit'}")
    print("-" * 80)

    for model in models:
        cost = estimate_cost(input_tokens, output_tokens, model)
        info = get_model_info(model)
        print(f"{model:<35} ${cost:<14.6f} {info['context_limit']:,} tokens")

    print()


def example_3_auto_truncation():
    """Example 3: Auto-truncate long context."""
    print("=" * 80)
    print("Example 3: Auto-Truncation for Long Context")
    print("=" * 80)

    # Simulate a very long context
    long_context = " ".join([f"Context paragraph {i}." for i in range(1000)])
    user_query = "What are the main points?"

    full_prompt = f"Context:\n{long_context}\n\nQuestion: {user_query}\n\nAnswer:"

    print(f"Original prompt: {count_tokens(full_prompt, 'gpt-4')} tokens")

    # Truncate to fit in GPT-4's 8K context
    truncated = truncate_to_fit(
        full_prompt,
        model="gpt-4",
        output_tokens=1000,
        truncate_from="middle"
    )

    print(f"Truncated prompt: {count_tokens(truncated, 'gpt-4')} tokens")
    print(f"\nTruncated text preview:")
    print(truncated[:200] + "...")
    print()


def example_4_batch_cost_tracking():
    """Example 4: Track costs for batch processing."""
    print("=" * 80)
    print("Example 4: Batch Processing Cost Tracking")
    print("=" * 80)

    prompts = [
        "Summarize this article about AI",
        "Translate this text to French",
        "Generate test cases for this function",
        "Explain this code snippet",
        "Write documentation for this API"
    ]

    model = "claude-3-5-sonnet-20241022"
    max_output = 500

    total_cost = 0.0
    total_tokens = 0

    print(f"Processing {len(prompts)} prompts with {model}\n")

    for i, prompt in enumerate(prompts, 1):
        input_tokens = count_tokens(prompt, model)
        cost = estimate_cost(input_tokens, max_output, model)

        total_cost += cost
        total_tokens += input_tokens + max_output

        print(f"Prompt {i}: {input_tokens} tokens, ${cost:.6f}")

    print(f"\n{'='*40}")
    print(f"Total tokens: {total_tokens}")
    print(f"Total cost: ${total_cost:.4f}")
    print()


def example_5_context_window_management():
    """Example 5: Manage conversation history within context limits."""
    print("=" * 80)
    print("Example 5: Context Window Management")
    print("=" * 80)

    system_prompt = "You are a helpful coding assistant."
    conversation_history = [
        ("user", "How do I create a list in Python?"),
        ("assistant", "You can create a list using square brackets: my_list = [1, 2, 3]"),
        ("user", "How do I add items to it?"),
        ("assistant", "Use the append() method: my_list.append(4)"),
        ("user", "What about removing items?"),
        ("assistant", "Use remove() to remove by value or pop() to remove by index"),
        ("user", "Can you show me list comprehensions?"),
    ]

    model = "gpt-4"
    max_output = 500

    # Build prompt with as much history as fits
    current_prompt = f"{system_prompt}\n\n"

    for role, message in conversation_history:
        test_prompt = current_prompt + f"{role}: {message}\n"

        is_valid, info = validate_before_send(
            test_prompt + "assistant:",
            model=model,
            max_output_tokens=max_output
        )

        if is_valid:
            current_prompt = test_prompt
        else:
            print(f"⚠ Cannot fit entire conversation history")
            print(f"  Dropping early messages to stay within {model} limits")
            break

    current_prompt += "assistant:"

    final_tokens = count_tokens(current_prompt, model)
    print(f"\nFinal prompt: {final_tokens} tokens")
    print(f"Messages included: {len(conversation_history)}")
    print(f"Preview:\n{current_prompt[:200]}...")
    print()


def example_6_pre_send_validation():
    """Example 6: Validate-before-send integration pattern."""
    print("=" * 80)
    print("Example 6: Pre-Send Validation Pattern")
    print("=" * 80)

    def send_to_api(prompt: str, model: str, max_output: int = 2000):
        """Wrapper function that validates before sending."""

        # Validate first
        is_valid, info = validate_before_send(
            prompt=prompt,
            model=model,
            max_output_tokens=max_output
        )

        if not is_valid:
            raise ValueError(
                f"Prompt exceeds context limit by {abs(info.remaining_tokens)} tokens. "
                f"Limit: {get_model_info(model)['context_limit']}, "
                f"Needed: {info.total}"
            )

        # Log cost
        print(f"Sending to {model}:")
        print(f"  Tokens: {info.input_tokens} input + {max_output} output")
        print(f"  Cost: ${info.cost_estimate:.4f}")

        # In production, this would actually call the API
        print("  Status: ✓ Would send to API (simulation)")

        return info

    # Example usage
    try:
        prompt = "Explain machine learning in simple terms."
        info = send_to_api(prompt, "gpt-4o", max_output=1000)
        print(f"  Result: Success, used {info.input_tokens} tokens\n")
    except ValueError as e:
        print(f"  Error: {e}\n")


def example_7_model_selection():
    """Example 7: Select cheapest model that fits requirements."""
    print("=" * 80)
    print("Example 7: Smart Model Selection")
    print("=" * 80)

    prompt = "Simple question: What is 2+2?"
    expected_output = 50  # Simple answer

    # Models to consider (cheapest to most expensive)
    candidates = [
        "gpt-4o-mini",
        "claude-3-haiku-20240307",
        "gpt-4o",
        "claude-3-5-sonnet-20241022",
        "gpt-4-turbo"
    ]

    input_tokens = count_tokens(prompt, candidates[0])

    print(f"Finding best model for: '{prompt}'")
    print(f"Input tokens: {input_tokens}, Expected output: {expected_output}\n")

    best_model = None
    best_cost = float('inf')

    for model in candidates:
        within_limit, remaining = check_limits(input_tokens, model, expected_output)

        if within_limit:
            cost = estimate_cost(input_tokens, expected_output, model)
            print(f"{model:<35} ${cost:.6f} {'✓' if cost < best_cost else ''}")

            if cost < best_cost:
                best_cost = cost
                best_model = model

    print(f"\nRecommended: {best_model} (${best_cost:.6f})")
    print()


def main():
    """Run all examples."""
    print("\n")
    print("╔" + "═" * 78 + "╗")
    print("║" + " TOKEN COUNTER INTEGRATION EXAMPLES ".center(78) + "║")
    print("╚" + "═" * 78 + "╝")
    print()

    examples = [
        example_1_basic_validation,
        example_2_cost_comparison,
        example_3_auto_truncation,
        example_4_batch_cost_tracking,
        example_5_context_window_management,
        example_6_pre_send_validation,
        example_7_model_selection,
    ]

    for example in examples:
        try:
            example()
            input("Press Enter to continue to next example...")
            print("\n")
        except KeyboardInterrupt:
            print("\n\nExamples interrupted by user.")
            break
        except Exception as e:
            print(f"Error in {example.__name__}: {e}")
            continue

    print("=" * 80)
    print("All examples completed!")
    print("=" * 80)


if __name__ == "__main__":
    main()
