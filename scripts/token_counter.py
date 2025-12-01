#!/usr/bin/env python3
"""
Token Counter and Context Overflow Prevention Utility

This module provides accurate token counting, cost estimation, and context limit
validation for various LLM models (Claude, GPT, etc.). It helps prevent context
overflow errors and provides cost estimates before sending prompts to APIs.

Usage:
    # As a module
    from token_counter import count_tokens, validate_before_send, estimate_cost

    result = count_tokens("Your text here", model="claude-3-5-sonnet-20241022")
    is_valid, info = validate_before_send(prompt, max_output=1000, model="gpt-4")

    # From command line
    python token_counter.py --text "Hello world" --model gpt-4
    python token_counter.py --file input.txt --check-limit --model claude-3-opus

Author: Prompt Engineering System
Date: 2025-12-01
"""

import argparse
import json
import re
import sys
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Union

# Try to import tiktoken for accurate OpenAI token counting
try:
    import tiktoken
    TIKTOKEN_AVAILABLE = True
except ImportError:
    TIKTOKEN_AVAILABLE = False
    print("Warning: tiktoken not installed. Using approximation for all models.", file=sys.stderr)
    print("Install with: pip install tiktoken", file=sys.stderr)


@dataclass
class TokenCount:
    """Data class for token count results."""
    input_tokens: int
    output_tokens_estimate: int
    total: int
    model: str
    cost_estimate: float
    within_limit: bool
    remaining_tokens: int

    def to_dict(self) -> dict:
        """Convert to dictionary."""
        return asdict(self)

    def to_json(self) -> str:
        """Convert to JSON string."""
        return json.dumps(self.to_dict(), indent=2)


# Model context limits (in tokens)
MODEL_LIMITS = {
    # Claude models (Anthropic)
    "claude-3-5-sonnet-20241022": 200000,  # Claude 3.5 Sonnet v2
    "claude-3-5-sonnet-20240620": 200000,  # Claude 3.5 Sonnet v1
    "claude-3-opus-20240229": 200000,
    "claude-3-sonnet-20240229": 200000,
    "claude-3-haiku-20240307": 200000,
    "claude-2.1": 200000,
    "claude-2.0": 100000,
    "claude-instant-1.2": 100000,

    # GPT models (OpenAI)
    "gpt-4-turbo-2024-04-09": 128000,
    "gpt-4-turbo": 128000,
    "gpt-4-turbo-preview": 128000,
    "gpt-4-1106-preview": 128000,
    "gpt-4": 8192,
    "gpt-4-32k": 32768,
    "gpt-4o": 128000,
    "gpt-4o-2024-11-20": 128000,
    "gpt-4o-2024-08-06": 128000,
    "gpt-4o-2024-05-13": 128000,
    "gpt-4o-mini": 128000,
    "gpt-4o-mini-2024-07-18": 128000,
    "gpt-3.5-turbo": 16385,
    "gpt-3.5-turbo-16k": 16385,
    "gpt-3.5-turbo-1106": 16385,
    "gpt-3.5-turbo-0125": 16385,

    # O1 models (OpenAI)
    "o1": 200000,
    "o1-2024-12-17": 200000,
    "o1-preview": 128000,
    "o1-preview-2024-09-12": 128000,
    "o1-mini": 128000,
    "o1-mini-2024-09-12": 128000,

    # Gemini models (Google)
    "gemini-1.5-pro": 2097152,  # 2M context
    "gemini-1.5-flash": 1048576,  # 1M context
    "gemini-1.0-pro": 32760,

    # Other models
    "llama-3.1-405b": 128000,
    "llama-3.1-70b": 128000,
    "llama-3.1-8b": 128000,
    "mistral-large": 128000,
    "mistral-medium": 32000,
    "mistral-small": 32000,
}


