# Prompt Doctor - Advanced Usage & API Guide

## Python API Examples

### Basic Usage

```python
from prompt_doctor import PromptDoctor, DiagnosticResult, Issue, format_report

# Create doctor instance
doctor = PromptDoctor(verbose=False)

# Diagnose a prompt
prompt = "Write a story about robots"
result = doctor.diagnose_prompt(prompt)

# Access results
print(f"Quality Score: {result.quality_score}/100")
print(f"Health: {result.overall_health}")
print(f"Issues Found: {len(result.issues)}")

# Iterate through issues
for issue in result.issues:
    print(f"\n{issue.severity.value}: {issue.type.value}")
    print(f"  {issue.description}")
    print(f"  Fix: {issue.suggestion}")
```

### Working with Issues

```python
# Filter issues by severity
from prompt_doctor import Severity

high_priority = [i for i in result.issues if i.severity == Severity.HIGH]
medium_priority = [i for i in result.issues if i.severity == Severity.MEDIUM]
low_priority = [i for i in result.issues if i.severity == Severity.LOW]

print(f"Critical fixes needed: {len(high_priority)}")

# Filter by type
from prompt_doctor import IssueType

format_issues = [i for i in result.issues
                 if i.type == IssueType.MISSING_FORMAT]

if format_issues:
    print("Add format specification!")
```

### Dimension Scores

```python
# Access individual dimension scores
scores = {
    'clarity': result.clarity_score,
    'specificity': result.specificity_score,
    'completeness': result.completeness_score,
    'complexity': result.complexity_score,
    'overall': result.quality_score
}

# Find weakest dimension
weakest = min(scores.items(), key=lambda x: x[1])
print(f"Focus on improving: {weakest[0]} (score: {weakest[1]})")

# Check if meets threshold
MIN_QUALITY = 70
if result.quality_score < MIN_QUALITY:
    print(f"Below threshold! Needs {MIN_QUALITY - result.quality_score} point improvement")
```

### Auto-Fix and Iteration

```python
# Auto-fix and re-diagnose
original = "Write something"
result1 = doctor.diagnose_prompt(original)

fixed = doctor.auto_fix(original, result1)
result2 = doctor.diagnose_prompt(fixed)

print(f"Original score: {result1.quality_score}")
print(f"Fixed score: {result2.quality_score}")
print(f"Improvement: {result2.quality_score - result1.quality_score} points")
```

### JSON Export/Import

```python
import json

# Export to JSON
result_dict = result.to_dict()
json_str = json.dumps(result_dict, indent=2)

# Save to file
with open('diagnostic_report.json', 'w') as f:
    json.dump(result_dict, f, indent=2)

# Load and analyze
with open('diagnostic_report.json', 'r') as f:
    data = json.load(f)

print(f"Loaded quality score: {data['quality_score']}")
print(f"Issue count: {len(data['issues'])}")
```

### Custom Reporting

```python
# Create custom report
def create_summary_report(result: DiagnosticResult) -> str:
    lines = [
        f"PROMPT HEALTH: {result.overall_health}",
        f"Quality: {result.quality_score}/100",
        "",
        "Top 3 Improvements:"
    ]

    # Sort by severity and take top 3
    sorted_issues = sorted(
        result.issues,
        key=lambda x: {'HIGH': 0, 'MEDIUM': 1, 'LOW': 2}[x.severity.value]
    )

    for i, issue in enumerate(sorted_issues[:3], 1):
        lines.append(f"{i}. {issue.suggestion}")

    return "\n".join(lines)

print(create_summary_report(result))
```

## Batch Processing

### Analyze Multiple Prompts

```python
import os
from pathlib import Path

def analyze_prompt_directory(directory: str) -> dict:
    """Analyze all .txt files in a directory"""
    doctor = PromptDoctor()
    results = {}

    for filepath in Path(directory).glob('*.txt'):
        with open(filepath, 'r', encoding='utf-8') as f:
            prompt = f.read()

        result = doctor.diagnose_prompt(prompt)
        results[filepath.name] = {
            'quality': result.quality_score,
            'issues': len(result.issues),
            'health': result.overall_health
        }

    return results

# Run analysis
results = analyze_prompt_directory('prompts/')

# Generate report
for filename, data in sorted(results.items(), key=lambda x: x[1]['quality']):
    print(f"{filename:30s} {data['health']:10s} {data['quality']:5.1f}/100")
```

