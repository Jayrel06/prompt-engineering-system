#!/usr/bin/env python3
"""
Cache Integration Examples

Demonstrates how to integrate cache_manager with existing scripts:
- embed_context.py: Cache embeddings
- search_knowledge.py: Cache search results
- prompt_optimizer.py: Cache prompt analysis
- Any LLM API calls: Cache responses
"""

import hashlib
import time
from pathlib import Path
from typing import List, Dict, Optional, Any

# Import cache manager
from cache_manager import CacheManager, cached, make_cache_key


# ============================================================================
# Example 1: Caching Embeddings (for embed_context.py)
# ============================================================================

class CachedEmbeddingModel:
    """Wrapper for embedding model with caching."""

    def __init__(self, model_name: str = "all-MiniLM-L6-v2", cache_ttl: int = 604800):
        """
        Initialize cached embedding model.

        Args:
            model_name: Name of the embedding model
            cache_ttl: Cache TTL in seconds (default: 7 days)
        """
        self.model_name = model_name
        self.cache = CacheManager(backend='file')
        self.cache_ttl = cache_ttl

        # Initialize actual model (lazy loading could be added)
        try:
            from sentence_transformers import SentenceTransformer
            self.model = SentenceTransformer(model_name)
        except ImportError:
            print("sentence-transformers not installed, using mock embeddings")
            self.model = None

    def _compute_text_hash(self, text: str) -> str:
        """Compute hash of text for cache key."""
        return hashlib.sha256(text.encode()).hexdigest()

    def encode(self, texts: List[str]) -> List[List[float]]:
        """
        Encode texts with caching.

        Args:
            texts: List of texts to embed

        Returns:
            List of embeddings
        """
        embeddings = []

        for text in texts:
            # Create cache key
            text_hash = self._compute_text_hash(text)
            cache_key = f"embedding:{self.model_name}:{text_hash}"

            # Check cache
            cached_embedding = self.cache.get(cache_key)

            if cached_embedding is not None:
                embeddings.append(cached_embedding)
            else:
                # Compute embedding
                if self.model:
                    embedding = self.model.encode(text).tolist()
                else:
                    # Mock embedding for testing
                    embedding = [0.1] * 384

                # Cache it
                self.cache.set(cache_key, embedding, ttl=self.cache_ttl)
                embeddings.append(embedding)

        return embeddings

    def get_cache_stats(self):
        """Get cache statistics."""
        return self.cache.get_stats()


# ============================================================================
# Example 2: Caching Search Results (for search_knowledge.py)
# ============================================================================

@cached(ttl=1800)  # 30 minutes
def cached_vector_search(query: str, collection: str = "prompt_context", limit: int = 5):
    """
    Cached vector search.

    Args:
        query: Search query
        collection: Collection name
        limit: Number of results

    Returns:
        Search results
    """
    # This would call the actual vector search
    # For demo purposes, we'll return mock results
    return {
        'query': query,
        'collection': collection,
        'results': [
            {'score': 0.95, 'text': f'Result 1 for: {query}'},
            {'score': 0.87, 'text': f'Result 2 for: {query}'},
        ],
        'count': 2
    }


class CachedKnowledgeSearch:
    """Knowledge search with intelligent caching."""

    def __init__(self, cache_ttl: int = 1800):
        """
        Initialize cached search.

        Args:
            cache_ttl: Cache TTL in seconds (default: 30 minutes)
        """
        self.cache = CacheManager(backend='file')
        self.cache_ttl = cache_ttl

    def search(self, query: str, collection: str = "prompt_context",
               filters: Optional[Dict] = None, limit: int = 5) -> List[Dict]:
        """
        Search with caching.

        Args:
            query: Search query
            collection: Collection name
            filters: Optional filters
            limit: Number of results

        Returns:
            Search results
        """
        # Create cache key including all parameters
        cache_key = f"search:{make_cache_key(query, collection, filters, limit)}"

        # Check cache
        cached_results = self.cache.get(cache_key)
        if cached_results is not None:
            return cached_results['results']

        # Perform search (mock for demo)
        results = [
            {'score': 0.95, 'text': f'Result for: {query}', 'metadata': {}},
            {'score': 0.87, 'text': f'Another result', 'metadata': {}},
        ]

        # Cache results
        self.cache.set(cache_key, {
            'query': query,
            'collection': collection,
            'filters': filters,
            'results': results,
            'timestamp': time.time()
        }, ttl=self.cache_ttl)

        return results

    def invalidate_collection(self, collection: str):
        """Invalidate all cached searches for a collection."""
        self.cache.invalidate(pattern=f"search:{collection}")


