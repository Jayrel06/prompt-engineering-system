#!/usr/bin/env python3
"""
Smart Context Selection System

Scores context files by semantic relevance to the current task and selects only
the most relevant context to optimize token usage while preserving meaning.

Features:
- Semantic similarity scoring using sentence-transformers (with keyword fallback)
- Token counting and budget management
- Context compression and summarization
- Dynamic context from git, file system, etc.
- Embedding caching for performance
- Integration with existing context-loader.py
"""

import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import List, Dict, Optional, Tuple, Set
import pickle
from datetime import datetime, timedelta

# Try to import optional dependencies
try:
    from sentence_transformers import SentenceTransformer
    import numpy as np
    HAS_SENTENCE_TRANSFORMERS = True
except ImportError:
    HAS_SENTENCE_TRANSFORMERS = False

try:
    import tiktoken
    HAS_TIKTOKEN = True
except ImportError:
    HAS_TIKTOKEN = False

# Project paths
SCRIPT_DIR = Path(__file__).parent
PROJECT_ROOT = SCRIPT_DIR.parent
CONTEXT_DIR = PROJECT_ROOT / "context"
FRAMEWORKS_DIR = PROJECT_ROOT / "frameworks"
TEMPLATES_DIR = PROJECT_ROOT / "templates"
CACHE_DIR = SCRIPT_DIR / "__pycache__" / "embeddings_cache"
CACHE_DIR.mkdir(parents=True, exist_ok=True)


@dataclass
class ContextChunk:
    """Represents a chunk of context with metadata and scoring."""
    source: str  # File path or source identifier
    content: str  # The actual content
    relevance_score: float = 0.0  # Similarity score to task (0-1)
    token_count: int = 0  # Estimated token count
    summary: Optional[str] = None  # Compressed summary if needed
    category: str = ""  # Context category (technical, identity, etc.)
    metadata: Dict = None  # Additional metadata

    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}
        if self.token_count == 0:
            self.token_count = estimate_tokens(self.content)


class EmbeddingCache:
    """Cache for text embeddings to avoid recomputation."""

    def __init__(self, cache_dir: Path = CACHE_DIR):
        self.cache_dir = cache_dir
        self.cache_file = cache_dir / "embeddings.pkl"
        self.metadata_file = cache_dir / "metadata.json"
        self.cache = self._load_cache()
        self.metadata = self._load_metadata()

    def _load_cache(self) -> Dict:
        """Load embedding cache from disk."""
        if self.cache_file.exists():
            try:
                with open(self.cache_file, 'rb') as f:
                    return pickle.load(f)
            except Exception as e:
                print(f"Warning: Could not load cache: {e}", file=sys.stderr)
        return {}

    def _load_metadata(self) -> Dict:
        """Load cache metadata (timestamps, file hashes)."""
        if self.metadata_file.exists():
            try:
                with open(self.metadata_file, 'r') as f:
                    return json.load(f)
            except Exception:
                pass
        return {}

    def _save_cache(self):
        """Save cache to disk."""
        try:
            with open(self.cache_file, 'wb') as f:
                pickle.dump(self.cache, f)
            with open(self.metadata_file, 'w') as f:
                json.dump(self.metadata, f, indent=2)
        except Exception as e:
            print(f"Warning: Could not save cache: {e}", file=sys.stderr)

    def get_key(self, text: str) -> str:
        """Generate cache key from text."""
        return hashlib.md5(text.encode()).hexdigest()

    def get(self, text: str) -> Optional[List[float]]:
        """Get cached embedding for text."""
        key = self.get_key(text)
        return self.cache.get(key)

    def set(self, text: str, embedding: List[float], source: str = ""):
        """Cache an embedding."""
        key = self.get_key(text)
        self.cache[key] = embedding
        self.metadata[key] = {
            'timestamp': datetime.now().isoformat(),
            'source': source,
            'length': len(text)
        }
        self._save_cache()

    def clear_old(self, days: int = 7):
        """Clear cache entries older than specified days."""
        cutoff = datetime.now() - timedelta(days=days)
        keys_to_remove = []

        for key, meta in self.metadata.items():
            try:
                timestamp = datetime.fromisoformat(meta['timestamp'])
                if timestamp < cutoff:
                    keys_to_remove.append(key)
            except (KeyError, ValueError):
                keys_to_remove.append(key)

        for key in keys_to_remove:
            self.cache.pop(key, None)
            self.metadata.pop(key, None)

        if keys_to_remove:
            self._save_cache()
            print(f"Cleared {len(keys_to_remove)} old cache entries", file=sys.stderr)


