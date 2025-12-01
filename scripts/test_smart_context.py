#!/usr/bin/env python3
"""
Tests for smart_context.py

Tests the smart context selection system including:
- Token estimation
- Keyword similarity (fallback)
- Context chunk creation and scoring
- Context selection within budget
- Context compression
- Dynamic context gathering
- Cache functionality
"""

import sys
import unittest
from pathlib import Path
from datetime import datetime, timedelta
import tempfile
import shutil

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

from smart_context import (
    ContextChunk,
    estimate_tokens,
    keyword_similarity,
    load_context_file,
    select_context,
    compress_context,
    get_dynamic_context,
    EmbeddingCache,
    SemanticScorer,
    score_relevance,
)


class TestTokenEstimation(unittest.TestCase):
    """Test token counting functionality."""

    def test_estimate_tokens_short_text(self):
        """Test token estimation for short text."""
        text = "Hello world"
        tokens = estimate_tokens(text)
        self.assertGreater(tokens, 0)
        self.assertLess(tokens, 10)

    def test_estimate_tokens_long_text(self):
        """Test token estimation scales with text length."""
        short_text = "Hello world"
        long_text = short_text * 100

        short_tokens = estimate_tokens(short_text)
        long_tokens = estimate_tokens(long_text)

        self.assertGreater(long_tokens, short_tokens * 50)

    def test_estimate_tokens_empty(self):
        """Test token estimation for empty string."""
        tokens = estimate_tokens("")
        self.assertEqual(tokens, 0)


class TestKeywordSimilarity(unittest.TestCase):
    """Test keyword-based similarity scoring."""

    def test_identical_texts(self):
        """Identical texts should have high similarity."""
        text = "machine learning algorithms for text processing"
        score = keyword_similarity(text, text)
        self.assertEqual(score, 1.0)

    def test_similar_texts(self):
        """Similar texts should have moderate similarity."""
        text1 = "machine learning algorithms for data analysis"
        text2 = "machine learning techniques for data processing"
        score = keyword_similarity(text1, text2)
        self.assertGreater(score, 0.3)
        self.assertLess(score, 1.0)

    def test_different_texts(self):
        """Different texts should have low similarity."""
        text1 = "quantum physics and particle acceleration"
        text2 = "cooking recipes for italian cuisine"
        score = keyword_similarity(text1, text2)
        self.assertLess(score, 0.2)

    def test_empty_texts(self):
        """Empty texts should return zero similarity."""
        self.assertEqual(keyword_similarity("", "hello"), 0.0)
        self.assertEqual(keyword_similarity("hello", ""), 0.0)
        self.assertEqual(keyword_similarity("", ""), 0.0)

    def test_case_insensitive(self):
        """Similarity should be case-insensitive."""
        text1 = "Machine Learning"
        text2 = "machine learning"
        score = keyword_similarity(text1, text2)
        self.assertEqual(score, 1.0)


class TestContextChunk(unittest.TestCase):
    """Test ContextChunk dataclass."""

    def test_create_chunk(self):
        """Test creating a basic context chunk."""
        chunk = ContextChunk(
            source="test.md",
            content="This is test content",
            category="test"
        )

        self.assertEqual(chunk.source, "test.md")
        self.assertEqual(chunk.content, "This is test content")
        self.assertEqual(chunk.category, "test")
        self.assertGreater(chunk.token_count, 0)
        self.assertEqual(chunk.relevance_score, 0.0)

    def test_chunk_with_metadata(self):
        """Test chunk with custom metadata."""
        metadata = {'author': 'test', 'date': '2024-01-01'}
        chunk = ContextChunk(
            source="test.md",
            content="Content",
            metadata=metadata
        )

        self.assertEqual(chunk.metadata, metadata)

    def test_chunk_auto_token_count(self):
        """Test automatic token counting."""
        chunk = ContextChunk(
            source="test.md",
            content="A" * 1000  # Long content
        )

        self.assertGreater(chunk.token_count, 100)


