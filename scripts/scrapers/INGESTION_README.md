# Vector Database Ingestion Pipeline

This directory contains scripts to scrape Reddit and GitHub data and ingest it into the Qdrant vector database for the prompt engineering system.

## Scripts

### 1. `ingest_to_vector.py`
Processes scraped JSON files and stores them in Qdrant with embeddings.

**Features:**
- Reads scraped data from `data/reddit/*.json` and `data/github/*.json`
- Chunks long content (max 1000 tokens per chunk)
- Creates rich metadata (source, URL, score, date, tags)
- Deduplicates based on content hash
- Extracts keywords automatically
- Progress tracking with detailed statistics

**Usage:**
```bash
# Ingest all Reddit data
python ingest_to_vector.py --source reddit

# Ingest all GitHub data
python ingest_to_vector.py --source github

# Ingest everything
python ingest_to_vector.py --all

# Ingest a specific file
python ingest_to_vector.py --file data/reddit/specific.json

# Dry run to see what would be ingested
python ingest_to_vector.py --source reddit --dry-run
```

### 2. `scrape_and_ingest.py`
Runs the full pipeline: scrape → ingest

**Features:**
- Orchestrates scraping from Reddit and/or GitHub
- Automatically ingests scraped data into Qdrant
- Configurable options for both sources
- Comprehensive error handling
- Summary reporting

**Usage:**
```bash
# Scrape and ingest Reddit data from the past week
python scrape_and_ingest.py --reddit --timeframe week

# Scrape and ingest GitHub repos with 100+ stars
python scrape_and_ingest.py --github --min-stars 100

# Scrape both Reddit and GitHub, then ingest
python scrape_and_ingest.py --reddit --github --timeframe month

# Scrape everything quickly
python scrape_and_ingest.py --all --timeframe day --reddit-limit 25

# Scrape specific subreddit and GitHub topic
python scrape_and_ingest.py --reddit --subreddit PromptEngineering --github --topic llm-prompts

# Scrape only (skip ingestion)
python scrape_and_ingest.py --reddit --github --skip-ingestion

# Dry run to see what would happen
python scrape_and_ingest.py --all --dry-run
```

## How It Works

### Ingestion Process

1. **Reading Data**
   - Scans `data/reddit/` and `data/github/` directories
   - Loads JSON files containing scraped content

2. **Processing Content**

   **Reddit Posts:**
   - Combines title and body
   - Extracts code blocks and prompts
   - Processes top comments
   - Filters by score (minimum: 3)

   **GitHub Repos:**
   - Processes README content
   - Extracts prompts from markdown
   - Includes prompt files
   - Uses repository topics as tags

3. **Chunking**
   - Splits long content into ~1000 token chunks
   - Smart sentence boundary detection
   - 200 character overlap between chunks
   - Preserves context across chunks

4. **Metadata Creation**

   **Reddit metadata:**
   - Source file path
   - Post ID and URL
   - Score and author
   - Creation date
   - Subreddit name
   - Chunk information

   **GitHub metadata:**
   - Repository name and URL
   - Stars count
   - Topics/tags
   - Programming language
   - File paths
   - Chunk information

5. **Keyword Extraction**
   - Automatic keyword extraction from content
   - Filters common stop words
   - Frequency-based ranking
   - Used as searchable tags

6. **Embedding & Storage**
   - Uses `sentence-transformers` model (all-MiniLM-L6-v2)
   - Stores in Qdrant collection: `prompt_context`
   - Category: "reddit" or "github"
   - Content hash-based deduplication

7. **Progress Tracking**
   - Real-time progress indicators
   - Error logging without stopping
   - Comprehensive summary report

## Data Flow

