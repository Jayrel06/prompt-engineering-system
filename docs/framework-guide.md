# Framework Guide

How to use the thinking frameworks effectively.

## What Are Frameworks?

Frameworks are structured approaches to thinking. Unlike task-specific prompts, frameworks are reusable across many different problems.

## Available Frameworks

### Planning Frameworks

| Framework | Use When | Key Output |
|-----------|----------|------------|
| **First Principles** | Questioning assumptions, novel problems | Core assumptions + recommended approach |
| **Pre-Mortem** | Before starting something risky | Risk list + mitigation strategies |
| **Opportunity Cost** | Choosing between options | True cost analysis + recommendation |
| **Constraint Mapping** | Feeling stuck | Real vs assumed constraints |
| **Strategic Planning** | Quarterly/annual planning | Strategy + 90-day plan |

### Analysis Frameworks

| Framework | Use When | Key Output |
|-----------|----------|------------|
| **Steelman Critique** | Evaluating ideas fairly | Strongest version + valid critique |
| **Assumption Surfacing** | Plans seem too easy | Hidden assumptions + tests |
| **Second-Order Effects** | Considering consequences | Effect chains + net assessment |
| **Root Cause Analysis** | Problems keep recurring | Actual cause + countermeasures |

### Decision Frameworks

| Framework | Use When | Key Output |
|-----------|----------|------------|
| **Reversibility Assessment** | Calibrating analysis depth | One-way vs two-way door |
| **Regret Minimization** | Major life/career decisions | Long-term perspective |
| **Decision Matrix** | Comparing multiple options | Weighted scores + recommendation |

### Technical Frameworks

| Framework | Use When | Key Output |
|-----------|----------|------------|
| **Architecture Design** | Starting new systems | Components + data flow + tech choices |
| **Debugging** | Something isn't working | Root cause + fix + prevention |

### Communication Frameworks

| Framework | Use When | Key Output |
|-----------|----------|------------|
| **Audience Adaptation** | Tailoring message | Adapted content for specific audience |

## How to Use Frameworks

### Via CLI

```bash
# Use a specific framework
prompt framework first-principles "Should I build or buy this feature?"

# Framework name is the filename without .md
prompt framework pre-mortem "Launch new product line"
prompt framework decision-matrix "Choose between three vendors"
```

### Via Direct File Reference

```bash
# Read the framework, apply manually
cat frameworks/planning/first-principles.md
```

### Via Copy-Paste

1. Open the framework file
2. Copy the relevant sections
3. Paste into your AI conversation
4. Add your specific task

## Combining Frameworks

For complex decisions, use multiple frameworks:

1. **First Principles** → Understand the fundamental problem
2. **Assumption Surfacing** → Identify what you're assuming
3. **Pre-Mortem** → Consider what could go wrong
4. **Decision Matrix** → Compare options systematically

## Creating New Frameworks

When you develop a new thinking pattern:

1. Create file in appropriate category: `frameworks/[category]/[name].md`
2. Include these sections:
   - **Purpose:** What this framework does
   - **When to Use:** Situations where it applies
   - **The Process:** Step-by-step approach
   - **Output Format:** What the result should look like

### Template

```markdown
# [Framework Name]

## Purpose
[What this framework helps you do]

## When to Use
- [Situation 1]
- [Situation 2]
- [Situation 3]

## The Process

### Stage 1: [Name]
[What to do and why]

### Stage 2: [Name]
[What to do and why]

### Stage N: [Name]
[What to do and why]

## Output Format

1. **[Section 1]:** [What it contains]
2. **[Section 2]:** [What it contains]
...
```

## Framework Best Practices

### Do
- Work through each stage fully
- Be honest in your answers
- Challenge your initial assumptions
- Document insights for future reference

### Don't
- Skip stages that seem obvious
- Use frameworks for simple problems
- Blindly follow framework output
- Forget to actually decide/act
