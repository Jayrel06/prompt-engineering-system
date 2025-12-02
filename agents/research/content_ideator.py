#!/usr/bin/env python3
"""
Content Ideator Agent

Generates content ideas based on trends, audience insights, and
strategic goals. Creates content calendars and idea backlogs.
"""

import os
import json
import re
from datetime import datetime, timedelta
from typing import List, Dict, Optional
from dataclasses import dataclass, asdict
from pathlib import Path
import random

try:
    import anthropic
    HAS_ANTHROPIC = True
except ImportError:
    HAS_ANTHROPIC = False


@dataclass
class ContentIdea:
    """A content idea."""
    title: str
    format: str  # "blog", "video", "linkedin", "twitter", "email", "guide"
    topic: str
    hook: str
    outline: List[str]
    target_audience: str
    goal: str  # "awareness", "consideration", "conversion"
    estimated_effort: str  # "low", "medium", "high"
    priority_score: float
    keywords: List[str]
    similar_successful_content: List[str]


@dataclass
class ContentCalendar:
    """A content calendar."""
    start_date: str
    end_date: str
    theme: str
    items: List[Dict]
    notes: str


@dataclass
class IdeationSession:
    """Results of an ideation session."""
    generated_at: str
    focus_topic: str
    ideas: List[ContentIdea]
    calendar: Optional[ContentCalendar]
    quick_wins: List[str]
    evergreen_ideas: List[str]


