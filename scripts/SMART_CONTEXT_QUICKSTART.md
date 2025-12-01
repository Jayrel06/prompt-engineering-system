# Smart Context Selection - Quick Start

## TL;DR

Smart context selection automatically finds and loads the most relevant context for your task while respecting token budgets.

```bash
# Basic usage
python scripts/smart_context.py --task "Design a new workflow"

# With token limit
python scripts/smart_context.py --task "Debug API issues" --max-tokens 4000

# Top 5 most relevant
python scripts/smart_context.py --task "Write docs" --top-n 5

# Include git status and recent files
python scripts/smart_context.py --task "Continue dev" --include-dynamic
```

## Quick Install

```bash
# Minimal (keyword matching only)
# No installation needed - uses stdlib only

# Recommended (semantic similarity)
pip install sentence-transformers

# Optimal (accurate token counting)
pip install sentence-transformers tiktoken

# Full (all features)
pip install -r scripts/requirements.txt
```

## Common Use Cases

### 1. Get Context for a New Task

```bash
python scripts/smart_context.py \
  --task "Implement OAuth2 authentication for the API" \
  --max-tokens 5000 \
  --boost-category technical=0.5
```

### 2. Continue Yesterday's Work

```bash
python scripts/smart_context.py \
  --task "Continue implementing the email processing feature" \
  --include-dynamic \
  --top-n 5
```

### 3. Planning Session

```bash
python scripts/smart_context.py \
  --task "Plan Q1 product roadmap" \
  --boost-category identity=0.4 \
  --boost-category business=0.3 \
  --max-tokens 6000
```

### 4. Debugging

```bash
python scripts/smart_context.py \
  --task "Debug webhook timeout issues in n8n" \
  --boost-category technical=0.6 \
  --top-n 3 \
  --show-scores
```

### 5. Export for Later

```bash
python scripts/smart_context.py \
  --task "Refactor authentication module" \
  --max-tokens 8000 \
  --output context_for_task.md
```

## Understanding the Output

### Standard Output Format

```markdown
# Smart Context Selection

**Task:** Your task here
**Context Selected:** 5 chunks, ~3500 tokens

## Relevant Context

### 1. technical/infrastructure-inventory.md
[Most relevant file content...]

### 2. frameworks/technical/architecture-design.md
[Second most relevant file content...]
```

### With --show-scores

```markdown
### 1. technical/api-integration.md (score: 0.856, tokens: 1250)
[Content with quality metrics...]
```

### With --include-dynamic

```markdown
## Dynamic Context

### Git Status
```
M  scripts/smart_context.py
A  docs/new_feature.md
```

### Recent Commits
```
abc1234 Add authentication
def5678 Update docs
```
```

## Key Parameters Explained

### --max-tokens
**Purpose:** Control total context size
**Default:** 8000
**Use when:** API costs matter, strict context window limits

**Guidelines:**
- Small task: 2000-4000
- Medium task: 4000-6000
- Large task: 6000-10000

### --top-n
**Purpose:** Limit number of files regardless of size
**Default:** None (use all that fit)
**Use when:** You want consistent file count, quality over quantity

**Guidelines:**
- Focused task: 3-5 files
- General task: 8-12 files
- Comprehensive: 15-20 files

### --min-score
**Purpose:** Filter out low-relevance content
**Default:** 0.1
**Range:** 0.0 to 1.0

**Guidelines:**
- 0.05: Include almost everything
- 0.1: Reasonable minimum (default)
- 0.2: Only relevant content
- 0.5: Only highly relevant content

### --boost-category
**Purpose:** Increase relevance of specific categories
**Format:** `category=boost_value`

**Examples:**
```bash
--boost-category technical=0.5        # 50% boost
--boost-category identity=0.3         # 30% boost
--boost-category framework/planning=0.4
```

**Available Categories:**
- `identity` - Core values, communication style
- `technical` - Infrastructure, tools, patterns
- `business` - Service offerings, markets
- `framework` - Thinking frameworks
- `template` - Document templates

## Command Cheat Sheet

