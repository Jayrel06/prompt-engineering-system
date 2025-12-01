# Prompt History and Search System

A production-ready system for storing, searching, and analyzing prompt engineering history with SQLite, FTS5 full-text search, tagging, and comprehensive analytics.

## Features

- **SQLite Database**: Robust local storage with automatic schema management
- **FTS5 Full-Text Search**: Fast, indexed searching across all prompts and outputs
- **Tagging System**: Categorize prompts with multiple tags for easy retrieval
- **Framework Tracking**: Track which prompt engineering framework was used
- **Cost Analytics**: Monitor token usage and API costs
- **Export Capabilities**: Export to JSON or CSV for backup and analysis
- **CLI Interface**: Full command-line interface for all operations
- **Integration Hooks**: Easy integration with other scripts
- **Production-Ready**: Proper indexing, error handling, and performance optimization

## Installation

No additional dependencies required beyond Python 3.8+ standard library!

```bash
# The script is ready to use immediately
python prompt_history.py --help
```

## Quick Start

### Save a Prompt

```bash
python prompt_history.py --save "Explain quantum computing" \
  --output "Quantum computing uses quantum mechanics..." \
  --model "gpt-4" \
  --tags "science,education" \
  --tokens 150 \
  --cost 0.0045
```

### Search History

```bash
# Full-text search
python prompt_history.py --search "quantum"

# Search with limit
python prompt_history.py --search "machine learning" --limit 5
```

### List Recent Entries

```bash
# Show 10 most recent
python prompt_history.py --list-recent 10

# Show recent with full output
python prompt_history.py --list-recent 5 --verbose
```

### Filter by Tag

```bash
python prompt_history.py --tag "science"
```

### Get Statistics

```bash
python prompt_history.py --stats
```

### Export History

```bash
# Export to JSON
python prompt_history.py --export history.json

# Export to CSV
python prompt_history.py --export history.csv
```

## Python API Usage

### Basic Usage

```python
from prompt_history import PromptHistory

# Initialize
history = PromptHistory()

# Save an entry
entry_id = history.save(
    prompt="What is machine learning?",
    output="Machine learning is...",
    model="gpt-4",
    tokens=100,
    cost=0.003,
    tags=["ai", "education"]
)

# Search
results = history.search("machine learning")

# Get recent
recent = history.get_recent(limit=10)

# Get by tag
tagged = history.get_by_tag("ai")

# Get statistics
stats = history.stats()
```

### Advanced Usage

```python
from prompt_history import PromptHistory, HistoryEntry

history = PromptHistory()

# Save with framework and template info
entry_id = history.save(
    prompt="Solve this step by step: 2 + 2 * 3",
    output="Step 1: Multiply 2 * 3 = 6\nStep 2: Add 2 + 6 = 8",
    framework="chain-of-thought",
    template="math-solver",
    model="gpt-4-turbo",
    tokens=85,
    cost=0.00255,
    tags=["math", "step-by-step"],
    metadata={
        "difficulty": "easy",
        "steps": 2,
        "accuracy": "correct"
    }
)

# Get entries from today
today = history.get_today()

# Get entries from this week
week = history.get_this_week()

# Export
history.export_json("backup.json")
history.export_csv("backup.csv")
```

## Integration Examples

### Auto-Tracking Wrapper

```python
from prompt_history import PromptHistory

class AIClient:
    def __init__(self):
        self.history = PromptHistory()

    def call_api(self, prompt, model="gpt-4", framework=None):
        # Make your API call
        response = your_api_call(prompt, model)

        # Automatically track
        self.history.save(
            prompt=prompt,
            output=response.text,
            model=model,
            framework=framework,
            tokens=response.usage.total_tokens,
            cost=calculate_cost(response.usage),
            tags=["auto-tracked"],
            metadata={
                "response_time": response.elapsed,
                "status": "success"
            }
        )

        return response
```

### Integration with Prompt Templates

```python
from prompt_history import PromptHistory

history = PromptHistory()

def use_template(template_name, variables):
    # Load and fill template
    prompt = load_template(template_name).format(**variables)

    # Execute
    output = call_ai(prompt)

    # Track with template info
    history.save(
        prompt=prompt,
        output=output,
        template=template_name,
        tags=["templated"],
        metadata={"variables": variables}
    )

    return output
```

### Integration with Model Orchestrator

