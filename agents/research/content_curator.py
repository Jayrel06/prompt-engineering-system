#!/usr/bin/env python3
"""
Content Curator Agent

Curates, organizes, and recommends content from various sources
for research and content creation purposes.
"""

import os
import json
import re
from datetime import datetime, timedelta
from typing import List, Dict, Optional
from dataclasses import dataclass, asdict
from pathlib import Path
from collections import defaultdict

try:
    import anthropic
    HAS_ANTHROPIC = True
except ImportError:
    HAS_ANTHROPIC = False


@dataclass
class ContentItem:
    """A piece of curated content."""
    title: str
    source: str
    url: str
    content_type: str  # "article", "video", "podcast", "tool", "case_study"
    summary: str
    key_takeaways: List[str]
    relevance_score: float
    topics: List[str]
    author: str
    date_published: str
    reading_time: str
    quality_score: float


@dataclass
class ContentBundle:
    """A curated bundle of related content."""
    theme: str
    description: str
    items: List[ContentItem]
    total_reading_time: str
    difficulty_level: str
    target_audience: str
    learning_outcomes: List[str]


class ContentCuratorAgent:
    """Agent that curates and organizes content for research."""

    CONTENT_SOURCES = [
        "arxiv",
        "hacker_news",
        "medium",
        "substack",
        "youtube",
        "podcasts",
        "github",
        "twitter",
        "linkedin"
    ]

    def __init__(self, topics: List[str] = None):
        self.topics = topics or ["AI", "automation", "prompt engineering"]
        self.client = anthropic.Anthropic() if HAS_ANTHROPIC else None
        self.content_library: Dict[str, List[ContentItem]] = defaultdict(list)

    def curate_content(
        self,
        theme: str,
        sources: Optional[List[str]] = None,
        max_items: int = 10,
        time_range: str = "7d"
    ) -> ContentBundle:
        """
        Curate content around a specific theme.

        Args:
            theme: Topic or theme to curate around
            sources: Content sources to include
            max_items: Maximum items to include
            time_range: How far back to look

        Returns:
            ContentBundle with curated items
        """
        sources = sources or self.CONTENT_SOURCES

        if not self.client:
            return self._generate_mock_bundle(theme)

        prompt = f"""You are a content curator specializing in AI and technology.

Curate the best recent content about: "{theme}"

Sources to consider: {', '.join(sources)}
Time range: {time_range}
Maximum items: {max_items}

For each piece of content, provide:
- Title
- Source platform
- URL (realistic example URL)
- Content type (article/video/podcast/tool/case_study)
- 2-3 sentence summary
- 3-5 key takeaways
- Relevance to AI consulting (0-1)
- Topics covered
- Author
- Date published
- Estimated reading/watching time
- Quality score (0-1)

Return as JSON:
{{
    "theme": "theme name",
    "description": "bundle description",
    "items": [
        {{
            "title": "string",
            "source": "string",
            "url": "string",
            "content_type": "string",
            "summary": "string",
            "key_takeaways": ["string"],
            "relevance_score": 0.0,
            "topics": ["string"],
            "author": "string",
            "date_published": "YYYY-MM-DD",
            "reading_time": "X min",
            "quality_score": 0.0
        }}
    ],
    "total_reading_time": "X hours",
    "difficulty_level": "beginner/intermediate/advanced",
    "target_audience": "who this is for",
    "learning_outcomes": ["what you'll learn"]
}}

Focus on high-quality, actionable content that would help an AI consultant.
"""

        response = self.client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=4096,
            messages=[{"role": "user", "content": prompt}]
        )

        response_text = response.content[0].text
        json_match = re.search(r'\{[\s\S]*\}', response_text)

        if json_match:
            try:
                data = json.loads(json_match.group())
                items = [ContentItem(**item) for item in data.get("items", [])]

                return ContentBundle(
                    theme=data.get("theme", theme),
                    description=data.get("description", ""),
                    items=items,
                    total_reading_time=data.get("total_reading_time", ""),
                    difficulty_level=data.get("difficulty_level", "intermediate"),
                    target_audience=data.get("target_audience", ""),
                    learning_outcomes=data.get("learning_outcomes", [])
                )
            except (json.JSONDecodeError, TypeError):
                pass

        return self._generate_mock_bundle(theme)

    def _generate_mock_bundle(self, theme: str) -> ContentBundle:
        """Generate mock bundle when API unavailable."""
        today = datetime.now()

        mock_items = [
            ContentItem(
                title="Building Production AI Agents: A Practical Guide",
                source="medium",
                url="https://medium.com/@example/ai-agents-guide",
                content_type="article",
                summary="Comprehensive guide to building AI agents that work in production. Covers architecture, error handling, and scaling considerations.",
                key_takeaways=[
                    "Start simple, add complexity as needed",
                    "Implement robust error handling from day one",
                    "Use structured outputs for reliability",
                    "Monitor and log everything"
                ],
                relevance_score=0.95,
                topics=["AI agents", "production systems", "architecture"],
                author="AI Engineering Expert",
                date_published=(today - timedelta(days=3)).strftime("%Y-%m-%d"),
                reading_time="15 min",
                quality_score=0.9
            ),
            ContentItem(
                title="The State of LLM Applications in 2024",
                source="substack",
                url="https://example.substack.com/llm-state-2024",
                content_type="article",
                summary="Analysis of how enterprises are actually using LLMs. Based on surveys and interviews with 200+ companies.",
                key_takeaways=[
                    "RAG is the most common pattern",
                    "Cost optimization is top priority",
                    "Evaluation remains challenging",
                    "Multi-model strategies emerging"
                ],
                relevance_score=0.88,
                topics=["LLM", "enterprise", "trends"],
                author="Industry Analyst",
                date_published=(today - timedelta(days=5)).strftime("%Y-%m-%d"),
                reading_time="20 min",
                quality_score=0.85
            ),
            ContentItem(
                title="Prompt Engineering Masterclass",
                source="youtube",
                url="https://youtube.com/watch?v=example",
                content_type="video",
                summary="Deep dive into advanced prompt engineering techniques with practical examples and live coding.",
                key_takeaways=[
                    "Chain-of-thought improves reasoning",
                    "Few-shot examples boost consistency",
                    "XML tags help with structure",
                    "Temperature affects creativity vs precision"
                ],
                relevance_score=0.92,
                topics=["prompt engineering", "LLM", "techniques"],
                author="AI YouTuber",
                date_published=(today - timedelta(days=7)).strftime("%Y-%m-%d"),
                reading_time="45 min",
                quality_score=0.88
            ),
            ContentItem(
                title="Voice AI Case Study: 50% Cost Reduction",
                source="linkedin",
                url="https://linkedin.com/pulse/example",
                content_type="case_study",
                summary="How a dental practice reduced phone handling costs by 50% with voice AI while improving patient satisfaction.",
                key_takeaways=[
                    "ROI achieved within 3 months",
                    "Patient satisfaction increased 20%",
                    "Staff freed for higher-value tasks",
                    "24/7 availability key benefit"
                ],
                relevance_score=0.94,
                topics=["voice AI", "case study", "ROI", "healthcare"],
                author="AI Consultant",
                date_published=(today - timedelta(days=2)).strftime("%Y-%m-%d"),
                reading_time="8 min",
                quality_score=0.9
            )
        ]

        return ContentBundle(
            theme=theme,
            description=f"Curated content collection on {theme} for AI consultants",
            items=mock_items,
            total_reading_time="1.5 hours",
            difficulty_level="intermediate",
            target_audience="AI consultants, business owners considering AI",
            learning_outcomes=[
                "Understand current AI agent architecture patterns",
                "Learn enterprise LLM adoption trends",
                "Master advanced prompt engineering",
                "See real ROI examples from voice AI"
            ]
        )

    def create_reading_list(
        self,
        goal: str,
        time_budget: str = "2h",
        level: str = "intermediate"
    ) -> Dict:
        """Create a focused reading list for a specific goal."""
        return {
            "goal": goal,
            "time_budget": time_budget,
            "level": level,
            "reading_list": [
                {
                    "order": 1,
                    "title": "Start here: Foundations",
                    "items": ["Foundation article 1", "Foundation article 2"],
                    "time": "30 min"
                },
                {
                    "order": 2,
                    "title": "Deep dive: Core concepts",
                    "items": ["Technical deep dive", "Practical examples"],
                    "time": "45 min"
                },
                {
                    "order": 3,
                    "title": "Apply: Hands-on",
                    "items": ["Tutorial", "Exercise"],
                    "time": "45 min"
                }
            ],
            "optional_extras": [
                "Advanced topic 1",
                "Related area exploration"
            ]
        }

    def get_daily_digest(self) -> Dict:
        """Generate a daily content digest."""
        today = datetime.now()

        return {
            "date": today.strftime("%Y-%m-%d"),
            "top_picks": [
                {
                    "title": "Today's must-read on AI",
                    "source": "HackerNews",
                    "why": "Trending discussion with practical insights"
                }
            ],
            "by_topic": {
                "AI Development": ["Article 1", "Video 1"],
                "Business Applications": ["Case study 1"],
                "Tools & Frameworks": ["New release notes"]
            },
            "quick_reads": ["5 min article 1", "5 min article 2"],
            "deep_dives": ["Long form piece for weekend reading"],
            "to_watch": ["Emerging topic to monitor"]
        }

    def to_dict(self, bundle: ContentBundle) -> Dict:
        """Convert bundle to dictionary."""
        return {
            "theme": bundle.theme,
            "description": bundle.description,
            "items": [asdict(item) for item in bundle.items],
            "total_reading_time": bundle.total_reading_time,
            "difficulty_level": bundle.difficulty_level,
            "target_audience": bundle.target_audience,
            "learning_outcomes": bundle.learning_outcomes
        }