```bash
# Most common patterns

# General task with semantic search
python scripts/smart_context.py --task "YOUR_TASK"

# Strict token budget
python scripts/smart_context.py --task "YOUR_TASK" --max-tokens 4000

# Technical work
python scripts/smart_context.py \
  --task "YOUR_TASK" \
  --boost-category technical=0.5 \
  --max-tokens 5000

# Planning work
python scripts/smart_context.py \
  --task "YOUR_TASK" \
  --boost-category identity=0.4 \
  --boost-category business=0.3

# Continue work (with git context)
python scripts/smart_context.py \
  --task "YOUR_TASK" \
  --include-dynamic \
  --top-n 5

# Export to file
python scripts/smart_context.py \
  --task "YOUR_TASK" \
  --output context.md

# Debug with scores
python scripts/smart_context.py \
  --task "YOUR_TASK" \
  --show-scores \
  --verbose
```

## Performance Tips

### 1. Use Cache (Enabled by Default)
First run: ~7-13 seconds
Cached runs: ~2-3 seconds

### 2. Clear Old Cache Periodically
```bash
python scripts/smart_context.py --clear-cache --cache-days 7
```

### 3. Disable Cache for One-Time Queries
```bash
python scripts/smart_context.py --task "Quick lookup" --no-cache
```

## Troubleshooting

### "sentence-transformers not available"
**Fix:** `pip install sentence-transformers`
**Impact:** Still works, but uses keyword matching (less accurate)

### Too much/too little context selected
**Fix:**
- Adjust `--min-score` (lower = more content)
- Adjust `--max-tokens` (higher = more content)
- Use `--top-n` for fixed count

### Slow first run
**Normal:** Loading model + computing embeddings
**Solution:** Keep cache enabled (default)

### No relevant context found
**Fix:**
- Lower `--min-score` to 0.05
- Use broader task description
- Check that context files exist

## Examples

### Run Interactive Examples
```bash
# Run all examples
python scripts/smart_context_example.py all

# Run specific example
python scripts/smart_context_example.py 1

# Run with menu
python scripts/smart_context_example.py
```

### Test Suite
```bash
# Run tests
python scripts/test_smart_context.py

# Should show: Ran 31 tests ... OK
```

## Integration

### With context-loader.py

**Option 1: Replace context-loader**
```bash
# Old way
python scripts/context-loader.py --mode technical --task "Debug API"

# New way
python scripts/smart_context.py --task "Debug API" --boost-category technical=0.5
```

**Option 2: Use both (hybrid)**
```bash
# Get baseline from context-loader
python scripts/context-loader.py --mode technical --task "Debug" > base.md

# Add smart context
python scripts/smart_context.py --task "Debug API OAuth2" --top-n 3 > smart.md

# Combine manually
cat base.md smart.md > final.md
```

### In Python Scripts

```python
from smart_context import (
    SemanticScorer, discover_context_files,
    score_relevance, select_context
)

scorer = SemanticScorer()
chunks = discover_context_files()
scored = score_relevance("YOUR_TASK", chunks, scorer)
selected = select_context(scored, max_tokens=5000)

for chunk in selected:
    print(f"{chunk.source}: {chunk.content[:100]}...")
```

## Next Steps

1. **Try it:** `python scripts/smart_context.py --task "Your task here"`
2. **Run examples:** `python scripts/smart_context_example.py all`
3. **Read full guide:** See `SMART_CONTEXT_INTEGRATION.md`
4. **Run tests:** `python scripts/test_smart_context.py`

## Pro Tips

1. **Combine --max-tokens and --top-n** for best results
2. **Use --boost-category** when you know the domain
3. **Use --include-dynamic** for continuing work
4. **Use --show-scores** to tune --min-score
5. **Use --verbose** to understand what's happening
6. **Keep cache enabled** for better performance

## Quick Reference

| Goal | Command |
|------|---------|
| Basic | `--task "..."` |
| Limit tokens | `--max-tokens 4000` |
| Limit files | `--top-n 5` |
| Boost category | `--boost-category technical=0.5` |
| Git context | `--include-dynamic` |
| See scores | `--show-scores` |
| Save to file | `--output file.md` |
| Debug | `--verbose --show-scores` |

---

**Need help?** Check the full documentation: `SMART_CONTEXT_INTEGRATION.md`

**Report issues:** Run with `--verbose` and check test suite