```python
from prompt_history import PromptHistory

history = PromptHistory()

def orchestrate_prompt(prompt, requirements):
    # Select best model
    model = select_model(requirements)

    # Execute
    response = call_model(model, prompt)

    # Track with orchestration metadata
    history.save(
        prompt=prompt,
        output=response.text,
        framework="model-orchestration",
        model=model,
        tokens=response.tokens,
        cost=response.cost,
        metadata={
            "requirements": requirements,
            "selection_reason": response.selection_reason,
            "alternatives": response.alternatives_considered
        }
    )

    return response
```

## Database Schema

### Main Table: `history`

| Column | Type | Description |
|--------|------|-------------|
| id | INTEGER PRIMARY KEY | Auto-incrementing ID |
| prompt | TEXT | The prompt text |
| output | TEXT | The output/response |
| timestamp | TIMESTAMP | When the entry was created |
| framework_used | TEXT | Framework (e.g., 'chain-of-thought') |
| template_used | TEXT | Template name (if applicable) |
| model | TEXT | Model name (e.g., 'gpt-4') |
| tokens | INTEGER | Token count |
| cost | REAL | Cost in dollars |
| tags | TEXT | Comma-separated tags |
| metadata | TEXT | JSON-encoded metadata |

### Indexes

- `idx_timestamp`: Fast sorting by date
- `idx_framework`: Fast filtering by framework
- `idx_model`: Fast filtering by model
- `idx_tags`: Fast tag lookups

### FTS5 Table: `history_fts`

Full-text search virtual table with automatic sync triggers.

## CLI Reference

### Saving Entries

```bash
--save TEXT          # Prompt text to save
--output TEXT        # Output/response text
--framework TEXT     # Framework used
--template TEXT      # Template name
--model TEXT         # Model name
--tokens INT         # Token count
--cost FLOAT         # Cost in dollars
--tags TEXT          # Comma-separated tags
--metadata JSON      # JSON metadata
```

### Querying

```bash
--search QUERY       # Full-text search
--tag TAG            # Filter by tag
--framework FW       # Filter by framework
--list-recent N      # Show N recent entries
--today              # Show today's entries
--week               # Show this week's entries
```

### Export

```bash
--export FILE        # Export to JSON or CSV
```

### Statistics

```bash
--stats              # Show comprehensive statistics
```

### Display Options

```bash
-v, --verbose        # Show full output
--limit N            # Limit results
--db PATH            # Custom database path
```

## FTS5 Search Syntax

The full-text search supports advanced FTS5 syntax:

```bash
# Basic search
python prompt_history.py --search "machine learning"

# Phrase search
python prompt_history.py --search '"neural networks"'

# AND operator
python prompt_history.py --search "python AND programming"

# OR operator
python prompt_history.py --search "python OR javascript"

# NOT operator
python prompt_history.py --search "programming NOT python"

# Column-specific search
python prompt_history.py --search "prompt:tutorial"

# Prefix search
python prompt_history.py --search "mach*"
```

## Statistics Output

The `--stats` flag provides:

- **Total Entries**: Count of all stored prompts
- **Total Tokens**: Sum of all token usage
- **Total Cost**: Sum of all API costs
- **Date Range**: Earliest and latest entries
- **Top Frameworks**: Most used frameworks with counts
- **Top Models**: Most used models with counts
- **Top Tags**: Most common tags with usage counts
- **Recent Activity**: Entries per day for last 7 days

## Performance

- **Indexed Queries**: All common queries use indexes for fast performance
- **FTS5 Search**: Optimized full-text search with ranking
- **Batch Operations**: Efficient handling of large result sets
- **Connection Pooling**: Proper connection management with context managers

## Data Location

Default database location:
```
C:/Users/JRiel/prompt-engineering-system/data/prompt_history.db
```

Custom location:
```bash
python prompt_history.py --db /path/to/custom.db
```

## Export Formats

### JSON Export

```json
[
  {
    "id": 1,
    "prompt": "Explain quantum computing",
    "output": "Quantum computing uses...",
    "timestamp": "2024-12-01T14:30:00",
    "framework_used": "zero-shot",
    "template_used": null,
    "model": "gpt-4",
    "tokens": 150,
    "cost": 0.0045,
    "tags": "science,education",
    "metadata": "{\"difficulty\": \"medium\"}"
  }
]
```

