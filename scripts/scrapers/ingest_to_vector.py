#!/usr/bin/env python3
"""
Ingest scraped Reddit and GitHub data into Qdrant vector database.

This script processes scraped data from Reddit posts and GitHub repositories,
chunks content appropriately, and stores it in Qdrant with rich metadata for
the prompt engineering system.

Usage:
    python ingest_to_vector.py --source reddit
    python ingest_to_vector.py --source github
    python ingest_to_vector.py --all
    python ingest_to_vector.py --file data/reddit/specific.json
"""

import argparse
import hashlib
import json
import re
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Set, Any
from collections import defaultdict

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))
from embed_output import EmbeddingService


# Configuration
SCRIPT_DIR = Path(__file__).parent
PROJECT_ROOT = SCRIPT_DIR.parent.parent
DATA_DIR = PROJECT_ROOT / "data"
REDDIT_DIR = DATA_DIR / "reddit"
GITHUB_DIR = DATA_DIR / "github"

# Chunking parameters
MAX_TOKENS = 1000  # Max tokens per chunk (roughly 750 words)
MAX_CHARS = 4000   # Approximate character limit per chunk
OVERLAP_CHARS = 200  # Overlap between chunks for context

# Quality thresholds
MIN_CONTENT_LENGTH = 50  # Skip very short content
MIN_REDDIT_SCORE = 3     # Skip low-quality posts


class ContentChunker:
    """Intelligently chunk long content into smaller pieces."""

    @staticmethod
    def estimate_tokens(text: str) -> int:
        """Estimate token count (rough approximation)."""
        # Rough estimate: 1 token ≈ 4 characters
        return len(text) // 4

    @staticmethod
    def chunk_text(text: str, max_chars: int = MAX_CHARS, overlap: int = OVERLAP_CHARS) -> List[str]:
        """
        Split text into chunks with overlap.

        Args:
            text: Text to chunk
            max_chars: Maximum characters per chunk
            overlap: Characters to overlap between chunks

        Returns:
            List of text chunks
        """
        if len(text) <= max_chars:
            return [text]

        chunks = []
        start = 0

        while start < len(text):
            # Calculate end position
            end = start + max_chars

            # If this is not the last chunk, try to break at a sentence boundary
            if end < len(text):
                # Look for sentence endings in the last 200 characters of the chunk
                chunk_end = text[max(start, end - 200):end]
                sentence_endings = ['. ', '.\n', '! ', '!\n', '? ', '?\n']

                best_break = -1
                for ending in sentence_endings:
                    pos = chunk_end.rfind(ending)
                    if pos > best_break:
                        best_break = pos

                if best_break > -1:
                    # Adjust end to the sentence boundary
                    end = max(start, end - 200) + best_break + 1

            chunk = text[start:end].strip()
            if chunk:
                chunks.append(chunk)

            # Move start position (with overlap)
            start = end - overlap if end < len(text) else end

        return chunks


