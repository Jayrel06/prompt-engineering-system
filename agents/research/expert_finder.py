#!/usr/bin/env python3
"""
Expert Finder Agent

Identifies and profiles experts, influencers, and thought leaders
in target domains for collaboration and learning opportunities.
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
class Expert:
    """An expert or influencer profile."""
    name: str
    title: str
    organization: str
    expertise_areas: List[str]
    platforms: Dict[str, str]  # platform -> handle/url
    follower_count: str
    engagement_rate: str
    content_focus: List[str]
    collaboration_potential: str  # "low", "medium", "high"
    contact_approach: str
    notable_content: List[str]
    relevance_score: float


@dataclass
class ExpertNetwork:
    """A network of related experts."""
    domain: str
    experts: List[Expert]
    connections: List[Dict]  # relationships between experts
    key_communities: List[str]
    events_and_conferences: List[str]
    publications: List[str]


@dataclass
class ExpertFinderReport:
    """Complete expert finding report."""
    generated_at: str
    search_query: str
    networks: List[ExpertNetwork]
    top_experts: List[Expert]
    collaboration_opportunities: List[Dict]
    outreach_templates: Dict[str, str]


class ExpertFinderAgent:
    """Agent that finds and profiles domain experts."""

    PLATFORMS = [
        "twitter",
        "linkedin",
        "youtube",
        "substack",
        "medium",
        "podcast",
        "conference_speaker"
    ]

    def __init__(self, domain: str = "AI and automation"):
        self.domain = domain
        self.client = anthropic.Anthropic() if HAS_ANTHROPIC else None

    def find_experts(
        self,
        query: str,
        min_followers: int = 1000,
        platforms: Optional[List[str]] = None
    ) -> ExpertFinderReport:
        """
        Find experts in a given domain.

        Args:
            query: Topic or domain to find experts in
            min_followers: Minimum follower threshold
            platforms: Platforms to search

        Returns:
            ExpertFinderReport with found experts
        """
        platforms = platforms or self.PLATFORMS

        if not self.client:
            return self._generate_mock_report(query)

        prompt = f"""You are an expert researcher finding thought leaders in {self.domain}.

Find experts related to: "{query}"

Minimum followers: {min_followers}
Platforms to search: {', '.join(platforms)}

For each expert, provide:
1. Name and title
2. Organization
3. Expertise areas
4. Platform presence (handles/URLs)
5. Follower count estimate
6. Engagement rate estimate
7. Content focus areas
8. Collaboration potential (low/medium/high)
9. Best approach for outreach
10. Notable content they've created
11. Relevance score (0-1)

Also identify:
- Expert networks and communities
- Key events and conferences
- Relevant publications
- Collaboration opportunities

