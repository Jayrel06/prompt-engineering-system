# Feedback Capture and Learning Loop System

A production-ready system for capturing user feedback on prompt outputs, analyzing patterns, and generating actionable insights for continuous improvement.

## Features

- **Real-time Feedback Capture**: Thumbs up/down and 1-5 star ratings
- **Persistent Storage**: SQLite database for all feedback entries
- **Pattern Analysis**: Identifies what works and what doesn't
- **Automated Reports**: Weekly/monthly improvement reports
- **AI-Powered Suggestions**: Get prompt modification recommendations
- **Router Integration**: Learn from feedback to improve routing decisions

## Quick Start

### 1. Initialize the Database

```bash
cd scripts
python feedback_system.py --init
```

This creates the database at `data/feedback.db` with the proper schema.

### 2. Capture Feedback

After generating a prompt output, capture user feedback:

```bash
python feedback_system.py --capture \
  --prompt "Explain quantum computing in simple terms" \
  --output "Quantum computing uses quantum mechanics..." \
  --rating 5 \
  --thumbs-up \
  --tags "technical,explanation" \
  --framework "chain-of-thought" \
  --model "claude-sonnet-4"
```

**Parameters:**
- `--prompt`: The original prompt text (required)
- `--output`: The generated output (required)
- `--rating`: Rating from 1-5 (required)
- `--thumbs-up` or `--thumbs-down`: User sentiment
- `--tags`: Comma-separated categorization tags
- `--framework`: Framework used (for context)
- `--model`: Model used (for context)
- `--notes`: Optional user notes

### 3. Analyze Patterns

Analyze feedback patterns to identify what's working:

```bash
# Analyze last 7 days (default)
python feedback_system.py --analyze

# Analyze last 30 days with minimum 10 samples
python feedback_system.py --analyze --days 30 --min-samples 10
```

**Output:**
- Success rate statistics
- Common patterns in successful prompts
- Common patterns in failed prompts
- Tag performance metrics
- Framework performance metrics
- Actionable recommendations

### 4. Generate Reports

Create weekly or monthly improvement reports:

```bash
# Weekly report
python feedback_system.py --report --period weekly

# Monthly report saved to file
python feedback_system.py --report --period monthly --output monthly_report.json
```

**Report Includes:**
- Overall metrics (total prompts, avg rating, success rate)
- Improvement vs previous period
- Top performing frameworks/techniques
- Problem areas requiring attention
- Action items for improvement

### 5. Get AI Suggestions

Get intelligent prompt improvement suggestions:

```bash
# General suggestions based on recent feedback
python feedback_system.py --suggest

# Target specific framework
python feedback_system.py --suggest --framework "chain-of-thought" --limit 5

# Analyze longer time period
python feedback_system.py --suggest --days 30
```

**Note:** Requires `ANTHROPIC_API_KEY` environment variable.

## Integration with Prompt Router

### Basic Integration

```python
from prompt_router import route_prompt, build_enhanced_prompt
from feedback_system import capture_feedback, FeedbackDatabase

# 1. Route the prompt
task = "Explain how neural networks learn"
routing = route_prompt(task)

# 2. Build enhanced prompt
enhanced = build_enhanced_prompt(task, routing)

# 3. Get LLM response (your code here)
response = your_llm_call(enhanced)

# 4. Capture user feedback
db = FeedbackDatabase()
capture_feedback(
    prompt=enhanced,
    output=response,
    rating=user_rating,  # Get from user
    thumbs_up=user_thumbs_up,  # Get from user
    tags=["explanation", "neural-networks"],
    context={
        "framework": routing.primary_framework,
        "model": routing.model_recommendation,
        "confidence": routing.confidence
    },
    db=db
)
```

### Advanced Integration: Learning Loop

```python
from prompt_router import route_prompt
from feedback_system import FeedbackDatabase, FeedbackAnalyzer

class AdaptivePromptRouter:
    """Prompt router that learns from feedback."""

    def __init__(self):
        self.db = FeedbackDatabase()
        self.analyzer = FeedbackAnalyzer(self.db)

    def route_with_learning(self, task, days_to_analyze=7):
        """Route prompt and incorporate learnings from feedback."""
        # Standard routing
        routing = route_prompt(task)

        # Get recent feedback analysis
        try:
            analysis = self.analyzer.analyze_patterns(days=days_to_analyze, min_samples=3)

            # Adjust confidence based on framework performance
            if routing.primary_framework in analysis.framework_performance:
                perf = analysis.framework_performance[routing.primary_framework]

                # Boost confidence if framework is performing well
                if perf['success_rate'] > 0.8:
                    routing.confidence = min(1.0, routing.confidence * 1.1)
                    routing.reasoning += f" | Framework performing well ({perf['success_rate']:.0%} success)"

                # Lower confidence if framework struggling
                elif perf['success_rate'] < 0.5:
                    routing.confidence *= 0.9
                    routing.reasoning += f" | Framework needs improvement ({perf['success_rate']:.0%} success)"

        except ValueError:
            # Not enough feedback data yet
            pass

        return routing

# Usage
router = AdaptivePromptRouter()
routing = router.route_with_learning("Calculate the derivative of x^2")
```

