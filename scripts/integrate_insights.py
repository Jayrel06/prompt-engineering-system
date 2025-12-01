#!/usr/bin/env python3
"""
Insight Integration Script

Analyzes scraped content from Reddit/GitHub and suggests updates to
existing frameworks or creates drafts for new frameworks.
"""

import os
import json
import re
from pathlib import Path
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass
from datetime import datetime
from collections import Counter

try:
    import anthropic
    HAS_ANTHROPIC = True
except ImportError:
    HAS_ANTHROPIC = False

try:
    from qdrant_client import QdrantClient
    HAS_QDRANT = True
except ImportError:
    HAS_QDRANT = False


@dataclass
class Insight:
    """An insight extracted from scraped content."""
    category: str
    title: str
    description: str
    source: str
    relevance_score: float
    actionable: bool
    suggested_framework: Optional[str]


@dataclass
class FrameworkUpdate:
    """A suggested update to an existing framework."""
    framework_path: str
    section: str
    current_content: Optional[str]
    suggested_addition: str
    reasoning: str
    priority: str  # HIGH, MEDIUM, LOW


@dataclass
class NewFramework:
    """A suggested new framework."""
    name: str
    category: str
    description: str
    content: str
    sources: List[str]


INSIGHT_CATEGORIES = [
    "prompting_technique",
    "model_behavior",
    "common_mistake",
    "best_practice",
    "tool_integration",
    "workflow_pattern",
    "performance_tip",
]


def load_scraped_data(data_dir: Path) -> List[Dict]:
    """Load scraped data from JSON files."""
    data = []

    if not data_dir.exists():
        return data

    for file_path in data_dir.glob("*.json"):
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = json.load(f)
                if isinstance(content, list):
                    data.extend(content)
                else:
                    data.append(content)
        except Exception as e:
            print(f"Warning: Could not load {file_path}: {e}")

    return data


def extract_insights_with_llm(
    content: List[Dict],
    categories: List[str] = INSIGHT_CATEGORIES
) -> List[Insight]:
    """Use LLM to extract actionable insights from scraped content."""
    if not HAS_ANTHROPIC:
        print("Warning: anthropic not installed, using rule-based extraction")
        return extract_insights_rules(content)

    client = anthropic.Anthropic()

    # Prepare content summary
    content_text = ""
    for item in content[:50]:  # Limit to avoid token limits
        title = item.get("title", "")
        body = item.get("body", item.get("content", ""))[:500]
        source = item.get("source", item.get("url", "unknown"))
        content_text += f"\n---\nTitle: {title}\nContent: {body}\nSource: {source}\n"

    prompt = f"""Analyze these scraped posts/content from Reddit and GitHub about prompt engineering and AI.

Extract actionable insights that could improve a prompt engineering system.

Categories to consider:
{', '.join(categories)}

Content:
{content_text}

For each insight found, provide:
1. category (from the list above)
2. title (brief, descriptive)
3. description (1-2 sentences)
4. source (which post it came from)
5. relevance_score (0.0-1.0, how useful is this)
6. actionable (true/false, can this be directly implemented)
7. suggested_framework (if applicable, which framework this relates to)

Return as JSON array of objects.
Only include insights with relevance_score >= 0.6
Limit to top 10 most valuable insights.
"""

    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=4096,
        messages=[{"role": "user", "content": prompt}]
    )

    # Parse JSON from response
    response_text = response.content[0].text

    # Find JSON in response
    json_match = re.search(r'\[[\s\S]*\]', response_text)
    if not json_match:
        return []

    try:
        insights_data = json.loads(json_match.group())
    except json.JSONDecodeError:
        return []

    insights = []
    for item in insights_data:
        insights.append(Insight(
            category=item.get("category", "best_practice"),
            title=item.get("title", ""),
            description=item.get("description", ""),
            source=item.get("source", ""),
            relevance_score=float(item.get("relevance_score", 0.5)),
            actionable=item.get("actionable", False),
            suggested_framework=item.get("suggested_framework")
        ))

    return insights


