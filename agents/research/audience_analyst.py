#!/usr/bin/env python3
"""
Audience Analyst Agent

Analyzes target audience characteristics, preferences, and behaviors
to optimize content and messaging strategies.
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
class AudienceSegment:
    """A target audience segment."""
    name: str
    description: str
    size_estimate: str
    demographics: Dict[str, str]
    psychographics: Dict[str, List[str]]
    pain_points: List[str]
    goals: List[str]
    preferred_channels: List[str]
    content_preferences: Dict[str, str]
    buying_triggers: List[str]
    objections: List[str]
    engagement_level: str  # "cold", "warm", "hot"


@dataclass
class AudiencePersona:
    """A detailed audience persona."""
    name: str
    role: str
    company_size: str
    industry: str
    background: str
    daily_challenges: List[str]
    goals: List[str]
    fears: List[str]
    information_sources: List[str]
    decision_factors: List[str]
    content_format_preferences: List[str]
    messaging_tone: str
    example_quotes: List[str]


@dataclass
class AudienceAnalysis:
    """Complete audience analysis."""
    generated_at: str
    business_context: str
    segments: List[AudienceSegment]
    personas: List[AudiencePersona]
    content_recommendations: List[Dict]
    channel_strategy: Dict[str, Dict]
    messaging_guidelines: List[str]


class AudienceAnalystAgent:
    """Agent that analyzes and segments target audiences."""

    def __init__(self, business_type: str = "AI consulting"):
        self.business_type = business_type
        self.client = anthropic.Anthropic() if HAS_ANTHROPIC else None

    def analyze_audience(
        self,
        target_description: str,
        depth: str = "detailed"
    ) -> AudienceAnalysis:
        """
        Analyze target audience and create segments/personas.

        Args:
            target_description: Description of target market
            depth: Analysis depth (basic/detailed/comprehensive)

        Returns:
            AudienceAnalysis with segments and personas
        """
        if not self.client:
            return self._generate_mock_analysis()

        prompt = f"""You are an audience research specialist for {self.business_type}.

Analyze this target audience: "{target_description}"

Analysis depth: {depth}

Provide:
1. 2-3 distinct audience segments
2. 2 detailed buyer personas
3. Content recommendations per segment
4. Channel strategy
5. Messaging guidelines

