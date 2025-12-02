#!/usr/bin/env python3
"""
Case Study Builder Agent

Helps research, structure, and build compelling case studies
from project data and client outcomes.
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
class ProjectData:
    """Raw project data for case study."""
    client_industry: str
    client_size: str
    challenge: str
    solution: str
    timeline: str
    results: List[Dict[str, str]]
    testimonial: Optional[str]
    technologies: List[str]


@dataclass
class CaseStudyOutline:
    """Structured case study outline."""
    title: str
    subtitle: str
    executive_summary: str
    sections: List[Dict]
    key_metrics: List[Dict]
    visuals_needed: List[str]
    seo_keywords: List[str]
    target_audience: str


@dataclass
class CaseStudyDraft:
    """Complete case study draft."""
    title: str
    metadata: Dict
    sections: Dict[str, str]
    pull_quotes: List[str]
    statistics_callouts: List[Dict]
    cta: str
    seo_title: str
    seo_description: str


class CaseStudyBuilderAgent:
    """Agent that builds compelling case studies from project data."""

    CASE_STUDY_TYPES = [
        "success_story",      # Traditional before/after
        "transformation",     # Focus on change journey
        "roi_focused",        # Heavy on numbers
        "problem_solution",   # Technical focus
        "interview_style"     # Q&A format
    ]

    def __init__(self):
        self.client = anthropic.Anthropic() if HAS_ANTHROPIC else None

    def create_outline(
        self,
        project_data: ProjectData,
        style: str = "success_story",
        length: str = "medium"
    ) -> CaseStudyOutline:
        """
        Create a case study outline from project data.

        Args:
            project_data: Raw project information
            style: Type of case study
            length: short/medium/long

        Returns:
            CaseStudyOutline
        """
        if not self.client:
            return self._generate_mock_outline(project_data, style)

        prompt = f"""You are a case study writer creating compelling B2B content.

Create a case study outline from this project data:

Industry: {project_data.client_industry}
Company Size: {project_data.client_size}
Challenge: {project_data.challenge}
Solution: {project_data.solution}
Timeline: {project_data.timeline}
Results: {json.dumps(project_data.results)}
Technologies: {', '.join(project_data.technologies)}
Testimonial: {project_data.testimonial or 'N/A'}

Style: {style}
Length: {length}