### Automated Weekly Review

```python
from feedback_system import generate_report, analyze_patterns

def weekly_review_job():
    """Run this as a weekly cron job."""

    # Generate report
    report = generate_report(
        period="weekly",
        output_file=f"reports/week_{datetime.now().strftime('%Y-%W')}.json"
    )

    # Analyze patterns
    analysis = analyze_patterns(days=7, min_samples=5)

    # Send alerts if metrics are declining
    if report.improvement_vs_previous and report.improvement_vs_previous < -10:
        send_alert(f"Success rate declined by {abs(report.improvement_vs_previous):.1f}%")

    # Send recommendations to team
    send_recommendations(analysis.recommendations)

# Schedule with cron:
# 0 9 * * MON python -c "from your_module import weekly_review_job; weekly_review_job()"
```

## Data Model

### FeedbackEntry

```python
@dataclass
class FeedbackEntry:
    prompt: str                    # Original prompt
    output: str                    # Generated output
    rating: int                    # 1-5 rating
    thumbs_up: bool               # Thumbs up/down
    tags: List[str]               # Categorization tags
    timestamp: str                # ISO format timestamp
    context: Dict[str, Any]       # Additional context (model, framework, etc.)
    feedback_id: Optional[str]    # Unique identifier
    notes: Optional[str]          # Optional user notes
```

### PatternAnalysis

```python
@dataclass
class PatternAnalysis:
    total_feedback: int                                 # Total entries analyzed
    positive_count: int                                 # Positive feedback count
    negative_count: int                                 # Negative feedback count
    success_rate: float                                 # Overall success rate
    common_positive_patterns: List[Dict[str, Any]]     # Patterns in successes
    common_negative_patterns: List[Dict[str, Any]]     # Patterns in failures
    tag_performance: Dict[str, Dict[str, Any]]         # Performance by tag
    framework_performance: Dict[str, Dict[str, Any]]   # Performance by framework
    recommendations: List[str]                          # Action items
```

### ImprovementReport

```python
@dataclass
class ImprovementReport:
    period: str                              # Period identifier (e.g., "2024-W48")
    start_date: str                          # Period start
    end_date: str                            # Period end
    total_prompts: int                       # Total prompts in period
    avg_rating: float                        # Average rating
    success_rate: float                      # Success rate
    improvement_vs_previous: Optional[float] # % change vs previous period
    top_performers: List[Dict[str, Any]]    # Best performing areas
    problem_areas: List[Dict[str, Any]]     # Areas needing work
    action_items: List[str]                  # Recommended actions
```

## Database Schema

### feedback table

| Column | Type | Description |
|--------|------|-------------|
| id | INTEGER | Primary key |
| feedback_id | TEXT | Unique entry identifier |
| timestamp | DATETIME | Entry timestamp |
| prompt | TEXT | Prompt text |
| output | TEXT | Output text |
| rating | INTEGER | Rating 1-5 |
| thumbs_up | BOOLEAN | Thumbs up/down |
| tags | TEXT | JSON array of tags |
| context | TEXT | JSON context object |
| notes | TEXT | Optional user notes |

### pattern_cache table

Stores cached pattern analysis results for performance.

### reports table

Stores generated improvement reports.

## Best Practices

### 1. Consistent Tagging

Use consistent tags for better analysis:

```python
# Good - consistent categories
tags = ["technical", "explanation", "code-review"]

# Bad - inconsistent, too specific
tags = ["tech stuff", "explaining things", "reviewing the code I wrote"]
```

**Recommended tag categories:**
- **Type**: `technical`, `creative`, `analytical`, `planning`
- **Domain**: `code`, `content`, `research`, `decision`
- **Format**: `structured`, `freeform`, `step-by-step`

### 2. Capture Context

Always include framework and model information:

```python
context = {
    "framework": routing.primary_framework,
    "model": model_used,
    "confidence": routing.confidence,
    "techniques": routing.techniques,
    "execution_time": time_taken
}
```

