# Smart Context Integration Guide

## Overview

The Smart Context Selection System (`smart_context.py`) intelligently selects and compresses context based on semantic relevance to your task, optimizing token usage while preserving the most important information.

## Key Features

### 1. Semantic Relevance Scoring
- Uses sentence-transformers for semantic similarity (when available)
- Falls back to keyword matching for lightweight operation
- Scores all context files against your task (0-1 scale)

### 2. Token Budget Management
- Accurate token counting with tiktoken (or estimation)
- Respects maximum token limits
- Selects highest-value context within budget

### 3. Context Compression
- Extracts key sections (headings, first paragraphs)
- Removes code blocks and verbose content
- Truncates with [...] markers when needed

### 4. Dynamic Context
- Git status and recent commits
- Recently modified files
- Current branch information
- System metadata

### 5. Embedding Cache
- Caches embeddings to disk for performance
- Automatic cache invalidation (7-day default)
- Supports manual cache clearing

## Installation

### Required Dependencies
```bash
# Basic functionality (keyword matching)
# No additional dependencies needed

# For semantic similarity (recommended)
pip install sentence-transformers

# For accurate token counting
pip install tiktoken
```

### Optional Dependencies
```bash
# For full functionality
pip install -r scripts/requirements.txt
```

## Basic Usage

### Simple Task Context Selection
```bash
python scripts/smart_context.py \
  --task "Design a new n8n workflow for email processing"
```

### With Token Budget
```bash
python scripts/smart_context.py \
  --task "Debug authentication issues" \
  --max-tokens 4000
```

### Limit to Top N Most Relevant
```bash
python scripts/smart_context.py \
  --task "Write technical documentation" \
  --top-n 5
```

### Include Dynamic Context
```bash
python scripts/smart_context.py \
  --task "Continue development from yesterday" \
  --include-dynamic
```

### Boost Specific Categories
```bash
python scripts/smart_context.py \
  --task "Fix API integration bug" \
  --boost-category technical=0.5 \
  --boost-category infrastructure=0.3
```

### Show Relevance Scores
```bash
python scripts/smart_context.py \
  --task "Plan Q1 strategy" \
  --show-scores
```

### Export to File
```bash
python scripts/smart_context.py \
  --task "Build new feature" \
  -o context_output.md
```

## Integration with context-loader.py

### Using Both Together

The smart context system complements the existing context-loader:

**context-loader.py**: Rule-based context selection by mode
- Good for: Consistent, predictable context sets
- Uses: Predefined modes (planning, technical, analysis, etc.)

**smart_context.py**: AI-driven context selection by relevance
- Good for: Dynamic, task-specific context optimization
- Uses: Semantic similarity and token budgets

### Hybrid Approach

```bash
# 1. Use context-loader for baseline context
python scripts/context-loader.py \
  --mode technical \
  --task "Debug API integration" \
  --output base_context.md

# 2. Use smart_context for additional relevant context
python scripts/smart_context.py \
  --task "Debug API integration with OAuth2" \
  --max-tokens 3000 \
  --output smart_context.md

# 3. Combine both (manually or via script)
```

## Advanced Usage

### Custom Scoring Models

```bash
# Use different sentence-transformer model
python scripts/smart_context.py \
  --task "Analyze code architecture" \
  --model "paraphrase-MiniLM-L6-v2"
```

### Cache Management

```bash
# Clear cache older than 3 days
python scripts/smart_context.py --clear-cache --cache-days 3

# Disable caching for one-time use
python scripts/smart_context.py \
  --task "Quick lookup" \
  --no-cache
```

### Minimum Relevance Threshold

```bash
# Only include highly relevant context (score >= 0.5)
python scripts/smart_context.py \
  --task "Implement new feature" \
  --min-score 0.5
```

## Programmatic Usage

### Python Integration

```python
from smart_context import (
    SemanticScorer,
    discover_context_files,
    score_relevance,
    select_context,
    get_dynamic_context,
    format_output
)

# Initialize scorer
scorer = SemanticScorer(model_name="all-MiniLM-L6-v2", use_cache=True)

# Discover available context
chunks = discover_context_files()

# Score by relevance to task
task = "Design a new automation workflow"
boost_categories = {"technical": 0.3, "framework": 0.2}
scored = score_relevance(task, chunks, scorer, boost_categories)

# Select best context within budget
selected = select_context(
    scored,
    max_tokens=6000,
    top_n=10,
    min_score=0.15
)

# Get dynamic context
dynamic = get_dynamic_context()

# Format for output
output = format_output(task, selected, dynamic, include_scores=True)
print(output)
```

### Custom Context Sources