### Compare Prompts

```python
def compare_prompts(prompt1: str, prompt2: str) -> dict:
    """Compare two prompts and show which is better"""
    doctor = PromptDoctor()

    r1 = doctor.diagnose_prompt(prompt1)
    r2 = doctor.diagnose_prompt(prompt2)

    comparison = {
        'winner': 'Prompt 1' if r1.quality_score > r2.quality_score else 'Prompt 2',
        'scores': {
            'prompt1': r1.quality_score,
            'prompt2': r2.quality_score,
            'difference': abs(r1.quality_score - r2.quality_score)
        },
        'dimensions': {
            'clarity': (r1.clarity_score, r2.clarity_score),
            'specificity': (r1.specificity_score, r2.specificity_score),
            'completeness': (r1.completeness_score, r2.completeness_score),
            'complexity': (r1.complexity_score, r2.complexity_score)
        }
    }

    return comparison

# Compare
result = compare_prompts(
    "Write a story",
    "Write a 500-word science fiction story about AI for teenagers"
)

print(f"Winner: {result['winner']}")
print(f"Score difference: {result['scores']['difference']:.1f} points")
```

## Integration Examples

### Pre-Commit Hook

Save as `.git/hooks/pre-commit`:

```bash
#!/bin/bash
# Validate prompt quality before commit

THRESHOLD=60
FAILED=0

for file in prompts/*.txt; do
    if [ -f "$file" ]; then
        score=$(python scripts/prompt_doctor.py --diagnose "$file" --json | \
                jq '.quality_score')

        if (( $(echo "$score < $THRESHOLD" | bc -l) )); then
            echo "❌ $file: Quality too low ($score/100, minimum: $THRESHOLD)"
            FAILED=1
        else
            echo "✅ $file: Quality OK ($score/100)"
        fi
    fi
done

exit $FAILED
```

### CI/CD Pipeline (GitHub Actions)

`.github/workflows/validate-prompts.yml`:

```yaml
name: Validate Prompts

on: [push, pull_request]

jobs:
  validate:
    runs-on: ubuntu-latest

    steps:
    - uses: actions/checkout@v2

    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: '3.9'

    - name: Validate prompts
      run: |
        for file in prompts/*.txt; do
          python scripts/prompt_doctor.py --diagnose "$file" --json > report.json
          score=$(jq '.quality_score' report.json)

          if (( $(echo "$score < 60" | bc -l) )); then
            echo "::error file=$file::Quality score $score below threshold"
            exit 1
          fi
        done
```

### Flask API Endpoint

```python
from flask import Flask, request, jsonify
from prompt_doctor import PromptDoctor

app = Flask(__name__)
doctor = PromptDoctor()

@app.route('/api/diagnose', methods=['POST'])
def diagnose_endpoint():
    """API endpoint for prompt diagnosis"""
    data = request.get_json()

    if 'prompt' not in data:
        return jsonify({'error': 'Missing prompt field'}), 400

    result = doctor.diagnose_prompt(data['prompt'])

    response = result.to_dict()

    # Add recommendations
    if result.quality_score < 60:
        response['recommendation'] = 'Needs significant improvement'
    elif result.quality_score < 80:
        response['recommendation'] = 'Good, minor improvements possible'
    else:
        response['recommendation'] = 'Excellent quality'

    return jsonify(response)

@app.route('/api/compare', methods=['POST'])
def compare_endpoint():
    """Compare two prompts"""
    data = request.get_json()

    if 'prompt1' not in data or 'prompt2' not in data:
        return jsonify({'error': 'Missing prompts'}), 400

    r1 = doctor.diagnose_prompt(data['prompt1'])
    r2 = doctor.diagnose_prompt(data['prompt2'])

    return jsonify({
        'prompt1': r1.to_dict(),
        'prompt2': r2.to_dict(),
        'winner': 'prompt1' if r1.quality_score > r2.quality_score else 'prompt2',
        'difference': abs(r1.quality_score - r2.quality_score)
    })

if __name__ == '__main__':
    app.run(debug=True)
```

### Gradio UI