class TestContextSelection(unittest.TestCase):
    """Test context selection logic."""

    def setUp(self):
        """Create test chunks."""
        self.chunks = [
            ContextChunk(
                source="high_score.md",
                content="A" * 1000,
                relevance_score=0.9,
                category="technical"
            ),
            ContextChunk(
                source="medium_score.md",
                content="B" * 1000,
                relevance_score=0.5,
                category="identity"
            ),
            ContextChunk(
                source="low_score.md",
                content="C" * 1000,
                relevance_score=0.2,
                category="business"
            ),
            ContextChunk(
                source="tiny_score.md",
                content="D" * 100,
                relevance_score=0.05,
                category="other"
            ),
        ]

    def test_select_top_n(self):
        """Test selecting top N chunks."""
        selected = select_context(self.chunks, top_n=2)
        self.assertEqual(len(selected), 2)
        self.assertEqual(selected[0].source, "high_score.md")
        self.assertEqual(selected[1].source, "medium_score.md")

    def test_select_within_token_budget(self):
        """Test selection respects token budget."""
        selected = select_context(self.chunks, max_tokens=500)
        total_tokens = sum(c.token_count for c in selected)
        self.assertLessEqual(total_tokens, 500)

    def test_select_min_score_filter(self):
        """Test minimum score filtering."""
        selected = select_context(self.chunks, min_score=0.3)
        self.assertTrue(all(c.relevance_score >= 0.3 for c in selected))

    def test_select_empty_chunks(self):
        """Test selection with empty chunk list."""
        selected = select_context([], max_tokens=1000)
        self.assertEqual(len(selected), 0)

    def test_select_sorts_by_relevance(self):
        """Test chunks are sorted by relevance."""
        selected = select_context(self.chunks, max_tokens=10000)
        scores = [c.relevance_score for c in selected]
        self.assertEqual(scores, sorted(scores, reverse=True))


class TestContextCompression(unittest.TestCase):
    """Test context compression functionality."""

    def test_compress_markdown(self):
        """Test compression of markdown content."""
        content = """# Main Title

This is the introduction paragraph that should be kept.

More details here.

## Section 1

First paragraph of section 1.

More content that might be removed.

## Section 2

First paragraph of section 2.
"""
        chunk = ContextChunk(source="test.md", content=content)
        compressed = compress_context(chunk, max_tokens=100)

        self.assertIsNotNone(compressed)
        self.assertLess(compressed.token_count, chunk.token_count)
        self.assertIn("# Main Title", compressed.content)
        self.assertIn("## Section 1", compressed.content)

    def test_compress_removes_code_blocks(self):
        """Test that code blocks are removed during compression."""
        content = """# Title

Some text.

```python
def foo():
    pass
```

More text.
"""
        chunk = ContextChunk(source="test.md", content=content)
        compressed = compress_context(chunk, max_tokens=50)

        self.assertIsNotNone(compressed)
        self.assertNotIn("```", compressed.content)
        self.assertNotIn("def foo", compressed.content)

    def test_compress_zero_budget(self):
        """Test compression with zero token budget."""
        chunk = ContextChunk(source="test.md", content="Some content")
        compressed = compress_context(chunk, max_tokens=0)

        self.assertIsNone(compressed)

    def test_compress_truncates_if_needed(self):
        """Test truncation when compression isn't enough."""
        content = "# " + "A" * 10000  # Very long heading
        chunk = ContextChunk(source="test.md", content=content)
        compressed = compress_context(chunk, max_tokens=50)

        self.assertIsNotNone(compressed)
        self.assertIn("[...truncated]", compressed.content)


class TestEmbeddingCache(unittest.TestCase):
    """Test embedding cache functionality."""

    def setUp(self):
        """Create temporary cache directory."""
        self.temp_dir = Path(tempfile.mkdtemp())
        self.cache = EmbeddingCache(cache_dir=self.temp_dir)

    def tearDown(self):
        """Clean up temporary directory."""
        shutil.rmtree(self.temp_dir)

    def test_cache_get_set(self):
        """Test basic cache get/set."""
        text = "test text"
        embedding = [0.1, 0.2, 0.3]

        self.cache.set(text, embedding, source="test")
        cached = self.cache.get(text)

        self.assertEqual(cached, embedding)

    def test_cache_miss(self):
        """Test cache miss returns None."""
        cached = self.cache.get("nonexistent text")
        self.assertIsNone(cached)

    def test_cache_persistence(self):
        """Test cache persists across instances."""
        text = "persistent text"
        embedding = [0.4, 0.5, 0.6]

        self.cache.set(text, embedding)

        # Create new cache instance
        new_cache = EmbeddingCache(cache_dir=self.temp_dir)
        cached = new_cache.get(text)

        self.assertEqual(cached, embedding)

    def test_cache_clear_old(self):
        """Test clearing old cache entries."""
        # Add entry
        self.cache.set("old text", [0.1, 0.2])

        # Manually set old timestamp
        key = self.cache.get_key("old text")
        old_date = (datetime.now() - timedelta(days=10)).isoformat()
        self.cache.metadata[key]['timestamp'] = old_date
        self.cache._save_cache()

        # Clear old entries
        self.cache.clear_old(days=7)

        # Should be gone
        cached = self.cache.get("old text")
        self.assertIsNone(cached)


