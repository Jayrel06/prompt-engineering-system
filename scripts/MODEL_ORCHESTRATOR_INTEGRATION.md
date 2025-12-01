# Model Orchestrator - Integration Guide

## Overview

This guide shows how to integrate the Model Orchestrator into your existing workflows and scripts.

## Python Integration

### Basic Usage

```python
#!/usr/bin/env python3
import sys
sys.path.insert(0, 'C:/Users/JRiel/prompt-engineering-system/scripts')

from model_orchestrator import run_orchestration

# Simple query with auto-routing
result = run_orchestration(
    prompt="What is Docker?",
    strategy="cheapest"
)

print(f"Response: {result.response}")
print(f"Cost: ${result.cost}")
print(f"Model: {result.model_used}")
```

### Advanced Usage

```python
from model_orchestrator import (
    run_orchestration,
    run_with_fallback,
    run_ensemble,
    route_to_model,
    ComplexityAnalyzer,
    MODEL_REGISTRY
)

# 1. Analyze complexity before routing
capability, confidence = ComplexityAnalyzer.score_complexity(
    "Design a distributed system"
)
print(f"Required capability: {capability.value}")
print(f"Confidence: {confidence:.2f}")

# 2. Route to optimal model
model_name = route_to_model(
    prompt="Your prompt here",
    max_cost=Decimal("0.01")  # Optional cost limit
)
print(f"Selected model: {model_name}")

# 3. Run with fallback
result = run_with_fallback(
    prompt="Explain quantum computing",
    chain=["claude-haiku-3.5", "claude-sonnet-3.5"],
    confidence_threshold=0.7,
    max_cost=Decimal("0.05")
)

# 4. Run ensemble
result = run_ensemble(
    prompt="Compare REST vs GraphQL",
    models=["claude-sonnet-3.5", "gpt-4o", "claude-haiku-3.5"],
    ensemble_size=3,
    max_cost=Decimal("0.10")
)

# Access detailed results
print(f"Strategy: {result.strategy}")
print(f"Model used: {result.model_used}")
print(f"Cost: ${result.cost:.6f}")
print(f"Latency: {result.latency:.2f}s")
print(f"Confidence: {result.confidence:.2f}")
print(f"Input tokens: {result.input_tokens}")
print(f"Output tokens: {result.output_tokens}")

if result.fallback_chain:
    print(f"Fallback chain: {' -> '.join(result.fallback_chain)}")

if result.ensemble_models:
    print(f"Ensemble models: {', '.join(result.ensemble_models)}")

# Export to dict
data = result.to_dict()
import json
with open('result.json', 'w') as f:
    json.dump(data, f, indent=2)
```

### Building a Custom Application

```python
#!/usr/bin/env python3
"""
Example: Question Answering System with Smart Routing
"""
import sys
sys.path.insert(0, 'C:/Users/JRiel/prompt-engineering-system/scripts')

from model_orchestrator import run_orchestration
from decimal import Decimal

class SmartQASystem:
    def __init__(self, max_cost_per_query=0.01):
        self.max_cost = Decimal(str(max_cost_per_query))
        self.total_cost = Decimal("0")
        self.query_count = 0

    def ask(self, question, strategy="cheapest", verbose=False):
        """Ask a question using smart model routing."""
        try:
            result = run_orchestration(
                prompt=question,
                strategy=strategy,
                max_cost=float(self.max_cost),
                verbose=verbose
            )

            self.total_cost += result.cost
            self.query_count += 1

            return {
                'answer': result.response,
                'model': result.model_used,
                'cost': float(result.cost),
                'confidence': result.confidence,
                'metadata': result.metadata
            }

        except Exception as e:
            return {
                'error': str(e),
                'answer': None
            }

    def get_stats(self):
        """Get usage statistics."""
        return {
            'total_queries': self.query_count,
            'total_cost': float(self.total_cost),
            'avg_cost_per_query': float(self.total_cost / self.query_count) if self.query_count > 0 else 0
        }

# Usage
qa = SmartQASystem(max_cost_per_query=0.01)

# Simple questions use cheap models
response = qa.ask("What is Python?", strategy="cheapest")
print(f"Answer: {response['answer']}")
print(f"Model: {response['model']}, Cost: ${response['cost']:.6f}")

# Complex questions use fallback
response = qa.ask("Design a microservices architecture", strategy="fallback")
print(f"Answer: {response['answer']}")
print(f"Model: {response['model']}, Cost: ${response['cost']:.6f}")

# Important decisions use ensemble
response = qa.ask("Should I use SQL or NoSQL?", strategy="ensemble")
print(f"Answer: {response['answer']}")
print(f"Model: {response['model']}, Cost: ${response['cost']:.6f}")

# Get statistics
stats = qa.get_stats()
print(f"\nTotal queries: {stats['total_queries']}")
print(f"Total cost: ${stats['total_cost']:.6f}")
print(f"Average cost: ${stats['avg_cost_per_query']:.6f}")
```

