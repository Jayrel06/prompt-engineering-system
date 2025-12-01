#!/usr/bin/env python3
"""
GitHub Scraper for Prompt Engineering Content

Scrapes GitHub repositories, awesome lists, and prompt collections.
Supports searching by topic, stars, and specific repositories.
Saves data to JSON files with deduplication and rate limit handling.

Usage:
    python github_scraper.py --topic prompt-engineering --min-stars 100 --limit 50
    python github_scraper.py --repo "f/awesome-chatgpt-prompts"
    python github_scraper.py --search "system prompt claude" --limit 30
    python github_scraper.py --awesome
"""

import argparse
import json
import os
import re
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any
from urllib.parse import quote
import urllib.request
import urllib.error

# Configuration
SCRIPT_DIR = Path(__file__).parent
PROJECT_ROOT = SCRIPT_DIR.parent.parent
DATA_DIR = PROJECT_ROOT / "data" / "github"
CACHE_FILE = DATA_DIR / "scraped_repos.json"

# GitHub API configuration
GITHUB_API_BASE = "https://api.github.com"
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN", "")
RATE_LIMIT_DELAY = 2  # seconds between requests when not authenticated
AUTHENTICATED_DELAY = 0.5  # seconds between requests when authenticated

# Known awesome lists for prompt engineering
AWESOME_LISTS = [
    "f/awesome-chatgpt-prompts",
    "promptslab/Awesome-Prompt-Engineering",
    "ai-boost/awesome-prompts",
    "yokoffing/ChatGPT-Prompts",
]

# Topics to search
DEFAULT_TOPICS = [
    "prompt-engineering",
    "llm-prompts",
    "chatgpt-prompts",
    "claude-prompts",
    "ai-prompts",
]