class TestDynamicContext(unittest.TestCase):
    """Test dynamic context gathering."""

    def test_get_dynamic_context(self):
        """Test getting dynamic context."""
        context = get_dynamic_context()

        self.assertIsInstance(context, dict)
        self.assertIn('timestamp', context)
        self.assertIn('platform', context)

    def test_dynamic_context_has_timestamp(self):
        """Test dynamic context includes current timestamp."""
        context = get_dynamic_context()
        timestamp = context.get('timestamp', '')

        self.assertTrue(timestamp)
        # Should be parseable as date
        datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S')


class TestSemanticScorer(unittest.TestCase):
    """Test semantic scoring functionality."""

    def test_scorer_initialization(self):
        """Test scorer can be initialized."""
        scorer = SemanticScorer(use_cache=False)
        self.assertIsNotNone(scorer)

    def test_scorer_keyword_fallback(self):
        """Test scorer falls back to keyword matching."""
        scorer = SemanticScorer(use_cache=False)

        # Should work even without embeddings
        score = scorer.score_similarity(
            "machine learning",
            "machine learning algorithms"
        )

        self.assertGreater(score, 0.0)
        self.assertLessEqual(score, 1.0)

    def test_score_relevance_function(self):
        """Test the score_relevance function."""
        chunks = [
            ContextChunk(
                source="test1.md",
                content="machine learning and artificial intelligence",
                category="technical"
            ),
            ContextChunk(
                source="test2.md",
                content="cooking recipes and food preparation",
                category="other"
            ),
        ]

        scorer = SemanticScorer(use_cache=False)
        task = "How to implement machine learning models"

        scored = score_relevance(task, chunks, scorer)

        # First chunk should score higher
        self.assertGreater(scored[0].relevance_score, scored[1].relevance_score)

    def test_score_relevance_with_boost(self):
        """Test scoring with category boost."""
        chunks = [
            ContextChunk(
                source="technical.md",
                content="generic content",
                category="technical"
            ),
            ContextChunk(
                source="other.md",
                content="generic content",
                category="other"
            ),
        ]

        scorer = SemanticScorer(use_cache=False)
        task = "generic task"
        boost = {"technical": 0.5}

        scored = score_relevance(task, chunks, scorer, boost)

        # Technical should be boosted
        self.assertGreater(scored[0].relevance_score, scored[1].relevance_score)


class TestIntegration(unittest.TestCase):
    """Integration tests for the full pipeline."""

    def test_end_to_end_selection(self):
        """Test complete context selection pipeline."""
        # Create test chunks
        chunks = [
            ContextChunk(
                source="relevant.md",
                content="machine learning model training and deployment",
                category="technical"
            ),
            ContextChunk(
                source="somewhat_relevant.md",
                content="software development and programming practices",
                category="technical"
            ),
            ContextChunk(
                source="not_relevant.md",
                content="cooking recipes and culinary techniques",
                category="other"
            ),
        ]

        # Score and select
        scorer = SemanticScorer(use_cache=False)
        task = "How to train and deploy machine learning models"

        scored = score_relevance(task, chunks, scorer)
        selected = select_context(scored, max_tokens=2000, min_score=0.1)

        # Should select relevant chunks
        self.assertGreater(len(selected), 0)
        self.assertEqual(selected[0].source, "relevant.md")


def run_tests():
    """Run all tests."""
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromModule(sys.modules[__name__])
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    return result.wasSuccessful()


if __name__ == '__main__':
    success = run_tests()
    sys.exit(0 if success else 1)
