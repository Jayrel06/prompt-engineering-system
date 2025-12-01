# Cost Tracking System

A comprehensive cost tracking system for monitoring LLM API usage and expenses across Claude and GPT models.

## Overview

This system tracks token usage and costs for all LLM requests, providing detailed reports, analytics, and export capabilities to help you monitor and optimize AI spending.

## Features

- **Token Usage Tracking**: Log input/output tokens for every API request
- **Cost Calculation**: Automatic cost calculation based on current model pricing
- **Multi-Model Support**: Claude 3.5 Sonnet, Claude 3 Haiku, GPT-4o, GPT-4o-mini
- **Category Tracking**: Organize usage by category (planning, technical, communication, analysis)
- **Flexible Reporting**: Daily, weekly, monthly reports with filtering
- **Data Export**: Export to CSV or JSON for external analysis
- **CLI Integration**: Seamlessly integrated with the prompt.sh CLI

## Files

### 1. `scripts/cost_tracker.py`
Main cost tracking script with full CLI interface.

**Commands:**
- `init` - Initialize the SQLite database
- `log` - Log a new usage entry
- `report` - Generate usage reports
- `stats` - Show quick statistics
- `export` - Export data to CSV/JSON

### 2. `context/technical/model-pricing.md`
Reference document with current model pricing, optimization strategies, and cost-effective patterns.

### 3. `data/usage.db`
SQLite database storing all usage data (auto-created on first use).

## Quick Start

### 1. Initialize the Database

```bash
cd C:/Users/JRiel/prompt-engineering-system
python3 scripts/cost_tracker.py init
```

Or via the prompt CLI:

```bash
prompt cost-init
```

### 2. Log Usage

```bash
# Log a request manually
python3 scripts/cost_tracker.py log \
  --model claude-sonnet-3.5 \
  --input-tokens 1500 \
  --output-tokens 750 \
  --category planning \
  --description "Q1 strategy planning"

# Using model aliases
python3 scripts/cost_tracker.py log \
  --model haiku \
  --input-tokens 800 \
  --output-tokens 300 \
  --category technical
```

**Supported Models:**
- `claude-sonnet-3.5`, `sonnet`, `claude-3.5-sonnet`, `claude-3-5-sonnet-20241022`
- `claude-haiku-3`, `haiku`, `claude-3-haiku`, `claude-3-haiku-20240307`
- `gpt-4o`, `gpt4o`, `gpt-4o-2024-11-20`
- `gpt-4o-mini`, `gpt4mini`, `gpt-4o-mini-2024-07-18`

### 3. View Reports

```bash
# Monthly report (default)
python3 scripts/cost_tracker.py report

# Weekly report
python3 scripts/cost_tracker.py report --period weekly

# Filter by model
python3 scripts/cost_tracker.py report --model claude-sonnet-3.5

# Filter by category
python3 scripts/cost_tracker.py report --category planning

# Custom date range
python3 scripts/cost_tracker.py report \
  --start-date 2025-11-01 \
  --end-date 2025-11-30
```

### 4. Quick Statistics

```bash
# Monthly stats
python3 scripts/cost_tracker.py stats

# Daily stats
python3 scripts/cost_tracker.py stats --period daily

# Stats for specific model
python3 scripts/cost_tracker.py stats --model gpt-4o
```

### 5. Export Data

```bash
# Export to CSV
python3 scripts/cost_tracker.py export --format csv --output usage_report.csv

# Export to JSON
python3 scripts/cost_tracker.py export --format json --output usage_report.json

# Export filtered data
python3 scripts/cost_tracker.py export \
  --format csv \
  --model claude-sonnet-3.5 \
  --start-date 2025-11-01 \
  --output november_sonnet.csv
```

## Integration with prompt.sh

The cost tracking system is fully integrated with the prompt CLI:

```bash
# Check system status (includes cost DB status)
prompt status

# View cost reports
prompt cost-report --period weekly
prompt cost-report --model claude-sonnet-3.5

# View quick stats
prompt cost-stats
prompt cost-stats --period daily

# Export data
prompt cost-export --format csv --output usage.csv

# Initialize database
prompt cost-init
```

### Enabling Cost Tracking for Requests

Add the `--track` flag to any prompt command to enable cost tracking:

```bash
# Track a planning request
prompt --track --category planning plan "Build Q1 roadmap"

# Track with custom description
prompt --track \
  --category technical \
  --description "Docker network architecture" \
  quick "Best practices for Docker networking"
```

**Note:** The `--track` flag currently prepares the infrastructure but requires manual logging of actual API response tokens. Full automatic tracking can be implemented by capturing API responses.

## Model Pricing (Current)

### Anthropic Claude

| Model | Input (per 1M tokens) | Output (per 1M tokens) |
|-------|----------------------|------------------------|
| Claude 3.5 Sonnet | $3.00 | $15.00 |
| Claude 3 Haiku | $0.25 | $1.25 |

### OpenAI

| Model | Input (per 1M tokens) | Output (per 1M tokens) |
|-------|----------------------|------------------------|
| GPT-4o | $2.50 | $10.00 |
| GPT-4o-mini | $0.15 | $0.60 |

See `context/technical/model-pricing.md` for detailed pricing info and optimization strategies.

## Database Schema

