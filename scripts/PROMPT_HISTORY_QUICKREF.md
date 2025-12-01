# Prompt History Quick Reference

## CLI Commands

### Save Entry
```bash
# Basic save
python prompt_history.py --save "Your prompt" --output "Response"

# Full save with all options
python prompt_history.py \
  --save "Explain quantum computing" \
  --output "Quantum computing uses..." \
  --framework "chain-of-thought" \
  --template "education" \
  --model "gpt-4" \
  --tokens 150 \
  --cost 0.0045 \
  --tags "science,education,physics"
```

### Search
```bash
# Basic search
python prompt_history.py --search "quantum"

# Limit results
python prompt_history.py --search "machine learning" --limit 10

# Verbose output
python prompt_history.py --search "python" -v
```

### List Recent
```bash
# Show 10 most recent
python prompt_history.py --list-recent 10

# Show 5 with full output
python prompt_history.py --list-recent 5 --verbose
```

### Filter
```bash
# By tag
python prompt_history.py --tag "science"

# By framework
python prompt_history.py --framework "chain-of-thought"

# Today's entries
python prompt_history.py --today

# This week's entries
python prompt_history.py --week
```

### Export
```bash
# Export to JSON
python prompt_history.py --export history.json

# Export to CSV
python prompt_history.py --export history.csv
```

### Statistics
```bash
python prompt_history.py --stats
```

## Python API

### Import
```python
from prompt_history import PromptHistory
```

### Initialize
```python
# Default database location
history = PromptHistory()

# Custom database
from pathlib import Path
history = PromptHistory(db_path=Path("/path/to/db.sqlite"))
```

### Save
```python
# Basic save
entry_id = history.save(
    prompt="Your prompt",
    output="Response"
)

# Full save
entry_id = history.save(
    prompt="Your prompt",
    output="Response",
    framework="chain-of-thought",
    template="template-name",
    model="gpt-4",
    tokens=150,
    cost=0.0045,
    tags=["tag1", "tag2"],
    metadata={"key": "value"}
)
```

### Search
```python
# Full-text search
results = history.search("keyword")

# With limit
results = history.search("keyword", limit=20)
```

### Get Entries
```python
# Recent entries
recent = history.get_recent(limit=10)

# By tag
tagged = history.get_by_tag("science")

# Today
today = history.get_today()

# This week
week = history.get_this_week()
```

### Export
```python
# JSON
history.export_json("output.json")

# CSV
history.export_csv("output.csv")
```

### Statistics
```python
stats = history.stats()
print(f"Total entries: {stats['total_entries']}")
print(f"Total tokens: {stats['total_tokens']}")
print(f"Total cost: ${stats['total_cost']:.2f}")
```

## Integration Patterns

### Pattern 1: Auto-tracking Function
```python
def track_ai_call(prompt, model="gpt-4"):
    response = call_ai(prompt, model)
    history.save(
        prompt=prompt,
        output=response.text,
        model=model,
        tokens=response.tokens,
        cost=response.cost
    )
    return response
```

### Pattern 2: Context Manager
```python
from contextlib import contextmanager

@contextmanager
def tracked_execution(prompt):
    try:
        yield
    finally:
        # Save after execution
        pass
```

### Pattern 3: Decorator
```python
def track_prompt(framework=None):
    def decorator(func):
        def wrapper(prompt, *args, **kwargs):
            result = func(prompt, *args, **kwargs)
            history.save(prompt=prompt, output=result, framework=framework)
            return result
        return wrapper
    return decorator
```

## FTS5 Search Syntax

```bash
# Exact phrase
--search '"machine learning"'

# AND
--search "python AND programming"

# OR
--search "python OR javascript"

# NOT
--search "programming NOT python"

# Prefix
--search "mach*"

# Column-specific
--search "prompt:tutorial"
```

## Common Workflows

### Workflow 1: Daily Review
```bash
# See what you worked on today
python prompt_history.py --today -v
```

### Workflow 2: Weekly Summary
```bash
# Get stats for the week
python prompt_history.py --week
python prompt_history.py --stats
```

### Workflow 3: Find Similar Prompts
```bash
# Search for related prompts
python prompt_history.py --search "your topic" --limit 10
```

### Workflow 4: Export Backup
```bash
# Regular backups
python prompt_history.py --export backup_$(date +%Y%m%d).json
```

### Workflow 5: Analyze Framework Usage
```bash
# Check framework effectiveness
python prompt_history.py --framework "chain-of-thought"
python prompt_history.py --stats
```

## HistoryEntry Fields

| Field | Type | Description |
|-------|------|-------------|
| id | int | Auto-incrementing ID |
| prompt | str | The prompt text |
| output | str | The response |
| timestamp | datetime | When created |
| framework_used | str | Framework name |
| template_used | str | Template name |
| model | str | Model identifier |
| tokens | int | Token count |
| cost | float | Cost in dollars |
| tags | list | List of tags |
| metadata | dict | JSON metadata |

## Database Location

Default: `C:/Users/JRiel/prompt-engineering-system/data/prompt_history.db`

## Tips

1. **Tag Everything**: Makes searching easier
2. **Track Costs**: Monitor spending
3. **Use Frameworks**: Categorize approaches
4. **Add Metadata**: Store context
5. **Regular Exports**: Backup frequently
6. **Search Smart**: Use FTS5 syntax
7. **Review Stats**: Optimize usage

## Examples

### Example 1: Chain-of-Thought
```python
history.save(
    prompt="Solve step by step: 2x + 5 = 15",
    output="Step 1: Subtract 5...",
    framework="chain-of-thought",
    tags=["math", "algebra"]
)
```

### Example 2: Few-Shot
```python
history.save(
    prompt="Example 1: ...\nExample 2: ...\nNow: ...",
    output="Classification: positive",
    framework="few-shot",
    template="sentiment-3shot",
    tags=["classification", "sentiment"]
)
```

### Example 3: Template
```python
history.save(
    prompt=template.format(topic="AI"),
    output=response,
    template="explain-concept",
    tags=["education", "AI"]
)
```

## Error Tracking

```python
# Track failures
try:
    output = call_ai(prompt)
except Exception as e:
    history.save(
        prompt=prompt,
        output=f"ERROR: {str(e)}",
        tags=["error"],
        metadata={"error_type": type(e).__name__}
    )
```

## Batch Processing

```python
# Process multiple prompts
for prompt in prompts:
    output = call_ai(prompt)
    history.save(
        prompt=prompt,
        output=output,
        tags=["batch"],
        metadata={"batch_id": batch_id}
    )
```

## Analysis

```python
# Get all entries
entries = history.get_recent(limit=1000)

# Calculate metrics
total_cost = sum(e.cost for e in entries if e.cost)
avg_tokens = sum(e.tokens for e in entries if e.tokens) / len(entries)

# Group by framework
from collections import Counter
frameworks = Counter(e.framework_used for e in entries)
```

## Custom Database

```python
# Project-specific database
from pathlib import Path
project_db = Path("./my_project/prompts.db")
history = PromptHistory(db_path=project_db)
```

## Performance

- Uses indexes for fast queries
- FTS5 for optimized full-text search
- Batch operations supported
- Efficient for 100k+ entries

## Related Files

- `prompt_history.py` - Main script
- `prompt_history_examples.py` - Usage examples
- `test_prompt_history.py` - Test suite
- `PROMPT_HISTORY_README.md` - Full documentation
