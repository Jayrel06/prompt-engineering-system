"""
Research Agent System

A collection of specialized agents for content research, trend analysis,
competitor monitoring, and content strategy development.

Agents:
- TrendScoutAgent: Monitors emerging trends across platforms
- TechStackHunterAgent: Researches technology stacks and tools
- CompetitorMonitorAgent: Tracks competitor activities
- ContentCuratorAgent: Curates relevant content from sources
- AudienceAnalystAgent: Analyzes and segments target audiences
- DataMinerAgent: Extracts insights from data sources
- KeywordResearcherAgent: Researches SEO keywords
- SocialListenerAgent: Monitors social media conversations
- CaseStudyBuilderAgent: Creates case studies from project data
- ContentIdeatorAgent: Generates content ideas
- ExpertFinderAgent: Finds and profiles domain experts
- FormatAdapterAgent: Adapts content for different platforms
"""

from .trend_scout import TrendScoutAgent, Trend, TrendReport
from .tech_stack_hunter import TechStackHunterAgent, Technology, TechStack
from .competitor_monitor import CompetitorMonitorAgent, Competitor, MarketAnalysis
from .content_curator import ContentCuratorAgent, ContentItem, ContentBundle
from .audience_analyst import AudienceAnalystAgent, AudienceSegment, AudiencePersona
from .data_miner import DataMinerAgent, DataPoint, DataMiningReport
from .keyword_researcher import KeywordResearcherAgent, Keyword, KeywordCluster
from .social_listener import SocialListenerAgent, SocialMention, SocialListeningReport
from .case_study_builder import CaseStudyBuilderAgent, ProjectData, CaseStudyDraft
from .content_ideator import ContentIdeatorAgent, ContentIdea, IdeationSession
from .expert_finder import ExpertFinderAgent, Expert, ExpertNetwork
from .format_adapter import FormatAdapterAgent, AdaptedContent, ContentRepurposeBundle

__all__ = [
    # Agents
    "TrendScoutAgent",
    "TechStackHunterAgent",
    "CompetitorMonitorAgent",
    "ContentCuratorAgent",
    "AudienceAnalystAgent",
    "DataMinerAgent",
    "KeywordResearcherAgent",
    "SocialListenerAgent",
    "CaseStudyBuilderAgent",
    "ContentIdeatorAgent",
    "ExpertFinderAgent",
    "FormatAdapterAgent",
    # Data classes
    "Trend",
    "TrendReport",
    "Technology",
    "TechStack",
    "Competitor",
    "MarketAnalysis",
    "ContentItem",
    "ContentBundle",
    "AudienceSegment",
    "AudiencePersona",
    "DataPoint",
    "DataMiningReport",
    "Keyword",
    "KeywordCluster",
    "SocialMention",
    "SocialListeningReport",
    "ProjectData",
    "CaseStudyDraft",
    "ContentIdea",
    "IdeationSession",
    "Expert",
    "ExpertNetwork",
    "AdaptedContent",
    "ContentRepurposeBundle",
]
