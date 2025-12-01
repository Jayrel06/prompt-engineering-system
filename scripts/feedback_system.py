#!/usr/bin/env python3
"""
Feedback Capture and Learning Loop System

Captures user feedback on prompt outputs, analyzes patterns in successful vs failed
outputs, generates improvement reports, and suggests prompt modifications.

Features:
- Real-time feedback capture (thumbs up/down, 1-5 rating)
- SQLite database for persistent storage
- Pattern analysis on successful vs failed outputs
- Weekly improvement reports
- AI-powered prompt modification suggestions
- Integration with prompt router for continuous learning

Usage:
    feedback_system.py --capture --prompt "..." --output "..." [--rating 1-5] [--thumbs-up] [--tags tag1,tag2]
    feedback_system.py --analyze [--days 7] [--min-samples 5]
    feedback_system.py --report [--period weekly|monthly] [--output report.json]
    feedback_system.py --suggest [--framework chain-of-thought] [--limit 5]
    feedback_system.py init

Examples:
    # Capture positive feedback
    feedback_system.py --capture --prompt "Explain X" --output "Response..." --rating 5 --thumbs-up --tags "technical,explanation"

    # Analyze patterns
    feedback_system.py --analyze --days 30 --min-samples 10

    # Generate weekly report
    feedback_system.py --report --period weekly --output weekly_report.json

    # Get prompt suggestions
    feedback_system.py --suggest --framework chain-of-thought --limit 5
"""

import argparse
import sqlite3
import json
import sys
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, asdict, field
from collections import defaultdict, Counter
import hashlib
import re

try:
    import anthropic
    HAS_ANTHROPIC = True
except ImportError:
    HAS_ANTHROPIC = False

# Get project paths
SCRIPT_DIR = Path(__file__).parent
PROJECT_ROOT = SCRIPT_DIR.parent
DATA_DIR = PROJECT_ROOT / "data"
DB_PATH = DATA_DIR / "feedback.db"

# Rating thresholds
POSITIVE_RATING_THRESHOLD = 4  # Ratings >= 4 are considered positive
NEGATIVE_RATING_THRESHOLD = 2  # Ratings <= 2 are considered negative


@dataclass
class FeedbackEntry:
    """
    Represents a single feedback entry.

    Attributes:
        prompt: The original prompt text
        output: The generated output text
        rating: Numeric rating from 1-5 (1=very bad, 5=excellent)
        thumbs_up: Boolean thumbs up/down (True=up, False=down)
        tags: List of categorization tags
        timestamp: When the feedback was captured
        context: Additional context (model, framework, etc.)
        feedback_id: Unique identifier for this entry
        notes: Optional user notes about the feedback
    """
    prompt: str
    output: str
    rating: int
    thumbs_up: bool
    tags: List[str]
    timestamp: str
    context: Dict[str, Any]
    feedback_id: Optional[str] = None
    notes: Optional[str] = None

    def __post_init__(self):
        """Validate and generate ID if needed."""
        if not 1 <= self.rating <= 5:
            raise ValueError("Rating must be between 1 and 5")

        if self.feedback_id is None:
            # Generate unique ID based on content and timestamp
            content = f"{self.prompt}{self.output}{self.timestamp}"
            self.feedback_id = hashlib.md5(content.encode()).hexdigest()[:16]

    def is_positive(self) -> bool:
        """Check if feedback is positive."""
        return self.rating >= POSITIVE_RATING_THRESHOLD and self.thumbs_up

    def is_negative(self) -> bool:
        """Check if feedback is negative."""
        return self.rating <= NEGATIVE_RATING_THRESHOLD or not self.thumbs_up

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            'feedback_id': self.feedback_id,
            'prompt': self.prompt,
            'output': self.output,
            'rating': self.rating,
            'thumbs_up': self.thumbs_up,
            'tags': self.tags,
            'timestamp': self.timestamp,
            'context': self.context,
            'notes': self.notes
        }


@dataclass
class PatternAnalysis:
    """
    Results from analyzing feedback patterns.

    Attributes:
        total_feedback: Total number of feedback entries analyzed
        positive_count: Number of positive feedback entries
        negative_count: Number of negative feedback entries
        success_rate: Overall success rate (0-1)
        common_positive_patterns: Patterns found in successful outputs
        common_negative_patterns: Patterns found in failed outputs
        tag_performance: Performance metrics by tag
        framework_performance: Performance metrics by framework
        recommendations: List of actionable recommendations
    """
    total_feedback: int
    positive_count: int
    negative_count: int
    success_rate: float
    common_positive_patterns: List[Dict[str, Any]]
    common_negative_patterns: List[Dict[str, Any]]
    tag_performance: Dict[str, Dict[str, Any]]
    framework_performance: Dict[str, Dict[str, Any]]
    recommendations: List[str]
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return asdict(self)


