#!/usr/bin/env python3
"""
Test suite for token_counter.py

Run with: python test_token_counter.py
"""

import sys
from pathlib import Path

# Import the token counter module
from token_counter import (
    count_tokens,
    estimate_cost,
    check_limits,
    truncate_to_fit,
    summarize_to_fit,
    validate_before_send,
    get_model_info,
    list_supported_models,
    TokenCount,
    MODEL_LIMITS,
    PRICING
)


def test_count_tokens():
    """Test token counting."""
    print("Testing token counting...")

    # Test basic counting
    text = "Hello, world!"
    tokens = count_tokens(text, "gpt-4")
    print(f"  '{text}' -> {tokens} tokens")
    assert tokens > 0, "Token count should be positive"

    # Test empty string
    tokens = count_tokens("", "claude-3-5-sonnet-20241022")
    print(f"  Empty string -> {tokens} tokens")
    assert tokens == 0, "Empty string should have 0 tokens"

    # Test long text
    long_text = " ".join(["word"] * 1000)
    tokens = count_tokens(long_text, "gpt-4o")
    print(f"  1000 words -> {tokens} tokens")
    assert tokens > 500, "1000 words should be more than 500 tokens"

    print("  [PASS] Token counting tests passed\n")


def test_estimate_cost():
    """Test cost estimation."""
    print("Testing cost estimation...")

    # Test GPT-4o
    cost = estimate_cost(1000, 500, "gpt-4o")
    expected = (1000 / 1_000_000 * 2.50) + (500 / 1_000_000 * 10.00)
    print(f"  GPT-4o: 1000 input + 500 output = ${cost:.6f}")
    assert abs(cost - expected) < 0.000001, "Cost calculation incorrect"

    # Test Claude 3.5 Sonnet
    cost = estimate_cost(10000, 2000, "claude-3-5-sonnet-20241022")
    expected = (10000 / 1_000_000 * 3.00) + (2000 / 1_000_000 * 15.00)
    print(f"  Claude 3.5 Sonnet: 10000 input + 2000 output = ${cost:.6f}")
    assert abs(cost - expected) < 0.000001, "Cost calculation incorrect"

    # Test zero tokens
    cost = estimate_cost(0, 0, "gpt-4o-mini")
    print(f"  Zero tokens = ${cost:.6f}")
    assert cost == 0.0, "Zero tokens should cost nothing"

    print("  [PASS] Cost estimation tests passed\n")


def test_check_limits():
    """Test limit checking."""
    print("Testing limit checking...")

    # Test within limits
    within, remaining = check_limits(5000, "gpt-4", output_tokens=1000)
    print(f"  GPT-4 with 5000 tokens (1000 output): within={within}, remaining={remaining}")
    assert within is True, "Should be within limits"
    assert remaining == 8192 - 6000, "Remaining calculation incorrect"

    # Test over limits
    within, remaining = check_limits(150000, "gpt-4")
    print(f"  GPT-4 with 150000 tokens: within={within}, remaining={remaining}")
    assert within is False, "Should exceed limits"
    assert remaining < 0, "Remaining should be negative"

    # Test Claude with large context
    within, remaining = check_limits(100000, "claude-3-5-sonnet-20241022", output_tokens=4000)
    print(f"  Claude 3.5 with 100000 tokens (4000 output): within={within}, remaining={remaining}")
    assert within is True, "Should be within Claude's 200k limit"

    print("  [PASS] Limit checking tests passed\n")


def test_truncate_to_fit():
    """Test truncation."""
    print("Testing truncation...")

    # Create a long text
    long_text = " ".join([f"Word{i}" for i in range(1000)])

    # Test truncate from end
    truncated = truncate_to_fit(long_text, "gpt-4", max_tokens=100, truncate_from="end")
    tokens = count_tokens(truncated, "gpt-4")
    print(f"  Truncated from end: {tokens} tokens")
    assert tokens <= 100, "Truncated text should be within limit"
    assert "[...truncated]" in truncated, "Should have truncation marker"

    # Test truncate from start
    truncated = truncate_to_fit(long_text, "gpt-4", max_tokens=100, truncate_from="start")
    tokens = count_tokens(truncated, "gpt-4")
    print(f"  Truncated from start: {tokens} tokens")
    assert tokens <= 100, "Truncated text should be within limit"
    assert "[...truncated]" in truncated, "Should have truncation marker"

    # Test truncate from middle
    truncated = truncate_to_fit(long_text, "gpt-4", max_tokens=100, truncate_from="middle")
    tokens = count_tokens(truncated, "gpt-4")
    print(f"  Truncated from middle: {tokens} tokens")
    assert tokens <= 100, "Truncated text should be within limit"
    assert "[...truncated...]" in truncated, "Should have middle truncation marker"

    # Test text already within limits
    short_text = "Hello world"
    truncated = truncate_to_fit(short_text, "gpt-4", max_tokens=1000)
    print(f"  Short text (no truncation needed): unchanged={truncated == short_text}")
    assert truncated == short_text, "Short text should not be modified"

    print("  [PASS] Truncation tests passed\n")


