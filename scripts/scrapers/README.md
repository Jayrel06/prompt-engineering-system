# Reddit Scraper for Prompt Engineering

A Python-based scraper that collects prompt engineering knowledge from Reddit using the public JSON API (no authentication required).

## Features

- **No Authentication Required**: Uses Reddit's public JSON API
- **Multiple Subreddits**: Scrapes r/PromptEngineering, r/ChatGPT, r/ClaudeAI, r/LocalLLaMA, r/MachineLearning, r/artificial
- **Smart Filtering**: Quality thresholds, keyword filtering for r/MachineLearning
- **Content Extraction**: Automatically extracts code blocks and prompt examples
- **Comment Support**: Fetches top-level comments from posts
- **Deduplication**: Tracks scraped post IDs to avoid duplicates
- **Rate Limiting**: Respects Reddit's API with 2-second delays
- **Multiple Modes**: Top posts by timeframe, search queries, or both

## Installation

```bash
cd scripts/scrapers
pip install -r requirements.txt
```

## Usage

### Basic Examples

```bash
# Scrape top posts from a single subreddit
python reddit_scraper.py --subreddit PromptEngineering --timeframe week --limit 50

# Scrape all configured subreddits
python reddit_scraper.py --all --timeframe month --limit 100

# Search for specific terms
python reddit_scraper.py --search "claude prompt" --limit 100

# Search all subreddits
python reddit_scraper.py --search "few-shot learning" --all

# Skip comments for faster scraping
python reddit_scraper.py --all --timeframe day --no-comments

# Get statistics
python reddit_scraper.py --stats

# List configured subreddits
python reddit_scraper.py --list-subreddits
```

### Command-Line Options

- `--subreddit SUBREDDIT`: Subreddit to scrape (without r/)
- `--all`: Scrape all configured subreddits
- `--timeframe {hour,day,week,month,year,all}`: Timeframe for top posts (default: week)
- `--limit LIMIT`: Number of posts per subreddit (default: 50, max: 100)
- `--search QUERY`: Search for specific terms instead of top posts
- `--no-comments`: Skip fetching comments (faster)
- `--output-dir DIR`: Custom output directory (default: ../../data/reddit/)
- `--stats`: Show statistics about scraped data
- `--list-subreddits`: List all configured subreddits

## Output Format

Each post is saved as JSON with the following structure:

```json
{
  "id": "abc123",
  "subreddit": "PromptEngineering",
  "title": "Amazing prompt technique",
  "body": "Post content here...",
  "url": "https://reddit.com/...",
  "permalink": "https://reddit.com/r/PromptEngineering/comments/...",
  "score": 150,
  "num_comments": 45,
  "created_utc": 1700000000,
  "created_date": "2023-11-14T16:53:20",
  "author": "username",
  "flair": "Discussion",
  "top_comments": [
    {
      "author": "commenter",
      "body": "Great insight!",
      "score": 25,
      "created_utc": 1700001000,
      "id": "comment123",
      "extracted_code": ["code example"],
      "extracted_prompts": ["prompt example"]
    }
  ],
  "extracted_code": ["```python\ncode here\n```"],
  "extracted_prompts": ["You are an expert..."]
}
```

## Configuration

### Subreddits

The scraper targets these subreddits by default:
- **r/PromptEngineering**: Dedicated prompt engineering discussions
- **r/ChatGPT**: ChatGPT-specific prompts and techniques
- **r/ClaudeAI**: Claude-specific content
- **r/LocalLLaMA**: Local LLM and prompting techniques
- **r/MachineLearning**: Filtered for prompt-related content
- **r/artificial**: General AI discussions

### Quality Thresholds

- Minimum score: 5 upvotes
- Minimum comments: 2
- Maximum comments fetched: 10 (top-level only)

### Rate Limiting

- 2-second delay between requests
- Respects Reddit's API limits

## Content Extraction

### Code Blocks

Automatically extracts:
- Fenced code blocks (```...```)
- Indented code blocks (4 spaces or tab)
- Inline code (`...`)

### Prompt Examples

Identifies prompts by looking for:
- Quoted text with prompt keywords
- Sections labeled "prompt:", "example:", "instruction:"
- Text containing: "You are", "Act as", "Task:", etc.

## File Organization

```
data/reddit/
├── top_week_promptengineering_20241201_120000.json
├── top_week_chatgpt_20241201_120030.json
├── search_claude_prompt_claudeai_20241201_130000.json
└── ...
```

Files are named: `{prefix}_{subreddit}_{timestamp}.json`

## MachineLearning Filtering

For r/MachineLearning, posts are filtered to include only those mentioning:
- prompt, prompting
- gpt, llm, language model
- claude, chatgpt
- instruction, few-shot, zero-shot

## Deduplication

The scraper tracks post IDs across all existing JSON files to avoid duplicates. This allows you to run the scraper multiple times without worrying about duplicate data.

## Error Handling

- Gracefully handles API errors
- Skips deleted/removed comments
- Continues scraping if individual posts fail
- Provides detailed progress output

## Statistics

View statistics about your scraped data:

```bash
python reddit_scraper.py --stats
```

Output includes:
- Total posts, code blocks, prompts, comments
- Average score and comment count
- Posts by subreddit breakdown

## Best Practices

1. **Start Small**: Test with a single subreddit first
2. **Use --no-comments**: For faster initial scraping
3. **Timeframe Selection**: Use 'week' or 'month' for recent content
4. **Search Queries**: Use specific terms for targeted scraping
5. **Rate Limiting**: Don't modify the delay - respect Reddit's API

## Troubleshooting

### No posts found
- Check if the subreddit name is correct (case-sensitive)
- Verify internet connection
- Try a different timeframe

### Rate limiting errors
- Increase RATE_LIMIT_DELAY in the script
- Reduce --limit value

### Missing data
- Some posts may have no body (link posts)
- Deleted content won't be scraped
- Comments may be disabled on some posts

## Integration

The scraped data can be used with other tools in the prompt-engineering-system:

```bash
# Search scraped Reddit data
python scripts/search_knowledge.py --query "few-shot" --source reddit

# Embed Reddit posts for semantic search
python scripts/embed_output.py --input data/reddit/ --output data/embeddings/
```

## API Reference

### Reddit JSON API Endpoints

- Top posts: `https://reddit.com/r/{subreddit}/top.json?t={timeframe}&limit={limit}`
- Search: `https://reddit.com/r/{subreddit}/search.json?q={query}&restrict_sr=on`
- Comments: `https://reddit.com/r/{subreddit}/comments/{post_id}.json`

No authentication required for public posts.

## License

Part of the prompt-engineering-system project.