### 3. Regular Analysis

Run analysis regularly to catch trends early:

```bash
# Daily quick check
python feedback_system.py --analyze --days 1

# Weekly deep dive
python feedback_system.py --analyze --days 7 --min-samples 10

# Monthly comprehensive analysis
python feedback_system.py --analyze --days 30
```

### 4. Act on Recommendations

The system generates actionable recommendations - implement them:

```python
analysis = analyze_patterns(days=7)

for rec in analysis.recommendations:
    print(f"TODO: {rec}")
    # Create GitHub issues, Jira tickets, etc.
```

### 5. Monitor Success Rate

Track success rate trends over time:

```python
# Get success rate for each week
for week in range(4):
    start = (datetime.now() - timedelta(weeks=week+1)).isoformat()
    end = (datetime.now() - timedelta(weeks=week)).isoformat()

    stats = db.get_statistics(start_date=start, end_date=end)
    print(f"Week -{week}: {stats['success_rate']:.1%}")
```

## Troubleshooting

### "Insufficient feedback data" error

**Problem:** Not enough feedback entries for analysis.

**Solution:**
```bash
# Check how much data you have
python feedback_system.py --analyze --min-samples 1

# Lower minimum samples threshold
python feedback_system.py --analyze --min-samples 3
```

### AI suggestions not working

**Problem:** Missing Anthropic API key.

**Solution:**
```bash
# Set environment variable
export ANTHROPIC_API_KEY="your-key-here"

# Or use fallback suggestions
# The system will automatically use rule-based suggestions if AI fails
```

### Database locked error

**Problem:** Multiple processes accessing database simultaneously.

**Solution:**
```python
# Use context manager for safe access
from feedback_system import FeedbackDatabase

with FeedbackDatabase().get_connection() as conn:
    # Your database operations
    pass
```

## Performance Tips

### Batch Feedback Capture

For high-volume scenarios, batch inserts:

```python
entries = []
for user_interaction in interactions:
    entry = FeedbackEntry(...)
    entries.append(entry)

# Insert all at once
db = FeedbackDatabase()
conn = db.get_connection()
for entry in entries:
    db.insert_feedback(entry)
conn.close()
```

### Use Cached Analysis

Pattern analysis is cached - use it:

```python
# First call - analyzes and caches
analysis1 = analyze_patterns(days=7)

# Subsequent calls on same day - uses cache
# (In production, you'd implement cache retrieval)
```

### Index Optimization

The database includes indexes on:
- `timestamp` - for date range queries
- `rating` - for filtering by rating
- `thumbs_up` - for positive/negative filtering
- `feedback_id` - for unique lookups

## API Reference

### Core Functions

#### `capture_feedback()`
Capture user feedback and store in database.

**Parameters:**
- `prompt` (str): Original prompt
- `output` (str): Generated output
- `rating` (int): 1-5 rating
- `thumbs_up` (bool): Thumbs up/down
- `tags` (List[str]): Category tags
- `context` (Dict): Additional context
- `notes` (Optional[str]): User notes
- `db` (Optional[FeedbackDatabase]): Database instance

**Returns:** `FeedbackEntry`

#### `analyze_patterns()`
Analyze feedback patterns.

**Parameters:**
- `days` (int): Days to analyze (default: 7)
- `min_samples` (int): Minimum samples required (default: 5)
- `db` (Optional[FeedbackDatabase]): Database instance

**Returns:** `PatternAnalysis`

#### `generate_report()`
Generate improvement report.

**Parameters:**
- `period` (str): "weekly" or "monthly" (default: "weekly")
- `output_file` (Optional[str]): File to save report
- `db` (Optional[FeedbackDatabase]): Database instance

**Returns:** `ImprovementReport`

#### `suggest_improvements()`
Get AI-powered suggestions.

**Parameters:**
- `framework` (Optional[str]): Target framework
- `days` (int): Days to analyze (default: 7)
- `limit` (int): Max suggestions (default: 5)
- `db` (Optional[FeedbackDatabase]): Database instance

**Returns:** `List[Dict[str, str]]`

## Examples

See `scripts/feedback_system_examples.py` for more examples:
- Basic feedback capture workflow
- Integration with prompt router
- Automated reporting setup
- Custom analysis queries
- Export and visualization

## License

Part of the Prompt Engineering System. See main repository license.

## Support

For issues or questions:
1. Check this documentation
2. Review `test_feedback_system.py` for usage examples
3. Examine the source code comments
4. Open an issue in the main repository
