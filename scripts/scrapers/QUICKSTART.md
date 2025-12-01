# Reddit Scraper Quickstart Guide

Get started scraping Reddit for prompt engineering knowledge in 5 minutes.

## Quick Start

### 1. Install Dependencies

```bash
cd scripts/scrapers
pip install -r requirements.txt
```

### 2. Run Your First Scrape

**Option A: Use Presets (Easiest)**

```bash
# Windows
scrape.bat daily

# Linux/Mac
./scrape.sh daily
```

**Option B: Use Python Directly**

```bash
# Scrape one subreddit
python reddit_scraper.py --subreddit PromptEngineering --timeframe week --limit 50

# Scrape all subreddits
python reddit_scraper.py --all --timeframe week --limit 50
```

### 3. Check Results

```bash
# View statistics
python reddit_scraper.py --stats

# Check output files
ls ../../data/reddit/
```

## Available Presets

Use `scrape.bat` (Windows) or `./scrape.sh` (Linux/Mac) with these presets:

- **`daily`** - Daily update from all subreddits (25 posts each)
- **`weekly`** - Weekly update from all subreddits (50 posts each)
- **`monthly`** - Monthly update from all subreddits (100 posts each)
- **`quick`** - Fast scan without comments (10 posts each)
- **`claude`** - Search for Claude-specific content
- **`chatgpt`** - Search for ChatGPT-specific content
- **`techniques`** - Search for prompt engineering techniques

## Common Commands

### Scrape Specific Subreddits

```bash
# Single subreddit
python reddit_scraper.py --subreddit ClaudeAI --timeframe month --limit 100

# Multiple runs for different subreddits
python reddit_scraper.py --subreddit PromptEngineering --timeframe week --limit 50
python reddit_scraper.py --subreddit ChatGPT --timeframe week --limit 50
```

### Search for Specific Topics

```bash
# Search one subreddit
python reddit_scraper.py --subreddit PromptEngineering --search "few-shot" --limit 50

# Search all subreddits
python reddit_scraper.py --all --search "claude prompt" --limit 50
```

### Speed Up Scraping

```bash
# Skip comments for faster scraping
python reddit_scraper.py --all --timeframe day --limit 25 --no-comments
```

### Get Statistics

```bash
python reddit_scraper.py --stats
```

## Output Format

Data is saved to `C:/Users/JRiel/prompt-engineering-system/data/reddit/` as JSON files:

```
data/reddit/
├── top_week_promptengineering_20241201_080000.json
├── top_week_chatgpt_20241201_080030.json
├── top_week_claudeai_20241201_080100.json
└── ...
```

Each file contains an array of posts with:
- Post metadata (title, score, comments, etc.)
- Post body text
- Top comments
- Extracted code blocks
- Extracted prompt examples

## Testing

Before running a full scrape, test that everything works:

```bash
python test_scraper.py
```

This will:
- Check that dependencies are installed
- Test Reddit API connectivity
- Verify the scraper functions
- Validate a sample scrape

## Timeframe Options

- `hour` - Last hour
- `day` - Last 24 hours
- `week` - Last 7 days (recommended)
- `month` - Last 30 days
- `year` - Last year
- `all` - All time

## Targeted Subreddits

The scraper targets these subreddits by default:

1. **r/PromptEngineering** - Dedicated prompt engineering discussions
2. **r/ChatGPT** - ChatGPT prompts and techniques
3. **r/ClaudeAI** - Claude-specific content
4. **r/LocalLLaMA** - Local LLM techniques
5. **r/MachineLearning** - ML content (filtered for prompts)
6. **r/artificial** - General AI discussions

## Tips

### Quality Over Quantity

- The scraper filters posts with minimum 5 upvotes and 2 comments
- This ensures you get quality content
- Adjust thresholds in `config.json` if needed

### Regular Scraping

Set up a daily or weekly cron job:

```bash
# Add to crontab (Linux/Mac)
0 8 * * * cd /path/to/scripts/scrapers && ./scrape.sh daily

# Or Windows Task Scheduler
# Run: C:\Users\JRiel\prompt-engineering-system\scripts\scrapers\scrape.bat daily
# Schedule: Daily at 8:00 AM
```

### Rate Limiting

- The scraper waits 2 seconds between requests
- This respects Reddit's API limits
- Don't modify the delay unless you understand the consequences

### Deduplication

- The scraper tracks post IDs automatically
- Running multiple times won't create duplicates
- Safe to run as often as you want

## Troubleshooting

### "No module named 'requests'"

```bash
pip install requests
```

### "No posts found"

- Check internet connection
- Verify subreddit name is correct (case-sensitive)
- Try a different timeframe (e.g., `--timeframe month`)

### Rate limiting errors

- Increase delay in script (edit RATE_LIMIT_DELAY)
- Reduce --limit value
- Wait a few minutes and try again

### Permission errors

- Ensure data/reddit/ directory exists
- Check write permissions
- Run with appropriate privileges

## Next Steps

After scraping:

1. **Analyze the data**: Browse JSON files in `data/reddit/`
2. **Extract insights**: Look at extracted_prompts and extracted_code
3. **Search the data**: Use scripts/search_knowledge.py
4. **Embed for semantic search**: Use scripts/embed_output.py

## Advanced Usage

See README.md for:
- Custom configurations
- API details
- Integration with other tools
- Advanced filtering options

## Support

- Check README.md for detailed documentation
- Run `python reddit_scraper.py --help` for all options
- Test with `python test_scraper.py`
- View example output in `example_output.json`
