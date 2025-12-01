#!/usr/bin/env python3
"""
Cache Manager Installation Verification

Verifies that cache_manager is properly installed and working.
"""

import sys
from pathlib import Path

def check_import():
    """Test importing cache_manager."""
    try:
        from cache_manager import (
            CacheManager,
            CacheEntry,
            CacheStats,
            cached,
            make_cache_key,
            warm_cache
        )
        print("[PASS] Cache manager imports successfully")
        return True
    except ImportError as e:
        print(f"[FAIL] Import failed: {e}")
        return False


def check_basic_operations():
    """Test basic cache operations."""
    try:
        from cache_manager import CacheManager

        cache = CacheManager(backend='file')

        # Test set/get
        cache.set('test', 'value', ttl=60)
        result = cache.get('test')

        if result == 'value':
            print("[PASS] Basic get/set operations work")
            return True
        else:
            print(f"[FAIL] Expected 'value', got {result}")
            return False
    except Exception as e:
        print(f"[FAIL] Basic operations failed: {e}")
        return False


def check_decorator():
    """Test @cached decorator."""
    try:
        from cache_manager import cached, CacheManager
        import time

        # Clear cache to ensure clean test
        cache = CacheManager()
        cache.invalidate()

        call_count = [0]

        @cached(ttl=60)
        def test_func(x):
            call_count[0] += 1
            return x * 2

        # Use unique value to avoid conflicts
        test_val = int(time.time()) % 1000
        result1 = test_func(test_val)
        result2 = test_func(test_val)

        expected = test_val * 2
        if result1 == expected and result2 == expected and call_count[0] == 1:
            print("[PASS] @cached decorator works")
            return True
        else:
            print(f"[FAIL] Decorator test failed: results={result1},{result2}, calls={call_count[0]}")
            return False
    except Exception as e:
        print(f"[FAIL] Decorator test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def check_stats():
    """Test cache statistics."""
    try:
        from cache_manager import CacheManager

        cache = CacheManager(backend='file')
        stats = cache.get_stats()

        if hasattr(stats, 'hits') and hasattr(stats, 'misses'):
            print("[PASS] Cache statistics work")
            return True
        else:
            print("[FAIL] Stats missing attributes")
            return False
    except Exception as e:
        print(f"[FAIL] Stats test failed: {e}")
        return False


def check_files():
    """Check that all files exist."""
    script_dir = Path(__file__).parent
    required_files = [
        'cache_manager.py',
        'test_cache_manager.py',
        'cache_integration_examples.py',
        'CACHE_MANAGER_README.md',
        'CACHE_QUICKSTART.md',
        'CACHE_MANAGER_SUMMARY.md'
    ]

    all_exist = True
    for filename in required_files:
        filepath = script_dir / filename
        if filepath.exists():
            print(f"[PASS] {filename} exists")
        else:
            print(f"[FAIL] {filename} not found")
            all_exist = False

    return all_exist


def check_redis_support():
    """Check if Redis support is available (optional)."""
    try:
        import redis
        print("[INFO] Redis support available (optional)")
        return True
    except ImportError:
        print("[INFO] Redis not installed (optional - file backend will be used)")
        return True  # Not required


def main():
    """Run all verification checks."""
    print("=" * 80)
    print("CACHE MANAGER INSTALLATION VERIFICATION")
    print("=" * 80)
    print()

    checks = [
        ("File existence", check_files),
        ("Module imports", check_import),
        ("Basic operations", check_basic_operations),
        ("Decorator functionality", check_decorator),
        ("Statistics tracking", check_stats),
        ("Redis support", check_redis_support),
    ]

    passed = 0
    failed = 0

    for name, check_func in checks:
        print(f"\nChecking: {name}")
        print("-" * 40)
        try:
            if check_func():
                passed += 1
            else:
                failed += 1
        except Exception as e:
            print(f"[FAIL] Unexpected error: {e}")
            failed += 1

    print("\n" + "=" * 80)
    print(f"VERIFICATION RESULTS: {passed}/{len(checks)} passed")
    print("=" * 80)

    if failed == 0:
        print("\n[SUCCESS] Cache manager is properly installed and working!")
        print("\nNext steps:")
        print("  1. Run tests: python test_cache_manager.py")
        print("  2. Try examples: python cache_integration_examples.py")
        print("  3. Check CLI: python cache_manager.py --help")
        print("  4. View docs: cat CACHE_QUICKSTART.md")
        return 0
    else:
        print(f"\n[ERROR] {failed} check(s) failed. Please review errors above.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
