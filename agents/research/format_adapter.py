#!/usr/bin/env python3
"""
Format Adapter Agent

Adapts and reformats content for different platforms, audiences,
and use cases. Handles content repurposing and optimization.
"""

import os
import json
import re
from datetime import datetime
from typing import List, Dict, Optional
from dataclasses import dataclass, asdict
from pathlib import Path

try:
    import anthropic
    HAS_ANTHROPIC = True
except ImportError:
    HAS_ANTHROPIC = False


@dataclass
class ContentFormat:
    """A content format specification."""
    platform: str
    format_type: str
    max_length: int
    character_count: Optional[int]
    constraints: List[str]
    best_practices: List[str]
    example_structure: str


@dataclass
class AdaptedContent:
    """Content adapted for a specific format."""
    original_type: str
    target_format: str
    platform: str
    content: str
    hashtags: List[str]
    cta: str
    media_suggestions: List[str]
    posting_tips: List[str]


@dataclass
class ContentRepurposeBundle:
    """Bundle of repurposed content from single source."""
    source_content: str
    source_type: str
    adaptations: List[AdaptedContent]
    content_calendar: List[Dict]
    efficiency_score: float


class FormatAdapterAgent:
    """Agent that adapts content for different formats and platforms."""

    PLATFORM_SPECS = {
        "twitter": ContentFormat(
            platform="twitter",
            format_type="short_form",
            max_length=280,
            character_count=280,
            constraints=["280 character limit", "No markdown in main tweet", "Images boost engagement"],
            best_practices=[
                "Hook in first line",
                "Use line breaks for readability",
                "End with CTA or question",
                "2-3 hashtags max"
            ],
            example_structure="Hook → Value → CTA"
        ),
        "twitter_thread": ContentFormat(
            platform="twitter",
            format_type="thread",
            max_length=2500,
            character_count=280,
            constraints=["280 per tweet", "Number tweets", "First tweet is crucial"],
            best_practices=[
                "Hook in tweet 1",
                "One idea per tweet",
                "Use visuals",
                "End with recap and CTA"
            ],
            example_structure="1/ Hook\n2-N/ Points\nLast/ Recap + CTA"
        ),
        "linkedin": ContentFormat(
            platform="linkedin",
            format_type="long_form",
            max_length=3000,
            character_count=3000,
            constraints=["3000 character limit", "First 2 lines visible", "Algorithm favors native content"],
            best_practices=[
                "Strong hook in first 2 lines",
                "Use line breaks liberally",
                "Personal stories perform well",
                "End with question for engagement"
            ],
            example_structure="Hook → Story/Context → Value points → Takeaway → CTA/Question"
        ),
        "email": ContentFormat(
            platform="email",
            format_type="newsletter",
            max_length=1500,
            character_count=None,
            constraints=["Mobile-friendly", "Scannable", "Clear CTA"],
            best_practices=[
                "Compelling subject line",
                "Personal tone",
                "One main CTA",
                "Easy to skim"
            ],
            example_structure="Subject → Hook → Main content → CTA → PS"
        ),
        "blog": ContentFormat(
            platform="blog",
            format_type="article",
            max_length=5000,
            character_count=None,
            constraints=["SEO optimized", "Scannable headers", "Internal links"],
            best_practices=[
                "Compelling title",
                "Hook in first paragraph",
                "Headers every 200-300 words",
                "Conclusion with CTA"
            ],
            example_structure="Title → Hook → Sections with H2/H3 → Conclusion → CTA"
        ),
        "youtube_short": ContentFormat(
            platform="youtube",
            format_type="short_video",
            max_length=60,
            character_count=None,
            constraints=["Under 60 seconds", "Vertical format", "Hook in first 3 seconds"],
            best_practices=[
                "Immediate hook",
                "Fast pacing",
                "Text overlays",
                "Clear takeaway"
            ],
            example_structure="Hook (3s) → Value (45s) → CTA (10s)"
        )
    }

    def __init__(self):
        self.client = anthropic.Anthropic() if HAS_ANTHROPIC else None

    def adapt_content(
        self,
        content: str,
        source_format: str,
        target_formats: List[str],
        tone: str = "professional"
    ) -> ContentRepurposeBundle:
        """
        Adapt content to multiple formats.

        Args:
            content: Original content
            source_format: Source format type
            target_formats: Target formats to adapt to
            tone: Desired tone

        Returns:
            ContentRepurposeBundle with all adaptations
        """
        if not self.client:
            return self._generate_mock_bundle(content, source_format, target_formats)

        adaptations_prompt = ""
        for fmt in target_formats:
            spec = self.PLATFORM_SPECS.get(fmt)
            if spec:
                adaptations_prompt += f"""

For {fmt}:
- Max length: {spec.max_length}
- Constraints: {', '.join(spec.constraints)}
- Best practices: {', '.join(spec.best_practices)}
- Structure: {spec.example_structure}
"""

        prompt = f"""You are a content adaptation specialist.

Adapt this content for multiple platforms:

ORIGINAL CONTENT ({source_format}):
{content[:2000]}

TONE: {tone}

TARGET FORMATS AND SPECS:
{adaptations_prompt}

For each format, provide:
1. Adapted content
2. Relevant hashtags
3. CTA
4. Media suggestions
5. Posting tips

Also create a 1-week content calendar for releasing these adaptations.

Return as JSON:
{{
    "adaptations": [
        {{
            "original_type": "{source_format}",
            "target_format": "format",
            "platform": "platform",
            "content": "adapted content",
            "hashtags": [],
            "cta": "call to action",
            "media_suggestions": [],
            "posting_tips": []
        }}
    ],
    "content_calendar": [
        {{
            "day": 1,
            "platform": "platform",
            "content_type": "type",
            "best_time": "time"
        }}
    ],
    "efficiency_score": 0.0
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
                adaptations = [AdaptedContent(**a) for a in data.get("adaptations", [])]

                return ContentRepurposeBundle(
                    source_content=content,
                    source_type=source_format,
                    adaptations=adaptations,
                    content_calendar=data.get("content_calendar", []),
                    efficiency_score=data.get("efficiency_score", 0.8)
                )
            except (json.JSONDecodeError, TypeError):
                pass

        return self._generate_mock_bundle(content, source_format, target_formats)

    def _generate_mock_bundle(
        self,
        content: str,
        source_format: str,
        target_formats: List[str]
    ) -> ContentRepurposeBundle:
        """Generate mock bundle when API unavailable."""

        # Extract key points from content
        first_line = content.split('\n')[0][:100]

        adaptations = []

        if "twitter" in target_formats or "twitter_thread" in target_formats:
            adaptations.append(AdaptedContent(
                original_type=source_format,
                target_format="twitter_thread",
                platform="twitter",
                content=f"""🧵 {first_line}