# ============================================================================
# Example 3: Caching LLM Responses
# ============================================================================

class CachedLLMClient:
    """LLM client with response caching."""

    def __init__(self, cache_ttl: int = 3600):
        """
        Initialize cached LLM client.

        Args:
            cache_ttl: Cache TTL in seconds (default: 1 hour)
        """
        self.cache = CacheManager(backend='file')
        self.cache_ttl = cache_ttl

    def _create_prompt_hash(self, prompt: str, model: str, temperature: float,
                           max_tokens: int) -> str:
        """Create deterministic hash for prompt parameters."""
        key_str = f"{prompt}|{model}|{temperature}|{max_tokens}"
        return hashlib.sha256(key_str.encode()).hexdigest()

    def complete(self, prompt: str, model: str = "gpt-4",
                temperature: float = 0.7, max_tokens: int = 1000) -> str:
        """
        Get completion with caching.

        Args:
            prompt: The prompt
            model: Model name
            temperature: Temperature parameter
            max_tokens: Max tokens

        Returns:
            Completion text
        """
        # Create cache key
        prompt_hash = self._create_prompt_hash(prompt, model, temperature, max_tokens)
        cache_key = f"llm:response:{prompt_hash}"

        # Check cache
        cached_response = self.cache.get(cache_key)
        if cached_response is not None:
            return cached_response['text']

        # Call LLM (mock for demo)
        response_text = f"Response for: {prompt[:50]}..."

        # Cache response
        self.cache.set(cache_key, {
            'prompt': prompt[:200],  # Store preview only
            'model': model,
            'temperature': temperature,
            'max_tokens': max_tokens,
            'text': response_text,
            'timestamp': time.time()
        }, ttl=self.cache_ttl)

        return response_text


# ============================================================================
# Example 4: Caching Prompt Analysis (for prompt_optimizer.py)
# ============================================================================

@cached(ttl=7200)  # 2 hours
def analyze_prompt_with_cache(prompt: str) -> Dict[str, Any]:
    """
    Analyze prompt with caching.

    Args:
        prompt: Prompt to analyze

    Returns:
        Analysis results
    """
    # This would perform actual prompt analysis
    # Mock for demo
    return {
        'complexity': 'medium',
        'token_count': len(prompt.split()),
        'suggestions': [
            'Consider adding specific examples',
            'Be more explicit about output format'
        ],
        'score': 7.5
    }


class CachedPromptOptimizer:
    """Prompt optimizer with result caching."""

    def __init__(self, cache_ttl: int = 7200):
        """
        Initialize cached optimizer.

        Args:
            cache_ttl: Cache TTL in seconds (default: 2 hours)
        """
        self.cache = CacheManager(backend='file')
        self.cache_ttl = cache_ttl

    def optimize(self, prompt: str, context: Optional[Dict] = None) -> Dict:
        """
        Optimize prompt with caching.

        Args:
            prompt: Original prompt
            context: Optional context

        Returns:
            Optimization results
        """
        # Create cache key
        prompt_hash = hashlib.sha256(prompt.encode()).hexdigest()
        context_hash = hashlib.sha256(str(context).encode()).hexdigest() if context else "none"
        cache_key = f"optimize:{prompt_hash}:{context_hash}"

        # Check cache
        cached_result = self.cache.get(cache_key)
        if cached_result is not None:
            return cached_result

        # Perform optimization (mock)
        result = {
            'original': prompt,
            'optimized': f"Optimized: {prompt}",
            'improvements': ['Added clarity', 'Structured better'],
            'score_improvement': 2.5
        }

        # Cache result
        self.cache.set(cache_key, result, ttl=self.cache_ttl)

        return result


# ============================================================================
# Example 5: File Hash-Based Caching
# ============================================================================

def compute_file_hash(file_path: Path) -> str:
    """Compute hash of file for cache key."""
    with open(file_path, 'rb') as f:
        return hashlib.sha256(f.read()).hexdigest()


def process_file_with_cache(file_path: Path, processor_func: callable) -> Any:
    """
    Process file with caching based on file hash.

    Args:
        file_path: Path to file
        processor_func: Function to process file

    Returns:
        Processing result
    """
    cache = CacheManager(backend='file')

    # Compute file hash
    try:
        file_hash = compute_file_hash(file_path)
    except Exception as e:
        print(f"Could not hash file: {e}")
        return processor_func(file_path)

    # Create cache key
    func_name = processor_func.__name__
    cache_key = f"file:{func_name}:{file_hash}"

    # Check cache
    cached_result = cache.get(cache_key)
    if cached_result is not None:
        return cached_result

    # Process file
    result = processor_func(file_path)

    # Cache result (7 days TTL)
    cache.set(cache_key, result, ttl=604800)

    return result


