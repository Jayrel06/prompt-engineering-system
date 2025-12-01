# Feedback System Integration Guide

Quick guide for integrating the feedback system into your prompt engineering workflow.

## 1. Quick Setup (5 minutes)

### Initialize Database

```bash
cd scripts
python feedback_system.py --init
```

### Set API Key (for AI suggestions)

```bash
# Windows
set ANTHROPIC_API_KEY=your-key-here

# Linux/Mac
export ANTHROPIC_API_KEY=your-key-here
```

## 2. Basic Workflow Integration

### Modify Your Prompt Execution Script

```python
from prompt_router import route_prompt, build_enhanced_prompt
from feedback_system import capture_feedback

def execute_prompt(user_task):
    """Execute a prompt with feedback capture."""

    # 1. Route the prompt
    routing = route_prompt(user_task)
    enhanced_prompt = build_enhanced_prompt(user_task, routing)

    # 2. Call your LLM (example with Anthropic)
    import anthropic
    client = anthropic.Anthropic()
    response = client.messages.create(
        model=routing.model_recommendation,
        max_tokens=2048,
        messages=[{"role": "user", "content": enhanced_prompt}]
    )
    output = response.content[0].text

    # 3. Display output to user
    print(output)

    # 4. Capture feedback
    print("\nHow would you rate this response?")
    rating = int(input("Rating (1-5): "))
    thumbs_up = rating >= 4

    # Optional: Let user add tags
    print("Add tags (comma-separated, or press Enter to skip):")
    tags_input = input("> ").strip()
    tags = [t.strip() for t in tags_input.split(",")] if tags_input else []

    # Store feedback
    capture_feedback(
        prompt=enhanced_prompt,
        output=output,
        rating=rating,
        thumbs_up=thumbs_up,
        tags=tags,
        context={
            "framework": routing.primary_framework,
            "model": routing.model_recommendation,
            "confidence": routing.confidence,
            "original_task": user_task
        }
    )

    return output

# Use it
result = execute_prompt("Explain how recursion works")
```

## 3. Interactive CLI with Feedback

Create `interactive_prompt.py`:

```python
#!/usr/bin/env python3
"""Interactive prompt tool with feedback capture."""

from prompt_router import route_prompt, build_enhanced_prompt
from feedback_system import capture_feedback
import anthropic

def main():
    client = anthropic.Anthropic()

    print("Interactive Prompt Tool with Feedback")
    print("=" * 60)

    while True:
        # Get user task
        print("\nEnter your task (or 'quit' to exit):")
        task = input("> ").strip()

        if not task or task.lower() == 'quit':
            break

        # Route and enhance
        routing = route_prompt(task)
        print(f"\nUsing framework: {routing.primary_framework}")
        print(f"Confidence: {routing.confidence:.0%}")

        enhanced = build_enhanced_prompt(task, routing)

        # Execute
        print("\nGenerating response...\n")
        response = client.messages.create(
            model=routing.model_recommendation,
            max_tokens=2048,
            messages=[{"role": "user", "content": enhanced}]
        )
        output = response.content[0].text

        # Display
        print("-" * 60)
        print(output)
        print("-" * 60)

        # Capture feedback
        print("\nRate this response (1-5):")
        rating = int(input("> "))

        # Auto-capture with smart defaults
        capture_feedback(
            prompt=enhanced,
            output=output,
            rating=rating,
            thumbs_up=rating >= 4,
            tags=[routing.primary_framework.split("-")[0]],  # First word as tag
            context={
                "framework": routing.primary_framework,
                "model": routing.model_recommendation
            }
        )

        print("\nFeedback saved!")

if __name__ == "__main__":
    main()
```

Run it:

```bash
python interactive_prompt.py
```

## 4. Automated Daily/Weekly Reports

### Create `daily_feedback_check.py`:

```python
#!/usr/bin/env python3
"""Daily feedback check - run as a cron job."""

from feedback_system import analyze_patterns, FeedbackDatabase
from datetime import datetime

def daily_check():
    """Run daily feedback analysis."""

    print(f"\nDaily Feedback Check - {datetime.now().strftime('%Y-%m-%d')}")
    print("=" * 60)

    # Get stats
    db = FeedbackDatabase()
    stats = db.get_statistics()

    print(f"\nAll-time stats:")
    print(f"  Total feedback: {stats['total_count']}")
    print(f"  Success rate: {stats['success_rate']:.1%}")
    print(f"  Average rating: {stats['avg_rating']:.2f}/5")

    # Analyze recent patterns
    try:
        analysis = analyze_patterns(days=7, min_samples=3)
        print(f"\nTop recommendation:")
        print(f"  {analysis.recommendations[0]}")
    except ValueError:
        print("\n  (Need more data for pattern analysis)")

if __name__ == "__main__":
    daily_check()
```

### Create `weekly_report.py`:

