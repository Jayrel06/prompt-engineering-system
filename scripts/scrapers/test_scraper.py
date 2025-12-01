#!/usr/bin/env python3
"""
Test script for Reddit scraper

Validates that the scraper is working correctly without doing a full scrape.
"""

import sys
from pathlib import Path
import requests


def test_reddit_api():
    """Test that Reddit's API is accessible."""
    print("Testing Reddit API accessibility...")

    try:
        response = requests.get(
            'https://www.reddit.com/r/PromptEngineering/hot.json',
            headers={'User-Agent': 'TestBot/1.0'},
            params={'limit': 1},
            timeout=10
        )
        response.raise_for_status()
        data = response.json()

        if 'data' in data and 'children' in data['data']:
            posts = data['data']['children']
            if posts:
                print("✓ Successfully connected to Reddit API")
                print(f"  Sample post: {posts[0]['data']['title'][:50]}...")
                return True
        else:
            print("✗ Unexpected API response format")
            return False

    except Exception as e:
        print(f"✗ Failed to connect to Reddit API: {e}")
        return False


def test_imports():
    """Test that all required modules can be imported."""
    print("\nTesting imports...")

    required_modules = ['requests', 'json', 're', 'argparse', 'pathlib']
    all_ok = True

    for module in required_modules:
        try:
            __import__(module)
            print(f"✓ {module}")
        except ImportError:
            print(f"✗ {module} - not installed")
            all_ok = False

    return all_ok


def test_directories():
    """Test that required directories exist or can be created."""
    print("\nTesting directories...")

    script_dir = Path(__file__).parent
    data_dir = script_dir / '../../data/reddit'

    try:
        data_dir = data_dir.resolve()
        data_dir.mkdir(parents=True, exist_ok=True)
        print(f"✓ Output directory exists: {data_dir}")

        # Test write permissions
        test_file = data_dir / '.test_write'
        test_file.write_text('test')
        test_file.unlink()
        print("✓ Write permissions OK")

        return True
    except Exception as e:
        print(f"✗ Directory test failed: {e}")
        return False


def test_scraper_module():
    """Test that the scraper module can be imported."""
    print("\nTesting scraper module...")

    try:
        script_dir = Path(__file__).parent
        sys.path.insert(0, str(script_dir))

        # Try to import the module
        import reddit_scraper

        print("✓ reddit_scraper module imported successfully")

        # Test basic functionality
        test_text = '''
        Here's a prompt example:

        ```
        You are an expert assistant.
        Task: Help users with their questions.
        ```

        This works well with `inline code` too.
        '''

        scraper = reddit_scraper.RedditScraper(Path('/tmp'))

        code_blocks = scraper._extract_code_blocks(test_text)
        if code_blocks:
            print(f"✓ Code extraction works ({len(code_blocks)} blocks found)")
        else:
            print("⚠ Code extraction returned no results")

        prompts = scraper._extract_prompts(test_text)
        if prompts:
            print(f"✓ Prompt extraction works ({len(prompts)} prompts found)")
        else:
            print("⚠ Prompt extraction returned no results")

        return True

    except Exception as e:
        print(f"✗ Scraper module test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_sample_scrape():
    """Test a minimal scrape operation."""
    print("\nTesting sample scrape (1 post, no comments)...")

    try:
        script_dir = Path(__file__).parent
        sys.path.insert(0, str(script_dir))
        import reddit_scraper

        scraper = reddit_scraper.RedditScraper(Path('/tmp'))

        # Fetch just 1 post without comments
        url = 'https://www.reddit.com/r/PromptEngineering/hot.json'
        params = {'limit': 1}

        data = scraper._make_request(url, params)
        if data and 'data' in data:
            posts = data['data']['children']
            if posts:
                post = scraper._process_post(posts[0], 'PromptEngineering', fetch_comments=False)
                if post:
                    print("✓ Successfully processed a sample post")
                    print(f"  Title: {post['title'][:50]}...")
                    print(f"  Score: {post['score']}")
                    print(f"  Comments: {post['num_comments']}")
                    return True
                else:
                    print("⚠ Post was filtered out (normal if below quality threshold)")
                    return True

        print("✗ Sample scrape failed")
        return False

    except Exception as e:
        print(f"✗ Sample scrape failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Run all tests."""
    print("=" * 60)
    print("Reddit Scraper Test Suite")
    print("=" * 60)

    tests = [
        ("Imports", test_imports),
        ("Directories", test_directories),
        ("Reddit API", test_reddit_api),
        ("Scraper Module", test_scraper_module),
        ("Sample Scrape", test_sample_scrape),
    ]

    results = []
    for name, test_func in tests:
        try:
            result = test_func()
            results.append((name, result))
        except Exception as e:
            print(f"\n✗ {name} test crashed: {e}")
            results.append((name, False))

    # Summary
    print("\n" + "=" * 60)
    print("Test Summary")
    print("=" * 60)

    passed = sum(1 for _, result in results if result)
    total = len(results)

    for name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{status:8} {name}")

    print("-" * 60)
    print(f"Total: {passed}/{total} tests passed")

    if passed == total:
        print("\n✓ All tests passed! The scraper is ready to use.")
        return 0
    else:
        print(f"\n✗ {total - passed} test(s) failed. Please fix the issues above.")
        return 1


if __name__ == '__main__':
    sys.exit(main())
