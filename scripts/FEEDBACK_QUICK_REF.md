# Feedback System - Quick Reference

## 🚀 Getting Started (3 Commands)

```bash
# 1. Initialize database (one time only)
python feedback_system.py --init

# 2. Run interactive tutorial
python quickstart_feedback.py

# 3. View examples
python feedback_system_examples.py --all
```

## 📝 Common Commands

### Capture Feedback
```bash
python feedback_system.py --capture \
  --prompt "Your prompt here" \
  --output "LLM output here" \
  --rating 5 \
  --thumbs-up \
  --tags "tag1,tag2" \
  --framework "chain-of-thought" \
  --notes "Optional notes"
```

### Analyze Patterns
```bash
# Last 7 days (default)
python feedback_system.py --analyze

# Custom period
python feedback_system.py --analyze --days 30 --min-samples 10
```

### Generate Reports
```bash
# Weekly report (display only)
python feedback_system.py --report --period weekly

# Save to file
python feedback_system.py --report --period monthly --output report.json
```

### Get AI Suggestions
```bash
# General suggestions
python feedback_system.py --suggest

# Target specific framework
python feedback_system.py --suggest --framework "chain-of-thought" --limit 5
```

## 💻 Code Integration

### Basic Integration
```python
from feedback_system import capture_feedback

# After LLM call, capture feedback
capture_feedback(
    prompt=prompt_text,
    output=llm_response,
    rating=5,
    thumbs_up=True,
    tags=["category"],
    context={"model": "claude", "framework": "cot"}
)
```

### With Prompt Router
```python
from prompt_router import route_prompt, build_enhanced_prompt
from feedback_system import capture_feedback

# Route
routing = route_prompt(task)
enhanced = build_enhanced_prompt(task, routing)

# Execute (your LLM call here)
response = your_llm_call(enhanced)

# Capture feedback
capture_feedback(
    prompt=enhanced,
    output=response,
    rating=user_rating,
    thumbs_up=user_thumbs_up,
    tags=["tag"],
    context={
        "framework": routing.primary_framework,
        "confidence": routing.confidence
    }
)
```

### Learning Router
```python
from adaptive_router import LearningRouter

router = LearningRouter()
routing = router.route(task)  # Learns from feedback!
```

## 📊 Querying Data

### Python API
```python
from feedback_system import FeedbackDatabase

db = FeedbackDatabase()

# Get all feedback
all_feedback = db.get_feedback()

# Get positive only (rating >= 4)
positive = db.get_feedback(min_rating=4)

# Get by date range
recent = db.get_feedback(
    start_date="2024-11-01",
    end_date="2024-12-01"
)

# Get statistics
stats = db.get_statistics()
print(f"Success rate: {stats['success_rate']:.1%}")
```

## 🔍 Pattern Analysis

```python
from feedback_system import analyze_patterns

analysis = analyze_patterns(days=7, min_samples=5)

print(f"Success rate: {analysis.success_rate:.1%}")
print("Recommendations:")
for rec in analysis.recommendations:
    print(f"  - {rec}")
```

## 📈 Reports

```python
from feedback_system import generate_report

report = generate_report(period="weekly")

print(f"Total prompts: {report.total_prompts}")
print(f"Avg rating: {report.avg_rating:.2f}/5")
print(f"Success rate: {report.success_rate:.1%}")
```

## 🎯 Best Practices

### Tagging Strategy
```python
tags = [
    "type:technical",      # Task type
    "domain:code",         # Domain
    "format:structured"    # Output format
]
```

### Context to Include
```python
context = {
    "framework": routing.primary_framework,
    "model": model_name,
    "confidence": routing.confidence,
    "execution_time": time_taken,
    "tokens": token_count
}
```

### Rating Guidelines
- **5** = Perfect, exactly what was needed
- **4** = Good, minor improvements possible
- **3** = Acceptable, some issues
- **2** = Poor, significant problems
- **1** = Failed, completely wrong

## ⏰ Automation

### Daily Check
```bash
# Cron (Linux/Mac)
0 9 * * * cd /path && python feedback_system.py --analyze --days 1

# Task Scheduler (Windows)
schtasks /create /tn "FeedbackDaily" /tr "python feedback_system.py --analyze" /sc daily /st 09:00
```

### Weekly Report
```bash
# Cron (Monday 10 AM)
0 10 * * MON cd /path && python feedback_system.py --report --period weekly

# Task Scheduler
schtasks /create /tn "FeedbackWeekly" /tr "python feedback_system.py --report" /sc weekly /d MON /st 10:00
```

## 🧪 Testing

```bash
# Run all tests
python tests/test_feedback_system.py

# Run specific example
python feedback_system_examples.py --example 3

# Quick verification
python feedback_system.py --analyze --days 1 --min-samples 1
```

## 🔧 Troubleshooting

| Problem | Solution |
|---------|----------|
| "Insufficient feedback data" | Lower `--min-samples` or collect more data |
| AI suggestions failing | Set `ANTHROPIC_API_KEY` or use fallback |
| Database locked | Ensure single writer access |
| Unicode errors | Already fixed in current version |

## 📚 Documentation

- **Full Guide:** `FEEDBACK_SYSTEM_README.md`
- **Integration:** `FEEDBACK_INTEGRATION_GUIDE.md`
- **Summary:** `FEEDBACK_SYSTEM_SUMMARY.md`
- **This File:** Quick reference

## 📂 File Locations

```
scripts/
├── feedback_system.py              # Main system (1,363 lines)
├── feedback_system_examples.py     # Examples (566 lines)
├── quickstart_feedback.py          # Tutorial (297 lines)
└── FEEDBACK_*.md                   # Documentation

tests/
└── test_feedback_system.py         # Tests (422 lines)

data/
└── feedback.db                     # Database
```

## 🎓 Learning Path

1. **Day 1:** Run `quickstart_feedback.py`
2. **Day 2:** Integrate basic capture into workflow
3. **Week 1:** Collect 20-30 feedback entries
4. **Week 2:** Run first analysis, review recommendations
5. **Month 1:** Implement learning router, automate reports
6. **Ongoing:** Continuous improvement based on insights

## 💡 Key Metrics to Track

```python
# Get current metrics
stats = db.get_statistics()

key_metrics = {
    "success_rate": stats['success_rate'],      # Target: > 70%
    "avg_rating": stats['avg_rating'],          # Target: > 4.0
    "total_feedback": stats['total_count'],     # Growth indicator
    "thumbs_up_ratio": stats['thumbs_up_count'] / stats['total_count']
}
```

## 🚨 Quick Alerts

```python
# Check if metrics are declining
if stats['success_rate'] < 0.6:
    print("WARNING: Success rate below 60%")
    # Review recent negative feedback
    negative = db.get_feedback(max_rating=2, limit=10)

if stats['avg_rating'] < 3.5:
    print("WARNING: Average rating below 3.5")
    # Analyze patterns
    analysis = analyze_patterns()
```

## 📞 Support

1. Check documentation (see above)
2. Review examples: `feedback_system_examples.py`
3. Run tests: `test_feedback_system.py`
4. Read source code (well-documented)

---

**Version:** 1.0
**Status:** Production Ready
**Tests:** 17/17 Passing
**Lines of Code:** 2,648
**Documentation:** Complete
