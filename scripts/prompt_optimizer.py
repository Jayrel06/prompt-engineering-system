#!/usr/bin/env python3
"""
Prompt Optimizer

Automatically optimizes prompts by generating variations, testing them,
and tracking which techniques work best. Supports both automatic optimization
using LLMs and manual A/B testing workflows.

Features:
- Generate 3-5 prompt variations using different optimization techniques
- Evaluate variations against clarity, specificity, and output criteria
- Score and rank variations with detailed metrics
- Store winning prompts in JSON for future reference
- Support for Anthropic and OpenAI APIs
"""

import os
import json
import hashlib
import logging
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass, asdict, field
from collections import defaultdict
from enum import Enum

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

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class OptimizationTechnique(Enum):
    """Enumeration of prompt optimization techniques."""
    MORE_SPECIFIC = "more_specific"
    MORE_CONCISE = "more_concise"
    STRUCTURED = "structured"
    WITH_EXAMPLES = "with_examples"
    ROLE_BASED = "role_based"
    STEP_BY_STEP = "step_by_step"
    CONSTRAINED = "constrained"
    CONTEXT_RICH = "context_rich"


@dataclass
class EvaluationCriteria:
    """Criteria for evaluating prompt quality."""
    clarity: float = 0.0  # 0-10: How clear and unambiguous is the prompt?
    specificity: float = 0.0  # 0-10: How specific are the instructions?
    format_guidance: float = 0.0  # 0-10: Does it specify output format?
    examples_quality: float = 0.0  # 0-10: Quality of examples provided
    conciseness: float = 0.0  # 0-10: Is it concise while being complete?

    def overall_score(self) -> float:
        """Calculate weighted overall score."""
        weights = {
            'clarity': 0.25,
            'specificity': 0.25,
            'format_guidance': 0.20,
            'examples_quality': 0.15,
            'conciseness': 0.15
        }
        return (
            self.clarity * weights['clarity'] +
            self.specificity * weights['specificity'] +
            self.format_guidance * weights['format_guidance'] +
            self.examples_quality * weights['examples_quality'] +
            self.conciseness * weights['conciseness']
        )


@dataclass
class TestResult:
    """Result from testing a prompt variation."""
    test_input: str
    expected_output: Optional[str]
    actual_output: str
    success: bool
    execution_time: float
    error: Optional[str] = None


@dataclass
class PromptVariation:
    """A variation of a prompt with metadata."""
    id: str
    content: str
    technique_used: str
    scores: EvaluationCriteria
    test_results: List[TestResult] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def average_test_success_rate(self) -> float:
        """Calculate success rate across all tests."""
        if not self.test_results:
            return 0.0
        successes = sum(1 for t in self.test_results if t.success)
        return successes / len(self.test_results)

    def total_score(self) -> float:
        """Calculate total score including test results."""
        base_score = self.scores.overall_score()
        test_score = self.average_test_success_rate() * 10
        return (base_score * 0.6) + (test_score * 0.4)


@dataclass
class OptimizationResult:
    """Result of prompt optimization process."""
    original: str
    variations: List[PromptVariation]
    winner: PromptVariation
    improvement_percentage: float
    timestamp: str
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        return {
            'original': self.original,
            'variations': [
                {
                    'id': v.id,
                    'content': v.content,
                    'technique_used': v.technique_used,
                    'scores': asdict(v.scores),
                    'test_results': [asdict(t) for t in v.test_results],
                    'metadata': v.metadata,
                    'total_score': v.total_score()
                }
                for v in self.variations
            ],
            'winner': {
                'id': self.winner.id,
                'content': self.winner.content,
                'technique_used': self.winner.technique_used,
                'total_score': self.winner.total_score()
            },
            'improvement_percentage': self.improvement_percentage,
            'timestamp': self.timestamp,
            'metadata': self.metadata
        }


