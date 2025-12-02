#!/usr/bin/env python3
"""
Tech Stack Hunter Agent

Researches and catalogs technology stacks, tools, and frameworks
relevant to AI consulting and automation projects.
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
class Technology:
    """A technology or tool."""
    name: str
    category: str  # "llm", "framework", "database", "infrastructure", "tool"
    description: str
    use_cases: List[str]
    pros: List[str]
    cons: List[str]
    pricing_model: str
    learning_curve: str  # "low", "medium", "high"
    maturity: str  # "emerging", "growing", "mature", "declining"
    alternatives: List[str]
    integration_difficulty: str
    documentation_quality: str
    community_size: str
    official_url: str


@dataclass
class TechStack:
    """A recommended technology stack."""
    name: str
    use_case: str
    components: Dict[str, str]  # category -> technology
    estimated_cost: str
    setup_time: str
    maintenance_level: str
    scalability: str
    notes: str


class TechStackHunterAgent:
    """Agent that researches and recommends technology stacks."""

    CATEGORIES = [
        "llm_providers",
        "vector_databases",
        "frameworks",
        "orchestration",
        "deployment",
        "monitoring",
        "security",
        "integrations"
    ]

    def __init__(self):
        self.client = anthropic.Anthropic() if HAS_ANTHROPIC else None
        self.tech_catalog: Dict[str, Technology] = {}
        self._load_known_tech()

    def _load_known_tech(self):
        """Load known technologies into catalog."""
        known_tech = [
            Technology(
                name="Claude API",
                category="llm_providers",
                description="Anthropic's Claude models via API",
                use_cases=["Conversational AI", "Analysis", "Code generation", "Content creation"],
                pros=["Strong reasoning", "Long context", "Safe outputs", "Great for complex tasks"],
                cons=["API-only", "Higher cost for large volume", "Rate limits"],
                pricing_model="Per token (input/output)",
                learning_curve="low",
                maturity="mature",
                alternatives=["OpenAI GPT-4", "Google Gemini", "Mistral"],
                integration_difficulty="low",
                documentation_quality="excellent",
                community_size="large",
                official_url="https://anthropic.com"
            ),
            Technology(
                name="OpenAI GPT-4",
                category="llm_providers",
                description="OpenAI's GPT-4 and GPT-4o models",
                use_cases=["General AI tasks", "Function calling", "Vision", "Code"],
                pros=["Versatile", "Strong ecosystem", "Function calling", "Vision support"],
                cons=["Expensive at scale", "Rate limits", "Data privacy concerns"],
                pricing_model="Per token",
                learning_curve="low",
                maturity="mature",
                alternatives=["Claude API", "Google Gemini", "Llama"],
                integration_difficulty="low",
                documentation_quality="excellent",
                community_size="very large",
                official_url="https://openai.com"
            ),
            Technology(
                name="Qdrant",
                category="vector_databases",
                description="High-performance vector database",
                use_cases=["Semantic search", "RAG", "Recommendations", "Similarity matching"],
                pros=["Fast", "Filtering support", "Easy to deploy", "Rust-based"],
                cons=["Newer than alternatives", "Smaller community"],
                pricing_model="Free/Cloud pricing",
                learning_curve="low",
                maturity="growing",
                alternatives=["Pinecone", "Weaviate", "Milvus", "ChromaDB"],
                integration_difficulty="low",
                documentation_quality="good",
                community_size="medium",
                official_url="https://qdrant.tech"
            ),
            Technology(
                name="LangChain",
                category="frameworks",
                description="Framework for LLM application development",
                use_cases=["Chains", "Agents", "RAG pipelines", "Tool integration"],
                pros=["Feature-rich", "Large ecosystem", "Many integrations"],
                cons=["Complex", "Rapidly changing API", "Over-abstraction"],
                pricing_model="Open source",
                learning_curve="medium",
                maturity="growing",
                alternatives=["LlamaIndex", "Haystack", "Custom"],
                integration_difficulty="medium",
                documentation_quality="good",
                community_size="very large",
                official_url="https://langchain.com"
            ),
            Technology(
                name="n8n",
                category="orchestration",
                description="Workflow automation platform",
                use_cases=["Process automation", "Integrations", "Scheduled tasks", "Data pipelines"],
                pros=["Visual builder", "Self-hostable", "Extensible", "AI nodes"],
                cons=["Can be complex", "Performance at scale", "Learning curve"],
                pricing_model="Open source / Cloud",
                learning_curve="medium",
                maturity="mature",
                alternatives=["Make", "Zapier", "Temporal"],
                integration_difficulty="low",
                documentation_quality="good",
                community_size="large",
                official_url="https://n8n.io"
            ),
            Technology(
                name="FastAPI",
                category="frameworks",
                description="Modern Python web framework",
                use_cases=["APIs", "Microservices", "ML serving", "Webhooks"],
                pros=["Fast", "Auto docs", "Type hints", "Async support"],
                cons=["Python only", "Newer ecosystem"],
                pricing_model="Open source",
                learning_curve="low",
                maturity="mature",
                alternatives=["Flask", "Django", "Express"],
                integration_difficulty="low",
                documentation_quality="excellent",
                community_size="large",
                official_url="https://fastapi.tiangolo.com"
            ),
            Technology(
                name="Vercel",
                category="deployment",
                description="Frontend cloud platform",
                use_cases=["Web apps", "Serverless functions", "Edge computing"],
                pros=["Easy deployment", "Great DX", "Edge network", "Preview deploys"],
                cons=["Vendor lock-in", "Cost at scale", "Limited backend"],
                pricing_model="Free tier / Usage-based",
                learning_curve="low",
                maturity="mature",
                alternatives=["Netlify", "Railway", "Fly.io"],
                integration_difficulty="low",
                documentation_quality="excellent",
                community_size="very large",
                official_url="https://vercel.com"
            ),
            Technology(
                name="Supabase",
                category="database",
                description="Open source Firebase alternative",
                use_cases=["Auth", "Database", "Storage", "Realtime"],
                pros=["PostgreSQL", "Open source", "Good DX", "Generous free tier"],
                cons=["Scaling complexity", "Some features beta"],
                pricing_model="Free tier / Usage-based",
                learning_curve="low",
                maturity="growing",
                alternatives=["Firebase", "PlanetScale", "Neon"],
                integration_difficulty="low",
                documentation_quality="good",
                community_size="large",
                official_url="https://supabase.com"
            )
        ]

        for tech in known_tech:
            self.tech_catalog[tech.name.lower()] = tech

    def search_technologies(
        self,
        category: Optional[str] = None,
        use_case: Optional[str] = None,
        max_learning_curve: str = "high"
    ) -> List[Technology]:
        """Search technologies by criteria."""
        results = []

        curve_order = {"low": 1, "medium": 2, "high": 3}
        max_curve = curve_order.get(max_learning_curve, 3)

        for tech in self.tech_catalog.values():
            if category and tech.category != category:
                continue

            tech_curve = curve_order.get(tech.learning_curve, 3)
            if tech_curve > max_curve:
                continue

            if use_case:
                if not any(use_case.lower() in uc.lower() for uc in tech.use_cases):
                    continue

            results.append(tech)

        return results

    def recommend_stack(
        self,
        project_type: str,
        requirements: List[str],
        budget: str = "medium",
        team_size: str = "small"
    ) -> TechStack:
        """Recommend a technology stack for a project."""

        if not self.client:
            return self._get_default_stack(project_type)

        prompt = f"""You are a technical architect specializing in AI and automation projects.

