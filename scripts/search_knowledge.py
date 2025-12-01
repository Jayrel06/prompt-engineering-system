#!/usr/bin/env python3
"""
Search the Qdrant vector database for relevant content.

This script performs semantic search on embedded content using vector similarity.
Supports filtering by category and returns ranked results with metadata.
"""

import argparse
import sys
from typing import List, Dict, Any, Optional

from qdrant_client import QdrantClient
from qdrant_client.models import Filter, FieldCondition, MatchValue
from sentence_transformers import SentenceTransformer


class SearchService:
    """Service for searching embedded content in Qdrant."""

    def __init__(
        self,
        qdrant_host: str = "localhost",
        qdrant_port: int = 6333,
        model_name: str = "all-MiniLM-L6-v2",
        collection_name: str = "prompt_context"
    ):
        """
        Initialize the search service.

        Args:
            qdrant_host: Qdrant server host
            qdrant_port: Qdrant server port
            model_name: Sentence transformer model name (must match embedding model)
            collection_name: Name of the Qdrant collection to search
        """
        self.collection_name = collection_name

        print(f"Loading embedding model: {model_name}...")
        try:
            self.model = SentenceTransformer(model_name)
            print("Model loaded successfully.")
        except Exception as e:
            print(f"Error loading model: {e}", file=sys.stderr)
            sys.exit(1)

        print(f"Connecting to Qdrant at {qdrant_host}:{qdrant_port}...")
        try:
            self.client = QdrantClient(host=qdrant_host, port=qdrant_port)
            print("Connected to Qdrant successfully.")
        except Exception as e:
            print(f"Error connecting to Qdrant: {e}", file=sys.stderr)
            print("Make sure Qdrant is running on localhost:6333", file=sys.stderr)
            sys.exit(1)

        self._verify_collection_exists()

    def _verify_collection_exists(self) -> None:
        """Verify that the collection exists."""
        try:
            collections = self.client.get_collections().collections
            collection_names = [col.name for col in collections]

            if self.collection_name not in collection_names:
                print(f"Error: Collection '{self.collection_name}' does not exist.", file=sys.stderr)
                print("Run embed_output.py first to create and populate the collection.", file=sys.stderr)
                sys.exit(1)

            # Get collection info
            info = self.client.get_collection(self.collection_name)
            print(f"Collection '{self.collection_name}' contains {info.points_count} points")

        except Exception as e:
            print(f"Error verifying collection: {e}", file=sys.stderr)
            sys.exit(1)

    def search(
        self,
        query: str,
        limit: int = 5,
        category: Optional[str] = None,
        score_threshold: float = 0.0
    ) -> List[Dict[str, Any]]:
        """
        Search for similar content using semantic search.

        Args:
            query: Search query text
            limit: Maximum number of results to return
            category: Optional category filter
            score_threshold: Minimum similarity score (0.0 to 1.0)

        Returns:
            List of search results with score, text, and metadata
        """
        if not query.strip():
            raise ValueError("Query cannot be empty")

        print(f"\nEmbedding query: '{query}'...")
        try:
            query_vector = self.model.encode(query).tolist()
            print(f"Query embedded (dimension: {len(query_vector)})")
        except Exception as e:
            print(f"Error embedding query: {e}", file=sys.stderr)
            raise

        # Build filter if category specified
        search_filter = None
        if category:
            print(f"Filtering by category: {category}")
            search_filter = Filter(
                must=[
                    FieldCondition(
                        key="category",
                        match=MatchValue(value=category)
                    )
                ]
            )

        print(f"Searching for top {limit} results...")
        try:
            search_results = self.client.search(
                collection_name=self.collection_name,
                query_vector=query_vector,
                limit=limit,
                query_filter=search_filter,
                score_threshold=score_threshold
            )

            print(f"Found {len(search_results)} results")

        except Exception as e:
            print(f"Error searching: {e}", file=sys.stderr)
            raise

        # Format results
        results = []
        for hit in search_results:
            result = {
                "id": hit.id,
                "score": hit.score,
                "text": hit.payload.get("text", ""),
                "category": hit.payload.get("category", "unknown"),
                "tags": hit.payload.get("tags", []),
                "timestamp": hit.payload.get("timestamp", ""),
                "source_file": hit.payload.get("source_file", "unknown"),
                "text_length": hit.payload.get("text_length", 0)
            }
            results.append(result)

        return results