class SemanticScorer:
    """Semantic similarity scoring with caching."""

    def __init__(self, model_name: str = "all-MiniLM-L6-v2", use_cache: bool = True):
        self.use_cache = use_cache
        self.cache = EmbeddingCache() if use_cache else None

        if HAS_SENTENCE_TRANSFORMERS:
            self.model = SentenceTransformer(model_name)
            self.use_embeddings = True
        else:
            self.model = None
            self.use_embeddings = False
            print("Warning: sentence-transformers not available, using keyword matching",
                  file=sys.stderr)

    def get_embedding(self, text: str, source: str = "") -> Optional[List[float]]:
        """Get embedding for text, using cache if available."""
        if not self.use_embeddings:
            return None

        # Check cache first
        if self.cache:
            cached = self.cache.get(text)
            if cached is not None:
                return cached

        # Compute embedding
        embedding = self.model.encode(text).tolist()

        # Cache it
        if self.cache:
            self.cache.set(text, embedding, source)

        return embedding

    def score_similarity(self, text1: str, text2: str) -> float:
        """Score semantic similarity between two texts (0-1)."""
        if self.use_embeddings:
            emb1 = self.get_embedding(text1)
            emb2 = self.get_embedding(text2)

            if emb1 and emb2:
                # Cosine similarity
                emb1_np = np.array(emb1)
                emb2_np = np.array(emb2)
                similarity = np.dot(emb1_np, emb2_np) / (
                    np.linalg.norm(emb1_np) * np.linalg.norm(emb2_np)
                )
                # Convert from [-1, 1] to [0, 1]
                return float((similarity + 1) / 2)

        # Fallback to keyword matching
        return keyword_similarity(text1, text2)


def estimate_tokens(text: str, model: str = "gpt-4") -> int:
    """Estimate token count for text."""
    if HAS_TIKTOKEN:
        try:
            encoding = tiktoken.encoding_for_model(model)
            return len(encoding.encode(text))
        except Exception:
            pass

    # Fallback: rough estimation (1 token ≈ 4 characters)
    return len(text) // 4


def keyword_similarity(text1: str, text2: str) -> float:
    """Compute keyword-based similarity score (fallback method)."""
    # Extract keywords (words longer than 3 chars, alphanumeric)
    def extract_keywords(text: str) -> Set[str]:
        words = re.findall(r'\b\w+\b', text.lower())
        return {w for w in words if len(w) > 3 and not w.isdigit()}

    keywords1 = extract_keywords(text1)
    keywords2 = extract_keywords(text2)

    if not keywords1 or not keywords2:
        return 0.0

    # Jaccard similarity
    intersection = keywords1 & keywords2
    union = keywords1 | keywords2

    return len(intersection) / len(union) if union else 0.0


def load_context_file(filepath: Path, category: str = "") -> Optional[ContextChunk]:
    """Load a context file into a ContextChunk."""
    if not filepath.exists():
        return None

    try:
        content = filepath.read_text(encoding='utf-8')

        # Extract metadata
        metadata = {
            'filename': filepath.name,
            'modified': datetime.fromtimestamp(filepath.stat().st_mtime).isoformat()
        }

        # Try to extract title from markdown
        lines = content.split('\n')
        for line in lines[:10]:
            if line.startswith('# '):
                metadata['title'] = line[2:].strip()
                break

        return ContextChunk(
            source=str(filepath),
            content=content,
            category=category,
            metadata=metadata
        )
    except Exception as e:
        print(f"Warning: Could not load {filepath}: {e}", file=sys.stderr)
        return None