```python
from smart_context import ContextChunk, estimate_tokens

# Create custom context chunks
custom_chunks = [
    ContextChunk(
        source="api_docs.md",
        content=open("api_docs.md").read(),
        category="documentation",
        metadata={"type": "api", "version": "2.0"}
    ),
    ContextChunk(
        source="recent_changes.txt",
        content="Recent updates...",
        category="dynamic"
    )
]

# Add to discovered chunks and process
all_chunks = discover_context_files() + custom_chunks
scored = score_relevance(task, all_chunks, scorer)
selected = select_context(scored, max_tokens=5000)
```

## Output Format

### Standard Output Structure

```markdown
# Smart Context Selection

**Task:** Your task description here

**Context Selected:** 5 chunks, ~3500 tokens

## Dynamic Context (if --include-dynamic)

### Git Status
```
M  scripts/smart_context.py
A  scripts/test_smart_context.py
```

### Recent Commits
```
abc1234 Add smart context selection
def5678 Update documentation
```

---

## Relevant Context

### 1. technical/infrastructure-inventory.md

[Content of most relevant file...]

### 2. frameworks/technical/architecture-design.md

[Content of second most relevant file...]
```

### With Scores (--show-scores)

```markdown
### 1. technical/api-integration.md (score: 0.856, tokens: 1250)

[Content...]
```

## Performance Optimization

### Caching Strategy

The embedding cache significantly improves performance:

**First Run** (no cache):
- Load model: ~2-3 seconds
- Embed 50 files: ~5-10 seconds
- Total: ~7-13 seconds

**Subsequent Runs** (with cache):
- Load model: ~2-3 seconds
- Embed task only: ~0.1 seconds
- Retrieve cached embeddings: <0.1 seconds
- Total: ~2-3 seconds

### Cache Location

Cache files are stored in:
```
scripts/__pycache__/embeddings_cache/
├── embeddings.pkl      # Binary embedding data
└── metadata.json       # Cache metadata and timestamps
```

### When to Clear Cache

- After major content updates
- When changing embedding models
- To free disk space (cache can grow to ~10-50 MB)
- Automatically via `--cache-days` parameter

## Best Practices

### 1. Token Budget Guidelines

- **Short prompts** (< 4K context): `--max-tokens 2000`
- **Medium prompts** (4K-8K context): `--max-tokens 4000`
- **Long prompts** (8K+ context): `--max-tokens 8000`

Remember to leave room for:
- Your actual task/question
- Model's response
- Dynamic context (if enabled)

### 2. Top-N vs Token Budget

Use `--top-n` when:
- You want consistent number of files
- Quality > quantity
- You know roughly how many relevant files exist

Use `--max-tokens` when:
- You have strict token limits (API costs, context windows)
- Files vary widely in size
- You want to maximize information density

**Best:** Use both together:
```bash
--max-tokens 6000 --top-n 15
```

### 3. Category Boosting

Boost categories when you know what type of context is most relevant:

```bash
# For technical implementation tasks
--boost-category technical=0.5 --boost-category framework=0.3

# For planning tasks
--boost-category identity=0.4 --boost-category business=0.3

# For communication tasks
--boost-category identity/communication=0.5
```

Boost values:
- `0.2-0.3`: Slight preference
- `0.4-0.5`: Strong preference
- `0.6-1.0`: Very strong preference (use sparingly)

### 4. Minimum Score Tuning

- `--min-score 0.05`: Include almost everything (default: 0.1)
- `--min-score 0.2`: Only moderately relevant content
- `--min-score 0.3`: Only highly relevant content
- `--min-score 0.5`: Only extremely relevant content

Start with default (0.1) and increase if getting too much irrelevant context.

## Troubleshooting

### "sentence-transformers not available"

**Issue:** Script falls back to keyword matching

**Solutions:**
```bash
# Install sentence-transformers
pip install sentence-transformers

# Or install all dependencies
pip install -r scripts/requirements.txt
```

**Impact:** Keyword matching still works but less accurate than semantic similarity.

### Slow First Run

**Issue:** First run takes 10+ seconds

**Cause:** Loading sentence-transformer model and computing embeddings

**Solutions:**
- Keep cache enabled (default)
- Model is cached after first load
- Embeddings cached after first computation

### Cache Growing Too Large

**Issue:** Cache directory exceeds 100 MB

**Solutions:**
```bash
# Clear old entries
python scripts/smart_context.py --clear-cache --cache-days 3

# Or disable cache for specific runs
python scripts/smart_context.py --task "..." --no-cache
```

### No Context Selected

**Issue:** Output shows "0 chunks selected"

**Possible Causes:**
1. `--min-score` too high
2. `--max-tokens` too low
3. Task too different from available content

**Solutions:**
```bash
# Lower minimum score
--min-score 0.05

# Increase token budget
--max-tokens 10000

# Use more general task description
```

### Token Count Inaccurate

**Issue:** Token estimates don't match actual usage

**Cause:** Using fallback estimation (4 chars = 1 token)

**Solution:**
```bash
pip install tiktoken
```

