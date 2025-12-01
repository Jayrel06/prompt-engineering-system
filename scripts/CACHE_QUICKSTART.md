# Cache Manager Quick Start

Get started with the cache manager in 5 minutes.

## Installation

No installation needed! Cache manager works out of the box with file-based caching.

For Redis support (optional):
```bash
pip install redis
```

## Basic Usage

### 1. Simple Get/Set

```python
from cache_manager import CacheManager

cache = CacheManager()

# Set value with 1 hour TTL
cache.set('my_key', {'data': 'value'}, ttl=3600)

# Get value
value = cache.get('my_key')
print(value)  # {'data': 'value'}
```

### 2. Using the Decorator

```python
from cache_manager import cached

@cached(ttl=3600)  # Cache for 1 hour
def expensive_function(x, y):
    # This runs only once per unique (x, y)
    return x + y

result = expensive_function(5, 10)  # Computed
result = expensive_function(5, 10)  # From cache
```

### 3. CLI Commands

```bash
# View statistics
python cache_manager.py --stats

# Set a value
python cache_manager.py --set mykey '{"value": "data"}' --ttl 3600

# Get a value
python cache_manager.py --get mykey

# Clear cache
python cache_manager.py --clear

# Clean expired entries
python cache_manager.py --cleanup
```

## Common Use Cases

### Cache Embeddings

```python
from cache_manager import CacheManager
import hashlib

cache = CacheManager()

def get_embedding(text):
    # Create hash-based key
    text_hash = hashlib.sha256(text.encode()).hexdigest()
    cache_key = f"embedding:{text_hash}"

    # Check cache
    cached = cache.get(cache_key)
    if cached:
        return cached

    # Compute embedding
    embedding = compute_embedding(text)

    # Cache for 24 hours
    cache.set(cache_key, embedding, ttl=86400)

    return embedding
```

### Cache Search Results

```python
from cache_manager import cached

@cached(ttl=1800)  # 30 minutes
def search_knowledge(query):
    # Expensive search operation
    return perform_vector_search(query)

# First call: performs search
results = search_knowledge("prompt engineering")

# Second call: uses cache
results = search_knowledge("prompt engineering")
```

### Cache API Responses

```python
from cache_manager import CacheManager
import hashlib

cache = CacheManager()

def call_llm(prompt, model="gpt-4"):
    # Create deterministic key
    key_str = f"{prompt}|{model}"
    cache_key = f"llm:{hashlib.sha256(key_str.encode()).hexdigest()}"

    # Check cache
    cached = cache.get(cache_key)
    if cached:
        return cached['response']

    # Call API
    response = api_call(prompt, model)

    # Cache for 1 hour
    cache.set(cache_key, {'response': response}, ttl=3600)

    return response
```

## Key Features

### TTL (Time To Live)

Set expiration time for cached entries:

```python
cache.set('key', 'value', ttl=3600)  # Expires in 1 hour
cache.set('key', 'value', ttl=86400) # Expires in 24 hours
cache.set('key', 'value')            # Never expires
```

### Cache Statistics

Track cache performance:

```python
stats = cache.get_stats()
print(f"Hit rate: {stats.hit_rate}%")
print(f"Total entries: {stats.total_entries}")
print(f"Size: {stats.total_size_mb} MB")
```

### Pattern Invalidation

Clear related entries:

```python
# Cache multiple user entries
cache.set('user:1:profile', data1, ttl=3600)
cache.set('user:2:profile', data2, ttl=3600)
cache.set('config:settings', data3, ttl=3600)

# Invalidate all user entries
cache.invalidate(pattern='user:')

# Config entry still exists
```

### Cache Warming

Pre-populate cache:

```python
from cache_manager import warm_cache

cache = CacheManager()
warm_cache(cache)  # Loads common queries
```

## Best Practices

### 1. Use Namespaced Keys

```python
# Good
cache.set('user:123:profile', data)
cache.set('search:results:query1', data)
cache.set('embedding:file:abc123', data)

# Bad
cache.set('123', data)
cache.set('query1', data)
```

### 2. Choose Appropriate TTL

```python
# Long TTL for stable data
cache.set('embedding:hash', embedding, ttl=604800)  # 7 days

# Medium TTL for periodic updates
cache.set('search:query', results, ttl=1800)  # 30 minutes

# Short TTL for volatile data
cache.set('api:data', response, ttl=300)  # 5 minutes
```

### 3. Handle Cache Misses

```python
cached = cache.get('key')
if cached:
    return cached

# Compute if not cached
result = expensive_operation()
cache.set('key', result, ttl=3600)
return result
```

## Backend Options

### File Backend (Default)

```python
cache = CacheManager(backend='file')
```

- No dependencies
- Persistent across restarts
- Best for: Development, single-server deployments

### Redis Backend

```python
cache = CacheManager(backend='redis', redis_url='redis://localhost:6379/0')
```

- Fast and scalable
- Supports distributed systems
- Best for: Production, high-frequency operations

## Maintenance

### View Cache Status

```bash
python cache_manager.py --stats
```

### Clean Expired Entries

```bash
python cache_manager.py --cleanup
```

### Clear All Cache

```bash
python cache_manager.py --clear
```

### Schedule Regular Cleanup

Add to crontab:
```bash
0 2 * * * cd /path/to/project && python scripts/cache_manager.py --cleanup
```

## Examples

Run the comprehensive examples:

```bash
python scripts/cache_integration_examples.py
```

Run the test suite:

```bash
python scripts/test_cache_manager.py
```

## Next Steps

- Read the full [Cache Manager README](CACHE_MANAGER_README.md)
- Check [integration examples](cache_integration_examples.py)
- Run the test suite to understand all features
- Integrate with your existing scripts

## Common TTL Values

- **5 minutes**: `ttl=300` - Volatile data, frequent updates
- **30 minutes**: `ttl=1800` - Search results, API responses
- **1 hour**: `ttl=3600` - General purpose caching
- **6 hours**: `ttl=21600` - Semi-stable data
- **24 hours**: `ttl=86400` - Daily refresh data
- **7 days**: `ttl=604800` - File embeddings, stable data
- **No expiration**: `ttl=None` - Permanent cache

## Troubleshooting

### Cache not working?

Check the cache file exists:
```bash
ls -la data/cache/cache.json
```

### Poor hit rate?

1. Check if keys are consistent
2. Verify TTL is appropriate
3. Monitor with `--stats`

### Need to reset cache?

```bash
python cache_manager.py --clear
```

## Support

For more help:
- Read the [full documentation](CACHE_MANAGER_README.md)
- Check the [test suite](test_cache_manager.py)
- Review [integration examples](cache_integration_examples.py)
