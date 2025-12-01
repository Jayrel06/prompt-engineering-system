#!/usr/bin/env python3
"""
Context Embedding Script

Embeds all context, framework, and template files into the Qdrant vector database
for semantic search capabilities.
"""

import os
import json
import hashlib
from pathlib import Path
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass
import argparse

try:
    from qdrant_client import QdrantClient
    from qdrant_client.http import models
    HAS_QDRANT = True
except ImportError:
    HAS_QDRANT = False

try:
    from sentence_transformers import SentenceTransformer
    HAS_SENTENCE_TRANSFORMERS = True
except ImportError:
    HAS_SENTENCE_TRANSFORMERS = False

try:
    import openai
    HAS_OPENAI = True
except ImportError:
    HAS_OPENAI = False


@dataclass
class Document:
    """A document to be embedded."""
    id: str
    content: str
    metadata: Dict
    path: str


# Directories to embed
EMBED_DIRS = [
    "context",
    "frameworks",
    "templates",
    "chains",
    "docs",
]

# File extensions to process
VALID_EXTENSIONS = {".md", ".txt", ".yaml", ".yml", ".json"}

# Files to skip
SKIP_FILES = {".gitkeep", ".DS_Store", "Thumbs.db"}


def get_qdrant_client(url: Optional[str] = None) -> "QdrantClient":
    """Get Qdrant client."""
    if not HAS_QDRANT:
        raise ImportError("qdrant-client not installed. Run: pip install qdrant-client")

    url = url or os.environ.get("QDRANT_URL", "http://localhost:6333")
    return QdrantClient(url=url)


def get_embedding_model(model_name: str = "all-MiniLM-L6-v2") -> "SentenceTransformer":
    """Get sentence transformer model."""
    if not HAS_SENTENCE_TRANSFORMERS:
        raise ImportError("sentence-transformers not installed. Run: pip install sentence-transformers")

    return SentenceTransformer(model_name)


def get_openai_embeddings(texts: List[str], model: str = "text-embedding-3-small") -> List[List[float]]:
    """Get embeddings using OpenAI API."""
    if not HAS_OPENAI:
        raise ImportError("openai not installed. Run: pip install openai")

    client = openai.OpenAI()
    response = client.embeddings.create(input=texts, model=model)
    return [item.embedding for item in response.data]


def compute_file_hash(content: str) -> str:
    """Compute hash of file content for change detection."""
    return hashlib.md5(content.encode()).hexdigest()


def load_documents(base_dir: Path) -> List[Document]:
    """Load all documents from the specified directories."""
    documents = []

    for dir_name in EMBED_DIRS:
        dir_path = base_dir / dir_name
        if not dir_path.exists():
            continue

        for file_path in dir_path.rglob("*"):
            if not file_path.is_file():
                continue

            if file_path.name in SKIP_FILES:
                continue

            if file_path.suffix.lower() not in VALID_EXTENSIONS:
                continue

            try:
                content = file_path.read_text(encoding="utf-8")
            except Exception as e:
                print(f"Warning: Could not read {file_path}: {e}")
                continue

            if not content.strip():
                continue

            # Create relative path for ID
            rel_path = file_path.relative_to(base_dir)
            doc_id = str(rel_path).replace("\\", "/").replace("/", "_").replace(".", "_")

            # Extract metadata from content
            metadata = extract_metadata(content, file_path, dir_name)

            documents.append(Document(
                id=doc_id,
                content=content,
                metadata=metadata,
                path=str(rel_path)
            ))

    return documents


def extract_metadata(content: str, file_path: Path, category: str) -> Dict:
    """Extract metadata from document content."""
    metadata = {
        "category": category,
        "filename": file_path.name,
        "path": str(file_path),
        "extension": file_path.suffix,
        "content_hash": compute_file_hash(content),
        "char_count": len(content),
        "line_count": content.count("\n") + 1,
    }

    # Extract title from first heading
    lines = content.split("\n")
    for line in lines[:10]:
        if line.startswith("# "):
            metadata["title"] = line[2:].strip()
            break

    # Try to detect subcategory from path
    parts = file_path.parts
    if len(parts) > 2:
        metadata["subcategory"] = parts[-2]

    return metadata


def chunk_document(doc: Document, chunk_size: int = 1000, overlap: int = 200) -> List[Document]:
    """Split large documents into chunks for better retrieval."""
    content = doc.content

    if len(content) <= chunk_size:
        return [doc]

    chunks = []
    start = 0
    chunk_num = 0

    while start < len(content):
        end = start + chunk_size

        # Try to break at paragraph or sentence boundary
        if end < len(content):
            # Look for paragraph break
            para_break = content.rfind("\n\n", start, end)
            if para_break > start + chunk_size // 2:
                end = para_break
            else:
                # Look for sentence break
                sent_break = content.rfind(". ", start, end)
                if sent_break > start + chunk_size // 2:
                    end = sent_break + 1

        chunk_content = content[start:end].strip()

        if chunk_content:
            chunk_metadata = doc.metadata.copy()
            chunk_metadata["chunk_num"] = chunk_num
            chunk_metadata["is_chunk"] = True

            chunks.append(Document(
                id=f"{doc.id}_chunk{chunk_num}",
                content=chunk_content,
                metadata=chunk_metadata,
                path=doc.path
            ))
            chunk_num += 1

        start = end - overlap

    return chunks