Return as JSON:
{{
    "networks": [
        {{
            "domain": "domain name",
            "experts": [
                {{
                    "name": "name",
                    "title": "title",
                    "organization": "org",
                    "expertise_areas": [],
                    "platforms": {{"twitter": "@handle"}},
                    "follower_count": "10K",
                    "engagement_rate": "3%",
                    "content_focus": [],
                    "collaboration_potential": "high",
                    "contact_approach": "approach",
                    "notable_content": [],
                    "relevance_score": 0.0
                }}
            ],
            "connections": [],
            "key_communities": [],
            "events_and_conferences": [],
            "publications": []
        }}
    ],
    "top_experts": [],
    "collaboration_opportunities": [
        {{
            "type": "type",
            "expert": "name",
            "opportunity": "description",
            "priority": "high/medium/low"
        }}
    ],
    "outreach_templates": {{
        "cold_intro": "template",
        "collaboration_pitch": "template",
        "guest_content": "template"
    }}
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

                networks = []
                for net_data in data.get("networks", []):
                    experts = [Expert(**e) for e in net_data.get("experts", [])]
                    networks.append(ExpertNetwork(
                        domain=net_data.get("domain", ""),
                        experts=experts,
                        connections=net_data.get("connections", []),
                        key_communities=net_data.get("key_communities", []),
                        events_and_conferences=net_data.get("events_and_conferences", []),
                        publications=net_data.get("publications", [])
                    ))

                top_experts = [Expert(**e) for e in data.get("top_experts", [])]

                return ExpertFinderReport(
                    generated_at=datetime.now().isoformat(),
                    search_query=query,
                    networks=networks,
                    top_experts=top_experts,
                    collaboration_opportunities=data.get("collaboration_opportunities", []),
                    outreach_templates=data.get("outreach_templates", {})
                )
            except (json.JSONDecodeError, TypeError):
                pass

        return self._generate_mock_report(query)

    def _generate_mock_report(self, query: str) -> ExpertFinderReport:
        """Generate mock report when API unavailable."""

        experts = [
            Expert(
                name="AI Industry Leader",
                title="CEO & AI Researcher",
                organization="AI Research Lab",
                expertise_areas=["LLMs", "AI Strategy", "Enterprise AI"],
                platforms={
                    "twitter": "@ai_leader",
                    "linkedin": "/in/ai-leader",
                    "substack": "ai-insights.substack.com"
                },
                follower_count="150K",
                engagement_rate="4.2%",
                content_focus=["AI trends", "Research insights", "Industry analysis"],
                collaboration_potential="medium",
                contact_approach="Engage with content first, then DM with specific value prop",
                notable_content=[
                    "Thread on LLM scaling laws (50K likes)",
                    "Blog on enterprise AI adoption",
                    "Podcast appearances on AI futures"
                ],
                relevance_score=0.92
            ),
            Expert(
                name="Automation Expert",
                title="Founder & Consultant",
                organization="Automation Consulting Co",
                expertise_areas=["Business Automation", "Workflow Design", "SMB Tech"],
                platforms={
                    "twitter": "@auto_expert",
                    "linkedin": "/in/auto-expert",
                    "youtube": "AutomationMasterclass"
                },
                follower_count="45K",
                engagement_rate="6.1%",
                content_focus=["Practical automation", "Tool tutorials", "Case studies"],
                collaboration_potential="high",
                contact_approach="Direct DM works, mention specific content you liked",
                notable_content=[
                    "YouTube series on n8n (100K views)",
                    "Automation templates library",
                    "SMB automation guide"
                ],
                relevance_score=0.88
            ),
            Expert(
                name="Prompt Engineering Pro",
                title="AI Consultant & Educator",
                organization="Independent",
                expertise_areas=["Prompt Engineering", "Claude/GPT", "AI Education"],
                platforms={
                    "twitter": "@prompt_pro",
                    "linkedin": "/in/prompt-pro",
                    "medium": "@prompt.pro"
                },
                follower_count="25K",
                engagement_rate="5.5%",
                content_focus=["Prompt tips", "Technique tutorials", "Tool reviews"],
                collaboration_potential="high",
                contact_approach="Open to collaborations, prefers email intro",
                notable_content=[
                    "Prompt engineering masterclass",
                    "Claude vs GPT comparison threads",
                    "Weekly prompt tips newsletter"
                ],
                relevance_score=0.95
            )
        ]

        network = ExpertNetwork(
            domain=query,
            experts=experts,
            connections=[
                {"from": "AI Industry Leader", "to": "Prompt Engineering Pro", "type": "collaborators"},
                {"from": "Automation Expert", "to": "Prompt Engineering Pro", "type": "content_crossover"}
            ],
            key_communities=[
                "AI Twitter community",
                "Latent Space Discord",
                "AI consulting Slack groups",
                "LinkedIn AI creator network"
            ],
            events_and_conferences=[
                "AI Engineer Summit",
                "NeurIPS workshops",
                "Local AI meetups",
                "Virtual AI conferences"
            ],
            publications=[
                "The Gradient",
                "AI Weekly newsletter",
                "Towards Data Science"
            ]
        )

        return ExpertFinderReport(
            generated_at=datetime.now().isoformat(),
            search_query=query,
            networks=[network],
            top_experts=experts[:3],
            collaboration_opportunities=[
                {
                    "type": "Guest Post",
                    "expert": "Prompt Engineering Pro",
                    "opportunity": "Write guest post for their newsletter",
                    "priority": "high"
                },
                {
                    "type": "Podcast",
                    "expert": "Automation Expert",
                    "opportunity": "Guest on their YouTube channel",
                    "priority": "high"
                },
                {
                    "type": "Co-creation",
                    "expert": "AI Industry Leader",
                    "opportunity": "Collaborate on research report",
                    "priority": "medium"
                }
            ],
            outreach_templates={
                "cold_intro": """Hi [Name],

I've been following your work on [specific topic] and particularly loved your [specific content].

I'm [your name], working on [your focus]. I'd love to connect and share some thoughts on [overlap topic].

Would you be open to a brief chat?

Best,
[Your name]""",
                "collaboration_pitch": """Hi [Name],

I have an idea for a collaboration that I think could be valuable for both our audiences.

[Specific collaboration idea]

I've been following your work and think our expertise in [overlap] would create something unique.

Would you be interested in exploring this?

Best,
[Your name]""",
                "guest_content": """Hi [Name],

I'd love to contribute a guest piece to [their platform] on [topic].

Specifically, I'm thinking about [specific angle] which I believe would resonate with your audience because [reason].

I've written about this topic at [your examples].

Would this be something you'd consider?

Best,
[Your name]"""
            }
        )

    def find_collaboration_matches(
        self,
        your_expertise: List[str],
        your_audience_size: str,
        collaboration_goals: List[str]
    ) -> List[Dict]:
        """Find experts who match collaboration criteria."""
        return [
            {
                "expert": "Prompt Engineering Pro",
                "match_score": 0.9,
                "overlap_areas": ["prompt engineering", "AI consulting"],
                "complementary_areas": ["education content", "newsletter audience"],
                "suggested_collab": "Co-create prompt engineering guide"
            },
            {
                "expert": "Automation Expert",
                "match_score": 0.85,
                "overlap_areas": ["automation", "SMB focus"],
                "complementary_areas": ["YouTube presence", "tutorial content"],
                "suggested_collab": "Joint webinar on AI automation"
            }
        ]

    def to_dict(self, report: ExpertFinderReport) -> Dict:
        """Convert report to dictionary."""
        return {
            "generated_at": report.generated_at,
            "search_query": report.search_query,
            "networks": [
                {
                    "domain": n.domain,
                    "experts": [asdict(e) for e in n.experts],
                    "connections": n.connections,
                    "key_communities": n.key_communities,
                    "events_and_conferences": n.events_and_conferences,
                    "publications": n.publications
                }
                for n in report.networks
            ],
            "top_experts": [asdict(e) for e in report.top_experts],
            "collaboration_opportunities": report.collaboration_opportunities,
            "outreach_templates": report.outreach_templates
        }


def main():
    """Run expert finder."""
    import argparse

    parser = argparse.ArgumentParser(description="Find domain experts")
    parser.add_argument("query", nargs="?", default="AI automation and prompt engineering",
                       help="Domain or topic to find experts in")
    parser.add_argument("--min-followers", type=int, default=1000,
                       help="Minimum follower count")
    parser.add_argument("--platforms", nargs="+",
                       help="Platforms to search")
    parser.add_argument("--opportunities", action="store_true",
                       help="Show collaboration opportunities")
    parser.add_argument("--templates", action="store_true",
                       help="Show outreach templates")
    parser.add_argument("--output", type=Path,
                       help="Output file for JSON")

    args = parser.parse_args()

    agent = ExpertFinderAgent()
    report = agent.find_experts(
        query=args.query,
        min_followers=args.min_followers,
        platforms=args.platforms
    )

    if args.opportunities:
        print("\n🤝 COLLABORATION OPPORTUNITIES:\n")
        for opp in report.collaboration_opportunities:
            priority_icon = {"high": "🔴", "medium": "🟡", "low": "🟢"}.get(opp["priority"], "⚪")
            print(f"{priority_icon} {opp['type']}: {opp['expert']}")
            print(f"   {opp['opportunity']}")
            print()
        return

    if args.templates:
        print("\n📧 OUTREACH TEMPLATES:\n")
        for template_name, template in report.outreach_templates.items():
            print(f"{'='*60}")
            print(f"📝 {template_name.upper().replace('_', ' ')}")
            print("="*60)
            print(template)
            print()
        return

    print(f"\n👥 EXPERT FINDER REPORT")
    print(f"Query: {report.search_query}")
    print(f"Generated: {report.generated_at}")
    print("=" * 60)

    print(f"\n🌟 TOP EXPERTS ({len(report.top_experts)}):\n")
    for expert in report.top_experts:
        collab_icon = {"high": "🔥", "medium": "✨", "low": "💡"}.get(expert.collaboration_potential, "")

        print(f"👤 {expert.name}")
        print(f"   {expert.title} at {expert.organization}")
        print(f"   Followers: {expert.follower_count} | Engagement: {expert.engagement_rate}")
        print(f"   Expertise: {', '.join(expert.expertise_areas[:3])}")
        print(f"   Relevance: {expert.relevance_score:.0%} | Collab potential: {collab_icon} {expert.collaboration_potential}")
        print(f"   Approach: {expert.contact_approach[:60]}...")
        print()

    if report.networks:
        network = report.networks[0]
        print(f"🌐 NETWORK INFO:\n")
        print(f"  Communities: {', '.join(network.key_communities[:3])}")
        print(f"  Events: {', '.join(network.events_and_conferences[:3])}")
        print(f"  Publications: {', '.join(network.publications[:3])}")

    print("\n🤝 TOP COLLABORATION OPPORTUNITIES:\n")
    for opp in report.collaboration_opportunities[:3]:
        print(f"  • {opp['type']} with {opp['expert']}: {opp['opportunity']}")

    if args.output:
        with open(args.output, "w") as f:
            json.dump(agent.to_dict(report), f, indent=2)
        print(f"\n✅ Report saved to {args.output}")


if __name__ == "__main__":
    main()