def main():
    """Run content curation."""
    import argparse

    parser = argparse.ArgumentParser(description="Curate content")
    parser.add_argument("theme", nargs="?", default="AI agents",
                       help="Theme to curate content for")
    parser.add_argument("--sources", nargs="+",
                       help="Content sources to include")
    parser.add_argument("--max-items", type=int, default=10,
                       help="Maximum items to curate")
    parser.add_argument("--time-range", default="7d",
                       help="Time range for content")
    parser.add_argument("--digest", action="store_true",
                       help="Show daily digest instead")
    parser.add_argument("--reading-list", action="store_true",
                       help="Create reading list for theme")
    parser.add_argument("--output", type=Path,
                       help="Output file for JSON")

    args = parser.parse_args()

    agent = ContentCuratorAgent()

    if args.digest:
        digest = agent.get_daily_digest()
        print("\n📰 DAILY CONTENT DIGEST")
        print(f"Date: {digest['date']}")
        print("=" * 60)

        print("\n🌟 TOP PICKS:\n")
        for pick in digest['top_picks']:
            print(f"  • {pick['title']} ({pick['source']})")
            print(f"    Why: {pick['why']}")

        print("\n📚 BY TOPIC:\n")
        for topic, items in digest['by_topic'].items():
            print(f"  {topic}:")
            for item in items:
                print(f"    • {item}")

        return

    if args.reading_list:
        reading_list = agent.create_reading_list(goal=args.theme)
        print(f"\n📖 READING LIST: {reading_list['goal']}")
        print(f"Time budget: {reading_list['time_budget']}")
        print("=" * 60)

        for section in reading_list['reading_list']:
            print(f"\n{section['order']}. {section['title']} ({section['time']})")
            for item in section['items']:
                print(f"   • {item}")

        return

    bundle = agent.curate_content(
        theme=args.theme,
        sources=args.sources,
        max_items=args.max_items,
        time_range=args.time_range
    )

    print(f"\n📚 CONTENT BUNDLE: {bundle.theme}")
    print(f"Total reading time: {bundle.total_reading_time}")
    print(f"Level: {bundle.difficulty_level}")
    print("=" * 60)

    print(f"\n{bundle.description}\n")

    print(f"📝 CURATED CONTENT ({len(bundle.items)} items):\n")
    for i, item in enumerate(bundle.items, 1):
        print(f"{i}. {item.title}")
        print(f"   Source: {item.source} | Type: {item.content_type} | {item.reading_time}")
        print(f"   {item.summary[:100]}...")
        print(f"   Relevance: {item.relevance_score:.0%} | Quality: {item.quality_score:.0%}")
        print()

    print("🎯 LEARNING OUTCOMES:\n")
    for outcome in bundle.learning_outcomes:
        print(f"  ✓ {outcome}")

    if args.output:
        with open(args.output, "w") as f:
            json.dump(agent.to_dict(bundle), f, indent=2)
        print(f"\n✅ Bundle saved to {args.output}")


if __name__ == "__main__":
    main()