class ContentIdeatorAgent:
    """Agent that generates content ideas and calendars."""

    CONTENT_FORMATS = [
        "blog_post",
        "linkedin_post",
        "twitter_thread",
        "youtube_video",
        "short_video",
        "email_newsletter",
        "guide_ebook",
        "case_study",
        "infographic",
        "podcast_episode",
        "webinar"
    ]

    CONTENT_PILLARS = [
        "educational",
        "thought_leadership",
        "case_studies",
        "behind_the_scenes",
        "industry_news",
        "tools_and_tips"
    ]

    def __init__(self, brand_voice: str = "professional and approachable"):
        self.brand_voice = brand_voice
        self.client = anthropic.Anthropic() if HAS_ANTHROPIC else None

    def generate_ideas(
        self,
        topic: str,
        count: int = 10,
        formats: Optional[List[str]] = None,
        audience: str = "business decision makers"
    ) -> IdeationSession:
        """
        Generate content ideas around a topic.

        Args:
            topic: Focus topic for ideas
            count: Number of ideas to generate
            formats: Content formats to include
            audience: Target audience

        Returns:
            IdeationSession with ideas and calendar
        """
        formats = formats or self.CONTENT_FORMATS[:5]

        if not self.client:
            return self._generate_mock_session(topic, count, formats, audience)

        prompt = f"""You are a content strategist generating ideas for a {self.brand_voice} brand.

Generate {count} content ideas about: "{topic}"

Target audience: {audience}
Formats to include: {', '.join(formats)}

For each idea, provide:
1. Compelling title
2. Format
3. Topic/theme
4. Hook (first line or angle)
5. Outline (3-5 points)
6. Target audience segment
7. Funnel goal (awareness/consideration/conversion)
8. Effort estimate
9. Priority score (0-1 based on potential impact)
10. SEO keywords
11. Similar successful content examples

Also provide:
- 3 quick wins (can be created in <1 hour)
- 3 evergreen ideas (relevant year-round)
- A 4-week content calendar

Return as JSON:
{{
    "ideas": [
        {{
            "title": "string",
            "format": "string",
            "topic": "string",
            "hook": "string",
            "outline": [],
            "target_audience": "string",
            "goal": "awareness/consideration/conversion",
            "estimated_effort": "low/medium/high",
            "priority_score": 0.0,
            "keywords": [],
            "similar_successful_content": []
        }}
    ],
    "calendar": {{
        "start_date": "YYYY-MM-DD",
        "end_date": "YYYY-MM-DD",
        "theme": "Monthly theme",
        "items": [
            {{
                "week": 1,
                "day": "Monday",
                "content": "title",
                "format": "format",
                "platform": "platform"
            }}
        ],
        "notes": "Calendar notes"
    }},
    "quick_wins": [],
    "evergreen_ideas": []
}}
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
                ideas = [ContentIdea(**idea) for idea in data.get("ideas", [])]

                calendar_data = data.get("calendar")
                calendar = ContentCalendar(**calendar_data) if calendar_data else None

                return IdeationSession(
                    generated_at=datetime.now().isoformat(),
                    focus_topic=topic,
                    ideas=ideas,
                    calendar=calendar,
                    quick_wins=data.get("quick_wins", []),
                    evergreen_ideas=data.get("evergreen_ideas", [])
                )
            except (json.JSONDecodeError, TypeError):
                pass

        return self._generate_mock_session(topic, count, formats, audience)

    def _generate_mock_session(
        self,
        topic: str,
        count: int,
        formats: List[str],
        audience: str
    ) -> IdeationSession:
        """Generate mock ideation session when API unavailable."""
        today = datetime.now()

        ideas = [
            ContentIdea(
                title="5 AI Automation Mistakes That Cost Businesses Thousands",
                format="blog_post",
                topic="AI automation",
                hook="Most businesses get AI automation wrong. Here's what they miss.",
                outline=[
                    "Introduction: The hidden costs of bad automation",
                    "Mistake 1: Automating the wrong processes",
                    "Mistake 2: Ignoring the human element",
                    "Mistake 3: Not measuring ROI properly",
                    "Mistake 4: Over-engineering simple solutions",
                    "Mistake 5: Skipping the testing phase",
                    "Conclusion: How to avoid these mistakes"
                ],
                target_audience="SMB owners considering AI",
                goal="awareness",
                estimated_effort="medium",
                priority_score=0.9,
                keywords=["AI automation", "business mistakes", "automation ROI"],
                similar_successful_content=[
                    "Common marketing mistakes blog (50K views)",
                    "Automation fails Twitter thread (10K likes)"
                ]
            ),
            ContentIdea(
                title="AI Automation ROI Calculator: Is It Worth It for Your Business?",
                format="guide_ebook",
                topic="AI ROI",
                hook="Before you invest in AI, run the numbers. This calculator shows you exactly what to expect.",
                outline=[
                    "Why ROI matters for AI investments",
                    "The ROI calculation framework",
                    "Interactive calculator section",
                    "Case study examples",
                    "Next steps based on your results"
                ],
                target_audience="CFOs and business owners",
                goal="consideration",
                estimated_effort="high",
                priority_score=0.95,
                keywords=["AI ROI", "automation calculator", "AI investment"],
                similar_successful_content=[
                    "HubSpot ROI calculators (lead magnets)",
                    "Marketing budget calculators"
                ]
            ),
            ContentIdea(
                title="We Automated Our Client's Reception: Here's What Happened",
                format="linkedin_post",
                topic="Voice AI case study",
                hook="Last month we implemented an AI receptionist for a dental practice. The results surprised even us.",
                outline=[
                    "The challenge they faced",
                    "What we implemented",
                    "Results after 30 days",
                    "What they'd do differently",
                    "CTA: Want similar results?"
                ],
                target_audience="Healthcare practice owners",
                goal="consideration",
                estimated_effort="low",
                priority_score=0.85,
                keywords=["AI receptionist", "voice AI", "healthcare AI"],
                similar_successful_content=[
                    "SaaS implementation stories on LinkedIn",
                    "Before/after case studies"
                ]
            ),
            ContentIdea(
                title="How to Write Prompts That Actually Work (Thread)",
                format="twitter_thread",
                topic="Prompt engineering",
                hook="After writing 1000+ prompts for clients, here are the patterns that actually work:",
                outline=[
                    "Tweet 1: Hook + credentials",
                    "Tweet 2-5: Core techniques",
                    "Tweet 6-8: Examples",
                    "Tweet 9: Common mistakes",
                    "Tweet 10: CTA"
                ],
                target_audience="AI enthusiasts and builders",
                goal="awareness",
                estimated_effort="low",
                priority_score=0.8,
                keywords=["prompt engineering", "AI prompts", "ChatGPT"],
                similar_successful_content=[
                    "Prompt engineering threads (viral)",
                    "AI tips threads"
                ]
            ),
            ContentIdea(
                title="The Small Business Guide to AI in 2024",
                format="guide_ebook",
                topic="AI for SMBs",
                hook="AI isn't just for big companies anymore. Here's exactly how small businesses are using it.",
                outline=[
                    "Introduction: AI is now accessible",
                    "Chapter 1: AI tools you can start using today",
                    "Chapter 2: Where AI delivers the best ROI",
                    "Chapter 3: Implementation roadmap",
                    "Chapter 4: Common pitfalls and how to avoid them",
                    "Chapter 5: Future-proofing your AI strategy",
                    "Conclusion + resources"
                ],
                target_audience="Small business owners",
                goal="consideration",
                estimated_effort="high",
                priority_score=0.88,
                keywords=["small business AI", "AI guide", "SMB automation"],
                similar_successful_content=[
                    "State of AI reports",
                    "Ultimate guides in marketing"
                ]
            )
        ]

        # Create calendar
        calendar = ContentCalendar(
            start_date=today.strftime("%Y-%m-%d"),
            end_date=(today + timedelta(days=28)).strftime("%Y-%m-%d"),
            theme=f"AI Automation for {audience}",
            items=[
                {"week": 1, "day": "Monday", "content": ideas[3].title, "format": "twitter_thread", "platform": "Twitter"},
                {"week": 1, "day": "Wednesday", "content": ideas[2].title, "format": "linkedin_post", "platform": "LinkedIn"},
                {"week": 1, "day": "Friday", "content": "Quick tip video", "format": "short_video", "platform": "LinkedIn/Twitter"},
                {"week": 2, "day": "Monday", "content": ideas[0].title, "format": "blog_post", "platform": "Blog"},
                {"week": 2, "day": "Wednesday", "content": "Blog summary", "format": "linkedin_post", "platform": "LinkedIn"},
                {"week": 2, "day": "Friday", "content": "AI tool review", "format": "twitter_thread", "platform": "Twitter"},
                {"week": 3, "day": "Monday", "content": "Case study teaser", "format": "linkedin_post", "platform": "LinkedIn"},
                {"week": 3, "day": "Wednesday", "content": "Full case study", "format": "blog_post", "platform": "Blog"},
                {"week": 3, "day": "Friday", "content": "Behind the scenes", "format": "short_video", "platform": "All"},
                {"week": 4, "day": "Monday", "content": ideas[1].title, "format": "guide_ebook", "platform": "Website"},
                {"week": 4, "day": "Wednesday", "content": "Guide promo", "format": "linkedin_post", "platform": "LinkedIn"},
                {"week": 4, "day": "Friday", "content": "Monthly wrap-up", "format": "email_newsletter", "platform": "Email"}
            ],
            notes="Focus on mixing educational content with social proof. Repurpose blog content across platforms."
        )

        return IdeationSession(
            generated_at=datetime.now().isoformat(),
            focus_topic=topic,
            ideas=ideas,
            calendar=calendar,
            quick_wins=[
                "Twitter thread on prompt engineering tips",
                "LinkedIn post: Quick case study summary",
                "Short video: One AI tool you should try"
            ],
            evergreen_ideas=[
                "The Complete Guide to AI for Small Business",
                "AI ROI Calculator (interactive tool)",
                "AI Implementation Checklist"
            ]
        )

    def remix_idea(
        self,
        original_idea: ContentIdea,
        new_formats: List[str]
    ) -> List[ContentIdea]:
        """
        Remix an idea into different formats.

        Args:
            original_idea: Original content idea
            new_formats: Formats to remix into

        Returns:
            List of remixed content ideas
        """
        remixed = []

        for fmt in new_formats:
            if fmt == original_idea.format:
                continue

            remixed.append(ContentIdea(
                title=f"{original_idea.title} ({fmt.replace('_', ' ').title()})",
                format=fmt,
                topic=original_idea.topic,
                hook=original_idea.hook,
                outline=original_idea.outline[:3],  # Shortened for other formats
                target_audience=original_idea.target_audience,
                goal=original_idea.goal,
                estimated_effort="low" if fmt in ["twitter_thread", "linkedin_post"] else "medium",
                priority_score=original_idea.priority_score * 0.8,
                keywords=original_idea.keywords,
                similar_successful_content=[]
            ))

        return remixed

    def prioritize_ideas(
        self,
        ideas: List[ContentIdea],
        criteria: Dict[str, float]
    ) -> List[ContentIdea]:
        """
        Prioritize ideas based on custom criteria.

        Args:
            ideas: List of content ideas
            criteria: Weighting for different factors

        Returns:
            Sorted list of ideas
        """
        def score(idea: ContentIdea) -> float:
            base = idea.priority_score
            effort_multiplier = {"low": 1.2, "medium": 1.0, "high": 0.8}.get(idea.estimated_effort, 1.0)
            goal_weight = criteria.get(idea.goal, 1.0)
            return base * effort_multiplier * goal_weight

        return sorted(ideas, key=score, reverse=True)

    def to_dict(self, session: IdeationSession) -> Dict:
        """Convert session to dictionary."""
        return {
            "generated_at": session.generated_at,
            "focus_topic": session.focus_topic,
            "ideas": [asdict(idea) for idea in session.ideas],
            "calendar": asdict(session.calendar) if session.calendar else None,
            "quick_wins": session.quick_wins,
            "evergreen_ideas": session.evergreen_ideas
        }


def main():
    """Run content ideation."""
    import argparse

    parser = argparse.ArgumentParser(description="Generate content ideas")
    parser.add_argument("topic", nargs="?", default="AI automation for business",
                       help="Topic for ideation")
    parser.add_argument("--count", type=int, default=5,
                       help="Number of ideas to generate")
    parser.add_argument("--formats", nargs="+",
                       help="Content formats to include")
    parser.add_argument("--audience", default="small business owners",
                       help="Target audience")
    parser.add_argument("--calendar", action="store_true",
                       help="Show content calendar")
    parser.add_argument("--quick-wins", action="store_true",
                       help="Show only quick wins")
    parser.add_argument("--output", type=Path,
                       help="Output file for JSON")

    args = parser.parse_args()

    agent = ContentIdeatorAgent()
    session = agent.generate_ideas(
        topic=args.topic,
        count=args.count,
        formats=args.formats,
        audience=args.audience
    )

    if args.quick_wins:
        print("\n⚡ QUICK WINS (< 1 hour to create):\n")
        for win in session.quick_wins:
            print(f"  • {win}")
        return

    if args.calendar and session.calendar:
        print(f"\n📅 CONTENT CALENDAR: {session.calendar.theme}")
        print(f"Period: {session.calendar.start_date} to {session.calendar.end_date}")
        print("=" * 60)

        current_week = 0
        for item in session.calendar.items:
            if item["week"] != current_week:
                current_week = item["week"]
                print(f"\n📅 WEEK {current_week}")

            print(f"  {item['day']}: {item['content']}")
            print(f"    Format: {item['format']} | Platform: {item['platform']}")

        print(f"\n📝 Notes: {session.calendar.notes}")
        return

    print(f"\n💡 CONTENT IDEATION: {session.focus_topic}")
    print(f"Generated: {session.generated_at}")
    print("=" * 60)

    print(f"\n📝 IDEAS ({len(session.ideas)}):\n")
    for i, idea in enumerate(session.ideas, 1):
        effort_icon = {"low": "🟢", "medium": "🟡", "high": "🔴"}.get(idea.estimated_effort, "⚪")
        goal_icon = {"awareness": "👀", "consideration": "🤔", "conversion": "💰"}.get(idea.goal, "")

        print(f"{i}. {idea.title}")
        print(f"   Format: {idea.format} | {effort_icon} Effort | {goal_icon} {idea.goal}")
        print(f"   Priority: {idea.priority_score:.0%}")
        print(f"   Hook: {idea.hook[:80]}...")
        print(f"   Keywords: {', '.join(idea.keywords[:3])}")
        print()

    print("⚡ QUICK WINS:\n")
    for win in session.quick_wins:
        print(f"  • {win}")

    print("\n🌲 EVERGREEN IDEAS:\n")
    for idea in session.evergreen_ideas:
        print(f"  • {idea}")

    if args.output:
        with open(args.output, "w") as f:
            json.dump(agent.to_dict(session), f, indent=2)
        print(f"\n✅ Session saved to {args.output}")


if __name__ == "__main__":
    main()
