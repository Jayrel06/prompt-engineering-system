# GitHub Scraper for Prompt Engineering Content

A comprehensive scraper for collecting prompt engineering content from GitHub repositories, awesome lists, and prompt collections.

## Features

- **Topic-based search**: Find repositories by topics like `prompt-engineering`, `llm-prompts`, `chatgpt-prompts`
- **Awesome lists**: Scrape curated awesome lists for prompt collections
- **Smart extraction**: Automatically extracts prompts from README files and markdown documents
- **Rate limit handling**: Respects GitHub API rate limits with automatic backoff
- **Deduplication**: Tracks scraped repositories to avoid duplicates
- **Authentication support**: Works with or without GitHub token (60 vs 5000 requests/hour)

## Installation

No additional dependencies required - uses Python standard library only.

```bash
cd C:/Users/JRiel/prompt-engineering-system/scripts/scrapers
```

## Quick Start

### Basic Usage

```bash
# Search by topic (default: 30 repositories)
python github_scraper.py --topic prompt-engineering

# Search with minimum stars and custom limit
python github_scraper.py --topic llm-prompts --min-stars 100 --limit 50

# Scrape a specific repository
python github_scraper.py --repo "f/awesome-chatgpt-prompts"

# Custom search query
python github_scraper.py --search "system prompt claude" --limit 20

# Scrape all known awesome lists
python github_scraper.py --awesome
```

### With GitHub Token (Recommended)

For higher rate limits (5000 requests/hour instead of 60):

```bash
# Linux/Mac
export GITHUB_TOKEN=your_github_token_here
python github_scraper.py --topic prompt-engineering --limit 100

# Windows (CMD)
set GITHUB_TOKEN=your_github_token_here
python github_scraper.py --topic prompt-engineering --limit 100

# Windows (PowerShell)
$env:GITHUB_TOKEN="your_github_token_here"
python github_scraper.py --topic prompt-engineering --limit 100

# Or use the --token flag
python github_scraper.py --topic prompt-engineering --token your_github_token_here
```

## Command Line Options

| Option | Description | Example |
|--------|-------------|---------|
| `--topic` | Search by GitHub topic | `--topic prompt-engineering` |
| `--search` | Custom search query | `--search "claude system prompt"` |
| `--repo` | Scrape specific repository | `--repo "owner/name"` |
| `--awesome` | Scrape known awesome lists | `--awesome` |
| `--min-stars` | Minimum star count (default: 0) | `--min-stars 100` |
| `--limit` | Max repositories to scrape (default: 30) | `--limit 50` |
| `--output` | Custom output filename | `--output my_results.json` |
| `--token` | GitHub personal access token | `--token ghp_xxx...` |

## Output Format

Results are saved to `data/github/github_scrape_TIMESTAMP.json` with this structure:

```json
{
  "repo": "owner/repository-name",
  "url": "https://github.com/owner/repository-name",
  "description": "Repository description",
  "stars": 5000,
  "topics": ["prompt-engineering", "chatgpt", "llm"],
  "last_updated": "2024-11-01T12:00:00Z",
  "language": "Python",
  "readme_content": "Full README content...",
  "prompt_files": [
    {
      "path": "prompts/system.md",
      "content": "System prompt content..."
    }
  ],
  "extracted_prompts": [
    {
      "type": "code_block",
      "content": "Extracted prompt text...",
      "index": 0
    },
    {
      "type": "section",
      "title": "Prompt Title",
      "content": "Prompt content...",
      "source_file": "prompts/example.md"
    }
  ],
  "scraped_at": "2024-11-27T10:30:00"
}
```

## What Gets Scraped

### Repository Data
- Basic metadata (name, description, stars, topics, language)
- Last update timestamp
- Fork count

### Content
- **README files**: Full content with prompt extraction
- **Prompt files**: Files matching patterns like `*prompt*.md`, `*system*.md`, `*.txt` with "prompt" in name
- **Code blocks**: Fenced code blocks from markdown files
- **Sections**: Markdown sections containing prompt-related keywords

### Extraction Logic

The scraper intelligently extracts prompts by:
1. Finding fenced code blocks (```...```) longer than 50 characters
2. Identifying sections with headers containing keywords: prompt, system, instruction, role, task
3. Parsing markdown files in directories like `prompts/`, `examples/`, `templates/`