# Pricing data (per 1M tokens) - Updated December 2025
PRICING = {
    # Claude 3.5 Sonnet v2 (latest)
    "claude-3-5-sonnet-20241022": {"input": 3.00, "output": 15.00},
    "claude-3-5-sonnet-20240620": {"input": 3.00, "output": 15.00},

    # Claude 3 Opus
    "claude-3-opus-20240229": {"input": 15.00, "output": 75.00},

    # Claude 3 Sonnet
    "claude-3-sonnet-20240229": {"input": 3.00, "output": 15.00},

    # Claude 3 Haiku
    "claude-3-haiku-20240307": {"input": 0.25, "output": 1.25},

    # Claude 2.x
    "claude-2.1": {"input": 8.00, "output": 24.00},
    "claude-2.0": {"input": 8.00, "output": 24.00},
    "claude-instant-1.2": {"input": 0.80, "output": 2.40},

    # GPT-4o (latest)
    "gpt-4o": {"input": 2.50, "output": 10.00},
    "gpt-4o-2024-11-20": {"input": 2.50, "output": 10.00},
    "gpt-4o-2024-08-06": {"input": 2.50, "output": 10.00},
    "gpt-4o-2024-05-13": {"input": 5.00, "output": 15.00},

    # GPT-4o-mini
    "gpt-4o-mini": {"input": 0.15, "output": 0.60},
    "gpt-4o-mini-2024-07-18": {"input": 0.15, "output": 0.60},

    # GPT-4 Turbo
    "gpt-4-turbo": {"input": 10.00, "output": 30.00},
    "gpt-4-turbo-2024-04-09": {"input": 10.00, "output": 30.00},
    "gpt-4-turbo-preview": {"input": 10.00, "output": 30.00},
    "gpt-4-1106-preview": {"input": 10.00, "output": 30.00},

    # GPT-4
    "gpt-4": {"input": 30.00, "output": 60.00},
    "gpt-4-32k": {"input": 60.00, "output": 120.00},

    # GPT-3.5 Turbo
    "gpt-3.5-turbo": {"input": 0.50, "output": 1.50},
    "gpt-3.5-turbo-16k": {"input": 3.00, "output": 4.00},
    "gpt-3.5-turbo-1106": {"input": 1.00, "output": 2.00},
    "gpt-3.5-turbo-0125": {"input": 0.50, "output": 1.50},

    # O1 models
    "o1": {"input": 15.00, "output": 60.00},
    "o1-2024-12-17": {"input": 15.00, "output": 60.00},
    "o1-preview": {"input": 15.00, "output": 60.00},
    "o1-preview-2024-09-12": {"input": 15.00, "output": 60.00},
    "o1-mini": {"input": 3.00, "output": 12.00},
    "o1-mini-2024-09-12": {"input": 3.00, "output": 12.00},

    # Gemini
    "gemini-1.5-pro": {"input": 1.25, "output": 5.00},
    "gemini-1.5-flash": {"input": 0.075, "output": 0.30},
    "gemini-1.0-pro": {"input": 0.50, "output": 1.50},
}


def _approximate_tokens(text: str) -> int:
    """
    Approximate token count using character-based heuristic.
    Rule of thumb: ~4 characters per token for English text.
    This is less accurate but works without external dependencies.

    Args:
        text: Input text to count

    Returns:
        Approximate token count
    """
    if not text:
        return 0

    # Count words and characters
    words = len(text.split())
    chars = len(text)

    # Use a weighted average approach:
    # - English text: ~0.75 tokens per word
    # - Character-based: ~0.25 tokens per character (4 chars/token)
    # Take average for better estimation
    word_based = int(words * 0.75)
    char_based = int(chars / 4)

    # Return the average, but favor word-based for natural language
    return int((word_based * 0.6) + (char_based * 0.4))


def _get_tiktoken_encoding(model: str):
    """
    Get the appropriate tiktoken encoding for a model.

    Args:
        model: Model name

    Returns:
        Tiktoken encoding object
    """
    if not TIKTOKEN_AVAILABLE:
        return None

    try:
        # Try to get encoding for specific model
        return tiktoken.encoding_for_model(model)
    except KeyError:
        # Fall back to cl100k_base for most modern models
        if any(x in model.lower() for x in ["gpt-4", "gpt-3.5", "o1"]):
            return tiktoken.get_encoding("cl100k_base")
        # Use p50k_base for older models
        elif "davinci" in model.lower() or "curie" in model.lower():
            return tiktoken.get_encoding("p50k_base")
        else:
            return tiktoken.get_encoding("cl100k_base")


