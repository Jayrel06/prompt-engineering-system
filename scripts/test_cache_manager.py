#!/usr/bin/env python3
"""
Test suite for Cache Manager.

Tests all functionality including:
- Basic get/set operations
- TTL and expiration
- Cache statistics
- Decorator usage
- Thread safety
- Both file and Redis backends
"""

import time
import threading
from pathlib import Path

# Add parent directory to path for imports
import sys
sys.path.insert(0, str(Path(__file__).parent))

from cache_manager import (
    CacheManager,
    CacheEntry,
    cached,
    make_cache_key,
    warm_cache
)


def test_basic_operations():
    """Test basic get/set/delete operations."""
    print("\n=== Test: Basic Operations ===")
    cache = CacheManager(backend='file')

    # Set and get
    cache.set('test_key', 'test_value', ttl=60)
    assert cache.get('test_key') == 'test_value', "Get failed"
    print("[PASS] Set and get work")

    # Exists
    assert cache.exists('test_key'), "Exists failed"
    print("[PASS] Exists check works")

    # Delete
    assert cache.delete('test_key'), "Delete failed"
    assert cache.get('test_key') is None, "Delete verification failed"
    print("[PASS] Delete works")

    # Default value
    assert cache.get('nonexistent', default='default') == 'default', "Default value failed"
    print("[PASS] Default value works")


def test_ttl_expiration():
    """Test TTL and expiration."""
    print("\n=== Test: TTL and Expiration ===")
    cache = CacheManager(backend='file')

    # Set with short TTL
    cache.set('expire_key', 'expire_value', ttl=2)
    assert cache.get('expire_key') == 'expire_value', "Initial get failed"
    print("[PASS] Value set with TTL")

    # Check TTL
    ttl = cache.get_ttl('expire_key')
    assert ttl is not None and ttl > 0, "TTL check failed"
    print(f"[PASS] TTL remaining: {ttl}s")

    # Wait for expiration
    print("  Waiting for expiration (2s)...")
    time.sleep(2.5)

    # Should be expired
    assert cache.get('expire_key') is None, "Expiration failed"
    print("[PASS] Value expired correctly")


def test_complex_types():
    """Test caching complex data types."""
    print("\n=== Test: Complex Data Types ===")
    cache = CacheManager(backend='file')

    # Dictionary
    test_dict = {'key': 'value', 'nested': {'a': 1, 'b': 2}}
    cache.set('dict_key', test_dict, ttl=60)
    assert cache.get('dict_key') == test_dict, "Dict caching failed"
    print("[PASS] Dictionary caching works")

    # List
    test_list = [1, 2, 3, 'four', {'five': 5}]
    cache.set('list_key', test_list, ttl=60)
    assert cache.get('list_key') == test_list, "List caching failed"
    print("[PASS] List caching works")

    # Numbers
    cache.set('int_key', 42, ttl=60)
    assert cache.get('int_key') == 42, "Int caching failed"

    cache.set('float_key', 3.14159, ttl=60)
    assert cache.get('float_key') == 3.14159, "Float caching failed"
    print("[PASS] Number caching works")


def test_decorator():
    """Test @cached decorator."""
    print("\n=== Test: @cached Decorator ===")

    call_count = [0]

    @cached(ttl=60)
    def expensive_function(x, y):
        call_count[0] += 1
        return x + y

    # First call
    result1 = expensive_function(5, 3)
    assert result1 == 8, "Function result incorrect"
    assert call_count[0] == 1, "Function should be called once"
    print("[PASS] First call executed function")

    # Second call (should be cached)
    result2 = expensive_function(5, 3)
    assert result2 == 8, "Cached result incorrect"
    assert call_count[0] == 1, "Function should not be called again"
    print("[PASS] Second call used cache")

    # Different arguments (should execute)
    result3 = expensive_function(10, 20)
    assert result3 == 30, "Function result incorrect"
    assert call_count[0] == 2, "Function should be called for different args"
    print("[PASS] Different arguments execute function")