```python
import gradio as gr
from prompt_doctor import PromptDoctor, format_report

doctor = PromptDoctor()

def analyze_prompt(prompt_text):
    """Gradio interface function"""
    result = doctor.diagnose_prompt(prompt_text)
    report = format_report(result, verbose=False)

    # Also show auto-fix
    fixed = doctor.auto_fix(prompt_text, result)

    return report, fixed, result.quality_score

# Create interface
with gr.Blocks() as demo:
    gr.Markdown("# Prompt Doctor")

    with gr.Row():
        with gr.Column():
            prompt_input = gr.Textbox(
                label="Enter your prompt",
                lines=10,
                placeholder="Write your prompt here..."
            )
            analyze_btn = gr.Button("Diagnose")

        with gr.Column():
            report_output = gr.Textbox(
                label="Diagnostic Report",
                lines=15
            )
            score = gr.Number(label="Quality Score")
            fixed_output = gr.Textbox(
                label="Auto-Fixed Prompt",
                lines=10
            )

    analyze_btn.click(
        fn=analyze_prompt,
        inputs=prompt_input,
        outputs=[report_output, fixed_output, score]
    )

demo.launch()
```

## Custom Extensions

### Add Custom Issue Types

```python
from prompt_doctor import PromptDoctor, Issue, IssueType, Severity
import re

class CustomPromptDoctor(PromptDoctor):
    """Extended version with custom checks"""

    def check_industry_terms(self, prompt: str) -> list[Issue]:
        """Check for industry-specific requirements"""
        issues = []

        # Example: Check for medical disclaimers
        if 'medical' in prompt.lower() or 'health' in prompt.lower():
            if 'disclaimer' not in prompt.lower():
                issues.append(Issue(
                    type=IssueType.MISSING_CONSTRAINTS,
                    severity=Severity.HIGH,
                    description="Medical content without disclaimer requirement",
                    suggestion="Add requirement for medical disclaimer",
                    location="constraints"
                ))

        return issues

    def diagnose_prompt(self, prompt: str):
        """Override to add custom checks"""
        result = super().diagnose_prompt(prompt)

        # Add custom checks
        result.issues.extend(self.check_industry_terms(prompt))

        # Recalculate quality score
        result.quality_score = self._calculate_quality_score(result)

        return result

# Use custom doctor
custom_doctor = CustomPromptDoctor()
result = custom_doctor.diagnose_prompt("Provide medical advice...")
```

### Track Metrics Over Time

```python
import sqlite3
from datetime import datetime
from prompt_doctor import PromptDoctor

class PromptMetricsTracker:
    """Track prompt quality metrics over time"""

    def __init__(self, db_path='prompt_metrics.db'):
        self.db = sqlite3.connect(db_path)
        self.doctor = PromptDoctor()
        self._init_db()

    def _init_db(self):
        self.db.execute("""
            CREATE TABLE IF NOT EXISTS metrics (
                id INTEGER PRIMARY KEY,
                timestamp TEXT,
                prompt_hash TEXT,
                quality_score REAL,
                clarity_score REAL,
                specificity_score REAL,
                completeness_score REAL,
                complexity_score REAL,
                issue_count INTEGER
            )
        """)

    def track(self, prompt: str, identifier: str = None):
        """Track a prompt's metrics"""
        result = self.doctor.diagnose_prompt(prompt)

        self.db.execute("""
            INSERT INTO metrics
            (timestamp, prompt_hash, quality_score, clarity_score,
             specificity_score, completeness_score, complexity_score, issue_count)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            datetime.now().isoformat(),
            identifier or str(hash(prompt)),
            result.quality_score,
            result.clarity_score,
            result.specificity_score,
            result.completeness_score,
            result.complexity_score,
            len(result.issues)
        ))

        self.db.commit()
        return result

    def get_trends(self, prompt_hash: str):
        """Get quality trends for a specific prompt"""
        cursor = self.db.execute("""
            SELECT timestamp, quality_score
            FROM metrics
            WHERE prompt_hash = ?
            ORDER BY timestamp
        """, (prompt_hash,))

        return cursor.fetchall()

# Usage
tracker = PromptMetricsTracker()
result = tracker.track("Write a story", identifier="story_v1")
print(f"Quality: {result.quality_score}")

# Later, track improvement
result2 = tracker.track("Write a 500-word story about...", identifier="story_v2")
trends = tracker.get_trends("story_v2")
```