def discover_context_files() -> List[ContextChunk]:
    """Discover all available context files."""
    chunks = []

    # Context directory
    if CONTEXT_DIR.exists():
        for filepath in CONTEXT_DIR.rglob("*.md"):
            # Determine category from path
            try:
                rel_path = filepath.relative_to(CONTEXT_DIR)
                category = str(rel_path.parts[0]) if len(rel_path.parts) > 1 else "general"
            except ValueError:
                category = "general"

            chunk = load_context_file(filepath, category)
            if chunk:
                chunks.append(chunk)

    # Frameworks directory
    if FRAMEWORKS_DIR.exists():
        for filepath in FRAMEWORKS_DIR.rglob("*.md"):
            try:
                rel_path = filepath.relative_to(FRAMEWORKS_DIR)
                category = f"framework/{rel_path.parts[0]}" if len(rel_path.parts) > 1 else "framework"
            except ValueError:
                category = "framework"

            chunk = load_context_file(filepath, category)
            if chunk:
                chunks.append(chunk)

    # Templates directory
    if TEMPLATES_DIR.exists():
        for filepath in TEMPLATES_DIR.rglob("*.md"):
            chunk = load_context_file(filepath, "template")
            if chunk:
                chunks.append(chunk)

    return chunks


def score_relevance(
    task: str,
    chunks: List[ContextChunk],
    scorer: SemanticScorer,
    boost_categories: Dict[str, float] = None
) -> List[ContextChunk]:
    """Score all chunks by relevance to the task."""
    boost_categories = boost_categories or {}

    for chunk in chunks:
        # Compute base similarity score
        chunk.relevance_score = scorer.score_similarity(task, chunk.content)

        # Apply category boost
        for category_prefix, boost in boost_categories.items():
            if chunk.category.startswith(category_prefix):
                chunk.relevance_score *= (1 + boost)
                break

        # Cap at 1.0
        chunk.relevance_score = min(chunk.relevance_score, 1.0)

    return chunks


def select_context(
    chunks: List[ContextChunk],
    max_tokens: int = 8000,
    top_n: Optional[int] = None,
    min_score: float = 0.1
) -> List[ContextChunk]:
    """Select the most relevant context within token budget."""
    # Filter by minimum score
    filtered = [c for c in chunks if c.relevance_score >= min_score]

    # Sort by relevance
    sorted_chunks = sorted(filtered, key=lambda x: x.relevance_score, reverse=True)

    # Apply top_n limit if specified
    if top_n:
        sorted_chunks = sorted_chunks[:top_n]

    # Select within token budget
    selected = []
    total_tokens = 0

    for chunk in sorted_chunks:
        if total_tokens + chunk.token_count <= max_tokens:
            selected.append(chunk)
            total_tokens += chunk.token_count
        else:
            # Try to compress and fit
            compressed = compress_context(chunk, max_tokens - total_tokens)
            if compressed and compressed.token_count > 0:
                selected.append(compressed)
                total_tokens += compressed.token_count
            break

    return selected


def compress_context(chunk: ContextChunk, max_tokens: int) -> Optional[ContextChunk]:
    """Compress/summarize a context chunk to fit within token budget."""
    if max_tokens <= 0:
        return None

    # Extract key sections (headings and first paragraph of each section)
    lines = chunk.content.split('\n')
    compressed_lines = []
    in_code_block = False
    last_was_heading = False

    for line in lines:
        # Track code blocks
        if line.strip().startswith('```'):
            in_code_block = not in_code_block
            continue

        # Skip code blocks in compression
        if in_code_block:
            continue

        # Keep headings
        if line.startswith('#'):
            compressed_lines.append(line)
            last_was_heading = True
            continue

        # Keep first non-empty line after heading
        if last_was_heading and line.strip():
            compressed_lines.append(line)
            last_was_heading = False
            continue

        last_was_heading = False

    summary = '\n'.join(compressed_lines)

    # If still too long, truncate
    estimated_tokens = estimate_tokens(summary)
    if estimated_tokens > max_tokens:
        # Rough truncation
        chars_to_keep = int(len(summary) * (max_tokens / estimated_tokens))
        summary = summary[:chars_to_keep] + "\n\n[...truncated]"

    return ContextChunk(
        source=chunk.source,
        content=summary,
        relevance_score=chunk.relevance_score,
        token_count=estimate_tokens(summary),
        summary=f"Compressed from {chunk.token_count} to {estimate_tokens(summary)} tokens",
        category=chunk.category,
        metadata=chunk.metadata
    )