def extract_insights_rules(content: List[Dict]) -> List[Insight]:
    """Rule-based insight extraction (fallback when no LLM)."""
    insights = []

    # Keywords that indicate valuable content
    value_keywords = {
        "prompting_technique": ["prompt", "technique", "method", "approach", "strategy"],
        "best_practice": ["best practice", "tip", "trick", "learned", "works well"],
        "common_mistake": ["mistake", "avoid", "don't", "wrong", "error", "fail"],
        "performance_tip": ["faster", "better", "improve", "optimize", "performance"],
    }

    for item in content:
        text = f"{item.get('title', '')} {item.get('body', item.get('content', ''))}".lower()

        # Score by upvotes/stars if available
        score = item.get("upvotes", item.get("stars", 0))
        if score < 10:
            continue

        # Categorize
        for category, keywords in value_keywords.items():
            if any(kw in text for kw in keywords):
                insights.append(Insight(
                    category=category,
                    title=item.get("title", "")[:100],
                    description=text[:200],
                    source=item.get("source", item.get("url", "unknown")),
                    relevance_score=min(score / 100, 1.0),
                    actionable=True,
                    suggested_framework=None
                ))
                break

    # Sort by relevance and limit
    insights.sort(key=lambda x: x.relevance_score, reverse=True)
    return insights[:20]


def match_to_frameworks(
    insights: List[Insight],
    frameworks_dir: Path
) -> List[Tuple[Insight, str]]:
    """Match insights to existing frameworks."""
    matches = []

    # Load framework info
    frameworks = {}
    for framework_path in frameworks_dir.rglob("*.md"):
        rel_path = framework_path.relative_to(frameworks_dir)
        content = framework_path.read_text(encoding="utf-8")

        # Extract title
        title_match = re.search(r'^#\s+(.+)', content, re.MULTILINE)
        title = title_match.group(1) if title_match else framework_path.stem

        frameworks[str(rel_path)] = {
            "path": framework_path,
            "title": title,
            "content": content[:500],  # Preview
        }

    # Match insights to frameworks
    for insight in insights:
        if insight.suggested_framework:
            # Use LLM suggestion if available
            for path, fw in frameworks.items():
                if insight.suggested_framework.lower() in path.lower() or \
                   insight.suggested_framework.lower() in fw["title"].lower():
                    matches.append((insight, str(fw["path"])))
                    break
        else:
            # Simple keyword matching
            insight_text = f"{insight.title} {insight.description}".lower()
            best_match = None
            best_score = 0

            for path, fw in frameworks.items():
                fw_text = f"{fw['title']} {fw['content']}".lower()
                # Count shared words
                insight_words = set(insight_text.split())
                fw_words = set(fw_text.split())
                shared = len(insight_words & fw_words)

                if shared > best_score:
                    best_score = shared
                    best_match = str(fw["path"])

            if best_match and best_score >= 3:
                matches.append((insight, best_match))

    return matches


def generate_framework_updates(
    matches: List[Tuple[Insight, str]]
) -> List[FrameworkUpdate]:
    """Generate specific update suggestions for frameworks."""
    updates = []

    # Group by framework
    by_framework: Dict[str, List[Insight]] = {}
    for insight, path in matches:
        if path not in by_framework:
            by_framework[path] = []
        by_framework[path].append(insight)

    for path, insights in by_framework.items():
        # Create update suggestion
        additions = []
        for insight in insights[:3]:  # Limit per framework
            additions.append(f"- **{insight.title}**: {insight.description}")

        updates.append(FrameworkUpdate(
            framework_path=path,
            section="Community Insights",
            current_content=None,
            suggested_addition="\n".join(additions),
            reasoning=f"Based on {len(insights)} insights from community discussions",
            priority="MEDIUM" if insights[0].relevance_score > 0.7 else "LOW"
        ))

    return updates


def generate_new_framework_draft(
    insights: List[Insight],
    category: str
) -> Optional[NewFramework]:
    """Generate a draft for a new framework based on insights."""
    # Group insights by category
    category_insights = [i for i in insights if i.category == category]

    if len(category_insights) < 3:
        return None

    # Build framework content
    content_parts = [
        f"# {category.replace('_', ' ').title()} Framework",
        "",
        "## Overview",
        "",
        "This framework captures patterns and practices from the prompt engineering community.",
        "",
        "## Key Patterns",
        "",
    ]

    for insight in category_insights[:10]:
        content_parts.append(f"### {insight.title}")
        content_parts.append("")
        content_parts.append(insight.description)
        content_parts.append("")
        content_parts.append(f"*Source: {insight.source}*")
        content_parts.append("")

    content_parts.extend([
        "## When to Use",
        "",
        "- [Add specific use cases]",
        "",
        "## Prompt Template",
        "",
        "```",
        "[Add template based on patterns above]",
        "```",
        "",
        "---",
        f"*Generated from {len(category_insights)} community insights on {datetime.now().strftime('%Y-%m-%d')}*",
    ])

    return NewFramework(
        name=category.replace("_", "-"),
        category="prompting",
        description=f"Framework for {category.replace('_', ' ')} based on community insights",
        content="\n".join(content_parts),
        sources=[i.source for i in category_insights[:5]]
    )


