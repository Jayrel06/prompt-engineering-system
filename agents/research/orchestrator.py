#!/usr/bin/env python3
"""
Research Orchestrator

Coordinates multiple research agents to perform comprehensive
research tasks and generate unified reports.
"""

import os
import json
import asyncio
from datetime import datetime
from typing import List, Dict, Optional, Any
from dataclasses import dataclass, asdict
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed

# Import all agents
from .trend_scout import TrendScoutAgent
from .tech_stack_hunter import TechStackHunterAgent
from .competitor_monitor import CompetitorMonitorAgent
from .content_curator import ContentCuratorAgent
from .audience_analyst import AudienceAnalystAgent
from .data_miner import DataMinerAgent
from .keyword_researcher import KeywordResearcherAgent
from .social_listener import SocialListenerAgent
from .case_study_builder import CaseStudyBuilderAgent, ProjectData
from .content_ideator import ContentIdeatorAgent
from .expert_finder import ExpertFinderAgent
from .format_adapter import FormatAdapterAgent


@dataclass
class ResearchTask:
    """A research task to execute."""
    agent_type: str
    method: str
    kwargs: Dict
    priority: int = 1


@dataclass
class ResearchResult:
    """Result from a research agent."""
    agent_type: str
    method: str
    success: bool
    data: Any
    error: Optional[str]
    execution_time: float


@dataclass
class OrchestratedReport:
    """Combined report from multiple agents."""
    generated_at: str
    research_topic: str
    agents_used: List[str]
    results: Dict[str, Any]
    insights: List[str]
    recommendations: List[str]
    next_steps: List[str]


