#!/usr/bin/env python3
"""
Tests for the Feedback System

Run with: python -m pytest tests/test_feedback_system.py -v
Or: python tests/test_feedback_system.py
"""

import unittest
import tempfile
import json
from pathlib import Path
from datetime import datetime, timedelta
import sys

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

from feedback_system import (
    FeedbackEntry,
    FeedbackDatabase,
    FeedbackAnalyzer,
    PatternAnalysis,
    ImprovementReport,
    capture_feedback,
    analyze_patterns,
    generate_report
)


class TestFeedbackEntry(unittest.TestCase):
    """Test FeedbackEntry dataclass."""

    def test_create_entry(self):
        """Test creating a feedback entry."""
        entry = FeedbackEntry(
            prompt="Test prompt",
            output="Test output",
            rating=5,
            thumbs_up=True,
            tags=["test", "example"],
            timestamp=datetime.now().isoformat(),
            context={"framework": "chain-of-thought"}
        )

        self.assertEqual(entry.prompt, "Test prompt")
        self.assertEqual(entry.rating, 5)
        self.assertTrue(entry.thumbs_up)
        self.assertIsNotNone(entry.feedback_id)

    def test_invalid_rating(self):
        """Test that invalid ratings raise ValueError."""
        with self.assertRaises(ValueError):
            FeedbackEntry(
                prompt="Test",
                output="Test",
                rating=0,
                thumbs_up=True,
                tags=[],
                timestamp=datetime.now().isoformat(),
                context={}
            )

        with self.assertRaises(ValueError):
            FeedbackEntry(
                prompt="Test",
                output="Test",
                rating=6,
                thumbs_up=True,
                tags=[],
                timestamp=datetime.now().isoformat(),
                context={}
            )

    def test_is_positive(self):
        """Test positive feedback detection."""
        positive = FeedbackEntry(
            prompt="Test",
            output="Test",
            rating=5,
            thumbs_up=True,
            tags=[],
            timestamp=datetime.now().isoformat(),
            context={}
        )
        self.assertTrue(positive.is_positive())

        negative = FeedbackEntry(
            prompt="Test",
            output="Test",
            rating=2,
            thumbs_up=False,
            tags=[],
            timestamp=datetime.now().isoformat(),
            context={}
        )
        self.assertFalse(negative.is_positive())

    def test_is_negative(self):
        """Test negative feedback detection."""
        negative = FeedbackEntry(
            prompt="Test",
            output="Test",
            rating=2,
            thumbs_up=False,
            tags=[],
            timestamp=datetime.now().isoformat(),
            context={}
        )
        self.assertTrue(negative.is_negative())

    def test_to_dict(self):
        """Test conversion to dictionary."""
        entry = FeedbackEntry(
            prompt="Test",
            output="Test",
            rating=5,
            thumbs_up=True,
            tags=["test"],
            timestamp=datetime.now().isoformat(),
            context={"key": "value"}
        )

        data = entry.to_dict()
        self.assertIn('feedback_id', data)
        self.assertIn('prompt', data)
        self.assertIn('rating', data)
        self.assertEqual(data['tags'], ["test"])


