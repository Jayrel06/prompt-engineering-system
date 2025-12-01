#!/usr/bin/env python3
"""
Prompt Doctor - Diagnostic Tool for Prompt Engineering

Analyzes prompts to detect issues and suggest improvements across multiple dimensions:
- Clarity and specificity
- Context completeness
- Complexity and structure
- Format specifications
- Example inclusion
- Constraint definition
"""

import re
import argparse
import sys
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Tuple
from enum import Enum
import json


class Severity(Enum):
    """Issue severity levels"""
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"


class IssueType(Enum):
    """Types of prompt issues"""
    VAGUE_INSTRUCTION = "vague_instruction"
    MISSING_CONTEXT = "missing_context"
    MISSING_FORMAT = "missing_format"
    MISSING_EXAMPLES = "missing_examples"
    OVERLY_COMPLEX = "overly_complex"
    AMBIGUOUS_LANGUAGE = "ambiguous_language"
    MISSING_CONSTRAINTS = "missing_constraints"
    UNCLEAR_GOAL = "unclear_goal"
    INCONSISTENT_TONE = "inconsistent_tone"
    MISSING_EDGE_CASES = "missing_edge_cases"


@dataclass
class Issue:
    """Represents a single diagnostic issue"""
    type: IssueType
    severity: Severity
    description: str
    suggestion: str
    location: Optional[str] = None

    def __str__(self) -> str:
        loc = f" [{self.location}]" if self.location else ""
        return f"[{self.severity.value}] {self.type.value}{loc}: {self.description}\n  -> {self.suggestion}"


@dataclass
class DiagnosticResult:
    """Complete diagnostic results for a prompt"""
    issues: List[Issue] = field(default_factory=list)
    suggestions: List[str] = field(default_factory=list)
    quality_score: float = 0.0  # 0-100
    complexity_score: float = 0.0  # 0-100
    clarity_score: float = 0.0  # 0-100
    specificity_score: float = 0.0  # 0-100
    completeness_score: float = 0.0  # 0-100

    @property
    def overall_health(self) -> str:
        """Overall prompt health assessment"""
        if self.quality_score >= 80:
            return "EXCELLENT"
        elif self.quality_score >= 60:
            return "GOOD"
        elif self.quality_score >= 40:
            return "FAIR"
        elif self.quality_score >= 20:
            return "POOR"
        else:
            return "CRITICAL"

    def to_dict(self) -> Dict:
        """Convert to dictionary for JSON serialization"""
        return {
            "quality_score": self.quality_score,
            "complexity_score": self.complexity_score,
            "clarity_score": self.clarity_score,
            "specificity_score": self.specificity_score,
            "completeness_score": self.completeness_score,
            "overall_health": self.overall_health,
            "issues": [
                {
                    "type": issue.type.value,
                    "severity": issue.severity.value,
                    "description": issue.description,
                    "suggestion": issue.suggestion,
                    "location": issue.location
                }
                for issue in self.issues
            ],
            "suggestions": self.suggestions
        }


