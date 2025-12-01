# Cache Manager

Production-ready caching layer for the Prompt Engineering System with dual backend support (file-based and Redis).

## Features

- **Dual Backend Support**: File-based JSON cache (default) or Redis with automatic fallback
- **TTL-based Expiration**: Automatic expiration of cached entries
- **Thread-Safe Operations**: Safe for concurrent access
- **Cache Statistics**: Track hits, misses, hit rate, and memory usage
- **Easy Decorator**: `@cached()` decorator for function result caching
- **Hash-based Keys**: Automatic key generation from function arguments
- **Cache Warming**: Pre-populate cache with common queries
- **CLI Management**: Command-line tools for stats, cleanup, and maintenance

## Installation

### Basic Setup (File-based cache)

No additional dependencies required. The cache manager works out of the box with file-based caching.

### Redis Support (Optional)

For Redis backend support:

```bash
pip install redis
```

Ensure Redis is running:

```bash
# Docker
docker run -d -p 6379:6379 redis:alpine

# Or using docker-compose (add to your docker-compose.yml)
redis:
  image: redis:alpine
  ports:
    - "6379:6379"
```

## Quick Start

### As a Library

```python
from cache_manager import CacheManager, cached

# Initialize cache
cache = CacheManager(backend='file')  # or 'redis'

# Basic operations
cache.set('key', 'value', ttl=3600)  # Cache for 1 hour
result = cache.get('key')
cache.delete('key')

# Check existence
if cache.exists('key'):
    print("Key exists!")

# Get TTL
remaining = cache.get_ttl('key')
print(f"Expires in {remaining} seconds")
```

### Using the Decorator

```python
from cache_manager import cached

@cached(ttl=3600)  # Cache for 1 hour
def expensive_function(x, y):
    # This will only run once per unique (x, y) combination
    # within the TTL window
    return complex_calculation(x, y)

result = expensive_function(5, 10)  # Computed and cached
result = expensive_function(5, 10)  # Retrieved from cache
```

### CLI Usage

```bash
# Show cache statistics
python cache_manager.py --stats

# Clear all cache
python cache_manager.py --clear

# Clean up expired entries
python cache_manager.py --cleanup

# Warm cache with common queries
python cache_manager.py --warm

# Get a value
python cache_manager.py --get mykey

# Set a value
python cache_manager.py --set mykey '{"value": "data"}' --ttl 3600

# Delete a key
python cache_manager.py --delete mykey

# Use Redis backend
python cache_manager.py --backend redis --stats
python cache_manager.py --backend redis --redis-url redis://localhost:6379/0
```

## Use Cases

### 1. Caching Embeddings

Avoid recomputing embeddings for unchanged files:

```python
from cache_manager import CacheManager
import hashlib

cache = CacheManager()

def get_file_embedding(file_path):
    # Compute file hash
    with open(file_path, 'rb') as f:
        file_hash = hashlib.sha256(f.read()).hexdigest()

    # Check cache
    cache_key = f"embedding:{file_hash}"
    cached = cache.get(cache_key)

    if cached:
        return cached['embedding']

    # Compute embedding
    embedding = compute_embedding(file_path)

    # Cache for 24 hours
    cache.set(cache_key, {
        'file_path': file_path,
        'hash': file_hash,
        'embedding': embedding,
        'model': 'all-MiniLM-L6-v2'
    }, ttl=86400)

    return embedding
```

### 2. Caching Search Results

Cache search results with TTL:

```python
from cache_manager import cached, make_cache_key

@cached(ttl=1800)  # 30 minutes
def search_knowledge_base(query, filters=None):
    # Expensive search operation
    results = vector_search(query, filters)
    return results

# First call performs search
results = search_knowledge_base("prompt engineering")

# Subsequent calls within 30 minutes use cache
results = search_knowledge_base("prompt engineering")
```

### 3. Caching Prompt Responses

Cache LLM responses for repeated prompts:

```python
from cache_manager import cached, make_cache_key
import hashlib

def cache_key_for_prompt(prompt, model, temperature):
    """Generate deterministic cache key for prompt."""
    key_str = f"{prompt}|{model}|{temperature}"
    return hashlib.sha256(key_str.encode()).hexdigest()

def get_llm_response(prompt, model="gpt-4", temperature=0.7):
    cache = CacheManager()

    # Check cache
    cache_key = f"llm:{cache_key_for_prompt(prompt, model, temperature)}"
    cached = cache.get(cache_key)

    if cached:
        return cached['response']

    # Call LLM
    response = call_llm_api(prompt, model, temperature)

    # Cache for 1 hour
    cache.set(cache_key, {
        'prompt': prompt,
        'model': model,
        'temperature': temperature,
        'response': response
    }, ttl=3600)

    return response
```

### 4. Integration with Existing Scripts

Update `search_knowledge.py` to use caching:

```python
from cache_manager import CacheManager, cached

cache = CacheManager()

@cached(ttl=1800, key_prefix="search:")
def search_with_cache(query, collection="prompt_context", limit=5):
    """Search with automatic caching."""
    # Original search logic
    return perform_vector_search(query, collection, limit)
```

Update `embed_context.py` to cache embeddings:

```python
from cache_manager import CacheManager

cache = CacheManager()

def get_cached_embedding(text, model_name="all-MiniLM-L6-v2"):
    """Get embedding with caching."""
    # Create cache key from content hash
    text_hash = hashlib.sha256(text.encode()).hexdigest()
    cache_key = f"embedding:{model_name}:{text_hash}"

    # Check cache
    cached = cache.get(cache_key)
    if cached:
        return cached

    # Compute embedding
    model = SentenceTransformer(model_name)
    embedding = model.encode(text).tolist()

    # Cache for 7 days
    cache.set(cache_key, embedding, ttl=604800)

    return embedding
```

## API Reference

### CacheManager

Main cache manager class.

```python
cache = CacheManager(backend='file', redis_url=None)
```

#### Methods

**`get(key: str, default=None) -> Any`**

Get value from cache.

```python
value = cache.get('mykey', default='not found')
```

**`set(key: str, value: Any, ttl: int = None)`**

Set value in cache with optional TTL.

```python
cache.set('mykey', {'data': 'value'}, ttl=3600)
```

**`delete(key: str) -> bool`**

Delete entry from cache.

```python
deleted = cache.delete('mykey')
```

**`exists(key: str) -> bool`**

Check if key exists.

```python
if cache.exists('mykey'):
    print("Key exists!")
```

**`get_ttl(key: str) -> Optional[int]`**

Get remaining TTL in seconds.

```python
ttl = cache.get_ttl('mykey')
print(f"Expires in {ttl} seconds")
```

**`invalidate(pattern: Optional[str] = None) -> int`**

Invalidate cache entries matching pattern.

```python
# Clear all
count = cache.invalidate()

# Clear matching pattern
count = cache.invalidate(pattern='user:')
```

**`cleanup_expired() -> int`**

Remove expired entries (file backend only).

```python
removed = cache.cleanup_expired()
```

**`get_stats() -> CacheStats`**

Get cache statistics.

```python
stats = cache.get_stats()
print(f"Hit rate: {stats.hit_rate}%")
print(f"Total entries: {stats.total_entries}")
print(f"Size: {stats.total_size_mb} MB")
```

### Decorator

**`@cached(ttl=3600, key_prefix='', backend='file')`**

Decorator for caching function results.

```python
@cached(ttl=3600)
def my_function(x, y):
    return x + y
```

### Helper Functions

**`make_cache_key(*args, **kwargs) -> str`**

Generate cache key from arguments.

```python
key = make_cache_key(1, 2, x=3, y=4)
```

**`get_cache(backend='file', redis_url=None) -> CacheManager`**

Get or create global cache instance.

```python
cache = get_cache(backend='redis')
```

**`warm_cache(cache: CacheManager)`**

Warm cache with common queries.

```python
warm_cache(cache)
```

## Data Classes

### CacheEntry

Represents a single cache entry.

```python
@dataclass
class CacheEntry:
    key: str
    value: Any
    created_at: float
    expires_at: Optional[float]
    hit_count: int = 0
    last_accessed: Optional[float] = None
    size_bytes: int = 0
```

### CacheStats

Cache statistics.

```python
@dataclass
class CacheStats:
    hits: int
    misses: int
    hit_rate: float
    total_entries: int
    expired_entries: int
    size_bytes: int
    total_size_mb: float
    avg_entry_size: float
    most_accessed_keys: List[tuple]
```