class ResearchOrchestrator:
    """
    Orchestrates multiple research agents for comprehensive analysis.

    Usage:
        orchestrator = ResearchOrchestrator()
        report = orchestrator.full_research("AI automation for small business")
    """

    def __init__(self, industry: str = "AI consulting"):
        self.industry = industry
        self.agents = {
            "trend_scout": TrendScoutAgent(industry=industry),
            "tech_stack": TechStackHunterAgent(),
            "competitor": CompetitorMonitorAgent(industry=industry),
            "content_curator": ContentCuratorAgent(),
            "audience": AudienceAnalystAgent(business_type=industry),
            "data_miner": DataMinerAgent(),
            "keyword": KeywordResearcherAgent(domain=industry),
            "social": SocialListenerAgent(),
            "case_study": CaseStudyBuilderAgent(),
            "ideator": ContentIdeatorAgent(),
            "expert": ExpertFinderAgent(domain=industry),
            "format": FormatAdapterAgent()
        }

    def full_research(
        self,
        topic: str,
        include_agents: Optional[List[str]] = None,
        parallel: bool = True
    ) -> OrchestratedReport:
        """
        Perform comprehensive research using multiple agents.

        Args:
            topic: Research topic
            include_agents: Specific agents to use (default: all)
            parallel: Run agents in parallel

        Returns:
            OrchestratedReport with combined findings
        """
        include_agents = include_agents or list(self.agents.keys())

        # Define research tasks
        tasks = self._build_task_list(topic, include_agents)

        # Execute tasks
        if parallel:
            results = self._execute_parallel(tasks)
        else:
            results = self._execute_sequential(tasks)

        # Combine results
        return self._combine_results(topic, results)

    def _build_task_list(
        self,
        topic: str,
        include_agents: List[str]
    ) -> List[ResearchTask]:
        """Build list of research tasks to execute."""
        tasks = []

        if "trend_scout" in include_agents:
            tasks.append(ResearchTask(
                agent_type="trend_scout",
                method="analyze_trends",
                kwargs={"time_window": "7d"},
                priority=1
            ))

        if "keyword" in include_agents:
            tasks.append(ResearchTask(
                agent_type="keyword",
                method="research_keywords",
                kwargs={"seed_topic": topic, "depth": "comprehensive"},
                priority=1
            ))

        if "audience" in include_agents:
            tasks.append(ResearchTask(
                agent_type="audience",
                method="analyze_audience",
                kwargs={"target_description": f"People interested in {topic}"},
                priority=2
            ))

        if "competitor" in include_agents:
            tasks.append(ResearchTask(
                agent_type="competitor",
                method="analyze_market",
                kwargs={"focus_areas": ["content", "pricing", "positioning"]},
                priority=2
            ))

        if "social" in include_agents:
            tasks.append(ResearchTask(
                agent_type="social",
                method="listen",
                kwargs={"time_period": "24h"},
                priority=1
            ))

        if "content_curator" in include_agents:
            tasks.append(ResearchTask(
                agent_type="content_curator",
                method="curate_content",
                kwargs={"theme": topic, "max_items": 10},
                priority=2
            ))

        if "data_miner" in include_agents:
            tasks.append(ResearchTask(
                agent_type="data_miner",
                method="mine_data",
                kwargs={"query": topic},
                priority=2
            ))

        if "ideator" in include_agents:
            tasks.append(ResearchTask(
                agent_type="ideator",
                method="generate_ideas",
                kwargs={"topic": topic, "count": 10},
                priority=3
            ))

        if "expert" in include_agents:
            tasks.append(ResearchTask(
                agent_type="expert",
                method="find_experts",
                kwargs={"query": topic},
                priority=3
            ))

        # Sort by priority
        tasks.sort(key=lambda t: t.priority)

        return tasks

    def _execute_task(self, task: ResearchTask) -> ResearchResult:
        """Execute a single research task."""
        import time
        start = time.time()

        try:
            agent = self.agents.get(task.agent_type)
            if not agent:
                raise ValueError(f"Unknown agent: {task.agent_type}")

            method = getattr(agent, task.method)
            result = method(**task.kwargs)

            return ResearchResult(
                agent_type=task.agent_type,
                method=task.method,
                success=True,
                data=result,
                error=None,
                execution_time=time.time() - start
            )

        except Exception as e:
            return ResearchResult(
                agent_type=task.agent_type,
                method=task.method,
                success=False,
                data=None,
                error=str(e),
                execution_time=time.time() - start
            )

    def _execute_parallel(self, tasks: List[ResearchTask]) -> List[ResearchResult]:
        """Execute tasks in parallel."""
        results = []

        with ThreadPoolExecutor(max_workers=6) as executor:
            futures = {executor.submit(self._execute_task, task): task for task in tasks}

            for future in as_completed(futures):
                results.append(future.result())

        return results

    def _execute_sequential(self, tasks: List[ResearchTask]) -> List[ResearchResult]:
        """Execute tasks sequentially."""
        return [self._execute_task(task) for task in tasks]

    def _combine_results(
        self,
        topic: str,
        results: List[ResearchResult]
    ) -> OrchestratedReport:
        """Combine results from multiple agents into unified report."""
        combined_data = {}
        agents_used = []
        all_insights = []
        all_recommendations = []

        for result in results:
            agents_used.append(result.agent_type)

            if not result.success:
                combined_data[result.agent_type] = {"error": result.error}
                continue

            # Extract key data based on agent type
            if result.agent_type == "trend_scout" and result.data:
                combined_data["trends"] = {
                    "count": len(result.data.trends),
                    "top_trends": [
                        {"topic": t.topic, "growth": t.growth_rate, "relevance": t.relevance_to_ai}
                        for t in result.data.trends[:5]
                    ],
                    "opportunities": result.data.top_opportunities
                }
                all_recommendations.extend(result.data.recommended_actions)

            elif result.agent_type == "keyword" and result.data:
                combined_data["keywords"] = {
                    "clusters": len(result.data.clusters),
                    "top_opportunities": [
                        {"keyword": k.keyword, "volume": k.search_volume, "difficulty": k.difficulty}
                        for k in result.data.top_opportunities[:5]
                    ],
                    "quick_wins": result.data.quick_wins
                }

            elif result.agent_type == "audience" and result.data:
                combined_data["audience"] = {
                    "segments": len(result.data.segments),
                    "personas": len(result.data.personas),
                    "channel_strategy": result.data.channel_strategy,
                    "messaging_guidelines": result.data.messaging_guidelines
                }
                all_recommendations.extend(result.data.messaging_guidelines)

            elif result.agent_type == "competitor" and result.data:
                combined_data["competitors"] = {
                    "count": len(result.data.competitors),
                    "market_gaps": result.data.market_gaps,
                    "opportunities": result.data.opportunities,
                    "threats": result.data.threats
                }
                all_insights.extend(result.data.market_gaps)

            elif result.agent_type == "social" and result.data:
                combined_data["social"] = {
                    "total_mentions": result.data.total_mentions,
                    "sentiment": result.data.sentiment_summary,
                    "trending_topics": result.data.trending_topics,
                    "engagement_opportunities": result.data.engagement_opportunities,
                    "content_ideas": result.data.content_ideas
                }
                all_insights.extend(result.data.content_ideas[:3])

            elif result.agent_type == "data_miner" and result.data:
                combined_data["data"] = {
                    "key_metrics": result.data.key_metrics,
                    "insights_count": len(result.data.insights)
                }
                all_recommendations.extend(result.data.recommendations)

            elif result.agent_type == "ideator" and result.data:
                combined_data["content_ideas"] = {
                    "ideas_count": len(result.data.ideas),
                    "top_ideas": [
                        {"title": i.title, "format": i.format, "priority": i.priority_score}
                        for i in result.data.ideas[:5]
                    ],
                    "quick_wins": result.data.quick_wins,
                    "evergreen": result.data.evergreen_ideas
                }

            elif result.agent_type == "expert" and result.data:
                combined_data["experts"] = {
                    "found": len(result.data.top_experts),
                    "top_experts": [
                        {"name": e.name, "relevance": e.relevance_score, "collab_potential": e.collaboration_potential}
                        for e in result.data.top_experts[:5]
                    ],
                    "collaboration_opportunities": result.data.collaboration_opportunities
                }

        # Generate next steps
        next_steps = self._generate_next_steps(combined_data)

        return OrchestratedReport(
            generated_at=datetime.now().isoformat(),
            research_topic=topic,
            agents_used=agents_used,
            results=combined_data,
            insights=list(set(all_insights))[:10],
            recommendations=list(set(all_recommendations))[:10],
            next_steps=next_steps
        )

    def _generate_next_steps(self, data: Dict) -> List[str]:
        """Generate recommended next steps based on research."""
        steps = []

        if "keywords" in data:
            steps.append("Create content targeting top keyword opportunities")

        if "trends" in data:
            steps.append("Develop content around rising trends")

        if "audience" in data:
            steps.append("Review messaging guidelines for upcoming content")

        if "competitors" in data:
            steps.append("Address identified market gaps")

        if "social" in data:
            steps.append("Engage with high-priority social opportunities")

        if "content_ideas" in data:
            steps.append("Schedule quick-win content pieces")

        if "experts" in data:
            steps.append("Reach out to high-potential collaboration targets")

        return steps

    def quick_research(self, topic: str) -> Dict:
        """
        Perform quick research using essential agents only.

        Args:
            topic: Research topic

        Returns:
            Dict with key findings
        """
        essential = ["trend_scout", "keyword", "social"]
        report = self.full_research(topic, include_agents=essential, parallel=True)

        return {
            "topic": topic,
            "trends": report.results.get("trends", {}),
            "keywords": report.results.get("keywords", {}),
            "social": report.results.get("social", {}),
            "recommendations": report.recommendations[:5]
        }

    def content_research(self, topic: str) -> Dict:
        """
        Research focused on content creation.

        Args:
            topic: Content topic

        Returns:
            Dict with content-focused findings
        """
        content_agents = ["keyword", "audience", "ideator", "content_curator", "social"]
        report = self.full_research(topic, include_agents=content_agents, parallel=True)

        return {
            "topic": topic,
            "keywords": report.results.get("keywords", {}),
            "audience": report.results.get("audience", {}),
            "ideas": report.results.get("content_ideas", {}),
            "recommendations": report.recommendations
        }

    def competitive_research(self, topic: str) -> Dict:
        """
        Research focused on competitive analysis.

        Args:
            topic: Market/topic to analyze

        Returns:
            Dict with competitive findings
        """
        comp_agents = ["competitor", "trend_scout", "expert", "data_miner"]
        report = self.full_research(topic, include_agents=comp_agents, parallel=True)

        return {
            "topic": topic,
            "competitors": report.results.get("competitors", {}),
            "trends": report.results.get("trends", {}),
            "experts": report.results.get("experts", {}),
            "data": report.results.get("data", {}),
            "recommendations": report.recommendations
        }

    def to_dict(self, report: OrchestratedReport) -> Dict:
        """Convert report to dictionary."""
        return asdict(report)

    def save_report(self, report: OrchestratedReport, output_path: Path):
        """Save report to file."""
        with open(output_path, "w") as f:
            json.dump(self.to_dict(report), f, indent=2, default=str)


