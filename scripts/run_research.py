#!/usr/bin/env python3
"""
Research System CLI

Command-line interface for running the multi-agent research system.
"""

import sys
import os
import json
import argparse
from pathlib import Path
from datetime import datetime

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from agents.research.orchestrator import ResearchOrchestrator
from agents.research.trend_scout import TrendScoutAgent
from agents.research.keyword_researcher import KeywordResearcherAgent
from agents.research.content_ideator import ContentIdeatorAgent
from agents.research.audience_analyst import AudienceAnalystAgent
from agents.research.social_listener import SocialListenerAgent
from agents.research.competitor_monitor import CompetitorMonitorAgent
from agents.research.expert_finder import ExpertFinderAgent
from agents.research.format_adapter import FormatAdapterAgent
from agents.research.case_study_builder import CaseStudyBuilderAgent, ProjectData
from agents.research.data_miner import DataMinerAgent
from agents.research.content_curator import ContentCuratorAgent
from agents.research.tech_stack_hunter import TechStackHunterAgent


def cmd_research(args):
    """Run comprehensive research on a topic."""
    orchestrator = ResearchOrchestrator(industry=args.industry)

    print(f"\n🔬 Running {args.mode} research on: {args.topic}")
    print("=" * 60)

    if args.mode == "full":
        report = orchestrator.full_research(
            args.topic,
            include_agents=args.agents,
            parallel=not args.sequential
        )
    elif args.mode == "quick":
        result = orchestrator.quick_research(args.topic)
        print(json.dumps(result, indent=2, default=str))
        return
    elif args.mode == "content":
        result = orchestrator.content_research(args.topic)
        print(json.dumps(result, indent=2, default=str))
        return
    elif args.mode == "competitive":
        result = orchestrator.competitive_research(args.topic)
        print(json.dumps(result, indent=2, default=str))
        return

    # Display report
    print(f"\n📊 Research Results:")
    print(json.dumps(orchestrator.to_dict(report), indent=2, default=str)[:2000])

    if args.output:
        orchestrator.save_report(report, Path(args.output))
        print(f"\n✅ Full report saved to {args.output}")


def cmd_trends(args):
    """Analyze trends."""
    agent = TrendScoutAgent(industry=args.industry)
    report = agent.analyze_trends(
        platforms=args.platforms,
        time_window=args.time_window,
        min_relevance=args.min_relevance
    )

    print(f"\n🔥 TREND REPORT")
    print("=" * 60)
    print(f"Found {len(report.trends)} relevant trends\n")

    for trend in report.trends[:5]:
        print(f"📈 {trend.topic}")
        print(f"   Platform: {trend.platform} | Growth: {trend.growth_rate}")
        print(f"   Relevance: {trend.relevance_to_ai:.0%}")
        print()

    print("🎯 Top Opportunities:")
    for opp in report.top_opportunities[:3]:
        print(f"  • {opp['opportunity']}")


def cmd_keywords(args):
    """Research keywords."""
    agent = KeywordResearcherAgent(domain=args.industry)
    report = agent.research_keywords(
        seed_topic=args.topic,
        depth="comprehensive",
        focus_intent=args.intent
    )

    print(f"\n🔍 KEYWORD RESEARCH: {args.topic}")
    print("=" * 60)

    for cluster in report.clusters[:3]:
        print(f"\n📊 Cluster: {cluster.cluster_name}")
        print(f"   Volume: {cluster.total_volume}")
        for kw in cluster.keywords[:3]:
            print(f"     • {kw.keyword} ({kw.search_volume}, {kw.difficulty})")

    print("\n⚡ Quick Wins:")
    for win in report.quick_wins:
        print(f"  ☐ {win}")


def cmd_ideas(args):
    """Generate content ideas."""
    agent = ContentIdeatorAgent()
    session = agent.generate_ideas(
        topic=args.topic,
        count=args.count,
        formats=args.formats
    )

    print(f"\n💡 CONTENT IDEAS: {args.topic}")
    print("=" * 60)

    for i, idea in enumerate(session.ideas[:args.count], 1):
        print(f"\n{i}. {idea.title}")
        print(f"   Format: {idea.format} | Effort: {idea.estimated_effort}")
        print(f"   Hook: {idea.hook[:60]}...")

    print("\n⚡ Quick Wins:")
    for win in session.quick_wins:
        print(f"  • {win}")


def cmd_audience(args):
    """Analyze audience."""
    agent = AudienceAnalystAgent(business_type=args.industry)
    analysis = agent.analyze_audience(
        target_description=args.target,
        depth="detailed"
    )

    print(f"\n👥 AUDIENCE ANALYSIS")
    print("=" * 60)

    for segment in analysis.segments:
        print(f"\n🎯 {segment.name}")
        print(f"   {segment.description}")
        print(f"   Channels: {', '.join(segment.preferred_channels[:3])}")

    for persona in analysis.personas:
        print(f"\n👤 {persona.name}")
        print(f"   {persona.role} at {persona.company_size}")
        print(f"   Challenge: {persona.daily_challenges[0]}")