class DataIngestor:
    """Ingest scraped data into Qdrant vector database."""

    def __init__(self, embedding_service: EmbeddingService, dry_run: bool = False):
        """
        Initialize the ingestor.

        Args:
            embedding_service: EmbeddingService instance
            dry_run: If True, don't actually store in database
        """
        self.service = embedding_service
        self.dry_run = dry_run
        self.chunker = ContentChunker()

        # Track statistics
        self.stats = {
            'total_items': 0,
            'total_chunks': 0,
            'duplicates_skipped': 0,
            'errors': 0,
            'reddit_posts': 0,
            'reddit_comments': 0,
            'github_repos': 0,
            'github_prompts': 0,
        }

        # Track content hashes to avoid duplicates
        self.seen_hashes: Set[str] = set()
        self.error_log: List[Dict[str, str]] = []

    def _compute_hash(self, content: str) -> str:
        """Compute SHA-256 hash of content for deduplication."""
        return hashlib.sha256(content.encode('utf-8')).hexdigest()

    def _is_duplicate(self, content: str) -> bool:
        """Check if content is a duplicate."""
        content_hash = self._compute_hash(content)
        if content_hash in self.seen_hashes:
            return True
        self.seen_hashes.add(content_hash)
        return False

    def _extract_keywords(self, text: str, max_keywords: int = 10) -> List[str]:
        """
        Extract relevant keywords from text.

        Args:
            text: Text to extract keywords from
            max_keywords: Maximum number of keywords to extract

        Returns:
            List of keywords
        """
        # Simple keyword extraction based on frequency and relevance
        # Remove common words and extract meaningful terms

        # Common stop words to ignore
        stop_words = {
            'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
            'of', 'with', 'by', 'from', 'as', 'is', 'was', 'are', 'were', 'been',
            'be', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would',
            'should', 'could', 'may', 'might', 'must', 'can', 'this', 'that',
            'these', 'those', 'i', 'you', 'he', 'she', 'it', 'we', 'they',
            'what', 'which', 'who', 'when', 'where', 'why', 'how'
        }

        # Tokenize and count words
        words = re.findall(r'\b[a-zA-Z]{3,}\b', text.lower())
        word_freq = defaultdict(int)

        for word in words:
            if word not in stop_words:
                word_freq[word] += 1

        # Sort by frequency and return top keywords
        sorted_words = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)
        return [word for word, _ in sorted_words[:max_keywords]]

    def _store_chunk(
        self,
        content: str,
        tags: List[str],
        category: str,
        metadata: Dict[str, Any]
    ) -> bool:
        """
        Store a single chunk in the vector database.

        Args:
            content: Text content to store
            tags: Tags for the content
            category: Category (reddit/github)
            metadata: Additional metadata

        Returns:
            True if stored successfully, False otherwise
        """
        try:
            if self.dry_run:
                print(f"  [DRY RUN] Would store chunk ({len(content)} chars, {len(tags)} tags)")
                return True

            # Store in Qdrant
            self.service.embed_and_store(
                text=content,
                tags=tags,
                category=category,
                source_file=metadata.get('source_file', 'unknown')
            )
            return True

        except Exception as e:
            self.stats['errors'] += 1
            error_msg = f"Error storing chunk: {str(e)}"
            print(f"  ERROR: {error_msg}")
            self.error_log.append({
                'error': error_msg,
                'content_preview': content[:100],
                'metadata': str(metadata)
            })
            return False

    def ingest_reddit_post(self, post: Dict, source_file: str) -> int:
        """
        Ingest a Reddit post into the vector database.

        Args:
            post: Reddit post data
            source_file: Source JSON file path

        Returns:
            Number of chunks stored
        """
        chunks_stored = 0

        # Extract post data
        post_id = post.get('id', 'unknown')
        title = post.get('title', '')
        body = post.get('body', '')
        subreddit = post.get('subreddit', 'unknown')
        score = post.get('score', 0)
        url = post.get('permalink', '')
        created_date = post.get('created_date', '')
        author = post.get('author', 'unknown')

        # Apply quality filter
        if score < MIN_REDDIT_SCORE:
            return 0

        # Combine title and body
        full_content = f"{title}\n\n{body}".strip()

        if len(full_content) < MIN_CONTENT_LENGTH:
            return 0

        # Check for duplicates
        if self._is_duplicate(full_content):
            self.stats['duplicates_skipped'] += 1
            return 0

        # Extract keywords
        keywords = self._extract_keywords(full_content)

        # Chunk the content
        chunks = self.chunker.chunk_text(full_content)

        # Process each chunk
        for i, chunk in enumerate(chunks):
            # Build tags
            tags = [subreddit] + keywords[:5]

            # Add specific tags based on content
            if 'prompt' in chunk.lower():
                tags.append('prompts')
            if any(word in chunk.lower() for word in ['claude', 'chatgpt', 'gpt-4', 'llm']):
                tags.append('llm')
            if 'code' in chunk.lower() or '```' in chunk:
                tags.append('code')

            # Remove duplicates from tags
            tags = list(set(tags))

            # Store the chunk
            metadata = {
                'source_file': source_file,
                'post_id': post_id,
                'url': url,
                'score': score,
                'author': author,
                'created_date': created_date,
                'chunk_index': i,
                'total_chunks': len(chunks)
            }

            if self._store_chunk(chunk, tags, 'reddit', metadata):
                chunks_stored += 1
                self.stats['total_chunks'] += 1

        # Process extracted prompts
        for prompt in post.get('extracted_prompts', []):
            if len(prompt) >= MIN_CONTENT_LENGTH and not self._is_duplicate(prompt):
                tags = [subreddit, 'extracted-prompt'] + keywords[:3]
                metadata = {
                    'source_file': source_file,
                    'post_id': post_id,
                    'url': url,
                    'type': 'extracted_prompt'
                }

                if self._store_chunk(prompt, tags, 'reddit', metadata):
                    chunks_stored += 1
                    self.stats['total_chunks'] += 1

        # Process top comments
        for comment in post.get('top_comments', []):
            comment_body = comment.get('body', '')
            if len(comment_body) >= MIN_CONTENT_LENGTH and not self._is_duplicate(comment_body):
                comment_chunks = self.chunker.chunk_text(comment_body)

                for i, chunk in enumerate(comment_chunks):
                    tags = [subreddit, 'comment'] + self._extract_keywords(chunk)[:3]
                    metadata = {
                        'source_file': source_file,
                        'post_id': post_id,
                        'comment_author': comment.get('author', 'unknown'),
                        'comment_score': comment.get('score', 0),
                        'chunk_index': i,
                        'type': 'comment'
                    }

                    if self._store_chunk(chunk, tags, 'reddit', metadata):
                        chunks_stored += 1
                        self.stats['total_chunks'] += 1
                        self.stats['reddit_comments'] += 1

        self.stats['reddit_posts'] += 1
        return chunks_stored

    def ingest_github_repo(self, repo: Dict, source_file: str) -> int:
        """
        Ingest a GitHub repository into the vector database.

        Args:
            repo: GitHub repository data
            source_file: Source JSON file path

        Returns:
            Number of chunks stored
        """
        chunks_stored = 0

        # Extract repo data
        repo_name = repo.get('repo', 'unknown')
        description = repo.get('description', '')
        topics = repo.get('topics', [])
        stars = repo.get('stars', 0)
        url = repo.get('url', '')
        language = repo.get('language', 'unknown')

        # Process README content
        readme = repo.get('readme_content', '')
        if readme and len(readme) >= MIN_CONTENT_LENGTH:
            if not self._is_duplicate(readme):
                chunks = self.chunker.chunk_text(readme)

                for i, chunk in enumerate(chunks):
                    # Build tags from topics and keywords
                    keywords = self._extract_keywords(chunk, max_keywords=5)
                    tags = topics[:5] + keywords[:5] + ['readme']

                    # Add language tag if available
                    if language and language != 'unknown':
                        tags.append(language.lower())

                    tags = list(set(tags))

                    metadata = {
                        'source_file': source_file,
                        'repo': repo_name,
                        'url': url,
                        'stars': stars,
                        'language': language,
                        'type': 'readme',
                        'chunk_index': i,
                        'total_chunks': len(chunks)
                    }

                    if self._store_chunk(chunk, tags, 'github', metadata):
                        chunks_stored += 1
                        self.stats['total_chunks'] += 1

        # Process extracted prompts
        for prompt_data in repo.get('extracted_prompts', []):
            prompt_content = prompt_data.get('content', '')
            prompt_type = prompt_data.get('type', 'unknown')
            prompt_title = prompt_data.get('title', '')

            if len(prompt_content) >= MIN_CONTENT_LENGTH and not self._is_duplicate(prompt_content):
                # Combine title and content if available
                full_prompt = f"{prompt_title}\n\n{prompt_content}" if prompt_title else prompt_content

                chunks = self.chunker.chunk_text(full_prompt)

                for i, chunk in enumerate(chunks):
                    keywords = self._extract_keywords(chunk, max_keywords=5)
                    tags = topics[:3] + keywords[:5] + ['extracted-prompt', prompt_type]
                    tags = list(set(tags))

                    metadata = {
                        'source_file': source_file,
                        'repo': repo_name,
                        'url': url,
                        'stars': stars,
                        'prompt_type': prompt_type,
                        'prompt_title': prompt_title,
                        'chunk_index': i,
                        'type': 'extracted_prompt'
                    }

                    if self._store_chunk(chunk, tags, 'github', metadata):
                        chunks_stored += 1
                        self.stats['total_chunks'] += 1
                        self.stats['github_prompts'] += 1

        # Process prompt files
        for file_data in repo.get('prompt_files', []):
            file_path = file_data.get('path', '')
            file_content = file_data.get('content', '')

            if len(file_content) >= MIN_CONTENT_LENGTH and not self._is_duplicate(file_content):
                chunks = self.chunker.chunk_text(file_content)

                for i, chunk in enumerate(chunks):
                    keywords = self._extract_keywords(chunk, max_keywords=5)
                    tags = topics[:3] + keywords[:5] + ['prompt-file']
                    tags = list(set(tags))

                    metadata = {
                        'source_file': source_file,
                        'repo': repo_name,
                        'url': url,
                        'stars': stars,
                        'file_path': file_path,
                        'chunk_index': i,
                        'type': 'prompt_file'
                    }

                    if self._store_chunk(chunk, tags, 'github', metadata):
                        chunks_stored += 1
                        self.stats['total_chunks'] += 1

        self.stats['github_repos'] += 1
        return chunks_stored

    def ingest_file(self, filepath: Path) -> int:
        """
        Ingest a single JSON file.

        Args:
            filepath: Path to JSON file

        Returns:
            Number of chunks stored
        """
        print(f"\nProcessing: {filepath.name}")

        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except Exception as e:
            print(f"  ERROR: Failed to load file: {e}")
            self.stats['errors'] += 1
            self.error_log.append({
                'error': f'Failed to load file: {e}',
                'file': str(filepath)
            })
            return 0

        chunks_stored = 0
        source_file = str(filepath.absolute())

        # Determine if this is Reddit or GitHub data
        if 'reddit' in str(filepath).lower():
            # Process Reddit data
            if isinstance(data, list):
                for post in data:
                    self.stats['total_items'] += 1
                    chunks = self.ingest_reddit_post(post, source_file)
                    chunks_stored += chunks

                    # Progress indicator
                    if self.stats['total_items'] % 10 == 0:
                        print(f"  Processed {self.stats['total_items']} items, stored {self.stats['total_chunks']} chunks...")
            elif isinstance(data, dict):
                self.stats['total_items'] += 1
                chunks_stored = self.ingest_reddit_post(data, source_file)

        elif 'github' in str(filepath).lower():
            # Process GitHub data
            if isinstance(data, list):
                for repo in data:
                    self.stats['total_items'] += 1
                    chunks = self.ingest_github_repo(repo, source_file)
                    chunks_stored += chunks

                    # Progress indicator
                    if self.stats['total_items'] % 5 == 0:
                        print(f"  Processed {self.stats['total_items']} items, stored {self.stats['total_chunks']} chunks...")
            elif isinstance(data, dict):
                self.stats['total_items'] += 1
                chunks_stored = self.ingest_github_repo(data, source_file)

        else:
            print(f"  WARNING: Could not determine data type (reddit/github) from path")
            return 0

        print(f"  Stored {chunks_stored} chunks from this file")
        return chunks_stored

    def ingest_directory(self, directory: Path, pattern: str = "*.json") -> int:
        """
        Ingest all JSON files in a directory.

        Args:
            directory: Directory to search
            pattern: File pattern to match

        Returns:
            Total number of chunks stored
        """
        if not directory.exists():
            print(f"ERROR: Directory does not exist: {directory}")
            return 0

        json_files = list(directory.glob(pattern))

        if not json_files:
            print(f"No JSON files found in {directory}")
            return 0

        print(f"\nFound {len(json_files)} JSON files in {directory}")

        total_chunks = 0
        for filepath in json_files:
            chunks = self.ingest_file(filepath)
            total_chunks += chunks

        return total_chunks

    def print_summary(self):
        """Print ingestion summary."""
        print("\n" + "=" * 70)
        print("INGESTION SUMMARY")
        print("=" * 70)
        print(f"Total items processed:      {self.stats['total_items']}")
        print(f"Total chunks stored:        {self.stats['total_chunks']}")
        print(f"Duplicates skipped:         {self.stats['duplicates_skipped']}")
        print(f"Errors encountered:         {self.stats['errors']}")
        print()
        print(f"Reddit posts ingested:      {self.stats['reddit_posts']}")
        print(f"Reddit comments ingested:   {self.stats['reddit_comments']}")
        print(f"GitHub repos ingested:      {self.stats['github_repos']}")
        print(f"GitHub prompts extracted:   {self.stats['github_prompts']}")

        if self.error_log:
            print("\n" + "-" * 70)
            print(f"ERRORS ({len(self.error_log)} total):")
            print("-" * 70)
            for i, error in enumerate(self.error_log[:10], 1):  # Show first 10 errors
                print(f"{i}. {error.get('error', 'Unknown error')}")
                if 'file' in error:
                    print(f"   File: {error['file']}")

            if len(self.error_log) > 10:
                print(f"... and {len(self.error_log) - 10} more errors")

        print("=" * 70)