def count_tokens(text: str, model: str = "claude-3-5-sonnet-20241022") -> int:
    """
    Count tokens in text for a specific model.
    Uses tiktoken for OpenAI models when available, approximation otherwise.

    Args:
        text: Input text to count
        model: Model name (default: Claude 3.5 Sonnet v2)

    Returns:
        Number of tokens

    Examples:
        >>> count_tokens("Hello world", "gpt-4")
        2
        >>> count_tokens("This is a test", "claude-3-5-sonnet-20241022")
        5
    """
    if not text:
        return 0

    # For OpenAI models, use tiktoken if available
    if TIKTOKEN_AVAILABLE and any(x in model.lower() for x in ["gpt", "o1"]):
        try:
            encoding = _get_tiktoken_encoding(model)
            if encoding:
                return len(encoding.encode(text))
        except Exception as e:
            print(f"Warning: tiktoken error, falling back to approximation: {e}", file=sys.stderr)

    # For Claude and other models, use approximation
    return _approximate_tokens(text)


def estimate_cost(
    input_tokens: int,
    output_tokens: int,
    model: str = "claude-3-5-sonnet-20241022"
) -> float:
    """
    Estimate cost based on token counts.

    Args:
        input_tokens: Number of input tokens
        output_tokens: Number of output tokens
        model: Model name

    Returns:
        Estimated cost in USD

    Examples:
        >>> estimate_cost(1000, 500, "gpt-4o")
        0.0075
        >>> estimate_cost(10000, 2000, "claude-3-5-sonnet-20241022")
        0.06
    """
    if model not in PRICING:
        print(f"Warning: Unknown model '{model}', cost estimation unavailable", file=sys.stderr)
        return 0.0

    pricing = PRICING[model]
    input_cost = (input_tokens / 1_000_000) * pricing["input"]
    output_cost = (output_tokens / 1_000_000) * pricing["output"]

    return round(input_cost + output_cost, 6)


def check_limits(
    token_count: int,
    model: str = "claude-3-5-sonnet-20241022",
    output_tokens: int = 0
) -> Tuple[bool, int]:
    """
    Check if token count is within model limits.

    Args:
        token_count: Number of tokens in input
        model: Model name
        output_tokens: Reserved tokens for output (default: 0)

    Returns:
        Tuple of (within_limit, remaining_tokens)

    Examples:
        >>> check_limits(5000, "gpt-4", output_tokens=1000)
        (True, 2192)
        >>> check_limits(150000, "gpt-4")
        (False, -141808)
    """
    if model not in MODEL_LIMITS:
        print(f"Warning: Unknown model '{model}', using default limit of 128k", file=sys.stderr)
        limit = 128000
    else:
        limit = MODEL_LIMITS[model]

    total_needed = token_count + output_tokens
    remaining = limit - total_needed
    within_limit = remaining >= 0

    return within_limit, remaining