The `usage_log` table stores:
- `id` - Auto-incrementing primary key
- `timestamp` - Request timestamp (auto-generated)
- `model` - Canonical model name
- `input_tokens` - Input token count
- `output_tokens` - Output token count
- `total_tokens` - Sum of input + output
- `input_cost` - Calculated input cost
- `output_cost` - Calculated output cost
- `total_cost` - Total cost for the request
- `category` - Optional category (planning, technical, etc.)
- `description` - Optional description
- `metadata` - Optional JSON metadata

Indexes on `timestamp`, `model`, and `category` for fast queries.

## Example Workflows

### Track Daily Usage

```bash
# View today's usage
python3 scripts/cost_tracker.py stats --period daily

# View this week's usage
python3 scripts/cost_tracker.py stats --period weekly
```

### Monthly Budget Monitoring

```bash
# Full monthly report
python3 scripts/cost_tracker.py report --period monthly

# Export for spreadsheet analysis
python3 scripts/cost_tracker.py export \
  --format csv \
  --start-date 2025-11-01 \
  --end-date 2025-11-30 \
  --output november_2025.csv
```

### Category Analysis

```bash
# See which categories cost the most
python3 scripts/cost_tracker.py report --period monthly

# Filter specific category
python3 scripts/cost_tracker.py report --category planning

# Export category data
python3 scripts/cost_tracker.py export \
  --category technical \
  --format csv \
  --output technical_usage.csv
```

### Model Comparison

```bash
# Compare Sonnet vs Haiku usage
python3 scripts/cost_tracker.py report --model claude-sonnet-3.5
python3 scripts/cost_tracker.py report --model claude-haiku-3

# View all models in one report
python3 scripts/cost_tracker.py report --period monthly
```

## Sample Report Output

```
================================================================================
USAGE REPORT - MONTHLY
================================================================================

OVERALL SUMMARY
--------------------------------------------------------------------------------
Total Requests:      3
Total Input Tokens:  4,300
Total Output Tokens: 2,050
Total Tokens:        6,350
Total Input Cost:    $0.009700
Total Output Cost:   $0.021625
TOTAL COST:          $0.03


BREAKDOWN BY MODEL
--------------------------------------------------------------------------------
Model                            Requests          Tokens         Cost
--------------------------------------------------------------------------------
claude-sonnet-3.5                       1           2,250 $       0.02
gpt-4o                                  1           3,000 $       0.01
claude-haiku-3                          1           1,100 $       0.00


BREAKDOWN BY CATEGORY
--------------------------------------------------------------------------------
Category                         Requests          Tokens         Cost
--------------------------------------------------------------------------------
planning                                1           2,250 $       0.02
analysis                                1           3,000 $       0.01
technical                               1           1,100 $       0.00
```

## Advanced Usage

### Custom Metadata

Store additional metadata as JSON:

```python
from scripts.cost_tracker import log_usage

log_usage(
    model="claude-sonnet-3.5",
    input_tokens=1500,
    output_tokens=750,
    category="planning",
    description="Q1 planning",
    metadata={
        "user": "john@example.com",
        "project": "CoreReceptionAI",
        "session_id": "abc123"
    }
)
```

### Programmatic Access

```python
from scripts.cost_tracker import (
    get_db_connection,
    calculate_cost,
    normalize_model_name
)

# Calculate cost without logging
model = normalize_model_name("sonnet")
input_cost, output_cost, total = calculate_cost(model, 1000, 500)

# Query database directly
conn = get_db_connection()
cursor = conn.cursor()
cursor.execute("SELECT * FROM usage_log WHERE category = ?", ("planning",))
results = cursor.fetchall()
```

## Tips & Best Practices

1. **Log Consistently**: Make logging part of your workflow to get accurate cost tracking
2. **Use Categories**: Categorize requests to identify high-cost areas
3. **Regular Reviews**: Run weekly reports to catch cost spikes early
4. **Export Monthly**: Export monthly data for accounting/budgeting
5. **Model Selection**: Use the pricing reference to choose cost-effective models
6. **Set Budgets**: Monitor cumulative costs against your budget limits

## Troubleshooting

### Database Not Found

```bash
# Initialize the database
python3 scripts/cost_tracker.py init
```

### Unknown Model Error

Use one of the supported models or their aliases. Check `model-pricing.md` for the full list.

### Cost Tracking Not Working in prompt.sh

The `--track` flag sets up tracking but requires integration with your LLM API client to capture actual token counts. Manual logging is currently required.

## Future Enhancements

- Automatic token capture from LiteLLM responses
- Real-time budget alerts
- Cost forecasting based on historical trends
- Web dashboard for visualization
- Cost per project/user tracking
- API rate limiting based on budget
- Integration with cloud billing systems

## Files Created

```
C:/Users/JRiel/prompt-engineering-system/
├── scripts/
│   └── cost_tracker.py          # Main cost tracking script (19KB)
├── context/technical/
│   └── model-pricing.md         # Pricing reference (6.1KB)
├── data/
│   └── usage.db                 # SQLite database (auto-created)
└── COST_TRACKING_README.md      # This file
```

## Support

For issues or questions:
1. Check the pricing reference: `context/technical/model-pricing.md`
2. Run `python3 scripts/cost_tracker.py --help`
3. Review the database with any SQLite tool

## License

Part of the prompt-engineering-system project.
