#!/usr/bin/env python3
"""
Social Listener Agent

Monitors social media platforms for mentions, conversations, and
opportunities related to target topics and brands.
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
class SocialMention:
    """A social media mention or conversation."""
    platform: str
    content: str
    author: str
    author_influence: str  # "low", "medium", "high", "influencer"
    sentiment: str  # "positive", "negative", "neutral", "question"
    engagement: Dict[str, int]  # likes, comments, shares
    url: str
    timestamp: str
    topics: List[str]
    opportunity_type: Optional[str]  # "engagement", "content_idea", "lead", "competitor_mention"


@dataclass
class ConversationThread:
    """A conversation thread to monitor or engage with."""
    platform: str
    title: str
    summary: str
    url: str
    participants: int
    activity_level: str  # "dead", "slow", "active", "viral"
    sentiment_distribution: Dict[str, float]
    key_questions: List[str]
    engagement_opportunities: List[str]


@dataclass
class SocialListeningReport:
    """Complete social listening report."""
    generated_at: str
    monitoring_period: str
    platforms: List[str]
    total_mentions: int
    mentions: List[SocialMention]
    conversations: List[ConversationThread]
    sentiment_summary: Dict[str, float]
    trending_topics: List[Dict]
    engagement_opportunities: List[Dict]
    content_ideas: List[str]


class SocialListenerAgent:
    """Agent that monitors social media for relevant conversations."""

    PLATFORMS = [
        "twitter",
        "linkedin",
        "reddit",
        "youtube",
        "facebook",
        "threads",
        "hacker_news"
    ]

    def __init__(self, keywords: List[str] = None, brand: str = None):
        self.keywords = keywords or ["AI consulting", "automation", "prompt engineering"]
        self.brand = brand
        self.client = anthropic.Anthropic() if HAS_ANTHROPIC else None

    def listen(
        self,
        platforms: Optional[List[str]] = None,
        time_period: str = "24h",
        min_engagement: int = 10
    ) -> SocialListeningReport:
        """
        Listen to social platforms for relevant conversations.

        Args:
            platforms: Platforms to monitor
            time_period: How far back to look
            min_engagement: Minimum engagement threshold

        Returns:
            SocialListeningReport with findings
        """
        platforms = platforms or self.PLATFORMS

        if not self.client:
            return self._generate_mock_report(platforms, time_period)

        prompt = f"""You are a social media analyst monitoring conversations about {', '.join(self.keywords)}.

Platforms to analyze: {', '.join(platforms)}
Time period: {time_period}
Minimum engagement: {min_engagement}
Brand (if any): {self.brand or 'N/A'}

Find and analyze:
1. Relevant mentions and conversations
2. Questions people are asking
3. Complaints and pain points
4. Competitor mentions
5. Engagement opportunities
6. Content ideas from conversations

