#!/usr/bin/env python3
"""
Context Loader - Assembles context based on task type and loads relevant knowledge.
"""

import argparse
import os
import sys
from pathlib import Path
from typing import List, Dict, Optional

# Get project root
SCRIPT_DIR = Path(__file__).parent
PROJECT_ROOT = SCRIPT_DIR.parent
CONTEXT_DIR = PROJECT_ROOT / "context"
FRAMEWORKS_DIR = PROJECT_ROOT / "frameworks"
TEMPLATES_DIR = PROJECT_ROOT / "templates"

# Context loading rules based on task type
CONTEXT_RULES = {
    "planning": {
        "context_files": [
            "identity/core-values.md",
            "identity/decision-frameworks.md",
            "business/corereceptionai-overview.md",
            "learnings/what-works.md"
        ],
        "frameworks": ["planning/first-principles.md", "planning/pre-mortem.md"],
        "include_projects": True
    },
    "technical": {
        "context_files": [
            "technical/infrastructure-inventory.md",
            "technical/tool-preferences.md",
            "technical/coding-standards.md",
            "technical/n8n-patterns.md"
        ],
        "frameworks": ["technical/architecture-design.md", "technical/debugging.md"],
        "include_projects": True
    },
    "communication": {
        "context_files": [
            "identity/communication-style.md",
            "business/service-offerings.md",
            "business/target-markets.md"
        ],
        "frameworks": [],
        "include_projects": False
    },
    "analysis": {
        "context_files": [
            "identity/expertise-areas.md",
            "learnings/what-works.md",
            "learnings/what-doesnt.md"
        ],
        "frameworks": ["analysis/steelman-critique.md", "analysis/assumption-surfacing.md"],
        "include_projects": True
    },
    "minimal": {
        "context_files": [],
        "frameworks": [],
        "include_projects": False
    },
    "full": {
        "context_files": [
            "identity/core-values.md",
            "identity/expertise-areas.md",
            "business/corereceptionai-overview.md",
            "technical/infrastructure-inventory.md",
            "learnings/what-works.md"
        ],
        "frameworks": [],
        "include_projects": True
    },
    "handoff": {
        "context_files": [
            "technical/infrastructure-inventory.md",
            "technical/coding-standards.md",
            "technical/n8n-patterns.md"
        ],
        "frameworks": [],
        "include_projects": True,
        "template": "development/claude-code-handoff.md"
    }
}


def load_file(filepath: Path) -> str:
    """Load content from a file."""
    if filepath.exists():
        return filepath.read_text(encoding='utf-8')
    return f"[File not found: {filepath}]"


def find_framework(name: str) -> Optional[Path]:
    """Find a framework file by name."""
    # Check all framework subdirectories
    for category in ["planning", "analysis", "decision", "technical", "communication", "creation"]:
        path = FRAMEWORKS_DIR / category / f"{name}.md"
        if path.exists():
            return path
    return None


def assemble_context(
    task: str,
    mode: str = "full",
    framework: Optional[str] = None,
    project: Optional[str] = None,
    verbose: bool = False
) -> str:
    """Assemble complete context for a task."""

    rules = CONTEXT_RULES.get(mode, CONTEXT_RULES["full"])
    sections = []

    # Header
    sections.append("# Context-Enriched Prompt")
    sections.append("")

    # Add task
    sections.append("## Task")
    sections.append("")
    sections.append(task)
    sections.append("")

    # Load context files
    if rules["context_files"]:
        sections.append("---")
        sections.append("")
        sections.append("## Relevant Context")
        sections.append("")

        for filepath in rules["context_files"]:
            full_path = CONTEXT_DIR / filepath
            if full_path.exists():
                if verbose:
                    print(f"Loading context: {filepath}", file=sys.stderr)
                content = load_file(full_path)
                sections.append(f"### {filepath}")
                sections.append("")
                sections.append(content)
                sections.append("")

    # Load framework if specified or from rules
    frameworks_to_load = []
    if framework:
        fw_path = find_framework(framework)
        if fw_path:
            frameworks_to_load.append(fw_path)
        else:
            print(f"Warning: Framework '{framework}' not found", file=sys.stderr)
    else:
        for fw in rules.get("frameworks", []):
            fw_path = FRAMEWORKS_DIR / fw
            if fw_path.exists():
                frameworks_to_load.append(fw_path)

    if frameworks_to_load:
        sections.append("---")
        sections.append("")
        sections.append("## Thinking Framework")
        sections.append("")
        for fw_path in frameworks_to_load:
            if verbose:
                print(f"Loading framework: {fw_path.name}", file=sys.stderr)
            content = load_file(fw_path)
            sections.append(content)
            sections.append("")

    # Load template if specified
    if "template" in rules:
        template_path = TEMPLATES_DIR / rules["template"]
        if template_path.exists():
            if verbose:
                print(f"Loading template: {rules['template']}", file=sys.stderr)
            sections.append("---")
            sections.append("")
            sections.append("## Template")
            sections.append("")
            sections.append(load_file(template_path))
            sections.append("")

    # Load project context if specified
    if project and rules.get("include_projects"):
        project_path = CONTEXT_DIR / "projects" / "active" / f"{project}.md"
        if project_path.exists():
            if verbose:
                print(f"Loading project: {project}", file=sys.stderr)
            sections.append("---")
            sections.append("")
            sections.append(f"## Project Context: {project}")
            sections.append("")
            sections.append(load_file(project_path))
            sections.append("")

    return "\n".join(sections)


def main():
    parser = argparse.ArgumentParser(
        description="Assemble context for AI tasks",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Modes:
  full        - All core context (default)
  minimal     - Task only, no context
  planning    - Planning-focused context + frameworks
  technical   - Technical context + frameworks
  analysis    - Analysis context + frameworks
  communication - Communication context
  handoff     - Claude Code handoff template

Examples:
  python context-loader.py --task "Design a new workflow"
  python context-loader.py --mode planning --task "Q1 strategy"
  python context-loader.py --framework first-principles --task "Should I build or buy?"
        """
    )
    parser.add_argument("--mode", default="full",
                       choices=["full", "minimal", "planning", "technical",
                               "communication", "analysis", "handoff"],
                       help="Context assembly mode")
    parser.add_argument("--task", required=True, help="Task description")
    parser.add_argument("--framework", help="Specific framework to use")
    parser.add_argument("--project", help="Project name for additional context")
    parser.add_argument("--output", "-o", help="Output file (default: stdout)")
    parser.add_argument("--verbose", "-v", action="store_true",
                       help="Show context assembly details")

    args = parser.parse_args()

    # If framework is specified, override mode
    if args.framework and args.mode == "full":
        args.mode = "minimal"  # Just framework + task

    context = assemble_context(
        task=args.task,
        mode=args.mode,
        framework=args.framework,
        project=args.project,
        verbose=args.verbose
    )

    if args.output:
        Path(args.output).write_text(context, encoding='utf-8')
        print(f"Context written to {args.output}", file=sys.stderr)
    else:
        print(context)


if __name__ == "__main__":
    main()