class PromptDoctor:
    """Main diagnostic engine for prompt analysis"""

    # Anti-patterns and detection rules
    VAGUE_VERBS = [
        "handle", "deal with", "manage", "process", "work with",
        "fix", "improve", "enhance", "optimize", "better",
        "nice", "good", "some", "stuff", "things"
    ]

    AMBIGUOUS_WORDS = [
        "maybe", "perhaps", "possibly", "might", "could",
        "somewhat", "fairly", "relatively", "kind of", "sort of"
    ]

    FORMAT_KEYWORDS = [
        "format", "structure", "template", "schema", "json", "xml",
        "csv", "table", "list", "bullet", "numbered", "markdown"
    ]

    EXAMPLE_KEYWORDS = [
        "example", "instance", "sample", "demonstration", "illustration",
        "such as", "like", "e.g.", "for example"
    ]

    CONSTRAINT_KEYWORDS = [
        "must", "should", "required", "mandatory", "always", "never",
        "limit", "maximum", "minimum", "constraint", "rule", "requirement"
    ]

    CONTEXT_INDICATORS = [
        "context", "background", "assume", "given", "situation",
        "scenario", "use case", "audience", "purpose", "goal"
    ]

    def __init__(self, verbose: bool = False):
        self.verbose = verbose

    def diagnose_prompt(self, prompt: str) -> DiagnosticResult:
        """
        Main diagnostic function - analyzes prompt across all dimensions

        Args:
            prompt: The prompt text to analyze

        Returns:
            DiagnosticResult with all findings and scores
        """
        result = DiagnosticResult()

        if not prompt or not prompt.strip():
            result.issues.append(Issue(
                type=IssueType.UNCLEAR_GOAL,
                severity=Severity.HIGH,
                description="Empty prompt provided",
                suggestion="Provide a prompt to analyze"
            ))
            return result

        # Run all diagnostic checks
        result.issues.extend(self.check_clarity(prompt))
        result.issues.extend(self.check_specificity(prompt))
        result.issues.extend(self.check_format(prompt))
        result.issues.extend(self.check_examples(prompt))
        result.issues.extend(self.check_context(prompt))
        result.issues.extend(self.check_constraints(prompt))
        result.issues.extend(self.check_complexity(prompt))
        result.issues.extend(self.check_goal_clarity(prompt))

        # Calculate dimension scores
        result.clarity_score = self._calculate_clarity_score(prompt, result.issues)
        result.specificity_score = self._calculate_specificity_score(prompt, result.issues)
        result.complexity_score = self._calculate_complexity_score(prompt, result.issues)
        result.completeness_score = self._calculate_completeness_score(prompt, result.issues)

        # Calculate overall quality score
        result.quality_score = self._calculate_quality_score(result)

        # Generate high-level suggestions
        result.suggestions = self.suggest_improvements(prompt, result)

        return result

    def check_clarity(self, prompt: str) -> List[Issue]:
        """Check for clarity issues"""
        issues = []

        # Check for vague verbs
        found_vague = []
        for verb in self.VAGUE_VERBS:
            pattern = r'\b' + re.escape(verb) + r'\b'
            if re.search(pattern, prompt, re.IGNORECASE):
                found_vague.append(verb)

        if found_vague:
            issues.append(Issue(
                type=IssueType.VAGUE_INSTRUCTION,
                severity=Severity.MEDIUM,
                description=f"Vague verbs detected: {', '.join(found_vague[:3])}",
                suggestion="Replace with specific action verbs (e.g., 'extract', 'generate', 'transform', 'validate')",
                location="throughout"
            ))

        # Check for ambiguous language
        found_ambiguous = []
        for word in self.AMBIGUOUS_WORDS:
            pattern = r'\b' + re.escape(word) + r'\b'
            if re.search(pattern, prompt, re.IGNORECASE):
                found_ambiguous.append(word)

        if found_ambiguous:
            issues.append(Issue(
                type=IssueType.AMBIGUOUS_LANGUAGE,
                severity=Severity.MEDIUM,
                description=f"Ambiguous language detected: {', '.join(found_ambiguous[:3])}",
                suggestion="Use definitive language and clear instructions",
                location="throughout"
            ))

        # Check for questions without clear instructions
        questions = re.findall(r'[^.!?]*\?', prompt)
        statements = re.findall(r'[^.!?]*[.!]', prompt)

        if questions and len(questions) > len(statements):
            issues.append(Issue(
                type=IssueType.UNCLEAR_GOAL,
                severity=Severity.HIGH,
                description="Prompt consists mostly of questions without clear instructions",
                suggestion="Convert questions into clear imperative statements about what you want the AI to do",
                location="structure"
            ))

        return issues

    def check_specificity(self, prompt: str) -> List[Issue]:
        """Check for specificity and detail"""
        issues = []

        # Check prompt length
        word_count = len(prompt.split())

        if word_count < 10:
            issues.append(Issue(
                type=IssueType.VAGUE_INSTRUCTION,
                severity=Severity.HIGH,
                description=f"Very short prompt ({word_count} words)",
                suggestion="Add more specific details about what you want, how you want it, and why",
                location="overall"
            ))
        elif word_count < 20:
            issues.append(Issue(
                type=IssueType.VAGUE_INSTRUCTION,
                severity=Severity.MEDIUM,
                description=f"Short prompt ({word_count} words) may lack detail",
                suggestion="Consider adding context, constraints, and expected output details",
                location="overall"
            ))

        # Check for pronouns without clear antecedents
        pronouns = re.findall(r'\b(it|this|that|these|those|them|they)\b', prompt, re.IGNORECASE)
        if len(pronouns) > 3 and word_count < 50:
            issues.append(Issue(
                type=IssueType.AMBIGUOUS_LANGUAGE,
                severity=Severity.LOW,
                description="Multiple pronouns may create ambiguity",
                suggestion="Use specific nouns instead of pronouns to improve clarity",
                location="throughout"
            ))

        return issues

    def check_format(self, prompt: str) -> List[Issue]:
        """Check for output format specifications"""
        issues = []

        has_format_keywords = any(
            re.search(r'\b' + re.escape(kw) + r'\b', prompt, re.IGNORECASE)
            for kw in self.FORMAT_KEYWORDS
        )

        if not has_format_keywords:
            issues.append(Issue(
                type=IssueType.MISSING_FORMAT,
                severity=Severity.MEDIUM,
                description="No output format specification detected",
                suggestion="Specify the desired output format (e.g., JSON, markdown, bullet points, paragraph)",
                location="missing"
            ))
        else:
            # Check if format is actually defined or just mentioned
            format_mentions = sum(1 for kw in self.FORMAT_KEYWORDS
                                 if re.search(r'\b' + re.escape(kw) + r'\b', prompt, re.IGNORECASE))

            if format_mentions == 1:
                issues.append(Issue(
                    type=IssueType.MISSING_FORMAT,
                    severity=Severity.LOW,
                    description="Format mentioned but may need more detail",
                    suggestion="Provide a template or detailed structure specification",
                    location="format section"
                ))

        return issues

    def check_examples(self, prompt: str) -> List[Issue]:
        """Check for examples and demonstrations"""
        issues = []

        has_examples = any(
            re.search(r'\b' + re.escape(kw) + r'\b', prompt, re.IGNORECASE)
            for kw in self.EXAMPLE_KEYWORDS
        )

        word_count = len(prompt.split())

        # For complex prompts, examples are more important
        if word_count > 30 and not has_examples:
            issues.append(Issue(
                type=IssueType.MISSING_EXAMPLES,
                severity=Severity.MEDIUM,
                description="No examples provided for complex prompt",
                suggestion="Add 1-2 examples showing input/output pairs to clarify expectations",
                location="missing"
            ))
        elif word_count > 50 and not has_examples:
            issues.append(Issue(
                type=IssueType.MISSING_EXAMPLES,
                severity=Severity.HIGH,
                description="No examples provided for very complex prompt",
                suggestion="Add multiple examples demonstrating edge cases and expected behavior",
                location="missing"
            ))

        return issues

    def check_context(self, prompt: str) -> List[Issue]:
        """Check for context and background information"""
        issues = []

        has_context = any(
            re.search(r'\b' + re.escape(kw) + r'\b', prompt, re.IGNORECASE)
            for kw in self.CONTEXT_INDICATORS
        )

        word_count = len(prompt.split())

        # Check for imperative-only prompts
        if not has_context and word_count > 15:
            # Check if it's all instructions with no background
            sentences = re.split(r'[.!?]+', prompt)
            instruction_verbs = sum(1 for s in sentences
                                   if s.strip() and s.strip().split()[0].lower() in
                                   ['create', 'generate', 'write', 'make', 'build', 'analyze', 'extract'])

            if instruction_verbs >= len(sentences) * 0.7:
                issues.append(Issue(
                    type=IssueType.MISSING_CONTEXT,
                    severity=Severity.MEDIUM,
                    description="Prompt lacks context or background information",
                    suggestion="Add context about the use case, audience, or purpose to improve results",
                    location="missing"
                ))

        return issues

    def check_constraints(self, prompt: str) -> List[Issue]:
        """Check for constraints and requirements"""
        issues = []

        has_constraints = any(
            re.search(r'\b' + re.escape(kw) + r'\b', prompt, re.IGNORECASE)
            for kw in self.CONSTRAINT_KEYWORDS
        )

        word_count = len(prompt.split())

        if not has_constraints and word_count > 20:
            issues.append(Issue(
                type=IssueType.MISSING_CONSTRAINTS,
                severity=Severity.LOW,
                description="No explicit constraints or requirements specified",
                suggestion="Add constraints (length limits, style requirements, what to avoid, etc.)",
                location="missing"
            ))

        return issues

    def check_complexity(self, prompt: str) -> List[Issue]:
        """Check if prompt is overly complex"""
        issues = []

        word_count = len(prompt.split())
        sentences = re.split(r'[.!?]+', prompt)
        sentence_count = len([s for s in sentences if s.strip()])

        # Check for very long single sentence
        if sentence_count > 0:
            avg_sentence_length = word_count / sentence_count

            if avg_sentence_length > 40:
                issues.append(Issue(
                    type=IssueType.OVERLY_COMPLEX,
                    severity=Severity.MEDIUM,
                    description=f"Very long sentences (avg {avg_sentence_length:.1f} words)",
                    suggestion="Break down into shorter, clearer sentences",
                    location="structure"
                ))

        # Check for multiple distinct tasks
        task_indicators = ['also', 'and then', 'additionally', 'furthermore', 'moreover', 'next']
        task_count = sum(1 for indicator in task_indicators
                        if re.search(r'\b' + re.escape(indicator) + r'\b', prompt, re.IGNORECASE))

        if task_count >= 3:
            issues.append(Issue(
                type=IssueType.OVERLY_COMPLEX,
                severity=Severity.HIGH,
                description=f"Multiple distinct tasks detected ({task_count + 1})",
                suggestion="Split into separate prompts, one per task, for better results",
                location="structure"
            ))

        # Check for nested conditions
        if_count = len(re.findall(r'\bif\b', prompt, re.IGNORECASE))
        when_count = len(re.findall(r'\bwhen\b', prompt, re.IGNORECASE))

        if if_count + when_count >= 3:
            issues.append(Issue(
                type=IssueType.OVERLY_COMPLEX,
                severity=Severity.MEDIUM,
                description=f"Multiple conditional branches ({if_count + when_count})",
                suggestion="Simplify logic or use a decision tree/flowchart format",
                location="logic"
            ))

        return issues

    def check_goal_clarity(self, prompt: str) -> List[Issue]:
        """Check if the goal/desired outcome is clear"""
        issues = []

        # Check for clear outcome indicators
        outcome_verbs = [
            'output', 'result', 'produce', 'generate', 'create',
            'return', 'provide', 'give', 'show', 'display'
        ]

        has_outcome = any(
            re.search(r'\b' + re.escape(verb) + r'\b', prompt, re.IGNORECASE)
            for verb in outcome_verbs
        )

        word_count = len(prompt.split())

        if not has_outcome and word_count > 10:
            issues.append(Issue(
                type=IssueType.UNCLEAR_GOAL,
                severity=Severity.HIGH,
                description="Goal or desired outcome not clearly stated",
                suggestion="Start with or include a clear statement of what you want as output",
                location="overall"
            ))

        return issues

    def _calculate_clarity_score(self, prompt: str, issues: List[Issue]) -> float:
        """Calculate clarity score (0-100)"""
        score = 100.0

        # Deduct points for clarity issues
        for issue in issues:
            if issue.type in [IssueType.VAGUE_INSTRUCTION, IssueType.AMBIGUOUS_LANGUAGE, IssueType.UNCLEAR_GOAL]:
                if issue.severity == Severity.HIGH:
                    score -= 20
                elif issue.severity == Severity.MEDIUM:
                    score -= 10
                else:
                    score -= 5

        return max(0.0, score)

    def _calculate_specificity_score(self, prompt: str, issues: List[Issue]) -> float:
        """Calculate specificity score (0-100)"""
        score = 100.0

        # Deduct for vagueness
        for issue in issues:
            if issue.type in [IssueType.VAGUE_INSTRUCTION, IssueType.MISSING_CONTEXT]:
                if issue.severity == Severity.HIGH:
                    score -= 25
                elif issue.severity == Severity.MEDIUM:
                    score -= 12
                else:
                    score -= 6

        # Bonus for length and detail
        word_count = len(prompt.split())
        if word_count > 50:
            score += 10
        elif word_count > 30:
            score += 5

        return max(0.0, min(100.0, score))

    def _calculate_complexity_score(self, prompt: str, issues: List[Issue]) -> float:
        """Calculate complexity score (0-100, lower is simpler)"""
        score = 0.0

        word_count = len(prompt.split())
        sentences = re.split(r'[.!?]+', prompt)
        sentence_count = len([s for s in sentences if s.strip()])

        # Base complexity on length
        score += min(30, word_count / 3)

        # Add complexity for structure
        if sentence_count > 0:
            avg_sentence_length = word_count / sentence_count
            score += min(30, avg_sentence_length * 0.5)

        # Add complexity for issues
        for issue in issues:
            if issue.type == IssueType.OVERLY_COMPLEX:
                if issue.severity == Severity.HIGH:
                    score += 20
                elif issue.severity == Severity.MEDIUM:
                    score += 10

        return min(100.0, score)

    def _calculate_completeness_score(self, prompt: str, issues: List[Issue]) -> float:
        """Calculate completeness score (0-100)"""
        score = 100.0

        # Deduct for missing elements
        for issue in issues:
            if issue.type in [IssueType.MISSING_FORMAT, IssueType.MISSING_EXAMPLES,
                            IssueType.MISSING_CONTEXT, IssueType.MISSING_CONSTRAINTS]:
                if issue.severity == Severity.HIGH:
                    score -= 20
                elif issue.severity == Severity.MEDIUM:
                    score -= 10
                else:
                    score -= 5

        return max(0.0, score)

    def _calculate_quality_score(self, result: DiagnosticResult) -> float:
        """Calculate overall quality score"""
        # Weighted average of dimension scores
        weights = {
            'clarity': 0.3,
            'specificity': 0.25,
            'completeness': 0.25,
            'complexity': 0.2  # Inverse - lower complexity is better
        }

        # Invert complexity score (high complexity = bad)
        complexity_inverted = 100 - result.complexity_score

        quality = (
            result.clarity_score * weights['clarity'] +
            result.specificity_score * weights['specificity'] +
            result.completeness_score * weights['completeness'] +
            complexity_inverted * weights['complexity']
        )

        return round(quality, 1)

    def suggest_improvements(self, prompt: str, result: DiagnosticResult) -> List[str]:
        """Generate high-level improvement suggestions"""
        suggestions = []

        # Prioritize by severity and type
        high_severity = [i for i in result.issues if i.severity == Severity.HIGH]

        if high_severity:
            suggestions.append(f"PRIORITY: Address {len(high_severity)} high-severity issues first")

        # Specific suggestions based on patterns
        issue_types = {issue.type for issue in result.issues}

        if IssueType.UNCLEAR_GOAL in issue_types:
            suggestions.append("Start your prompt with a clear statement: 'Create/Generate/Analyze...'")

        if IssueType.MISSING_FORMAT in issue_types:
            suggestions.append("Add a 'Format:' section specifying output structure")

        if IssueType.MISSING_EXAMPLES in issue_types:
            suggestions.append("Include at least one example of desired input/output")

        if IssueType.OVERLY_COMPLEX in issue_types:
            suggestions.append("Consider using a template structure: Goal → Context → Format → Constraints → Examples")

        if result.quality_score < 50:
            suggestions.append("Consider using a prompt template or framework (e.g., CRISPE, RTF)")

        if result.completeness_score < 60:
            suggestions.append("Review the 5 W's: What, Why, Who, When, Where")

        return suggestions

    def auto_fix(self, prompt: str, result: DiagnosticResult) -> str:
        """
        Attempt to automatically fix some issues
        Note: This is basic - for complex fixes, use LLM-powered mode
        """
        fixed = prompt

        # Add format suggestion if missing
        if any(i.type == IssueType.MISSING_FORMAT for i in result.issues):
            if not fixed.endswith('\n'):
                fixed += '\n'
            fixed += "\nFormat: [Please specify: JSON, markdown, plain text, etc.]\n"

        # Add example placeholder if missing
        if any(i.type == IssueType.MISSING_EXAMPLES for i in result.issues):
            if not fixed.endswith('\n'):
                fixed += '\n'
            fixed += "\nExample:\n[Add example here]\n"

        # Add constraint section if missing
        if any(i.type == IssueType.MISSING_CONSTRAINTS for i in result.issues):
            if not fixed.endswith('\n'):
                fixed += '\n'
            fixed += "\nConstraints:\n- [Add requirements here]\n"

        return fixed


