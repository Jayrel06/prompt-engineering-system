#!/usr/bin/env python3
"""
Smart Prompt Generator

Combines context-loader.py and smart_context.py for optimal context selection.

This wrapper provides a unified interface that:
1. Uses context-loader for baseline mode-based context
2. Uses smart_context for AI-driven relevance selection
3. Merges both for comprehensive, optimized prompts
"""

import argparse
import subprocess
import sys
from pathlib import Path
from typing import List, Optional

# Add to path
sys.path.insert(0, str(Path(__file__).parent))

from smart_context import (
    SemanticScorer,
    discover_context_files,
    score_relevance,
    select_context,
    get_dynamic_context,
    format_output,
    ContextChunk
)

from context_loader import CONTEXT_RULES, assemble_context


def get_mode_context(
    task: str,
    mode: str = "full",
    framework: Optional[str] = None,
    project: Optional[str] = None,
    verbose: bool = False
) -> str:
    """Get context using traditional mode-based loader."""
    if verbose:
        print(f"Loading mode-based context: {mode}", file=sys.stderr)

    return assemble_context(
        task=task,
        mode=mode,
        framework=framework,
        project=project,
        verbose=verbose
    )


def get_smart_context(
    task: str,
    max_tokens: int = 6000,
    top_n: Optional[int] = None,
    boost_categories: dict = None,
    min_score: float = 0.1,
    include_dynamic: bool = False,
    verbose: bool = False
) -> tuple[List[ContextChunk], Optional[dict]]:
    """Get context using smart semantic selection."""
    if verbose:
        print(f"Performing smart context selection...", file=sys.stderr)

    # Initialize scorer
    scorer = SemanticScorer(use_cache=True)

    # Discover and score
    chunks = discover_context_files()

    if verbose:
        print(f"Found {len(chunks)} context files", file=sys.stderr)

    scored = score_relevance(task, chunks, scorer, boost_categories)

    # Select best
    selected = select_context(
        scored,
        max_tokens=max_tokens,
        top_n=top_n,
        min_score=min_score
    )

    if verbose:
        total_tokens = sum(c.token_count for c in selected)
        print(f"Selected {len(selected)} chunks ({total_tokens} tokens)", file=sys.stderr)

    # Get dynamic context
    dynamic = None
    if include_dynamic:
        dynamic = get_dynamic_context()
        if verbose:
            print(f"Gathered dynamic context ({len(dynamic)} items)", file=sys.stderr)

    return selected, dynamic


def merge_contexts(
    task: str,
    mode_context: Optional[str],
    smart_chunks: List[ContextChunk],
    dynamic: Optional[dict],
    strategy: str = "smart_only"
) -> str:
    """Merge mode-based and smart context based on strategy."""

    sections = []

    # Header
    sections.append("# Context-Enriched Prompt")
    sections.append("")
    sections.append(f"**Task:** {task}")
    sections.append("")

    # Add mode context if using hybrid strategy
    if strategy in ["mode_only", "hybrid"] and mode_context:
        sections.append("## Mode-Based Context")
        sections.append("")
        sections.append(mode_context)
        sections.append("")

    # Add smart context if using smart or hybrid strategy
    if strategy in ["smart_only", "hybrid"] and smart_chunks:
        sections.append("## AI-Selected Context")
        sections.append("")
        total_tokens = sum(c.token_count for c in smart_chunks)
        sections.append(f"*Selected {len(smart_chunks)} most relevant chunks (~{total_tokens} tokens)*")
        sections.append("")

        for i, chunk in enumerate(smart_chunks, 1):
            source_name = Path(chunk.source).name
            sections.append(f"### {i}. {source_name}")
            sections.append("")
            sections.append(chunk.content)
            sections.append("")

    # Add dynamic context
    if dynamic:
        sections.append("---")
        sections.append("")
        sections.append("## Dynamic Context")
        sections.append("")
        for key, value in dynamic.items():
            sections.append(f"### {key.replace('_', ' ').title()}")
            sections.append("```")
            sections.append(value)
            sections.append("```")
            sections.append("")

    return "\n".join(sections)


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Smart prompt generator with dual-mode context selection",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Strategies:
  smart_only  - Use AI-based semantic selection (default)
  mode_only   - Use traditional mode-based selection
  hybrid      - Combine both mode and smart selection