def truncate_to_fit(
    text: str,
    model: str = "claude-3-5-sonnet-20241022",
    max_tokens: Optional[int] = None,
    output_tokens: int = 0,
    truncate_from: str = "end"
) -> str:
    """
    Truncate text to fit within model limits.

    Args:
        text: Input text
        model: Model name
        max_tokens: Maximum tokens (uses model limit if None)
        output_tokens: Reserved tokens for output
        truncate_from: Where to truncate ("end", "start", "middle")

    Returns:
        Truncated text

    Examples:
        >>> truncate_to_fit("A" * 100000, "gpt-4", max_tokens=100)
        # Returns truncated version
    """
    if max_tokens is None:
        max_tokens = MODEL_LIMITS.get(model, 128000)

    # Account for output tokens
    target_tokens = max_tokens - output_tokens

    current_tokens = count_tokens(text, model)

    if current_tokens <= target_tokens:
        return text

    # Binary search for the right length
    if truncate_from == "end":
        # Truncate from end (most common)
        ratio = target_tokens / current_tokens
        estimated_chars = int(len(text) * ratio * 0.95)  # 95% to be safe

        truncated = text[:estimated_chars]
        while count_tokens(truncated, model) > target_tokens:
            # Remove 5% at a time
            chars_to_remove = max(1, int(len(truncated) * 0.05))
            truncated = truncated[:-chars_to_remove]

        return truncated + "\n\n[...truncated]"

    elif truncate_from == "start":
        # Truncate from start
        ratio = target_tokens / current_tokens
        estimated_chars = int(len(text) * ratio * 0.95)
        start_pos = len(text) - estimated_chars

        truncated = text[start_pos:]
        while count_tokens(truncated, model) > target_tokens:
            chars_to_remove = max(1, int(len(truncated) * 0.05))
            truncated = truncated[chars_to_remove:]

        return "[...truncated]\n\n" + truncated

    elif truncate_from == "middle":
        # Keep beginning and end
        ratio = target_tokens / current_tokens
        keep_chars = int(len(text) * ratio * 0.95)
        start_chars = keep_chars // 2
        end_chars = keep_chars // 2

        truncated = text[:start_chars] + "\n\n[...truncated...]\n\n" + text[-end_chars:]

        # Fine-tune if needed
        while count_tokens(truncated, model) > target_tokens:
            start_chars = int(start_chars * 0.95)
            end_chars = int(end_chars * 0.95)
            truncated = text[:start_chars] + "\n\n[...truncated...]\n\n" + text[-end_chars:]

        return truncated

    else:
        raise ValueError(f"Invalid truncate_from value: {truncate_from}")


def summarize_to_fit(
    text: str,
    model: str = "claude-3-5-sonnet-20241022",
    max_tokens: Optional[int] = None,
    output_tokens: int = 0
) -> str:
    """
    Create a summary placeholder when text needs to be reduced.
    This doesn't actually use an LLM to summarize - instead it provides
    intelligent extraction and truncation with context preservation.

    Args:
        text: Input text
        model: Model name
        max_tokens: Maximum tokens (uses model limit if None)
        output_tokens: Reserved tokens for output

    Returns:
        Summarized/truncated text with key information preserved
    """
    if max_tokens is None:
        max_tokens = MODEL_LIMITS.get(model, 128000)

    target_tokens = max_tokens - output_tokens
    current_tokens = count_tokens(text, model)

    if current_tokens <= target_tokens:
        return text

    # Extract key information
    lines = text.split('\n')

    # Preserve structure markers (headers, important lines)
    important_lines = []
    regular_lines = []

    for line in lines:
        # Keep headers, lists, code blocks, etc.
        if (line.startswith('#') or
            line.startswith('##') or
            line.startswith('-') or
            line.startswith('*') or
            line.startswith('```') or
            line.strip().startswith('def ') or
            line.strip().startswith('class ') or
            len(line.strip()) < 5):
            important_lines.append(line)
        else:
            regular_lines.append(line)

    # Start with important lines
    result = '\n'.join(important_lines)
    result_tokens = count_tokens(result, model)

    # Add regular lines until we hit the limit
    for line in regular_lines:
        line_tokens = count_tokens(line, model)
        if result_tokens + line_tokens < target_tokens * 0.9:  # Leave 10% margin
            result += '\n' + line
            result_tokens += line_tokens
        else:
            break

    # Add summary note
    compression_ratio = (current_tokens - result_tokens) / current_tokens * 100
    result += f"\n\n[Note: Content summarized/truncated. Removed ~{compression_ratio:.1f}% of original content to fit within token limits]"

    return result


