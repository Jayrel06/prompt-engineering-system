#!/usr/bin/env python3
"""
Quick Scrape Script - Simplified interface for common scraping tasks

This script provides preset configurations for common scraping scenarios.
"""

import argparse
import subprocess
import sys
from pathlib import Path


PRESETS = {
    'daily': {
        'description': 'Daily update - scrape all subreddits for the last day',
        'args': ['--all', '--timeframe', 'day', '--limit', '25']
    },
    'weekly': {
        'description': 'Weekly update - scrape all subreddits for the week',
        'args': ['--all', '--timeframe', 'week', '--limit', '50']
    },
    'monthly': {
        'description': 'Monthly update - scrape all subreddits for the month',
        'args': ['--all', '--timeframe', 'month', '--limit', '100']
    },
    'quick': {
        'description': 'Quick scan - top posts from each subreddit, no comments',
        'args': ['--all', '--timeframe', 'day', '--limit', '10', '--no-comments']
    },
    'claude': {
        'description': 'Search for Claude-specific content across all subreddits',
        'args': ['--search', 'claude', '--all', '--limit', '50']
    },
    'chatgpt': {
        'description': 'Search for ChatGPT-specific content across all subreddits',
        'args': ['--search', 'chatgpt', '--all', '--limit', '50']
    },
    'techniques': {
        'description': 'Search for prompt engineering techniques',
        'args': ['--search', 'prompt technique OR few-shot OR chain-of-thought', '--all', '--limit', '50']
    }
}


def run_scraper(preset_name: str):
    """Run the scraper with a preset configuration."""
    if preset_name not in PRESETS:
        print(f"Error: Unknown preset '{preset_name}'")
        print(f"Available presets: {', '.join(PRESETS.keys())}")
        return 1

    preset = PRESETS[preset_name]
    print(f"Running preset: {preset_name}")
    print(f"Description: {preset['description']}")
    print()

    # Build command
    scraper_path = Path(__file__).parent / 'reddit_scraper.py'
    cmd = [sys.executable, str(scraper_path)] + preset['args']

    print(f"Command: {' '.join(cmd[1:])}")
    print()

    # Run scraper
    try:
        result = subprocess.run(cmd, check=True)
        return result.returncode
    except subprocess.CalledProcessError as e:
        print(f"Error running scraper: {e}")
        return e.returncode
    except KeyboardInterrupt:
        print("\nScraping interrupted by user")
        return 130


def main():
    parser = argparse.ArgumentParser(
        description='Quick scrape with preset configurations',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=f"""
Available presets:

{chr(10).join(f"  {name:12} - {info['description']}" for name, info in PRESETS.items())}

Examples:
  %(prog)s daily     # Daily update
  %(prog)s claude    # Search for Claude content
  %(prog)s quick     # Fast scan without comments
        """
    )

    parser.add_argument(
        'preset',
        choices=list(PRESETS.keys()),
        help='Preset configuration to use'
    )

    parser.add_argument(
        '--list',
        action='store_true',
        help='List all available presets'
    )

    args = parser.parse_args()

    if args.list:
        print("Available presets:")
        for name, info in PRESETS.items():
            print(f"\n{name}:")
            print(f"  Description: {info['description']}")
            print(f"  Arguments: {' '.join(info['args'])}")
        return 0

    return run_scraper(args.preset)


if __name__ == '__main__':
    sys.exit(main())
