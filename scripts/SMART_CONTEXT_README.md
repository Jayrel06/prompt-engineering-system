# Smart Context Selection System

Production-ready AI-driven context selection for the Prompt Engineering System.

## Overview

The Smart Context Selection System intelligently selects and optimizes context for any task using semantic similarity, token budgets, and dynamic environment data. It replaces or complements the traditional rule-based context-loader with AI-powered relevance scoring.

### Key Features

- **Semantic Relevance Scoring** - Uses sentence-transformers for accurate similarity matching
- **Token Budget Management** - Respects strict token limits with accurate counting
- **Context Compression** - Automatically summarizes long content to fit budgets
- **Dynamic Context** - Includes git status, recent changes, system metadata
- **Embedding Cache** - Persistent cache for fast repeated queries
- **Category Boosting** - Prioritize specific content categories
- **Fallback Support** - Works without dependencies using keyword matching

## Quick Start

### Installation

```bash
# Minimal (keyword matching only)
# No installation needed

# Recommended (semantic similarity)
pip install sentence-transformers

# Optimal (accurate token counting)
pip install sentence-transformers tiktoken

# Full features
pip install -r scripts/requirements.txt
```

### Basic Usage

```bash
# Simple task
python scripts/smart_context.py --task "Design a new workflow"

# With token budget
python scripts/smart_context.py --task "Debug API" --max-tokens 4000

# Top 5 most relevant
python scripts/smart_context.py --task "Write docs" --top-n 5

# Include dynamic context
python scripts/smart_context.py --task "Continue dev" --include-dynamic
```

## Components

### 1. smart_context.py
Main script for AI-driven context selection.

**Features:**
- Semantic similarity scoring
- Token budget management
- Context compression
- Dynamic context gathering
- Embedding cache

**Usage:** See [SMART_CONTEXT_QUICKSTART.md](SMART_CONTEXT_QUICKSTART.md)

### 2. smart_prompt.py
Unified interface combining mode-based and smart selection.

**Features:**
- Three strategies: smart_only, mode_only, hybrid
- Combines context-loader.py with smart_context.py
- Flexible output formatting

**Example:**
```bash
# Smart only (default)
python scripts/smart_prompt.py --task "Implement OAuth2"

# Hybrid approach
python scripts/smart_prompt.py \
  --task "Build new feature" \
  --strategy hybrid \
  --mode technical \
  --boost technical=0.5
```

### 3. test_smart_context.py
Comprehensive test suite with 31 tests.

**Run tests:**
```bash
python scripts/test_smart_context.py
```

**Test coverage:**
- Token estimation
- Keyword similarity
- Context chunks
- Context selection
- Compression
- Caching
- Dynamic context
- End-to-end pipeline

### 4. smart_context_example.py
Interactive examples demonstrating all features.

**Run examples:**
```bash
# Interactive menu
python scripts/smart_context_example.py

# Run all examples
python scripts/smart_context_example.py all

# Run specific example
python scripts/smart_context_example.py 3
```

**Examples included:**
1. Basic usage
2. Token budget management
3. Category boosting
4. Dynamic context
5. Compression
6. Custom chunks
7. Similarity comparison
8. Cache performance
9. Full pipeline

## Architecture

### Data Flow

```
Task Description
      ↓
[Discover Context Files]
      ↓
[Semantic Scoring] ←→ [Embedding Cache]
      ↓
[Category Boosting]
      ↓
[Select by Relevance + Token Budget]
      ↓
[Compress if Needed]
      ↓
[Add Dynamic Context]
      ↓
Formatted Output
```

### Components

```
ContextChunk (dataclass)
├── source: str          # File path
├── content: str         # Actual content
├── relevance_score: float  # 0-1 similarity
├── token_count: int     # Estimated tokens
├── summary: str         # Compression note
├── category: str        # Content category
└── metadata: dict       # Additional info

SemanticScorer (class)
├── model: SentenceTransformer
├── cache: EmbeddingCache
├── get_embedding()
└── score_similarity()

EmbeddingCache (class)
├── cache: dict          # In-memory cache
├── metadata: dict       # Cache metadata
├── get()
├── set()
└── clear_old()
```

### Functions

**Core Functions:**
- `discover_context_files()` - Find all available context
- `score_relevance()` - Score chunks against task
- `select_context()` - Select best within budget
- `compress_context()` - Summarize long content
- `get_dynamic_context()` - Gather env data
- `format_output()` - Format for output

