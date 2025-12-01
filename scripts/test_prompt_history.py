#!/usr/bin/env python3
"""
Test Suite for Prompt History System

Comprehensive tests for prompt_history.py functionality.
"""

import unittest
import tempfile
import json
from pathlib import Path
from datetime import datetime, timedelta
import sys

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

from prompt_history import (
    HistoryEntry,
    PromptHistoryDB,
    PromptHistory
)


class TestHistoryEntry(unittest.TestCase):
    """Test HistoryEntry dataclass."""

    def test_basic_creation(self):
        """Test basic entry creation."""
        entry = HistoryEntry(
            prompt="Test prompt",
            output="Test output"
        )
        self.assertEqual(entry.prompt, "Test prompt")
        self.assertEqual(entry.output, "Test output")
        self.assertIsNotNone(entry.timestamp)

    def test_full_entry(self):
        """Test entry with all fields."""
        entry = HistoryEntry(
            prompt="Test",
            output="Output",
            framework_used="chain-of-thought",
            template_used="test-template",
            model="gpt-4",
            tokens=100,
            cost=0.003,
            tags=["test", "unit"],
            metadata={"key": "value"}
        )
        self.assertEqual(entry.framework_used, "chain-of-thought")
        self.assertEqual(entry.model, "gpt-4")
        self.assertEqual(entry.tokens, 100)
        self.assertEqual(len(entry.tags), 2)

    def test_to_dict(self):
        """Test conversion to dictionary."""
        entry = HistoryEntry(
            prompt="Test",
            output="Output",
            tags=["tag1", "tag2"],
            metadata={"key": "value"}
        )
        data = entry.to_dict()
        self.assertIn("prompt", data)
        self.assertIn("timestamp", data)
        self.assertIsInstance(data["tags"], str)  # Should be comma-separated
        self.assertIsInstance(data["metadata"], str)  # Should be JSON

    def test_from_dict(self):
        """Test creation from dictionary."""
        data = {
            "prompt": "Test",
            "output": "Output",
            "tags": "tag1,tag2",
            "metadata": '{"key": "value"}'
        }
        entry = HistoryEntry.from_dict(data)
        self.assertEqual(entry.prompt, "Test")
        self.assertIsInstance(entry.tags, list)
        self.assertEqual(len(entry.tags), 2)
        self.assertIsInstance(entry.metadata, dict)


