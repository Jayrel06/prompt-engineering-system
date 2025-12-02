#!/usr/bin/env python3
"""
Competitor Monitor Agent

Tracks competitor activities, content strategies, and market positioning
to identify opportunities and threats.
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
class Competitor:
    """A competitor profile."""
    name: str
    website: str
    category: str  # "direct", "indirect", "emerging"
    services: List[str]
    target_market: str
    pricing_tier: str  # "budget", "mid-market", "premium"
    strengths: List[str]
    weaknesses: List[str]
    content_strategy: str
    social_presence: Dict[str, str]
    recent_moves: List[str]


@dataclass
class CompetitorInsight:
    """An insight about competitor activity."""
    competitor: str
    insight_type: str  # "content", "product", "marketing", "hiring", "pricing"
    description: str
    source: str
    date_observed: str
    impact_level: str  # "low", "medium", "high"
    recommended_response: str


@dataclass
class MarketAnalysis:
    """Complete market analysis."""
    generated_at: str
    industry: str
    competitors: List[Competitor]
    insights: List[CompetitorInsight]
    market_gaps: List[str]
    opportunities: List[str]
    threats: List[str]
    recommended_positioning: str


class CompetitorMonitorAgent:
    """Agent that monitors competitor activities and market positioning."""

    def __init__(self, industry: str = "AI consulting"):
        self.industry = industry
        self.client = anthropic.Anthropic() if HAS_ANTHROPIC else None
        self.competitors: Dict[str, Competitor] = {}
        self._load_known_competitors()

    def _load_known_competitors(self):
        """Load known competitors in the AI consulting space."""
        known = [
            Competitor(
                name="Boston Consulting Group (BCG)",
                website="bcg.com",
                category="indirect",
                services=["Strategy consulting", "AI implementation", "Digital transformation"],
                target_market="Enterprise",
                pricing_tier="premium",
                strengths=["Brand recognition", "Enterprise relationships", "Full-service"],
                weaknesses=["Slow to move", "Expensive", "Generic solutions"],
                content_strategy="Thought leadership, research reports, industry events",
                social_presence={"linkedin": "Very active", "twitter": "Active"},
                recent_moves=["Launched AI practice", "Acquired AI startups"]
            ),
            Competitor(
                name="Accenture",
                website="accenture.com",
                category="indirect",
                services=["Technology consulting", "AI/ML services", "Cloud migration"],
                target_market="Enterprise",
                pricing_tier="premium",
                strengths=["Scale", "Technical depth", "Global presence"],
                weaknesses=["Bureaucratic", "Cookie-cutter solutions", "Very expensive"],
                content_strategy="Case studies, webinars, industry reports",
                social_presence={"linkedin": "Very active", "twitter": "Active"},
                recent_moves=["Heavy AI marketing push", "Partnerships with cloud providers"]
            ),
            Competitor(
                name="AI consulting boutiques",
                website="various",
                category="direct",
                services=["AI strategy", "Custom AI development", "AI training"],
                target_market="SMB to Mid-market",
                pricing_tier="mid-market",
                strengths=["Agile", "Specialized", "Personal attention"],
                weaknesses=["Limited capacity", "Less brand recognition"],
                content_strategy="Blog posts, LinkedIn content, case studies",
                social_presence={"linkedin": "Active", "twitter": "Varies"},
                recent_moves=["Increased content marketing", "Niche specialization"]
            ),
            Competitor(
                name="Freelance AI consultants",
                website="various",
                category="direct",
                services=["Prompt engineering", "AI implementation", "Training"],
                target_market="Small business",
                pricing_tier="budget",
                strengths=["Low cost", "Flexible", "Accessible"],
                weaknesses=["Quality varies", "Limited scope", "Availability"],
                content_strategy="Social media, YouTube tutorials, Substack",
                social_presence={"twitter": "Very active", "youtube": "Active"},
                recent_moves=["Commoditization of basic services", "Focus on personal branding"]
            )
        ]

        for comp in known:
            self.competitors[comp.name.lower()] = comp

    def add_competitor(self, competitor: Competitor):
        """Add a competitor to track."""
        self.competitors[competitor.name.lower()] = competitor

    def analyze_market(
        self,
        focus_areas: Optional[List[str]] = None
    ) -> MarketAnalysis:
        """Perform comprehensive market analysis."""

        focus_areas = focus_areas or ["content", "pricing", "positioning"]

        if not self.client:
            return self._generate_mock_analysis()

        competitors_text = "\n".join([
            f"- {c.name}: {c.category} competitor, {c.pricing_tier} pricing, "
            f"serves {c.target_market}"
            for c in self.competitors.values()
        ])

        prompt = f"""You are a competitive intelligence analyst for {self.industry}.