class PromptOptimizer:
    """Main class for optimizing prompts."""

    def __init__(
        self,
        provider: str = "anthropic",
        model: Optional[str] = None,
        api_key: Optional[str] = None,
        cache_dir: Optional[Path] = None,
        results_dir: Optional[Path] = None
    ):
        """
        Initialize the prompt optimizer.

        Args:
            provider: "anthropic" or "openai"
            model: Model to use (defaults based on provider)
            api_key: API key (uses env vars if not provided)
            cache_dir: Directory for caching API responses
            results_dir: Directory for storing optimization results
        """
        self.provider = provider.lower()
        self.model = model or self._default_model()

        # Setup API client
        if self.provider == "anthropic":
            if not HAS_ANTHROPIC:
                raise ImportError("anthropic package not installed. Run: pip install anthropic")
            self.client = anthropic.Anthropic(api_key=api_key)
        elif self.provider == "openai":
            if not HAS_OPENAI:
                raise ImportError("openai package not installed. Run: pip install openai")
            self.client = openai.OpenAI(api_key=api_key)
        else:
            raise ValueError(f"Unknown provider: {provider}")

        # Setup directories
        self.cache_dir = Path(cache_dir) if cache_dir else Path.home() / ".prompt_optimizer" / "cache"
        self.results_dir = Path(results_dir) if results_dir else Path.home() / ".prompt_optimizer" / "results"
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.results_dir.mkdir(parents=True, exist_ok=True)

        logger.info(f"Initialized PromptOptimizer with {provider}/{self.model}")

    def _default_model(self) -> str:
        """Get default model for provider."""
        defaults = {
            "anthropic": "claude-sonnet-4-20250514",
            "openai": "gpt-4"
        }
        return defaults.get(self.provider, "claude-sonnet-4-20250514")

    def _call_llm(
        self,
        prompt: str,
        system: str = "",
        temperature: float = 0.7,
        max_tokens: int = 2048
    ) -> str:
        """
        Call LLM API with error handling.

        Args:
            prompt: User prompt
            system: System prompt
            temperature: Sampling temperature
            max_tokens: Maximum tokens to generate

        Returns:
            Generated text response
        """
        try:
            if self.provider == "anthropic":
                response = self.client.messages.create(
                    model=self.model,
                    max_tokens=max_tokens,
                    temperature=temperature,
                    system=system if system else "You are a helpful AI assistant.",
                    messages=[{"role": "user", "content": prompt}]
                )
                return response.content[0].text

            elif self.provider == "openai":
                messages = []
                if system:
                    messages.append({"role": "system", "content": system})
                messages.append({"role": "user", "content": prompt})

                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=messages,
                    temperature=temperature,
                    max_tokens=max_tokens
                )
                return response.choices[0].message.content

        except Exception as e:
            logger.error(f"LLM API call failed: {e}")
            raise

    def generate_variations(
        self,
        base_prompt: str,
        num_variations: int = 5,
        techniques: Optional[List[OptimizationTechnique]] = None
    ) -> List[PromptVariation]:
        """
        Generate variations of a prompt using different techniques.

        Args:
            base_prompt: Original prompt to optimize
            num_variations: Number of variations to generate (3-5)
            techniques: Specific techniques to use (auto-selected if None)

        Returns:
            List of prompt variations
        """
        logger.info(f"Generating {num_variations} variations of prompt")

        # Select techniques if not provided
        if techniques is None:
            all_techniques = list(OptimizationTechnique)
            techniques = all_techniques[:min(num_variations, len(all_techniques))]
        else:
            techniques = techniques[:num_variations]

        variations = []

        for technique in techniques:
            try:
                logger.info(f"Applying technique: {technique.value}")
                variation_content = self._apply_technique(base_prompt, technique)

                # Generate unique ID
                variation_id = hashlib.md5(
                    (variation_content + technique.value).encode()
                ).hexdigest()[:12]

                variation = PromptVariation(
                    id=variation_id,
                    content=variation_content,
                    technique_used=technique.value,
                    scores=EvaluationCriteria(),
                    metadata={'generation_timestamp': datetime.now().isoformat()}
                )

                variations.append(variation)

            except Exception as e:
                logger.error(f"Failed to generate variation with {technique.value}: {e}")
                continue

        logger.info(f"Successfully generated {len(variations)} variations")
        return variations

    def _apply_technique(
        self,
        base_prompt: str,
        technique: OptimizationTechnique
    ) -> str:
        """
        Apply a specific optimization technique to a prompt.

        Args:
            base_prompt: Original prompt
            technique: Optimization technique to apply

        Returns:
            Optimized prompt variation
        """
        technique_prompts = {
            OptimizationTechnique.MORE_SPECIFIC: f"""
Take this prompt and make it MORE SPECIFIC by adding details, constraints, and requirements:

Original prompt:
{base_prompt}

Provide ONLY the improved prompt, no explanation:""",

            OptimizationTechnique.MORE_CONCISE: f"""
Take this prompt and make it MORE CONCISE while preserving all key information:

Original prompt:
{base_prompt}

Provide ONLY the improved prompt, no explanation:""",

            OptimizationTechnique.STRUCTURED: f"""
Take this prompt and RESTRUCTURE it with clear sections, numbered steps, or bullet points:

Original prompt:
{base_prompt}

Provide ONLY the improved prompt, no explanation:""",

            OptimizationTechnique.WITH_EXAMPLES: f"""
Take this prompt and add 1-2 CONCRETE EXAMPLES to clarify expectations:

Original prompt:
{base_prompt}

Provide ONLY the improved prompt with examples, no explanation:""",

            OptimizationTechnique.ROLE_BASED: f"""
Take this prompt and add a ROLE SPECIFICATION (e.g., "You are an expert X..."):

Original prompt:
{base_prompt}

Provide ONLY the improved prompt, no explanation:""",

            OptimizationTechnique.STEP_BY_STEP: f"""
Take this prompt and rewrite it to request STEP-BY-STEP reasoning:

Original prompt:
{base_prompt}

Provide ONLY the improved prompt, no explanation:""",

            OptimizationTechnique.CONSTRAINED: f"""
Take this prompt and add OUTPUT CONSTRAINTS (format, length, style, etc.):

Original prompt:
{base_prompt}

Provide ONLY the improved prompt, no explanation:""",

            OptimizationTechnique.CONTEXT_RICH: f"""
Take this prompt and add RELEVANT CONTEXT that would help generate better responses:

Original prompt:
{base_prompt}

Provide ONLY the improved prompt, no explanation:"""
        }

        optimization_prompt = technique_prompts[technique]

        system_prompt = """You are an expert prompt engineer. Your job is to optimize prompts
to be more effective. Focus on the specific technique requested. Return ONLY the optimized
prompt without any meta-commentary or explanation."""

        return self._call_llm(
            optimization_prompt,
            system=system_prompt,
            temperature=0.7
        ).strip()

    def evaluate_prompt(
        self,
        variation: PromptVariation,
        reference_prompt: Optional[str] = None
    ) -> EvaluationCriteria:
        """
        Evaluate a prompt variation against quality criteria.

        Args:
            variation: Prompt variation to evaluate
            reference_prompt: Optional reference prompt for comparison

        Returns:
            EvaluationCriteria with scores
        """
        logger.info(f"Evaluating prompt variation {variation.id}")

        evaluation_prompt = f"""
Evaluate this prompt on the following criteria. Rate each from 0-10:

1. CLARITY (0-10): How clear and unambiguous are the instructions?
2. SPECIFICITY (0-10): How specific and detailed are the requirements?
3. FORMAT_GUIDANCE (0-10): Does it clearly specify the desired output format?
4. EXAMPLES_QUALITY (0-10): Quality of examples provided (0 if none)
5. CONCISENESS (0-10): Is it concise while being complete?

Prompt to evaluate:
{variation.content}

Provide your evaluation in this EXACT format (just the numbers):
CLARITY: X
SPECIFICITY: X
FORMAT_GUIDANCE: X
EXAMPLES_QUALITY: X
CONCISENESS: X
"""

        system_prompt = """You are an expert prompt evaluator. Provide objective,
numerical ratings. Be strict but fair."""

        try:
            response = self._call_llm(
                evaluation_prompt,
                system=system_prompt,
                temperature=0.3
            )

            # Parse scores
            scores = {}
            for line in response.strip().split('\n'):
                if ':' in line:
                    key, value = line.split(':', 1)
                    key = key.strip().lower()
                    try:
                        score = float(value.strip())
                        scores[key] = max(0.0, min(10.0, score))
                    except ValueError:
                        logger.warning(f"Could not parse score for {key}: {value}")

            criteria = EvaluationCriteria(
                clarity=scores.get('clarity', 5.0),
                specificity=scores.get('specificity', 5.0),
                format_guidance=scores.get('format_guidance', 5.0),
                examples_quality=scores.get('examples_quality', 5.0),
                conciseness=scores.get('conciseness', 5.0)
            )

            variation.scores = criteria
            logger.info(f"Evaluation complete. Overall score: {criteria.overall_score():.2f}")

            return criteria

        except Exception as e:
            logger.error(f"Evaluation failed: {e}")
            # Return default middle scores on error
            return EvaluationCriteria(
                clarity=5.0,
                specificity=5.0,
                format_guidance=5.0,
                examples_quality=5.0,
                conciseness=5.0
            )

    def run_ab_test(
        self,
        variations: List[PromptVariation],
        test_inputs: List[str],
        expected_outputs: Optional[List[str]] = None,
        auto_evaluate: bool = True
    ) -> List[PromptVariation]:
        """
        Run A/B testing on prompt variations.

        Args:
            variations: List of prompt variations to test
            test_inputs: List of test inputs to try
            expected_outputs: Optional expected outputs for each test
            auto_evaluate: Whether to automatically evaluate success

        Returns:
            Variations with test results populated
        """
        logger.info(f"Running A/B test with {len(test_inputs)} test cases")

        if expected_outputs and len(expected_outputs) != len(test_inputs):
            raise ValueError("Number of expected outputs must match test inputs")

        for i, test_input in enumerate(test_inputs):
            expected = expected_outputs[i] if expected_outputs else None
            logger.info(f"Test case {i+1}/{len(test_inputs)}")

            for variation in variations:
                try:
                    # Construct full prompt
                    full_prompt = f"{variation.content}\n\nInput: {test_input}"

                    # Execute
                    import time
                    start_time = time.time()
                    actual_output = self._call_llm(full_prompt, temperature=0.5)
                    execution_time = time.time() - start_time

                    # Evaluate success
                    success = True
                    error = None

                    if auto_evaluate and expected:
                        success = self._evaluate_output_match(expected, actual_output)

                    result = TestResult(
                        test_input=test_input,
                        expected_output=expected,
                        actual_output=actual_output,
                        success=success,
                        execution_time=execution_time,
                        error=error
                    )

                    variation.test_results.append(result)

                except Exception as e:
                    logger.error(f"Test failed for variation {variation.id}: {e}")
                    result = TestResult(
                        test_input=test_input,
                        expected_output=expected,
                        actual_output="",
                        success=False,
                        execution_time=0.0,
                        error=str(e)
                    )
                    variation.test_results.append(result)

        logger.info("A/B testing complete")
        return variations

    def _evaluate_output_match(
        self,
        expected: str,
        actual: str
    ) -> bool:
        """
        Evaluate if actual output matches expected output.

        Uses LLM to do semantic comparison.
        """
        evaluation_prompt = f"""
Compare these two outputs and determine if they are semantically equivalent:

Expected output:
{expected}

Actual output:
{actual}

Answer with ONLY 'YES' or 'NO':"""

        try:
            response = self._call_llm(
                evaluation_prompt,
                temperature=0.1
            ).strip().upper()

            return 'YES' in response
        except Exception as e:
            logger.error(f"Output evaluation failed: {e}")
            return False

    def optimize(
        self,
        base_prompt: str,
        num_variations: int = 5,
        test_inputs: Optional[List[str]] = None,
        expected_outputs: Optional[List[str]] = None,
        techniques: Optional[List[OptimizationTechnique]] = None
    ) -> OptimizationResult:
        """
        Full optimization workflow: generate, evaluate, test, rank.

        Args:
            base_prompt: Original prompt to optimize
            num_variations: Number of variations to generate
            test_inputs: Optional test inputs for A/B testing
            expected_outputs: Optional expected outputs
            techniques: Specific techniques to use

        Returns:
            OptimizationResult with winner and all variations
        """
        logger.info("Starting optimization workflow")

        # Generate variations
        variations = self.generate_variations(
            base_prompt,
            num_variations=num_variations,
            techniques=techniques
        )

        if not variations:
            raise RuntimeError("Failed to generate any variations")

        # Evaluate each variation
        for variation in variations:
            self.evaluate_prompt(variation)

        # Run A/B tests if test inputs provided
        if test_inputs:
            variations = self.run_ab_test(
                variations,
                test_inputs,
                expected_outputs
            )

        # Rank variations
        variations.sort(key=lambda v: v.total_score(), reverse=True)
        winner = variations[0]

        # Calculate baseline score (estimate for original)
        baseline_variation = PromptVariation(
            id="baseline",
            content=base_prompt,
            technique_used="original",
            scores=EvaluationCriteria()
        )
        self.evaluate_prompt(baseline_variation)
        baseline_score = baseline_variation.total_score()

        # Calculate improvement
        improvement = ((winner.total_score() - baseline_score) / baseline_score * 100) \
            if baseline_score > 0 else 0.0

        result = OptimizationResult(
            original=base_prompt,
            variations=variations,
            winner=winner,
            improvement_percentage=improvement,
            timestamp=datetime.now().isoformat(),
            metadata={
                'num_variations': len(variations),
                'provider': self.provider,
                'model': self.model,
                'baseline_score': baseline_score
            }
        )

        logger.info(f"Optimization complete. Winner: {winner.technique_used} "
                   f"(score: {winner.total_score():.2f}, improvement: {improvement:.1f}%)")

        return result

    def save_results(
        self,
        result: OptimizationResult,
        filename: Optional[str] = None
    ) -> Path:
        """
        Save optimization results to JSON file.

        Args:
            result: OptimizationResult to save
            filename: Optional filename (auto-generated if not provided)

        Returns:
            Path to saved file
        """
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            technique = result.winner.technique_used
            filename = f"optimization_{technique}_{timestamp}.json"

        filepath = self.results_dir / filename

        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(result.to_dict(), f, indent=2, ensure_ascii=False)

        logger.info(f"Results saved to {filepath}")
        return filepath

    def load_results(self, filename: str) -> Dict[str, Any]:
        """
        Load optimization results from JSON file.

        Args:
            filename: Name of file to load

        Returns:
            Dictionary with optimization results
        """
        filepath = self.results_dir / filename

        if not filepath.exists():
            raise FileNotFoundError(f"Results file not found: {filepath}")

        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)

    def get_winning_prompts(
        self,
        technique: Optional[str] = None,
        min_score: float = 7.0,
        limit: int = 10
    ) -> List[Dict[str, Any]]:
        """
        Get top performing prompts from saved results.

        Args:
            technique: Filter by technique
            min_score: Minimum score threshold
            limit: Maximum number of results

        Returns:
            List of top performing prompts
        """
        results = []

        for filepath in self.results_dir.glob("optimization_*.json"):
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    winner = data['winner']

                    if technique and winner['technique_used'] != technique:
                        continue

                    if winner['total_score'] < min_score:
                        continue

                    results.append({
                        'prompt': winner['content'],
                        'technique': winner['technique_used'],
                        'score': winner['total_score'],
                        'timestamp': data['timestamp'],
                        'improvement': data['improvement_percentage']
                    })
            except Exception as e:
                logger.warning(f"Failed to load {filepath}: {e}")
                continue

        # Sort by score
        results.sort(key=lambda x: x['score'], reverse=True)

        return results[:limit]