def main():
    """Main CLI interface."""
    parser = argparse.ArgumentParser(
        description="Ingest scraped Reddit and GitHub data into Qdrant vector database",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Ingest all Reddit data
  python ingest_to_vector.py --source reddit

  # Ingest all GitHub data
  python ingest_to_vector.py --source github

  # Ingest everything
  python ingest_to_vector.py --all

  # Ingest a specific file
  python ingest_to_vector.py --file data/reddit/specific.json

  # Dry run to see what would be ingested
  python ingest_to_vector.py --source reddit --dry-run

Connection:
  Uses the existing EmbeddingService from embed_output.py
  Connects to Qdrant at localhost:6333 by default
  Stores in the 'prompt_context' collection
        """
    )

    # Source selection
    source_group = parser.add_mutually_exclusive_group()
    source_group.add_argument(
        '--source',
        choices=['reddit', 'github'],
        help='Ingest data from a specific source'
    )
    source_group.add_argument(
        '--all',
        action='store_true',
        help='Ingest all available data (Reddit and GitHub)'
    )
    source_group.add_argument(
        '--file',
        type=Path,
        help='Ingest a specific JSON file'
    )

    # Connection options
    parser.add_argument(
        '--host',
        type=str,
        default='localhost',
        help='Qdrant host (default: localhost)'
    )
    parser.add_argument(
        '--port',
        type=int,
        default=6333,
        help='Qdrant port (default: 6333)'
    )

    # Other options
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Dry run - process but do not store in database'
    )
    parser.add_argument(
        '--data-dir',
        type=Path,
        help=f'Data directory (default: {DATA_DIR})'
    )

    args = parser.parse_args()

    # Validate arguments
    if not any([args.source, args.all, args.file]):
        parser.error("Must specify --source, --all, or --file")

    # Determine data directory
    data_dir = args.data_dir if args.data_dir else DATA_DIR
    reddit_dir = data_dir / "reddit"
    github_dir = data_dir / "github"

    print("=" * 70)
    print("VECTOR DATABASE INGESTION")
    print("=" * 70)
    print(f"Data directory: {data_dir}")
    print(f"Qdrant: {args.host}:{args.port}")
    print(f"Dry run: {args.dry_run}")
    print("=" * 70)

    # Initialize embedding service
    try:
        service = EmbeddingService(
            qdrant_host=args.host,
            qdrant_port=args.port
        )
    except Exception as e:
        print(f"\nERROR: Failed to initialize embedding service: {e}")
        print("Make sure Qdrant is running and accessible.")
        sys.exit(1)

    # Initialize ingestor
    ingestor = DataIngestor(service, dry_run=args.dry_run)

    # Perform ingestion
    try:
        if args.file:
            # Ingest single file
            if not args.file.exists():
                print(f"ERROR: File not found: {args.file}")
                sys.exit(1)

            ingestor.ingest_file(args.file)

        elif args.source:
            # Ingest from specific source
            if args.source == 'reddit':
                ingestor.ingest_directory(reddit_dir)
            elif args.source == 'github':
                ingestor.ingest_directory(github_dir)

        elif args.all:
            # Ingest everything
            print("\n>>> Ingesting Reddit data...")
            ingestor.ingest_directory(reddit_dir)

            print("\n>>> Ingesting GitHub data...")
            ingestor.ingest_directory(github_dir)

        # Print summary
        ingestor.print_summary()

        # Get collection info
        if not args.dry_run:
            print("\n>>> Collection Status:")
            info = service.get_collection_info()
            if info:
                print(f"Collection: {info['name']}")
                print(f"Total points: {info['points_count']}")
                print(f"Total vectors: {info['vectors_count']}")

        print("\nIngestion completed successfully!")

    except KeyboardInterrupt:
        print("\n\nIngestion interrupted by user.")
        ingestor.print_summary()
        sys.exit(1)
    except Exception as e:
        print(f"\nERROR: Ingestion failed: {e}")
        import traceback
        traceback.print_exc()
        ingestor.print_summary()
        sys.exit(1)


if __name__ == "__main__":
    main()
