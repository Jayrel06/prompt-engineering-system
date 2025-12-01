# Contributing to Your Prompt Engineering System

This is a personal system designed to improve through use. Here's how to evolve it effectively.

## Philosophy

This system follows the principle of **learning through doing**:
- Document what works
- Learn from what doesn't
- Build patterns from experience
- Share knowledge when it's proven

## Adding New Content

### Frameworks

When you develop a new thinking pattern that works repeatedly:

1. Create a new file in the appropriate `frameworks/` subdirectory
2. Follow this structure:

```markdown
# Framework Name

## When to Use
[Describe the situations where this framework applies]

## The Framework
[Step-by-step process]

## Prompt Template
[Ready-to-use prompt that implements this framework]

## Examples
[Real examples of the framework in action]

## Anti-patterns
[Common mistakes to avoid]
```

### Templates

For recurring tasks that benefit from standardization:

1. Create a new file in the appropriate `templates/` subdirectory
2. Include:
   - Clear purpose statement
   - Variable placeholders with `{{variable_name}}`
   - Example outputs
   - Success criteria

### Context Files

When adding new knowledge:

1. Choose the appropriate directory:
   - `identity/` - Personal principles, style, preferences
   - `business/` - Company, market, competitive info
   - `technical/` - Infrastructure, tools, patterns
   - `projects/` - Specific project context
   - `learnings/` - What works and what doesn't

2. Keep files focused—one topic per file
3. Use clear, scannable formatting
4. Include dates for time-sensitive information

## Documenting Learnings

### What Works (`context/learnings/what-works.md`)

When something produces exceptional results:

```markdown
## [Category] - [Brief Title]

**Context:** [When/where this was used]
**Technique:** [What you did]
**Result:** [Measurable outcome]
**Why it worked:** [Your analysis]
**Reusable pattern:** [How to apply elsewhere]
```

### What Doesn't (`context/learnings/what-doesnt.md`)

When something fails or underperforms:

```markdown
## [Category] - [Brief Title]

**Context:** [When/where this was tried]
**Approach:** [What you attempted]
**Result:** [What went wrong]
**Root cause:** [Why it failed]
**Better alternative:** [What to do instead]
```

## Versioning Prompts

For critical prompts that evolve:

1. Add version header:
```markdown
---
version: 1.2.0
last_updated: 2024-01-15
changelog:
  - 1.2.0: Added error handling section
  - 1.1.0: Improved output format
  - 1.0.0: Initial version
---
```

2. Keep previous versions in `archive/` if needed for rollback

## Testing Changes

Before committing framework or template changes:

1. Test with real tasks
2. Document the test case
3. Compare outputs to previous version
4. Update promptfoo tests if applicable

```bash
cd tests
promptfoo eval
```

## Code Style

### Markdown
- Use ATX headers (`#`, `##`, `###`)
- One sentence per line for easier diffs
- Use fenced code blocks with language hints

### Python Scripts
- Follow PEP 8
- Add docstrings to functions
- Type hints for function signatures

### Bash Scripts
- Use shellcheck
- Quote variables
- Add usage comments

## Commit Messages

Format: `[category] Brief description`

Categories:
- `[framework]` - Changes to frameworks
- `[template]` - Changes to templates
- `[context]` - Updates to context files
- `[script]` - CLI or automation changes
- `[infra]` - Infrastructure updates
- `[docs]` - Documentation only
- `[fix]` - Bug fixes

Examples:
```
[framework] Add chain-of-thought prompting guide
[template] Update Claude Code handoff with error handling
[context] Add Q1 2024 project priorities
[script] Improve vector search relevance scoring
```

## Pull Request Process

If sharing improvements:

1. Ensure all tests pass
2. Update relevant documentation
3. Add entry to CHANGELOG.md if significant
4. Describe the problem solved and approach taken

## Questions?

This is your system—modify these guidelines to match how you work best.