Return as JSON:
{{
    "title": "Compelling title",
    "subtitle": "Supporting subtitle",
    "executive_summary": "2-3 sentence summary",
    "sections": [
        {{
            "title": "Section title",
            "purpose": "What this section accomplishes",
            "key_points": [],
            "word_count": 0
        }}
    ],
    "key_metrics": [
        {{
            "metric": "Metric name",
            "value": "Value",
            "context": "Why it matters"
        }}
    ],
    "visuals_needed": [],
    "seo_keywords": [],
    "target_audience": "Who this case study is for"
}}
"""

        response = self.client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=2048,
            messages=[{"role": "user", "content": prompt}]
        )

        response_text = response.content[0].text
        json_match = re.search(r'\{[\s\S]*\}', response_text)

        if json_match:
            try:
                data = json.loads(json_match.group())
                return CaseStudyOutline(**data)
            except (json.JSONDecodeError, TypeError):
                pass

        return self._generate_mock_outline(project_data, style)

    def _generate_mock_outline(
        self,
        project_data: ProjectData,
        style: str
    ) -> CaseStudyOutline:
        """Generate mock outline when API unavailable."""
        return CaseStudyOutline(
            title=f"How a {project_data.client_size} {project_data.client_industry} Company Transformed with AI",
            subtitle=f"Achieving {project_data.results[0]['value'] if project_data.results else 'significant'} improvement in {project_data.timeline}",
            executive_summary=(
                f"A {project_data.client_size} company in the {project_data.client_industry} industry "
                f"faced {project_data.challenge}. Through implementing {project_data.solution}, "
                f"they achieved remarkable results including {project_data.results[0]['value'] if project_data.results else 'significant improvements'}."
            ),
            sections=[
                {
                    "title": "The Challenge",
                    "purpose": "Establish the problem and stakes",
                    "key_points": [
                        "Describe the business pain point",
                        "Quantify the impact of the problem",
                        "Show what was at stake"
                    ],
                    "word_count": 200
                },
                {
                    "title": "The Solution",
                    "purpose": "Explain the approach and implementation",
                    "key_points": [
                        "Overview of the solution",
                        "Implementation process",
                        "Key technologies used"
                    ],
                    "word_count": 300
                },
                {
                    "title": "The Results",
                    "purpose": "Showcase outcomes with data",
                    "key_points": [
                        "Primary metric improvements",
                        "Secondary benefits",
                        "Timeline to value"
                    ],
                    "word_count": 250
                },
                {
                    "title": "Key Learnings",
                    "purpose": "Provide actionable insights",
                    "key_points": [
                        "What made this successful",
                        "Advice for others",
                        "Future plans"
                    ],
                    "word_count": 150
                }
            ],
            key_metrics=[
                {
                    "metric": result.get("metric", "Key Metric"),
                    "value": result.get("value", "N/A"),
                    "context": "Impact on business operations"
                }
                for result in project_data.results[:3]
            ],
            visuals_needed=[
                "Before/after comparison graphic",
                "Timeline infographic",
                "Results chart/graph",
                "Client logo and quote"
            ],
            seo_keywords=[
                f"AI {project_data.client_industry}",
                "automation case study",
                f"{project_data.client_industry} technology",
                "digital transformation"
            ],
            target_audience=f"Decision makers in {project_data.client_industry} looking for AI solutions"
        )

    def write_draft(
        self,
        outline: CaseStudyOutline,
        tone: str = "professional"
    ) -> CaseStudyDraft:
        """
        Write a full case study draft from an outline.

        Args:
            outline: Case study outline
            tone: Writing tone

        Returns:
            CaseStudyDraft with full content
        """
        sections = {}

        # Generate each section
        for section in outline.sections:
            sections[section["title"]] = self._write_section(
                section["title"],
                section["key_points"],
                section.get("word_count", 200)
            )

        # Extract statistics for callouts
        stats_callouts = [
            {
                "stat": metric["value"],
                "label": metric["metric"],
                "context": metric.get("context", "")
            }
            for metric in outline.key_metrics
        ]

        return CaseStudyDraft(
            title=outline.title,
            metadata={
                "generated_at": datetime.now().isoformat(),
                "target_audience": outline.target_audience,
                "seo_keywords": outline.seo_keywords
            },
            sections=sections,
            pull_quotes=[
                "\"This transformation exceeded our expectations.\"",
                "\"We saw ROI within the first month.\""
            ],
            statistics_callouts=stats_callouts,
            cta="Ready to achieve similar results? Let's discuss your project.",
            seo_title=outline.title[:60],
            seo_description=outline.executive_summary[:160]
        )

    def _write_section(
        self,
        title: str,
        key_points: List[str],
        word_count: int
    ) -> str:
        """Write a section of the case study."""
        # In production, this would use the LLM
        points_text = "\n\n".join([f"**{point}**\n\n[Content about {point.lower()}]" for point in key_points])
        return f"## {title}\n\n{points_text}"

    def generate_variations(
        self,
        case_study: CaseStudyDraft,
        formats: List[str]
    ) -> Dict[str, str]:
        """
        Generate variations of a case study for different formats.

        Args:
            case_study: Original case study
            formats: List of formats (linkedin, twitter, email, etc.)

        Returns:
            Dict of format -> content
        """
        variations = {}

        for fmt in formats:
            if fmt == "linkedin":
                variations["linkedin"] = self._format_linkedin(case_study)
            elif fmt == "twitter":
                variations["twitter"] = self._format_twitter(case_study)
            elif fmt == "email":
                variations["email"] = self._format_email(case_study)
            elif fmt == "one_pager":
                variations["one_pager"] = self._format_one_pager(case_study)

        return variations

    def _format_linkedin(self, case_study: CaseStudyDraft) -> str:
        """Format case study for LinkedIn post."""
        stats = case_study.statistics_callouts[0] if case_study.statistics_callouts else {"stat": "significant", "label": "improvement"}

        return f"""🎯 Case Study: {case_study.title}

{stats['stat']} {stats['label']} - here's how we did it:

THE CHALLENGE:
Our client was struggling with [challenge]. This was costing them time and money.

THE SOLUTION:
We implemented [solution] focused on delivering quick wins while building for scale.

THE RESULTS:
📈 {stats['stat']} {stats['label']}
🚀 [Additional metric]
⏱️ ROI achieved in [timeframe]

Key lesson: [Key insight]

{case_study.cta}

#AI #Automation #CaseStudy #BusinessTransformation
"""

    def _format_twitter(self, case_study: CaseStudyDraft) -> str:
        """Format case study as Twitter thread."""
        stats = case_study.statistics_callouts[0] if case_study.statistics_callouts else {"stat": "significant", "label": "improvement"}

        return f"""🧵 Thread: {case_study.title}

1/ The Challenge:
[Client] was struggling with [challenge]. It was costing them [impact].

2/ The Solution:
We implemented [solution]. Here's the approach:
- Step 1
- Step 2
- Step 3