def create_collection(
    client: "QdrantClient",
    collection_name: str,
    vector_size: int,
    recreate: bool = False
):
    """Create or recreate the vector collection."""
    collections = client.get_collections().collections
    exists = any(c.name == collection_name for c in collections)

    if exists:
        if recreate:
            print(f"Deleting existing collection: {collection_name}")
            client.delete_collection(collection_name)
        else:
            print(f"Collection {collection_name} already exists. Use --recreate to rebuild.")
            return False

    print(f"Creating collection: {collection_name}")
    client.create_collection(
        collection_name=collection_name,
        vectors_config=models.VectorParams(
            size=vector_size,
            distance=models.Distance.COSINE
        )
    )

    return True


def embed_documents(
    documents: List[Document],
    client: "QdrantClient",
    collection_name: str,
    embedding_provider: str = "local",
    batch_size: int = 32
):
    """Embed documents and store in Qdrant."""
    if embedding_provider == "local":
        model = get_embedding_model()
        vector_size = model.get_sentence_embedding_dimension()
    else:
        vector_size = 1536  # OpenAI text-embedding-3-small

    # Chunk documents
    all_chunks = []
    for doc in documents:
        chunks = chunk_document(doc)
        all_chunks.extend(chunks)

    print(f"Processing {len(documents)} documents ({len(all_chunks)} chunks)")

    # Create collection
    create_collection(client, collection_name, vector_size, recreate=True)

    # Process in batches
    for i in range(0, len(all_chunks), batch_size):
        batch = all_chunks[i:i + batch_size]
        texts = [chunk.content for chunk in batch]

        # Get embeddings
        if embedding_provider == "local":
            embeddings = model.encode(texts).tolist()
        else:
            embeddings = get_openai_embeddings(texts)

        # Prepare points
        points = []
        for j, (chunk, embedding) in enumerate(zip(batch, embeddings)):
            points.append(models.PointStruct(
                id=i + j,
                vector=embedding,
                payload={
                    "doc_id": chunk.id,
                    "content": chunk.content[:1000],  # Store preview
                    "path": chunk.path,
                    **chunk.metadata
                }
            ))

        # Upsert to Qdrant
        client.upsert(collection_name=collection_name, points=points)
        print(f"  Embedded batch {i // batch_size + 1}/{(len(all_chunks) + batch_size - 1) // batch_size}")

    print(f"Successfully embedded {len(all_chunks)} chunks into {collection_name}")


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description="Embed context files into vector database")
    parser.add_argument("--base-dir", type=Path, default=Path(__file__).parent.parent,
                        help="Base directory of the prompt system")
    parser.add_argument("--collection", default=os.environ.get("QDRANT_COLLECTION", "prompt_context"),
                        help="Qdrant collection name")
    parser.add_argument("--qdrant-url", default=os.environ.get("QDRANT_URL", "http://localhost:6333"),
                        help="Qdrant server URL")
    parser.add_argument("--embedding", choices=["local", "openai"], default="local",
                        help="Embedding provider (local uses sentence-transformers)")
    parser.add_argument("--recreate", action="store_true",
                        help="Recreate collection from scratch")
    parser.add_argument("--dry-run", action="store_true",
                        help="Only show what would be embedded")

    args = parser.parse_args()

    # Load documents
    print(f"Loading documents from {args.base_dir}")
    documents = load_documents(args.base_dir)
    print(f"Found {len(documents)} documents")

    if args.dry_run:
        print("\nDocuments to embed:")
        for doc in documents:
            print(f"  - {doc.path} ({doc.metadata.get('title', 'No title')})")
        return

    # Connect to Qdrant
    try:
        client = get_qdrant_client(args.qdrant_url)
        client.get_collections()  # Test connection
    except Exception as e:
        print(f"Error connecting to Qdrant at {args.qdrant_url}: {e}")
        print("Make sure Qdrant is running: docker-compose up -d qdrant")
        return

    # Embed documents
    embed_documents(
        documents=documents,
        client=client,
        collection_name=args.collection,
        embedding_provider=args.embedding
    )

    print(f"\nDone! Search your context with:")
    print(f"  python scripts/search_knowledge.py 'your query'")


if __name__ == "__main__":
    main()
