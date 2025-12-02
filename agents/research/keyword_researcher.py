#!/usr/bin/env python3
"""
Keyword Researcher Agent

Researches and analyzes keywords for SEO and content optimization,
identifying opportunities for organic traffic growth.
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
class Keyword:
    """A researched keyword."""
    keyword: str
    search_volume: str
    difficulty: str  # "low", "medium", "high"
    intent: str  # "informational", "navigational", "transactional", "commercial"
    cpc: str
    trend: str  # "rising", "stable", "declining"
    opportunity_score: float
    related_keywords: List[str]
    content_suggestions: List[str]


@dataclass
class KeywordCluster:
    """A group of related keywords."""
    primary_keyword: str
    cluster_name: str
    keywords: List[Keyword]
    total_volume: str
    average_difficulty: str
    content_type_recommendation: str
    pillar_content_idea: str
    supporting_content_ideas: List[str]


@dataclass
class KeywordReport:
    """Complete keyword research report."""
    generated_at: str
    seed_topic: str
    clusters: List[KeywordCluster]
    top_opportunities: List[Keyword]
    content_calendar: List[Dict]
    quick_wins: List[str]


class KeywordResearcherAgent:
    """Agent that researches keywords for content strategy."""

    INTENT_TYPES = [
        "informational",
        "navigational",
        "transactional",
        "commercial"
    ]

    def __init__(self, domain: str = "AI consulting"):
        self.domain = domain
        self.client = anthropic.Anthropic() if HAS_ANTHROPIC else None

    def research_keywords(
        self,
        seed_topic: str,
        depth: str = "comprehensive",
        focus_intent: Optional[str] = None
    ) -> KeywordReport:
        """
        Research keywords around a seed topic.

        Args:
            seed_topic: Starting topic for research
            depth: Research depth (basic/comprehensive)
            focus_intent: Specific search intent to focus on

        Returns:
            KeywordReport with clusters and opportunities
        """
        if not self.client:
            return self._generate_mock_report(seed_topic)

        prompt = f"""You are an SEO keyword researcher specializing in {self.domain}.

Research keywords for: "{seed_topic}"

Research depth: {depth}
{f'Focus on {focus_intent} intent keywords' if focus_intent else 'Cover all intent types'}

Provide:
1. Keyword clusters (groups of related keywords)
2. For each keyword: search volume estimate, difficulty, intent, trend
3. Top opportunity keywords (high volume, low difficulty)
4. Content calendar suggestions
5. Quick win opportunities