## Integration Examples

### Shell Script Integration

```bash
#!/bin/bash
# smart_prompt.sh - Generate context-enriched prompt

TASK="$1"

if [ -z "$TASK" ]; then
    echo "Usage: $0 '<task description>'"
    exit 1
fi

# Select smart context
python scripts/smart_context.py \
    --task "$TASK" \
    --max-tokens 6000 \
    --top-n 10 \
    --include-dynamic \
    --output /tmp/smart_context.md

# Combine with your prompt
{
    echo "# Context-Enriched Prompt"
    echo ""
    cat /tmp/smart_context.md
    echo ""
    echo "---"
    echo ""
    echo "# Your Response"
    echo ""
} | pbcopy  # or xclip on Linux

echo "Context-enriched prompt copied to clipboard!"
```

### Python Wrapper

```python
#!/usr/bin/env python3
"""
smart_prompt.py - Generate optimal context for any task
"""

import subprocess
import sys

def generate_smart_prompt(task: str, max_tokens: int = 6000) -> str:
    """Generate context-enriched prompt for task."""
    result = subprocess.run(
        [
            'python', 'scripts/smart_context.py',
            '--task', task,
            '--max-tokens', str(max_tokens),
            '--include-dynamic'
        ],
        capture_output=True,
        text=True
    )

    return result.stdout

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python smart_prompt.py '<task>'")
        sys.exit(1)

    task = ' '.join(sys.argv[1:])
    context = generate_smart_prompt(task)
    print(context)
```

### API Integration

```python
from typing import List, Dict
import openai
from smart_context import (
    SemanticScorer, discover_context_files,
    score_relevance, select_context
)

def get_ai_response_with_smart_context(
    task: str,
    max_context_tokens: int = 6000
) -> str:
    """Get AI response with automatically selected relevant context."""

    # Initialize
    scorer = SemanticScorer()
    chunks = discover_context_files()

    # Select relevant context
    scored = score_relevance(task, chunks, scorer)
    selected = select_context(scored, max_tokens=max_context_tokens)

    # Build context string
    context_parts = []
    for chunk in selected:
        context_parts.append(f"## {chunk.source}")
        context_parts.append(chunk.content)
        context_parts.append("")

    full_context = "\n".join(context_parts)

    # Call AI with context
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {
                "role": "system",
                "content": "You are an AI assistant with access to relevant context."
            },
            {
                "role": "user",
                "content": f"{full_context}\n\n---\n\nTask: {task}"
            }
        ]
    )

    return response.choices[0].message.content

# Usage
response = get_ai_response_with_smart_context(
    "How should I structure my n8n workflow for email processing?"
)
print(response)
```

## Command Reference

### All CLI Options

```
--task TEXT              Task description (required)
--max-tokens INT         Maximum total tokens (default: 8000)
--top-n INT             Limit to top N chunks
--min-score FLOAT       Minimum relevance score 0-1 (default: 0.1)
--include-dynamic       Include dynamic context (git, files, etc.)
--boost-category TEXT   Boost category (format: category=boost)
--show-scores          Show relevance scores in output
--output PATH          Output file (default: stdout)
--no-cache             Disable embedding cache
--clear-cache          Clear old cache entries and exit
--cache-days INT       Cache retention days (default: 7)
--model TEXT           Sentence transformer model
--verbose, -v          Verbose output
```

## Comparison: context-loader vs smart_context

| Feature | context-loader.py | smart_context.py |
|---------|------------------|------------------|
| **Selection Method** | Rule-based (modes) | AI-based (relevance) |
| **Consistency** | High (same mode = same files) | Variable (task-dependent) |
| **Token Awareness** | No | Yes (strict budgets) |
| **Dynamic Context** | No | Yes (git, files, etc.) |
| **Compression** | No | Yes (automatic) |
| **Semantic Search** | No | Yes (when available) |
| **Setup Complexity** | Low | Medium (optional deps) |
| **Best For** | Structured workflows | Ad-hoc, varied tasks |

**Recommendation:** Use context-loader for consistent, workflow-based prompts. Use smart_context for dynamic, AI-driven optimization. Combine both for maximum flexibility.

## Future Enhancements

Planned improvements:

1. **Integration with Vector DB** - Leverage existing Qdrant setup
2. **Multi-chunk Summarization** - Better compression using AI
3. **Context Dependency Graph** - Understand file relationships
4. **Auto-mode Detection** - Classify task and suggest boost categories
5. **Usage Analytics** - Track which context is most useful
6. **Streaming Selection** - Progressive context loading for large sets

## Support

For issues or questions:

1. Check test suite: `python scripts/test_smart_context.py`
2. Run with `--verbose` for debug output
3. Review this integration guide
4. Check existing context-loader.py documentation

## License

Part of the Prompt Engineering System. Same license as parent project.
