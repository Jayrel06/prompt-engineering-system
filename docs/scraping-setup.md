# Scraping Setup Guide

This guide explains how to configure and use the automated scraping system for collecting prompt engineering knowledge from Reddit and GitHub.

## Table of Contents

- [Overview](#overview)
- [Prerequisites](#prerequisites)
- [Configuration](#configuration)
- [n8n Workflow Setup](#n8n-workflow-setup)
- [Running Manual Scrapes](#running-manual-scrapes)
- [Checking Scraping Status](#checking-scraping-status)
- [Recommended Schedule](#recommended-schedule)
- [Troubleshooting](#troubleshooting)

## Overview

The scraping system consists of:

1. **Python Scrapers**: Located in `scripts/scrapers/`
   - `reddit_scraper.py` - Scrapes Reddit posts and comments
   - `github_scraper.py` - Scrapes GitHub repositories and prompts

2. **n8n Workflows**: Located in `workflows/scrapers/`
   - `scheduled-reddit-scrape.json` - Runs Reddit scraper weekly
   - `scheduled-github-scrape.json` - Runs GitHub scraper weekly
   - `on-demand-scrape.json` - Webhook-triggered on-demand scraping

3. **Data Storage**: Scraped data is saved to `data/`
   - `data/reddit/` - Reddit posts and comments
   - `data/github/` - GitHub repositories and prompts

## Prerequisites

### Python Environment

Ensure you have Python 3.8+ installed with the following packages:

```bash
pip install requests
```

### GitHub Token (Optional but Recommended)

For higher API rate limits (5000 req/hour instead of 60), set up a GitHub Personal Access Token:

1. Go to GitHub Settings > Developer settings > Personal access tokens > Tokens (classic)
2. Generate new token with `public_repo` scope
3. Add to your `.env` file:

```bash
GITHUB_TOKEN=ghp_your_token_here
```

### Notification Webhooks (Optional)

For completion notifications, configure either Slack or Discord webhooks:

**For Slack:**
1. Create a Slack app and enable Incoming Webhooks
2. Add webhook URL to `.env`:

```bash
SLACK_WEBHOOK_URL=https://hooks.slack.com/services/YOUR/WEBHOOK/URL
```

**For Discord:**
1. Create a Discord webhook in your server settings
2. Add webhook URL to `.env`:

```bash
DISCORD_WEBHOOK_URL=https://discord.com/api/webhooks/YOUR/WEBHOOK/URL
```

### n8n Installation

If you don't have n8n installed:

```bash
# Using Docker (recommended)
docker run -it --rm \
  --name n8n \
  -p 5678:5678 \
  -v ~/.n8n:/home/node/.n8n \
  n8nio/n8n

# Or using npm
npm install -g n8n
n8n
```

Access n8n at `http://localhost:5678`

## Configuration

### Environment Variables

Create or update your `.env` file in the project root:

```bash
# GitHub Token (optional, but recommended)
GITHUB_TOKEN=ghp_your_token_here

# Notification Webhooks (optional)
SLACK_WEBHOOK_URL=https://hooks.slack.com/services/YOUR/WEBHOOK/URL
# OR
DISCORD_WEBHOOK_URL=https://discord.com/api/webhooks/YOUR/WEBHOOK/URL

# n8n Configuration (if using)
N8N_HOST=http://localhost:5678
```

### Scraper Configuration

You can customize scraper behavior by editing the Python scripts:

**Reddit Scraper** (`scripts/scrapers/reddit_scraper.py`):
- `SUBREDDITS`: List of subreddits to scrape (lines 26-33)
- `MIN_SCORE`: Minimum post score threshold (line 44)
- `MIN_COMMENTS`: Minimum comments threshold (line 45)
- `MAX_TOP_COMMENTS`: Number of comments to fetch (line 46)
- `RATE_LIMIT_DELAY`: Delay between requests in seconds (line 49)

**GitHub Scraper** (`scripts/scrapers/github_scraper.py`):
- `AWESOME_LISTS`: Curated awesome lists to scrape (lines 42-47)
- `DEFAULT_TOPICS`: GitHub topics to search (lines 50-56)
- `RATE_LIMIT_DELAY`: Delay between requests (line 38)

## n8n Workflow Setup

### 1. Import Workflows

1. Open n8n web interface (`http://localhost:5678`)
2. Click **Workflows** > **Import from File**
3. Import each workflow JSON file from `workflows/scrapers/`:
   - `scheduled-reddit-scrape.json`
   - `scheduled-github-scrape.json`
   - `on-demand-scrape.json`

### 2. Configure Environment Variables in n8n

Add environment variables to n8n (if not already set):

**Method 1: Docker Environment Variables**
```bash
docker run -it --rm \
  --name n8n \
  -p 5678:5678 \
  -e GITHUB_TOKEN=ghp_your_token \
  -e SLACK_WEBHOOK_URL=https://hooks.slack.com/... \
  -v ~/.n8n:/home/node/.n8n \
  n8nio/n8n
```

**Method 2: n8n Environment File**
Create `~/.n8n/.env`:
```bash
GITHUB_TOKEN=ghp_your_token
SLACK_WEBHOOK_URL=https://hooks.slack.com/...
```

### 3. Adjust File Paths (if needed)

If your project is not located at `C:/Users/JRiel/prompt-engineering-system/`, update the paths in each workflow:

1. Open the workflow in n8n
2. Edit the "Execute Command" nodes
3. Update the path in the command field:
   ```bash
   cd "YOUR_PROJECT_PATH/scripts/scrapers" && python reddit_scraper.py ...
   ```

### 4. Configure Scheduled Workflows

**Reddit Scraper** (Every Sunday at 2 AM):
1. Open `Scheduled Reddit Scraper` workflow
2. Click on "Every Sunday at 2 AM" node
3. Adjust cron expression if needed: `0 2 * * 0`
4. Click **Save** and **Activate** the workflow

**GitHub Scraper** (Every Monday at 3 AM):
1. Open `Scheduled GitHub Scraper` workflow
2. Click on "Every Monday at 3 AM" node
3. Adjust cron expression if needed: `0 3 * * 1`
4. Click **Save** and **Activate** the workflow

### 5. Get Webhook URL for On-Demand Scraping

1. Open `On-Demand Scraper` workflow
2. Click on "Webhook Trigger" node
3. Copy the **Production URL** (e.g., `http://localhost:5678/webhook/scrape`)
4. Save this URL for triggering manual scrapes
5. Click **Save** and **Activate** the workflow

## Running Manual Scrapes

### Using Command Line

**Reddit Scraper:**

```bash
# Navigate to scrapers directory
cd C:/Users/JRiel/prompt-engineering-system/scripts/scrapers

# Scrape all configured subreddits (past week, 50 posts each)
python reddit_scraper.py --all --timeframe week --limit 50

# Scrape specific subreddit
python reddit_scraper.py --subreddit PromptEngineering --timeframe month --limit 100

# Search across all subreddits
python reddit_scraper.py --search "claude prompt" --all --limit 30

# Get statistics about scraped data
python reddit_scraper.py --stats
```

**GitHub Scraper:**

```bash
# Navigate to scrapers directory
cd C:/Users/JRiel/prompt-engineering-system/scripts/scrapers

# Scrape awesome lists
python github_scraper.py --awesome

# Search by topic with minimum stars
python github_scraper.py --topic prompt-engineering --min-stars 100 --limit 50

# Scrape specific repository
python github_scraper.py --repo "f/awesome-chatgpt-prompts"

# Custom search
python github_scraper.py --search "system prompt claude" --limit 30
```

### Using n8n Webhook

Trigger on-demand scraping via HTTP POST request:

```bash
# Scrape both sources
curl -X POST http://localhost:5678/webhook/scrape \
  -H "Content-Type: application/json" \
  -d '{
    "source": "both",
    "timeframe": "week",
    "limit": 50
  }'

# Scrape only Reddit
curl -X POST http://localhost:5678/webhook/scrape \
  -H "Content-Type: application/json" \
  -d '{
    "source": "reddit",
    "timeframe": "month",
    "limit": 100
  }'

# Scrape only GitHub
curl -X POST http://localhost:5678/webhook/scrape \
  -H "Content-Type: application/json" \
  -d '{
    "source": "github",
    "topic": "llm-prompts",
    "min_stars": 50,
    "limit": 30
  }'
```

**Webhook Parameters:**

- `source`: `"reddit"`, `"github"`, or `"both"` (default: `"both"`)
- `timeframe`: `"hour"`, `"day"`, `"week"`, `"month"`, `"year"`, `"all"` (default: `"week"`)
- `limit`: Number of items to fetch (default: `50`)
- `min_stars`: Minimum GitHub stars (default: `50`)
- `topic`: GitHub topic to search (default: `"prompt-engineering"`)

**Example Response:**

```json
{
  "status": "completed",
  "timestamp": "2025-12-01T12:00:00.000Z",
  "reddit": {
    "status": "success",
    "posts": "42",
    "error": ""
  },
  "github": {
    "status": "success",
    "repos": "15",
    "prompts": "127",
    "error": ""
  },
  "message": "Scraping completed. Data saved to disk and ready for ingestion."
}
```

### Quick Scrape Script

For a quick test scrape:

```bash
cd C:/Users/JRiel/prompt-engineering-system/scripts/scrapers
python quick_scrape.py
```

This runs a quick scrape of top posts from major subreddits.

## Checking Scraping Status

### View Scraped Data

**Reddit Data:**
```bash
# List all Reddit scrapes
ls -lh C:/Users/JRiel/prompt-engineering-system/data/reddit/

# View latest Reddit scrape
cat C:/Users/JRiel/prompt-engineering-system/data/reddit/reddit_*_latest.json | jq
```

**GitHub Data:**
```bash
# List all GitHub scrapes
ls -lh C:/Users/JRiel/prompt-engineering-system/data/github/

# View latest GitHub scrape
cat C:/Users/JRiel/prompt-engineering-system/data/github/github_scrape_*.json | jq
```

### Get Statistics

**Reddit Statistics:**
```bash
cd C:/Users/JRiel/prompt-engineering-system/scripts/scrapers
python reddit_scraper.py --stats
```

Output example:
```
=== Reddit Scraper Statistics ===
Total posts: 342
Total code blocks: 156
Total prompts: 89
Total comments: 1,234
Average score: 45.2
Average comments: 12.3

Posts by subreddit:
  r/PromptEngineering: 125
  r/ChatGPT: 98
  r/ClaudeAI: 67
  r/LocalLLaMA: 52
```

### Monitor n8n Executions

1. Open n8n web interface
2. Click **Executions** in the sidebar
3. View execution history, logs, and errors
4. Filter by workflow to see specific scraper runs

### Check Logs

**n8n Docker Logs:**
```bash
docker logs n8n -f
```

**Python Scraper Output:**
Scrapers print progress to stdout during execution. When run via n8n, this output is captured and can be viewed in the execution details.

## Recommended Schedule

### Default Schedule

The default configuration runs scrapers at off-peak hours to minimize API rate limiting:

| Scraper | Schedule | Cron Expression | Rationale |
|---------|----------|----------------|-----------|
| Reddit | Every Sunday at 2 AM | `0 2 * * 0` | Weekly digest of top weekly posts |
| GitHub | Every Monday at 3 AM | `0 3 * * 1` | Weekly check for new repos and prompts |

### Customizing the Schedule

**For more frequent scraping:**

- **Daily Reddit scraping**: `0 2 * * *` (every day at 2 AM)
- **Bi-weekly GitHub scraping**: `0 3 * * 1,4` (Monday and Thursday at 3 AM)

**For less frequent scraping:**

- **Bi-weekly Reddit**: `0 2 * * 0,3` (Sunday and Wednesday at 2 AM)
- **Monthly GitHub**: `0 3 1 * *` (1st of each month at 3 AM)

**To change the schedule:**

1. Open the workflow in n8n
2. Click on the Schedule Trigger node
3. Modify the cron expression
4. Save and re-activate the workflow

### Best Practices

1. **Rate Limiting**: Don't scrape too frequently to avoid API rate limits
   - Reddit: 60 requests per minute (no auth), use 2-second delays
   - GitHub: 60 requests per hour (no auth), 5000/hour (with token)

2. **Data Freshness**: Weekly scraping is usually sufficient for prompt engineering content

3. **Storage Management**: Periodically clean old scrapes to save disk space
   ```bash
   # Keep only last 30 days of data
   find data/reddit/ -name "*.json" -mtime +30 -delete
   find data/github/ -name "*.json" -mtime +30 -delete
   ```

4. **Off-Peak Hours**: Run scrapers during low-traffic hours (2-4 AM) to minimize impact

## Troubleshooting

### Common Issues

**1. Rate Limit Exceeded**

**Symptoms:**
- Error: "Rate limit exceeded"
- HTTP 403 responses

**Solutions:**
- For GitHub: Add `GITHUB_TOKEN` to `.env` for 5000 req/hour limit
- Increase delay between requests in scraper configuration
- Wait for rate limit reset (check `X-RateLimit-Reset` header)
- Reduce `--limit` parameter

**2. No Data Scraped**

**Symptoms:**
- Scraper completes but no JSON files created
- "No posts found" messages

**Solutions:**
- Check quality thresholds (`MIN_SCORE`, `MIN_COMMENTS`)
- Verify subreddit names are correct (case-sensitive)
- Try different timeframe (`--timeframe month` instead of `week`)
- Check network connectivity

**3. Workflow Not Triggering**

**Symptoms:**
- Scheduled workflow doesn't run at expected time
- No executions in n8n

**Solutions:**
- Verify workflow is **Activated** (toggle in top-right)
- Check cron expression is valid (use [crontab.guru](https://crontab.guru))
- Ensure n8n process is running
- Check n8n timezone settings match your expectations

**4. Command Execution Fails**

**Symptoms:**
- "Command not found" errors
- "Python not found" errors

**Solutions:**
- Verify Python is installed and in PATH
- Use full path to Python executable:
  ```bash
  /usr/bin/python3 reddit_scraper.py ...
  ```
- Check file paths are correct (use absolute paths)
- Verify working directory is correct

**5. Notifications Not Sending**

**Symptoms:**
- Scraper completes but no Slack/Discord notification

**Solutions:**
- Verify webhook URL is set in environment variables
- Test webhook manually:
  ```bash
  curl -X POST $SLACK_WEBHOOK_URL \
    -H "Content-Type: application/json" \
    -d '{"text": "Test message"}'
  ```
- Check n8n HTTP Request node configuration
- Review n8n execution logs for errors

**6. Encoding Issues**

**Symptoms:**
- Unicode errors when reading/writing JSON
- Corrupted text in scraped content

**Solutions:**
- Ensure UTF-8 encoding is used (already configured in scrapers)
- Check terminal/console encoding settings
- Verify JSON files with: `python -m json.tool file.json`

### Debug Mode

Enable verbose logging for debugging:

**Reddit Scraper:**
```bash
python reddit_scraper.py --all --limit 10 2>&1 | tee scraper.log
```

**GitHub Scraper:**
```bash
python github_scraper.py --awesome 2>&1 | tee scraper.log
```

**n8n Debug Mode:**
```bash
# Set log level to debug
export N8N_LOG_LEVEL=debug
n8n
```

### Getting Help

If you encounter issues:

1. Check scraper output logs
2. Review n8n execution details
3. Verify environment variables are set correctly
4. Test scrapers manually from command line
5. Check API rate limits and quotas

## Data Flow

```
┌─────────────────────────────────────────────────────────────────┐
│                         Scraping Pipeline                         │
└─────────────────────────────────────────────────────────────────┘

1. Trigger (Scheduled or Webhook)
   │
   ├─→ [Execute Reddit Scraper]
   │   └─→ Fetch posts from subreddits
   │       └─→ Extract prompts and code blocks
   │           └─→ Save to data/reddit/*.json
   │
   └─→ [Execute GitHub Scraper]
       └─→ Search repositories by topic
           └─→ Fetch READMEs and prompt files
               └─→ Extract prompts
                   └─→ Save to data/github/*.json

2. Parse Results
   └─→ Extract statistics from stdout

3. Trigger Ingestion Pipeline
   └─→ embed_output.py processes JSON files
       └─→ Generates embeddings
           └─→ Stores in vector database

4. Send Notification
   └─→ Slack/Discord webhook
       └─→ Report statistics and status
```

## Next Steps

After setting up scraping:

1. **Configure Ingestion**: Set up `embed_output.py` to process scraped data
2. **Vector Database**: Configure Qdrant for storing embeddings
3. **Search System**: Use `search_knowledge.py` to query scraped prompts
4. **Monitoring**: Set up dashboards to track scraping metrics

## Additional Resources

- [Reddit API Documentation](https://www.reddit.com/dev/api/)
- [GitHub API Documentation](https://docs.github.com/en/rest)
- [n8n Documentation](https://docs.n8n.io/)
- [Cron Expression Generator](https://crontab.guru/)

## Maintenance

### Regular Tasks

**Weekly:**
- Check scraper execution logs
- Verify notifications are being sent
- Monitor disk space usage

**Monthly:**
- Review and update scraper configurations
- Clean old data files
- Update GitHub token if needed
- Review rate limit usage

**Quarterly:**
- Update Python dependencies
- Review and add new subreddits/topics
- Optimize scraper performance
- Update awesome lists

---

**Last Updated**: 2025-12-01
**Version**: 1.0