## Bash Integration

### Simple Script

```bash
#!/bin/bash
# analyze_logs.sh

SCRIPT_DIR="C:/Users/JRiel/prompt-engineering-system/scripts"

# Read log file
LOG_CONTENT=$(cat error.log)

# Analyze with model orchestrator
python "$SCRIPT_DIR/model_orchestrator.py" \
  --prompt "Analyze these logs and identify the root cause: $LOG_CONTENT" \
  --strategy fallback \
  --max-cost 0.01 \
  --output analysis.json

# Check result
if [ $? -eq 0 ]; then
    echo "Analysis complete!"
    echo "Model used: $(jq -r '.model_used' analysis.json)"
    echo "Cost: \$$(jq -r '.cost' analysis.json)"
    echo ""
    echo "Analysis:"
    jq -r '.response' analysis.json
else
    echo "Analysis failed!"
    exit 1
fi
```

### Batch Processing

```bash
#!/bin/bash
# batch_process.sh - Process multiple prompts with cost tracking

SCRIPT_DIR="C:/Users/JRiel/prompt-engineering-system/scripts"
TOTAL_COST=0

# Read prompts from file
while IFS= read -r prompt; do
    echo "Processing: $prompt"

    # Run orchestration
    python "$SCRIPT_DIR/model_orchestrator.py" \
      --prompt "$prompt" \
      --strategy cheapest \
      --output "result_$$.json" \
      --max-cost 0.005

    if [ $? -eq 0 ]; then
        cost=$(jq -r '.cost' "result_$$.json")
        TOTAL_COST=$(echo "$TOTAL_COST + $cost" | bc)
        echo "  Cost: \$$cost"
        rm "result_$$.json"
    else
        echo "  Failed!"
    fi

    echo ""
done < prompts.txt

echo "Total cost: \$$TOTAL_COST"
```

### Pipeline with Error Handling

```bash
#!/bin/bash
# intelligent_pipeline.sh

set -e  # Exit on error

SCRIPT_DIR="C:/Users/JRiel/prompt-engineering-system/scripts"
MAX_RETRIES=3

run_with_retry() {
    local prompt="$1"
    local strategy="$2"
    local output="$3"
    local attempt=1

    while [ $attempt -le $MAX_RETRIES ]; do
        echo "Attempt $attempt of $MAX_RETRIES..."

        if python "$SCRIPT_DIR/model_orchestrator.py" \
            --prompt "$prompt" \
            --strategy "$strategy" \
            --output "$output" \
            --max-cost 0.02; then
            echo "Success!"
            return 0
        fi

        attempt=$((attempt + 1))
        sleep 2
    done

    echo "Failed after $MAX_RETRIES attempts"
    return 1
}

# Step 1: Classify input (cheap)
echo "Step 1: Classification..."
run_with_retry "Classify this text: $INPUT" "cheapest" "step1.json"

CATEGORY=$(jq -r '.response' step1.json | grep -oP 'Category: \K\w+')

# Step 2: Process based on category
echo "Step 2: Processing ($CATEGORY)..."
if [ "$CATEGORY" = "complex" ]; then
    run_with_retry "Detailed analysis: $INPUT" "ensemble" "step2.json"
else
    run_with_retry "Quick summary: $INPUT" "cheapest" "step2.json"
fi

# Step 3: Generate report
echo "Step 3: Report generation..."
run_with_retry "Summarize findings" "cheapest" "final.json"

echo "Pipeline complete!"
```

## Make Integration