def cmd_social(args):
    """Social listening."""
    agent = SocialListenerAgent(keywords=args.keywords)
    report = agent.listen(
        platforms=args.platforms,
        time_period=args.period
    )

    print(f"\n👂 SOCIAL LISTENING")
    print("=" * 60)
    print(f"Total mentions: {report.total_mentions}")
    print(f"Sentiment: {report.sentiment_summary}")

    print("\n🎯 Engagement Opportunities:")
    for opp in report.engagement_opportunities[:3]:
        print(f"  • [{opp['platform']}] {opp['description']}")

    print("\n💡 Content Ideas:")
    for idea in report.content_ideas[:3]:
        print(f"  • {idea}")


def cmd_experts(args):
    """Find experts."""
    agent = ExpertFinderAgent(domain=args.industry)
    report = agent.find_experts(
        query=args.query,
        min_followers=args.min_followers
    )

    print(f"\n👥 EXPERT FINDER: {args.query}")
    print("=" * 60)

    for expert in report.top_experts[:5]:
        print(f"\n👤 {expert.name}")
        print(f"   {expert.title} at {expert.organization}")
        print(f"   Followers: {expert.follower_count}")
        print(f"   Collaboration: {expert.collaboration_potential}")

    print("\n🤝 Collaboration Opportunities:")
    for opp in report.collaboration_opportunities[:3]:
        print(f"  • {opp['type']}: {opp['opportunity']}")


def main():
    parser = argparse.ArgumentParser(
        description="Research System CLI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python run_research.py research "AI automation" --mode quick
  python run_research.py trends --platforms twitter linkedin
  python run_research.py keywords "voice AI" --intent commercial
  python run_research.py ideas "AI for small business" --count 5
  python run_research.py audience "SMB owners interested in AI"
  python run_research.py social --keywords "AI consulting" "automation"
  python run_research.py experts "prompt engineering"
        """
    )

    parser.add_argument("--industry", default="AI consulting",
                       help="Industry context for research")
    parser.add_argument("--output", "-o", help="Output file for JSON report")

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Research command
    research_parser = subparsers.add_parser("research", help="Comprehensive research")
    research_parser.add_argument("topic", help="Research topic")
    research_parser.add_argument("--mode", choices=["full", "quick", "content", "competitive"],
                                 default="quick", help="Research mode")
    research_parser.add_argument("--agents", nargs="+", help="Specific agents to use")
    research_parser.add_argument("--sequential", action="store_true",
                                 help="Run agents sequentially")
    research_parser.set_defaults(func=cmd_research)

    # Trends command
    trends_parser = subparsers.add_parser("trends", help="Trend analysis")
    trends_parser.add_argument("--platforms", nargs="+",
                               default=["twitter", "linkedin", "reddit"],
                               help="Platforms to analyze")
    trends_parser.add_argument("--time-window", default="7d", help="Time window")
    trends_parser.add_argument("--min-relevance", type=float, default=0.6,
                               help="Minimum relevance score")
    trends_parser.set_defaults(func=cmd_trends)

    # Keywords command
    keywords_parser = subparsers.add_parser("keywords", help="Keyword research")
    keywords_parser.add_argument("topic", help="Seed topic")
    keywords_parser.add_argument("--intent", choices=["informational", "commercial", "transactional"],
                                 help="Focus on specific intent")
    keywords_parser.set_defaults(func=cmd_keywords)

    # Ideas command
    ideas_parser = subparsers.add_parser("ideas", help="Content ideation")
    ideas_parser.add_argument("topic", help="Content topic")
    ideas_parser.add_argument("--count", type=int, default=5, help="Number of ideas")
    ideas_parser.add_argument("--formats", nargs="+",
                              default=["blog_post", "linkedin_post", "twitter_thread"],
                              help="Content formats")
    ideas_parser.set_defaults(func=cmd_ideas)

    # Audience command
    audience_parser = subparsers.add_parser("audience", help="Audience analysis")
    audience_parser.add_argument("target", help="Target audience description")
    audience_parser.set_defaults(func=cmd_audience)

    # Social command
    social_parser = subparsers.add_parser("social", help="Social listening")
    social_parser.add_argument("--keywords", nargs="+",
                               default=["AI consulting", "automation"],
                               help="Keywords to monitor")
    social_parser.add_argument("--platforms", nargs="+",
                               default=["twitter", "linkedin", "reddit"],
                               help="Platforms to monitor")
    social_parser.add_argument("--period", default="24h", help="Time period")
    social_parser.set_defaults(func=cmd_social)

    # Experts command
    experts_parser = subparsers.add_parser("experts", help="Find experts")
    experts_parser.add_argument("query", help="Domain or topic")
    experts_parser.add_argument("--min-followers", type=int, default=1000,
                                help="Minimum follower count")
    experts_parser.set_defaults(func=cmd_experts)

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return

    args.func(args)


if __name__ == "__main__":
    main()