def save_updates(
    updates: List[FrameworkUpdate],
    new_frameworks: List[NewFramework],
    output_dir: Path
):
    """Save update suggestions and new framework drafts."""
    output_dir.mkdir(parents=True, exist_ok=True)

    # Save updates report
    report = {
        "generated_at": datetime.now().isoformat(),
        "updates": [
            {
                "framework": u.framework_path,
                "section": u.section,
                "addition": u.suggested_addition,
                "reasoning": u.reasoning,
                "priority": u.priority,
            }
            for u in updates
        ],
        "new_frameworks": [
            {
                "name": f.name,
                "category": f.category,
                "description": f.description,
            }
            for f in new_frameworks
        ]
    }

    report_path = output_dir / "integration_report.json"
    with open(report_path, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)

    print(f"Saved integration report to {report_path}")

    # Save new framework drafts
    drafts_dir = output_dir / "framework_drafts"
    drafts_dir.mkdir(exist_ok=True)

    for framework in new_frameworks:
        draft_path = drafts_dir / f"{framework.name}.md"
        with open(draft_path, "w", encoding="utf-8") as f:
            f.write(framework.content)
        print(f"Saved draft framework to {draft_path}")


def main():
    """Main entry point."""
    import argparse

    parser = argparse.ArgumentParser(
        description="Integrate scraped insights into frameworks"
    )
    parser.add_argument("--data-dir", type=Path,
                        default=Path(__file__).parent / "scrapers" / "data",
                        help="Directory containing scraped JSON data")
    parser.add_argument("--frameworks-dir", type=Path,
                        default=Path(__file__).parent.parent / "frameworks",
                        help="Directory containing framework files")
    parser.add_argument("--output-dir", type=Path,
                        default=Path(__file__).parent.parent / "outputs" / "integrations",
                        help="Directory for output files")
    parser.add_argument("--use-llm", action="store_true",
                        help="Use LLM for insight extraction (requires anthropic)")
    parser.add_argument("--dry-run", action="store_true",
                        help="Only analyze, don't save files")

    args = parser.parse_args()

    # Load scraped data
    print(f"Loading scraped data from {args.data_dir}")
    content = load_scraped_data(args.data_dir)
    print(f"Found {len(content)} items")

    if not content:
        print("No scraped data found. Run the scrapers first:")
        print("  python scripts/scrapers/scrape_and_ingest.py")
        return

    # Extract insights
    print("Extracting insights...")
    if args.use_llm and HAS_ANTHROPIC:
        insights = extract_insights_with_llm(content)
    else:
        insights = extract_insights_rules(content)

    print(f"Found {len(insights)} insights")

    for insight in insights[:5]:
        print(f"  - [{insight.category}] {insight.title} (score: {insight.relevance_score:.2f})")

    # Match to frameworks
    print("\nMatching insights to existing frameworks...")
    matches = match_to_frameworks(insights, args.frameworks_dir)
    print(f"Found {len(matches)} matches")

    # Generate updates
    updates = generate_framework_updates(matches)
    print(f"Generated {len(updates)} framework update suggestions")

    # Generate new frameworks
    print("\nChecking for new framework opportunities...")
    new_frameworks = []
    category_counts = Counter(i.category for i in insights)

    for category, count in category_counts.items():
        if count >= 3:
            draft = generate_new_framework_draft(insights, category)
            if draft:
                new_frameworks.append(draft)
                print(f"  - Draft created for: {category}")

    # Save results
    if not args.dry_run:
        save_updates(updates, new_frameworks, args.output_dir)
    else:
        print("\nDry run - no files saved")
        print("\nSummary:")
        print(f"  - {len(updates)} framework updates suggested")
        print(f"  - {len(new_frameworks)} new framework drafts ready")


if __name__ == "__main__":
    main()