def format_report(result: DiagnosticResult, verbose: bool = False) -> str:
    """Format diagnostic result as readable report"""
    lines = []

    lines.append("=" * 70)
    lines.append("PROMPT DOCTOR DIAGNOSTIC REPORT")
    lines.append("=" * 70)
    lines.append("")

    # Overall scores
    lines.append(f"Overall Health: {result.overall_health} ({result.quality_score}/100)")
    lines.append("")
    lines.append("Dimension Scores:")
    lines.append(f"  Clarity:       {result.clarity_score:>5.1f}/100")
    lines.append(f"  Specificity:   {result.specificity_score:>5.1f}/100")
    lines.append(f"  Completeness:  {result.completeness_score:>5.1f}/100")
    lines.append(f"  Complexity:    {result.complexity_score:>5.1f}/100 (lower is better)")
    lines.append("")

    # Issues by severity
    if result.issues:
        high = [i for i in result.issues if i.severity == Severity.HIGH]
        medium = [i for i in result.issues if i.severity == Severity.MEDIUM]
        low = [i for i in result.issues if i.severity == Severity.LOW]

        lines.append(f"Issues Found: {len(result.issues)} total "
                    f"({len(high)} high, {len(medium)} medium, {len(low)} low)")
        lines.append("-" * 70)

        for issue in high + medium + low:
            lines.append("")
            lines.append(str(issue))
    else:
        lines.append("No issues found! This is a well-structured prompt.")

    # Suggestions
    if result.suggestions:
        lines.append("")
        lines.append("-" * 70)
        lines.append("IMPROVEMENT SUGGESTIONS:")
        lines.append("")
        for i, suggestion in enumerate(result.suggestions, 1):
            lines.append(f"{i}. {suggestion}")

    lines.append("")
    lines.append("=" * 70)

    return "\n".join(lines)


