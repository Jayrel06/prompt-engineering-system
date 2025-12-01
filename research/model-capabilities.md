# Model Capabilities Reference

## Claude Models

### Claude Opus 4 (claude-opus-4-20250514)
- **Best For:** Deep analysis, nuanced thinking, complex reasoning
- **Context:** 200K tokens
- **Strengths:**
  - Most capable reasoning
  - Best for ambiguous problems
  - Strongest coding abilities
  - Most reliable for complex tasks
- **Cost:** Highest
- **Use When:**
  - Strategic planning
  - Complex architecture decisions
  - Nuanced analysis
  - Tasks requiring extended thinking

### Claude Sonnet 4 (claude-sonnet-4-20250514)
- **Best For:** Balanced performance, fast iteration
- **Context:** 200K tokens
- **Strengths:**
  - Fast response times
  - Good quality for most tasks
  - Cost-effective
  - Reliable coding
- **Cost:** Medium
- **Use When:**
  - Day-to-day development
  - Code generation
  - Content creation
  - Most standard tasks

### Claude Haiku 3.5 (claude-haiku-4-5-20251001)
- **Best For:** Simple tasks, high volume, classification
- **Context:** 200K tokens
- **Strengths:**
  - Very fast
  - Very cheap
  - Good for simple tasks
  - Great for preprocessing
- **Cost:** Lowest
- **Use When:**
  - Intent classification
  - Simple transformations
  - High-volume tasks
  - Preprocessing/routing

---

## Model Selection Matrix

| Task Type | Primary Model | Fallback |
|-----------|---------------|----------|
| Strategic Planning | Opus | Sonnet |
| Code Generation | Sonnet | Opus |
| Code Review | Sonnet | Opus |
| Content Writing | Sonnet | Haiku |
| Classification | Haiku | Sonnet |
| Data Transformation | Haiku | Sonnet |
| Complex Analysis | Opus | Sonnet |
| Quick Questions | Haiku | Sonnet |
| Voice AI Prompts | Sonnet | Opus |

---

## Routing Logic

```python
def select_model(task_type: str, complexity: str) -> str:
    """Select appropriate model based on task and complexity."""

    # High complexity always uses Opus
    if complexity == "high":
        return "claude-opus"

    # Task-specific routing
    routing = {
        "planning": "claude-opus",
        "analysis": "claude-sonnet",
        "creation": "claude-sonnet",
        "technical": "claude-sonnet",
        "communication": "claude-sonnet",
        "classification": "claude-haiku",
        "transformation": "claude-haiku",
        "quick": "claude-haiku"
    }

    return routing.get(task_type, "claude-sonnet")
```

---

## Cost Optimization

### Token Pricing (Approximate)
| Model | Input (per 1M) | Output (per 1M) |
|-------|----------------|-----------------|
| Opus | $15 | $75 |
| Sonnet | $3 | $15 |
| Haiku | $0.25 | $1.25 |

### Optimization Strategies
1. **Use Haiku for preprocessing** - Classification, extraction, routing
2. **Cache common contexts** - Reduce input tokens
3. **Summarize long documents** - Before sending to expensive models
4. **Batch similar requests** - Amortize context costs
5. **Set appropriate max_tokens** - Don't request more than needed