Recommend a technology stack for:
- Project type: {project_type}
- Requirements: {', '.join(requirements)}
- Budget: {budget}
- Team size: {team_size}

Consider these categories:
- LLM Provider (Claude, OpenAI, etc.)
- Vector Database (if needed)
- Framework (LangChain, custom, etc.)
- Backend (FastAPI, Node, etc.)
- Database
- Deployment platform
- Monitoring

Return JSON:
{{
    "name": "Stack name",
    "use_case": "What this stack is for",
    "components": {{
        "llm": "Provider name",
        "vector_db": "Database name or null",
        "framework": "Framework name",
        "backend": "Backend framework",
        "database": "Database",
        "deployment": "Platform",
        "monitoring": "Tool"
    }},
    "estimated_cost": "Monthly estimate",
    "setup_time": "Time to set up",
    "maintenance_level": "low/medium/high",
    "scalability": "Description",
    "notes": "Important considerations"
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
                return TechStack(**data)
            except (json.JSONDecodeError, TypeError):
                pass

        return self._get_default_stack(project_type)

    def _get_default_stack(self, project_type: str) -> TechStack:
        """Return a sensible default stack."""
        stacks = {
            "ai_chatbot": TechStack(
                name="AI Chatbot Stack",
                use_case="Building conversational AI applications",
                components={
                    "llm": "Claude API",
                    "vector_db": "Qdrant",
                    "framework": "LangChain",
                    "backend": "FastAPI",
                    "database": "Supabase",
                    "deployment": "Railway",
                    "monitoring": "Langfuse"
                },
                estimated_cost="$50-200/month",
                setup_time="1-2 weeks",
                maintenance_level="medium",
                scalability="Good for 10K+ daily users",
                notes="Consider Claude for complex reasoning, add caching for cost control"
            ),
            "voice_ai": TechStack(
                name="Voice AI Reception Stack",
                use_case="AI-powered phone reception and call handling",
                components={
                    "llm": "Claude API + Whisper",
                    "vector_db": "Qdrant",
                    "framework": "Custom",
                    "backend": "FastAPI",
                    "database": "PostgreSQL",
                    "deployment": "Railway",
                    "monitoring": "Custom + Sentry"
                },
                estimated_cost="$100-500/month",
                setup_time="2-4 weeks",
                maintenance_level="medium",
                scalability="Handles 1000+ calls/day",
                notes="Latency critical - optimize for speed, consider regional deployment"
            ),
            "automation": TechStack(
                name="Business Automation Stack",
                use_case="Workflow automation and process optimization",
                components={
                    "llm": "Claude Haiku (speed) + Sonnet (quality)",
                    "vector_db": None,
                    "framework": "n8n",
                    "backend": "n8n + webhooks",
                    "database": "Supabase",
                    "deployment": "Self-hosted / n8n Cloud",
                    "monitoring": "n8n built-in"
                },
                estimated_cost="$0-100/month",
                setup_time="1-2 weeks",
                maintenance_level="low",
                scalability="Good for most SMB needs",
                notes="Start with n8n for rapid iteration, migrate to custom if needed"
            )
        }

        return stacks.get(project_type, stacks["ai_chatbot"])

    def compare_technologies(self, tech_names: List[str]) -> Dict:
        """Compare multiple technologies side by side."""
        comparison = {
            "technologies": [],
            "recommendation": "",
            "comparison_matrix": {}
        }

        for name in tech_names:
            tech = self.tech_catalog.get(name.lower())
            if tech:
                comparison["technologies"].append(asdict(tech))

        if len(comparison["technologies"]) >= 2:
            # Build comparison matrix
            criteria = ["learning_curve", "maturity", "integration_difficulty",
                       "documentation_quality", "community_size"]

            for criterion in criteria:
                comparison["comparison_matrix"][criterion] = {
                    tech["name"]: tech.get(criterion, "N/A")
                    for tech in comparison["technologies"]
                }

        return comparison


def main():
    """Run tech stack hunter."""
    import argparse

    parser = argparse.ArgumentParser(description="Hunt for technology stacks")
    parser.add_argument("--project-type",
                       choices=["ai_chatbot", "voice_ai", "automation", "custom"],
                       default="ai_chatbot",
                       help="Type of project")
    parser.add_argument("--requirements", nargs="+",
                       default=["conversational ai", "knowledge base"],
                       help="Project requirements")
    parser.add_argument("--budget", choices=["low", "medium", "high"],
                       default="medium", help="Budget level")
    parser.add_argument("--list-category", help="List technologies in category")
    parser.add_argument("--compare", nargs="+", help="Compare technologies")
    parser.add_argument("--output", type=Path, help="Output file")

    args = parser.parse_args()

    agent = TechStackHunterAgent()

    if args.list_category:
        techs = agent.search_technologies(category=args.list_category)
        print(f"\n🔧 Technologies in '{args.list_category}':\n")
        for tech in techs:
            print(f"  {tech.name}")
            print(f"    {tech.description}")
            print(f"    Maturity: {tech.maturity} | Learning: {tech.learning_curve}")
            print()
        return

    if args.compare:
        comparison = agent.compare_technologies(args.compare)
        print(f"\n📊 TECHNOLOGY COMPARISON\n")
        print("=" * 60)
        for tech in comparison["technologies"]:
            print(f"\n{tech['name']}")
            print(f"  Category: {tech['category']}")
            print(f"  Pros: {', '.join(tech['pros'][:3])}")
            print(f"  Cons: {', '.join(tech['cons'][:2])}")
        return

    # Recommend stack
    stack = agent.recommend_stack(
        project_type=args.project_type,
        requirements=args.requirements,
        budget=args.budget
    )

    print(f"\n🏗️ RECOMMENDED STACK: {stack.name}")
    print("=" * 60)
    print(f"Use case: {stack.use_case}\n")

    print("Components:")
    for category, tech in stack.components.items():
        if tech:
            print(f"  {category}: {tech}")

    print(f"\n💰 Estimated cost: {stack.estimated_cost}")
    print(f"⏱️ Setup time: {stack.setup_time}")
    print(f"🔧 Maintenance: {stack.maintenance_level}")
    print(f"📈 Scalability: {stack.scalability}")
    print(f"\n📝 Notes: {stack.notes}")

    if args.output:
        with open(args.output, "w") as f:
            json.dump(asdict(stack), f, indent=2)
        print(f"\n✅ Stack saved to {args.output}")


if __name__ == "__main__":
    main()
