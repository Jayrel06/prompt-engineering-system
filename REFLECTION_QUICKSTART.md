# Reflection System - Quick Start Guide

A comprehensive system for learning from your prompt engineering practice through automated analysis and structured reflection.

## What Was Created

### 1. Core Files

**scripts/reflection.py** (19KB)
- Automated reflection report generator
- Pattern analysis engine
- Learning comparison system
- Supports multiple output formats (markdown, JSON)

**frameworks/meta/weekly-reflection.md** (8.7KB)
- Comprehensive reflection framework
- Structured questions and prompts
- Best practices and tips
- Action item templates

**context/learnings/reflection-log.md** (6.5KB)
- Weekly reflection log template
- Includes first example entry
- Tracks metrics and action items

**docs/reflection-system.md** (12KB)
- Complete documentation
- Usage examples
- Troubleshooting guide
- Integration instructions

### 2. CLI Integration

Updated **scripts/prompt.sh** with new commands:
- `reflect [days]` - Generate reflection report
- `reflect-prompts` - Get reflection questions
- `analyze [days]` - Analyze patterns only

## Quick Start

### 1. Check System Status

```bash
cd /c/Users/JRiel/prompt-engineering-system
./scripts/prompt.sh status
```

Make sure Qdrant is running. If not:

```bash
cd infrastructure
docker-compose up -d qdrant
```

### 2. Capture Some Content

Before you can reflect, you need content in the database:

```bash
# Capture a prompt output
./scripts/prompt.sh capture output.txt --category output --tags successful,example

# Capture a template
./scripts/prompt.sh capture my-template.md --category template --tags reusable
```

### 3. Generate Your First Reflection

```bash
# Generate weekly reflection (last 7 days)
./scripts/prompt.sh reflect

# Or specify custom period
./scripts/prompt.sh reflect 14
```

This creates: `context/learnings/reflection-YYYY-MM-DD.md`

### 4. Review Reflection Prompts

```bash
./scripts/prompt.sh reflect-prompts
```

Use these questions to guide your manual reflection.

### 5. Analyze Patterns

```bash
# Get JSON analysis
./scripts/prompt.sh analyze 7
```

## Typical Weekly Workflow

### Friday End-of-Week (30 minutes)

1. **Generate automated report** (5 min)
   ```bash
   ./scripts/prompt.sh reflect
   ```

2. **Review the report** (10 min)
   - Open `context/learnings/reflection-YYYY-MM-DD.md`
   - Note patterns and insights
   - Identify action items

3. **Manual reflection** (10 min)
   - Use `frameworks/meta/weekly-reflection.md`
   - Answer key questions
   - Add context the automation missed

4. **Update learnings** (5 min)
   - Add to `context/learnings/what-works.md`
   - Add to `context/learnings/what-doesnt.md`
   - Update `context/learnings/reflection-log.md`

### Daily Quick Capture (2-5 minutes)

Throughout the week, capture outputs as you create them:

```bash
# After a successful prompt
./scripts/prompt.sh capture successful-output.md --category output --tags success,pattern-name

# After creating a template
./scripts/prompt.sh capture new-template.md --category template --tags workflow
```

## Command Reference

### Reflection Commands

```bash
# Generate reflection report (default: 7 days)
./scripts/prompt.sh reflect

# Generate for specific period
./scripts/prompt.sh reflect 14

# Get reflection prompts
./scripts/prompt.sh reflect-prompts

# Analyze patterns only
./scripts/prompt.sh analyze 7
```

### Direct Python Usage

```bash
# Full reflection report
python3 scripts/reflection.py --report --days 7

# Save to specific file
python3 scripts/reflection.py --report --output my-reflection.md

# JSON output
python3 scripts/reflection.py --report --format json

# Just prompts
python3 scripts/reflection.py --prompts

# Pattern analysis
python3 scripts/reflection.py --analyze --days 14
```

### Content Capture

```bash
# Capture from file
./scripts/prompt.sh capture output.txt --category output --tags tag1,tag2

# Search captured content
./scripts/prompt.sh search "successful prompts"
```

