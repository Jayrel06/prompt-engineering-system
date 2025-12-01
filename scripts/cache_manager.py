#!/usr/bin/env python3
"""
Cache Manager - Production-ready caching layer with file and Redis support.

Provides intelligent caching for:
- Embeddings (avoid recomputing for unchanged files)
- Search results (with TTL)
- Prompt responses (hash-based)
- General function results

Features:
- Dual backend: JSON file cache (default) or Redis (with fallback)
- Thread-safe operations with proper locking
- TTL-based expiration
- Cache statistics and hit rate tracking
- Decorator for easy function caching
- CLI for management operations
- Cache warming for common queries

Usage:
    # As library
    from cache_manager import CacheManager, cached

    cache = CacheManager(backend='file')  # or 'redis'
    cache.set('key', value, ttl=3600)
    result = cache.get('key')

    # With decorator
    @cached(ttl=3600)
    def expensive_function(arg1, arg2):
        return compute_result(arg1, arg2)

    # CLI
    cache_manager.py --stats
    cache_manager.py --clear
    cache_manager.py --cleanup
    cache_manager.py --warm
"""

import argparse
import hashlib
import json
import os
import pickle
import sys
import threading
import time
from collections import defaultdict
from dataclasses import dataclass, asdict
from datetime import datetime, timedelta
from functools import wraps
from pathlib import Path
from typing import Any, Dict, List, Optional, Callable, Union
from decimal import Decimal

# Get project paths
SCRIPT_DIR = Path(__file__).parent
PROJECT_ROOT = SCRIPT_DIR.parent
DATA_DIR = PROJECT_ROOT / "data"
CACHE_DIR = DATA_DIR / "cache"
CACHE_FILE = CACHE_DIR / "cache.json"
CACHE_LOCK_FILE = CACHE_DIR / ".cache.lock"

# Redis support (optional)
try:
    import redis
    HAS_REDIS = True
except ImportError:
    HAS_REDIS = False


@dataclass
class CacheEntry:
    """A single cache entry with metadata."""
    key: str
    value: Any
    created_at: float
    expires_at: Optional[float]
    hit_count: int = 0
    last_accessed: Optional[float] = None
    size_bytes: int = 0

    def is_expired(self) -> bool:
        """Check if entry has expired."""
        if self.expires_at is None:
            return False
        return time.time() > self.expires_at

    def is_valid(self) -> bool:
        """Check if entry is valid (exists and not expired)."""
        return not self.is_expired()

    def increment_hit(self) -> None:
        """Increment hit counter and update access time."""
        self.hit_count += 1
        self.last_accessed = time.time()

    def to_dict(self) -> Dict:
        """Convert to dictionary for serialization."""
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict) -> 'CacheEntry':
        """Create from dictionary."""
        return cls(**data)


@dataclass
class CacheStats:
    """Cache statistics."""
    hits: int
    misses: int
    hit_rate: float
    total_entries: int
    expired_entries: int
    size_bytes: int
    total_size_mb: float
    avg_entry_size: float
    most_accessed_keys: List[tuple]

    def to_dict(self) -> Dict:
        """Convert to dictionary."""
        return asdict(self)


class CacheBackend:
    """Abstract cache backend interface."""

    def get(self, key: str) -> Optional[CacheEntry]:
        raise NotImplementedError

    def set(self, key: str, entry: CacheEntry) -> None:
        raise NotImplementedError

    def delete(self, key: str) -> bool:
        raise NotImplementedError

    def clear(self) -> int:
        raise NotImplementedError

    def keys(self) -> List[str]:
        raise NotImplementedError

    def size(self) -> int:
        raise NotImplementedError