## Known Awesome Lists

The scraper includes these curated awesome lists:
- `f/awesome-chatgpt-prompts` - Popular ChatGPT prompts
- `promptslab/Awesome-Prompt-Engineering` - Comprehensive prompt engineering resources
- `ai-boost/awesome-prompts` - AI prompt collection
- `yokoffing/ChatGPT-Prompts` - ChatGPT prompt examples

Access them all with: `python github_scraper.py --awesome`

## Default Topics

When searching without specific topics, these are included:
- `prompt-engineering`
- `llm-prompts`
- `chatgpt-prompts`
- `claude-prompts`
- `ai-prompts`

## Rate Limits

| Authentication | Rate Limit | Delay Between Requests |
|----------------|------------|------------------------|
| No token | 60 requests/hour | 2 seconds |
| With token | 5000 requests/hour | 0.5 seconds |

The scraper automatically:
- Monitors remaining rate limit
- Warns when running low
- Waits for reset if limit exceeded
- Shows reset time

## Data Management

### Cache File
Scraped repositories are cached in `data/github/scraped_repos.json` to:
- Avoid re-scraping the same repositories
- Speed up subsequent runs
- Track scraping history

### Output Organization
All results are saved to `data/github/` with timestamps:
- `github_scrape_20241127_103000.json`
- `github_scrape_20241127_143000.json`

## Examples

### Find High-Quality Prompt Engineering Resources
```bash
python github_scraper.py \
  --topic prompt-engineering \
  --min-stars 500 \
  --limit 20
```

### Scrape Claude-Specific Prompts
```bash
python github_scraper.py \
  --search "claude system prompt" \
  --min-stars 50 \
  --limit 30
```

### Build Complete Prompt Database
```bash
# 1. Scrape awesome lists
python github_scraper.py --awesome

# 2. Search by each topic
python github_scraper.py --topic prompt-engineering --min-stars 100 --limit 50
python github_scraper.py --topic llm-prompts --min-stars 50 --limit 50
python github_scraper.py --topic chatgpt-prompts --min-stars 100 --limit 50
python github_scraper.py --topic claude-prompts --min-stars 10 --limit 30
```

### Monitor Specific Repositories
```bash
python github_scraper.py --repo "anthropics/anthropic-cookbook"
python github_scraper.py --repo "openai/openai-cookbook"
```

## Creating a GitHub Token

1. Go to GitHub Settings → Developer settings → Personal access tokens → Tokens (classic)
2. Click "Generate new token (classic)"
3. Give it a name: "Prompt Engineering Scraper"
4. Select scopes: `public_repo` (for accessing public repositories)
5. Click "Generate token"
6. Copy the token and set it as environment variable

## Troubleshooting

### Rate Limit Exceeded
```
Error: Rate limit exceeded. Try again later or use a GitHub token.
```
**Solution**: Use a GitHub token or wait for the rate limit to reset.

### Repository Not Found
```
Not found: https://api.github.com/repos/...
```
**Solution**: Check the repository name format is correct: `owner/name`

### No Results
```
Found 0 repositories
```
**Solution**: Try different search terms, topics, or lower the `--min-stars` threshold.

## Integration with Prompt Engineering System

The scraper integrates with the larger prompt engineering system:

1. **Data Location**: Saves to `data/github/` for easy access by other tools
2. **Format**: JSON format compatible with embedding and search tools
3. **Deduplication**: Prevents duplicate scraping across runs
4. **Timestamps**: All data timestamped for version tracking

## Advanced Usage

### Combining with Other Tools

```bash
# 1. Scrape repositories
python github_scraper.py --topic prompt-engineering --limit 50

# 2. Process with embedding tool (if available)
# python ../embed_output.py --input data/github/github_scrape_*.json

# 3. Search scraped content (if available)
# python ../search_knowledge.py --query "system prompt for code review"
```

### Custom Filtering

Modify the scraper to add custom filters:
- Edit `_extract_prompts_from_markdown()` for different extraction logic
- Update `DEFAULT_TOPICS` for domain-specific topics
- Add custom file patterns in `_find_prompt_files()`

## License

Part of the Prompt Engineering System project.