class TestFeedbackDatabase(unittest.TestCase):
    """Test database operations."""

    def setUp(self):
        """Create temporary database for testing."""
        self.temp_dir = tempfile.mkdtemp()
        self.db_path = Path(self.temp_dir) / "test_feedback.db"
        self.db = FeedbackDatabase(db_path=self.db_path)
        self.db.init_database()

    def tearDown(self):
        """Clean up temporary database."""
        if self.db_path.exists():
            self.db_path.unlink()

    def test_init_database(self):
        """Test database initialization."""
        self.assertTrue(self.db_path.exists())

    def test_insert_feedback(self):
        """Test inserting feedback."""
        entry = FeedbackEntry(
            prompt="Test prompt",
            output="Test output",
            rating=5,
            thumbs_up=True,
            tags=["test"],
            timestamp=datetime.now().isoformat(),
            context={"framework": "test"}
        )

        row_id = self.db.insert_feedback(entry)
        self.assertIsNotNone(row_id)
        self.assertGreater(row_id, 0)

    def test_duplicate_insert(self):
        """Test that duplicate entries raise error."""
        entry = FeedbackEntry(
            prompt="Test",
            output="Test",
            rating=5,
            thumbs_up=True,
            tags=[],
            timestamp=datetime.now().isoformat(),
            context={},
            feedback_id="test-id-123"
        )

        self.db.insert_feedback(entry)

        # Try to insert again with same ID
        with self.assertRaises(ValueError):
            self.db.insert_feedback(entry)

    def test_get_feedback(self):
        """Test retrieving feedback."""
        # Insert some test data
        for i in range(5):
            entry = FeedbackEntry(
                prompt=f"Prompt {i}",
                output=f"Output {i}",
                rating=i + 1,
                thumbs_up=i >= 3,
                tags=[f"tag{i}"],
                timestamp=datetime.now().isoformat(),
                context={"index": i}
            )
            self.db.insert_feedback(entry)

        # Get all feedback
        all_feedback = self.db.get_feedback()
        self.assertEqual(len(all_feedback), 5)

        # Get with filters
        positive = self.db.get_feedback(thumbs_up=True)
        self.assertEqual(len(positive), 2)  # ratings 4 and 5

        high_rated = self.db.get_feedback(min_rating=4)
        self.assertEqual(len(high_rated), 2)

    def test_get_statistics(self):
        """Test statistics calculation."""
        # Insert test data
        for i in range(10):
            entry = FeedbackEntry(
                prompt=f"Prompt {i}",
                output=f"Output {i}",
                rating=(i % 5) + 1,  # Ratings 1-5
                thumbs_up=i >= 5,
                tags=[],
                timestamp=datetime.now().isoformat(),
                context={}
            )
            self.db.insert_feedback(entry)

        stats = self.db.get_statistics()

        self.assertEqual(stats['total_count'], 10)
        self.assertGreater(stats['avg_rating'], 0)
        self.assertEqual(stats['thumbs_up_count'], 5)
        self.assertEqual(stats['thumbs_down_count'], 5)

    def test_date_filtering(self):
        """Test filtering by date range."""
        # Insert entries with different dates
        base_date = datetime.now()

        for i in range(5):
            entry = FeedbackEntry(
                prompt=f"Prompt {i}",
                output=f"Output {i}",
                rating=5,
                thumbs_up=True,
                tags=[],
                timestamp=(base_date - timedelta(days=i)).isoformat(),
                context={}
            )
            self.db.insert_feedback(entry)

        # Get last 3 days
        three_days_ago = (base_date - timedelta(days=3)).isoformat()
        recent = self.db.get_feedback(start_date=three_days_ago)

        self.assertLessEqual(len(recent), 4)  # Days 0, 1, 2, 3


