# GitHub Scraper - Quick Start Guide

## Installation

```bash
cd C:/Users/JRiel/prompt-engineering-system/scripts/scrapers
# No dependencies needed - uses Python standard library only
```

## Most Common Commands

### 1. Scrape Top Prompt Engineering Repos
```bash
python github_scraper.py --topic prompt-engineering --min-stars 100 --limit 20
```

### 2. Scrape All Awesome Lists
```bash
python github_scraper.py --awesome
```

### 3. Search for Specific Content
```bash
python github_scraper.py --search "claude system prompt" --limit 30
```

### 4. Scrape a Specific Repository
```bash
python github_scraper.py --repo "f/awesome-chatgpt-prompts"
```

## With GitHub Token (Recommended)

Get 5000 requests/hour instead of 60:

```bash
# Windows PowerShell
$env:GITHUB_TOKEN="your_token_here"
python github_scraper.py --topic prompt-engineering --limit 100

# Windows CMD
set GITHUB_TOKEN=your_token_here
python github_scraper.py --topic prompt-engineering --limit 100

# Linux/Mac
export GITHUB_TOKEN=your_token_here
python github_scraper.py --topic prompt-engineering --limit 100
```

## Output Location

All scraped data goes to:
```
C:/Users/JRiel/prompt-engineering-system/data/github/
```

Files are named: `github_scrape_TIMESTAMP.json`

## What Gets Scraped

For each repository:
- Repository metadata (stars, topics, description)
- README content
- Prompt files (*.md, *.txt with "prompt" in name)
- Extracted prompts from code blocks
- Extracted prompts from markdown sections

## Example Output

```json
{
  "repo": "dair-ai/Prompt-Engineering-Guide",
  "url": "https://github.com/dair-ai/Prompt-Engineering-Guide",
  "stars": 67097,
  "topics": ["prompt-engineering", "llm"],
  "readme_content": "...",
  "extracted_prompts": [
    {
      "type": "code_block",
      "content": "You are an expert..."
    }
  ]
}
```

## Useful Combinations

### Build a Comprehensive Database
```bash
# Step 1: Get awesome lists
python github_scraper.py --awesome

# Step 2: Search by topics
python github_scraper.py --topic prompt-engineering --min-stars 100 --limit 50
python github_scraper.py --topic llm-prompts --min-stars 50 --limit 50
python github_scraper.py --topic chatgpt-prompts --min-stars 100 --limit 50

# Step 3: Search for specific use cases
python github_scraper.py --search "system prompt code" --min-stars 50
python github_scraper.py --search "claude prompt examples" --limit 30
```

### Target High-Quality Repos Only
```bash
python github_scraper.py --topic prompt-engineering --min-stars 1000 --limit 10
```

## Common Issues

### Rate Limited
```
Error: Rate limit exceeded
```
**Fix**: Use a GitHub token or wait for reset

### No Results
```
Found 0 repositories
```
**Fix**: Try lower --min-stars or different search terms

## Creating a GitHub Token

1. Go to: https://github.com/settings/tokens
2. Generate new token (classic)
3. Select scope: `public_repo`
4. Copy token and use as shown above

## Need Help?

```bash
python github_scraper.py --help
```

See full documentation: `GITHUB_README.md`