## Testing Utilities

### Create Test Suite

```python
import unittest
from prompt_doctor import PromptDoctor

class TestPromptQuality(unittest.TestCase):
    """Test suite for prompt quality standards"""

    def setUp(self):
        self.doctor = PromptDoctor()
        self.MIN_QUALITY = 70

    def test_production_prompts_meet_threshold(self):
        """All production prompts must meet minimum quality"""
        with open('prompts/production.txt', 'r') as f:
            prompt = f.read()

        result = self.doctor.diagnose_prompt(prompt)

        self.assertGreaterEqual(
            result.quality_score,
            self.MIN_QUALITY,
            f"Quality {result.quality_score} below threshold {self.MIN_QUALITY}"
        )

    def test_no_high_severity_issues(self):
        """Production prompts should have no high severity issues"""
        with open('prompts/production.txt', 'r') as f:
            prompt = f.read()

        result = self.doctor.diagnose_prompt(prompt)
        high_issues = [i for i in result.issues if i.severity.value == 'HIGH']

        self.assertEqual(
            len(high_issues),
            0,
            f"Found {len(high_issues)} high severity issues"
        )

if __name__ == '__main__':
    unittest.main()
```

## Best Practices

### 1. Iterative Improvement

```python
def improve_prompt_iteratively(initial_prompt: str, target_score: float = 80):
    """Iteratively improve prompt until target score reached"""
    doctor = PromptDoctor()
    current = initial_prompt
    iteration = 0
    max_iterations = 5

    while iteration < max_iterations:
        result = doctor.diagnose_prompt(current)

        print(f"\nIteration {iteration + 1}:")
        print(f"Score: {result.quality_score}/100")

        if result.quality_score >= target_score:
            print("Target reached!")
            return current, result

        # Auto-fix and continue
        current = doctor.auto_fix(current, result)
        iteration += 1

    print("Max iterations reached")
    return current, result
```

### 2. A/B Testing

```python
def ab_test_prompts(variants: list[str], test_func: callable):
    """A/B test different prompt variants"""
    doctor = PromptDoctor()
    results = []

    for i, prompt in enumerate(variants):
        quality_result = doctor.diagnose_prompt(prompt)
        performance = test_func(prompt)  # Your performance metric

        results.append({
            'variant': i,
            'quality_score': quality_result.quality_score,
            'performance': performance,
            'combined_score': (quality_result.quality_score + performance) / 2
        })

    return sorted(results, key=lambda x: x['combined_score'], reverse=True)
```

### 3. Template Validation

```python
def validate_template(template: str, required_placeholders: list[str]):
    """Validate a prompt template structure"""
    doctor = PromptDoctor()

    # Replace placeholders with examples
    example_filled = template
    for placeholder in required_placeholders:
        example_filled = example_filled.replace(
            f"{{{placeholder}}}",
            f"example_{placeholder}"
        )

    result = doctor.diagnose_prompt(example_filled)

    if result.quality_score < 70:
        print(f"Warning: Template quality only {result.quality_score}/100")
        for issue in result.issues:
            print(f"  - {issue.description}")

    return result
```

## Troubleshooting

### Handle Edge Cases

```python
# Empty prompts
result = doctor.diagnose_prompt("")
# Returns issues with empty prompt warning

# Very long prompts
long_prompt = "word " * 10000
result = doctor.diagnose_prompt(long_prompt)
# Still works, may detect complexity issues

# Unicode content
unicode_prompt = "生成一个关于AI的故事"
result = doctor.diagnose_prompt(unicode_prompt)
# Handles non-English prompts
```

### Performance Optimization

```python
# Cache results for identical prompts
from functools import lru_cache

class CachedPromptDoctor(PromptDoctor):
    @lru_cache(maxsize=100)
    def diagnose_prompt(self, prompt: str):
        return super().diagnose_prompt(prompt)

# Batch processing
def diagnose_batch(prompts: list[str]):
    """Diagnose multiple prompts efficiently"""
    doctor = PromptDoctor()
    return [doctor.diagnose_prompt(p) for p in prompts]
```