# ============================================================================
# Example 6: Batch Operations with Caching
# ============================================================================

def batch_embed_with_cache(texts: List[str], batch_size: int = 32) -> List[List[float]]:
    """
    Batch embed texts with per-text caching.

    Args:
        texts: List of texts to embed
        batch_size: Batch size for processing

    Returns:
        List of embeddings
    """
    cache = CacheManager(backend='file')
    embeddings = []
    uncached_texts = []
    uncached_indices = []

    # Check cache for each text
    for i, text in enumerate(texts):
        text_hash = hashlib.sha256(text.encode()).hexdigest()
        cache_key = f"embedding:batch:{text_hash}"

        cached = cache.get(cache_key)
        if cached:
            embeddings.append(cached)
        else:
            embeddings.append(None)
            uncached_texts.append(text)
            uncached_indices.append(i)

    # Process uncached texts in batches
    if uncached_texts:
        # Mock embedding computation
        for i, text in enumerate(uncached_texts):
            embedding = [0.1] * 384  # Mock
            text_hash = hashlib.sha256(text.encode()).hexdigest()
            cache_key = f"embedding:batch:{text_hash}"

            # Cache it
            cache.set(cache_key, embedding, ttl=604800)

            # Add to results
            embeddings[uncached_indices[i]] = embedding

    return embeddings


# ============================================================================
# Usage Examples
# ============================================================================

def demo_embedding_cache():
    """Demo embedding caching."""
    print("\n=== Embedding Cache Demo ===")

    model = CachedEmbeddingModel()

    # First call - computes and caches
    texts = ["Hello world", "Cache this text"]
    embeddings1 = model.encode(texts)
    print(f"First call: {len(embeddings1)} embeddings computed")

    # Second call - uses cache
    embeddings2 = model.encode(texts)
    print(f"Second call: {len(embeddings2)} embeddings from cache")

    # Check stats
    stats = model.get_cache_stats()
    print(f"Cache hit rate: {stats.hit_rate}%")


def demo_search_cache():
    """Demo search result caching."""
    print("\n=== Search Cache Demo ===")

    search = CachedKnowledgeSearch()

    # First search
    start = time.time()
    results1 = search.search("prompt engineering best practices")
    time1 = time.time() - start
    print(f"First search: {len(results1)} results in {time1*1000:.2f}ms")

    # Second search (cached)
    start = time.time()
    results2 = search.search("prompt engineering best practices")
    time2 = time.time() - start
    print(f"Cached search: {len(results2)} results in {time2*1000:.2f}ms")
    print(f"Speedup: {time1/time2:.1f}x")


def demo_llm_cache():
    """Demo LLM response caching."""
    print("\n=== LLM Response Cache Demo ===")

    client = CachedLLMClient()

    prompt = "Explain quantum computing in simple terms"

    # First call
    response1 = client.complete(prompt)
    print(f"First call: {response1[:50]}...")

    # Second call (cached)
    response2 = client.complete(prompt)
    print(f"Cached call: {response2[:50]}...")
    print(f"Responses match: {response1 == response2}")


def demo_decorator():
    """Demo @cached decorator."""
    print("\n=== @cached Decorator Demo ===")

    call_count = [0]

    @cached(ttl=3600)
    def expensive_computation(x: int, y: int) -> int:
        call_count[0] += 1
        time.sleep(0.1)  # Simulate expensive operation
        return x * y + x + y

    # First call
    start = time.time()
    result1 = expensive_computation(5, 10)
    time1 = time.time() - start
    print(f"First call: result={result1}, time={time1*1000:.2f}ms, calls={call_count[0]}")

    # Second call (cached)
    start = time.time()
    result2 = expensive_computation(5, 10)
    time2 = time.time() - start
    print(f"Cached call: result={result2}, time={time2*1000:.2f}ms, calls={call_count[0]}")
    print(f"Speedup: {time1/time2:.1f}x")


def main():
    """Run all demos."""
    print("=" * 80)
    print("CACHE INTEGRATION EXAMPLES")
    print("=" * 80)

    demo_embedding_cache()
    demo_search_cache()
    demo_llm_cache()
    demo_decorator()

    print("\n" + "=" * 80)
    print("All demos complete!")
    print("=" * 80)


if __name__ == "__main__":
    main()