class GitHubScraper:
    """Scrapes GitHub for prompt engineering content."""

    def __init__(self, token: str = ""):
        """Initialize the scraper.

        Args:
            token: GitHub personal access token for higher rate limits
        """
        self.token = token
        self.headers = {
            "Accept": "application/vnd.github.v3+json",
            "User-Agent": "Prompt-Engineering-Scraper/1.0",
        }
        if token:
            self.headers["Authorization"] = f"token {token}"

        self.delay = AUTHENTICATED_DELAY if token else RATE_LIMIT_DELAY
        self.scraped_repos = self._load_cache()

        # Ensure data directory exists
        DATA_DIR.mkdir(parents=True, exist_ok=True)

    def _load_cache(self) -> Dict[str, Any]:
        """Load cache of already scraped repositories."""
        if CACHE_FILE.exists():
            try:
                with open(CACHE_FILE, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                print(f"Warning: Could not load cache: {e}")
        return {}

    def _save_cache(self):
        """Save cache of scraped repositories."""
        try:
            with open(CACHE_FILE, 'w', encoding='utf-8') as f:
                json.dump(self.scraped_repos, f, indent=2)
        except Exception as e:
            print(f"Warning: Could not save cache: {e}")

    def _make_request(self, url: str) -> Optional[Dict]:
        """Make a GitHub API request with rate limit handling.

        Args:
            url: API endpoint URL

        Returns:
            JSON response data or None on error
        """
        try:
            req = urllib.request.Request(url, headers=self.headers)
            with urllib.request.urlopen(req) as response:
                data = json.loads(response.read().decode('utf-8'))

                # Check rate limit
                remaining = response.headers.get('X-RateLimit-Remaining')
                if remaining and int(remaining) < 10:
                    reset_time = int(response.headers.get('X-RateLimit-Reset', 0))
                    wait_time = max(0, reset_time - time.time())
                    if wait_time > 0:
                        print(f"Rate limit low ({remaining} remaining). Waiting {wait_time:.0f}s...")
                        time.sleep(wait_time)

                time.sleep(self.delay)
                return data

        except urllib.error.HTTPError as e:
            if e.code == 403:
                print(f"Rate limit exceeded. Try again later or use a GitHub token.")
                # Check if reset time is in headers
                reset_time = e.headers.get('X-RateLimit-Reset')
                if reset_time:
                    wait_time = max(0, int(reset_time) - time.time())
                    print(f"Rate limit resets in {wait_time:.0f} seconds")
            elif e.code == 404:
                print(f"Not found: {url}")
            else:
                print(f"HTTP error {e.code}: {e.reason}")
            return None
        except Exception as e:
            print(f"Request error: {e}")
            return None

    def _get_file_content(self, repo: str, path: str) -> Optional[str]:
        """Get content of a file from a repository.

        Args:
            repo: Repository in format "owner/name"
            path: File path in repository

        Returns:
            File content as string or None
        """
        url = f"{GITHUB_API_BASE}/repos/{repo}/contents/{quote(path)}"
        data = self._make_request(url)

        if data and 'content' in data:
            import base64
            try:
                content = base64.b64decode(data['content']).decode('utf-8')
                return content
            except Exception as e:
                print(f"Error decoding file content: {e}")
        return None

    def _extract_prompts_from_markdown(self, content: str) -> List[Dict[str, str]]:
        """Extract code blocks and potential prompts from markdown.

        Args:
            content: Markdown content

        Returns:
            List of extracted prompts with metadata
        """
        prompts = []

        # Extract fenced code blocks
        code_block_pattern = r'```(?:[\w]*\n)?(.*?)```'
        blocks = re.findall(code_block_pattern, content, re.DOTALL)

        for i, block in enumerate(blocks):
            block = block.strip()
            if len(block) > 50:  # Filter very short blocks
                prompts.append({
                    "type": "code_block",
                    "content": block,
                    "index": i
                })

        # Extract sections that look like prompts (headers followed by text)
        # Pattern: header followed by substantial text
        section_pattern = r'#{1,3}\s+([^\n]+)\n\n((?:(?!#{1,3}\s+)[^\n]+\n?)+)'
        sections = re.findall(section_pattern, content)

        for title, text in sections:
            text = text.strip()
            # Look for prompt indicators
            if any(keyword in title.lower() or keyword in text.lower()[:200]
                   for keyword in ['prompt', 'system', 'instruction', 'role', 'task']):
                if len(text) > 100:
                    prompts.append({
                        "type": "section",
                        "title": title.strip(),
                        "content": text
                    })

        return prompts

    def search_repositories(
        self,
        query: str = "",
        topic: str = "",
        min_stars: int = 0,
        limit: int = 30
    ) -> List[Dict]:
        """Search for repositories.

        Args:
            query: Search query string
            topic: Topic to filter by
            min_stars: Minimum number of stars
            limit: Maximum number of results

        Returns:
            List of repository data
        """
        # Build search query
        search_parts = []
        if query:
            search_parts.append(query)
        if topic:
            search_parts.append(f"topic:{topic}")
        if min_stars > 0:
            search_parts.append(f"stars:>={min_stars}")

        if not search_parts:
            search_parts.append("prompt engineering")

        search_query = " ".join(search_parts)

        # Search repositories
        url = f"{GITHUB_API_BASE}/search/repositories?q={quote(search_query)}&sort=stars&order=desc&per_page={min(limit, 100)}"

        print(f"Searching: {search_query}")
        data = self._make_request(url)

        if not data or 'items' not in data:
            return []

        repos = []
        for item in data['items'][:limit]:
            repo_data = {
                "repo": item['full_name'],
                "url": item['html_url'],
                "description": item.get('description', ''),
                "stars": item['stargazers_count'],
                "topics": item.get('topics', []),
                "last_updated": item['updated_at'],
                "language": item.get('language'),
                "forks": item['forks_count'],
            }
            repos.append(repo_data)

        print(f"Found {len(repos)} repositories")
        return repos

    def scrape_repository(self, repo: str) -> Optional[Dict]:
        """Scrape a single repository for prompt content.

        Args:
            repo: Repository in format "owner/name"

        Returns:
            Repository data with prompts or None
        """
        print(f"\nScraping repository: {repo}")

        # Check if already scraped
        if repo in self.scraped_repos:
            print(f"  Already scraped (cached)")
            return self.scraped_repos[repo]

        # Get repository info
        repo_url = f"{GITHUB_API_BASE}/repos/{repo}"
        repo_data = self._make_request(repo_url)

        if not repo_data:
            return None

        result = {
            "repo": repo,
            "url": repo_data['html_url'],
            "description": repo_data.get('description', ''),
            "stars": repo_data['stargazers_count'],
            "topics": repo_data.get('topics', []),
            "last_updated": repo_data['updated_at'],
            "language": repo_data.get('language'),
            "readme_content": "",
            "prompt_files": [],
            "extracted_prompts": [],
            "scraped_at": datetime.now().isoformat(),
        }

        # Get README
        print(f"  Fetching README...")
        readme_content = self._get_readme(repo)
        if readme_content:
            result["readme_content"] = readme_content
            result["extracted_prompts"].extend(
                self._extract_prompts_from_markdown(readme_content)
            )

        # Search for prompt files
        print(f"  Searching for prompt files...")
        prompt_files = self._find_prompt_files(repo)
        for file_path in prompt_files[:10]:  # Limit to 10 files per repo
            print(f"    - {file_path}")
            content = self._get_file_content(repo, file_path)
            if content:
                result["prompt_files"].append({
                    "path": file_path,
                    "content": content
                })

                # Extract prompts from file
                if file_path.endswith('.md'):
                    prompts = self._extract_prompts_from_markdown(content)
                    for prompt in prompts:
                        prompt["source_file"] = file_path
                    result["extracted_prompts"].extend(prompts)

        print(f"  Extracted {len(result['extracted_prompts'])} prompts")

        # Cache the result
        self.scraped_repos[repo] = result
        self._save_cache()

        return result

    def _get_readme(self, repo: str) -> Optional[str]:
        """Get README content for a repository.

        Args:
            repo: Repository in format "owner/name"

        Returns:
            README content or None
        """
        url = f"{GITHUB_API_BASE}/repos/{repo}/readme"
        data = self._make_request(url)

        if data and 'content' in data:
            import base64
            try:
                content = base64.b64decode(data['content']).decode('utf-8')
                return content
            except Exception as e:
                print(f"  Error decoding README: {e}")
        return None

    def _find_prompt_files(self, repo: str) -> List[str]:
        """Find files that likely contain prompts.

        Args:
            repo: Repository in format "owner/name"

        Returns:
            List of file paths
        """
        prompt_files = []

        # Search code for prompt-related files
        search_queries = [
            f"repo:{repo} filename:prompt",
            f"repo:{repo} filename:system",
            f"repo:{repo} extension:md prompt",
        ]

        for query in search_queries:
            url = f"{GITHUB_API_BASE}/search/code?q={quote(query)}&per_page=20"
            data = self._make_request(url)

            if data and 'items' in data:
                for item in data['items']:
                    path = item['path']
                    # Filter relevant files
                    if (path.endswith('.md') or path.endswith('.txt')) and path not in prompt_files:
                        prompt_files.append(path)

        return prompt_files

    def scrape_awesome_lists(self) -> List[Dict]:
        """Scrape known awesome lists for prompt engineering.

        Returns:
            List of scraped repository data
        """
        print(f"Scraping {len(AWESOME_LISTS)} awesome lists...")
        results = []

        for repo in AWESOME_LISTS:
            result = self.scrape_repository(repo)
            if result:
                results.append(result)

        return results

    def save_results(self, results: List[Dict], filename: str = None):
        """Save scraping results to JSON file.

        Args:
            results: List of repository data
            filename: Output filename (auto-generated if not provided)
        """
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"github_scrape_{timestamp}.json"

        output_path = DATA_DIR / filename

        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(results, f, indent=2, ensure_ascii=False)

            print(f"\nResults saved to: {output_path}")
            print(f"Total repositories: {len(results)}")
            total_prompts = sum(len(r.get('extracted_prompts', [])) for r in results)
            print(f"Total prompts extracted: {total_prompts}")

        except Exception as e:
            print(f"Error saving results: {e}")


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Scrape GitHub for prompt engineering content",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Search by topic with minimum stars
  python github_scraper.py --topic prompt-engineering --min-stars 100 --limit 50

  # Scrape a specific repository
  python github_scraper.py --repo "f/awesome-chatgpt-prompts"

  # Search with custom query
  python github_scraper.py --search "system prompt claude" --limit 30

  # Scrape all known awesome lists
  python github_scraper.py --awesome

  # Use GitHub token for higher rate limits
  export GITHUB_TOKEN=your_token_here
  python github_scraper.py --topic llm-prompts --limit 100
        """
    )

    parser.add_argument(
        "--topic",
        help="Search repositories by topic"
    )
    parser.add_argument(
        "--search",
        help="Search query string"
    )
    parser.add_argument(
        "--repo",
        help="Scrape a specific repository (format: owner/name)"
    )
    parser.add_argument(
        "--awesome",
        action="store_true",
        help="Scrape known awesome lists for prompts"
    )
    parser.add_argument(
        "--min-stars",
        type=int,
        default=0,
        help="Minimum number of stars (default: 0)"
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=30,
        help="Maximum number of repositories to scrape (default: 30)"
    )
    parser.add_argument(
        "--output",
        help="Output filename (auto-generated if not provided)"
    )
    parser.add_argument(
        "--token",
        help="GitHub personal access token (or use GITHUB_TOKEN env var)"
    )

    args = parser.parse_args()

    # Get GitHub token
    token = args.token or GITHUB_TOKEN
    if not token:
        print("Warning: No GitHub token provided. Rate limited to 60 requests/hour.")
        print("Use --token or set GITHUB_TOKEN environment variable for 5000 requests/hour.")
        print()

    # Initialize scraper
    scraper = GitHubScraper(token=token)
    results = []

    try:
        # Scrape based on arguments
        if args.repo:
            # Scrape specific repository
            result = scraper.scrape_repository(args.repo)
            if result:
                results.append(result)

        elif args.awesome:
            # Scrape awesome lists
            results = scraper.scrape_awesome_lists()

        else:
            # Search and scrape repositories
            repos = scraper.search_repositories(
                query=args.search or "",
                topic=args.topic or "",
                min_stars=args.min_stars,
                limit=args.limit
            )

            print(f"\nScraping {len(repos)} repositories...")
            for i, repo_info in enumerate(repos, 1):
                print(f"\n[{i}/{len(repos)}]")
                result = scraper.scrape_repository(repo_info['repo'])
                if result:
                    results.append(result)

        # Save results
        if results:
            scraper.save_results(results, args.output)
        else:
            print("\nNo results to save.")

    except KeyboardInterrupt:
        print("\n\nScraping interrupted by user.")
        if results:
            print(f"Saving {len(results)} results collected so far...")
            scraper.save_results(results, args.output)
    except Exception as e:
        print(f"\nError: {e}")
        import traceback
        traceback.print_exc()
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