class TestPromptHistoryDB(unittest.TestCase):
    """Test PromptHistoryDB functionality."""

    def setUp(self):
        """Create temporary database for testing."""
        self.temp_dir = tempfile.mkdtemp()
        self.db_path = Path(self.temp_dir) / "test.db"
        self.db = PromptHistoryDB(self.db_path)

    def tearDown(self):
        """Clean up temporary database."""
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_database_initialization(self):
        """Test database is properly initialized."""
        self.assertTrue(self.db_path.exists())

    def test_save_entry(self):
        """Test saving an entry."""
        entry = HistoryEntry(
            prompt="Test prompt",
            output="Test output"
        )
        entry_id = self.db.save_entry(entry)
        self.assertIsInstance(entry_id, int)
        self.assertGreater(entry_id, 0)

    def test_get_recent(self):
        """Test retrieving recent entries."""
        # Save multiple entries
        for i in range(5):
            entry = HistoryEntry(
                prompt=f"Prompt {i}",
                output=f"Output {i}"
            )
            self.db.save_entry(entry)

        # Retrieve recent
        recent = self.db.get_recent(limit=3)
        self.assertEqual(len(recent), 3)
        # Should be in reverse chronological order
        self.assertEqual(recent[0].prompt, "Prompt 4")

    def test_search_history(self):
        """Test full-text search."""
        # Save entries with searchable content
        entries = [
            HistoryEntry(prompt="Python programming", output="Code example"),
            HistoryEntry(prompt="JavaScript tutorial", output="Web development"),
            HistoryEntry(prompt="Python data science", output="Analysis code"),
        ]
        for entry in entries:
            self.db.save_entry(entry)

        # Search for Python
        results = self.db.search_history("Python")
        self.assertEqual(len(results), 2)

    def test_get_by_tag(self):
        """Test filtering by tag."""
        # Save entries with different tags
        entry1 = HistoryEntry(
            prompt="Test 1",
            output="Output 1",
            tags=["python", "tutorial"]
        )
        entry2 = HistoryEntry(
            prompt="Test 2",
            output="Output 2",
            tags=["javascript", "tutorial"]
        )
        entry3 = HistoryEntry(
            prompt="Test 3",
            output="Output 3",
            tags=["python", "advanced"]
        )

        self.db.save_entry(entry1)
        self.db.save_entry(entry2)
        self.db.save_entry(entry3)

        # Get Python entries
        python_entries = self.db.get_by_tag("python")
        self.assertEqual(len(python_entries), 2)

    def test_get_by_date_range(self):
        """Test filtering by date range."""
        # Save entries at different times
        now = datetime.now()
        yesterday = now - timedelta(days=1)
        last_week = now - timedelta(days=7)

        entry1 = HistoryEntry(prompt="Recent", output="Output", timestamp=now)
        entry2 = HistoryEntry(prompt="Yesterday", output="Output", timestamp=yesterday)
        entry3 = HistoryEntry(prompt="Last week", output="Output", timestamp=last_week)

        self.db.save_entry(entry1)
        self.db.save_entry(entry2)
        self.db.save_entry(entry3)

        # Get last 2 days
        two_days_ago = now - timedelta(days=2)
        recent = self.db.get_by_date_range(two_days_ago, now)
        self.assertEqual(len(recent), 2)

    def test_get_by_framework(self):
        """Test filtering by framework."""
        entry1 = HistoryEntry(
            prompt="Test 1",
            output="Output 1",
            framework_used="chain-of-thought"
        )
        entry2 = HistoryEntry(
            prompt="Test 2",
            output="Output 2",
            framework_used="few-shot"
        )

        self.db.save_entry(entry1)
        self.db.save_entry(entry2)

        cot_entries = self.db.get_by_framework("chain-of-thought")
        self.assertEqual(len(cot_entries), 1)
        self.assertEqual(cot_entries[0].framework_used, "chain-of-thought")

    def test_get_statistics(self):
        """Test statistics generation."""
        # Save entries with tokens and costs
        for i in range(3):
            entry = HistoryEntry(
                prompt=f"Prompt {i}",
                output=f"Output {i}",
                tokens=100 * (i + 1),
                cost=0.01 * (i + 1),
                framework_used="test-framework",
                model="gpt-4",
                tags=["test"]
            )
            self.db.save_entry(entry)

        stats = self.db.get_statistics()
        self.assertEqual(stats["total_entries"], 3)
        self.assertEqual(stats["total_tokens"], 600)  # 100 + 200 + 300
        self.assertAlmostEqual(stats["total_cost"], 0.06, places=2)  # 0.01 + 0.02 + 0.03

    def test_export_to_json(self):
        """Test JSON export."""
        entry = HistoryEntry(prompt="Test", output="Output")
        self.db.save_entry(entry)

        export_path = Path(self.temp_dir) / "export.json"
        self.db.export_to_json(export_path)

        self.assertTrue(export_path.exists())

        # Verify JSON content
        with open(export_path) as f:
            data = json.load(f)
        self.assertIsInstance(data, list)
        self.assertGreater(len(data), 0)

    def test_export_to_csv(self):
        """Test CSV export."""
        entry = HistoryEntry(prompt="Test", output="Output")
        self.db.save_entry(entry)

        export_path = Path(self.temp_dir) / "export.csv"
        self.db.export_to_csv(export_path)

        self.assertTrue(export_path.exists())

        # Verify CSV has content
        with open(export_path) as f:
            lines = f.readlines()
        self.assertGreater(len(lines), 1)  # Header + at least one row

    def test_delete_entry(self):
        """Test entry deletion."""
        entry = HistoryEntry(prompt="Test", output="Output")
        entry_id = self.db.save_entry(entry)

        # Delete entry
        result = self.db.delete_entry(entry_id)
        self.assertTrue(result)

        # Verify deleted
        recent = self.db.get_recent(limit=10)
        self.assertEqual(len([e for e in recent if e.id == entry_id]), 0)


