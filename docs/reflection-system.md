# Reflection System Documentation

The reflection system helps you systematically learn from your prompt engineering practice by analyzing patterns, identifying successful techniques, and tracking improvements over time.

## Overview

The reflection system consists of:

1. **Automated Analysis** (`scripts/reflection.py`) - Python script that analyzes your prompt history
2. **Reflection Framework** (`frameworks/meta/weekly-reflection.md`) - Structured framework for reflection
3. **Reflection Log** (`context/learnings/reflection-log.md`) - Template for storing reflections
4. **CLI Integration** - Easy-to-use commands via `prompt.sh`

## Quick Start

### Generate a Weekly Reflection

```bash
# Generate reflection for the last 7 days
./scripts/prompt.sh reflect

# Generate reflection for custom period
./scripts/prompt.sh reflect 14
```

This will:
- Analyze all prompts/outputs from the last N days
- Identify patterns and common themes
- Compare against documented learnings
- Generate actionable insights
- Save report to `context/learnings/reflection-YYYY-MM-DD.md`

### Get Reflection Prompts

```bash
# Generate context-aware reflection questions
./scripts/prompt.sh reflect-prompts
```

This generates customized reflection questions based on your recent activity.

### Analyze Patterns

```bash
# Analyze patterns without full report
./scripts/prompt.sh analyze 7
```

Returns JSON analysis of patterns, categories, and trends.

## Components

### 1. Automated Analysis Script (`scripts/reflection.py`)

The Python script provides automated analysis of your prompt engineering practice.

#### Features

- **Pattern Detection**: Identifies recurring themes and approaches
- **Trend Analysis**: Tracks what categories and tags you're using
- **Learning Alignment**: Compares activity against documented best practices
- **Customizable Periods**: Analyze any time period (days, weeks, months)
- **Multiple Output Formats**: Markdown reports or JSON data

#### Usage

```bash
# Generate full reflection report
python3 scripts/reflection.py --report --days 7

# Generate reflection prompts
python3 scripts/reflection.py --prompts

# Analyze patterns only
python3 scripts/reflection.py --analyze --days 14

# Output to file
python3 scripts/reflection.py --report --output my-reflection.md

# JSON format
python3 scripts/reflection.py --report --format json
```

#### How It Works

1. **Retrieves Entries**: Fetches all entries from Qdrant vector database for the specified period
2. **Analyzes Patterns**:
   - Counts categories and tags
   - Identifies popular topics
   - Finds common phrases
   - Tracks daily activity
3. **Compares with Learnings**: Checks entries against `what-works.md` and `what-doesnt.md`
4. **Generates Report**: Creates structured markdown or JSON output
5. **Provides Recommendations**: Suggests specific next steps

### 2. Reflection Framework (`frameworks/meta/weekly-reflection.md`)

A comprehensive framework for structured reflection on your prompt engineering practice.

#### Framework Structure

1. **What Prompts Worked Well This Week?**
   - Document successful prompts
   - Identify key success factors
   - Extract reusable patterns

2. **What Patterns Emerged?**
   - Structural patterns
   - Technique patterns
   - Domain patterns

3. **What Should Be Added to Learnings?**
   - Updates for what-works.md
   - Updates for what-doesnt.md
   - New insights

4. **What Templates Need Updating?**
   - Existing template refinements
   - New template creation
   - Template deprecation

5. **Deeper Questions**
   - Strategic questions
   - Learning questions
   - Process questions
   - Future-oriented questions

#### Using the Framework

```bash
# Use the reflection framework
./scripts/prompt.sh framework weekly-reflection "Conduct my weekly reflection"
```

Or manually work through it while reviewing your automated report.

### 3. Reflection Log (`context/learnings/reflection-log.md`)

A structured template for capturing weekly reflections.

#### Template Sections

- **Summary**: Overview of the week's activity
- **What Worked Well**: Successful techniques and approaches
- **Patterns Identified**: Recurring themes
- **Learnings to Capture**: Items for knowledge base
- **Templates Updated/Created**: Documentation changes
- **Challenges & Solutions**: Problem-solving record
- **Questions Raised**: Items for future exploration
- **Experiments**: Planned tests and trials
- **Metrics**: Quantitative observations
- **Action Items**: Concrete next steps

#### Using the Log

1. Copy the template for each week
2. Fill it out using your automated report and manual observations
3. Track action items week-over-week
4. Review past reflections to see progress

## Workflow

### Weekly Reflection Process

1. **Generate Automated Report** (5 minutes)
   ```bash
   ./scripts/prompt.sh reflect
   ```

2. **Review the Report** (10-15 minutes)
   - Read through patterns identified
   - Note what resonates
   - Flag items for deeper exploration

3. **Manual Reflection** (15-20 minutes)
   - Use frameworks/meta/weekly-reflection.md
   - Answer key questions
   - Add context automated analysis might miss

4. **Update Learnings** (10 minutes)
   - Add to context/learnings/what-works.md
   - Add to context/learnings/what-doesnt.md
   - Update context/learnings/insights-log.md

5. **Document in Reflection Log** (10 minutes)
   - Copy template in reflection-log.md
   - Fill in key sections
   - Create action items

6. **Update Templates** (as needed)
   - Refine existing templates
   - Create new ones
   - Archive outdated ones

### Daily Quick Capture (5 minutes)

