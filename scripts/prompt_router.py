#!/usr/bin/env python3
"""
Automatic Prompt Router

Analyzes task descriptions and selects the optimal prompting framework
and techniques based on task characteristics.
"""

import re
import json
from pathlib import Path
from typing import Dict, List, Optional
from dataclasses import dataclass


@dataclass
class RoutingResult:
    """Result of prompt routing analysis."""
    primary_framework: str
    framework_path: str
    techniques: List[str]
    model_recommendation: str
    confidence: float
    reasoning: str


# Task type patterns and their associated frameworks
TASK_PATTERNS = {
    "reasoning": {
        "patterns": [
            r"\b(why|how come|explain|reason|cause|because)\b",
            r"\b(analyze|evaluate|assess|compare|contrast)\b",
            r"\b(think through|figure out|understand)\b",
            r"\b(pros? and cons?|trade-?offs?|advantages?|disadvantages?)\b",
        ],
        "framework": "chain-of-thought",
        "path": "frameworks/prompting/chain-of-thought.md",
        "techniques": ["zero-shot-cot", "step-by-step"],
        "model": "claude-sonnet-4-20250514",
    },
    "math": {
        "patterns": [
            r"\b(calculate|compute|solve|equation|formula)\b",
            r"\b(sum|total|average|percentage|ratio)\b",
            r"\b\d+\s*[\+\-\*\/]\s*\d+\b",
            r"\b(math|arithmetic|algebra|geometry)\b",
        ],
        "framework": "chain-of-thought",
        "path": "frameworks/prompting/chain-of-thought.md",
        "techniques": ["zero-shot-cot", "show-work"],
        "model": "claude-sonnet-4-20250514",
    },
    "code": {
        "patterns": [
            r"\b(code|program|function|class|method|api)\b",
            r"\b(implement|build|create|develop|write)\b.*\b(script|app|tool)\b",
            r"\b(bug|fix|debug|error|exception)\b",
            r"\b(python|javascript|typescript|java|rust|go)\b",
        ],
        "framework": "code-generation-chain",
        "path": "chains/code-generation/chain.md",
        "techniques": ["requirements-first", "architecture-design", "self-review"],
        "model": "claude-sonnet-4-20250514",
    },
    "formatting": {
        "patterns": [
            r"\b(format|structure|template|layout)\b",
            r"\b(json|xml|yaml|csv|markdown|html)\b",
            r"\b(table|list|bullet|header)\b",
            r"\b(like this|in this format|as follows)\b",
        ],
        "framework": "few-shot",
        "path": "frameworks/prompting/few-shot.md",
        "techniques": ["example-driven", "format-specification"],
        "model": "claude-haiku",
    },
    "extraction": {
        "patterns": [
            r"\b(extract|pull|get|find|identify)\b.*\b(from|in)\b",
            r"\b(parse|scrape|collect)\b",
            r"\b(entities|names|dates|numbers|emails)\b",
        ],
        "framework": "structured-prompting",
        "path": "frameworks/prompting/structured-prompting.md",
        "techniques": ["xml-tags", "explicit-output-format"],
        "model": "claude-haiku",
    },
    "planning": {
        "patterns": [
            r"\b(plan|strategy|roadmap|approach)\b",
            r"\b(steps?|phases?|stages?|milestones?)\b",
            r"\b(how (should|can|do) (i|we)|what is the best way)\b",
            r"\b(prioritize|schedule|timeline)\b",
        ],
        "framework": "first-principles",
        "path": "frameworks/planning/first-principles.md",
        "techniques": ["constraint-mapping", "pre-mortem"],
        "model": "claude-sonnet-4-20250514",
    },
    "decision": {
        "patterns": [
            r"\b(decide|choose|pick|select|which)\b",
            r"\b(should (i|we)|better to|option|alternative)\b",
            r"\b(vs\.?|versus|or)\b.*\b(vs\.?|versus|or)\b",
            r"\b(recommend|suggest|advise)\b",
        ],
        "framework": "decision-matrix",
        "path": "frameworks/decision/decision-matrix.md",
        "techniques": ["criteria-weighting", "reversibility-check"],
        "model": "claude-sonnet-4-20250514",
    },
    "research": {
        "patterns": [
            r"\b(research|investigate|explore|study|learn about)\b",
            r"\b(what (is|are)|tell me about|explain)\b",
            r"\b(overview|summary|introduction|basics)\b",
            r"\b(find|discover|uncover)\b.*\b(information|data|insights)\b",
        ],
        "framework": "research-to-action-chain",
        "path": "chains/research-to-action/chain.md",
        "techniques": ["deep-research", "synthesis"],
        "model": "claude-sonnet-4-20250514",
    },
    "content": {
        "patterns": [
            r"\b(write|draft|compose|create)\b.*\b(blog|article|post|email|copy)\b",
            r"\b(content|writing|copywriting)\b",
            r"\b(headline|title|hook|cta|call to action)\b",
        ],
        "framework": "content-creation-chain",
        "path": "chains/content-creation/chain.md",
        "techniques": ["outline-first", "critique-and-polish"],
        "model": "claude-sonnet-4-20250514",
    },
    "simple": {
        "patterns": [
            r"^.{0,50}$",  # Very short queries
            r"\b(what time|where is|who is|when did)\b",
            r"\b(define|definition of|meaning of)\b",
        ],
        "framework": "direct-answer",
        "path": None,
        "techniques": ["concise-response"],
        "model": "claude-haiku",
    },
}