@dataclass
class ImprovementReport:
    """
    Weekly/monthly improvement report.

    Attributes:
        period: Report period (e.g., "2024-W48", "2024-11")
        start_date: Period start date
        end_date: Period end date
        total_prompts: Total prompts in period
        avg_rating: Average rating
        success_rate: Success rate
        improvement_vs_previous: Improvement percentage vs previous period
        top_performers: Best performing prompts/frameworks
        problem_areas: Areas needing improvement
        action_items: Suggested actions
    """
    period: str
    start_date: str
    end_date: str
    total_prompts: int
    avg_rating: float
    success_rate: float
    improvement_vs_previous: Optional[float]
    top_performers: List[Dict[str, Any]]
    problem_areas: List[Dict[str, Any]]
    action_items: List[str]
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return asdict(self)


class FeedbackDatabase:
    """Manages the SQLite database for feedback storage."""

    def __init__(self, db_path: Path = DB_PATH):
        """Initialize database connection."""
        self.db_path = db_path
        self.db_path.parent.mkdir(parents=True, exist_ok=True)

    def get_connection(self) -> sqlite3.Connection:
        """Get database connection with row factory."""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def init_database(self) -> None:
        """Initialize database schema."""
        conn = self.get_connection()
        cursor = conn.cursor()

        # Main feedback table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS feedback (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                feedback_id TEXT UNIQUE NOT NULL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                prompt TEXT NOT NULL,
                output TEXT NOT NULL,
                rating INTEGER NOT NULL CHECK (rating BETWEEN 1 AND 5),
                thumbs_up BOOLEAN NOT NULL,
                tags TEXT,  -- JSON array
                context TEXT,  -- JSON object
                notes TEXT,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # Indexes for performance
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_feedback_timestamp
            ON feedback(timestamp)
        """)

        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_feedback_rating
            ON feedback(rating)
        """)

        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_feedback_thumbs_up
            ON feedback(thumbs_up)
        """)

        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_feedback_id
            ON feedback(feedback_id)
        """)

        # Pattern analysis cache table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS pattern_cache (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                analysis_date DATE NOT NULL,
                days_analyzed INTEGER NOT NULL,
                analysis_results TEXT NOT NULL,  -- JSON
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # Reports table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS reports (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                period TEXT NOT NULL,
                report_type TEXT NOT NULL,
                report_data TEXT NOT NULL,  -- JSON
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)

        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_reports_period
            ON reports(period)
        """)

        conn.commit()
        conn.close()

        print(f"Database initialized at: {self.db_path}")

    def insert_feedback(self, entry: FeedbackEntry) -> int:
        """
        Insert a feedback entry into the database.

        Args:
            entry: FeedbackEntry to insert

        Returns:
            ID of inserted row
        """
        conn = self.get_connection()
        cursor = conn.cursor()

        try:
            cursor.execute("""
                INSERT INTO feedback
                (feedback_id, timestamp, prompt, output, rating, thumbs_up, tags, context, notes)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                entry.feedback_id,
                entry.timestamp,
                entry.prompt,
                entry.output,
                entry.rating,
                1 if entry.thumbs_up else 0,
                json.dumps(entry.tags),
                json.dumps(entry.context),
                entry.notes
            ))

            row_id = cursor.lastrowid
            conn.commit()
            return row_id

        except sqlite3.IntegrityError as e:
            if "UNIQUE constraint failed" in str(e):
                raise ValueError(f"Feedback entry {entry.feedback_id} already exists")
            raise
        finally:
            conn.close()

    def get_feedback(
        self,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        min_rating: Optional[int] = None,
        max_rating: Optional[int] = None,
        thumbs_up: Optional[bool] = None,
        tags: Optional[List[str]] = None,
        limit: Optional[int] = None
    ) -> List[FeedbackEntry]:
        """
        Query feedback entries with filters.

        Args:
            start_date: Filter by start date (ISO format)
            end_date: Filter by end date (ISO format)
            min_rating: Minimum rating (1-5)
            max_rating: Maximum rating (1-5)
            thumbs_up: Filter by thumbs up/down
            tags: Filter by tags (entries must have all listed tags)
            limit: Maximum number of results

        Returns:
            List of FeedbackEntry objects
        """
        conn = self.get_connection()
        cursor = conn.cursor()

        where_clauses = []
        params = []

        if start_date:
            where_clauses.append("timestamp >= ?")
            params.append(start_date)

        if end_date:
            where_clauses.append("timestamp <= ?")
            params.append(end_date)

        if min_rating is not None:
            where_clauses.append("rating >= ?")
            params.append(min_rating)

        if max_rating is not None:
            where_clauses.append("rating <= ?")
            params.append(max_rating)

        if thumbs_up is not None:
            where_clauses.append("thumbs_up = ?")
            params.append(1 if thumbs_up else 0)

        where_sql = " AND ".join(where_clauses) if where_clauses else "1=1"
        limit_sql = f"LIMIT {limit}" if limit else ""

        cursor.execute(f"""
            SELECT feedback_id, timestamp, prompt, output, rating, thumbs_up, tags, context, notes
            FROM feedback
            WHERE {where_sql}
            ORDER BY timestamp DESC
            {limit_sql}
        """, params)

        entries = []
        for row in cursor.fetchall():
            tags_list = json.loads(row['tags']) if row['tags'] else []

            # Filter by tags if specified
            if tags and not all(tag in tags_list for tag in tags):
                continue

            entry = FeedbackEntry(
                feedback_id=row['feedback_id'],
                timestamp=row['timestamp'],
                prompt=row['prompt'],
                output=row['output'],
                rating=row['rating'],
                thumbs_up=bool(row['thumbs_up']),
                tags=tags_list,
                context=json.loads(row['context']) if row['context'] else {},
                notes=row['notes']
            )
            entries.append(entry)

        conn.close()
        return entries

    def get_statistics(
        self,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Get aggregate statistics for a date range.

        Args:
            start_date: Start date (ISO format)
            end_date: End date (ISO format)

        Returns:
            Dictionary with statistics
        """
        conn = self.get_connection()
        cursor = conn.cursor()

        where_clauses = []
        params = []

        if start_date:
            where_clauses.append("timestamp >= ?")
            params.append(start_date)

        if end_date:
            where_clauses.append("timestamp <= ?")
            params.append(end_date)

        where_sql = " AND ".join(where_clauses) if where_clauses else "1=1"

        cursor.execute(f"""
            SELECT
                COUNT(*) as total_count,
                AVG(rating) as avg_rating,
                SUM(CASE WHEN thumbs_up = 1 THEN 1 ELSE 0 END) as thumbs_up_count,
                SUM(CASE WHEN thumbs_up = 0 THEN 1 ELSE 0 END) as thumbs_down_count,
                SUM(CASE WHEN rating >= {POSITIVE_RATING_THRESHOLD} THEN 1 ELSE 0 END) as positive_count,
                SUM(CASE WHEN rating <= {NEGATIVE_RATING_THRESHOLD} THEN 1 ELSE 0 END) as negative_count,
                MIN(timestamp) as earliest,
                MAX(timestamp) as latest
            FROM feedback
            WHERE {where_sql}
        """, params)

        row = cursor.fetchone()
        conn.close()

        total = row['total_count'] or 0

        return {
            'total_count': total,
            'avg_rating': row['avg_rating'] or 0.0,
            'thumbs_up_count': row['thumbs_up_count'] or 0,
            'thumbs_down_count': row['thumbs_down_count'] or 0,
            'positive_count': row['positive_count'] or 0,
            'negative_count': row['negative_count'] or 0,
            'success_rate': (row['positive_count'] or 0) / total if total > 0 else 0.0,
            'earliest': row['earliest'],
            'latest': row['latest']
        }

    def cache_analysis(self, days: int, analysis: PatternAnalysis) -> None:
        """Cache pattern analysis results."""
        conn = self.get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO pattern_cache (analysis_date, days_analyzed, analysis_results)
            VALUES (DATE('now'), ?, ?)
        """, (days, json.dumps(analysis.to_dict())))

        conn.commit()
        conn.close()

    def save_report(self, report: ImprovementReport, report_type: str = "weekly") -> None:
        """Save improvement report to database."""
        conn = self.get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO reports (period, report_type, report_data)
            VALUES (?, ?, ?)
        """, (report.period, report_type, json.dumps(report.to_dict())))

        conn.commit()
        conn.close()


class FeedbackAnalyzer:
    """Analyzes feedback patterns and generates insights."""

    def __init__(self, db: FeedbackDatabase):
        """Initialize analyzer with database."""
        self.db = db

    def analyze_patterns(
        self,
        days: int = 7,
        min_samples: int = 5
    ) -> PatternAnalysis:
        """
        Analyze patterns in feedback data.

        Args:
            days: Number of days to analyze
            min_samples: Minimum number of samples required

        Returns:
            PatternAnalysis with insights
        """
        # Get recent feedback
        start_date = (datetime.now() - timedelta(days=days)).isoformat()
        all_feedback = self.db.get_feedback(start_date=start_date)

        if len(all_feedback) < min_samples:
            raise ValueError(
                f"Insufficient feedback data. Found {len(all_feedback)} entries, "
                f"need at least {min_samples}"
            )

        # Separate positive and negative feedback
        positive = [f for f in all_feedback if f.is_positive()]
        negative = [f for f in all_feedback if f.is_negative()]

        # Analyze patterns
        positive_patterns = self._extract_patterns(positive, "positive")
        negative_patterns = self._extract_patterns(negative, "negative")

        # Analyze tag performance
        tag_performance = self._analyze_tag_performance(all_feedback)

        # Analyze framework performance
        framework_performance = self._analyze_framework_performance(all_feedback)

        # Generate recommendations
        recommendations = self._generate_recommendations(
            positive_patterns,
            negative_patterns,
            tag_performance,
            framework_performance
        )

        success_rate = len(positive) / len(all_feedback) if all_feedback else 0.0

        return PatternAnalysis(
            total_feedback=len(all_feedback),
            positive_count=len(positive),
            negative_count=len(negative),
            success_rate=success_rate,
            common_positive_patterns=positive_patterns,
            common_negative_patterns=negative_patterns,
            tag_performance=tag_performance,
            framework_performance=framework_performance,
            recommendations=recommendations
        )

    def _extract_patterns(
        self,
        feedback_list: List[FeedbackEntry],
        category: str
    ) -> List[Dict[str, Any]]:
        """Extract common patterns from feedback entries."""
        if not feedback_list:
            return []

        patterns = []

        # Pattern 1: Common words in prompts
        prompt_words = []
        for f in feedback_list:
            words = re.findall(r'\b\w+\b', f.prompt.lower())
            prompt_words.extend([w for w in words if len(w) > 4])

        common_words = Counter(prompt_words).most_common(10)
        if common_words:
            patterns.append({
                'type': 'common_prompt_words',
                'description': f'Common words in {category} prompts',
                'data': [{'word': w, 'count': c} for w, c in common_words],
                'sample_size': len(feedback_list)
            })

        # Pattern 2: Prompt length correlation
        avg_prompt_length = sum(len(f.prompt) for f in feedback_list) / len(feedback_list)
        avg_output_length = sum(len(f.output) for f in feedback_list) / len(feedback_list)

        patterns.append({
            'type': 'length_statistics',
            'description': f'Average lengths for {category} feedback',
            'data': {
                'avg_prompt_length': round(avg_prompt_length, 1),
                'avg_output_length': round(avg_output_length, 1)
            },
            'sample_size': len(feedback_list)
        })

        # Pattern 3: Common tags
        tag_counter = Counter()
        for f in feedback_list:
            tag_counter.update(f.tags)

        if tag_counter:
            patterns.append({
                'type': 'common_tags',
                'description': f'Most common tags in {category} feedback',
                'data': [{'tag': tag, 'count': count} for tag, count in tag_counter.most_common(5)],
                'sample_size': len(feedback_list)
            })

        # Pattern 4: Structural patterns
        structure_patterns = {
            'has_examples': sum(1 for f in feedback_list if 'example' in f.prompt.lower() or 'e.g.' in f.prompt.lower()),
            'has_constraints': sum(1 for f in feedback_list if any(word in f.prompt.lower() for word in ['must', 'should', 'only', 'exactly'])),
            'has_steps': sum(1 for f in feedback_list if any(word in f.prompt.lower() for word in ['step', 'first', 'then', 'finally'])),
            'has_format_spec': sum(1 for f in feedback_list if any(word in f.prompt.lower() for word in ['format', 'json', 'xml', 'structure']))
        }

        patterns.append({
            'type': 'structural_patterns',
            'description': f'Structural characteristics of {category} prompts',
            'data': structure_patterns,
            'sample_size': len(feedback_list)
        })

        return patterns

    def _analyze_tag_performance(
        self,
        feedback_list: List[FeedbackEntry]
    ) -> Dict[str, Dict[str, Any]]:
        """Analyze performance by tag."""
        tag_stats = defaultdict(lambda: {'ratings': [], 'thumbs_up': 0, 'thumbs_down': 0, 'count': 0})

        for f in feedback_list:
            for tag in f.tags:
                tag_stats[tag]['ratings'].append(f.rating)
                tag_stats[tag]['count'] += 1
                if f.thumbs_up:
                    tag_stats[tag]['thumbs_up'] += 1
                else:
                    tag_stats[tag]['thumbs_down'] += 1

        # Calculate averages and success rates
        result = {}
        for tag, stats in tag_stats.items():
            avg_rating = sum(stats['ratings']) / len(stats['ratings'])
            success_rate = stats['thumbs_up'] / stats['count']

            result[tag] = {
                'count': stats['count'],
                'avg_rating': round(avg_rating, 2),
                'success_rate': round(success_rate, 2),
                'thumbs_up': stats['thumbs_up'],
                'thumbs_down': stats['thumbs_down']
            }

        return result

    def _analyze_framework_performance(
        self,
        feedback_list: List[FeedbackEntry]
    ) -> Dict[str, Dict[str, Any]]:
        """Analyze performance by framework."""
        framework_stats = defaultdict(lambda: {'ratings': [], 'thumbs_up': 0, 'thumbs_down': 0, 'count': 0})

        for f in feedback_list:
            framework = f.context.get('framework', 'unknown')
            framework_stats[framework]['ratings'].append(f.rating)
            framework_stats[framework]['count'] += 1
            if f.thumbs_up:
                framework_stats[framework]['thumbs_up'] += 1
            else:
                framework_stats[framework]['thumbs_down'] += 1

        # Calculate averages and success rates
        result = {}
        for framework, stats in framework_stats.items():
            avg_rating = sum(stats['ratings']) / len(stats['ratings'])
            success_rate = stats['thumbs_up'] / stats['count']

            result[framework] = {
                'count': stats['count'],
                'avg_rating': round(avg_rating, 2),
                'success_rate': round(success_rate, 2),
                'thumbs_up': stats['thumbs_up'],
                'thumbs_down': stats['thumbs_down']
            }

        return result

    def _generate_recommendations(
        self,
        positive_patterns: List[Dict[str, Any]],
        negative_patterns: List[Dict[str, Any]],
        tag_performance: Dict[str, Dict[str, Any]],
        framework_performance: Dict[str, Dict[str, Any]]
    ) -> List[str]:
        """Generate actionable recommendations based on analysis."""
        recommendations = []

        # Recommend based on tag performance
        if tag_performance:
            best_tags = sorted(
                tag_performance.items(),
                key=lambda x: x[1]['success_rate'],
                reverse=True
            )[:3]

            if best_tags and best_tags[0][1]['success_rate'] > 0.7:
                top_tags = ', '.join([tag for tag, _ in best_tags])
                recommendations.append(
                    f"Use tags '{top_tags}' more frequently - they show high success rates"
                )

            worst_tags = sorted(
                tag_performance.items(),
                key=lambda x: x[1]['success_rate']
            )[:3]

            if worst_tags and worst_tags[0][1]['success_rate'] < 0.4:
                recommendations.append(
                    f"Review prompts tagged '{worst_tags[0][0]}' - success rate is only "
                    f"{worst_tags[0][1]['success_rate']:.0%}"
                )

        # Recommend based on framework performance
        if framework_performance:
            best_frameworks = sorted(
                framework_performance.items(),
                key=lambda x: x[1]['success_rate'],
                reverse=True
            )[:2]

            if best_frameworks and best_frameworks[0][1]['success_rate'] > 0.7:
                recommendations.append(
                    f"Framework '{best_frameworks[0][0]}' performing well "
                    f"({best_frameworks[0][1]['success_rate']:.0%} success) - use it for similar tasks"
                )

        # Recommend based on structural patterns
        for pattern in positive_patterns:
            if pattern['type'] == 'structural_patterns':
                data = pattern['data']
                total = pattern['sample_size']

                if data['has_examples'] / total > 0.6:
                    recommendations.append(
                        "Including examples in prompts correlates with success - add more examples"
                    )

                if data['has_constraints'] / total > 0.5:
                    recommendations.append(
                        "Prompts with explicit constraints perform better - be more specific about requirements"
                    )

                if data['has_format_spec'] / total > 0.5:
                    recommendations.append(
                        "Specifying output format improves results - always define expected structure"
                    )

        # Recommend based on length
        for pos_pattern in positive_patterns:
            if pos_pattern['type'] == 'length_statistics':
                pos_prompt_len = pos_pattern['data']['avg_prompt_length']

                for neg_pattern in negative_patterns:
                    if neg_pattern['type'] == 'length_statistics':
                        neg_prompt_len = neg_pattern['data']['avg_prompt_length']

                        if pos_prompt_len > neg_prompt_len * 1.3:
                            recommendations.append(
                                f"Successful prompts are {((pos_prompt_len/neg_prompt_len - 1) * 100):.0f}% "
                                "longer on average - add more context and detail"
                            )
                        elif pos_prompt_len < neg_prompt_len * 0.7:
                            recommendations.append(
                                "Successful prompts are more concise - reduce verbosity"
                            )

        if not recommendations:
            recommendations.append("Collect more feedback data to generate specific recommendations")

        return recommendations


class PromptSuggestionEngine:
    """Generates prompt improvement suggestions using AI."""

    def __init__(self, api_key: Optional[str] = None):
        """Initialize suggestion engine."""
        if not HAS_ANTHROPIC:
            raise ImportError("anthropic package required for suggestions. Run: pip install anthropic")

        self.client = anthropic.Anthropic(api_key=api_key)
        self.model = "claude-sonnet-4-20250514"

    def suggest_improvements(
        self,
        analysis: PatternAnalysis,
        framework: Optional[str] = None,
        limit: int = 5
    ) -> List[Dict[str, str]]:
        """
        Generate prompt improvement suggestions based on analysis.

        Args:
            analysis: PatternAnalysis results
            framework: Specific framework to target
            limit: Maximum number of suggestions

        Returns:
            List of suggestions with reasoning
        """
        # Build context for AI
        context = self._build_suggestion_context(analysis, framework)

        prompt = f"""Based on the following feedback analysis, suggest {limit} specific ways to improve prompts.