class TestPromptHistory(unittest.TestCase):
    """Test high-level PromptHistory interface."""

    def setUp(self):
        """Create temporary database for testing."""
        self.temp_dir = tempfile.mkdtemp()
        self.db_path = Path(self.temp_dir) / "test.db"
        self.history = PromptHistory(self.db_path)

    def tearDown(self):
        """Clean up temporary database."""
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_save(self):
        """Test high-level save method."""
        entry_id = self.history.save(
            prompt="Test prompt",
            output="Test output",
            model="gpt-4",
            tags=["test"]
        )
        self.assertIsInstance(entry_id, int)

    def test_search(self):
        """Test high-level search."""
        self.history.save(
            prompt="Python programming",
            output="Code example"
        )
        results = self.history.search("Python")
        self.assertGreater(len(results), 0)

    def test_get_by_tag(self):
        """Test tag filtering."""
        self.history.save(
            prompt="Test",
            output="Output",
            tags=["python"]
        )
        results = self.history.get_by_tag("python")
        self.assertGreater(len(results), 0)

    def test_get_recent(self):
        """Test recent retrieval."""
        self.history.save(prompt="Test 1", output="Output 1")
        self.history.save(prompt="Test 2", output="Output 2")

        recent = self.history.get_recent(limit=5)
        self.assertEqual(len(recent), 2)

    def test_get_today(self):
        """Test today's entries."""
        self.history.save(prompt="Today's test", output="Output")
        today = self.history.get_today()
        self.assertGreater(len(today), 0)

    def test_get_this_week(self):
        """Test this week's entries."""
        self.history.save(prompt="This week", output="Output")
        week = self.history.get_this_week()
        self.assertGreater(len(week), 0)

    def test_export_json(self):
        """Test JSON export."""
        self.history.save(prompt="Test", output="Output")
        export_path = Path(self.temp_dir) / "export.json"
        self.history.export_json(export_path)
        self.assertTrue(export_path.exists())

    def test_export_csv(self):
        """Test CSV export."""
        self.history.save(prompt="Test", output="Output")
        export_path = Path(self.temp_dir) / "export.csv"
        self.history.export_csv(export_path)
        self.assertTrue(export_path.exists())

    def test_stats(self):
        """Test statistics."""
        self.history.save(
            prompt="Test",
            output="Output",
            tokens=100,
            cost=0.003
        )
        stats = self.history.stats()
        self.assertIn("total_entries", stats)
        self.assertGreater(stats["total_entries"], 0)


class TestIntegration(unittest.TestCase):
    """Test integration scenarios."""

    def setUp(self):
        """Create temporary database for testing."""
        self.temp_dir = tempfile.mkdtemp()
        self.db_path = Path(self.temp_dir) / "test.db"
        self.history = PromptHistory(self.db_path)

    def tearDown(self):
        """Clean up temporary database."""
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_complete_workflow(self):
        """Test a complete workflow."""
        # Save multiple entries with different frameworks
        self.history.save(
            prompt="COT prompt",
            output="Step 1...",
            framework="chain-of-thought",
            model="gpt-4",
            tokens=150,
            cost=0.0045,
            tags=["reasoning", "math"]
        )

        self.history.save(
            prompt="Few-shot prompt",
            output="Based on examples...",
            framework="few-shot",
            model="claude-3",
            tokens=200,
            cost=0.004,
            tags=["learning", "examples"]
        )

        # Search
        results = self.history.search("prompt")
        self.assertEqual(len(results), 2)

        # Get by tag
        math_entries = self.history.get_by_tag("math")
        self.assertEqual(len(math_entries), 1)

        # Get statistics
        stats = self.history.stats()
        self.assertEqual(stats["total_entries"], 2)
        self.assertEqual(stats["total_tokens"], 350)

    def test_metadata_storage(self):
        """Test metadata storage and retrieval."""
        metadata = {
            "experiment": "A/B test",
            "variant": "A",
            "version": "1.0",
            "nested": {
                "key": "value"
            }
        }

        entry_id = self.history.save(
            prompt="Test",
            output="Output",
            metadata=metadata
        )

        # Retrieve and verify
        entries = self.history.get_recent(1)
        self.assertEqual(len(entries), 1)
        self.assertEqual(entries[0].metadata, metadata)


def run_tests():
    """Run all tests."""
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    # Add all test classes
    suite.addTests(loader.loadTestsFromTestCase(TestHistoryEntry))
    suite.addTests(loader.loadTestsFromTestCase(TestPromptHistoryDB))
    suite.addTests(loader.loadTestsFromTestCase(TestPromptHistory))
    suite.addTests(loader.loadTestsFromTestCase(TestIntegration))

    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    # Return exit code
    return 0 if result.wasSuccessful() else 1


if __name__ == '__main__':
    sys.exit(run_tests())
