#!/usr/bin/env python3
"""
Reflection System - Generates weekly reflections and identifies patterns in prompt usage.

This script analyzes captured outputs and prompts from the vector database to:
- Generate weekly reflection prompts
- Identify patterns in successful/unsuccessful prompts
- Suggest improvements based on learnings
- Track what-worked/what-didn't patterns
- Output structured reflection reports
"""

import argparse
import sys
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Dict, Any, Optional
from collections import Counter, defaultdict

from qdrant_client import QdrantClient
from qdrant_client.models import Filter, FieldCondition, Range, DatetimeRange
from sentence_transformers import SentenceTransformer


# Get project root
SCRIPT_DIR = Path(__file__).parent
PROJECT_ROOT = SCRIPT_DIR.parent
LEARNINGS_DIR = PROJECT_ROOT / "context" / "learnings"
FRAMEWORKS_DIR = PROJECT_ROOT / "frameworks"


class ReflectionService:
    """Service for analyzing prompt patterns and generating reflections."""

    def __init__(
        self,
        qdrant_host: str = "localhost",
        qdrant_port: int = 6333,
        model_name: str = "all-MiniLM-L6-v2",
        collection_name: str = "prompt_context"
    ):
        """Initialize the reflection service."""
        self.collection_name = collection_name

        print(f"Loading embedding model: {model_name}...")
        try:
            self.model = SentenceTransformer(model_name)
            print("Model loaded successfully.")
        except Exception as e:
            print(f"Error loading model: {e}", file=sys.stderr)
            sys.exit(1)

        print(f"Connecting to Qdrant at {qdrant_host}:{qdrant_port}...")
        try:
            self.client = QdrantClient(host=qdrant_host, port=qdrant_port)
            print("Connected to Qdrant successfully.")
        except Exception as e:
            print(f"Error connecting to Qdrant: {e}", file=sys.stderr)
            print("Make sure Qdrant is running on localhost:6333", file=sys.stderr)
            sys.exit(1)

    def get_recent_entries(
        self,
        days: int = 7,
        category: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Get all entries from the last N days.

        Args:
            days: Number of days to look back
            category: Optional category filter

        Returns:
            List of entries with metadata
        """
        print(f"\nFetching entries from the last {days} days...")

        try:
            # Calculate date range
            now = datetime.utcnow()
            start_date = now - timedelta(days=days)

            # Get all points (Qdrant doesn't have date range filter in scroll, so we filter manually)
            scroll_result = self.client.scroll(
                collection_name=self.collection_name,
                limit=1000,  # Adjust based on expected volume
                with_payload=True,
                with_vectors=False
            )

            points = scroll_result[0]

            # Filter by date and category
            entries = []
            for point in points:
                timestamp_str = point.payload.get("timestamp", "")
                if not timestamp_str:
                    continue

                try:
                    entry_date = datetime.fromisoformat(timestamp_str.replace('Z', '+00:00'))
                except:
                    continue

                # Check if within date range
                if entry_date < start_date:
                    continue

                # Check category if specified
                if category and point.payload.get("category") != category:
                    continue

                entries.append({
                    "id": point.id,
                    "text": point.payload.get("text", ""),
                    "category": point.payload.get("category", "unknown"),
                    "tags": point.payload.get("tags", []),
                    "timestamp": timestamp_str,
                    "source_file": point.payload.get("source_file", "unknown")
                })

            print(f"Found {len(entries)} entries")
            return sorted(entries, key=lambda x: x["timestamp"], reverse=True)

        except Exception as e:
            print(f"Error fetching entries: {e}", file=sys.stderr)
            return []

    def analyze_patterns(self, entries: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Analyze patterns in entries.

        Returns:
            Dictionary containing pattern analysis
        """
        print("\nAnalyzing patterns...")

        analysis = {
            "total_entries": len(entries),
            "categories": Counter(),
            "tags": Counter(),
            "daily_count": defaultdict(int),
            "popular_topics": [],
            "common_patterns": []
        }

        # Count categories and tags
        for entry in entries:
            analysis["categories"][entry["category"]] += 1

            for tag in entry["tags"]:
                analysis["tags"][tag] += 1

            # Count by day
            try:
                date = datetime.fromisoformat(entry["timestamp"].replace('Z', '+00:00'))
                day = date.strftime("%Y-%m-%d")
                analysis["daily_count"][day] += 1
            except:
                pass

        # Get top tags as popular topics
        analysis["popular_topics"] = [tag for tag, count in analysis["tags"].most_common(10)]

        # Identify common patterns by clustering similar texts
        if len(entries) >= 3:
            analysis["common_patterns"] = self._identify_text_patterns(entries)

        return analysis

    def _identify_text_patterns(self, entries: List[Dict[str, Any]]) -> List[str]:
        """
        Identify common patterns by analyzing text snippets.

        Args:
            entries: List of entries to analyze

        Returns:
            List of identified patterns
        """
        patterns = []

        # Look for common phrases
        all_text = " ".join([e["text"][:200] for e in entries])  # Use snippets
        words = all_text.lower().split()

        # Find common bigrams
        bigrams = [" ".join(words[i:i+2]) for i in range(len(words)-1)]
        common_bigrams = Counter(bigrams).most_common(5)

        for bigram, count in common_bigrams:
            if count >= 3:  # Appears at least 3 times
                patterns.append(f"Frequent phrase: '{bigram}' (appears {count} times)")

        # Analyze by category
        category_patterns = defaultdict(list)
        for entry in entries:
            category_patterns[entry["category"]].append(entry["text"][:100])

        for category, texts in category_patterns.items():
            if len(texts) >= 3:
                patterns.append(f"Category '{category}': {len(texts)} entries")

        return patterns

    def compare_with_learnings(
        self,
        entries: List[Dict[str, Any]]
    ) -> Dict[str, List[str]]:
        """
        Compare recent entries with documented learnings.

        Returns:
            Dictionary with suggestions and alignments
        """
        print("\nComparing with documented learnings...")

        what_works_file = LEARNINGS_DIR / "what-works.md"
        what_doesnt_file = LEARNINGS_DIR / "what-doesnt.md"

        suggestions = {
            "aligned_with_best_practices": [],
            "potential_anti_patterns": [],
            "new_learnings_to_add": [],
            "patterns_to_validate": []
        }

        # Load existing learnings
        what_works = ""
        what_doesnt = ""

        if what_works_file.exists():
            what_works = what_works_file.read_text(encoding='utf-8').lower()

        if what_doesnt_file.exists():
            what_doesnt = what_doesnt_file.read_text(encoding='utf-8').lower()

        # Analyze entries against learnings
        for entry in entries:
            text_lower = entry["text"].lower()

            # Check for known good patterns
            if "step by step" in text_lower or "chain-of-thought" in text_lower:
                suggestions["aligned_with_best_practices"].append(
                    "Using chain-of-thought reasoning"
                )

            if "output format" in text_lower or "json" in text_lower:
                suggestions["aligned_with_best_practices"].append(
                    "Specifying output format"
                )

            # Check for potential anti-patterns
            if len(entry["text"]) > 3000:
                suggestions["potential_anti_patterns"].append(
                    f"Very long prompt ({len(entry['text'])} chars) - consider breaking into chains"
                )

            if entry["category"] == "output" and "error" in text_lower:
                suggestions["patterns_to_validate"].append(
                    "Error in output - review what went wrong"
                )

        # Deduplicate
        for key in suggestions:
            suggestions[key] = list(set(suggestions[key]))

        return suggestions

    def generate_reflection_report(
        self,
        days: int = 7,
        output_format: str = "markdown"
    ) -> str:
        """
        Generate a complete reflection report.

        Args:
            days: Number of days to analyze
            output_format: Output format (markdown or json)

        Returns:
            Formatted reflection report
        """
        entries = self.get_recent_entries(days=days)

        if not entries:
            return "No entries found for the specified period."

        analysis = self.analyze_patterns(entries)
        suggestions = self.compare_with_learnings(entries)

        if output_format == "json":
            import json
            return json.dumps({
                "period": f"Last {days} days",
                "analysis": analysis,
                "suggestions": suggestions
            }, indent=2, default=str)

        # Generate Markdown report
        report_lines = []

        # Header
        report_lines.append(f"# Reflection Report")
        report_lines.append(f"\n**Period:** Last {days} days")
        report_lines.append(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report_lines.append(f"\n---\n")

        # Summary
        report_lines.append("## Summary\n")
        report_lines.append(f"- **Total Entries:** {analysis['total_entries']}")
        report_lines.append(f"- **Categories Used:** {len(analysis['categories'])}")
        report_lines.append(f"- **Unique Tags:** {len(analysis['tags'])}")
        report_lines.append(f"- **Most Active Day:** {max(analysis['daily_count'].items(), key=lambda x: x[1])[0] if analysis['daily_count'] else 'N/A'}")
        report_lines.append("\n")

        # Category Breakdown
        report_lines.append("## Category Breakdown\n")
        for category, count in analysis['categories'].most_common():
            report_lines.append(f"- **{category}:** {count} entries")
        report_lines.append("\n")

        # Popular Topics
        if analysis['popular_topics']:
            report_lines.append("## Popular Topics\n")
            for topic in analysis['popular_topics'][:10]:
                count = analysis['tags'][topic]
                report_lines.append(f"- {topic} ({count} mentions)")
            report_lines.append("\n")

        # Patterns Identified
        if analysis['common_patterns']:
            report_lines.append("## Patterns Identified\n")
            for pattern in analysis['common_patterns']:
                report_lines.append(f"- {pattern}")
            report_lines.append("\n")

        # Alignment with Best Practices
        if suggestions['aligned_with_best_practices']:
            report_lines.append("## What's Working Well\n")
            for practice in set(suggestions['aligned_with_best_practices']):
                report_lines.append(f"- {practice}")
            report_lines.append("\n")

        # Potential Improvements
        if suggestions['potential_anti_patterns']:
            report_lines.append("## Areas for Improvement\n")
            for anti_pattern in suggestions['potential_anti_patterns']:
                report_lines.append(f"- {anti_pattern}")
            report_lines.append("\n")

        # Items to Validate
        if suggestions['patterns_to_validate']:
            report_lines.append("## Patterns to Validate\n")
            for pattern in set(suggestions['patterns_to_validate']):
                report_lines.append(f"- {pattern}")
            report_lines.append("\n")

        # Reflection Questions
        report_lines.append("## Reflection Questions\n")
        report_lines.append("1. What prompts worked particularly well this week?")
        report_lines.append("2. What patterns emerged that should be documented?")
        report_lines.append("3. What learnings should be added to what-works.md or what-doesnt.md?")
        report_lines.append("4. What templates or frameworks need updating?")
        report_lines.append("5. What topics require deeper exploration?")
        report_lines.append("\n")

        # Next Steps
        report_lines.append("## Recommended Next Steps\n")
        if analysis['total_entries'] < 5:
            report_lines.append("- Capture more prompt outputs to build pattern database")
        if len(analysis['categories']) == 1:
            report_lines.append("- Diversify prompt categories for broader learning")
        if not suggestions['aligned_with_best_practices']:
            report_lines.append("- Review best practices in context/learnings/what-works.md")
        if suggestions['potential_anti_patterns']:
            report_lines.append("- Address identified anti-patterns in upcoming prompts")
        report_lines.append("\n")

        return "\n".join(report_lines)

    def generate_weekly_prompts(self) -> List[str]:
        """
        Generate reflection prompts based on the week's activity.

        Returns:
            List of reflection prompt questions
        """
        entries = self.get_recent_entries(days=7)
        analysis = self.analyze_patterns(entries)

        prompts = [
            "What was the most successful prompt or interaction this week?",
            "What patterns or approaches worked consistently well?",
            "What didn't work as expected, and why?",
            "What new insights or learnings emerged?",
        ]

        # Add context-specific prompts
        if analysis['total_entries'] > 10:
            prompts.append(f"You created {analysis['total_entries']} entries this week. What themes connect them?")

        if len(analysis['categories']) >= 3:
            top_category = analysis['categories'].most_common(1)[0][0]
            prompts.append(f"Your focus was on '{top_category}' category. What drove this focus?")

        if analysis['popular_topics']:
            top_topic = analysis['popular_topics'][0]
            prompts.append(f"The tag '{top_topic}' appeared frequently. What are you learning about this topic?")

        prompts.extend([
            "What should be added to the learnings repository?",
            "What templates or frameworks would make your work more efficient?",
            "What experiments do you want to try next week?"
        ])

        return prompts


def main():
    """Main entry point for the script."""
    parser = argparse.ArgumentParser(
        description="Generate reflection reports and identify prompt patterns",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Generate weekly reflection report
  python reflection.py --report --days 7

  # Generate reflection prompts
  python reflection.py --prompts

  # Analyze patterns only
  python reflection.py --analyze --days 14

  # Save report to file
  python reflection.py --report --output reflection.md

  # JSON output
  python reflection.py --report --format json
        """
    )

    # Action arguments
    action_group = parser.add_mutually_exclusive_group(required=True)
    action_group.add_argument(
        "--report",
        action="store_true",
        help="Generate full reflection report"
    )
    action_group.add_argument(
        "--prompts",
        action="store_true",
        help="Generate weekly reflection prompts"
    )
    action_group.add_argument(
        "--analyze",
        action="store_true",
        help="Analyze patterns only"
    )

    # Configuration arguments
    parser.add_argument(
        "--days",
        type=int,
        default=7,
        help="Number of days to analyze (default: 7)"
    )
    parser.add_argument(
        "--format",
        choices=["markdown", "json"],
        default="markdown",
        help="Output format (default: markdown)"
    )
    parser.add_argument(
        "--output",
        "-o",
        type=str,
        help="Output file path (default: stdout)"
    )

    # Connection arguments
    parser.add_argument(
        "--host",
        type=str,
        default="localhost",
        help="Qdrant host (default: localhost)"
    )
    parser.add_argument(
        "--port",
        type=int,
        default=6333,
        help="Qdrant port (default: 6333)"
    )

    args = parser.parse_args()

    # Initialize service
    try:
        service = ReflectionService(
            qdrant_host=args.host,
            qdrant_port=args.port
        )

        output = ""

        if args.report:
            print("\n" + "=" * 80)
            print("GENERATING REFLECTION REPORT")
            print("=" * 80)
            output = service.generate_reflection_report(
                days=args.days,
                output_format=args.format
            )

        elif args.prompts:
            print("\n" + "=" * 80)
            print("GENERATING REFLECTION PROMPTS")
            print("=" * 80)
            prompts = service.generate_weekly_prompts()
            output_lines = ["# Weekly Reflection Prompts\n"]
            for i, prompt in enumerate(prompts, 1):
                output_lines.append(f"{i}. {prompt}\n")
            output = "\n".join(output_lines)

        elif args.analyze:
            print("\n" + "=" * 80)
            print("ANALYZING PATTERNS")
            print("=" * 80)
            entries = service.get_recent_entries(days=args.days)
            analysis = service.analyze_patterns(entries)
            suggestions = service.compare_with_learnings(entries)

            import json
            output = json.dumps({
                "analysis": analysis,
                "suggestions": suggestions
            }, indent=2, default=str)

        # Output results
        if args.output:
            output_path = Path(args.output)
            output_path.write_text(output, encoding='utf-8')
            print(f"\nOutput written to: {args.output}")
        else:
            print("\n" + "=" * 80)
            print(output)

        print("\nReflection generation completed successfully!")

    except Exception as e:
        print(f"\nReflection generation failed: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