3/ The Results:
{stats['stat']} {stats['label']}
+ [Secondary result]
+ [Tertiary result]

4/ Key Learnings:
What made this work:
✅ [Learning 1]
✅ [Learning 2]
✅ [Learning 3]

5/ Want similar results?
{case_study.cta}

[Link to full case study]
"""

    def _format_email(self, case_study: CaseStudyDraft) -> str:
        """Format case study for email."""
        return f"""Subject: Case Study: {case_study.title}

Hi [Name],

I wanted to share a recent success story that might be relevant to your situation.

{case_study.seo_description}

Key Results:
{chr(10).join([f"• {s['stat']} {s['label']}" for s in case_study.statistics_callouts])}

Would you like to discuss how we could achieve similar results for [Company]?

[Read the full case study →]

Best,
[Your name]
"""

    def _format_one_pager(self, case_study: CaseStudyDraft) -> str:
        """Format case study as one-page summary."""
        return f"""# {case_study.title}

## At a Glance
{case_study.seo_description}

## Key Metrics
{chr(10).join([f"**{s['stat']}** {s['label']}" for s in case_study.statistics_callouts])}

## The Challenge
[Brief challenge description]

## The Solution
[Brief solution description]

## Results & Impact
[Results summary with key stats]

## Client Testimonial
> {case_study.pull_quotes[0] if case_study.pull_quotes else "Excellent results."}

---
{case_study.cta}
"""


def main():
    """Run case study builder."""
    import argparse

    parser = argparse.ArgumentParser(description="Build case studies")
    parser.add_argument("--industry", default="Healthcare",
                       help="Client industry")
    parser.add_argument("--size", default="Mid-market",
                       help="Company size")
    parser.add_argument("--style", choices=CaseStudyBuilderAgent.CASE_STUDY_TYPES,
                       default="success_story", help="Case study style")
    parser.add_argument("--formats", nargs="+",
                       default=["linkedin", "email"],
                       help="Output formats to generate")
    parser.add_argument("--output", type=Path,
                       help="Output file")

    args = parser.parse_args()

    # Sample project data
    project_data = ProjectData(
        client_industry=args.industry,
        client_size=args.size,
        challenge="High call volume overwhelming reception staff, missed calls leading to lost appointments",
        solution="AI-powered voice receptionist with appointment scheduling integration",
        timeline="6 weeks",
        results=[
            {"metric": "Call handling capacity", "value": "200% increase"},
            {"metric": "Missed calls", "value": "95% reduction"},
            {"metric": "Cost per call", "value": "60% decrease"},
            {"metric": "Patient satisfaction", "value": "4.8/5 rating"}
        ],
        testimonial="The AI receptionist transformed how we handle patient calls. It's like having a 24/7 reception team.",
        technologies=["Voice AI", "Calendar API", "Custom integrations"]
    )

    agent = CaseStudyBuilderAgent()

    # Create outline
    print("\n📋 CREATING CASE STUDY OUTLINE\n")
    outline = agent.create_outline(project_data, style=args.style)

    print(f"Title: {outline.title}")
    print(f"Subtitle: {outline.subtitle}")
    print(f"\nExecutive Summary:\n{outline.executive_summary}")

    print(f"\n📑 SECTIONS ({len(outline.sections)}):")
    for section in outline.sections:
        print(f"  • {section['title']} (~{section.get('word_count', 0)} words)")

    print(f"\n📊 KEY METRICS:")
    for metric in outline.key_metrics:
        print(f"  • {metric['value']} - {metric['metric']}")

    # Write draft
    print("\n\n📝 WRITING DRAFT...\n")
    draft = agent.write_draft(outline)

    # Generate format variations
    print(f"📤 GENERATING FORMATS: {', '.join(args.formats)}\n")
    variations = agent.generate_variations(draft, args.formats)

    for fmt, content in variations.items():
        print(f"\n{'='*60}")
        print(f"FORMAT: {fmt.upper()}")
        print("="*60)
        print(content[:500] + "..." if len(content) > 500 else content)

    if args.output:
        output_data = {
            "outline": asdict(outline) if hasattr(outline, '__dataclass_fields__') else {
                "title": outline.title,
                "subtitle": outline.subtitle,
                "executive_summary": outline.executive_summary,
                "sections": outline.sections,
                "key_metrics": outline.key_metrics,
                "seo_keywords": outline.seo_keywords
            },
            "draft": {
                "title": draft.title,
                "metadata": draft.metadata,
                "sections": draft.sections,
                "cta": draft.cta
            },
            "variations": variations
        }
        with open(args.output, "w") as f:
            json.dump(output_data, f, indent=2)
        print(f"\n✅ Saved to {args.output}")


if __name__ == "__main__":
    main()
