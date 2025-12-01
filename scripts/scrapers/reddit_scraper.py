#!/usr/bin/env python3
"""
Reddit Scraper for Prompt Engineering Knowledge

Scrapes Reddit posts and comments from AI/prompt engineering subreddits
using Reddit's public JSON API (no authentication required).

Usage:
    python reddit_scraper.py --subreddit PromptEngineering --timeframe week --limit 50
    python reddit_scraper.py --all --timeframe month
    python reddit_scraper.py --search "claude prompt" --limit 100
"""

import argparse
import json
import re
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Set
from urllib.parse import urljoin
import requests


# Configuration
SUBREDDITS = [
    'PromptEngineering',
    'ChatGPT',
    'ClaudeAI',
    'LocalLLaMA',
    'MachineLearning',
    'artificial'
]

MACHINE_LEARNING_KEYWORDS = [
    'prompt', 'prompting', 'gpt', 'llm', 'language model',
    'claude', 'chatgpt', 'instruction', 'few-shot', 'zero-shot'
]

BASE_URL = 'https://www.reddit.com'
USER_AGENT = 'PromptEngineeringResearchBot/1.0 (Educational purposes)'

# Quality thresholds
MIN_SCORE = 5
MIN_COMMENTS = 2
MAX_TOP_COMMENTS = 10

# Rate limiting
RATE_LIMIT_DELAY = 2  # seconds between requests


