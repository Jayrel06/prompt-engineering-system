#!/usr/bin/env python3
"""
Unified Prompt Improver - Single entry point for all prompt improvements

This script chains together all prompt improvement tools automatically:
1. Diagnoses issues with prompt_doctor
2. Routes to best framework with prompt_router
3. Loads relevant best practices
4. Generates optimized variations with prompt_optimizer
5. Returns comprehensive improvement results

Usage:
    python prompt_improver.py "your prompt here"
    python prompt_improver.py --file prompt.txt
    python prompt_improver.py "prompt" --json
    python prompt_improver.py "prompt" --verbose --num-variations 5
"""

import sys
import os
import json
import argparse
from pathlib import Path
from typing import List, Dict, Optional, Any
from dataclasses import dataclass, asdict, field
from datetime import datetime

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

# Import our tools
try:
    from prompt_doctor import PromptDoctor, DiagnosticResult
    HAS_DOCTOR = True
except ImportError as e:
    print(f"Warning: Could not import prompt_doctor: {e}", file=sys.stderr)
    HAS_DOCTOR = False

try:
    from prompt_router import route_prompt, RoutingResult
    HAS_ROUTER = True
except ImportError as e:
    print(f"Warning: Could not import prompt_router: {e}", file=sys.stderr)
    HAS_ROUTER = False

try:
    from prompt_optimizer import PromptOptimizer, OptimizationResult, OptimizationTechnique
    HAS_OPTIMIZER = True
except ImportError as e:
    print(f"Warning: Could not import prompt_optimizer: {e}", file=sys.stderr)
    HAS_OPTIMIZER = False


@dataclass
class ImprovementResult:
    """Complete result of prompt improvement process."""
    original: str
    improved: str
    diagnosis: Optional[Dict[str, Any]] = None
    framework_used: Optional[str] = None
    techniques_applied: List[str] = field(default_factory=list)
    improvement_score: float = 0.0
    explanation: str = ""
    all_variations: List[Dict[str, Any]] = field(default_factory=list)
    best_practices_applied: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        return {
            'original': self.original,
            'improved': self.improved,
            'diagnosis': self.diagnosis,
            'framework_used': self.framework_used,
            'techniques_applied': self.techniques_applied,
            'improvement_score': self.improvement_score,
            'explanation': self.explanation,
            'all_variations': self.all_variations,
            'best_practices_applied': self.best_practices_applied,
            'metadata': self.metadata,
            'timestamp': self.timestamp
        }

    def format_report(self) -> str:
        """Format as human-readable report."""
        lines = []
        lines.append("=" * 80)
        lines.append("PROMPT IMPROVEMENT REPORT")
        lines.append("=" * 80)
        lines.append("")

        # Original prompt
        lines.append("ORIGINAL PROMPT:")
        lines.append("-" * 80)
        lines.append(self.original)
        lines.append("")

        # Diagnosis
        if self.diagnosis:
            lines.append("DIAGNOSIS:")
            lines.append("-" * 80)
            lines.append(f"Quality Score: {self.diagnosis.get('quality_score', 0)}/100")
            lines.append(f"Health Status: {self.diagnosis.get('overall_health', 'UNKNOWN')}")

            issues = self.diagnosis.get('issues', [])
            if issues:
                lines.append(f"\nIssues Found: {len(issues)}")
                for issue in issues[:5]:  # Show first 5 issues
                    severity = issue.get('severity', 'UNKNOWN')
                    issue_type = issue.get('type', 'unknown')
                    description = issue.get('description', '')
                    lines.append(f"  [{severity}] {issue_type}: {description}")
            lines.append("")

        # Framework recommendation
        if self.framework_used:
            lines.append("RECOMMENDED FRAMEWORK:")
            lines.append("-" * 80)
            lines.append(f"{self.framework_used}")
            if self.techniques_applied:
                lines.append(f"Techniques: {', '.join(self.techniques_applied)}")
            lines.append("")

        # Best practices
        if self.best_practices_applied:
            lines.append("BEST PRACTICES APPLIED:")
            lines.append("-" * 80)
            for practice in self.best_practices_applied:
                lines.append(f"  - {practice}")
            lines.append("")

        # Improved prompt
        lines.append("IMPROVED PROMPT:")
        lines.append("-" * 80)
        lines.append(self.improved)
        lines.append("")

        # Improvement metrics
        lines.append("IMPROVEMENT METRICS:")
        lines.append("-" * 80)
        lines.append(f"Improvement Score: {self.improvement_score:.1f}%")
        lines.append("")

        # Explanation
        if self.explanation:
            lines.append("WHAT CHANGED AND WHY:")
            lines.append("-" * 80)
            lines.append(self.explanation)
            lines.append("")

        # All variations (if verbose)
        if self.all_variations and len(self.all_variations) > 1:
            lines.append(f"ALTERNATIVE VARIATIONS ({len(self.all_variations) - 1} more):")
            lines.append("-" * 80)
            for i, var in enumerate(self.all_variations[1:], 1):
                technique = var.get('technique_used', 'unknown')
                score = var.get('total_score', 0)
                lines.append(f"\n{i}. {technique} (Score: {score:.1f}/10)")
                content = var.get('content', '')
                lines.append(f"   {content[:150]}...")
            lines.append("")

        lines.append("=" * 80)
        return "\n".join(lines)