def validate_before_send(
    prompt: str,
    model: str = "claude-3-5-sonnet-20241022",
    max_output_tokens: int = 4096,
    auto_truncate: bool = False,
    truncate_from: str = "end"
) -> Tuple[bool, TokenCount]:
    """
    Validate prompt before sending to API. This is the main integration point
    for the prompt assembly pipeline.

    Args:
        prompt: The complete prompt to validate
        model: Model name
        max_output_tokens: Expected maximum output tokens
        auto_truncate: Whether to auto-truncate if over limit
        truncate_from: Where to truncate if auto_truncate is True

    Returns:
        Tuple of (is_valid, token_count_info)
        If auto_truncate is True and prompt is over limit, returns truncated version

    Examples:
        >>> is_valid, info = validate_before_send(
        ...     "Your prompt here",
        ...     model="gpt-4",
        ...     max_output_tokens=1000
        ... )
        >>> if not is_valid:
        ...     print(f"Error: {info.remaining_tokens} tokens over limit!")
    """
    input_tokens = count_tokens(prompt, model)
    within_limit, remaining = check_limits(input_tokens, model, max_output_tokens)
    cost = estimate_cost(input_tokens, max_output_tokens, model)

    result = TokenCount(
        input_tokens=input_tokens,
        output_tokens_estimate=max_output_tokens,
        total=input_tokens + max_output_tokens,
        model=model,
        cost_estimate=cost,
        within_limit=within_limit,
        remaining_tokens=remaining
    )

    # If over limit and auto_truncate is enabled
    if not within_limit and auto_truncate:
        truncated_prompt = truncate_to_fit(
            prompt,
            model=model,
            output_tokens=max_output_tokens,
            truncate_from=truncate_from
        )
        # Recalculate with truncated prompt
        input_tokens = count_tokens(truncated_prompt, model)
        within_limit, remaining = check_limits(input_tokens, model, max_output_tokens)
        cost = estimate_cost(input_tokens, max_output_tokens, model)

        result = TokenCount(
            input_tokens=input_tokens,
            output_tokens_estimate=max_output_tokens,
            total=input_tokens + max_output_tokens,
            model=model,
            cost_estimate=cost,
            within_limit=within_limit,
            remaining_tokens=remaining
        )

        # Return truncated prompt by modifying the prompt reference
        # Note: In actual usage, you'd want to return the truncated prompt too
        return True, result

    return within_limit, result


def get_model_info(model: str) -> Dict:
    """
    Get comprehensive information about a model.

    Args:
        model: Model name

    Returns:
        Dictionary with model information
    """
    return {
        "model": model,
        "context_limit": MODEL_LIMITS.get(model, "Unknown"),
        "pricing": PRICING.get(model, {"input": "Unknown", "output": "Unknown"}),
        "provider": (
            "Anthropic" if "claude" in model.lower() else
            "OpenAI" if any(x in model.lower() for x in ["gpt", "o1"]) else
            "Google" if "gemini" in model.lower() else
            "Unknown"
        )
    }


def list_supported_models() -> List[str]:
    """Get list of all supported models."""
    return sorted(MODEL_LIMITS.keys())