class TestFeedbackAnalyzer(unittest.TestCase):
    """Test pattern analysis."""

    def setUp(self):
        """Create temporary database with test data."""
        self.temp_dir = tempfile.mkdtemp()
        self.db_path = Path(self.temp_dir) / "test_feedback.db"
        self.db = FeedbackDatabase(db_path=self.db_path)
        self.db.init_database()

        # Insert varied test data
        test_data = [
            # Positive feedback
            ("Explain the concept step by step", "Great explanation with examples", 5, True, ["technical", "explanation"]),
            ("Write a function to calculate sum", "Clean, well-documented code", 5, True, ["code", "python"]),
            ("Summarize this article briefly", "Concise summary, hit key points", 4, True, ["content", "summary"]),
            ("Create a structured plan", "Clear roadmap with milestones", 5, True, ["planning"]),
            ("Analyze the pros and cons", "Balanced analysis with examples", 4, True, ["analysis"]),

            # Negative feedback
            ("Write some code", "Too vague, unclear output", 2, False, ["code"]),
            ("Explain this", "Explanation was too brief", 2, False, ["explanation"]),
            ("Do something", "No context provided", 1, False, ["vague"]),
        ]

        for prompt, output, rating, thumbs_up, tags in test_data:
            entry = FeedbackEntry(
                prompt=prompt,
                output=output,
                rating=rating,
                thumbs_up=thumbs_up,
                tags=tags,
                timestamp=datetime.now().isoformat(),
                context={"framework": "test"}
            )
            self.db.insert_feedback(entry)

        self.analyzer = FeedbackAnalyzer(self.db)

    def tearDown(self):
        """Clean up temporary database."""
        if self.db_path.exists():
            self.db_path.unlink()

    def test_analyze_patterns(self):
        """Test pattern analysis."""
        analysis = self.analyzer.analyze_patterns(days=7, min_samples=5)

        self.assertIsInstance(analysis, PatternAnalysis)
        self.assertEqual(analysis.total_feedback, 8)
        self.assertEqual(analysis.positive_count, 5)
        self.assertEqual(analysis.negative_count, 3)
        self.assertGreater(analysis.success_rate, 0.5)

    def test_insufficient_data(self):
        """Test that insufficient data raises error."""
        # Create new database with minimal data
        temp_db = FeedbackDatabase(db_path=Path(self.temp_dir) / "minimal.db")
        temp_db.init_database()

        analyzer = FeedbackAnalyzer(temp_db)

        with self.assertRaises(ValueError):
            analyzer.analyze_patterns(days=7, min_samples=10)

    def test_pattern_extraction(self):
        """Test that patterns are extracted."""
        analysis = self.analyzer.analyze_patterns(days=7, min_samples=5)

        self.assertGreater(len(analysis.common_positive_patterns), 0)
        self.assertGreater(len(analysis.recommendations), 0)

    def test_tag_performance(self):
        """Test tag performance analysis."""
        analysis = self.analyzer.analyze_patterns(days=7, min_samples=5)

        self.assertIn("code", analysis.tag_performance)
        self.assertIn("explanation", analysis.tag_performance)

        # Code has mixed results (1 positive, 1 negative)
        code_perf = analysis.tag_performance["code"]
        self.assertIn("avg_rating", code_perf)
        self.assertIn("success_rate", code_perf)


class TestIntegrationFunctions(unittest.TestCase):
    """Test high-level integration functions."""

    def setUp(self):
        """Create temporary database."""
        self.temp_dir = tempfile.mkdtemp()
        self.db_path = Path(self.temp_dir) / "test_feedback.db"
        self.db = FeedbackDatabase(db_path=self.db_path)
        self.db.init_database()

    def tearDown(self):
        """Clean up."""
        if self.db_path.exists():
            self.db_path.unlink()

    def test_capture_feedback_function(self):
        """Test capture_feedback function."""
        entry = capture_feedback(
            prompt="Test prompt",
            output="Test output",
            rating=5,
            thumbs_up=True,
            tags=["test"],
            context={"framework": "test"},
            db=self.db
        )

        self.assertIsInstance(entry, FeedbackEntry)
        self.assertEqual(entry.rating, 5)

        # Verify it's in database
        all_feedback = self.db.get_feedback()
        self.assertEqual(len(all_feedback), 1)

    def test_generate_report_function(self):
        """Test generate_report function."""
        # Insert some test data
        for i in range(10):
            entry = FeedbackEntry(
                prompt=f"Prompt {i}",
                output=f"Output {i}",
                rating=(i % 5) + 1,
                thumbs_up=i >= 5,
                tags=["test"],
                timestamp=datetime.now().isoformat(),
                context={"framework": "test"}
            )
            self.db.insert_feedback(entry)

        # Generate report
        report = generate_report(
            period="weekly",
            output_file=None,
            db=self.db
        )

        self.assertIsInstance(report, ImprovementReport)
        self.assertEqual(report.total_prompts, 10)
        self.assertGreater(report.avg_rating, 0)


def run_tests():
    """Run all tests."""
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    # Add all test classes
    suite.addTests(loader.loadTestsFromTestCase(TestFeedbackEntry))
    suite.addTests(loader.loadTestsFromTestCase(TestFeedbackDatabase))
    suite.addTests(loader.loadTestsFromTestCase(TestFeedbackAnalyzer))
    suite.addTests(loader.loadTestsFromTestCase(TestIntegrationFunctions))

    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    return result.wasSuccessful()


if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)