def main():
    """CLI interface for prompt optimizer."""
    import argparse
    import sys

    parser = argparse.ArgumentParser(
        description="Optimize prompts using various techniques",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Optimize a prompt
  python prompt_optimizer.py --prompt "Summarize this text" --num-variations 5

  # With test cases
  python prompt_optimizer.py --prompt "Extract email" --test-input "Contact: john@example.com"

  # View winning prompts
  python prompt_optimizer.py --show-winners --technique more_specific

  # Interactive mode
  python prompt_optimizer.py --interactive
"""
    )

    parser.add_argument(
        "-p", "--prompt",
        help="Base prompt to optimize"
    )
    parser.add_argument(
        "-n", "--num-variations",
        type=int,
        default=5,
        help="Number of variations to generate (default: 5)"
    )
    parser.add_argument(
        "--provider",
        choices=["anthropic", "openai"],
        default="anthropic",
        help="LLM provider (default: anthropic)"
    )
    parser.add_argument(
        "--model",
        help="Model to use (defaults based on provider)"
    )
    parser.add_argument(
        "--test-input",
        action="append",
        help="Test input for A/B testing (can specify multiple)"
    )
    parser.add_argument(
        "--expected-output",
        action="append",
        help="Expected output for test (must match test-input count)"
    )
    parser.add_argument(
        "--techniques",
        nargs="+",
        choices=[t.value for t in OptimizationTechnique],
        help="Specific techniques to use"
    )
    parser.add_argument(
        "--show-winners",
        action="store_true",
        help="Show top performing prompts from history"
    )
    parser.add_argument(
        "--technique",
        choices=[t.value for t in OptimizationTechnique],
        help="Filter by technique (for --show-winners)"
    )
    parser.add_argument(
        "--min-score",
        type=float,
        default=7.0,
        help="Minimum score threshold (default: 7.0)"
    )
    parser.add_argument(
        "--interactive",
        action="store_true",
        help="Interactive mode"
    )
    parser.add_argument(
        "--output",
        help="Output filename for results"
    )
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Verbose output"
    )

    args = parser.parse_args()

    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    try:
        optimizer = PromptOptimizer(
            provider=args.provider,
            model=args.model
        )

        # Show winners mode
        if args.show_winners:
            winners = optimizer.get_winning_prompts(
                technique=args.technique,
                min_score=args.min_score,
                limit=10
            )

            print(f"\nTop {len(winners)} Winning Prompts:")
            print("=" * 80)

            for i, winner in enumerate(winners, 1):
                print(f"\n{i}. Technique: {winner['technique']} | Score: {winner['score']:.2f}")
                print(f"   Improvement: {winner['improvement']:.1f}%")
                print(f"   Timestamp: {winner['timestamp']}")
                print(f"\n   Prompt:\n   {winner['prompt'][:200]}...")
                print("-" * 80)

            return

        # Interactive mode
        if args.interactive:
            print("Prompt Optimizer - Interactive Mode")
            print(f"Provider: {args.provider} | Model: {optimizer.model}")
            print("=" * 80)

            while True:
                try:
                    print("\nEnter prompt to optimize (or 'quit' to exit):")
                    prompt = input("> ").strip()

                    if not prompt or prompt.lower() == 'quit':
                        break

                    print(f"\nGenerating {args.num_variations} variations...")

                    result = optimizer.optimize(
                        base_prompt=prompt,
                        num_variations=args.num_variations
                    )

                    print("\n" + "=" * 80)
                    print("OPTIMIZATION RESULTS")
                    print("=" * 80)
                    print(f"\nWinner: {result.winner.technique_used}")
                    print(f"Score: {result.winner.total_score():.2f}/10")
                    print(f"Improvement: {result.improvement_percentage:.1f}%")
                    print(f"\nOptimized Prompt:\n{result.winner.content}")

                    if args.verbose:
                        print("\n" + "-" * 80)
                        print("All Variations:")
                        for i, var in enumerate(result.variations, 1):
                            print(f"\n{i}. {var.technique_used} (Score: {var.total_score():.2f})")
                            print(f"   {var.content[:150]}...")

                    # Save results
                    filepath = optimizer.save_results(result)
                    print(f"\nResults saved to: {filepath}")

                except KeyboardInterrupt:
                    print("\n\nExiting...")
                    break
                except Exception as e:
                    print(f"\nError: {e}")
                    if args.verbose:
                        import traceback
                        traceback.print_exc()

            return

        # Standard mode - optimize a prompt
        if not args.prompt:
            parser.print_help()
            sys.exit(1)

        # Parse techniques
        techniques = None
        if args.techniques:
            techniques = [OptimizationTechnique(t) for t in args.techniques]

        print(f"\nOptimizing prompt with {args.num_variations} variations...")
        print(f"Provider: {args.provider} | Model: {optimizer.model}")

        result = optimizer.optimize(
            base_prompt=args.prompt,
            num_variations=args.num_variations,
            test_inputs=args.test_input,
            expected_outputs=args.expected_output,
            techniques=techniques
        )

        # Display results
        print("\n" + "=" * 80)
        print("OPTIMIZATION RESULTS")
        print("=" * 80)

        print(f"\nOriginal Prompt:\n{result.original}\n")

        print(f"Winner: {result.winner.technique_used}")
        print(f"Score: {result.winner.total_score():.2f}/10")
        print(f"Improvement: {result.improvement_percentage:.1f}%")

        print(f"\nOptimized Prompt:\n{result.winner.content}")

        # Show detailed scores
        scores = result.winner.scores
        print(f"\nDetailed Scores:")
        print(f"  Clarity: {scores.clarity:.1f}/10")
        print(f"  Specificity: {scores.specificity:.1f}/10")
        print(f"  Format Guidance: {scores.format_guidance:.1f}/10")
        print(f"  Examples Quality: {scores.examples_quality:.1f}/10")
        print(f"  Conciseness: {scores.conciseness:.1f}/10")

        if result.winner.test_results:
            success_rate = result.winner.average_test_success_rate()
            print(f"\nTest Results: {success_rate:.0%} success rate")

        # Show all variations if verbose
        if args.verbose:
            print("\n" + "-" * 80)
            print("All Variations (ranked):")
            for i, var in enumerate(result.variations, 1):
                print(f"\n{i}. {var.technique_used}")
                print(f"   Score: {var.total_score():.2f}/10")
                print(f"   Prompt: {var.content[:200]}...")

        # Save results
        filepath = optimizer.save_results(result, filename=args.output)
        print(f"\n{'=' * 80}")
        print(f"Results saved to: {filepath}")

    except KeyboardInterrupt:
        print("\n\nInterrupted by user")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Error: {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
