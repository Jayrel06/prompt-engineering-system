# Prompt Improvement Commands

This directory contains Claude Code slash commands for improving prompts using the prompt engineering system.

## Available Commands

### /improve - Complete Prompt Improvement Workflow
**Usage:** `/improve [your prompt]`

Runs the full improvement workflow:
1. Diagnoses issues with prompt_doctor.py
2. Routes to optimal framework with prompt_router.py  
3. Generates optimized variations with prompt_optimizer.py
4. Returns before/after comparison with metrics

**Example:**
```
/improve Write a blog post about AI
```

---

### /diagnose - Analyze Prompt Issues
**Usage:** `/diagnose [your prompt]`

Runs comprehensive diagnostic analysis:
- Overall health score (0-100)
- Dimension scores (clarity, specificity, completeness, complexity)
- Issues grouped by severity (HIGH/MEDIUM/LOW)
- Specific fix suggestions for each issue
- Framework recommendations

**Example:**
```
/diagnose Summarize this text
```

---

### /optimize - Generate Prompt Variations
**Usage:** `/optimize [your prompt]`

Generates and ranks 3-5 optimized variations:
- Applies different optimization techniques
- Scores each variation on 5 criteria
- Ranks all variations by total score
- Returns winning prompt with reasoning

**Techniques Used:**
- more_specific
- more_concise
- structured
- with_examples
- role_based
- step_by_step
- constrained
- context_rich

**Example:**
```
/optimize Create a marketing email
```

---

### /plan - Strategic Planning (with Prompt Detection)
**Usage:** `/plan [your task or prompt]`

Smart planning command that:
1. Detects if input is a prompt needing improvement
2. Redirects to /improve if it's a prompt
3. Otherwise runs strategic planning frameworks

**Example:**
```
/plan Launch a new product feature
```

---

## Scripts Reference

All commands use these scripts in `C:/Users/JRiel/prompt-engineering-system/scripts/`:

- **prompt_doctor.py** - Diagnostic tool for analyzing prompt quality
- **prompt_router.py** - Routes prompts to optimal frameworks
- **prompt_optimizer.py** - Generates and evaluates variations

## Typical Workflow

1. Start with `/diagnose` to understand issues
2. Use `/optimize` to see multiple approaches
3. Or use `/improve` for the complete automated workflow
4. Use `/plan` when unclear if it's a prompt or planning task

## Output Format

All commands provide:
- Clear section headers
- Specific metrics and scores
- Before/after comparisons
- Actionable recommendations
- Referenced framework paths

---

Created: 2025-12-02
Location: C:/Users/JRiel/prompt-engineering-system/.claude/commands/