class FileBackend(CacheBackend):
    """File-based cache backend using JSON."""

    def __init__(self, cache_file: Path = CACHE_FILE):
        self.cache_file = cache_file
        self.lock = threading.RLock()
        self._cache: Dict[str, CacheEntry] = {}
        self._load_cache()

    def _load_cache(self) -> None:
        """Load cache from disk."""
        self.cache_file.parent.mkdir(parents=True, exist_ok=True)

        if self.cache_file.exists():
            try:
                with open(self.cache_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self._cache = {
                        k: CacheEntry.from_dict(v)
                        for k, v in data.items()
                    }
            except (json.JSONDecodeError, Exception) as e:
                print(f"Warning: Could not load cache file: {e}")
                self._cache = {}

    def _save_cache(self) -> None:
        """Save cache to disk."""
        try:
            with open(self.cache_file, 'w', encoding='utf-8') as f:
                data = {k: v.to_dict() for k, v in self._cache.items()}
                json.dump(data, f, indent=2)
        except Exception as e:
            print(f"Warning: Could not save cache file: {e}")

    def get(self, key: str) -> Optional[CacheEntry]:
        """Get entry from cache."""
        with self.lock:
            entry = self._cache.get(key)
            if entry and entry.is_valid():
                entry.increment_hit()
                return entry
            elif entry and entry.is_expired():
                # Clean up expired entry
                del self._cache[key]
                self._save_cache()
            return None

    def set(self, key: str, entry: CacheEntry) -> None:
        """Set entry in cache."""
        with self.lock:
            self._cache[key] = entry
            self._save_cache()

    def delete(self, key: str) -> bool:
        """Delete entry from cache."""
        with self.lock:
            if key in self._cache:
                del self._cache[key]
                self._save_cache()
                return True
            return False

    def clear(self) -> int:
        """Clear all entries."""
        with self.lock:
            count = len(self._cache)
            self._cache.clear()
            self._save_cache()
            return count

    def keys(self) -> List[str]:
        """Get all keys."""
        with self.lock:
            return list(self._cache.keys())

    def size(self) -> int:
        """Get number of entries."""
        with self.lock:
            return len(self._cache)

    def get_all_entries(self) -> Dict[str, CacheEntry]:
        """Get all entries (for stats)."""
        with self.lock:
            return self._cache.copy()


class RedisBackend(CacheBackend):
    """Redis-based cache backend."""

    def __init__(self, redis_url: Optional[str] = None, prefix: str = "cache:"):
        if not HAS_REDIS:
            raise ImportError("redis not installed. Run: pip install redis")

        redis_url = redis_url or os.environ.get("REDIS_URL", "redis://localhost:6379/0")
        self.redis_client = redis.from_url(redis_url, decode_responses=False)
        self.prefix = prefix
        self.lock = threading.RLock()

        # Test connection
        try:
            self.redis_client.ping()
        except Exception as e:
            raise ConnectionError(f"Could not connect to Redis at {redis_url}: {e}")

    def _make_key(self, key: str) -> str:
        """Add prefix to key."""
        return f"{self.prefix}{key}"

    def get(self, key: str) -> Optional[CacheEntry]:
        """Get entry from cache."""
        redis_key = self._make_key(key)
        data = self.redis_client.get(redis_key)

        if data:
            try:
                entry = pickle.loads(data)
                if entry.is_valid():
                    entry.increment_hit()
                    # Update in Redis
                    self.set(key, entry)
                    return entry
                else:
                    # Expired, delete
                    self.delete(key)
            except Exception as e:
                print(f"Warning: Could not deserialize cache entry: {e}")
                self.delete(key)

        return None

    def set(self, key: str, entry: CacheEntry) -> None:
        """Set entry in cache."""
        redis_key = self._make_key(key)
        data = pickle.dumps(entry)

        if entry.expires_at:
            ttl = int(entry.expires_at - time.time())
            if ttl > 0:
                self.redis_client.setex(redis_key, ttl, data)
        else:
            self.redis_client.set(redis_key, data)

    def delete(self, key: str) -> bool:
        """Delete entry from cache."""
        redis_key = self._make_key(key)
        return bool(self.redis_client.delete(redis_key))

    def clear(self) -> int:
        """Clear all entries with prefix."""
        pattern = f"{self.prefix}*"
        keys = self.redis_client.keys(pattern)
        if keys:
            return self.redis_client.delete(*keys)
        return 0

    def keys(self) -> List[str]:
        """Get all keys."""
        pattern = f"{self.prefix}*"
        redis_keys = self.redis_client.keys(pattern)
        return [k.decode() if isinstance(k, bytes) else k for k in redis_keys]

    def size(self) -> int:
        """Get number of entries."""
        return len(self.keys())

    def get_all_entries(self) -> Dict[str, CacheEntry]:
        """Get all entries (for stats)."""
        entries = {}
        for redis_key in self.keys():
            data = self.redis_client.get(redis_key)
            if data:
                try:
                    key = redis_key.replace(self.prefix, '')
                    entries[key] = pickle.loads(data)
                except:
                    pass
        return entries


class CacheManager:
    """Main cache manager with dual backend support."""

    def __init__(self, backend: str = 'file', redis_url: Optional[str] = None):
        """
        Initialize cache manager.

        Args:
            backend: 'file' or 'redis'
            redis_url: Redis connection URL (optional)
        """
        self.backend_type = backend
        self._stats_hits = 0
        self._stats_misses = 0
        self.lock = threading.RLock()

        # Initialize backend
        if backend == 'redis':
            try:
                self.backend = RedisBackend(redis_url)
                print("Using Redis cache backend")
            except Exception as e:
                print(f"Redis backend failed, falling back to file: {e}")
                self.backend = FileBackend()
                self.backend_type = 'file'
        else:
            self.backend = FileBackend()
            print("Using file cache backend")

    def _compute_key_hash(self, key: str) -> str:
        """Compute hash for key (useful for long keys)."""
        if len(key) > 200:
            return hashlib.sha256(key.encode()).hexdigest()
        return key

    def _serialize_value(self, value: Any) -> tuple[Any, int]:
        """Serialize value and compute size."""
        try:
            # Try JSON first (more portable)
            serialized = json.dumps(value)
            return serialized, len(serialized.encode('utf-8'))
        except (TypeError, ValueError):
            # Fall back to pickle
            serialized = pickle.dumps(value)
            return serialized, len(serialized)

    def _deserialize_value(self, value: Any) -> Any:
        """Deserialize value."""
        if isinstance(value, str):
            try:
                return json.loads(value)
            except:
                pass
        if isinstance(value, bytes):
            return pickle.loads(value)
        return value

    def get(self, key: str, default: Any = None) -> Any:
        """
        Get value from cache.

        Args:
            key: Cache key
            default: Default value if not found

        Returns:
            Cached value or default
        """
        with self.lock:
            key_hash = self._compute_key_hash(key)
            entry = self.backend.get(key_hash)

            if entry:
                self._stats_hits += 1
                return self._deserialize_value(entry.value)
            else:
                self._stats_misses += 1
                return default

    def set(self, key: str, value: Any, ttl: Optional[int] = None) -> None:
        """
        Set value in cache.

        Args:
            key: Cache key
            value: Value to cache
            ttl: Time to live in seconds (None = no expiration)
        """
        with self.lock:
            key_hash = self._compute_key_hash(key)
            serialized, size = self._serialize_value(value)

            now = time.time()
            expires_at = now + ttl if ttl else None

            entry = CacheEntry(
                key=key_hash,
                value=serialized,
                created_at=now,
                expires_at=expires_at,
                hit_count=0,
                last_accessed=None,
                size_bytes=size
            )

            self.backend.set(key_hash, entry)

    def delete(self, key: str) -> bool:
        """
        Delete entry from cache.

        Args:
            key: Cache key

        Returns:
            True if deleted, False if not found
        """
        with self.lock:
            key_hash = self._compute_key_hash(key)
            return self.backend.delete(key_hash)

    def invalidate(self, pattern: Optional[str] = None) -> int:
        """
        Invalidate cache entries matching pattern.

        Args:
            pattern: Key pattern (None = all)

        Returns:
            Number of entries invalidated
        """
        with self.lock:
            if pattern is None:
                return self.backend.clear()

            # Pattern matching
            count = 0
            for key in self.backend.keys():
                if pattern in key:
                    if self.backend.delete(key):
                        count += 1
            return count

    def cleanup_expired(self) -> int:
        """
        Remove expired entries.

        Returns:
            Number of entries removed
        """
        with self.lock:
            if isinstance(self.backend, FileBackend):
                entries = self.backend.get_all_entries()
                count = 0
                for key, entry in entries.items():
                    if entry.is_expired():
                        self.backend.delete(key)
                        count += 1
                return count
            else:
                # Redis handles expiration automatically
                return 0

    def get_stats(self) -> CacheStats:
        """
        Get cache statistics.

        Returns:
            CacheStats object
        """
        with self.lock:
            entries = self.backend.get_all_entries() if isinstance(self.backend, FileBackend) else {}

            total_entries = len(entries)
            expired_entries = sum(1 for e in entries.values() if e.is_expired())
            total_size = sum(e.size_bytes for e in entries.values())

            # Calculate hit rate
            total_requests = self._stats_hits + self._stats_misses
            hit_rate = (self._stats_hits / total_requests * 100) if total_requests > 0 else 0.0

            # Most accessed keys
            sorted_entries = sorted(
                entries.items(),
                key=lambda x: x[1].hit_count,
                reverse=True
            )[:10]
            most_accessed = [(k, e.hit_count) for k, e in sorted_entries]

            avg_size = total_size / total_entries if total_entries > 0 else 0

            return CacheStats(
                hits=self._stats_hits,
                misses=self._stats_misses,
                hit_rate=round(hit_rate, 2),
                total_entries=total_entries,
                expired_entries=expired_entries,
                size_bytes=total_size,
                total_size_mb=round(total_size / (1024 * 1024), 2),
                avg_entry_size=round(avg_size, 2),
                most_accessed_keys=most_accessed
            )

    def exists(self, key: str) -> bool:
        """Check if key exists in cache."""
        key_hash = self._compute_key_hash(key)
        entry = self.backend.get(key_hash)
        return entry is not None

    def get_ttl(self, key: str) -> Optional[int]:
        """Get remaining TTL for key in seconds."""
        key_hash = self._compute_key_hash(key)
        entry = self.backend.get(key_hash)

        if entry and entry.expires_at:
            remaining = entry.expires_at - time.time()
            return max(0, int(remaining))
        return None


# Global cache instance
_global_cache: Optional[CacheManager] = None


def get_cache(backend: str = 'file', redis_url: Optional[str] = None) -> CacheManager:
    """Get or create global cache instance."""
    global _global_cache
    if _global_cache is None:
        _global_cache = CacheManager(backend=backend, redis_url=redis_url)
    return _global_cache


def make_cache_key(*args, **kwargs) -> str:
    """
    Generate cache key from function arguments.

    Args:
        *args: Positional arguments
        **kwargs: Keyword arguments

    Returns:
        Hash-based cache key
    """
    # Create deterministic string representation
    key_parts = []

    for arg in args:
        if isinstance(arg, (str, int, float, bool)):
            key_parts.append(str(arg))
        else:
            # Use hash for complex objects
            key_parts.append(str(hash(str(arg))))

    for k, v in sorted(kwargs.items()):
        if isinstance(v, (str, int, float, bool)):
            key_parts.append(f"{k}={v}")
        else:
            key_parts.append(f"{k}={hash(str(v))}")

    key_str = "|".join(key_parts)
    return hashlib.sha256(key_str.encode()).hexdigest()


def cached(ttl: int = 3600, key_prefix: str = "", backend: str = 'file'):
    """
    Decorator for caching function results.

    Args:
        ttl: Time to live in seconds
        key_prefix: Prefix for cache keys
        backend: Cache backend ('file' or 'redis')

    Example:
        @cached(ttl=3600)
        def expensive_function(x, y):
            return x + y
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            cache = get_cache(backend=backend)

            # Generate cache key
            func_name = f"{func.__module__}.{func.__name__}"
            arg_key = make_cache_key(*args, **kwargs)
            cache_key = f"{key_prefix}{func_name}:{arg_key}"

            # Try to get from cache
            result = cache.get(cache_key)
            if result is not None:
                return result

            # Compute and cache
            result = func(*args, **kwargs)
            cache.set(cache_key, result, ttl=ttl)

            return result

        return wrapper
    return decorator


def warm_cache(cache: CacheManager) -> None:
    """
    Warm cache with common queries.

    Args:
        cache: CacheManager instance
    """
    print("Warming cache with common queries...")

    # Common embedding model configurations
    common_models = [
        "all-MiniLM-L6-v2",
        "text-embedding-3-small",
        "text-embedding-ada-002"
    ]

    for model in common_models:
        key = f"embedding_model:{model}"
        if not cache.exists(key):
            cache.set(key, {"model": model, "dimension": 384}, ttl=86400)

    # Common search configurations
    common_collections = ["prompt_context", "knowledge_base", "embeddings"]
    for collection in common_collections:
        key = f"collection_config:{collection}"
        if not cache.exists(key):
            cache.set(key, {"name": collection, "exists": True}, ttl=3600)

    print(f"Cache warmed with {len(common_models) + len(common_collections)} entries")


def print_stats(stats: CacheStats) -> None:
    """Print formatted cache statistics."""
    print("\n" + "=" * 80)
    print("CACHE STATISTICS")
    print("=" * 80)

    print("\nPerformance:")
    print(f"  Hits:        {stats.hits:,}")
    print(f"  Misses:      {stats.misses:,}")
    print(f"  Hit Rate:    {stats.hit_rate:.2f}%")

    print("\nStorage:")
    print(f"  Total Entries:   {stats.total_entries:,}")
    print(f"  Expired:         {stats.expired_entries:,}")
    print(f"  Total Size:      {stats.total_size_mb:.2f} MB")
    print(f"  Avg Entry Size:  {stats.avg_entry_size:.2f} bytes")

    if stats.most_accessed_keys:
        print("\nMost Accessed Keys:")
        for key, hits in stats.most_accessed_keys[:5]:
            display_key = key[:60] + "..." if len(key) > 60 else key
            print(f"  {display_key:<65} {hits:>8} hits")

    print("\n" + "=" * 80 + "\n")


def main():
    """CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Cache Manager - Intelligent caching layer",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )

    parser.add_argument("--backend", choices=["file", "redis"], default="file",
                       help="Cache backend to use")
    parser.add_argument("--redis-url", help="Redis connection URL")

    # Commands
    parser.add_argument("--stats", action="store_true",
                       help="Show cache statistics")
    parser.add_argument("--clear", action="store_true",
                       help="Clear all cache entries")
    parser.add_argument("--cleanup", action="store_true",
                       help="Remove expired entries")
    parser.add_argument("--warm", action="store_true",
                       help="Warm cache with common queries")

    # Key operations
    parser.add_argument("--get", metavar="KEY",
                       help="Get value for key")
    parser.add_argument("--set", nargs=2, metavar=("KEY", "VALUE"),
                       help="Set key-value pair")
    parser.add_argument("--delete", metavar="KEY",
                       help="Delete key")
    parser.add_argument("--ttl", type=int, default=3600,
                       help="TTL for --set operation (default: 3600)")

    args = parser.parse_args()

    try:
        # Initialize cache
        cache = CacheManager(backend=args.backend, redis_url=args.redis_url)

        # Execute commands
        if args.stats:
            stats = cache.get_stats()
            print_stats(stats)

        elif args.clear:
            count = cache.invalidate()
            print(f"Cleared {count} cache entries")

        elif args.cleanup:
            count = cache.cleanup_expired()
            print(f"Removed {count} expired entries")

        elif args.warm:
            warm_cache(cache)

        elif args.get:
            value = cache.get(args.get)
            if value is not None:
                print(json.dumps(value, indent=2))
            else:
                print(f"Key not found: {args.get}")
                sys.exit(1)

        elif args.set:
            key, value = args.set
            try:
                # Try to parse as JSON
                parsed_value = json.loads(value)
            except:
                # Use as string
                parsed_value = value

            cache.set(key, parsed_value, ttl=args.ttl)
            print(f"Set {key} with TTL {args.ttl}s")

        elif args.delete:
            if cache.delete(args.delete):
                print(f"Deleted key: {args.delete}")
            else:
                print(f"Key not found: {args.delete}")
                sys.exit(1)

        else:
            parser.print_help()

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