def format_result(result: Dict[str, Any], index: int, show_full_text: bool = False) -> str:
    """
    Format a search result for terminal display.

    Args:
        result: Search result dictionary
        index: Result index (1-based)
        show_full_text: Whether to show full text or snippet

    Returns:
        Formatted string for display
    """
    lines = []
    lines.append(f"\n{'=' * 80}")
    lines.append(f"RESULT #{index} (Score: {result['score']:.4f})")
    lines.append(f"{'=' * 80}")

    # Metadata
    lines.append(f"Category: {result['category']}")
    lines.append(f"Tags: {', '.join(result['tags']) if result['tags'] else 'none'}")
    lines.append(f"Source: {result['source_file']}")
    lines.append(f"Timestamp: {result['timestamp']}")
    lines.append(f"ID: {result['id']}")

    # Text content
    lines.append(f"\n{'-' * 80}")
    lines.append("CONTENT:")
    lines.append(f"{'-' * 80}")

    text = result['text']
    if show_full_text or len(text) <= 500:
        lines.append(text)
    else:
        # Show snippet with ellipsis
        snippet = text[:500].strip()
        lines.append(f"{snippet}...")
        lines.append(f"\n[Showing 500 of {result['text_length']} characters. Use --full to see complete text]")

    return '\n'.join(lines)


def main():
    """Main entry point for the script."""
    parser = argparse.ArgumentParser(
        description="Search the Qdrant vector database for relevant content",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Basic search
  python search_knowledge.py --query "how to write effective prompts"

  # Search with limit
  python search_knowledge.py --query "Claude prompt examples" --limit 10

  # Search within category
  python search_knowledge.py --query "few-shot examples" --category template

  # Show full text
  python search_knowledge.py --query "prompt framework" --full
        """
    )

    # Required arguments
    parser.add_argument(
        "--query",
        type=str,
        required=True,
        help="Search query text"
    )

    # Optional arguments
    parser.add_argument(
        "--limit",
        type=int,
        default=5,
        help="Maximum number of results to return (default: 5)"
    )
    parser.add_argument(
        "--category",
        type=str,
        choices=["framework", "template", "output", "learning"],
        help="Filter by category"
    )
    parser.add_argument(
        "--threshold",
        type=float,
        default=0.0,
        help="Minimum similarity score threshold 0.0-1.0 (default: 0.0)"
    )
    parser.add_argument(
        "--full",
        action="store_true",
        help="Show full text instead of snippets"
    )

    # Connection arguments
    parser.add_argument(
        "--host",
        type=str,
        default="localhost",
        help="Qdrant host (default: localhost)"
    )
    parser.add_argument(
        "--port",
        type=int,
        default=6333,
        help="Qdrant port (default: 6333)"
    )

    args = parser.parse_args()

    # Validate threshold
    if not 0.0 <= args.threshold <= 1.0:
        print("Error: Threshold must be between 0.0 and 1.0", file=sys.stderr)
        sys.exit(1)

    # Initialize service and search
    try:
        service = SearchService(
            qdrant_host=args.host,
            qdrant_port=args.port
        )

        print("\n" + "=" * 80)
        print("SEMANTIC SEARCH")
        print("=" * 80)
        print(f"Query: {args.query}")
        if args.category:
            print(f"Category Filter: {args.category}")
        if args.threshold > 0.0:
            print(f"Score Threshold: {args.threshold}")

        results = service.search(
            query=args.query,
            limit=args.limit,
            category=args.category,
            score_threshold=args.threshold
        )

        if not results:
            print("\n" + "=" * 80)
            print("No results found.")
            print("=" * 80)
            print("\nTry:")
            print("  - Using different search terms")
            print("  - Removing category filters")
            print("  - Lowering the score threshold")
            return

        # Display results
        for i, result in enumerate(results, 1):
            print(format_result(result, i, show_full_text=args.full))

        # Summary
        print("\n" + "=" * 80)
        print("SEARCH SUMMARY")
        print("=" * 80)
        print(f"Total results: {len(results)}")
        print(f"Average score: {sum(r['score'] for r in results) / len(results):.4f}")
        print(f"Top score: {results[0]['score']:.4f}")
        if len(results) > 1:
            print(f"Lowest score: {results[-1]['score']:.4f}")

    except Exception as e:
        print(f"\nSearch failed: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