Return as JSON:
{{
    "segments": [
        {{
            "name": "Segment name",
            "description": "Who they are",
            "size_estimate": "Market size",
            "demographics": {{"title": "", "company_size": "", "industry": ""}},
            "psychographics": {{"values": [], "motivations": [], "frustrations": []}},
            "pain_points": [],
            "goals": [],
            "preferred_channels": [],
            "content_preferences": {{"format": "", "length": "", "tone": ""}},
            "buying_triggers": [],
            "objections": [],
            "engagement_level": "cold/warm/hot"
        }}
    ],
    "personas": [
        {{
            "name": "Persona name",
            "role": "Job title",
            "company_size": "Size",
            "industry": "Industry",
            "background": "Brief background",
            "daily_challenges": [],
            "goals": [],
            "fears": [],
            "information_sources": [],
            "decision_factors": [],
            "content_format_preferences": [],
            "messaging_tone": "How to speak to them",
            "example_quotes": ["Things they might say"]
        }}
    ],
    "content_recommendations": [
        {{
            "segment": "Segment name",
            "content_types": [],
            "topics": [],
            "frequency": ""
        }}
    ],
    "channel_strategy": {{
        "linkedin": {{"priority": "high/medium/low", "content_type": "", "frequency": ""}},
        "twitter": {{}},
        "email": {{}},
        "youtube": {{}}
    }},
    "messaging_guidelines": []
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
                segments = [AudienceSegment(**s) for s in data.get("segments", [])]
                personas = [AudiencePersona(**p) for p in data.get("personas", [])]

                return AudienceAnalysis(
                    generated_at=datetime.now().isoformat(),
                    business_context=self.business_type,
                    segments=segments,
                    personas=personas,
                    content_recommendations=data.get("content_recommendations", []),
                    channel_strategy=data.get("channel_strategy", {}),
                    messaging_guidelines=data.get("messaging_guidelines", [])
                )
            except (json.JSONDecodeError, TypeError):
                pass

        return self._generate_mock_analysis()

    def _generate_mock_analysis(self) -> AudienceAnalysis:
        """Generate mock analysis when API unavailable."""
        segments = [
            AudienceSegment(
                name="Growth-Stage Founders",
                description="Founders of companies doing $1M-10M ARR looking to scale with AI",
                size_estimate="500K+ in the US",
                demographics={
                    "title": "CEO/Founder",
                    "company_size": "10-50 employees",
                    "industry": "Tech, SaaS, Professional Services"
                },
                psychographics={
                    "values": ["Efficiency", "Innovation", "Competitive edge"],
                    "motivations": ["Scale without headcount", "Stay competitive", "Reduce costs"],
                    "frustrations": ["Too many AI options", "Hard to evaluate ROI", "Limited technical resources"]
                },
                pain_points=[
                    "Can't hire fast enough",
                    "Competitors adopting AI faster",
                    "Overwhelmed by AI options",
                    "Need to do more with less"
                ],
                goals=[
                    "10x productivity gains",
                    "Automate repetitive work",
                    "Better customer experience",
                    "Data-driven decisions"
                ],
                preferred_channels=["LinkedIn", "Twitter/X", "Podcasts", "Email"],
                content_preferences={
                    "format": "Case studies, how-tos, tools",
                    "length": "Medium (5-10 min reads)",
                    "tone": "Direct, practical, no fluff"
                },
                buying_triggers=[
                    "Competitor success story",
                    "Clear ROI projection",
                    "Quick implementation timeline",
                    "Low-risk pilot option"
                ],
                objections=[
                    "Is this actually better than existing tools?",
                    "Do we have resources to implement?",
                    "What if it doesn't work?",
                    "How do we measure success?"
                ],
                engagement_level="warm"
            ),
            AudienceSegment(
                name="Operations Leaders",
                description="VP/Directors of Ops looking to automate and optimize",
                size_estimate="200K+ in the US",
                demographics={
                    "title": "VP/Director of Operations",
                    "company_size": "50-500 employees",
                    "industry": "Various B2B"
                },
                psychographics={
                    "values": ["Efficiency", "Process improvement", "Team productivity"],
                    "motivations": ["Hit KPIs", "Reduce costs", "Impress leadership"],
                    "frustrations": ["Manual processes", "Tool sprawl", "Resistance to change"]
                },
                pain_points=[
                    "Too much manual work",
                    "Inconsistent processes",
                    "Difficult to scale",
                    "Tool fatigue"
                ],
                goals=[
                    "Streamline operations",
                    "Reduce errors",
                    "Free up team for strategic work",
                    "Demonstrate impact"
                ],
                preferred_channels=["LinkedIn", "Webinars", "Email", "Industry conferences"],
                content_preferences={
                    "format": "Detailed guides, checklists, benchmarks",
                    "length": "Long-form acceptable",
                    "tone": "Professional, data-driven"
                },
                buying_triggers=[
                    "ROI calculator",
                    "Implementation roadmap",
                    "Similar company case study",
                    "Risk mitigation"
                ],
                objections=[
                    "Integration complexity",
                    "Change management concerns",
                    "Budget approval process",
                    "Proof of reliability"
                ],
                engagement_level="warm"
            )
        ]

        personas = [
            AudiencePersona(
                name="Growth-Focused Sarah",
                role="CEO/Founder",
                company_size="25 employees",
                industry="SaaS",
                background="Technical founder, built product from scratch, now focused on scaling",
                daily_challenges=[
                    "Wearing too many hats",
                    "Customer support taking too much time",
                    "Sales team needs better tools",
                    "Can't hire fast enough"
                ],
                goals=[
                    "Get to $5M ARR this year",
                    "Reduce operational overhead",
                    "Maintain quality while scaling",
                    "Stay ahead of competition"
                ],
                fears=[
                    "Falling behind competitors",
                    "Wasting money on wrong tools",
                    "Team burnout",
                    "Losing company culture"
                ],
                information_sources=[
                    "Twitter/X (tech founders)",
                    "LinkedIn",
                    "Founder podcasts",
                    "Peer networks"
                ],
                decision_factors=[
                    "Speed to value",
                    "Easy implementation",
                    "Clear ROI",
                    "Founder-friendly pricing"
                ],
                content_format_preferences=[
                    "Short-form videos",
                    "Twitter threads",
                    "Quick case studies",
                    "Tool comparisons"
                ],
                messaging_tone="Direct, founder-to-founder, practical",
                example_quotes=[
                    "Just tell me what works",
                    "I don't have time for long implementations",
                    "Show me the numbers",
                    "What are other founders doing?"
                ]
            ),
            AudiencePersona(
                name="Process-Driven Mike",
                role="Director of Operations",
                company_size="150 employees",
                industry="Professional Services",
                background="Operations career, moved up from analyst, process improvement certified",
                daily_challenges=[
                    "Manual data entry and reporting",
                    "Inconsistent processes across teams",
                    "Getting buy-in for new tools",
                    "Proving ROI to leadership"
                ],
                goals=[
                    "Automate 50% of manual work",
                    "Standardize processes",
                    "Reduce errors by 80%",
                    "Build case for larger budget"
                ],
                fears=[
                    "Implementing something that fails",
                    "Team resistance",
                    "Looking bad to leadership",
                    "Scope creep"
                ],
                information_sources=[
                    "LinkedIn",
                    "Industry webinars",
                    "Operations communities",
                    "Vendor demos"
                ],
                decision_factors=[
                    "Proven track record",
                    "Implementation support",
                    "Integration capabilities",
                    "Vendor stability"
                ],
                content_format_preferences=[
                    "Detailed guides",
                    "Webinars",
                    "ROI calculators",
                    "Implementation roadmaps"
                ],
                messaging_tone="Professional, detailed, data-backed",
                example_quotes=[
                    "Walk me through the implementation process",
                    "What metrics should I track?",
                    "How do I get my team on board?",
                    "What does the timeline look like?"
                ]
            )
        ]

        return AudienceAnalysis(
            generated_at=datetime.now().isoformat(),
            business_context=self.business_type,
            segments=segments,
            personas=personas,
            content_recommendations=[
                {
                    "segment": "Growth-Stage Founders",
                    "content_types": ["Case studies", "Quick wins", "Tool comparisons"],
                    "topics": ["AI automation ROI", "Founder productivity", "Scaling with AI"],
                    "frequency": "3x/week"
                },
                {
                    "segment": "Operations Leaders",
                    "content_types": ["Guides", "Webinars", "Templates"],
                    "topics": ["Process automation", "Change management", "Operations metrics"],
                    "frequency": "2x/week"
                }
            ],
            channel_strategy={
                "linkedin": {
                    "priority": "high",
                    "content_type": "Case studies, thought leadership",
                    "frequency": "Daily"
                },
                "twitter": {
                    "priority": "high",
                    "content_type": "Quick tips, threads, engagement",
                    "frequency": "3-5x daily"
                },
                "email": {
                    "priority": "medium",
                    "content_type": "Newsletter, case studies",
                    "frequency": "Weekly"
                },
                "youtube": {
                    "priority": "medium",
                    "content_type": "Tutorials, demos, interviews",
                    "frequency": "1-2x/week"
                }
            },
            messaging_guidelines=[
                "Lead with outcomes, not features",
                "Use specific numbers and timeframes",
                "Include social proof from similar companies",
                "Address implementation concerns upfront",
                "Make the next step clear and low-commitment"
            ]
        )

    def create_persona_brief(self, persona: AudiencePersona) -> str:
        """Create a quick reference brief for a persona."""
        return f"""
# {persona.name} - Quick Brief

**Role**: {persona.role} at {persona.company_size} {persona.industry} company

**Core Challenge**: {persona.daily_challenges[0]}

**Primary Goal**: {persona.goals[0]}

**Biggest Fear**: {persona.fears[0]}

**How to Reach Them**: {', '.join(persona.information_sources[:2])}

**What They Want to Hear**: {persona.messaging_tone}

**Example Quote**: "{persona.example_quotes[0]}"

**Content Format**: {', '.join(persona.content_format_preferences[:2])}
"""

    def to_dict(self, analysis: AudienceAnalysis) -> Dict:
        """Convert analysis to dictionary."""
        return {
            "generated_at": analysis.generated_at,
            "business_context": analysis.business_context,
            "segments": [asdict(s) for s in analysis.segments],
            "personas": [asdict(p) for p in analysis.personas],
            "content_recommendations": analysis.content_recommendations,
            "channel_strategy": analysis.channel_strategy,
            "messaging_guidelines": analysis.messaging_guidelines
        }


def main():
    """Run audience analysis."""
    import argparse

    parser = argparse.ArgumentParser(description="Analyze target audience")
    parser.add_argument("--target", default="small business owners interested in AI",
                       help="Target audience description")
    parser.add_argument("--business", default="AI consulting",
                       help="Your business type")
    parser.add_argument("--depth", choices=["basic", "detailed", "comprehensive"],
                       default="detailed", help="Analysis depth")
    parser.add_argument("--persona-brief", action="store_true",
                       help="Output persona quick briefs")
    parser.add_argument("--output", type=Path,
                       help="Output file for JSON")

    args = parser.parse_args()

    agent = AudienceAnalystAgent(business_type=args.business)
    analysis = agent.analyze_audience(
        target_description=args.target,
        depth=args.depth
    )

    print(f"\n👥 AUDIENCE ANALYSIS - {analysis.business_context}")
    print(f"Generated: {analysis.generated_at}")
    print("=" * 60)

    print(f"\n📊 SEGMENTS ({len(analysis.segments)}):\n")
    for segment in analysis.segments:
        print(f"🎯 {segment.name}")
        print(f"   {segment.description}")
        print(f"   Size: {segment.size_estimate}")
        print(f"   Engagement: {segment.engagement_level}")
        print(f"   Pain points: {', '.join(segment.pain_points[:2])}")
        print(f"   Channels: {', '.join(segment.preferred_channels[:3])}")
        print()

    print(f"👤 PERSONAS ({len(analysis.personas)}):\n")
    for persona in analysis.personas:
        if args.persona_brief:
            print(agent.create_persona_brief(persona))
        else:
            print(f"👤 {persona.name}")
            print(f"   {persona.role} at {persona.company_size} {persona.industry}")
            print(f"   Challenge: {persona.daily_challenges[0]}")
            print(f"   Goal: {persona.goals[0]}")
            print(f"   Tone: {persona.messaging_tone}")
            print()

    print("📝 MESSAGING GUIDELINES:\n")
    for guideline in analysis.messaging_guidelines:
        print(f"  • {guideline}")

    print("\n📣 CHANNEL STRATEGY:\n")
    for channel, strategy in analysis.channel_strategy.items():
        if strategy.get("priority"):
            print(f"  {channel}: {strategy['priority']} priority")
            print(f"    Content: {strategy.get('content_type', 'N/A')}")
            print(f"    Frequency: {strategy.get('frequency', 'N/A')}")

    if args.output:
        with open(args.output, "w") as f:
            json.dump(agent.to_dict(analysis), f, indent=2)
        print(f"\n✅ Analysis saved to {args.output}")


if __name__ == "__main__":
    main()