**Helper Functions:**
- `estimate_tokens()` - Count tokens (tiktoken or fallback)
- `keyword_similarity()` - Fallback similarity metric
- `load_context_file()` - Load file into chunk

## Usage Patterns

### Pattern 1: Simple Task Context

```bash
python scripts/smart_context.py \
  --task "Design email processing workflow" \
  --max-tokens 5000
```

**When to use:** Quick context for any task

### Pattern 2: Domain-Specific Task

```bash
python scripts/smart_context.py \
  --task "Debug API authentication" \
  --boost technical=0.5 \
  --boost infrastructure=0.3 \
  --max-tokens 4000
```

**When to use:** You know which context categories are relevant

### Pattern 3: Continue Previous Work

```bash
python scripts/smart_context.py \
  --task "Continue implementing feature X" \
  --include-dynamic \
  --top-n 5
```

**When to use:** Resuming work, need git context

### Pattern 4: Strict Budget

```bash
python scripts/smart_context.py \
  --task "Quick code review" \
  --max-tokens 2000 \
  --min-score 0.3
```

**When to use:** API cost limits, small context windows

### Pattern 5: Comprehensive Analysis

```bash
python scripts/smart_context.py \
  --task "Analyze system architecture" \
  --max-tokens 10000 \
  --min-score 0.05
```

**When to use:** Deep analysis, need broad context

### Pattern 6: Hybrid Approach

```bash
python scripts/smart_prompt.py \
  --task "Plan new feature" \
  --strategy hybrid \
  --mode planning \
  --boost identity=0.4 \
  --include-dynamic
```

**When to use:** Best of both mode-based and smart selection

## Integration

### With context-loader.py

**Replace:**
```bash
# Old
python scripts/context-loader.py --mode technical --task "Debug"

# New
python scripts/smart_context.py --task "Debug" --boost technical=0.5
```

**Combine:**
```bash
# Use both
python scripts/smart_prompt.py \
  --strategy hybrid \
  --mode technical \
  --task "Debug API issues"
```

### In Python Scripts

```python
from smart_context import (
    SemanticScorer, discover_context_files,
    score_relevance, select_context
)

# Initialize
scorer = SemanticScorer()
chunks = discover_context_files()

# Score and select
scored = score_relevance("Your task", chunks, scorer)
selected = select_context(scored, max_tokens=5000)

# Use selected context
for chunk in selected:
    print(f"Using: {chunk.source}")
    # Process chunk.content
```

### With AI APIs

```python
import openai
from smart_context import *

def ask_with_context(question: str) -> str:
    # Get context
    scorer = SemanticScorer()
    chunks = discover_context_files()
    scored = score_relevance(question, chunks, scorer)
    selected = select_context(scored, max_tokens=4000)

    # Build prompt
    context = "\n\n".join([c.content for c in selected])

    # Ask AI
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": context},
            {"role": "user", "content": question}
        ]
    )

    return response.choices[0].message.content
```

## Configuration

### Environment Variables

None required. Optional:
- `SENTENCE_TRANSFORMERS_HOME` - Model cache location
- `TRANSFORMERS_CACHE` - Alternative cache location

### Cache Configuration

**Location:** `scripts/__pycache__/embeddings_cache/`

**Files:**
- `embeddings.pkl` - Cached embeddings
- `metadata.json` - Cache metadata

**Management:**
```bash
# Clear old cache (7+ days)
python scripts/smart_context.py --clear-cache

# Clear with custom retention
python scripts/smart_context.py --clear-cache --cache-days 3

# Disable cache
python scripts/smart_context.py --task "..." --no-cache
```

## Performance

### Benchmarks

**First run (cold cache):**
- Model loading: ~2-3s
- Embedding 50 files: ~5-10s
- Total: ~7-13s

**Subsequent runs (warm cache):**
- Model loading: ~2-3s
- Cache retrieval: <0.1s
- Total: ~2-3s

**Cache stats:**
- Size per file: ~1-2 KB
- Total for 100 files: ~100-200 KB
- Speedup: ~3-5x

### Optimization Tips

1. **Keep cache enabled** (default)
2. **Use --top-n** to limit processing
3. **Adjust --min-score** to filter early
4. **Clear old cache** periodically
5. **Use smaller model** if needed

## Troubleshooting

### Common Issues

**Issue:** "sentence-transformers not available"
- **Fix:** `pip install sentence-transformers`
- **Impact:** Falls back to keyword matching (works but less accurate)