## File Locations

```
prompt-engineering-system/
├── scripts/
│   ├── reflection.py          # Automated analysis
│   ├── prompt.sh              # CLI (updated)
│   ├── embed_output.py        # Capture outputs
│   └── search_knowledge.py    # Search database
├── frameworks/
│   └── meta/
│       └── weekly-reflection.md  # Reflection framework
├── context/
│   └── learnings/
│       ├── reflection-log.md     # Your reflections
│       ├── what-works.md         # Best practices
│       ├── what-doesnt.md        # Anti-patterns
│       └── reflection-*.md       # Generated reports
└── docs/
    └── reflection-system.md      # Full documentation
```

## What Gets Generated

### Reflection Report Includes:

- **Summary**: Total entries, categories, tags
- **Category Breakdown**: How you're spending time
- **Popular Topics**: Most-used tags
- **Patterns Identified**: Recurring themes
- **What's Working Well**: Alignment with best practices
- **Areas for Improvement**: Anti-patterns detected
- **Patterns to Validate**: Items needing more data
- **Reflection Questions**: Context-aware prompts
- **Recommended Next Steps**: Actionable items

### Example Report Structure:

```markdown
# Reflection Report

**Period:** Last 7 days
**Generated:** 2024-11-27 23:59:00

## Summary
- Total Entries: 15
- Categories Used: 3
- Unique Tags: 8
- Most Active Day: 2024-11-25

## Category Breakdown
- output: 8 entries
- template: 5 entries
- framework: 2 entries

## Popular Topics
- prompt-engineering (12 mentions)
- successful (8 mentions)
- claude (6 mentions)

[... and more sections ...]
```

## Dependencies

The reflection system requires:

- Python 3.7+
- Qdrant (running on localhost:6333)
- sentence-transformers
- qdrant-client

Already installed if you've set up the base system.

## Troubleshooting

### "No entries found"

**Problem**: Reflection script can't find any entries

**Fix**:
```bash
# Check Qdrant is running
./scripts/prompt.sh status

# Capture some content first
./scripts/prompt.sh capture example.txt --category output --tags test
```

### "Connection refused to Qdrant"

**Problem**: Qdrant database not running

**Fix**:
```bash
cd infrastructure
docker-compose up -d qdrant

# Verify it's running
curl http://localhost:6333/
```

### Script won't execute

**Problem**: Permission denied

**Fix**:
```bash
chmod +x scripts/reflection.py
chmod +x scripts/prompt.sh
```

## Next Steps

1. **Capture content regularly** - Build your knowledge base
2. **Run weekly reflections** - Friday or Sunday
3. **Update learnings** - Keep what-works/what-doesnt current
4. **Create templates** - Based on identified patterns
5. **Review monthly** - Look at trends over time

## Advanced Usage

### Custom Analysis

```python
# In Python, you can customize the analysis
from scripts.reflection import ReflectionService

service = ReflectionService()
entries = service.get_recent_entries(days=30, category="template")
analysis = service.analyze_patterns(entries)
```

### Integration with Other Tools

```bash
# Export JSON for external processing
python3 scripts/reflection.py --analyze --format json > analysis.json

# Use with jq
python3 scripts/reflection.py --analyze --format json | jq '.analysis.categories'
```

### Batch Processing

```bash
# Generate reflections for multiple periods
for days in 7 14 30; do
  python3 scripts/reflection.py --report --days $days --output "reflection-${days}days.md"
done
```

## Tips for Success

1. **Be consistent** - Capture content as you work
2. **Tag thoughtfully** - Use descriptive, searchable tags
3. **Reflect weekly** - Don't let it pile up
4. **Act on insights** - Reflection without action is wasted
5. **Review progress** - Look at past reflections monthly

## Getting Help

- Full documentation: `docs/reflection-system.md`
- Framework guide: `frameworks/meta/weekly-reflection.md`
- Example reflections: `context/learnings/reflection-log.md`
- Code: `scripts/reflection.py`

---

**Remember**: The system is only as good as the content you feed it. Capture regularly, reflect weekly, and act on insights!