def get_dynamic_context() -> Dict[str, str]:
    """Get dynamic context from the environment."""
    context = {}

    # Git status (if in a git repo)
    try:
        result = subprocess.run(
            ['git', 'status', '--short'],
            capture_output=True,
            text=True,
            timeout=2,
            cwd=PROJECT_ROOT
        )
        if result.returncode == 0 and result.stdout.strip():
            context['git_status'] = result.stdout.strip()
    except (subprocess.TimeoutExpired, FileNotFoundError):
        pass

    # Recent git commits
    try:
        result = subprocess.run(
            ['git', 'log', '--oneline', '-5'],
            capture_output=True,
            text=True,
            timeout=2,
            cwd=PROJECT_ROOT
        )
        if result.returncode == 0:
            context['recent_commits'] = result.stdout.strip()
    except (subprocess.TimeoutExpired, FileNotFoundError):
        pass

    # Current branch
    try:
        result = subprocess.run(
            ['git', 'branch', '--show-current'],
            capture_output=True,
            text=True,
            timeout=2,
            cwd=PROJECT_ROOT
        )
        if result.returncode == 0:
            context['git_branch'] = result.stdout.strip()
    except (subprocess.TimeoutExpired, FileNotFoundError):
        pass

    # Recently modified files (last 7 days)
    recent_files = []
    cutoff = datetime.now() - timedelta(days=7)

    for directory in [CONTEXT_DIR, FRAMEWORKS_DIR, TEMPLATES_DIR]:
        if directory.exists():
            for filepath in directory.rglob("*.md"):
                try:
                    mtime = datetime.fromtimestamp(filepath.stat().st_mtime)
                    if mtime > cutoff:
                        recent_files.append(f"{filepath.name} (modified {mtime.strftime('%Y-%m-%d')})")
                except Exception:
                    pass

    if recent_files:
        context['recent_files'] = '\n'.join(sorted(recent_files)[:10])

    # System info
    context['timestamp'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    context['platform'] = sys.platform

    return context


def format_output(
    task: str,
    selected_chunks: List[ContextChunk],
    dynamic_context: Optional[Dict[str, str]] = None,
    include_scores: bool = False
) -> str:
    """Format the selected context into output."""
    sections = []

    # Header
    sections.append("# Smart Context Selection")
    sections.append("")
    sections.append(f"**Task:** {task}")
    sections.append("")

    total_tokens = sum(c.token_count for c in selected_chunks)
    sections.append(f"**Context Selected:** {len(selected_chunks)} chunks, ~{total_tokens} tokens")
    sections.append("")

    # Dynamic context
    if dynamic_context:
        sections.append("## Dynamic Context")
        sections.append("")
        for key, value in dynamic_context.items():
            sections.append(f"### {key.replace('_', ' ').title()}")
            sections.append("```")
            sections.append(value)
            sections.append("```")
            sections.append("")

    # Selected context chunks
    sections.append("---")
    sections.append("")
    sections.append("## Relevant Context")
    sections.append("")

    for i, chunk in enumerate(selected_chunks, 1):
        source_name = Path(chunk.source).name

        header = f"### {i}. {source_name}"
        if include_scores:
            header += f" (score: {chunk.relevance_score:.3f}, tokens: {chunk.token_count})"
        sections.append(header)
        sections.append("")

        if chunk.summary:
            sections.append(f"*{chunk.summary}*")
            sections.append("")

        sections.append(chunk.content)
        sections.append("")

    return '\n'.join(sections)


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Smart context selection with semantic relevance scoring",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Basic usage
  python smart_context.py --task "Design a new n8n workflow for email processing"

  # Limit to top 5 most relevant
  python smart_context.py --task "Debug authentication issues" --top-n 5

  # Set token budget
  python smart_context.py --task "Write technical documentation" --max-tokens 4000

  # Include dynamic context (git status, recent files)
  python smart_context.py --task "Continue development" --include-dynamic

  # Boost specific categories
  python smart_context.py --task "Fix API integration" --boost-category technical=0.5

  # Show relevance scores in output
  python smart_context.py --task "Plan Q1 strategy" --show-scores

  # Export to file
  python smart_context.py --task "Build feature X" -o context.md

  # Clear old cache entries
  python smart_context.py --clear-cache --cache-days 7
        """
    )

    parser.add_argument('--task', required=True, help="Task description for context selection")
    parser.add_argument('--max-tokens', type=int, default=8000,
                       help="Maximum total tokens for selected context (default: 8000)")
    parser.add_argument('--top-n', type=int,
                       help="Limit to top N most relevant chunks")
    parser.add_argument('--min-score', type=float, default=0.1,
                       help="Minimum relevance score to include (0-1, default: 0.1)")
    parser.add_argument('--include-dynamic', action='store_true',
                       help="Include dynamic context (git status, recent files, etc.)")
    parser.add_argument('--boost-category', action='append',
                       help="Boost category relevance (format: category=boost, e.g., technical=0.5)")
    parser.add_argument('--show-scores', action='store_true',
                       help="Show relevance scores in output")
    parser.add_argument('--output', '-o', type=Path,
                       help="Output file (default: stdout)")
    parser.add_argument('--no-cache', action='store_true',
                       help="Disable embedding cache")
    parser.add_argument('--clear-cache', action='store_true',
                       help="Clear old cache entries and exit")
    parser.add_argument('--cache-days', type=int, default=7,
                       help="Cache retention in days (default: 7)")
    parser.add_argument('--model', default='all-MiniLM-L6-v2',
                       help="Sentence transformer model (default: all-MiniLM-L6-v2)")
    parser.add_argument('--verbose', '-v', action='store_true',
                       help="Verbose output")

    args = parser.parse_args()

    # Handle cache clearing
    if args.clear_cache:
        cache = EmbeddingCache()
        cache.clear_old(args.cache_days)
        print(f"Cache cleared (older than {args.cache_days} days)")
        return

    # Parse category boosts
    boost_categories = {}
    if args.boost_category:
        for boost_spec in args.boost_category:
            try:
                category, boost_str = boost_spec.split('=')
                boost_categories[category.strip()] = float(boost_str.strip())
            except ValueError:
                print(f"Warning: Invalid boost format: {boost_spec}", file=sys.stderr)

    if args.verbose:
        print(f"Task: {args.task}", file=sys.stderr)
        print(f"Max tokens: {args.max_tokens}", file=sys.stderr)
        if boost_categories:
            print(f"Category boosts: {boost_categories}", file=sys.stderr)

    # Initialize scorer
    if args.verbose:
        print("Initializing semantic scorer...", file=sys.stderr)

    scorer = SemanticScorer(
        model_name=args.model,
        use_cache=not args.no_cache
    )

    # Discover context files
    if args.verbose:
        print("Discovering context files...", file=sys.stderr)

    chunks = discover_context_files()

    if args.verbose:
        print(f"Found {len(chunks)} context files", file=sys.stderr)

    # Score relevance
    if args.verbose:
        print("Scoring relevance...", file=sys.stderr)

    scored_chunks = score_relevance(args.task, chunks, scorer, boost_categories)

    # Select best context
    if args.verbose:
        print("Selecting optimal context...", file=sys.stderr)

    selected = select_context(
        scored_chunks,
        max_tokens=args.max_tokens,
        top_n=args.top_n,
        min_score=args.min_score
    )

    if args.verbose:
        print(f"Selected {len(selected)} chunks", file=sys.stderr)
        total_tokens = sum(c.token_count for c in selected)
        print(f"Total tokens: {total_tokens}", file=sys.stderr)

    # Get dynamic context if requested
    dynamic = None
    if args.include_dynamic:
        if args.verbose:
            print("Gathering dynamic context...", file=sys.stderr)
        dynamic = get_dynamic_context()

    # Format output
    output = format_output(args.task, selected, dynamic, args.show_scores)

    # Write output
    if args.output:
        args.output.write_text(output, encoding='utf-8')
        print(f"Context written to {args.output}", file=sys.stderr)
    else:
        print(output)


if __name__ == '__main__':
    main()