class PromptImprover:
    """Main class that orchestrates all prompt improvement tools."""

    def __init__(
        self,
        use_api: bool = True,
        provider: str = "anthropic",
        model: Optional[str] = None,
        api_key: Optional[str] = None,
        verbose: bool = False
    ):
        """
        Initialize the prompt improver.

        Args:
            use_api: Whether to use API-based optimization (requires API key)
            provider: API provider ("anthropic" or "openai")
            model: Model to use
            api_key: API key (uses env vars if not provided)
            verbose: Enable verbose output
        """
        self.use_api = use_api
        self.provider = provider
        self.model = model
        self.verbose = verbose

        # Load best practices
        self.best_practices = self._load_best_practices()

        # Initialize optimizer if API is available
        self.optimizer = None
        if use_api and HAS_OPTIMIZER:
            try:
                self.optimizer = PromptOptimizer(
                    provider=provider,
                    model=model,
                    api_key=api_key
                )
                if verbose:
                    print(f"Initialized optimizer with {provider}/{self.optimizer.model}")
            except Exception as e:
                print(f"Warning: Could not initialize optimizer: {e}", file=sys.stderr)
                print("Falling back to rule-based improvements", file=sys.stderr)
                self.use_api = False

    def _load_best_practices(self) -> Dict[str, List[str]]:
        """Load best practices from markdown file."""
        best_practices_path = Path(__file__).parent.parent / "context" / "technical" / "prompting-best-practices.md"

        practices = {
            'specificity': [
                "Be specific and direct",
                "Avoid vague verbs like 'handle', 'process', 'improve'",
                "Replace with action verbs: 'extract', 'generate', 'transform', 'validate'"
            ],
            'examples': [
                "Provide 2-4 concrete examples",
                "Show input/output pairs",
                "Demonstrate the desired pattern"
            ],
            'format': [
                "Specify output format explicitly",
                "Use structured templates",
                "Define exact structure (JSON, markdown, etc.)"
            ],
            'structure': [
                "Use clear delimiters (XML tags for Claude)",
                "Break complex tasks into steps",
                "Task first, context second"
            ],
            'constraints': [
                "Define boundaries and limits",
                "Specify what to avoid",
                "Set success criteria"
            ],
            'context': [
                "Provide relevant background",
                "Set role and expertise level",
                "Define audience and purpose"
            ]
        }

        # Try to load from file if it exists
        if best_practices_path.exists():
            try:
                content = best_practices_path.read_text(encoding='utf-8')
                # Extract key points from markdown
                if 'Be Specific' in content:
                    practices['loaded'] = True
            except Exception as e:
                if self.verbose:
                    print(f"Note: Using built-in best practices: {e}", file=sys.stderr)

        return practices

    def diagnose(self, prompt: str) -> Optional[DiagnosticResult]:
        """Run prompt diagnosis."""
        if not HAS_DOCTOR:
            return None

        try:
            doctor = PromptDoctor(verbose=self.verbose)
            result = doctor.diagnose_prompt(prompt)
            if self.verbose:
                print(f"Diagnosis complete: Quality={result.quality_score}/100, Health={result.overall_health}")
            return result
        except Exception as e:
            print(f"Warning: Diagnosis failed: {e}", file=sys.stderr)
            return None

    def route(self, prompt: str) -> Optional[RoutingResult]:
        """Route prompt to best framework."""
        if not HAS_ROUTER:
            return None

        try:
            result = route_prompt(prompt)
            if self.verbose:
                print(f"Routing complete: Framework={result.primary_framework}, Confidence={result.confidence:.0%}")
            return result
        except Exception as e:
            print(f"Warning: Routing failed: {e}", file=sys.stderr)
            return None

    def _apply_rule_based_improvements(
        self,
        prompt: str,
        diagnosis: Optional[DiagnosticResult] = None,
        routing: Optional[RoutingResult] = None
    ) -> ImprovementResult:
        """Apply rule-based improvements without API."""
        improved = prompt
        techniques = []
        best_practices_used = []

        # Apply fixes based on diagnosis
        if diagnosis:
            issues_by_type = {}
            for issue in diagnosis.issues:
                issue_type = issue.type.value
                if issue_type not in issues_by_type:
                    issues_by_type[issue_type] = []
                issues_by_type[issue_type].append(issue)

            # Fix missing format
            if 'missing_format' in issues_by_type:
                improved += "\n\nFormat: Please provide output in a clear, structured format."
                techniques.append("add_format_specification")
                best_practices_used.append("Specify output format explicitly")

            # Fix missing examples
            if 'missing_examples' in issues_by_type:
                improved += "\n\nExample:\n[Provide example input/output pairs here]"
                techniques.append("add_examples")
                best_practices_used.append("Include concrete examples")

            # Fix missing constraints
            if 'missing_constraints' in issues_by_type:
                improved += "\n\nConstraints:\n- [Define boundaries and requirements]"
                techniques.append("add_constraints")
                best_practices_used.append("Define clear constraints")

            # Fix vague instructions
            if 'vague_instruction' in issues_by_type:
                improved = "Task: " + improved
                best_practices_used.append("Lead with clear task statement")

        # Apply framework guidance
        if routing:
            framework_text = f"\n\n# Recommended Approach: {routing.primary_framework}\n"
            if routing.techniques:
                framework_text += f"Suggested techniques: {', '.join(routing.techniques)}\n"
            improved = framework_text + improved
            techniques.extend(routing.techniques)

        # Calculate improvement score
        baseline_score = diagnosis.quality_score if diagnosis else 50.0
        # Estimate improvement based on fixes applied
        improvement_score = min(100, baseline_score + len(techniques) * 10)
        improvement_percentage = ((improvement_score - baseline_score) / baseline_score * 100) if baseline_score > 0 else 0

        # Build explanation
        explanation_parts = [
            "Applied rule-based improvements:",
            f"- Fixed {len(techniques)} identified issues",
        ]
        if best_practices_used:
            explanation_parts.append(f"- Applied {len(best_practices_used)} best practices")
        if routing:
            explanation_parts.append(f"- Added framework guidance: {routing.primary_framework}")

        return ImprovementResult(
            original=prompt,
            improved=improved,
            diagnosis=diagnosis.to_dict() if diagnosis else None,
            framework_used=routing.primary_framework if routing else None,
            techniques_applied=techniques,
            improvement_score=improvement_percentage,
            explanation="\n".join(explanation_parts),
            best_practices_applied=best_practices_used,
            metadata={
                'mode': 'rule_based',
                'baseline_score': baseline_score,
                'final_score': improvement_score
            }
        )

    def improve_prompt(
        self,
        prompt: str,
        auto_fix: bool = True,
        num_variations: int = 3,
        verbose: bool = False
    ) -> ImprovementResult:
        """
        Main improvement function that chains all tools together.

        Args:
            prompt: Original prompt to improve
            auto_fix: Whether to automatically apply fixes
            num_variations: Number of variations to generate (if using API)
            verbose: Enable verbose output

        Returns:
            ImprovementResult with improved prompt and all metadata
        """
        if verbose:
            print("Starting prompt improvement workflow...")
            print(f"Mode: {'API-based' if self.use_api else 'Rule-based'}")

        # Step 1: Diagnose issues
        diagnosis = None
        if HAS_DOCTOR:
            if verbose:
                print("\n[1/4] Diagnosing issues...")
            diagnosis = self.diagnose(prompt)

        # Step 2: Route to framework
        routing = None
        if HAS_ROUTER:
            if verbose:
                print("\n[2/4] Identifying best framework...")
            routing = self.route(prompt)

        # Step 3: Load best practices
        if verbose:
            print("\n[3/4] Loading best practices...")
        # Best practices are already loaded in __init__

        # Step 4: Generate improvements
        if verbose:
            print("\n[4/4] Generating improvements...")

        # Use API-based optimization if available
        if self.use_api and self.optimizer and auto_fix:
            try:
                # Select techniques based on routing
                techniques = None
                if routing and routing.techniques:
                    # Map routing techniques to optimization techniques
                    technique_mapping = {
                        'zero-shot-cot': OptimizationTechnique.STEP_BY_STEP,
                        'example-driven': OptimizationTechnique.WITH_EXAMPLES,
                        'format-specification': OptimizationTechnique.STRUCTURED,
                        'requirements-first': OptimizationTechnique.MORE_SPECIFIC,
                    }
                    techniques = []
                    for tech in routing.techniques:
                        if tech in technique_mapping:
                            techniques.append(technique_mapping[tech])

                # Run optimization
                opt_result = self.optimizer.optimize(
                    base_prompt=prompt,
                    num_variations=num_variations,
                    techniques=techniques
                )

                # Extract best practices applied
                best_practices_used = []
                for var in opt_result.variations:
                    tech = var.technique_used
                    if 'specific' in tech:
                        best_practices_used.append("Increased specificity and detail")
                    elif 'example' in tech:
                        best_practices_used.append("Added concrete examples")
                    elif 'structured' in tech:
                        best_practices_used.append("Improved structure and organization")
                    elif 'constrained' in tech:
                        best_practices_used.append("Added clear constraints")

                # Build explanation
                explanation_parts = [
                    f"Generated {len(opt_result.variations)} optimized variations",
                    f"Winner technique: {opt_result.winner.technique_used}",
                    f"Quality score improved from {opt_result.metadata.get('baseline_score', 0):.1f} to {opt_result.winner.total_score():.1f}",
                ]
                if diagnosis:
                    explanation_parts.append(f"Addressed {len(diagnosis.issues)} identified issues")

                return ImprovementResult(
                    original=prompt,
                    improved=opt_result.winner.content,
                    diagnosis=diagnosis.to_dict() if diagnosis else None,
                    framework_used=routing.primary_framework if routing else None,
                    techniques_applied=[opt_result.winner.technique_used] + (routing.techniques if routing else []),
                    improvement_score=opt_result.improvement_percentage,
                    explanation="\n".join(explanation_parts),
                    all_variations=[
                        {
                            'content': v.content,
                            'technique_used': v.technique_used,
                            'total_score': v.total_score(),
                            'scores': asdict(v.scores)
                        }
                        for v in opt_result.variations
                    ],
                    best_practices_applied=list(set(best_practices_used)),
                    metadata={
                        'mode': 'api_based',
                        'provider': self.provider,
                        'model': self.optimizer.model,
                        'num_variations': len(opt_result.variations)
                    }
                )

            except Exception as e:
                print(f"Warning: API-based optimization failed: {e}", file=sys.stderr)
                print("Falling back to rule-based improvements", file=sys.stderr)
                # Fall through to rule-based

        # Fall back to rule-based improvements
        return self._apply_rule_based_improvements(prompt, diagnosis, routing)