# Technique combinations that work well together
TECHNIQUE_SYNERGIES = {
    ("chain-of-thought", "few-shot"): {
        "name": "few-shot-cot",
        "description": "Examples with reasoning traces - best for complex reasoning with specific output format",
        "boost": 0.15,
    },
    ("structured-prompting", "chain-of-thought"): {
        "name": "structured-reasoning",
        "description": "XML structure with step-by-step - best for complex extraction",
        "boost": 0.1,
    },
}


def calculate_pattern_score(text: str, patterns: List[str]) -> float:
    """Calculate how well text matches a set of patterns."""
    text_lower = text.lower()
    matches = 0
    for pattern in patterns:
        if re.search(pattern, text_lower, re.IGNORECASE):
            matches += 1
    return matches / len(patterns) if patterns else 0


def route_prompt(task_description: str) -> RoutingResult:
    """
    Analyze a task description and recommend the optimal prompting approach.

    Args:
        task_description: The user's task or question

    Returns:
        RoutingResult with framework, techniques, and model recommendations
    """
    scores: Dict[str, float] = {}

    # Score each task type
    for task_type, config in TASK_PATTERNS.items():
        score = calculate_pattern_score(task_description, config["patterns"])
        scores[task_type] = score

    # Get the best matching task type
    best_type = max(scores, key=scores.get)
    best_score = scores[best_type]

    # Get second best for potential technique synergy
    sorted_types = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    second_type = sorted_types[1][0] if len(sorted_types) > 1 else None
    second_score = sorted_types[1][1] if len(sorted_types) > 1 else 0

    config = TASK_PATTERNS[best_type]
    techniques = config["techniques"].copy()

    # Check for synergies
    if second_score > 0.3:
        synergy_key = (config["framework"].replace("-chain", ""),
                       TASK_PATTERNS[second_type]["framework"].replace("-chain", ""))
        if synergy_key in TECHNIQUE_SYNERGIES:
            synergy = TECHNIQUE_SYNERGIES[synergy_key]
            techniques.append(synergy["name"])
            best_score += synergy["boost"]

    # Determine confidence
    if best_score >= 0.6:
        confidence = 0.9
    elif best_score >= 0.4:
        confidence = 0.7
    elif best_score >= 0.2:
        confidence = 0.5
    else:
        confidence = 0.3

    # Build reasoning
    reasoning_parts = [f"Task type detected: {best_type} (score: {best_score:.2f})"]
    if second_score > 0.2:
        reasoning_parts.append(f"Secondary type: {second_type} (score: {second_score:.2f})")
    reasoning_parts.append(f"Recommended techniques: {', '.join(techniques)}")

    return RoutingResult(
        primary_framework=config["framework"],
        framework_path=config["path"],
        techniques=techniques,
        model_recommendation=config["model"],
        confidence=confidence,
        reasoning=" | ".join(reasoning_parts),
    )


def get_framework_content(framework_path: str, base_dir: Optional[Path] = None) -> Optional[str]:
    """Load the framework markdown content."""
    if not framework_path:
        return None

    if base_dir is None:
        base_dir = Path(__file__).parent.parent

    full_path = base_dir / framework_path
    if full_path.exists():
        return full_path.read_text(encoding="utf-8")
    return None


def build_enhanced_prompt(
    task: str,
    routing: RoutingResult,
    include_framework: bool = True,
    base_dir: Optional[Path] = None
) -> str:
    """
    Build an enhanced prompt using the routing results.

    Args:
        task: The original task
        routing: Routing analysis result
        include_framework: Whether to include framework content
        base_dir: Base directory for framework files

    Returns:
        Enhanced prompt string
    """
    parts = []

    # Add routing metadata as comment
    parts.append(f"<!-- Routing: {routing.primary_framework} | Confidence: {routing.confidence:.0%} -->")
    parts.append("")

    # Add technique-specific prefixes
    if "zero-shot-cot" in routing.techniques:
        parts.append("Think through this step by step:")
        parts.append("")

    if "requirements-first" in routing.techniques:
        parts.append("Before implementing, first clarify the requirements and identify any assumptions.")
        parts.append("")

    # Add the task
    parts.append(task)

    # Add technique-specific suffixes
    if "step-by-step" in routing.techniques:
        parts.append("")
        parts.append("Show your reasoning at each step.")

    if "explicit-output-format" in routing.techniques:
        parts.append("")
        parts.append("Structure your response clearly with labeled sections.")

    # Add confidence requirement
    parts.append("")
    parts.append("End with your confidence level (HIGH/MEDIUM/LOW) and brief reasoning.")

    return "\n".join(parts)


def main():
    """CLI interface for the prompt router."""
    import sys

    if len(sys.argv) < 2:
        print("Usage: python prompt_router.py <task_description>")
        print("       python prompt_router.py --interactive")
        sys.exit(1)

    if sys.argv[1] == "--interactive":
        print("Prompt Router - Interactive Mode")
        print("Enter tasks to analyze (Ctrl+C to exit)")
        print("-" * 40)

        while True:
            try:
                task = input("\nTask: ").strip()
                if not task:
                    continue

                result = route_prompt(task)
                print(f"\nFramework: {result.primary_framework}")
                print(f"Path: {result.framework_path}")
                print(f"Techniques: {', '.join(result.techniques)}")
                print(f"Model: {result.model_recommendation}")
                print(f"Confidence: {result.confidence:.0%}")
                print(f"Reasoning: {result.reasoning}")

            except KeyboardInterrupt:
                print("\nExiting.")
                break
    else:
        task = " ".join(sys.argv[1:])
        result = route_prompt(task)

        output = {
            "task": task,
            "routing": {
                "framework": result.primary_framework,
                "framework_path": result.framework_path,
                "techniques": result.techniques,
                "model": result.model_recommendation,
                "confidence": result.confidence,
                "reasoning": result.reasoning,
            }
        }
        print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