```
Reddit Scraper          GitHub Scraper
      ↓                       ↓
data/reddit/*.json      data/github/*.json
      ↓                       ↓
      └───────────┬───────────┘
                  ↓
        ingest_to_vector.py
                  ↓
          ┌───────┴───────┐
          ↓               ↓
      Chunking      Metadata Creation
          ↓               ↓
          └───────┬───────┘
                  ↓
           Embedding
                  ↓
      Qdrant Vector Database
     (prompt_context collection)
```

## Configuration

### Chunking Parameters
- `MAX_TOKENS = 1000` - Maximum tokens per chunk (~750 words)
- `MAX_CHARS = 4000` - Approximate character limit per chunk
- `OVERLAP_CHARS = 200` - Overlap between chunks for context

### Quality Thresholds
- `MIN_CONTENT_LENGTH = 50` - Skip very short content
- `MIN_REDDIT_SCORE = 3` - Skip low-quality Reddit posts

## Output Example

```
======================================================================
VECTOR DATABASE INGESTION
======================================================================
Data directory: C:/Users/JRiel/prompt-engineering-system/data
Qdrant: localhost:6333
Dry run: False
======================================================================

Processing: reddit_promptengineering_20231201.json
  Processed 50 items, stored 150 chunks...
  Stored 150 chunks from this file

Processing: github_scrape_20231201.json
  Processed 30 items, stored 420 chunks...
  Stored 420 chunks from this file

======================================================================
INGESTION SUMMARY
======================================================================
Total items processed:      80
Total chunks stored:        570
Duplicates skipped:         15
Errors encountered:         0

Reddit posts ingested:      50
Reddit comments ingested:   75
GitHub repos ingested:      30
GitHub prompts extracted:   145
======================================================================

>>> Collection Status:
Collection: prompt_context
Total points: 570
Total vectors: 570

Ingestion completed successfully!
```

## Requirements

The scripts use the existing `EmbeddingService` from `embed_output.py`, which requires:

- `qdrant-client` - Qdrant vector database client
- `sentence-transformers` - Text embedding models
- Qdrant running on `localhost:6333`

## Categories & Tags

### Categories
- `reddit` - Content from Reddit
- `github` - Content from GitHub repositories

### Common Tags
- Subreddit names (e.g., `PromptEngineering`, `ChatGPT`)
- GitHub topics (e.g., `prompt-engineering`, `llm-prompts`)
- Content types: `prompts`, `code`, `llm`, `extracted-prompt`, `comment`
- Programming languages (e.g., `python`, `javascript`)
- Auto-extracted keywords from content

## Deduplication

Content is deduplicated using SHA-256 hashing:
- Computes hash of content text
- Skips if hash already seen in current session
- Prevents duplicate embeddings
- Works across different source files

## Error Handling

- Continues processing even if individual items fail
- Logs all errors with context
- Reports summary at the end
- Provides detailed error information for debugging

## Best Practices

1. **Start Small**: Test with `--dry-run` first
2. **Monitor Progress**: Watch for errors in real-time
3. **Check Quality**: Review the summary statistics
4. **Verify Storage**: Check Qdrant collection after ingestion
5. **Avoid Duplicates**: Don't re-run on the same data without cleaning

## Integration with Search

Once ingested, the data can be searched using:

```bash
# Search the knowledge base
python scripts/search_knowledge.py "how to write better prompts"
```

The search will find relevant chunks across all ingested Reddit posts, comments, and GitHub repositories.

## Troubleshooting

### "No JSON files found"
- Ensure you've run the scrapers first
- Check the data directory paths
- Verify files are in `data/reddit/` or `data/github/`

### "Failed to initialize embedding service"
- Ensure Qdrant is running: `docker run -p 6333:6333 qdrant/qdrant`
- Check connection: `localhost:6333`
- Verify dependencies are installed

### "Rate limit exceeded"
- For GitHub: Use a personal access token
- For Reddit: Increase delay between requests
- Wait for rate limits to reset

### Memory Issues
- Process smaller batches
- Use `--source` to ingest one source at a time
- Reduce chunk size if needed