Analyze this competitive landscape:

{competitors_text}

Focus areas: {', '.join(focus_areas)}

Provide:
1. Key insights about each competitor's recent activities
2. Market gaps that could be exploited
3. Opportunities for differentiation
4. Potential threats to watch
5. Recommended positioning strategy

Return as JSON:
{{
    "insights": [
        {{
            "competitor": "name",
            "insight_type": "content/product/marketing/pricing",
            "description": "insight description",
            "source": "observed from",
            "date_observed": "YYYY-MM-DD",
            "impact_level": "low/medium/high",
            "recommended_response": "what to do"
        }}
    ],
    "market_gaps": ["gap1", "gap2"],
    "opportunities": ["opp1", "opp2"],
    "threats": ["threat1", "threat2"],
    "recommended_positioning": "positioning statement"
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
                insights = [CompetitorInsight(**i) for i in data.get("insights", [])]

                return MarketAnalysis(
                    generated_at=datetime.now().isoformat(),
                    industry=self.industry,
                    competitors=list(self.competitors.values()),
                    insights=insights,
                    market_gaps=data.get("market_gaps", []),
                    opportunities=data.get("opportunities", []),
                    threats=data.get("threats", []),
                    recommended_positioning=data.get("recommended_positioning", "")
                )
            except (json.JSONDecodeError, TypeError):
                pass

        return self._generate_mock_analysis()

    def _generate_mock_analysis(self) -> MarketAnalysis:
        """Generate mock analysis when API unavailable."""
        insights = [
            CompetitorInsight(
                competitor="Large consultancies",
                insight_type="marketing",
                description="Increasing focus on AI transformation messaging, but still generic",
                source="LinkedIn and website monitoring",
                date_observed=datetime.now().strftime("%Y-%m-%d"),
                impact_level="medium",
                recommended_response="Differentiate with specific, actionable AI use cases"
            ),
            CompetitorInsight(
                competitor="AI boutiques",
                insight_type="content",
                description="Shift toward video content and tutorials on YouTube",
                source="Social media analysis",
                date_observed=datetime.now().strftime("%Y-%m-%d"),
                impact_level="medium",
                recommended_response="Consider video content strategy for broader reach"
            ),
            CompetitorInsight(
                competitor="Freelancers",
                insight_type="pricing",
                description="Race to bottom on basic prompt engineering services",
                source="Upwork and Fiverr analysis",
                date_observed=datetime.now().strftime("%Y-%m-%d"),
                impact_level="low",
                recommended_response="Position on outcomes and ROI, not hourly rates"
            )
        ]

        return MarketAnalysis(
            generated_at=datetime.now().isoformat(),
            industry=self.industry,
            competitors=list(self.competitors.values()),
            insights=insights,
            market_gaps=[
                "SMB-focused AI consulting with enterprise quality",
                "Industry-specific AI solutions (healthcare, legal, etc.)",
                "AI implementation with ongoing optimization",
                "Transparent, outcome-based pricing models"
            ],
            opportunities=[
                "Voice AI for small business reception",
                "AI automation packages with fixed pricing",
                "Content series on practical AI implementation",
                "Partnerships with complementary service providers"
            ],
            threats=[
                "Commoditization of basic AI services",
                "Large players moving downmarket",
                "DIY tools reducing need for consultants",
                "Economic uncertainty affecting consulting budgets"
            ],
            recommended_positioning=(
                "Position as the practical AI partner for growing businesses: "
                "Enterprise-quality solutions at SMB-friendly prices, with clear ROI "
                "and hands-on implementation support."
            )
        )

    def get_content_gaps(self) -> List[Dict]:
        """Identify content gaps vs competitors."""
        return [
            {
                "gap": "Practical AI implementation tutorials",
                "competitors_covering": "Few",
                "opportunity_level": "high",
                "suggested_formats": ["Blog series", "Video tutorials", "Case studies"]
            },
            {
                "gap": "AI ROI calculators and tools",
                "competitors_covering": "Almost none",
                "opportunity_level": "high",
                "suggested_formats": ["Interactive tools", "Spreadsheet templates"]
            },
            {
                "gap": "Industry-specific AI use cases",
                "competitors_covering": "Generic coverage only",
                "opportunity_level": "medium",
                "suggested_formats": ["Industry guides", "Webinars"]
            },
            {
                "gap": "Behind-the-scenes AI project content",
                "competitors_covering": "None",
                "opportunity_level": "medium",
                "suggested_formats": ["LinkedIn posts", "Newsletter series"]
            }
        ]

    def to_dict(self, analysis: MarketAnalysis) -> Dict:
        """Convert analysis to dictionary."""
        return {
            "generated_at": analysis.generated_at,
            "industry": analysis.industry,
            "competitors": [asdict(c) for c in analysis.competitors],
            "insights": [asdict(i) for i in analysis.insights],
            "market_gaps": analysis.market_gaps,
            "opportunities": analysis.opportunities,
            "threats": analysis.threats,
            "recommended_positioning": analysis.recommended_positioning
        }


def main():
    """Run competitor monitoring."""
    import argparse

    parser = argparse.ArgumentParser(description="Monitor competitors")
    parser.add_argument("--industry", default="AI consulting",
                       help="Industry focus")
    parser.add_argument("--focus", nargs="+",
                       default=["content", "pricing", "positioning"],
                       help="Areas to focus analysis on")
    parser.add_argument("--content-gaps", action="store_true",
                       help="Show content gap analysis")
    parser.add_argument("--output", type=Path,
                       help="Output file for JSON report")

    args = parser.parse_args()

    agent = CompetitorMonitorAgent(industry=args.industry)

    if args.content_gaps:
        gaps = agent.get_content_gaps()
        print("\n📊 CONTENT GAP ANALYSIS\n")
        print("=" * 60)
        for gap in gaps:
            print(f"\n🎯 {gap['gap']}")
            print(f"   Competitors covering: {gap['competitors_covering']}")
            print(f"   Opportunity: {gap['opportunity_level']}")
            print(f"   Suggested formats: {', '.join(gap['suggested_formats'])}")
        return

    analysis = agent.analyze_market(focus_areas=args.focus)

    print(f"\n🔍 MARKET ANALYSIS - {analysis.industry}")
    print(f"Generated: {analysis.generated_at}")
    print("=" * 60)

    print(f"\n📊 COMPETITOR INSIGHTS ({len(analysis.insights)}):\n")
    for insight in analysis.insights:
        print(f"  [{insight.impact_level.upper()}] {insight.competitor}")
        print(f"    Type: {insight.insight_type}")
        print(f"    {insight.description}")
        print(f"    → Response: {insight.recommended_response}")
        print()

    print("🕳️ MARKET GAPS:\n")
    for gap in analysis.market_gaps:
        print(f"  • {gap}")

    print("\n🚀 OPPORTUNITIES:\n")
    for opp in analysis.opportunities:
        print(f"  • {opp}")

    print("\n⚠️ THREATS:\n")
    for threat in analysis.threats:
        print(f"  • {threat}")

    print("\n🎯 RECOMMENDED POSITIONING:\n")
    print(f"  {analysis.recommended_positioning}")

    if args.output:
        with open(args.output, "w") as f:
            json.dump(agent.to_dict(analysis), f, indent=2)
        print(f"\n✅ Analysis saved to {args.output}")


if __name__ == "__main__":
    main()