```makefile
# Makefile

ORCHESTRATOR = python C:/Users/JRiel/prompt-engineering-system/scripts/model_orchestrator.py
STRATEGY ?= cheapest
MAX_COST ?= 0.01

.PHONY: analyze test help

analyze:
	@echo "Analyzing code..."
	@$(ORCHESTRATOR) \
		--prompt "Analyze this code: $$(cat main.py)" \
		--strategy $(STRATEGY) \
		--max-cost $(MAX_COST) \
		--output analysis.json
	@echo "Analysis complete. See analysis.json"

review:
	@echo "Reviewing pull request..."
	@$(ORCHESTRATOR) \
		--prompt "Review these changes: $$(git diff)" \
		--strategy fallback \
		--max-cost 0.05 \
		--output review.json

docs:
	@echo "Generating documentation..."
	@$(ORCHESTRATOR) \
		--prompt "Generate docs for: $$(cat *.py)" \
		--strategy ensemble \
		--ensemble-size 2 \
		--output docs.json

test:
	@echo "Running orchestrator tests..."
	@$(ORCHESTRATOR) --test

help:
	@$(ORCHESTRATOR) --help
```

## GitHub Actions Integration

```yaml
# .github/workflows/ai-review.yml
name: AI Code Review

on:
  pull_request:
    types: [opened, synchronize]

jobs:
  review:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2

      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.9'

      - name: Install dependencies
        run: |
          pip install -r requirements.txt

      - name: Run AI Review
        run: |
          git diff origin/main...HEAD > changes.diff

          python scripts/model_orchestrator.py \
            --prompt "Review these code changes: $(cat changes.diff)" \
            --strategy fallback \
            --max-cost 0.10 \
            --output review.json

      - name: Post Comment
        run: |
          REVIEW=$(jq -r '.response' review.json)
          COST=$(jq -r '.cost' review.json)
          MODEL=$(jq -r '.model_used' review.json)

          gh pr comment ${{ github.event.pull_request.number }} \
            --body "## AI Code Review

          $REVIEW

          ---
          *Reviewed by: $MODEL | Cost: \$$COST*"
```

## Python Class Wrapper

```python
#!/usr/bin/env python3
"""
ModelOrchestrator wrapper class for easier integration
"""
import sys
sys.path.insert(0, 'C:/Users/JRiel/prompt-engineering-system/scripts')

from model_orchestrator import run_orchestration
from decimal import Decimal
from typing import Optional, List, Dict

class ModelOrchestrator:
    """Convenience wrapper for model orchestration."""

    def __init__(self, default_strategy: str = "cheapest",
                 max_cost_per_query: float = 0.01,
                 verbose: bool = False):
        self.default_strategy = default_strategy
        self.max_cost = max_cost_per_query
        self.verbose = verbose
        self.history = []

    def query(self, prompt: str, strategy: Optional[str] = None,
              max_cost: Optional[float] = None) -> Dict:
        """Execute a query with the orchestrator."""
        strategy = strategy or self.default_strategy
        max_cost = max_cost or self.max_cost

        result = run_orchestration(
            prompt=prompt,
            strategy=strategy,
            max_cost=max_cost,
            verbose=self.verbose
        )

        # Store in history
        self.history.append({
            'prompt': prompt[:100] + '...',
            'model': result.model_used,
            'cost': float(result.cost),
            'confidence': result.confidence,
            'strategy': strategy
        })

        return {
            'response': result.response,
            'model': result.model_used,
            'cost': float(result.cost),
            'confidence': result.confidence,
            'latency': result.latency,
            'metadata': result.metadata
        }

    def cheapest(self, prompt: str) -> Dict:
        """Route to cheapest capable model."""
        return self.query(prompt, strategy="cheapest")

    def fallback(self, prompt: str) -> Dict:
        """Use fallback chain."""
        return self.query(prompt, strategy="fallback")

    def ensemble(self, prompt: str, size: int = 3) -> Dict:
        """Use ensemble voting."""
        return self.query(prompt, strategy="ensemble")

    def get_total_cost(self) -> float:
        """Get total cost across all queries."""
        return sum(q['cost'] for q in self.history)

    def get_stats(self) -> Dict:
        """Get usage statistics."""
        if not self.history:
            return {'queries': 0, 'total_cost': 0, 'avg_cost': 0}

        return {
            'queries': len(self.history),
            'total_cost': self.get_total_cost(),
            'avg_cost': self.get_total_cost() / len(self.history),
            'models_used': list(set(q['model'] for q in self.history)),
            'strategies_used': list(set(q['strategy'] for q in self.history))
        }

# Usage Example
if __name__ == "__main__":
    orchestrator = ModelOrchestrator(verbose=True)

    # Simple queries
    result = orchestrator.cheapest("What is Kubernetes?")
    print(f"Response: {result['response']}")

    # Complex queries
    result = orchestrator.fallback("Design a microservices architecture")
    print(f"Model: {result['model']}, Confidence: {result['confidence']}")

    # Important decisions
    result = orchestrator.ensemble("Should I use PostgreSQL or MongoDB?")
    print(f"Cost: ${result['cost']:.6f}")

    # Get statistics
    stats = orchestrator.get_stats()
    print(f"\nStats: {stats}")
```