Between weekly reflections, capture quick notes:

```markdown
## YYYY-MM-DD

**What worked:**
- [Quick note]

**What didn't:**
- [Quick note]

**One insight:**
- [Key takeaway]
```

Store these in reflection-log.md under a "Daily Notes" section.

### Monthly Meta-Reflection (30-60 minutes)

Once a month, review your weekly reflections:

1. Read through all weekly reflections
2. Identify month-long trends
3. Assess progress toward learning goals
4. Refine the reflection process itself
5. Set goals for next month

## Integration with Other Systems

### Vector Database Integration

The reflection system reads from your Qdrant database where you store:
- Prompt templates
- Example outputs
- Framework documentation
- Learning resources

**Ensure you're capturing regularly:**

```bash
# Capture a prompt output
./scripts/prompt.sh capture my-output.txt --category output --tags prompt,success

# Capture a template
./scripts/prompt.sh capture my-template.md --category template --tags reusable
```

### Context Loader Integration

Use reflection insights in your context assembly:

```bash
# The context-loader already includes learnings
./scripts/prompt.sh plan "Design new workflow"
# This loads context/learnings/what-works.md automatically
```

Your reflections improve the context available for future prompts.

## Metrics to Track

### Quantitative Metrics

- **Entries per week**: Overall activity level
- **Categories used**: Breadth of work
- **Tags per entry**: Depth of categorization
- **Iterations per prompt**: Efficiency indicator
- **Time to successful output**: Speed metric

### Qualitative Metrics

- **Pattern recognition**: Are you identifying reusable patterns?
- **Learning velocity**: How quickly are you improving?
- **Knowledge application**: Are learnings being applied?
- **Template quality**: Are templates getting better?

## Tips for Effective Reflection

### Do's

1. **Schedule it**: Block time for reflection, don't leave it to chance
2. **Review actual outputs**: Don't rely on memory
3. **Be specific**: Vague reflections don't drive improvement
4. **Capture immediately**: Write insights when they occur
5. **Look for patterns**: Individual cases are interesting, patterns are valuable
6. **Be honest**: Document failures and anti-patterns
7. **Make it actionable**: Every reflection should produce action items
8. **Review past reflections**: Track how you're evolving

### Don'ts

1. **Don't skip weeks**: Consistency is key
2. **Don't be perfectionist**: Done is better than perfect
3. **Don't just list**: Analyze and draw conclusions
4. **Don't ignore small wins**: They compound
5. **Don't forget to act**: Reflection without action is wasted
6. **Don't work in isolation**: Share learnings when appropriate

## Troubleshooting

### No entries found

**Problem**: Reflection script finds no entries

**Solutions**:
- Check Qdrant is running: `./scripts/prompt.sh status`
- Verify you've captured content: Use `capture` command
- Check date range: Try longer period

### Reflection feels repetitive

**Problem**: Weekly reflections seem similar

**Solutions**:
- Diversify your prompt categories
- Try new techniques intentionally
- Use reflection to identify ruts
- Set specific learning goals

### Not seeing improvement

**Problem**: Reflections don't show progress

**Solutions**:
- Define specific, measurable goals
- Track quantitative metrics
- Review monthly for longer trends
- Focus on one area for deep improvement

### Taking too long

**Problem**: Reflection process is time-consuming

**Solutions**:
- Use automated report as starting point
- Focus on key insights, not comprehensiveness
- Batch similar reflection items
- Improve daily capture to ease weekly work

## Advanced Usage

### Custom Analysis Periods

```bash
# Analyze specific periods
python3 scripts/reflection.py --report --days 30  # Monthly
python3 scripts/reflection.py --report --days 90  # Quarterly
```

### Filtering by Category

Modify `reflection.py` to analyze specific categories:

```python
entries = service.get_recent_entries(days=7, category="template")
```

### Comparing Periods

Generate reports for different periods and compare:

```bash
python3 scripts/reflection.py --report --days 7 --output week1.md
python3 scripts/reflection.py --report --days 14 --output week2.md
# Then manually compare the reports
```

### Integration with Other Tools

Export analysis as JSON and process with other tools:

```bash
python3 scripts/reflection.py --analyze --format json > analysis.json
# Process with jq, import to spreadsheet, etc.
```

## Future Enhancements

Potential additions to the reflection system:

- **Visual dashboards**: Grafana integration for metrics
- **Automated insights**: LLM-powered pattern detection
- **Comparative analysis**: Compare against community benchmarks
- **Goal tracking**: Explicit learning goal management
- **Skill progression**: Track capability development over time
- **Template evolution**: Track how templates improve
- **A/B testing**: Compare different prompt approaches

## Related Documentation

- `context/learnings/what-works.md` - Documented best practices
- `context/learnings/what-doesnt.md` - Anti-patterns to avoid
- `context/learnings/insights-log.md` - General insights
- `context/learnings/prompt-evolution.md` - How prompts have evolved
- `frameworks/meta/weekly-reflection.md` - Full reflection framework

## Support

If you have questions or issues:

1. Check this documentation
2. Review example reflections in reflection-log.md
3. Examine the code in scripts/reflection.py
4. Test with smaller date ranges first

---

**Remember**: The goal of reflection is not perfection, but continuous improvement. Regular, honest reflection compounds into significant capability growth over time.