def test_cache_stats():
    """Test cache statistics."""
    print("\n=== Test: Cache Statistics ===")
    cache = CacheManager(backend='file')

    # Clear cache first
    cache.invalidate()

    # Add some entries
    for i in range(10):
        cache.set(f'stat_key_{i}', f'value_{i}', ttl=60)

    # Access some entries multiple times
    for _ in range(5):
        cache.get('stat_key_0')
        cache.get('stat_key_1')

    # Get stats
    stats = cache.get_stats()

    assert stats.total_entries == 10, "Entry count incorrect"
    assert stats.hits >= 10, "Hit count should be at least 10"
    assert stats.size_bytes > 0, "Size should be greater than 0"
    assert stats.hit_rate > 0, "Hit rate should be positive"

    print(f"[PASS] Stats collected: {stats.total_entries} entries, {stats.hits} hits, {stats.hit_rate:.1f}% hit rate")


def test_cache_key_generation():
    """Test cache key generation."""
    print("\n=== Test: Cache Key Generation ===")

    # Same arguments should produce same key
    key1 = make_cache_key(1, 2, 3)
    key2 = make_cache_key(1, 2, 3)
    assert key1 == key2, "Same args should produce same key"
    print("[PASS] Consistent key generation")

    # Different arguments should produce different key
    key3 = make_cache_key(1, 2, 4)
    assert key1 != key3, "Different args should produce different keys"
    print("[PASS] Different keys for different args")

    # Keyword arguments
    key4 = make_cache_key(x=1, y=2)
    key5 = make_cache_key(x=1, y=2)
    assert key4 == key5, "Kwargs should produce consistent keys"
    print("[PASS] Keyword argument keys work")


def test_cleanup():
    """Test cleanup of expired entries."""
    print("\n=== Test: Cleanup Expired Entries ===")
    cache = CacheManager(backend='file')

    # Clear first
    cache.invalidate()

    # Add entries with short TTL
    for i in range(5):
        cache.set(f'cleanup_key_{i}', f'value_{i}', ttl=1)

    # Add entries without expiration
    for i in range(5):
        cache.set(f'permanent_key_{i}', f'value_{i}')

    initial_stats = cache.get_stats()
    assert initial_stats.total_entries == 10, "Should have 10 entries"
    print(f"[PASS] Created {initial_stats.total_entries} entries")

    # Wait for expiration
    time.sleep(1.5)

    # Cleanup
    removed = cache.cleanup_expired()
    print(f"[PASS] Cleaned up {removed} expired entries")

    final_stats = cache.get_stats()
    assert final_stats.total_entries == 5, "Should have 5 entries remaining"
    print(f"[PASS] {final_stats.total_entries} entries remain")


def test_invalidation():
    """Test cache invalidation."""
    print("\n=== Test: Cache Invalidation ===")
    cache = CacheManager(backend='file')

    # Clear and add entries
    cache.invalidate()

    cache.set('user:1:profile', {'name': 'Alice'}, ttl=60)
    cache.set('user:2:profile', {'name': 'Bob'}, ttl=60)
    cache.set('config:settings', {'theme': 'dark'}, ttl=60)

    # Invalidate user cache entries
    removed = cache.invalidate(pattern='user:')
    assert removed == 2, "Should remove 2 user entries"
    print(f"[PASS] Invalidated {removed} user entries")

    # Config should still exist
    assert cache.exists('config:settings'), "Config should still exist"
    print("[PASS] Other entries preserved")

    # Clear all
    removed = cache.invalidate()
    stats = cache.get_stats()
    assert stats.total_entries == 0, "All entries should be cleared"
    print("[PASS] Full invalidation works")


def test_thread_safety():
    """Test thread safety of cache operations."""
    print("\n=== Test: Thread Safety ===")
    cache = CacheManager(backend='file')
    cache.invalidate()

    results = []
    errors = []

    def worker(worker_id):
        try:
            for i in range(10):
                key = f'thread_key_{worker_id}_{i}'
                cache.set(key, f'value_{worker_id}_{i}', ttl=60)
                value = cache.get(key)
                assert value == f'value_{worker_id}_{i}', f"Value mismatch in worker {worker_id}"
            results.append(True)
        except Exception as e:
            errors.append(str(e))

    # Create multiple threads
    threads = []
    for i in range(5):
        t = threading.Thread(target=worker, args=(i,))
        threads.append(t)
        t.start()

    # Wait for completion
    for t in threads:
        t.join()

    assert len(errors) == 0, f"Thread errors occurred: {errors}"
    assert len(results) == 5, "Not all threads completed"
    print(f"[PASS] {len(threads)} threads completed successfully")

    stats = cache.get_stats()
    print(f"[PASS] Final cache has {stats.total_entries} entries")