def main():
    """Run research orchestrator."""
    import argparse

    parser = argparse.ArgumentParser(description="Orchestrate research agents")
    parser.add_argument("topic", nargs="?", default="AI automation for small business",
                       help="Research topic")
    parser.add_argument("--mode", choices=["full", "quick", "content", "competitive"],
                       default="quick", help="Research mode")
    parser.add_argument("--agents", nargs="+",
                       help="Specific agents to use")
    parser.add_argument("--sequential", action="store_true",
                       help="Run agents sequentially instead of parallel")
    parser.add_argument("--output", type=Path,
                       help="Output file for JSON report")

    args = parser.parse_args()

    orchestrator = ResearchOrchestrator()

    print(f"\n🔬 RESEARCH ORCHESTRATOR")
    print(f"Topic: {args.topic}")
    print(f"Mode: {args.mode}")
    print("=" * 60)

    if args.mode == "full":
        print("\n🚀 Running full research (this may take a moment)...\n")
        report = orchestrator.full_research(
            args.topic,
            include_agents=args.agents,
            parallel=not args.sequential
        )
    elif args.mode == "quick":
        print("\n⚡ Running quick research...\n")
        result = orchestrator.quick_research(args.topic)
        print(json.dumps(result, indent=2, default=str))
        return
    elif args.mode == "content":
        print("\n📝 Running content research...\n")
        result = orchestrator.content_research(args.topic)
        print(json.dumps(result, indent=2, default=str))
        return
    elif args.mode == "competitive":
        print("\n🔍 Running competitive research...\n")
        result = orchestrator.competitive_research(args.topic)
        print(json.dumps(result, indent=2, default=str))
        return

    # Display full report
    print(f"Generated: {report.generated_at}")
    print(f"Agents used: {', '.join(report.agents_used)}")

    print("\n📊 RESULTS SUMMARY:\n")
    for agent, data in report.results.items():
        print(f"  {agent}:")
        if isinstance(data, dict):
            for key, value in list(data.items())[:3]:
                print(f"    {key}: {value}")
        print()

    print("💡 KEY INSIGHTS:\n")
    for insight in report.insights[:5]:
        print(f"  • {insight}")

    print("\n📋 RECOMMENDATIONS:\n")
    for rec in report.recommendations[:5]:
        print(f"  ☐ {rec}")

    print("\n➡️ NEXT STEPS:\n")
    for step in report.next_steps:
        print(f"  → {step}")

    if args.output:
        orchestrator.save_report(report, args.output)
        print(f"\n✅ Report saved to {args.output}")


if __name__ == "__main__":
    main()