Analysis Summary:
- Total Feedback: {analysis.total_feedback}
- Success Rate: {analysis.success_rate:.1%}
- Positive Feedback: {analysis.positive_count}
- Negative Feedback: {analysis.negative_count}

{context}

Current Recommendations:
{chr(10).join('- ' + r for r in analysis.recommendations)}

Provide {limit} SPECIFIC, ACTIONABLE suggestions for improving prompts. For each suggestion:
1. Describe the improvement technique
2. Explain why it will help based on the analysis
3. Provide a concrete example

Format as JSON array:
[
  {{
    "technique": "technique name",
    "reasoning": "why this helps",
    "example": "concrete example of the improvement"
  }}
]
"""

        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=2048,
                temperature=0.7,
                messages=[{"role": "user", "content": prompt}]
            )

            # Parse JSON response
            content = response.content[0].text
            # Extract JSON from potential markdown code blocks
            if "```json" in content:
                content = content.split("```json")[1].split("```")[0].strip()
            elif "```" in content:
                content = content.split("```")[1].split("```")[0].strip()

            suggestions = json.loads(content)
            return suggestions[:limit]

        except Exception as e:
            print(f"Warning: Failed to generate AI suggestions: {e}")
            return self._fallback_suggestions(analysis)[:limit]

    def _build_suggestion_context(
        self,
        analysis: PatternAnalysis,
        framework: Optional[str] = None
    ) -> str:
        """Build context string for AI suggestion prompt."""
        parts = []

        # Add positive patterns
        if analysis.common_positive_patterns:
            parts.append("Patterns in SUCCESSFUL prompts:")
            for pattern in analysis.common_positive_patterns[:3]:
                parts.append(f"  - {pattern['description']}: {pattern['data']}")

        # Add negative patterns
        if analysis.common_negative_patterns:
            parts.append("\nPatterns in FAILED prompts:")
            for pattern in analysis.common_negative_patterns[:3]:
                parts.append(f"  - {pattern['description']}: {pattern['data']}")

        # Add framework performance
        if framework and framework in analysis.framework_performance:
            perf = analysis.framework_performance[framework]
            parts.append(f"\nFramework '{framework}' performance:")
            parts.append(f"  - Success rate: {perf['success_rate']:.1%}")
            parts.append(f"  - Average rating: {perf['avg_rating']:.1f}/5")

        return "\n".join(parts)

    def _fallback_suggestions(self, analysis: PatternAnalysis) -> List[Dict[str, str]]:
        """Provide fallback suggestions if AI fails."""
        suggestions = []

        if analysis.success_rate < 0.6:
            suggestions.append({
                'technique': 'Add explicit output constraints',
                'reasoning': 'Low success rate indicates prompts may be too vague',
                'example': 'Add "Provide your answer in exactly 3 bullet points" to constrain output'
            })

        suggestions.append({
            'technique': 'Include concrete examples',
            'reasoning': 'Examples help clarify expectations',
            'example': 'Add "For example: Input: X → Output: Y" to show desired format'
        })

        suggestions.append({
            'technique': 'Use step-by-step instructions',
            'reasoning': 'Breaking down tasks improves consistency',
            'example': 'Restructure as "1. First, analyze X. 2. Then, consider Y. 3. Finally, conclude Z."'
        })

        return suggestions


def capture_feedback(
    prompt: str,
    output: str,
    rating: int,
    thumbs_up: bool,
    tags: List[str],
    context: Dict[str, Any],
    notes: Optional[str] = None,
    db: Optional[FeedbackDatabase] = None
) -> FeedbackEntry:
    """
    Capture user feedback and store in database.

    Args:
        prompt: The original prompt
        output: The generated output
        rating: Rating from 1-5
        thumbs_up: Thumbs up/down boolean
        tags: List of tags
        context: Additional context (model, framework, etc.)
        notes: Optional user notes
        db: Optional database instance (creates new if None)

    Returns:
        Created FeedbackEntry
    """
    if db is None:
        db = FeedbackDatabase()

    entry = FeedbackEntry(
        prompt=prompt,
        output=output,
        rating=rating,
        thumbs_up=thumbs_up,
        tags=tags,
        timestamp=datetime.now().isoformat(),
        context=context,
        notes=notes
    )

    db.insert_feedback(entry)

    print(f"Feedback captured: ID={entry.feedback_id}")
    print(f"  Rating: {rating}/5 | Thumbs: {'UP' if thumbs_up else 'DOWN'}")
    print(f"  Tags: {', '.join(tags)}")

    return entry


def analyze_patterns(
    days: int = 7,
    min_samples: int = 5,
    db: Optional[FeedbackDatabase] = None
) -> PatternAnalysis:
    """
    Analyze feedback patterns.

    Args:
        days: Number of days to analyze
        min_samples: Minimum samples required
        db: Optional database instance

    Returns:
        PatternAnalysis results
    """
    if db is None:
        db = FeedbackDatabase()

    analyzer = FeedbackAnalyzer(db)
    analysis = analyzer.analyze_patterns(days=days, min_samples=min_samples)

    # Cache the analysis
    db.cache_analysis(days, analysis)

    print("\n" + "=" * 80)
    print(f"FEEDBACK PATTERN ANALYSIS (Last {days} days)")
    print("=" * 80)
    print(f"\nOverall Statistics:")
    print(f"  Total Feedback: {analysis.total_feedback}")
    print(f"  Positive: {analysis.positive_count} ({analysis.positive_count/analysis.total_feedback:.1%})")
    print(f"  Negative: {analysis.negative_count} ({analysis.negative_count/analysis.total_feedback:.1%})")
    print(f"  Success Rate: {analysis.success_rate:.1%}")

    print(f"\n\nTop Recommendations:")
    for i, rec in enumerate(analysis.recommendations, 1):
        print(f"  {i}. {rec}")

    print("\n" + "=" * 80 + "\n")

    return analysis


def generate_report(
    period: str = "weekly",
    output_file: Optional[str] = None,
    db: Optional[FeedbackDatabase] = None
) -> ImprovementReport:
    """
    Generate improvement report.

    Args:
        period: "weekly" or "monthly"
        output_file: Optional file to save report
        db: Optional database instance

    Returns:
        ImprovementReport
    """
    if db is None:
        db = FeedbackDatabase()

    # Calculate date range
    end_date = datetime.now()

    if period == "weekly":
        start_date = end_date - timedelta(days=7)
        prev_start_date = start_date - timedelta(days=7)
        period_label = end_date.strftime("%Y-W%U")
    elif period == "monthly":
        start_date = end_date - timedelta(days=30)
        prev_start_date = start_date - timedelta(days=30)
        period_label = end_date.strftime("%Y-%m")
    else:
        raise ValueError("Period must be 'weekly' or 'monthly'")

    # Get current period stats
    current_stats = db.get_statistics(
        start_date=start_date.isoformat(),
        end_date=end_date.isoformat()
    )

    # Get previous period stats for comparison
    prev_stats = db.get_statistics(
        start_date=prev_start_date.isoformat(),
        end_date=start_date.isoformat()
    )

    # Calculate improvement
    improvement = None
    if prev_stats['success_rate'] > 0:
        improvement = (
            (current_stats['success_rate'] - prev_stats['success_rate'])
            / prev_stats['success_rate'] * 100
        )

    # Get feedback for analysis
    feedback_list = db.get_feedback(
        start_date=start_date.isoformat(),
        end_date=end_date.isoformat()
    )

    # Find top performers
    positive_feedback = [f for f in feedback_list if f.is_positive()]
    top_performers = []

    if positive_feedback:
        # Group by framework
        framework_groups = defaultdict(list)
        for f in positive_feedback:
            framework = f.context.get('framework', 'unknown')
            framework_groups[framework].append(f)

        for framework, entries in sorted(
            framework_groups.items(),
            key=lambda x: len(x[1]),
            reverse=True
        )[:5]:
            avg_rating = sum(e.rating for e in entries) / len(entries)
            top_performers.append({
                'framework': framework,
                'count': len(entries),
                'avg_rating': round(avg_rating, 2)
            })

    # Find problem areas
    negative_feedback = [f for f in feedback_list if f.is_negative()]
    problem_areas = []

    if negative_feedback:
        # Group by tags
        tag_groups = defaultdict(list)
        for f in negative_feedback:
            for tag in f.tags:
                tag_groups[tag].append(f)

        for tag, entries in sorted(
            tag_groups.items(),
            key=lambda x: len(x[1]),
            reverse=True
        )[:5]:
            problem_areas.append({
                'tag': tag,
                'failure_count': len(entries),
                'percentage': round(len(entries) / len(feedback_list) * 100, 1)
            })

    # Generate action items
    action_items = []

    if improvement and improvement < 0:
        action_items.append(f"Success rate decreased by {abs(improvement):.1f}% - review recent changes")
    elif improvement and improvement > 10:
        action_items.append(f"Success rate improved by {improvement:.1f}% - document what's working")

    if current_stats['success_rate'] < 0.7:
        action_items.append("Success rate below 70% - conduct thorough pattern analysis")

    if problem_areas:
        action_items.append(f"Focus on improving '{problem_areas[0]['tag']}' prompts - highest failure rate")

    if current_stats['total_count'] < 10:
        action_items.append("Collect more feedback data for better insights")

    if not action_items:
        action_items.append("Continue current approach - metrics are stable")

    # Create report
    report = ImprovementReport(
        period=period_label,
        start_date=start_date.isoformat(),
        end_date=end_date.isoformat(),
        total_prompts=current_stats['total_count'],
        avg_rating=round(current_stats['avg_rating'], 2),
        success_rate=round(current_stats['success_rate'], 3),
        improvement_vs_previous=round(improvement, 2) if improvement else None,
        top_performers=top_performers,
        problem_areas=problem_areas,
        action_items=action_items
    )

    # Save to database
    db.save_report(report, report_type=period)

    # Save to file if requested
    if output_file:
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(report.to_dict(), f, indent=2)
        print(f"Report saved to: {output_file}")

    # Print summary
    print("\n" + "=" * 80)
    print(f"IMPROVEMENT REPORT - {period.upper()} ({period_label})")
    print("=" * 80)
    print(f"\nPeriod: {start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}")
    print(f"\nMetrics:")
    print(f"  Total Prompts: {report.total_prompts}")
    print(f"  Average Rating: {report.avg_rating:.2f}/5")
    print(f"  Success Rate: {report.success_rate:.1%}")

    if report.improvement_vs_previous is not None:
        direction = "↑" if report.improvement_vs_previous > 0 else "↓"
        print(f"  Change vs Previous: {direction} {abs(report.improvement_vs_previous):.1f}%")

    if top_performers:
        print(f"\n\nTop Performers:")
        for p in top_performers:
            print(f"  - {p['framework']}: {p['count']} successes, {p['avg_rating']:.1f}/5 avg")

    if problem_areas:
        print(f"\n\nProblem Areas:")
        for p in problem_areas:
            print(f"  - {p['tag']}: {p['failure_count']} failures ({p['percentage']:.1f}%)")

    print(f"\n\nAction Items:")
    for i, action in enumerate(action_items, 1):
        print(f"  {i}. {action}")

    print("\n" + "=" * 80 + "\n")

    return report


def suggest_improvements(
    framework: Optional[str] = None,
    days: int = 7,
    limit: int = 5,
    db: Optional[FeedbackDatabase] = None
) -> List[Dict[str, str]]:
    """
    Get AI-powered prompt improvement suggestions.

    Args:
        framework: Specific framework to target
        days: Days of feedback to analyze
        limit: Maximum number of suggestions
        db: Optional database instance

    Returns:
        List of suggestions
    """
    if db is None:
        db = FeedbackDatabase()

    # First analyze patterns
    analyzer = FeedbackAnalyzer(db)
    analysis = analyzer.analyze_patterns(days=days, min_samples=3)

    # Generate suggestions
    engine = PromptSuggestionEngine()
    suggestions = engine.suggest_improvements(
        analysis=analysis,
        framework=framework,
        limit=limit
    )

    # Print suggestions
    print("\n" + "=" * 80)
    print(f"PROMPT IMPROVEMENT SUGGESTIONS")
    if framework:
        print(f"Framework: {framework}")
    print("=" * 80)

    for i, suggestion in enumerate(suggestions, 1):
        print(f"\n{i}. {suggestion['technique']}")
        print(f"\n   Why: {suggestion['reasoning']}")
        print(f"\n   Example: {suggestion['example']}")
        print("\n" + "-" * 80)

    return suggestions


def main():
    """CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Feedback Capture and Learning Loop System",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )

    # Commands
    parser.add_argument("--init", action="store_true", help="Initialize database")
    parser.add_argument("--capture", action="store_true", help="Capture feedback")
    parser.add_argument("--analyze", action="store_true", help="Analyze patterns")
    parser.add_argument("--report", action="store_true", help="Generate report")
    parser.add_argument("--suggest", action="store_true", help="Get improvement suggestions")

    # Capture options
    parser.add_argument("--prompt", help="Prompt text (for --capture)")
    parser.add_argument("--output", help="Output text (for --capture) or report file (for --report)")
    parser.add_argument("--rating", type=int, choices=[1, 2, 3, 4, 5], help="Rating 1-5 (for --capture)")
    parser.add_argument("--thumbs-up", action="store_true", help="Thumbs up (for --capture)")
    parser.add_argument("--thumbs-down", action="store_true", help="Thumbs down (for --capture)")
    parser.add_argument("--tags", help="Comma-separated tags (for --capture)")
    parser.add_argument("--notes", help="Optional notes (for --capture)")
    parser.add_argument("--framework", help="Framework name (for context/filtering)")
    parser.add_argument("--model", help="Model name (for context)")

    # Analysis options
    parser.add_argument("--days", type=int, default=7, help="Days to analyze (default: 7)")
    parser.add_argument("--min-samples", type=int, default=5, help="Minimum samples required (default: 5)")

    # Report options
    parser.add_argument("--period", choices=["weekly", "monthly"], default="weekly", help="Report period")

    # Suggestion options
    parser.add_argument("--limit", type=int, default=5, help="Maximum suggestions (default: 5)")

    args = parser.parse_args()

    # Initialize database if requested
    if args.init:
        db = FeedbackDatabase()
        db.init_database()
        return

    # Validate command
    if not any([args.capture, args.analyze, args.report, args.suggest]):
        parser.print_help()
        sys.exit(1)

    try:
        db = FeedbackDatabase()

        if args.capture:
            # Validate required fields
            if not all([args.prompt, args.output, args.rating is not None]):
                print("Error: --capture requires --prompt, --output, and --rating")
                sys.exit(1)

            if args.thumbs_up and args.thumbs_down:
                print("Error: Cannot specify both --thumbs-up and --thumbs-down")
                sys.exit(1)

            thumbs_up = args.thumbs_up if args.thumbs_up or args.thumbs_down else (args.rating >= 4)
            tags = [t.strip() for t in args.tags.split(',')] if args.tags else []

            context = {}
            if args.framework:
                context['framework'] = args.framework
            if args.model:
                context['model'] = args.model

            capture_feedback(
                prompt=args.prompt,
                output=args.output,
                rating=args.rating,
                thumbs_up=thumbs_up,
                tags=tags,
                context=context,
                notes=args.notes,
                db=db
            )

        elif args.analyze:
            analyze_patterns(
                days=args.days,
                min_samples=args.min_samples,
                db=db
            )

        elif args.report:
            generate_report(
                period=args.period,
                output_file=args.output,
                db=db
            )

        elif args.suggest:
            suggest_improvements(
                framework=args.framework,
                days=args.days,
                limit=args.limit,
                db=db
            )

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