def test_summarize_to_fit():
    """Test summarization."""
    print("Testing summarization...")

    # Create structured text
    text = """# Header 1
This is a long paragraph with lots of text that should be reduced.

## Header 2
- List item 1
- List item 2
- List item 3

More text that can be removed.

```python
def important_code():
    pass
```

Even more text that can be removed to fit within limits.
"""

    summarized = summarize_to_fit(text, "gpt-4", max_tokens=50)
    tokens = count_tokens(summarized, "gpt-4")
    print(f"  Summarized text: {tokens} tokens")
    assert tokens <= 50, "Summarized text should be within limit"
    assert "# Header 1" in summarized, "Should preserve headers"
    assert "[Note:" in summarized, "Should have summary note"

    print("  [PASS] Summarization tests passed\n")


def test_validate_before_send():
    """Test validation function."""
    print("Testing validate_before_send...")

    # Test valid prompt
    prompt = "Tell me about AI"
    is_valid, info = validate_before_send(prompt, "gpt-4", max_output_tokens=1000)
    print(f"  Valid prompt: is_valid={is_valid}, tokens={info.input_tokens}")
    assert is_valid, "Short prompt should be valid"
    assert info.within_limit, "Should be within limits"
    assert info.cost_estimate > 0, "Should have cost estimate"

    # Test invalid prompt (too long)
    long_prompt = " ".join(["word"] * 10000)
    is_valid, info = validate_before_send(long_prompt, "gpt-4", max_output_tokens=1000)
    print(f"  Long prompt: is_valid={is_valid}, remaining={info.remaining_tokens}")
    assert not is_valid, "Long prompt should be invalid for GPT-4"
    assert info.remaining_tokens < 0, "Should have negative remaining tokens"

    # Test auto-truncate
    is_valid, info = validate_before_send(
        long_prompt,
        "gpt-4",
        max_output_tokens=1000,
        auto_truncate=True
    )
    print(f"  Auto-truncated: is_valid={is_valid}, tokens={info.input_tokens}")
    # With auto-truncate, it should now be valid
    assert is_valid or info.input_tokens < 10000, "Auto-truncate should reduce tokens"

    print("  [PASS] Validation tests passed\n")


def test_get_model_info():
    """Test model info retrieval."""
    print("Testing get_model_info...")

    # Test Claude model
    info = get_model_info("claude-3-5-sonnet-20241022")
    print(f"  Claude 3.5 Sonnet: {info['context_limit']} tokens, ${info['pricing']['input']}/1M input")
    assert info['provider'] == "Anthropic", "Should identify Anthropic"
    assert info['context_limit'] == 200000, "Should have correct limit"

    # Test GPT model
    info = get_model_info("gpt-4o")
    print(f"  GPT-4o: {info['context_limit']} tokens, ${info['pricing']['input']}/1M input")
    assert info['provider'] == "OpenAI", "Should identify OpenAI"

    # Test Gemini model
    info = get_model_info("gemini-1.5-pro")
    print(f"  Gemini 1.5 Pro: {info['context_limit']} tokens")
    assert info['provider'] == "Google", "Should identify Google"

    print("  [PASS] Model info tests passed\n")


def test_list_supported_models():
    """Test model listing."""
    print("Testing list_supported_models...")

    models = list_supported_models()
    print(f"  Total supported models: {len(models)}")
    assert len(models) > 0, "Should have models"
    assert "claude-3-5-sonnet-20241022" in models, "Should include Claude 3.5"
    assert "gpt-4o" in models, "Should include GPT-4o"
    assert models == sorted(models), "Should be sorted"

    print("  [PASS] Model listing tests passed\n")