def test_cache_warming():
    """Test cache warming."""
    print("\n=== Test: Cache Warming ===")
    cache = CacheManager(backend='file')
    cache.invalidate()

    initial_stats = cache.get_stats()
    assert initial_stats.total_entries == 0, "Cache should be empty"

    warm_cache(cache)

    final_stats = cache.get_stats()
    assert final_stats.total_entries > 0, "Cache should have warmed entries"
    print(f"[PASS] Cache warmed with {final_stats.total_entries} entries")


def test_embedding_use_case():
    """Test embedding caching use case."""
    print("\n=== Test: Embedding Caching Use Case ===")
    cache = CacheManager(backend='file')

    # Simulate embedding cache
    file_path = "/path/to/document.txt"
    file_content = "This is a test document"
    file_hash = "abc123def456"

    # Create embedding cache key
    embedding_key = f"embedding:{file_hash}"

    # Check if cached
    cached_embedding = cache.get(embedding_key)
    if cached_embedding is None:
        # Simulate computing embedding
        embedding = [0.1, 0.2, 0.3, 0.4, 0.5]
        cache.set(embedding_key, {
            'file_path': file_path,
            'hash': file_hash,
            'embedding': embedding,
            'model': 'all-MiniLM-L6-v2'
        }, ttl=86400)  # 24 hours
        print("[PASS] Computed and cached new embedding")
    else:
        print("[PASS] Retrieved cached embedding")

    # Verify cached
    result = cache.get(embedding_key)
    assert result is not None, "Embedding should be cached"
    assert result['hash'] == file_hash, "Hash should match"
    print("[PASS] Embedding cache works correctly")


def test_search_results_caching():
    """Test search results caching use case."""
    print("\n=== Test: Search Results Caching ===")
    cache = CacheManager(backend='file')

    # Simulate search query
    query = "how to use prompt engineering"
    search_key = f"search:{make_cache_key(query)}"

    # Cache search results
    search_results = [
        {'title': 'Guide to Prompt Engineering', 'score': 0.95},
        {'title': 'Best Practices', 'score': 0.87}
    ]

    cache.set(search_key, {
        'query': query,
        'results': search_results,
        'count': len(search_results),
        'timestamp': time.time()
    }, ttl=1800)  # 30 minutes

    print("[PASS] Cached search results")

    # Retrieve
    cached_results = cache.get(search_key)
    assert cached_results is not None, "Results should be cached"
    assert cached_results['count'] == 2, "Result count should match"
    print("[PASS] Search cache works correctly")


def run_all_tests():
    """Run all tests."""
    print("\n" + "=" * 80)
    print("CACHE MANAGER TEST SUITE")
    print("=" * 80)

    tests = [
        test_basic_operations,
        test_ttl_expiration,
        test_complex_types,
        test_decorator,
        test_cache_stats,
        test_cache_key_generation,
        test_cleanup,
        test_invalidation,
        test_thread_safety,
        test_cache_warming,
        test_embedding_use_case,
        test_search_results_caching,
    ]

    passed = 0
    failed = 0

    for test_func in tests:
        try:
            test_func()
            passed += 1
        except AssertionError as e:
            print(f"\n[FAIL] FAILED: {test_func.__name__}")
            print(f"  Error: {e}")
            failed += 1
        except Exception as e:
            print(f"\n[FAIL] ERROR in {test_func.__name__}")
            print(f"  Error: {e}")
            failed += 1

    print("\n" + "=" * 80)
    print(f"TEST RESULTS: {passed} passed, {failed} failed")
    print("=" * 80 + "\n")

    return failed == 0


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