**Issue:** Slow first run
- **Cause:** Loading model + computing embeddings
- **Fix:** Keep cache enabled (default)

**Issue:** No context selected
- **Causes:**
  - `--min-score` too high
  - Task too different from content
- **Fix:** Lower --min-score to 0.05, use broader task

**Issue:** Too much/little context
- **Fix:** Adjust --max-tokens, --top-n, or --min-score

**Issue:** Token count inaccurate
- **Fix:** `pip install tiktoken`

### Debug Mode

```bash
python scripts/smart_context.py \
  --task "..." \
  --verbose \
  --show-scores
```

Shows:
- Files discovered
- Scoring progress
- Selection details
- Token counts

## Documentation

### Quick Reference
- **[SMART_CONTEXT_QUICKSTART.md](SMART_CONTEXT_QUICKSTART.md)** - Get started in 5 minutes
- **[SMART_CONTEXT_INTEGRATION.md](SMART_CONTEXT_INTEGRATION.md)** - Full integration guide
- **[smart_context_example.py](smart_context_example.py)** - Interactive examples
- **[test_smart_context.py](test_smart_context.py)** - Test suite

### API Documentation

See docstrings in `smart_context.py` for:
- ContextChunk dataclass
- SemanticScorer class
- EmbeddingCache class
- All functions

## Comparison

### smart_context.py vs context-loader.py

| Feature | context-loader | smart_context |
|---------|---------------|---------------|
| Selection | Rule-based | AI-based |
| Consistency | High | Variable |
| Token aware | No | Yes |
| Dynamic | No | Yes |
| Compression | No | Yes |
| Setup | Simple | Medium |
| Best for | Workflows | Ad-hoc tasks |

**Recommendation:** Use smart_context.py for most tasks, context-loader.py for consistent workflows. Use smart_prompt.py --strategy hybrid for best of both.

## Development

### Running Tests

```bash
# All tests
python scripts/test_smart_context.py

# Verbose
python scripts/test_smart_context.py -v

# Specific test
python scripts/test_smart_context.py TestContextSelection
```

### Adding Features

1. Add code to `smart_context.py`
2. Add tests to `test_smart_context.py`
3. Add example to `smart_context_example.py`
4. Update documentation

### Code Structure

```
smart_context.py
├── Data Models
│   ├── ContextChunk
│   ├── EmbeddingCache
│   └── SemanticScorer
├── Core Functions
│   ├── discover_context_files()
│   ├── score_relevance()
│   ├── select_context()
│   └── compress_context()
├── Utilities
│   ├── estimate_tokens()
│   ├── keyword_similarity()
│   └── get_dynamic_context()
└── CLI
    └── main()
```

## Future Enhancements

### Planned Features

1. **Vector DB Integration** - Use existing Qdrant setup
2. **Multi-chunk Summarization** - AI-powered compression
3. **Context Dependencies** - Understand file relationships
4. **Auto-mode Detection** - Classify task type
5. **Usage Analytics** - Track effectiveness
6. **Streaming Selection** - Progressive loading

### Contributions

To contribute:
1. Fork repository
2. Add feature with tests
3. Update documentation
4. Submit pull request

## Support

### Getting Help

1. Check [SMART_CONTEXT_QUICKSTART.md](SMART_CONTEXT_QUICKSTART.md)
2. Run examples: `python scripts/smart_context_example.py`
3. Run with --verbose
4. Check test suite: `python scripts/test_smart_context.py`
5. Review [SMART_CONTEXT_INTEGRATION.md](SMART_CONTEXT_INTEGRATION.md)

### Reporting Issues

Include:
- Command used
- Output with --verbose
- Python version
- Installed packages: `pip list | grep -E "sentence|tiktoken"`

## License

Part of the Prompt Engineering System. Same license as parent project.

## Credits

**Author:** Built for the Prompt Engineering System
**Model:** Uses sentence-transformers (all-MiniLM-L6-v2)
**Token counting:** Uses tiktoken (OpenAI)

## Version

**Version:** 1.0.0
**Date:** 2024-12-01
**Status:** Production-ready

---

**Quick Links:**
- [Quick Start](SMART_CONTEXT_QUICKSTART.md)
- [Integration Guide](SMART_CONTEXT_INTEGRATION.md)
- [Examples](smart_context_example.py)
- [Tests](test_smart_context.py)