class RedditScraper:
    """Scrapes Reddit posts and comments using the public JSON API."""

    def __init__(self, output_dir: Path):
        self.output_dir = output_dir
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.session = requests.Session()
        self.session.headers.update({'User-Agent': USER_AGENT})
        self.scraped_ids: Set[str] = set()
        self._load_existing_ids()

    def _load_existing_ids(self):
        """Load existing post IDs to avoid duplicates."""
        for json_file in self.output_dir.glob('*.json'):
            try:
                with open(json_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    if isinstance(data, list):
                        self.scraped_ids.update(post['id'] for post in data if 'id' in post)
                    elif isinstance(data, dict) and 'id' in data:
                        self.scraped_ids.add(data['id'])
            except Exception as e:
                print(f"Warning: Could not load {json_file}: {e}")

    def _make_request(self, url: str, params: Optional[Dict] = None) -> Optional[Dict]:
        """Make a rate-limited request to Reddit's API."""
        try:
            time.sleep(RATE_LIMIT_DELAY)
            response = self.session.get(url, params=params, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching {url}: {e}")
            return None

    def _extract_code_blocks(self, text: str) -> List[str]:
        """Extract code blocks from markdown text."""
        if not text:
            return []

        # Match fenced code blocks (```...```)
        fenced_pattern = r'```(?:\w+)?\n(.*?)```'
        fenced_blocks = re.findall(fenced_pattern, text, re.DOTALL)

        # Match indented code blocks (4 spaces or tab)
        indented_pattern = r'(?:^|\n)((?:(?:    |\t).+\n?)+)'
        indented_blocks = re.findall(indented_pattern, text, re.MULTILINE)

        # Match inline code (`...`)
        inline_pattern = r'`([^`\n]+)`'
        inline_blocks = re.findall(inline_pattern, text)

        all_blocks = fenced_blocks + indented_blocks + inline_blocks
        return [block.strip() for block in all_blocks if block.strip()]

    def _extract_prompts(self, text: str) -> List[str]:
        """Extract potential prompt examples from text."""
        if not text:
            return []

        prompts = []

        # Look for quoted text that looks like prompts
        quote_patterns = [
            r'"([^"]{50,500})"',  # Double quotes
            r"'([^']{50,500})'",  # Single quotes
        ]

        for pattern in quote_patterns:
            matches = re.findall(pattern, text, re.DOTALL)
            for match in matches:
                # Check if it contains prompt-related keywords
                lower_match = match.lower()
                if any(keyword in lower_match for keyword in [
                    'you are', 'act as', 'pretend', 'imagine', 'role',
                    'task:', 'instruction:', 'prompt:', 'system:',
                    'assistant', 'user:', 'context:', 'examples:'
                ]):
                    prompts.append(match.strip())

        # Look for sections explicitly labeled as prompts
        prompt_section_pattern = r'(?:prompt|example|instruction)s?:\s*\n+(.*?)(?:\n\n|\n#|$)'
        sections = re.findall(prompt_section_pattern, text, re.IGNORECASE | re.DOTALL)
        prompts.extend([s.strip() for s in sections if len(s.strip()) > 30])

        return list(set(prompts))[:5]  # Return up to 5 unique prompts

    def _process_comment(self, comment_data: Dict) -> Optional[Dict]:
        """Process a single comment."""
        if comment_data.get('kind') != 't1':
            return None

        data = comment_data.get('data', {})
        body = data.get('body', '')

        # Skip deleted/removed comments
        if body in ['[deleted]', '[removed]', '']:
            return None

        return {
            'author': data.get('author', '[deleted]'),
            'body': body,
            'score': data.get('score', 0),
            'created_utc': data.get('created_utc', 0),
            'id': data.get('id', ''),
            'extracted_code': self._extract_code_blocks(body),
            'extracted_prompts': self._extract_prompts(body)
        }

    def _fetch_comments(self, subreddit: str, post_id: str) -> List[Dict]:
        """Fetch top-level comments for a post."""
        url = f"{BASE_URL}/r/{subreddit}/comments/{post_id}.json"
        data = self._make_request(url, params={'limit': MAX_TOP_COMMENTS, 'depth': 1})

        if not data or len(data) < 2:
            return []

        comments = []
        comment_listing = data[1].get('data', {}).get('children', [])

        for comment_data in comment_listing[:MAX_TOP_COMMENTS]:
            comment = self._process_comment(comment_data)
            if comment:
                comments.append(comment)

        return comments

    def _process_post(self, post_data: Dict, subreddit: str, fetch_comments: bool = True) -> Optional[Dict]:
        """Process a single post."""
        data = post_data.get('data', {})

        # Extract basic info
        post_id = data.get('id', '')
        title = data.get('title', '')
        selftext = data.get('selftext', '')
        score = data.get('score', 0)
        num_comments = data.get('num_comments', 0)

        # Apply quality filters
        if score < MIN_SCORE or num_comments < MIN_COMMENTS:
            return None

        # Skip if already scraped
        if post_id in self.scraped_ids:
            return None

        # For MachineLearning, filter by keywords
        if subreddit.lower() == 'machinelearning':
            text_to_check = (title + ' ' + selftext).lower()
            if not any(keyword in text_to_check for keyword in MACHINE_LEARNING_KEYWORDS):
                return None

        # Fetch comments if requested
        top_comments = []
        if fetch_comments and num_comments > 0:
            top_comments = self._fetch_comments(subreddit, post_id)

        post = {
            'id': post_id,
            'subreddit': subreddit,
            'title': title,
            'body': selftext,
            'url': data.get('url', ''),
            'permalink': urljoin(BASE_URL, data.get('permalink', '')),
            'score': score,
            'num_comments': num_comments,
            'created_utc': data.get('created_utc', 0),
            'created_date': datetime.fromtimestamp(data.get('created_utc', 0)).isoformat(),
            'author': data.get('author', '[deleted]'),
            'flair': data.get('link_flair_text', ''),
            'top_comments': top_comments,
            'extracted_code': self._extract_code_blocks(selftext),
            'extracted_prompts': self._extract_prompts(selftext)
        }

        self.scraped_ids.add(post_id)
        return post

    def scrape_subreddit(
        self,
        subreddit: str,
        timeframe: str = 'week',
        limit: int = 50,
        fetch_comments: bool = True
    ) -> List[Dict]:
        """Scrape top posts from a subreddit."""
        print(f"Scraping r/{subreddit} (timeframe: {timeframe}, limit: {limit})...")

        url = f"{BASE_URL}/r/{subreddit}/top.json"
        params = {
            't': timeframe,
            'limit': min(limit, 100)  # Reddit API max is 100
        }

        data = self._make_request(url, params=params)
        if not data:
            print(f"Failed to fetch data from r/{subreddit}")
            return []

        posts = []
        post_listing = data.get('data', {}).get('children', [])

        for post_data in post_listing:
            post = self._process_post(post_data, subreddit, fetch_comments)
            if post:
                posts.append(post)
                print(f"  [{len(posts)}/{limit}] {post['title'][:60]}... (score: {post['score']})")

        print(f"Scraped {len(posts)} posts from r/{subreddit}")
        return posts

    def search_subreddit(
        self,
        subreddit: str,
        query: str,
        limit: int = 100,
        fetch_comments: bool = True
    ) -> List[Dict]:
        """Search for posts in a subreddit."""
        print(f"Searching r/{subreddit} for '{query}' (limit: {limit})...")

        url = f"{BASE_URL}/r/{subreddit}/search.json"
        params = {
            'q': query,
            'restrict_sr': 'on',
            'sort': 'relevance',
            'limit': min(limit, 100)
        }

        data = self._make_request(url, params=params)
        if not data:
            print(f"Failed to search r/{subreddit}")
            return []

        posts = []
        post_listing = data.get('data', {}).get('children', [])

        for post_data in post_listing:
            post = self._process_post(post_data, subreddit, fetch_comments)
            if post:
                posts.append(post)
                print(f"  [{len(posts)}/{limit}] {post['title'][:60]}... (score: {post['score']})")

        print(f"Found {len(posts)} posts in r/{subreddit}")
        return posts

    def search_all_subreddits(
        self,
        query: str,
        limit_per_subreddit: int = 50,
        fetch_comments: bool = True
    ) -> Dict[str, List[Dict]]:
        """Search across all configured subreddits."""
        results = {}
        for subreddit in SUBREDDITS:
            posts = self.search_subreddit(subreddit, query, limit_per_subreddit, fetch_comments)
            if posts:
                results[subreddit] = posts
        return results

    def scrape_all_subreddits(
        self,
        timeframe: str = 'week',
        limit_per_subreddit: int = 50,
        fetch_comments: bool = True
    ) -> Dict[str, List[Dict]]:
        """Scrape all configured subreddits."""
        results = {}
        for subreddit in SUBREDDITS:
            posts = self.scrape_subreddit(subreddit, timeframe, limit_per_subreddit, fetch_comments)
            if posts:
                results[subreddit] = posts
        return results

    def save_results(self, results: Dict[str, List[Dict]], prefix: str = 'reddit'):
        """Save scraping results to JSON files."""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')

        for subreddit, posts in results.items():
            filename = f"{prefix}_{subreddit.lower()}_{timestamp}.json"
            filepath = self.output_dir / filename

            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(posts, f, indent=2, ensure_ascii=False)

            print(f"Saved {len(posts)} posts to {filepath}")

    def get_stats(self) -> Dict:
        """Get statistics about scraped data."""
        all_posts = []
        for json_file in self.output_dir.glob('*.json'):
            try:
                with open(json_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    if isinstance(data, list):
                        all_posts.extend(data)
                    elif isinstance(data, dict):
                        all_posts.append(data)
            except Exception:
                continue

        if not all_posts:
            return {'total_posts': 0}

        total_code_blocks = sum(len(post.get('extracted_code', [])) for post in all_posts)
        total_prompts = sum(len(post.get('extracted_prompts', [])) for post in all_posts)
        total_comments = sum(len(post.get('top_comments', [])) for post in all_posts)

        subreddit_counts = {}
        for post in all_posts:
            sub = post.get('subreddit', 'unknown')
            subreddit_counts[sub] = subreddit_counts.get(sub, 0) + 1

        return {
            'total_posts': len(all_posts),
            'total_code_blocks': total_code_blocks,
            'total_prompts': total_prompts,
            'total_comments': total_comments,
            'posts_by_subreddit': subreddit_counts,
            'avg_score': sum(post.get('score', 0) for post in all_posts) / len(all_posts),
            'avg_comments': sum(post.get('num_comments', 0) for post in all_posts) / len(all_posts)
        }


def main():
    """Main CLI interface."""
    parser = argparse.ArgumentParser(
        description='Scrape Reddit for prompt engineering knowledge',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Scrape top posts from PromptEngineering subreddit
  %(prog)s --subreddit PromptEngineering --timeframe week --limit 50

  # Scrape all configured subreddits
  %(prog)s --all --timeframe month --limit 100

  # Search for specific terms
  %(prog)s --search "claude prompt" --limit 100

  # Search all subreddits for a term
  %(prog)s --search "few-shot learning" --all

  # Get statistics
  %(prog)s --stats
        """
    )

    parser.add_argument(
        '--subreddit',
        type=str,
        help='Subreddit to scrape (without r/)'
    )

    parser.add_argument(
        '--all',
        action='store_true',
        help='Scrape all configured subreddits'
    )

    parser.add_argument(
        '--timeframe',
        choices=['hour', 'day', 'week', 'month', 'year', 'all'],
        default='week',
        help='Timeframe for top posts (default: week)'
    )

    parser.add_argument(
        '--limit',
        type=int,
        default=50,
        help='Number of posts to fetch per subreddit (default: 50, max: 100)'
    )

    parser.add_argument(
        '--search',
        type=str,
        help='Search query instead of fetching top posts'
    )

    parser.add_argument(
        '--no-comments',
        action='store_true',
        help='Skip fetching comments (faster)'
    )

    parser.add_argument(
        '--output-dir',
        type=Path,
        help='Output directory for JSON files (default: ../../data/reddit/)'
    )

    parser.add_argument(
        '--stats',
        action='store_true',
        help='Show statistics about scraped data'
    )

    parser.add_argument(
        '--list-subreddits',
        action='store_true',
        help='List configured subreddits'
    )

    args = parser.parse_args()

    # List subreddits
    if args.list_subreddits:
        print("Configured subreddits:")
        for sub in SUBREDDITS:
            print(f"  - r/{sub}")
        return

    # Determine output directory
    if args.output_dir:
        output_dir = args.output_dir
    else:
        script_dir = Path(__file__).parent
        output_dir = script_dir / '../../data/reddit'

    output_dir = output_dir.resolve()

    # Initialize scraper
    scraper = RedditScraper(output_dir)

    # Show stats
    if args.stats:
        stats = scraper.get_stats()
        print("\n=== Reddit Scraper Statistics ===")
        print(f"Total posts: {stats.get('total_posts', 0)}")
        print(f"Total code blocks: {stats.get('total_code_blocks', 0)}")
        print(f"Total prompts: {stats.get('total_prompts', 0)}")
        print(f"Total comments: {stats.get('total_comments', 0)}")

        if stats.get('total_posts', 0) > 0:
            print(f"Average score: {stats.get('avg_score', 0):.1f}")
            print(f"Average comments: {stats.get('avg_comments', 0):.1f}")

            print("\nPosts by subreddit:")
            for sub, count in sorted(
                stats.get('posts_by_subreddit', {}).items(),
                key=lambda x: x[1],
                reverse=True
            ):
                print(f"  r/{sub}: {count}")

        return

    # Validate arguments
    if not (args.subreddit or args.all):
        parser.error('Must specify --subreddit or --all')

    fetch_comments = not args.no_comments

    # Execute scraping
    results = {}

    if args.search:
        # Search mode
        if args.all:
            results = scraper.search_all_subreddits(
                args.search,
                limit_per_subreddit=args.limit,
                fetch_comments=fetch_comments
            )
            prefix = f"search_{args.search.replace(' ', '_')}"
        elif args.subreddit:
            posts = scraper.search_subreddit(
                args.subreddit,
                args.search,
                limit=args.limit,
                fetch_comments=fetch_comments
            )
            results[args.subreddit] = posts
            prefix = f"search_{args.search.replace(' ', '_')}"
    else:
        # Top posts mode
        if args.all:
            results = scraper.scrape_all_subreddits(
                timeframe=args.timeframe,
                limit_per_subreddit=args.limit,
                fetch_comments=fetch_comments
            )
            prefix = f"top_{args.timeframe}"
        elif args.subreddit:
            posts = scraper.scrape_subreddit(
                args.subreddit,
                timeframe=args.timeframe,
                limit=args.limit,
                fetch_comments=fetch_comments
            )
            results[args.subreddit] = posts
            prefix = f"top_{args.timeframe}"

    # Save results
    if results:
        scraper.save_results(results, prefix=prefix)

        # Print summary
        total_posts = sum(len(posts) for posts in results.values())
        print(f"\n=== Summary ===")
        print(f"Total posts scraped: {total_posts}")
        print(f"Output directory: {output_dir}")
    else:
        print("No posts found matching criteria.")


if __name__ == '__main__':
    main()