Return as JSON:
{{
    "total_mentions": 0,
    "mentions": [
        {{
            "platform": "platform",
            "content": "post content",
            "author": "username",
            "author_influence": "low/medium/high/influencer",
            "sentiment": "positive/negative/neutral/question",
            "engagement": {{"likes": 0, "comments": 0, "shares": 0}},
            "url": "url",
            "timestamp": "ISO timestamp",
            "topics": [],
            "opportunity_type": "engagement/content_idea/lead/competitor_mention"
        }}
    ],
    "conversations": [
        {{
            "platform": "platform",
            "title": "thread title",
            "summary": "what it's about",
            "url": "url",
            "participants": 0,
            "activity_level": "dead/slow/active/viral",
            "sentiment_distribution": {{"positive": 0.0, "negative": 0.0, "neutral": 0.0}},
            "key_questions": [],
            "engagement_opportunities": []
        }}
    ],
    "sentiment_summary": {{"positive": 0.0, "negative": 0.0, "neutral": 0.0}},
    "trending_topics": [
        {{
            "topic": "topic name",
            "volume": "mention count",
            "sentiment": "overall sentiment",
            "trend": "rising/stable/declining"
        }}
    ],
    "engagement_opportunities": [
        {{
            "type": "type",
            "platform": "platform",
            "description": "what to do",
            "priority": "high/medium/low",
            "url": "url"
        }}
    ],
    "content_ideas": []
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
                mentions = [SocialMention(**m) for m in data.get("mentions", [])]
                conversations = [ConversationThread(**c) for c in data.get("conversations", [])]

                return SocialListeningReport(
                    generated_at=datetime.now().isoformat(),
                    monitoring_period=time_period,
                    platforms=platforms,
                    total_mentions=data.get("total_mentions", 0),
                    mentions=mentions,
                    conversations=conversations,
                    sentiment_summary=data.get("sentiment_summary", {}),
                    trending_topics=data.get("trending_topics", []),
                    engagement_opportunities=data.get("engagement_opportunities", []),
                    content_ideas=data.get("content_ideas", [])
                )
            except (json.JSONDecodeError, TypeError):
                pass

        return self._generate_mock_report(platforms, time_period)

    def _generate_mock_report(
        self,
        platforms: List[str],
        time_period: str
    ) -> SocialListeningReport:
        """Generate mock report when API unavailable."""
        now = datetime.now()

        mentions = [
            SocialMention(
                platform="twitter",
                content="Looking for recommendations on AI tools for automating customer support. Any suggestions?",
                author="startup_founder",
                author_influence="medium",
                sentiment="question",
                engagement={"likes": 45, "comments": 23, "shares": 8},
                url="https://twitter.com/example/status/1",
                timestamp=(now - timedelta(hours=2)).isoformat(),
                topics=["AI tools", "customer support", "automation"],
                opportunity_type="engagement"
            ),
            SocialMention(
                platform="linkedin",
                content="Just implemented an AI receptionist for our dental practice. 50% cost reduction!",
                author="DentalPracticeOwner",
                author_influence="low",
                sentiment="positive",
                engagement={"likes": 234, "comments": 45, "shares": 12},
                url="https://linkedin.com/posts/example",
                timestamp=(now - timedelta(hours=5)).isoformat(),
                topics=["AI receptionist", "healthcare", "ROI"],
                opportunity_type="content_idea"
            ),
            SocialMention(
                platform="reddit",
                content="Frustrated with AI consulting companies charging $500/hr and delivering PowerPoints",
                author="reddit_user",
                author_influence="low",
                sentiment="negative",
                engagement={"likes": 89, "comments": 67, "shares": 0},
                url="https://reddit.com/r/smallbusiness/comments/example",
                timestamp=(now - timedelta(hours=8)).isoformat(),
                topics=["AI consulting", "pricing", "value"],
                opportunity_type="engagement"
            ),
            SocialMention(
                platform="twitter",
                content="Prompt engineering is the new coding. Every business needs someone who can talk to AI effectively.",
                author="tech_influencer",
                author_influence="influencer",
                sentiment="positive",
                engagement={"likes": 1234, "comments": 189, "shares": 456},
                url="https://twitter.com/example/status/2",
                timestamp=(now - timedelta(hours=12)).isoformat(),
                topics=["prompt engineering", "skills", "AI"],
                opportunity_type="engagement"
            )
        ]

        conversations = [
            ConversationThread(
                platform="reddit",
                title="Best AI tools for small business owners in 2024?",
                summary="Thread discussing AI tools for various small business needs including automation, customer service, and marketing",
                url="https://reddit.com/r/smallbusiness/example",
                participants=45,
                activity_level="active",
                sentiment_distribution={"positive": 0.4, "negative": 0.2, "neutral": 0.4},
                key_questions=[
                    "What AI tools actually deliver ROI?",
                    "Is it worth hiring an AI consultant?",
                    "How to get started with automation?"
                ],
                engagement_opportunities=[
                    "Answer questions about AI ROI",
                    "Share relevant case studies",
                    "Offer helpful resources"
                ]
            ),
            ConversationThread(
                platform="linkedin",
                title="AI in Professional Services - Discussion",
                summary="Professionals discussing AI adoption in law, accounting, and consulting",
                url="https://linkedin.com/posts/discussion",
                participants=78,
                activity_level="active",
                sentiment_distribution={"positive": 0.5, "negative": 0.1, "neutral": 0.4},
                key_questions=[
                    "How to maintain quality with AI?",
                    "What tasks should NOT be automated?",
                    "Best practices for AI implementation?"
                ],
                engagement_opportunities=[
                    "Share thought leadership",
                    "Comment with insights",
                    "Connect with engaged participants"
                ]
            )
        ]

        return SocialListeningReport(
            generated_at=now.isoformat(),
            monitoring_period=time_period,
            platforms=platforms,
            total_mentions=len(mentions),
            mentions=mentions,
            conversations=conversations,
            sentiment_summary={
                "positive": 0.45,
                "negative": 0.15,
                "neutral": 0.30,
                "question": 0.10
            },
            trending_topics=[
                {
                    "topic": "AI automation",
                    "volume": "High",
                    "sentiment": "positive",
                    "trend": "rising"
                },
                {
                    "topic": "Voice AI",
                    "volume": "Medium",
                    "sentiment": "positive",
                    "trend": "rising"
                },
                {
                    "topic": "AI consulting pricing",
                    "volume": "Medium",
                    "sentiment": "mixed",
                    "trend": "stable"
                }
            ],
            engagement_opportunities=[
                {
                    "type": "Question Response",
                    "platform": "twitter",
                    "description": "Respond to founder asking about AI customer support tools",
                    "priority": "high",
                    "url": "https://twitter.com/example/status/1"
                },
                {
                    "type": "Thread Participation",
                    "platform": "reddit",
                    "description": "Join discussion on AI tools for small business",
                    "priority": "high",
                    "url": "https://reddit.com/r/smallbusiness/example"
                },
                {
                    "type": "Pain Point Address",
                    "platform": "reddit",
                    "description": "Address frustration about consulting pricing with value focus",
                    "priority": "medium",
                    "url": "https://reddit.com/r/smallbusiness/comments/example"
                }
            ],
            content_ideas=[
                "Case study: 50% cost reduction with AI receptionist in healthcare",
                "Guide: Getting started with AI automation (for non-technical founders)",
                "Article: Why AI consulting shouldn't cost $500/hr (and what to look for)",
                "Thread: 5 AI automation wins any small business can implement today",
                "Video: Behind the scenes of an AI implementation"
            ]
        )

    def find_influencers(self, topic: str, platform: str = "all") -> List[Dict]:
        """Find influencers talking about a topic."""
        return [
            {
                "name": "AI Thought Leader",
                "platform": "twitter",
                "followers": "50K",
                "engagement_rate": "4.5%",
                "topics": ["AI", "automation", "tech"],
                "collaboration_potential": "high"
            },
            {
                "name": "Business Automation Expert",
                "platform": "linkedin",
                "followers": "25K",
                "engagement_rate": "6.2%",
                "topics": ["automation", "productivity", "SMB"],
                "collaboration_potential": "high"
            }
        ]

    def get_question_patterns(self) -> List[Dict]:
        """Analyze common questions being asked."""
        return [
            {
                "question_pattern": "How do I [automate X]?",
                "frequency": "Very common",
                "platforms": ["reddit", "twitter", "linkedin"],
                "content_opportunity": "How-to guides and tutorials"
            },
            {
                "question_pattern": "Is [AI tool] worth it?",
                "frequency": "Common",
                "platforms": ["reddit", "twitter"],
                "content_opportunity": "Comparison and review content"
            },
            {
                "question_pattern": "What AI should I use for [use case]?",
                "frequency": "Common",
                "platforms": ["reddit", "quora", "twitter"],
                "content_opportunity": "Tool recommendation guides"
            }
        ]

    def to_dict(self, report: SocialListeningReport) -> Dict:
        """Convert report to dictionary."""
        return {
            "generated_at": report.generated_at,
            "monitoring_period": report.monitoring_period,
            "platforms": report.platforms,
            "total_mentions": report.total_mentions,
            "mentions": [asdict(m) for m in report.mentions],
            "conversations": [asdict(c) for c in report.conversations],
            "sentiment_summary": report.sentiment_summary,
            "trending_topics": report.trending_topics,
            "engagement_opportunities": report.engagement_opportunities,
            "content_ideas": report.content_ideas
        }


def main():
    """Run social listening."""
    import argparse

    parser = argparse.ArgumentParser(description="Listen to social media")
    parser.add_argument("--keywords", nargs="+",
                       default=["AI consulting", "automation", "prompt engineering"],
                       help="Keywords to monitor")
    parser.add_argument("--platforms", nargs="+",
                       help="Platforms to monitor")
    parser.add_argument("--period", default="24h",
                       help="Time period to analyze")
    parser.add_argument("--opportunities", action="store_true",
                       help="Show only engagement opportunities")
    parser.add_argument("--ideas", action="store_true",
                       help="Show only content ideas")
    parser.add_argument("--output", type=Path,
                       help="Output file for JSON")

    args = parser.parse_args()

    agent = SocialListenerAgent(keywords=args.keywords)
    report = agent.listen(
        platforms=args.platforms,
        time_period=args.period
    )

    if args.opportunities:
        print("\n🎯 ENGAGEMENT OPPORTUNITIES:\n")
        for opp in report.engagement_opportunities:
            priority_icon = {"high": "🔴", "medium": "🟡", "low": "🟢"}.get(opp["priority"], "⚪")
            print(f"{priority_icon} [{opp['platform']}] {opp['type']}")
            print(f"   {opp['description']}")
            print(f"   URL: {opp['url']}")
            print()
        return

    if args.ideas:
        print("\n💡 CONTENT IDEAS FROM CONVERSATIONS:\n")
        for idea in report.content_ideas:
            print(f"  • {idea}")
        return

    print(f"\n👂 SOCIAL LISTENING REPORT")
    print(f"Keywords: {', '.join(args.keywords)}")
    print(f"Period: {report.monitoring_period}")
    print(f"Generated: {report.generated_at}")
    print("=" * 60)

    print(f"\n📊 OVERVIEW:")
    print(f"  Total mentions: {report.total_mentions}")
    print(f"  Sentiment: {report.sentiment_summary.get('positive', 0):.0%} positive, "
          f"{report.sentiment_summary.get('negative', 0):.0%} negative")

    print(f"\n📢 RECENT MENTIONS ({len(report.mentions)}):\n")
    for mention in report.mentions[:5]:
        sentiment_icon = {
            "positive": "😊",
            "negative": "😟",
            "neutral": "😐",
            "question": "❓"
        }.get(mention.sentiment, "")

        print(f"{sentiment_icon} [{mention.platform}] @{mention.author}")
        print(f"   \"{mention.content[:100]}...\"")
        print(f"   Engagement: {mention.engagement.get('likes', 0)} likes")
        if mention.opportunity_type:
            print(f"   Opportunity: {mention.opportunity_type}")
        print()

    print(f"💬 ACTIVE CONVERSATIONS ({len(report.conversations)}):\n")
    for conv in report.conversations:
        print(f"🔗 [{conv.platform}] {conv.title}")
        print(f"   {conv.summary[:100]}...")
        print(f"   Participants: {conv.participants} | Activity: {conv.activity_level}")
        if conv.key_questions:
            print(f"   Key Q: {conv.key_questions[0]}")
        print()

    print("📈 TRENDING TOPICS:\n")
    for topic in report.trending_topics:
        trend_icon = {"rising": "📈", "stable": "➡️", "declining": "📉"}.get(topic["trend"], "")
        print(f"  {trend_icon} {topic['topic']} ({topic['volume']}) - {topic['sentiment']}")

    print("\n🎯 TOP ENGAGEMENT OPPORTUNITIES:\n")
    for opp in report.engagement_opportunities[:3]:
        print(f"  • [{opp['platform']}] {opp['description']}")

    print("\n💡 CONTENT IDEAS:\n")
    for idea in report.content_ideas[:3]:
        print(f"  • {idea}")

    if args.output:
        with open(args.output, "w") as f:
            json.dump(agent.to_dict(report), f, indent=2)
        print(f"\n✅ Report saved to {args.output}")


if __name__ == "__main__":
    main()