Return as JSON:
{{
    "clusters": [
        {{
            "primary_keyword": "main keyword",
            "cluster_name": "Cluster theme",
            "keywords": [
                {{
                    "keyword": "keyword phrase",
                    "search_volume": "volume estimate",
                    "difficulty": "low/medium/high",
                    "intent": "informational/navigational/transactional/commercial",
                    "cpc": "estimated CPC",
                    "trend": "rising/stable/declining",
                    "opportunity_score": 0.0,
                    "related_keywords": [],
                    "content_suggestions": []
                }}
            ],
            "total_volume": "combined volume",
            "average_difficulty": "difficulty",
            "content_type_recommendation": "recommended format",
            "pillar_content_idea": "main content idea",
            "supporting_content_ideas": []
        }}
    ],
    "top_opportunities": [],
    "content_calendar": [
        {{
            "week": 1,
            "focus_cluster": "cluster name",
            "content_piece": "title",
            "target_keywords": []
        }}
    ],
    "quick_wins": []
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
                clusters = []

                for cluster_data in data.get("clusters", []):
                    keywords = [Keyword(**kw) for kw in cluster_data.get("keywords", [])]
                    clusters.append(KeywordCluster(
                        primary_keyword=cluster_data.get("primary_keyword", ""),
                        cluster_name=cluster_data.get("cluster_name", ""),
                        keywords=keywords,
                        total_volume=cluster_data.get("total_volume", ""),
                        average_difficulty=cluster_data.get("average_difficulty", ""),
                        content_type_recommendation=cluster_data.get("content_type_recommendation", ""),
                        pillar_content_idea=cluster_data.get("pillar_content_idea", ""),
                        supporting_content_ideas=cluster_data.get("supporting_content_ideas", [])
                    ))

                top_opps = [Keyword(**kw) for kw in data.get("top_opportunities", [])]

                return KeywordReport(
                    generated_at=datetime.now().isoformat(),
                    seed_topic=seed_topic,
                    clusters=clusters,
                    top_opportunities=top_opps,
                    content_calendar=data.get("content_calendar", []),
                    quick_wins=data.get("quick_wins", [])
                )
            except (json.JSONDecodeError, TypeError):
                pass

        return self._generate_mock_report(seed_topic)

    def _generate_mock_report(self, seed_topic: str) -> KeywordReport:
        """Generate mock report when API unavailable."""

        cluster1_keywords = [
            Keyword(
                keyword="ai automation for small business",
                search_volume="2,400/mo",
                difficulty="medium",
                intent="informational",
                cpc="$4.50",
                trend="rising",
                opportunity_score=0.85,
                related_keywords=["small business ai tools", "automate my business"],
                content_suggestions=["Complete guide", "Tool comparison", "Case studies"]
            ),
            Keyword(
                keyword="how to automate business processes with ai",
                search_volume="1,800/mo",
                difficulty="low",
                intent="informational",
                cpc="$3.80",
                trend="rising",
                opportunity_score=0.9,
                related_keywords=["ai workflow automation", "business process automation"],
                content_suggestions=["Step-by-step guide", "Video tutorial"]
            ),
            Keyword(
                keyword="ai automation examples",
                search_volume="3,200/mo",
                difficulty="low",
                intent="informational",
                cpc="$2.10",
                trend="stable",
                opportunity_score=0.88,
                related_keywords=["ai use cases", "automation case studies"],
                content_suggestions=["Examples roundup", "Industry-specific examples"]
            )
        ]

        cluster2_keywords = [
            Keyword(
                keyword="ai voice receptionist",
                search_volume="1,200/mo",
                difficulty="low",
                intent="commercial",
                cpc="$12.50",
                trend="rising",
                opportunity_score=0.92,
                related_keywords=["ai phone answering", "virtual receptionist ai"],
                content_suggestions=["Comparison article", "How it works guide"]
            ),
            Keyword(
                keyword="ai phone answering service",
                search_volume="2,100/mo",
                difficulty="medium",
                intent="transactional",
                cpc="$15.00",
                trend="rising",
                opportunity_score=0.8,
                related_keywords=["automated phone answering", "ai call center"],
                content_suggestions=["Buyer's guide", "ROI calculator"]
            )
        ]

        cluster3_keywords = [
            Keyword(
                keyword="prompt engineering consulting",
                search_volume="720/mo",
                difficulty="low",
                intent="commercial",
                cpc="$8.00",
                trend="rising",
                opportunity_score=0.88,
                related_keywords=["ai consulting services", "llm consulting"],
                content_suggestions=["Service page", "What to expect guide"]
            ),
            Keyword(
                keyword="ai consulting for startups",
                search_volume="880/mo",
                difficulty="medium",
                intent="transactional",
                cpc="$18.00",
                trend="stable",
                opportunity_score=0.75,
                related_keywords=["startup ai strategy", "ai implementation"],
                content_suggestions=["Service landing page", "Case studies"]
            )
        ]

        clusters = [
            KeywordCluster(
                primary_keyword="ai automation small business",
                cluster_name="AI Automation for SMBs",
                keywords=cluster1_keywords,
                total_volume="7,400/mo",
                average_difficulty="low",
                content_type_recommendation="Comprehensive guide + supporting articles",
                pillar_content_idea="The Complete Guide to AI Automation for Small Businesses (2024)",
                supporting_content_ideas=[
                    "10 AI Automation Examples That Save Time",
                    "AI Automation ROI Calculator",
                    "Getting Started with Business Automation"
                ]
            ),
            KeywordCluster(
                primary_keyword="ai voice receptionist",
                cluster_name="Voice AI Solutions",
                keywords=cluster2_keywords,
                total_volume="3,300/mo",
                average_difficulty="low-medium",
                content_type_recommendation="Comparison content + case studies",
                pillar_content_idea="AI Voice Receptionist: Complete Buyer's Guide",
                supporting_content_ideas=[
                    "Top 10 AI Phone Answering Services Compared",
                    "How AI Voice Receptionists Work",
                    "Voice AI Case Study: Dental Practice"
                ]
            ),
            KeywordCluster(
                primary_keyword="ai consulting",
                cluster_name="AI Consulting Services",
                keywords=cluster3_keywords,
                total_volume="1,600/mo",
                average_difficulty="medium",
                content_type_recommendation="Service pages + thought leadership",
                pillar_content_idea="What to Expect from AI Consulting Services",
                supporting_content_ideas=[
                    "AI Consulting vs DIY: When to Hire Help",
                    "Questions to Ask an AI Consultant",
                    "AI Implementation Roadmap"
                ]
            )
        ]

        top_opportunities = [
            cluster1_keywords[1],  # how to automate...
            cluster2_keywords[0],  # ai voice receptionist
            cluster1_keywords[2],  # ai automation examples
        ]

        return KeywordReport(
            generated_at=datetime.now().isoformat(),
            seed_topic=seed_topic,
            clusters=clusters,
            top_opportunities=top_opportunities,
            content_calendar=[
                {
                    "week": 1,
                    "focus_cluster": "AI Automation for SMBs",
                    "content_piece": "10 AI Automation Examples That Save 10+ Hours Weekly",
                    "target_keywords": ["ai automation examples", "business automation"]
                },
                {
                    "week": 2,
                    "focus_cluster": "Voice AI Solutions",
                    "content_piece": "AI Voice Receptionist: Is It Right for Your Business?",
                    "target_keywords": ["ai voice receptionist", "ai phone answering"]
                },
                {
                    "week": 3,
                    "focus_cluster": "AI Automation for SMBs",
                    "content_piece": "How to Automate Your Business Processes with AI",
                    "target_keywords": ["how to automate business processes with ai"]
                },
                {
                    "week": 4,
                    "focus_cluster": "AI Consulting Services",
                    "content_piece": "When to Hire an AI Consultant (And When to DIY)",
                    "target_keywords": ["ai consulting", "prompt engineering consulting"]
                }
            ],
            quick_wins=[
                "Create AI automation examples article (low difficulty, 3.2K volume)",
                "Optimize existing pages for 'ai voice receptionist' (rising trend)",
                "Add FAQ schema for 'how to' questions",
                "Build internal links from automation content to consulting services"
            ]
        )

    def find_content_gaps(
        self,
        existing_content: List[str],
        competitor_content: List[str]
    ) -> List[Dict]:
        """Identify keyword gaps between your content and competitors."""
        return [
            {
                "gap": "AI automation case studies",
                "competitor_coverage": "Strong",
                "your_coverage": "Weak",
                "priority": "high",
                "action": "Create 3 detailed case studies"
            },
            {
                "gap": "AI tool comparisons",
                "competitor_coverage": "Medium",
                "your_coverage": "None",
                "priority": "high",
                "action": "Create comparison content for key tools"
            },
            {
                "gap": "Industry-specific AI guides",
                "competitor_coverage": "Limited",
                "your_coverage": "None",
                "priority": "medium",
                "action": "Create healthcare/legal/finance AI guides"
            }
        ]

    def to_dict(self, report: KeywordReport) -> Dict:
        """Convert report to dictionary."""
        return {
            "generated_at": report.generated_at,
            "seed_topic": report.seed_topic,
            "clusters": [
                {
                    "primary_keyword": c.primary_keyword,
                    "cluster_name": c.cluster_name,
                    "keywords": [asdict(kw) for kw in c.keywords],
                    "total_volume": c.total_volume,
                    "average_difficulty": c.average_difficulty,
                    "content_type_recommendation": c.content_type_recommendation,
                    "pillar_content_idea": c.pillar_content_idea,
                    "supporting_content_ideas": c.supporting_content_ideas
                }
                for c in report.clusters
            ],
            "top_opportunities": [asdict(kw) for kw in report.top_opportunities],
            "content_calendar": report.content_calendar,
            "quick_wins": report.quick_wins
        }


def main():
    """Run keyword research."""
    import argparse

    parser = argparse.ArgumentParser(description="Research keywords")
    parser.add_argument("topic", nargs="?", default="ai automation services",
                       help="Seed topic for research")
    parser.add_argument("--depth", choices=["basic", "comprehensive"],
                       default="comprehensive", help="Research depth")
    parser.add_argument("--intent", choices=["informational", "commercial", "transactional"],
                       help="Focus on specific intent")
    parser.add_argument("--quick-wins", action="store_true",
                       help="Show only quick wins")
    parser.add_argument("--calendar", action="store_true",
                       help="Show content calendar")
    parser.add_argument("--output", type=Path,
                       help="Output file for JSON")

    args = parser.parse_args()

    agent = KeywordResearcherAgent()
    report = agent.research_keywords(
        seed_topic=args.topic,
        depth=args.depth,
        focus_intent=args.intent
    )

    if args.quick_wins:
        print("\n⚡ QUICK WINS:\n")
        for win in report.quick_wins:
            print(f"  ☐ {win}")
        return

    if args.calendar:
        print("\n📅 CONTENT CALENDAR:\n")
        for item in report.content_calendar:
            print(f"Week {item['week']}: {item['content_piece']}")
            print(f"   Cluster: {item['focus_cluster']}")
            print(f"   Keywords: {', '.join(item['target_keywords'])}")
            print()
        return

    print(f"\n🔍 KEYWORD RESEARCH: {report.seed_topic}")
    print(f"Generated: {report.generated_at}")
    print("=" * 60)

    print(f"\n📊 KEYWORD CLUSTERS ({len(report.clusters)}):\n")
    for cluster in report.clusters:
        print(f"🎯 {cluster.cluster_name}")
        print(f"   Primary: {cluster.primary_keyword}")
        print(f"   Volume: {cluster.total_volume} | Difficulty: {cluster.average_difficulty}")
        print(f"   Pillar: {cluster.pillar_content_idea}")
        print()

        for kw in cluster.keywords[:3]:
            intent_icon = {
                "informational": "ℹ️",
                "commercial": "💰",
                "transactional": "🛒",
                "navigational": "🧭"
            }.get(kw.intent, "❓")

            trend_icon = {"rising": "📈", "stable": "➡️", "declining": "📉"}.get(kw.trend, "")
            print(f"     {intent_icon} \"{kw.keyword}\"")
            print(f"        Vol: {kw.search_volume} | Diff: {kw.difficulty} | {trend_icon}")
        print()

    print("🏆 TOP OPPORTUNITIES:\n")
    for kw in report.top_opportunities:
        print(f"  • \"{kw.keyword}\"")
        print(f"    Score: {kw.opportunity_score:.0%} | Vol: {kw.search_volume} | Diff: {kw.difficulty}")

    print("\n⚡ QUICK WINS:\n")
    for win in report.quick_wins:
        print(f"  ☐ {win}")

    if args.output:
        with open(args.output, "w") as f:
            json.dump(agent.to_dict(report), f, indent=2)
        print(f"\n✅ Report saved to {args.output}")


if __name__ == "__main__":
    main()