def main():
    """CLI entry point"""
    # Configure stdout for UTF-8 on Windows
    if sys.platform == 'win32':
        import io
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
        sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

    parser = argparse.ArgumentParser(
        description="Prompt Doctor - Diagnose and improve your prompts",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Diagnose a prompt from file
  python prompt_doctor.py --diagnose prompt.txt

  # Diagnose prompt from stdin
  echo "Write a story" | python prompt_doctor.py --diagnose -

  # Auto-fix issues
  python prompt_doctor.py --diagnose prompt.txt --fix

  # JSON output for automation
  python prompt_doctor.py --diagnose prompt.txt --json

  # Verbose output
  python prompt_doctor.py --diagnose prompt.txt --verbose
        """
    )

    parser.add_argument(
        '--diagnose',
        type=str,
        metavar='FILE',
        help='Diagnose prompt from file (use "-" for stdin)'
    )

    parser.add_argument(
        '--fix',
        action='store_true',
        help='Auto-apply basic fixes to the prompt'
    )

    parser.add_argument(
        '--verbose',
        '-v',
        action='store_true',
        help='Show detailed analysis'
    )

    parser.add_argument(
        '--json',
        action='store_true',
        help='Output results as JSON'
    )

    parser.add_argument(
        '--output',
        '-o',
        type=str,
        metavar='FILE',
        help='Write fixed prompt to file (requires --fix)'
    )

    args = parser.parse_args()

    if not args.diagnose:
        parser.print_help()
        return 0

    # Read prompt
    try:
        if args.diagnose == '-':
            prompt = sys.stdin.read()
        else:
            with open(args.diagnose, 'r', encoding='utf-8') as f:
                prompt = f.read()
    except FileNotFoundError:
        print(f"Error: File not found: {args.diagnose}", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"Error reading file: {e}", file=sys.stderr)
        return 1

    # Run diagnosis
    doctor = PromptDoctor(verbose=args.verbose)
    result = doctor.diagnose_prompt(prompt)

    # Output results
    if args.json:
        print(json.dumps(result.to_dict(), indent=2))
    else:
        print(format_report(result, verbose=args.verbose))

    # Auto-fix if requested
    if args.fix:
        fixed_prompt = doctor.auto_fix(prompt, result)

        if args.output:
            try:
                with open(args.output, 'w', encoding='utf-8') as f:
                    f.write(fixed_prompt)
                print(f"\nFixed prompt written to: {args.output}")
            except Exception as e:
                print(f"Error writing fixed prompt: {e}", file=sys.stderr)
                return 1
        else:
            print("\n" + "=" * 70)
            print("FIXED PROMPT:")
            print("=" * 70)
            print(fixed_prompt)

    # Exit code based on quality
    if result.quality_score < 40:
        return 2  # Critical issues
    elif result.quality_score < 60:
        return 1  # Needs improvement
    else:
        return 0  # Good


if __name__ == '__main__':
    sys.exit(main())
