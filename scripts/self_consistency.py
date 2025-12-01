#!/usr/bin/env python3
"""
Self-Consistency Prompting

Runs a prompt multiple times and aggregates responses to improve reliability.
Based on research showing that sampling multiple reasoning paths and taking
the majority answer significantly improves accuracy on complex tasks.
"""

import os
import json
import hashlib
from collections import Counter
from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass
from pathlib import Path

try:
    import anthropic
    HAS_ANTHROPIC = True
except ImportError:
    HAS_ANTHROPIC = False

try:
    import openai
    HAS_OPENAI = True
except ImportError:
    HAS_OPENAI = False


@dataclass
class ConsistencyResult:
    """Result of self-consistency analysis."""
    final_answer: str
    confidence: float
    agreement_ratio: float
    num_samples: int
    all_responses: List[str]
    all_answers: List[str]
    reasoning: str


def extract_answer(response: str, answer_marker: str = "FINAL ANSWER:") -> str:
    """
    Extract the final answer from a response.

    Looks for a marker like "FINAL ANSWER:" or extracts the last line/paragraph.
    """
    response = response.strip()

    # Try to find explicit answer marker
    if answer_marker.lower() in response.lower():
        idx = response.lower().rfind(answer_marker.lower())
        answer = response[idx + len(answer_marker):].strip()
        # Get first line of the answer
        answer = answer.split('\n')[0].strip()
        return answer

    # Try common patterns
    patterns = [
        "the answer is",
        "therefore,",
        "in conclusion,",
        "my answer:",
        "result:",
    ]

    for pattern in patterns:
        if pattern in response.lower():
            idx = response.lower().rfind(pattern)
            answer = response[idx + len(pattern):].strip()
            answer = answer.split('\n')[0].strip()
            # Clean up punctuation
            answer = answer.rstrip('.')
            return answer

    # Fall back to last non-empty line
    lines = [l.strip() for l in response.split('\n') if l.strip()]
    if lines:
        return lines[-1]

    return response


def normalize_answer(answer: str) -> str:
    """Normalize an answer for comparison."""
    # Lowercase
    normalized = answer.lower().strip()

    # Remove common prefixes
    prefixes = ["the answer is", "answer:", "result:", "therefore", "so"]
    for prefix in prefixes:
        if normalized.startswith(prefix):
            normalized = normalized[len(prefix):].strip()

    # Remove punctuation
    normalized = normalized.rstrip('.,!?')

    # Normalize whitespace
    normalized = ' '.join(normalized.split())

    return normalized


def call_anthropic(
    prompt: str,
    system: str = "",
    model: str = "claude-sonnet-4-20250514",
    temperature: float = 0.7,
    max_tokens: int = 1024
) -> str:
    """Call Anthropic API."""
    if not HAS_ANTHROPIC:
        raise ImportError("anthropic package not installed. Run: pip install anthropic")

    client = anthropic.Anthropic()

    messages = [{"role": "user", "content": prompt}]

    response = client.messages.create(
        model=model,
        max_tokens=max_tokens,
        temperature=temperature,
        system=system if system else "You are a helpful assistant. Think through problems carefully.",
        messages=messages
    )

    return response.content[0].text


def call_openai(
    prompt: str,
    system: str = "",
    model: str = "gpt-4",
    temperature: float = 0.7,
    max_tokens: int = 1024
) -> str:
    """Call OpenAI API."""
    if not HAS_OPENAI:
        raise ImportError("openai package not installed. Run: pip install openai")

    client = openai.OpenAI()

    messages = []
    if system:
        messages.append({"role": "system", "content": system})
    messages.append({"role": "user", "content": prompt})

    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=temperature,
        max_tokens=max_tokens
    )

    return response.choices[0].message.content