## Configuration

### Environment Variables

```bash
# Redis URL (optional)
export REDIS_URL="redis://localhost:6379/0"

# Or with authentication
export REDIS_URL="redis://username:password@localhost:6379/0"
```

### Cache Storage

File-based cache is stored at:
```
<project_root>/data/cache/cache.json
```

## Performance Considerations

### File Backend

- **Pros**: No external dependencies, persistent across restarts
- **Cons**: Slower for high-frequency operations, locks entire cache on write
- **Best for**: Development, low-frequency caching, simple deployments

### Redis Backend

- **Pros**: Fast, scalable, supports distributed systems
- **Cons**: Requires Redis server, additional dependency
- **Best for**: Production, high-frequency operations, distributed systems

## Thread Safety

All cache operations are thread-safe using `RLock` (reentrant lock):

```python
cache = CacheManager()

# Safe for concurrent access
threads = [
    threading.Thread(target=cache.set, args=(f'key_{i}', f'value_{i}'))
    for i in range(10)
]

for t in threads:
    t.start()

for t in threads:
    t.join()
```

## Best Practices

### 1. Choose Appropriate TTL

```python
# Embeddings - long TTL (file content rarely changes)
cache.set('embedding:abc123', embedding, ttl=86400)  # 24 hours

# Search results - medium TTL (data updates periodically)
cache.set('search:query', results, ttl=1800)  # 30 minutes

# API responses - short TTL (data changes frequently)
cache.set('api:data', response, ttl=300)  # 5 minutes
```

### 2. Use Namespaced Keys

```python
# Good - namespaced
cache.set('user:123:profile', data)
cache.set('search:results:query1', data)
cache.set('embedding:file:abc123', data)

# Bad - ambiguous
cache.set('123', data)
cache.set('query1', data)
```

### 3. Handle Cache Misses Gracefully

```python
def get_data(key):
    cached = cache.get(key)
    if cached:
        return cached

    # Compute/fetch data
    data = expensive_operation()

    # Cache for next time
    cache.set(key, data, ttl=3600)

    return data
```

### 4. Regular Cleanup

```bash
# Add to cron or scheduled task
0 2 * * * cd /path/to/project && python scripts/cache_manager.py --cleanup
```

### 5. Monitor Hit Rates

```python
# Check periodically
stats = cache.get_stats()
if stats.hit_rate < 50:
    print("Low hit rate - consider adjusting TTL or warming cache")
```

## Testing

Run the comprehensive test suite:

```bash
python scripts/test_cache_manager.py
```

Tests cover:
- Basic operations (get/set/delete)
- TTL and expiration
- Complex data types
- Decorator functionality
- Thread safety
- Cache statistics
- Use case scenarios

## Troubleshooting

### Cache not persisting

**File backend**: Check write permissions for `data/cache/` directory.

```bash
mkdir -p data/cache
chmod 755 data/cache
```

### Redis connection failed

Check Redis is running:

```bash
redis-cli ping
# Should return: PONG
```

Verify connection URL:

```bash
python cache_manager.py --backend redis --redis-url redis://localhost:6379/0 --stats
```

### High memory usage

Clear old entries:

```bash
python cache_manager.py --cleanup
python cache_manager.py --stats
```

Reduce TTL for less critical data.

### Poor hit rate

1. Check if keys are consistent
2. Increase TTL if appropriate
3. Warm cache with common queries
4. Review cache invalidation patterns

## Migration Guide

### From No Caching

```python
# Before
def search(query):
    return expensive_search(query)

# After
from cache_manager import cached

@cached(ttl=1800)
def search(query):
    return expensive_search(query)
```

### From Custom Cache

```python
# Before
_cache = {}

def get_or_compute(key):
    if key in _cache:
        return _cache[key]
    value = compute()
    _cache[key] = value
    return value

# After
from cache_manager import CacheManager

cache = CacheManager()

def get_or_compute(key):
    cached = cache.get(key)
    if cached:
        return cached
    value = compute()
    cache.set(key, value, ttl=3600)
    return value
```

## License

Part of the Prompt Engineering System.

## Support

For issues or questions, please check the test suite and examples or open an issue in the project repository.