def main():
    """CLI entry point."""
    # Configure stdout for UTF-8 on Windows
    if sys.platform == 'win32':
        import io
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
        sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

    parser = argparse.ArgumentParser(
        description="Unified Prompt Improver - One command to improve any prompt",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Improve a prompt directly
  python prompt_improver.py "Write a summary of this article"

  # Read from file
  python prompt_improver.py --file prompt.txt

  # JSON output for automation
  python prompt_improver.py "prompt" --json

  # Verbose mode with more variations
  python prompt_improver.py "prompt" --verbose --num-variations 5

  # Without API (rule-based only)
  python prompt_improver.py "prompt" --no-api

  # Save result to file
  python prompt_improver.py "prompt" --output improved.txt
        """
    )

    parser.add_argument(
        'prompt',
        nargs='?',
        help='Prompt to improve (or use --file)'
    )

    parser.add_argument(
        '--file',
        '-f',
        type=str,
        help='Read prompt from file'
    )

    parser.add_argument(
        '--no-api',
        action='store_true',
        help='Use rule-based improvements only (no API calls)'
    )

    parser.add_argument(
        '--no-fix',
        action='store_true',
        help='Disable automatic fixes (just diagnose and route)'
    )

    parser.add_argument(
        '--num-variations',
        '-n',
        type=int,
        default=3,
        help='Number of variations to generate (default: 3)'
    )

    parser.add_argument(
        '--provider',
        choices=['anthropic', 'openai'],
        default='anthropic',
        help='API provider (default: anthropic)'
    )

    parser.add_argument(
        '--model',
        type=str,
        help='Model to use (defaults based on provider)'
    )

    parser.add_argument(
        '--json',
        action='store_true',
        help='Output as JSON'
    )

    parser.add_argument(
        '--output',
        '-o',
        type=str,
        help='Write improved prompt to file'
    )

    parser.add_argument(
        '--verbose',
        '-v',
        action='store_true',
        help='Verbose output'
    )

    args = parser.parse_args()

    # Get prompt from args or file
    prompt = None
    if args.file:
        try:
            with open(args.file, 'r', encoding='utf-8') as f:
                prompt = f.read().strip()
        except FileNotFoundError:
            print(f"Error: File not found: {args.file}", file=sys.stderr)
            return 1
        except Exception as e:
            print(f"Error reading file: {e}", file=sys.stderr)
            return 1
    elif args.prompt:
        prompt = args.prompt
    else:
        parser.print_help()
        return 0

    if not prompt:
        print("Error: No prompt provided", file=sys.stderr)
        return 1

    # Initialize improver
    try:
        improver = PromptImprover(
            use_api=not args.no_api,
            provider=args.provider,
            model=args.model,
            verbose=args.verbose
        )
    except Exception as e:
        print(f"Error initializing improver: {e}", file=sys.stderr)
        if args.verbose:
            import traceback
            traceback.print_exc()
        return 1

    # Run improvement
    try:
        result = improver.improve_prompt(
            prompt=prompt,
            auto_fix=not args.no_fix,
            num_variations=args.num_variations,
            verbose=args.verbose
        )

        # Output results
        if args.json:
            print(json.dumps(result.to_dict(), indent=2, ensure_ascii=False))
        else:
            print(result.format_report())

        # Save to file if requested
        if args.output:
            try:
                with open(args.output, 'w', encoding='utf-8') as f:
                    f.write(result.improved)
                print(f"\nImproved prompt saved to: {args.output}")
            except Exception as e:
                print(f"Error writing output file: {e}", file=sys.stderr)
                return 1

        # Exit code based on improvement
        if result.improvement_score < 0:
            return 2  # Degradation
        elif result.improvement_score < 10:
            return 1  # Minimal improvement
        else:
            return 0  # Good improvement

    except KeyboardInterrupt:
        print("\n\nInterrupted by user", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"Error during improvement: {e}", file=sys.stderr)
        if args.verbose:
            import traceback
            traceback.print_exc()
        return 1


if __name__ == '__main__':
    sys.exit(main())