def test_token_count_dataclass():
    """Test TokenCount dataclass."""
    print("Testing TokenCount dataclass...")

    result = TokenCount(
        input_tokens=1000,
        output_tokens_estimate=500,
        total=1500,
        model="gpt-4o",
        cost_estimate=0.0075,
        within_limit=True,
        remaining_tokens=126500
    )

    # Test to_dict
    data = result.to_dict()
    print(f"  to_dict: {len(data)} fields")
    assert isinstance(data, dict), "Should be a dict"
    assert data['input_tokens'] == 1000, "Should have correct values"

    # Test to_json
    json_str = result.to_json()
    print(f"  to_json: {len(json_str)} chars")
    assert isinstance(json_str, str), "Should be a string"
    assert '"input_tokens": 1000' in json_str, "Should contain JSON data"

    print("  [PASS] TokenCount dataclass tests passed\n")


def test_edge_cases():
    """Test edge cases and error handling."""
    print("Testing edge cases...")

    # Test unknown model
    tokens = count_tokens("Hello", "unknown-model-xyz")
    print(f"  Unknown model: {tokens} tokens (using approximation)")
    assert tokens > 0, "Should fall back to approximation"

    # Test very long text
    very_long = "x" * 1000000
    tokens = count_tokens(very_long, "claude-3-5-sonnet-20241022")
    print(f"  Very long text (1M chars): {tokens} tokens")
    assert tokens > 100000, "Should count very long text"

    # Test special characters
    special = "Hello 世界 🌍 \n\t\r"
    tokens = count_tokens(special, "gpt-4")
    print(f"  Special characters: {tokens} tokens")
    assert tokens > 0, "Should handle special characters"

    # Test None-like inputs (handled by returning 0)
    tokens = count_tokens("", "gpt-4")
    print(f"  Empty string: {tokens} tokens")
    assert tokens == 0, "Empty should be 0 tokens"

    print("  [PASS] Edge case tests passed\n")


def test_integration_example():
    """Test a realistic integration scenario."""
    print("Testing integration scenario...")

    # Simulate a prompt assembly pipeline
    system_prompt = "You are a helpful AI assistant."
    user_query = "Explain quantum computing in simple terms."
    context = "Previous conversation: [...]"

    # Assemble full prompt
    full_prompt = f"{system_prompt}\n\n{context}\n\nUser: {user_query}\n\nAssistant:"

    # Validate before sending
    is_valid, info = validate_before_send(
        full_prompt,
        model="claude-3-5-sonnet-20241022",
        max_output_tokens=2000
    )

    print(f"  Full prompt validation:")
    print(f"    Input tokens: {info.input_tokens}")
    print(f"    Output tokens (estimate): {info.output_tokens_estimate}")
    print(f"    Total: {info.total}")
    print(f"    Cost estimate: ${info.cost_estimate:.6f}")
    print(f"    Within limit: {info.within_limit}")
    print(f"    Remaining: {info.remaining_tokens}")

    assert is_valid, "Realistic prompt should be valid"
    assert info.cost_estimate > 0, "Should have cost estimate"

    print("  [PASS] Integration scenario test passed\n")


def run_all_tests():
    """Run all tests."""
    print("=" * 80)
    print("Token Counter Test Suite")
    print("=" * 80)
    print()

    tests = [
        test_count_tokens,
        test_estimate_cost,
        test_check_limits,
        test_truncate_to_fit,
        test_summarize_to_fit,
        test_validate_before_send,
        test_get_model_info,
        test_list_supported_models,
        test_token_count_dataclass,
        test_edge_cases,
        test_integration_example,
    ]

    failed = []
    for test in tests:
        try:
            test()
        except Exception as e:
            print(f"  [FAIL] {test.__name__} FAILED: {e}\n")
            failed.append((test.__name__, e))

    print("=" * 80)
    if not failed:
        print("All tests passed! [PASS]")
        print("=" * 80)
        return 0
    else:
        print(f"{len(failed)} test(s) failed:")
        for name, error in failed:
            print(f"  - {name}: {error}")
        print("=" * 80)
        return 1


if __name__ == "__main__":
    sys.exit(run_all_tests())