Examples:
  # Smart selection only (default)
  python smart_prompt.py --task "Debug API authentication"

  # Mode-based only
  python smart_prompt.py --task "Plan Q1 strategy" --strategy mode_only --mode planning

  # Hybrid (best of both)
  python smart_prompt.py --task "Implement new feature" --strategy hybrid --mode technical

  # With category boost
  python smart_prompt.py --task "Fix OAuth2 flow" --boost technical=0.5

  # Include git status
  python smart_prompt.py --task "Continue dev work" --include-dynamic

  # Export to file
  python smart_prompt.py --task "Design architecture" -o prompt.md
        """
    )

    # Strategy
    parser.add_argument('--strategy', choices=['smart_only', 'mode_only', 'hybrid'],
                       default='smart_only',
                       help="Context selection strategy (default: smart_only)")

    # Task
    parser.add_argument('--task', required=True,
                       help="Task description")

    # Mode-based options
    parser.add_argument('--mode',
                       choices=['full', 'minimal', 'planning', 'technical',
                               'communication', 'analysis', 'handoff'],
                       help="Mode for traditional context loading")
    parser.add_argument('--framework',
                       help="Specific framework to include")
    parser.add_argument('--project',
                       help="Project name for additional context")

    # Smart selection options
    parser.add_argument('--max-tokens', type=int, default=6000,
                       help="Maximum tokens for smart selection (default: 6000)")
    parser.add_argument('--top-n', type=int,
                       help="Limit to top N most relevant chunks")
    parser.add_argument('--min-score', type=float, default=0.1,
                       help="Minimum relevance score (0-1, default: 0.1)")
    parser.add_argument('--boost', action='append', dest='boost_categories',
                       metavar='CATEGORY=BOOST',
                       help="Boost category relevance (e.g., technical=0.5)")

    # Dynamic context
    parser.add_argument('--include-dynamic', action='store_true',
                       help="Include git status, recent files, etc.")

    # Output
    parser.add_argument('--output', '-o', type=Path,
                       help="Output file (default: stdout)")
    parser.add_argument('--verbose', '-v', action='store_true',
                       help="Verbose output")

    args = parser.parse_args()

    # Parse boost categories
    boost_categories = {}
    if args.boost_categories:
        for boost_spec in args.boost_categories:
            try:
                category, boost_str = boost_spec.split('=')
                boost_categories[category.strip()] = float(boost_str.strip())
            except ValueError:
                print(f"Warning: Invalid boost format: {boost_spec}", file=sys.stderr)

    # Get mode context if needed
    mode_context = None
    if args.strategy in ['mode_only', 'hybrid']:
        mode = args.mode or 'full'
        mode_context = get_mode_context(
            task=args.task,
            mode=mode,
            framework=args.framework,
            project=args.project,
            verbose=args.verbose
        )

    # Get smart context if needed
    smart_chunks = []
    dynamic = None
    if args.strategy in ['smart_only', 'hybrid']:
        smart_chunks, dynamic = get_smart_context(
            task=args.task,
            max_tokens=args.max_tokens,
            top_n=args.top_n,
            boost_categories=boost_categories,
            min_score=args.min_score,
            include_dynamic=args.include_dynamic,
            verbose=args.verbose
        )

    # Merge contexts
    output = merge_contexts(
        task=args.task,
        mode_context=mode_context,
        smart_chunks=smart_chunks,
        dynamic=dynamic,
        strategy=args.strategy
    )

    # Write output
    if args.output:
        args.output.write_text(output, encoding='utf-8')
        print(f"Prompt written to {args.output}", file=sys.stderr)
    else:
        print(output)


if __name__ == '__main__':
    main()