```python
#!/usr/bin/env python3
"""Weekly report generator."""

from feedback_system import generate_report
from datetime import datetime

def weekly_report():
    """Generate and optionally email weekly report."""

    # Generate report
    report = generate_report(
        period="weekly",
        output_file=f"reports/weekly_{datetime.now().strftime('%Y-W%U')}.json"
    )

    # Could add email notification here
    # send_email(to="team@example.com", report=report)

    return report

if __name__ == "__main__":
    weekly_report()
```

### Schedule with Cron (Linux/Mac):

```bash
# Add to crontab
crontab -e

# Daily check at 9 AM
0 9 * * * cd /path/to/scripts && python daily_feedback_check.py

# Weekly report every Monday at 10 AM
0 10 * * MON cd /path/to/scripts && python weekly_report.py
```

### Schedule with Task Scheduler (Windows):

```powershell
# Create task for daily check
schtasks /create /tn "FeedbackDailyCheck" /tr "python C:\path\to\daily_feedback_check.py" /sc daily /st 09:00

# Create task for weekly report
schtasks /create /tn "FeedbackWeeklyReport" /tr "python C:\path\to\weekly_report.py" /sc weekly /d MON /st 10:00
```

## 5. Learning Router (Advanced)

Create `adaptive_router.py`:

```python
#!/usr/bin/env python3
"""Router that learns from feedback."""

from prompt_router import route_prompt, RoutingResult
from feedback_system import FeedbackDatabase, FeedbackAnalyzer
from typing import Optional

class LearningRouter:
    """Router that adapts based on feedback history."""

    def __init__(self):
        self.db = FeedbackDatabase()
        self.analyzer = FeedbackAnalyzer(self.db)
        self.min_samples = 5  # Minimum feedback samples before learning

    def route(self, task: str, learning_days: int = 7) -> RoutingResult:
        """
        Route task with learning from feedback.

        Args:
            task: User task
            learning_days: Days of feedback to consider

        Returns:
            Enhanced routing result
        """
        # Standard routing
        routing = route_prompt(task)

        # Try to incorporate learning
        try:
            analysis = self.analyzer.analyze_patterns(
                days=learning_days,
                min_samples=self.min_samples
            )

            # Adjust confidence based on framework performance
            framework = routing.primary_framework
            if framework in analysis.framework_performance:
                perf = analysis.framework_performance[framework]

                # Boost confidence for well-performing frameworks
                if perf['success_rate'] > 0.8 and perf['count'] >= self.min_samples:
                    routing.confidence = min(1.0, routing.confidence * 1.15)
                    routing.reasoning += f" (Framework: {perf['success_rate']:.0%} success rate)"

                # Lower confidence for poor performers
                elif perf['success_rate'] < 0.5 and perf['count'] >= self.min_samples:
                    routing.confidence *= 0.85
                    routing.reasoning += f" (Framework needs improvement: {perf['success_rate']:.0%})"

            # Add top recommendations as notes
            if analysis.recommendations:
                routing.reasoning += f" | Tip: {analysis.recommendations[0]}"

        except ValueError:
            # Not enough data yet - use standard routing
            pass

        return routing

# Usage
router = LearningRouter()
routing = router.route("Calculate derivative of x^2")
print(f"Framework: {routing.primary_framework}")
print(f"Confidence: {routing.confidence:.1%}")
print(f"Reasoning: {routing.reasoning}")
```

## 6. API Integration

### REST API Example (Flask):

```python
from flask import Flask, request, jsonify
from feedback_system import capture_feedback
from prompt_router import route_prompt

app = Flask(__name__)

@app.route('/api/feedback', methods=['POST'])
def submit_feedback():
    """API endpoint for feedback submission."""
    data = request.json

    entry = capture_feedback(
        prompt=data['prompt'],
        output=data['output'],
        rating=data['rating'],
        thumbs_up=data['thumbs_up'],
        tags=data.get('tags', []),
        context=data.get('context', {})
    )

    return jsonify({
        'success': True,
        'feedback_id': entry.feedback_id
    })

@app.route('/api/feedback/stats', methods=['GET'])
def get_stats():
    """Get feedback statistics."""
    from feedback_system import FeedbackDatabase

    db = FeedbackDatabase()
    stats = db.get_statistics()

    return jsonify(stats)

if __name__ == '__main__':
    app.run(debug=True)
```

### JavaScript Client:

```javascript
// Submit feedback
async function submitFeedback(prompt, output, rating, thumbsUp) {
    const response = await fetch('/api/feedback', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({
            prompt,
            output,
            rating,
            thumbs_up: thumbsUp,
            tags: ['web-ui'],
            context: {
                source: 'web-interface',
                timestamp: new Date().toISOString()
            }
        })
    });

    return await response.json();
}

// Get stats
async function getStats() {
    const response = await fetch('/api/feedback/stats');
    return await response.json();
}
```

## 7. Slack Integration

### Send Weekly Reports to Slack:

```python
import requests
from feedback_system import generate_report

def send_slack_report(webhook_url):
    """Send weekly report to Slack."""

    report = generate_report(period="weekly")

    # Format for Slack
    message = {
        "text": f"📊 Weekly Feedback Report - {report.period}",
        "blocks": [
            {
                "type": "header",
                "text": {
                    "type": "plain_text",
                    "text": f"📊 Weekly Report - {report.period}"
                }
            },
            {
                "type": "section",
                "fields": [
                    {"type": "mrkdwn", "text": f"*Total Prompts:*\n{report.total_prompts}"},
                    {"type": "mrkdwn", "text": f"*Avg Rating:*\n{report.avg_rating:.2f}/5"},
                    {"type": "mrkdwn", "text": f"*Success Rate:*\n{report.success_rate:.1%}"},
                ]
            }
        ]
    }

    if report.improvement_vs_previous:
        emoji = "📈" if report.improvement_vs_previous > 0 else "📉"
        message["blocks"].append({
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": f"{emoji} *Trend:* {report.improvement_vs_previous:+.1f}% vs last week"
            }
        })

    # Add action items
    if report.action_items:
        message["blocks"].append({
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": "*Action Items:*\n" + "\n".join(f"• {item}" for item in report.action_items[:3])
            }
        })

    # Send to Slack
    requests.post(webhook_url, json=message)

# Use it
send_slack_report("https://hooks.slack.com/services/YOUR/WEBHOOK/URL")
```

## 8. Export and Visualization

### Export to CSV for Analysis:

```python
from feedback_system import FeedbackDatabase
import csv

def export_to_csv(output_file="feedback_export.csv"):
    """Export feedback to CSV."""

    db = FeedbackDatabase()
    feedback = db.get_feedback(limit=1000)

    with open(output_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)

        # Header
        writer.writerow([
            'ID', 'Timestamp', 'Rating', 'Thumbs Up',
            'Prompt Length', 'Output Length', 'Tags', 'Framework'
        ])

        # Data
        for entry in feedback:
            writer.writerow([
                entry.feedback_id,
                entry.timestamp,
                entry.rating,
                entry.thumbs_up,
                len(entry.prompt),
                len(entry.output),
                ','.join(entry.tags),
                entry.context.get('framework', 'unknown')
            ])

    print(f"Exported {len(feedback)} entries to {output_file}")

export_to_csv()
```

### Create Simple Dashboard:

```python
from feedback_system import FeedbackDatabase, analyze_patterns
import matplotlib.pyplot as plt

def create_dashboard():
    """Create simple feedback dashboard."""

    db = FeedbackDatabase()

    # Get statistics
    stats = db.get_statistics()
    analysis = analyze_patterns(days=30, min_samples=5)

    # Create plots
    fig, axes = plt.subplots(2, 2, figsize=(12, 8))

    # Plot 1: Success rate over time
    # (simplified - you'd query by date ranges)
    axes[0, 0].bar(['Week 1', 'Week 2', 'Week 3', 'Week 4'],
                   [0.6, 0.7, 0.75, 0.8])
    axes[0, 0].set_title('Success Rate Trend')
    axes[0, 0].set_ylabel('Success Rate')

    # Plot 2: Rating distribution
    feedback = db.get_feedback(limit=100)
    ratings = [f.rating for f in feedback]
    axes[0, 1].hist(ratings, bins=5, range=(1, 6))
    axes[0, 1].set_title('Rating Distribution')
    axes[0, 1].set_xlabel('Rating')

    # Plot 3: Top frameworks
    framework_perf = analysis.framework_performance
    frameworks = list(framework_perf.keys())[:5]
    success_rates = [framework_perf[f]['success_rate'] for f in frameworks]
    axes[1, 0].barh(frameworks, success_rates)
    axes[1, 0].set_title('Framework Performance')

    # Plot 4: Tag performance
    tag_perf = analysis.tag_performance
    tags = list(tag_perf.keys())[:5]
    tag_rates = [tag_perf[t]['success_rate'] for t in tags]
    axes[1, 1].barh(tags, tag_rates)
    axes[1, 1].set_title('Tag Performance')

    plt.tight_layout()
    plt.savefig('feedback_dashboard.png')
    print("Dashboard saved to feedback_dashboard.png")

create_dashboard()
```

## 9. Testing

Always test your integration:

```bash
# Run unit tests
python tests/test_feedback_system.py

# Run examples
python feedback_system_examples.py --all

# Test capture
python feedback_system.py --capture \
  --prompt "Test" --output "Test" --rating 5 --thumbs-up \
  --tags "test"

# Test analysis
python feedback_system.py --analyze --days 1
```

## 10. Troubleshooting

### Issue: Database locked
**Solution:** Only one process should write at a time. Use locks or queue writes.

### Issue: Not enough feedback
**Solution:** Lower `--min-samples` threshold or collect more data.

### Issue: AI suggestions failing
**Solution:** Check `ANTHROPIC_API_KEY` is set. System will use fallback suggestions.

## Next Steps

1. ✅ Initialize database: `python feedback_system.py --init`
2. ✅ Run examples: `python feedback_system_examples.py --all`
3. ✅ Integrate into your workflow (use examples above)
4. ✅ Set up daily/weekly checks
5. ✅ Review patterns and act on recommendations

## Support

See `FEEDBACK_SYSTEM_README.md` for full documentation.