## FastAPI Integration

```python
#!/usr/bin/env python3
"""
FastAPI server with model orchestration
"""
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import sys
sys.path.insert(0, 'C:/Users/JRiel/prompt-engineering-system/scripts')

from model_orchestrator import run_orchestration

app = FastAPI(title="Model Orchestrator API")

class QueryRequest(BaseModel):
    prompt: str
    strategy: str = "cheapest"
    max_cost: float = 0.01
    ensemble_size: int = 3

class QueryResponse(BaseModel):
    response: str
    model_used: str
    cost: float
    confidence: float
    latency: float
    strategy: str

@app.post("/query", response_model=QueryResponse)
async def query(request: QueryRequest):
    """Execute a query with model orchestration."""
    try:
        result = run_orchestration(
            prompt=request.prompt,
            strategy=request.strategy,
            max_cost=request.max_cost,
            ensemble_size=request.ensemble_size
        )

        return QueryResponse(
            response=result.response,
            model_used=result.model_used,
            cost=float(result.cost),
            confidence=result.confidence,
            latency=result.latency,
            strategy=result.strategy
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/models")
async def list_models():
    """List available models."""
    from model_orchestrator import MODEL_REGISTRY
    return {
        name: {
            "provider": model.provider.value,
            "input_cost": float(model.cost_per_1k_input_tokens),
            "output_cost": float(model.cost_per_1k_output_tokens),
            "capabilities": [c.value for c in model.capabilities]
        }
        for name, model in MODEL_REGISTRY.items()
    }

# Run with: uvicorn api:app --reload
```

## Cost Monitoring Script

```python
#!/usr/bin/env python3
"""
Monitor orchestration costs and alert if budget exceeded
"""
import sys
sys.path.insert(0, 'C:/Users/JRiel/prompt-engineering-system/scripts')

from cost_tracker import get_db_connection
from datetime import datetime, timedelta

def check_daily_cost(budget: float = 1.00):
    """Check if daily orchestration cost exceeds budget."""
    conn = get_db_connection()
    cursor = conn.cursor()

    today = datetime.now().replace(hour=0, minute=0, second=0)

    cursor.execute("""
        SELECT SUM(total_cost) as daily_cost
        FROM usage_log
        WHERE category = 'orchestration'
          AND timestamp >= ?
    """, (today.isoformat(),))

    result = cursor.fetchone()
    daily_cost = result['daily_cost'] or 0

    conn.close()

    if daily_cost > budget:
        print(f"WARNING: Daily cost (${daily_cost:.2f}) exceeds budget (${budget:.2f})")
        return False
    else:
        print(f"Daily cost: ${daily_cost:.2f} / ${budget:.2f}")
        return True

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--budget", type=float, default=1.00)
    args = parser.parse_args()

    if not check_daily_cost(args.budget):
        sys.exit(1)
```

## Summary

The Model Orchestrator can be integrated into:
- Python applications (direct import)
- Bash scripts (CLI interface)
- CI/CD pipelines (GitHub Actions, etc.)
- Web APIs (FastAPI, Flask)
- Build systems (Make, CMake)
- Monitoring systems (cost tracking)

**Key Integration Points**:
1. Import functions directly in Python
2. Use CLI for scripts and pipelines
3. Monitor costs with cost_tracker.py
4. Export JSON for further processing
5. Build custom wrappers for your use case

**Best Practices**:
- Set max-cost limits in production
- Use fallback strategy for reliability
- Monitor costs regularly
- Cache results when possible
- Start with cheapest, escalate as needed