def run_self_consistency(
    prompt: str,
    num_samples: int = 5,
    provider: str = "anthropic",
    model: Optional[str] = None,
    temperature: float = 0.7,
    system_prompt: str = "",
    answer_marker: str = "FINAL ANSWER:",
    cache_dir: Optional[Path] = None
) -> ConsistencyResult:
    """
    Run self-consistency prompting.

    Args:
        prompt: The prompt to run
        num_samples: Number of times to run the prompt (3-10 recommended)
        provider: "anthropic" or "openai"
        model: Model to use (defaults based on provider)
        temperature: Sampling temperature (0.7-1.0 recommended for diversity)
        system_prompt: System prompt to use
        answer_marker: Marker to look for in responses
        cache_dir: Optional directory to cache responses

    Returns:
        ConsistencyResult with aggregated answer and confidence
    """
    if model is None:
        model = "claude-sonnet-4-20250514" if provider == "anthropic" else "gpt-4"

    # Add instruction to mark final answer
    enhanced_prompt = f"""{prompt}

After your reasoning, clearly state your final answer on a new line starting with "{answer_marker}"
"""

    # Check cache
    cache_key = None
    if cache_dir:
        cache_dir = Path(cache_dir)
        cache_dir.mkdir(parents=True, exist_ok=True)
        prompt_hash = hashlib.md5(enhanced_prompt.encode()).hexdigest()[:12]
        cache_key = cache_dir / f"sc_{prompt_hash}_{num_samples}.json"

        if cache_key.exists():
            cached = json.loads(cache_key.read_text())
            return ConsistencyResult(**cached)

    # Collect responses
    responses = []
    call_fn = call_anthropic if provider == "anthropic" else call_openai

    for i in range(num_samples):
        try:
            response = call_fn(
                prompt=enhanced_prompt,
                system=system_prompt,
                model=model,
                temperature=temperature
            )
            responses.append(response)
        except Exception as e:
            print(f"Warning: Sample {i+1} failed: {e}")

    if not responses:
        raise RuntimeError("All API calls failed")

    # Extract and normalize answers
    answers = [extract_answer(r, answer_marker) for r in responses]
    normalized = [normalize_answer(a) for a in answers]

    # Count occurrences
    answer_counts = Counter(normalized)
    most_common = answer_counts.most_common(1)[0]
    winning_answer = most_common[0]
    winning_count = most_common[1]

    # Find the best original answer (not normalized)
    for ans, norm in zip(answers, normalized):
        if norm == winning_answer:
            final_answer = ans
            break
    else:
        final_answer = winning_answer

    # Calculate confidence
    agreement_ratio = winning_count / len(responses)

    # Confidence based on agreement and sample size
    if agreement_ratio >= 0.8:
        confidence = 0.95
    elif agreement_ratio >= 0.6:
        confidence = 0.8
    elif agreement_ratio >= 0.4:
        confidence = 0.6
    else:
        confidence = 0.4

    # Adjust for sample size
    if len(responses) < 3:
        confidence *= 0.8

    # Build reasoning
    reasoning_parts = [
        f"Ran {len(responses)} samples",
        f"Agreement: {winning_count}/{len(responses)} ({agreement_ratio:.0%})",
    ]

    if len(answer_counts) > 1:
        other_answers = [f"'{a}': {c}" for a, c in answer_counts.most_common()[1:3]]
        reasoning_parts.append(f"Other answers: {', '.join(other_answers)}")

    result = ConsistencyResult(
        final_answer=final_answer,
        confidence=confidence,
        agreement_ratio=agreement_ratio,
        num_samples=len(responses),
        all_responses=responses,
        all_answers=answers,
        reasoning=" | ".join(reasoning_parts)
    )

    # Cache result
    if cache_key:
        cache_data = {
            "final_answer": result.final_answer,
            "confidence": result.confidence,
            "agreement_ratio": result.agreement_ratio,
            "num_samples": result.num_samples,
            "all_responses": result.all_responses,
            "all_answers": result.all_answers,
            "reasoning": result.reasoning,
        }
        cache_key.write_text(json.dumps(cache_data, indent=2))

    return result


def main():
    """CLI interface for self-consistency prompting."""
    import sys
    import argparse

    parser = argparse.ArgumentParser(
        description="Run self-consistency prompting for improved accuracy"
    )
    parser.add_argument("prompt", nargs="?", help="The prompt to run")
    parser.add_argument("-n", "--samples", type=int, default=5, help="Number of samples (default: 5)")
    parser.add_argument("-p", "--provider", choices=["anthropic", "openai"], default="anthropic")
    parser.add_argument("-m", "--model", help="Model to use")
    parser.add_argument("-t", "--temperature", type=float, default=0.7)
    parser.add_argument("--system", default="", help="System prompt")
    parser.add_argument("--interactive", action="store_true", help="Interactive mode")
    parser.add_argument("--verbose", action="store_true", help="Show all responses")

    args = parser.parse_args()

    if args.interactive:
        print("Self-Consistency Prompting - Interactive Mode")
        print(f"Provider: {args.provider} | Samples: {args.samples}")
        print("-" * 40)

        while True:
            try:
                prompt = input("\nPrompt: ").strip()
                if not prompt:
                    continue

                print(f"\nRunning {args.samples} samples...")
                result = run_self_consistency(
                    prompt=prompt,
                    num_samples=args.samples,
                    provider=args.provider,
                    model=args.model,
                    temperature=args.temperature,
                    system_prompt=args.system
                )

                print(f"\n{'='*40}")
                print(f"FINAL ANSWER: {result.final_answer}")
                print(f"Confidence: {result.confidence:.0%}")
                print(f"Agreement: {result.agreement_ratio:.0%} ({result.num_samples} samples)")
                print(f"Reasoning: {result.reasoning}")

                if args.verbose:
                    print(f"\nAll answers: {result.all_answers}")

            except KeyboardInterrupt:
                print("\nExiting.")
                break

    elif args.prompt:
        result = run_self_consistency(
            prompt=args.prompt,
            num_samples=args.samples,
            provider=args.provider,
            model=args.model,
            temperature=args.temperature,
            system_prompt=args.system
        )

        output = {
            "final_answer": result.final_answer,
            "confidence": result.confidence,
            "agreement_ratio": result.agreement_ratio,
            "num_samples": result.num_samples,
            "reasoning": result.reasoning,
        }

        if args.verbose:
            output["all_answers"] = result.all_answers
            output["all_responses"] = result.all_responses

        print(json.dumps(output, indent=2))

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