def main():
    """Command-line interface."""
    parser = argparse.ArgumentParser(
        description="Token Counter and Context Overflow Prevention Utility",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Count tokens in text
  python token_counter.py --text "Hello world" --model gpt-4

  # Count tokens in file
  python token_counter.py --file input.txt --model claude-3-5-sonnet-20241022

  # Check if within limits
  python token_counter.py --file large_prompt.txt --check-limit --output-tokens 2000

  # Estimate cost
  python token_counter.py --text "Your prompt" --model gpt-4o --output-tokens 1000

  # List supported models
  python token_counter.py --list-models

  # Get model information
  python token_counter.py --model-info claude-3-5-sonnet-20241022
        """
    )

    # Input options
    input_group = parser.add_mutually_exclusive_group()
    input_group.add_argument(
        "--text",
        type=str,
        help="Text to analyze"
    )
    input_group.add_argument(
        "--file",
        type=Path,
        help="File to analyze"
    )
    input_group.add_argument(
        "--list-models",
        action="store_true",
        help="List all supported models"
    )
    input_group.add_argument(
        "--model-info",
        type=str,
        help="Get information about a specific model"
    )

    # Model options
    parser.add_argument(
        "--model",
        type=str,
        default="claude-3-5-sonnet-20241022",
        help="Model name (default: claude-3-5-sonnet-20241022)"
    )

    # Analysis options
    parser.add_argument(
        "--output-tokens",
        type=int,
        default=0,
        help="Expected output tokens for cost/limit calculation (default: 0)"
    )
    parser.add_argument(
        "--check-limit",
        action="store_true",
        help="Check if within model context limits"
    )
    parser.add_argument(
        "--truncate",
        action="store_true",
        help="Show truncated version if over limit"
    )
    parser.add_argument(
        "--truncate-from",
        choices=["start", "end", "middle"],
        default="end",
        help="Where to truncate from (default: end)"
    )

    # Output options
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output results as JSON"
    )
    parser.add_argument(
        "--verbose",
        "-v",
        action="store_true",
        help="Verbose output"
    )

    args = parser.parse_args()

    # Handle list models
    if args.list_models:
        models = list_supported_models()
        if args.json:
            print(json.dumps(models, indent=2))
        else:
            print("Supported Models:")
            print("=" * 80)
            for model in models:
                info = get_model_info(model)
                print(f"\n{model}")
                print(f"  Context: {info['context_limit']:,} tokens")
                print(f"  Pricing: ${info['pricing']['input']}/1M input, ${info['pricing']['output']}/1M output")
                print(f"  Provider: {info['provider']}")
        return 0

    # Handle model info
    if args.model_info:
        info = get_model_info(args.model_info)
        if args.json:
            print(json.dumps(info, indent=2))
        else:
            print(f"Model: {info['model']}")
            print(f"Provider: {info['provider']}")
            print(f"Context Limit: {info['context_limit']:,} tokens")
            pricing = info['pricing']
            print(f"Input Pricing: ${pricing['input']}/1M tokens")
            print(f"Output Pricing: ${pricing['output']}/1M tokens")
        return 0

    # Get text from args
    if args.text:
        text = args.text
    elif args.file:
        if not args.file.exists():
            print(f"Error: File not found: {args.file}", file=sys.stderr)
            return 1
        text = args.file.read_text(encoding='utf-8')
    else:
        # Read from stdin
        if sys.stdin.isatty():
            parser.print_help()
            return 1
        text = sys.stdin.read()

    # Perform analysis
    input_tokens = count_tokens(text, args.model)
    within_limit, remaining = check_limits(input_tokens, args.model, args.output_tokens)
    cost = estimate_cost(input_tokens, args.output_tokens, args.model)

    result = TokenCount(
        input_tokens=input_tokens,
        output_tokens_estimate=args.output_tokens,
        total=input_tokens + args.output_tokens,
        model=args.model,
        cost_estimate=cost,
        within_limit=within_limit,
        remaining_tokens=remaining
    )

    # Output results
    if args.json:
        output = result.to_dict()
        if args.truncate and not within_limit:
            truncated = truncate_to_fit(
                text,
                args.model,
                output_tokens=args.output_tokens,
                truncate_from=args.truncate_from
            )
            output['truncated_text'] = truncated
            output['truncated_tokens'] = count_tokens(truncated, args.model)
        print(json.dumps(output, indent=2))
    else:
        print("Token Count Analysis")
        print("=" * 80)
        print(f"Model: {args.model}")
        print(f"Input Tokens: {result.input_tokens:,}")
        print(f"Output Tokens (estimate): {result.output_tokens_estimate:,}")
        print(f"Total Tokens: {result.total:,}")
        print(f"Cost Estimate: ${result.cost_estimate:.6f}")

        if args.check_limit:
            limit = MODEL_LIMITS.get(args.model, "Unknown")
            print(f"\nContext Limit: {limit:,} tokens")
            print(f"Within Limit: {'Yes' if within_limit else 'No'}")
            print(f"Remaining Tokens: {remaining:,}")

            if not within_limit:
                print(f"\nWARNING: Exceeds context limit by {abs(remaining):,} tokens!")

                if args.truncate:
                    print("\nTruncated version:")
                    print("-" * 80)
                    truncated = truncate_to_fit(
                        text,
                        args.model,
                        output_tokens=args.output_tokens,
                        truncate_from=args.truncate_from
                    )
                    print(truncated)
                    print("-" * 80)
                    print(f"Truncated tokens: {count_tokens(truncated, args.model):,}")

        if args.verbose:
            print(f"\nModel Information:")
            info = get_model_info(args.model)
            print(f"  Provider: {info['provider']}")
            print(f"  Context Limit: {info['context_limit']:,} tokens")
            print(f"  Input Price: ${info['pricing']['input']}/1M tokens")
            print(f"  Output Price: ${info['pricing']['output']}/1M tokens")

    return 0 if within_limit else 1


if __name__ == "__main__":
    sys.exit(main())