Here's what you need to know:

1/ [First key point from content]

2/ [Second key point]

3/ [Third key point]

4/ [Fourth key point]

5/ Key takeaway:
[Main lesson]

Like this thread? Follow for more insights on AI and automation.

♻️ RT to help others discover this.""",
                hashtags=["#AI", "#Automation", "#Tech"],
                cta="Follow for more + RT to share",
                media_suggestions=["Infographic of key points", "Screenshot of results"],
                posting_tips=[
                    "Post between 8-10am or 7-9pm",
                    "Engage with replies in first hour",
                    "Quote tweet with additional insight"
                ]
            ))

        if "linkedin" in target_formats:
            adaptations.append(AdaptedContent(
                original_type=source_format,
                target_format="linkedin",
                platform="linkedin",
                content=f"""{first_line}

Here's the thing most people miss:

[Expanded insight from content]

The key lessons:

→ Point 1
→ Point 2
→ Point 3
→ Point 4

What's worked for you?

Drop your experience in the comments 👇""",
                hashtags=["#AI", "#Innovation", "#BusinessStrategy"],
                cta="Comment with your experience",
                media_suggestions=["Carousel of key points", "Before/after visual"],
                posting_tips=[
                    "Post Tuesday-Thursday morning",
                    "Reply to every comment",
                    "Edit post to add insights from comments"
                ]
            ))

        if "email" in target_formats:
            adaptations.append(AdaptedContent(
                original_type=source_format,
                target_format="email",
                platform="email",
                content=f"""Subject: {first_line}

Hi [Name],

Quick insight I wanted to share:

{first_line}

Here's what matters:

1. [Key point 1]

2. [Key point 2]

3. [Key point 3]

The bottom line: [Main takeaway]

[CTA Button: Learn More]

Talk soon,
[Your name]

P.S. If you found this useful, forward it to someone who needs to hear it.""",
                hashtags=[],
                cta="Learn More button + P.S. forward request",
                media_suggestions=["Header image", "Inline stats graphic"],
                posting_tips=[
                    "Send Tuesday or Thursday morning",
                    "A/B test subject lines",
                    "Include preview text"
                ]
            ))

        if "youtube_short" in target_formats:
            adaptations.append(AdaptedContent(
                original_type=source_format,
                target_format="youtube_short",
                platform="youtube",
                content=f"""[0-3s] HOOK: "{first_line[:50]}..."

[3-10s] CONTEXT:
"Here's why this matters..."

[10-45s] VALUE:
"Point 1..."
"Point 2..."
"Point 3..."

[45-55s] TAKEAWAY:
"The key lesson..."

[55-60s] CTA:
"Follow for more tips like this"

