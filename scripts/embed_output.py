#!/usr/bin/env python3
"""
Embed and store content in Qdrant vector database.

This script embeds text content using sentence-transformers and stores it in a Qdrant
collection for later retrieval. Supports both file and direct text input with metadata.
"""

import argparse
import sys
from datetime import datetime
from pathlib import Path
from typing import List, Optional

from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
from sentence_transformers import SentenceTransformer


class EmbeddingService:
    """Service for embedding text and storing in Qdrant."""

    def __init__(
        self,
        qdrant_host: str = "localhost",
        qdrant_port: int = 6333,
        model_name: str = "all-MiniLM-L6-v2",
        collection_name: str = "prompt_context"
    ):
        """
        Initialize the embedding service.

        Args:
            qdrant_host: Qdrant server host
            qdrant_port: Qdrant server port
            model_name: Sentence transformer model name
            collection_name: Name of the Qdrant collection
        """
        self.collection_name = collection_name

        print(f"Initializing embedding model: {model_name}...")
        try:
            self.model = SentenceTransformer(model_name)
            self.embedding_size = self.model.get_sentence_embedding_dimension()
            print(f"Model loaded successfully. Embedding size: {self.embedding_size}")
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

        self._ensure_collection_exists()

    def _ensure_collection_exists(self) -> None:
        """Create collection if it doesn't exist."""
        try:
            collections = self.client.get_collections().collections
            collection_names = [col.name for col in collections]

            if self.collection_name not in collection_names:
                print(f"Creating collection '{self.collection_name}'...")
                self.client.create_collection(
                    collection_name=self.collection_name,
                    vectors_config=VectorParams(
                        size=self.embedding_size,
                        distance=Distance.COSINE
                    )
                )
                print(f"Collection '{self.collection_name}' created successfully.")
            else:
                print(f"Collection '{self.collection_name}' already exists.")
        except Exception as e:
            print(f"Error ensuring collection exists: {e}", file=sys.stderr)
            sys.exit(1)

    def embed_and_store(
        self,
        text: str,
        tags: Optional[List[str]] = None,
        category: Optional[str] = None,
        source_file: Optional[str] = None
    ) -> str:
        """
        Embed text and store in Qdrant.

        Args:
            text: Text content to embed
            tags: Optional list of tags for metadata
            category: Optional category (framework/template/output/learning)
            source_file: Optional source file path

        Returns:
            Point ID of the stored vector
        """
        if not text.strip():
            raise ValueError("Text content cannot be empty")

        print("\nEmbedding text...")
        try:
            embedding = self.model.encode(text).tolist()
            print(f"Generated embedding vector (dimension: {len(embedding)})")
        except Exception as e:
            print(f"Error generating embedding: {e}", file=sys.stderr)
            raise

        # Prepare metadata
        metadata = {
            "text": text,
            "timestamp": datetime.utcnow().isoformat(),
            "tags": tags or [],
            "category": category or "uncategorized",
            "source_file": source_file or "direct_input",
            "text_length": len(text)
        }

        # Generate unique point ID based on timestamp and text hash
        point_id = abs(hash(f"{metadata['timestamp']}_{text[:100]}")) % (10 ** 10)

        print(f"Storing in Qdrant (ID: {point_id})...")
        try:
            point = PointStruct(
                id=point_id,
                vector=embedding,
                payload=metadata
            )

            self.client.upsert(
                collection_name=self.collection_name,
                points=[point]
            )
            print(f"Successfully stored vector with ID: {point_id}")

        except Exception as e:
            print(f"Error storing vector: {e}", file=sys.stderr)
            raise

        return str(point_id)

    def get_collection_info(self) -> dict:
        """Get information about the collection."""
        try:
            info = self.client.get_collection(self.collection_name)
            return {
                "name": self.collection_name,
                "vectors_count": info.vectors_count,
                "points_count": info.points_count
            }
        except Exception as e:
            print(f"Error getting collection info: {e}", file=sys.stderr)
            return {}


def main():
    """Main entry point for the script."""
    parser = argparse.ArgumentParser(
        description="Embed and store content in Qdrant vector database",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Embed text directly
  python embed_output.py --text "This is a prompt template" --category template --tags prompt,example

  # Embed from file
  python embed_output.py --file prompts/example.txt --category framework --tags claude,prompt-engineering

Categories:
  - framework: Prompt engineering frameworks
  - template: Reusable prompt templates
  - output: Example outputs or responses
  - learning: Learning resources or notes
        """
    )

    # Input group (mutually exclusive)
    input_group = parser.add_mutually_exclusive_group(required=True)
    input_group.add_argument(
        "--file",
        type=str,
        help="Path to file containing text to embed"
    )
    input_group.add_argument(
        "--text",
        type=str,
        help="Direct text input to embed"
    )

    # Metadata arguments
    parser.add_argument(
        "--tags",
        type=str,
        help="Comma-separated tags for metadata (e.g., 'prompt,example,claude')"
    )
    parser.add_argument(
        "--category",
        type=str,
        choices=["framework", "template", "output", "learning"],
        help="Category for the content"
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

    # Get text content
    if args.file:
        file_path = Path(args.file)
        if not file_path.exists():
            print(f"Error: File not found: {args.file}", file=sys.stderr)
            sys.exit(1)

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                text = f.read()
            print(f"Loaded text from: {args.file}")
            print(f"Text length: {len(text)} characters")
            source_file = str(file_path.absolute())
        except Exception as e:
            print(f"Error reading file: {e}", file=sys.stderr)
            sys.exit(1)
    else:
        text = args.text
        print(f"Using direct text input ({len(text)} characters)")
        source_file = None

    # Parse tags
    tags = [tag.strip() for tag in args.tags.split(',')] if args.tags else None

    # Initialize service and embed
    try:
        service = EmbeddingService(
            qdrant_host=args.host,
            qdrant_port=args.port
        )

        print("\n" + "=" * 60)
        print("EMBEDDING CONTENT")
        print("=" * 60)

        point_id = service.embed_and_store(
            text=text,
            tags=tags,
            category=args.category,
            source_file=source_file
        )

        print("\n" + "=" * 60)
        print("SUMMARY")
        print("=" * 60)
        print(f"Point ID: {point_id}")
        print(f"Category: {args.category or 'uncategorized'}")
        print(f"Tags: {', '.join(tags) if tags else 'none'}")
        print(f"Source: {source_file or 'direct input'}")

        # Show collection stats
        info = service.get_collection_info()
        if info:
            print(f"\nCollection '{info['name']}' now contains {info['points_count']} points")

        print("\nEmbedding completed successfully!")

    except Exception as e:
        print(f"\nFailed to embed content: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
