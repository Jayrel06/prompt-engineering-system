#!/usr/bin/env python3
"""
Example usage of the GitHub scraper for prompt engineering content.

This demonstrates how to use the GitHubScraper class programmatically
in addition to the CLI interface.
"""

import os
from github_scraper import GitHubScraper

# Example 1: Basic scraper initialization
print("Example 1: Initialize scraper")
print("-" * 50)
scraper = GitHubScraper()
print("Scraper initialized without token (60 requests/hour)")
print()

# Example 2: Initialize with token for higher rate limits
print("Example 2: Initialize with GitHub token")
print("-" * 50)
token = os.environ.get("GITHUB_TOKEN", "")
if token:
    scraper = GitHubScraper(token=token)
    print("Scraper initialized with token (5000 requests/hour)")
else:
    print("No GITHUB_TOKEN found in environment")
    print("To use a token: export GITHUB_TOKEN=your_token_here")
print()

# Example 3: Search for repositories by topic
print("Example 3: Search repositories by topic")
print("-" * 50)
repos = scraper.search_repositories(
    topic="prompt-engineering",
    min_stars=100,
    limit=5
)
print(f"Found {len(repos)} repositories with topic 'prompt-engineering' and 100+ stars")
for repo in repos:
    print(f"  - {repo['repo']}: {repo['stars']} stars")
print()

# Example 4: Search with custom query
print("Example 4: Custom search query")
print("-" * 50)
repos = scraper.search_repositories(
    query="claude system prompt",
    limit=3
)
print(f"Found {len(repos)} repositories matching 'claude system prompt'")
for repo in repos:
    print(f"  - {repo['repo']}: {repo['description'][:60]}...")
print()

# Example 5: Scrape a specific repository
print("Example 5: Scrape specific repository")
print("-" * 50)
print("To scrape a repository:")
print('  result = scraper.scrape_repository("f/awesome-chatgpt-prompts")')
print('  print(f"README length: {len(result[\'readme_content\'])} chars")')
print('  print(f"Prompts extracted: {len(result[\'extracted_prompts\'])}")')
print()

# Example 6: Save results
print("Example 6: Save scraping results")
print("-" * 50)
print("To save results:")
print('  scraper.save_results(results, "my_custom_output.json")')
print("Results will be saved to: data/github/my_custom_output.json")
print()

# Example 7: Known awesome lists
print("Example 7: Scrape awesome lists")
print("-" * 50)
print("To scrape all known awesome lists:")
print('  results = scraper.scrape_awesome_lists()')
print("This will scrape:")
from github_scraper import AWESOME_LISTS
for repo in AWESOME_LISTS:
    print(f"  - {repo}")
print()

# Example 8: Extract prompts from markdown
print("Example 8: Extract prompts from markdown content")
print("-" * 50)
sample_markdown = """
# Example Prompt Collection

## System Prompt for Code Review

```
You are an expert code reviewer. Analyze the following code for:
- Security vulnerabilities
- Performance issues
- Best practices violations

Provide specific, actionable feedback.
```

## Task Prompt

Act as a technical writer. Create clear, concise documentation for the API endpoint.
"""

prompts = scraper._extract_prompts_from_markdown(sample_markdown)
print(f"Extracted {len(prompts)} prompts from sample markdown:")
for i, prompt in enumerate(prompts, 1):
    print(f"  Prompt {i} ({prompt['type']}): {prompt['content'][:60]}...")
print()

print("=" * 50)
print("For full CLI usage, run: python github_scraper.py --help")
print("=" * 50)