TEXT OVERLAYS:
- Hook text at start
- Key points as they're said
- CTA text at end""",
                hashtags=["#shorts", "#ai", "#tech", "#learnontiktok"],
                cta="Follow for more",
                media_suggestions=["B-roll of relevant visuals", "Screen recordings", "Text animations"],
                posting_tips=[
                    "Post between 12-3pm or 7-9pm",
                    "Use trending sounds if relevant",
                    "Pin a comment with more info"
                ]
            ))

        return ContentRepurposeBundle(
            source_content=content,
            source_type=source_format,
            adaptations=adaptations,
            content_calendar=[
                {"day": 1, "platform": "twitter", "content_type": "thread", "best_time": "9am"},
                {"day": 2, "platform": "linkedin", "content_type": "post", "best_time": "8am"},
                {"day": 3, "platform": "email", "content_type": "newsletter", "best_time": "10am"},
                {"day": 4, "platform": "youtube", "content_type": "short", "best_time": "2pm"},
                {"day": 5, "platform": "twitter", "content_type": "single tweet", "best_time": "12pm"},
            ],
            efficiency_score=0.85
        )

    def get_format_specs(self, platform: str) -> Optional[ContentFormat]:
        """Get format specifications for a platform."""
        return self.PLATFORM_SPECS.get(platform)

    def optimize_for_platform(
        self,
        content: str,
        platform: str
    ) -> Dict:
        """Optimize content specifically for one platform."""
        spec = self.PLATFORM_SPECS.get(platform)
        if not spec:
            return {"error": f"Unknown platform: {platform}"}

        return {
            "platform": platform,
            "original_length": len(content),
            "max_length": spec.max_length,
            "needs_trimming": len(content) > spec.max_length,
            "constraints": spec.constraints,
            "suggestions": spec.best_practices
        }

    def to_dict(self, bundle: ContentRepurposeBundle) -> Dict:
        """Convert bundle to dictionary."""
        return {
            "source_content": bundle.source_content[:500] + "..." if len(bundle.source_content) > 500 else bundle.source_content,
            "source_type": bundle.source_type,
            "adaptations": [asdict(a) for a in bundle.adaptations],
            "content_calendar": bundle.content_calendar,
            "efficiency_score": bundle.efficiency_score
        }


def main():
    """Run format adapter."""
    import argparse

    parser = argparse.ArgumentParser(description="Adapt content for different formats")
    parser.add_argument("--source", default="blog",
                       help="Source content format")
    parser.add_argument("--targets", nargs="+",
                       default=["twitter_thread", "linkedin", "email"],
                       help="Target formats")
    parser.add_argument("--content", type=Path,
                       help="File containing source content")
    parser.add_argument("--specs", action="store_true",
                       help="Show platform specifications")
    parser.add_argument("--output", type=Path,
                       help="Output file for JSON")

    args = parser.parse_args()

    agent = FormatAdapterAgent()

    if args.specs:
        print("\n📋 PLATFORM SPECIFICATIONS:\n")
        for platform, spec in agent.PLATFORM_SPECS.items():
            print(f"📱 {platform.upper()}")
            print(f"   Type: {spec.format_type}")
            print(f"   Max length: {spec.max_length}")
            print(f"   Best practices:")
            for bp in spec.best_practices:
                print(f"     • {bp}")
            print()
        return

    # Sample content if no file provided
    sample_content = """
# 5 Ways AI is Transforming Small Business Operations

Small businesses are discovering that AI isn't just for big corporations anymore.
Here are the top 5 ways AI is making a real difference:

1. Customer Service Automation
AI chatbots handle 80% of routine inquiries, freeing staff for complex issues.

2. Smart Scheduling
AI-powered scheduling reduces no-shows by 40% through intelligent reminders.

3. Inventory Management
Predictive AI helps businesses reduce inventory costs by 25%.

4. Marketing Optimization
AI analyzes customer data to personalize marketing, improving conversion by 30%.

5. Administrative Tasks
AI automates invoicing, data entry, and reporting, saving 10+ hours weekly.

The key takeaway: Start small, measure results, and scale what works.
"""

    if args.content and args.content.exists():
        sample_content = args.content.read_text()

    bundle = agent.adapt_content(
        content=sample_content,
        source_format=args.source,
        target_formats=args.targets
    )

    print(f"\n🔄 CONTENT ADAPTATION REPORT")
    print(f"Source: {bundle.source_type}")
    print(f"Efficiency: {bundle.efficiency_score:.0%}")
    print("=" * 60)

    print(f"\n📝 ADAPTATIONS ({len(bundle.adaptations)}):\n")
    for adaptation in bundle.adaptations:
        print(f"{'='*60}")
        print(f"📱 {adaptation.platform.upper()} - {adaptation.target_format}")
        print("="*60)
        print(f"\n{adaptation.content[:500]}...")
        print(f"\n🏷️ Hashtags: {' '.join(adaptation.hashtags)}")
        print(f"📣 CTA: {adaptation.cta}")
        print(f"\n🖼️ Media: {', '.join(adaptation.media_suggestions[:2])}")
        print(f"\n💡 Tips:")
        for tip in adaptation.posting_tips[:2]:
            print(f"   • {tip}")
        print()

    print("\n📅 CONTENT CALENDAR:\n")
    for item in bundle.content_calendar:
        print(f"  Day {item['day']}: {item['platform']} {item['content_type']} @ {item['best_time']}")

    if args.output:
        with open(args.output, "w") as f:
            json.dump(agent.to_dict(bundle), f, indent=2)
        print(f"\n✅ Bundle saved to {args.output}")


if __name__ == "__main__":
    main()