### CSV Export

Includes all fields in CSV format with proper escaping.

## Best Practices

1. **Always Tag**: Use descriptive tags for easier retrieval
2. **Track Costs**: Include token counts and costs for analytics
3. **Use Frameworks**: Specify which framework you're using
4. **Add Metadata**: Store additional context in metadata
5. **Regular Exports**: Backup your history regularly
6. **Search Smart**: Use FTS5 syntax for precise searches
7. **Monitor Stats**: Check statistics to optimize prompt usage

## Integration Patterns

### Pattern 1: Decorator

```python
def track_prompt(framework=None, tags=None):
    def decorator(func):
        def wrapper(prompt, *args, **kwargs):
            output = func(prompt, *args, **kwargs)
            history.save(
                prompt=prompt,
                output=output,
                framework=framework,
                tags=tags or []
            )
            return output
        return wrapper
    return decorator

@track_prompt(framework="chain-of-thought", tags=["math"])
def solve_math_problem(prompt):
    return call_ai(prompt)
```

### Pattern 2: Context Manager

```python
from contextlib import contextmanager

@contextmanager
def tracked_prompt(prompt, **kwargs):
    start_time = time.time()
    try:
        yield
        output = kwargs.get('output')
        if output:
            kwargs['metadata'] = kwargs.get('metadata', {})
            kwargs['metadata']['duration'] = time.time() - start_time
            history.save(prompt=prompt, output=output, **kwargs)
    except Exception as e:
        history.save(
            prompt=prompt,
            output=f"ERROR: {str(e)}",
            tags=["error"],
            **kwargs
        )
        raise
```

### Pattern 3: Callback

```python
class PromptCallback:
    def __init__(self):
        self.history = PromptHistory()

    def on_completion(self, prompt, output, **kwargs):
        self.history.save(prompt=prompt, output=output, **kwargs)

callback = PromptCallback()
ai_client.register_callback('completion', callback.on_completion)
```

## Troubleshooting

### Database Locked

If you get "database is locked" errors:
- Close any other connections to the database
- Use the context manager properly (it's automatic in PromptHistory)
- Check for long-running transactions

### Search Not Finding Results

- Verify FTS5 table is properly synced
- Check search syntax (use quotes for phrases)
- Try simpler queries to narrow down the issue

### Performance Issues

- Ensure indexes are created (automatic on init)
- Use `--limit` to restrict result sets
- Consider archiving old entries

## Advanced Features

### Custom Database Path

```python
from pathlib import Path
from prompt_history import PromptHistory

custom_db = Path("/path/to/project/prompts.db")
history = PromptHistory(db_path=custom_db)
```

### Metadata Queries

```python
# Store structured metadata
history.save(
    prompt=prompt,
    output=output,
    metadata={
        "version": "1.0",
        "experiment": "A/B test",
        "variant": "A"
    }
)

# Query and filter
entries = history.get_recent(100)
variant_a = [e for e in entries if e.metadata.get("variant") == "A"]
```

### Batch Analysis

```python
# Analyze all entries
all_entries = history.get_recent(limit=10000)

# Calculate metrics
total_tokens = sum(e.tokens for e in all_entries if e.tokens)
avg_cost = sum(e.cost for e in all_entries if e.cost) / len(all_entries)

# Group by framework
from collections import defaultdict
by_framework = defaultdict(list)
for entry in all_entries:
    by_framework[entry.framework_used].append(entry)
```

## Future Enhancements

Potential additions (not yet implemented):
- Version control for prompts
- A/B test result tracking
- Performance benchmarking
- Automatic quality scoring
- Prompt template extraction
- Duplicate detection
- Advanced analytics dashboard

## Contributing

When extending this system:
1. Maintain backward compatibility with database schema
2. Add indexes for new query patterns
3. Update FTS triggers if changing searchable fields
4. Document new features in this README

## License

Part of the Prompt Engineering System.

## Related Scripts

- `prompt_optimizer.py`: Optimize prompts (can integrate with history)
- `model_orchestrator.py`: Select models (can auto-track with history)
- `feedback_system.py`: Evaluate outputs (can reference history)
- `cache_manager.py`: Cache responses (complementary to history)

## Support

For issues or questions:
1. Check this README
2. Review examples in `prompt_history_examples.py`
3. Examine the database schema
4. Test with `--verbose` flag for detailed output
