# Template Guide

How to use and create templates for recurring tasks.

## What Are Templates?

Templates are structured prompts for specific, recurring tasks. Unlike frameworks (which are thinking patterns), templates are task-specific and production-ready.

## Available Templates

### Voice AI Templates

| Template | Purpose |
|----------|---------|
| **receptionist-base** | Complete AI receptionist system prompt |
| **emergency-handling** | Emergency detection and response |
| **appointment-booking** | Appointment scheduling flow |
| **lead-qualification** | Lead qualification conversation |

### Development Templates

| Template | Purpose |
|----------|---------|
| **claude-code-handoff** | Comprehensive spec for Claude Code |
| **n8n-workflow-spec** | Specification for n8n workflows |
| **api-integration-spec** | API integration requirements |

### Outreach Templates

| Template | Purpose |
|----------|---------|
| **cold-email-personalization** | Personalized cold outreach |
| **linkedin-outreach** | LinkedIn connection messages |
| **follow-up-sequences** | Multi-touch follow-up |

### Client Templates

| Template | Purpose |
|----------|---------|
| **proposal-generation** | Client proposals |
| **sop-documentation** | Standard operating procedures |
| **onboarding-guide** | Client onboarding docs |

## Using Templates

### Via CLI

```bash
# Generate handoff prompt
prompt handoff "Build a lead scoring system"
```

### Via Direct Reference

```bash
# View template
cat templates/development/claude-code-handoff.md

# Copy and customize manually
```

### Via Copy-Paste

1. Open template file
2. Copy the structure
3. Fill in your specific details
4. Use with AI

## Template Customization

Templates contain variables in `[BRACKETS]` that need replacement:

```markdown
You are [NAME], the receptionist for [BUSINESS_NAME]...
```

Replace with actual values:

```markdown
You are Sarah, the receptionist for ABC Heating...
```

## Creating New Templates

### When to Create a Template

Create a template when:
- You do the same type of task repeatedly
- The task has consistent structure
- Quality matters (client-facing, production use)
- You want consistency across instances

### Template Structure

```markdown
# [Template Name]

## Purpose
[What this template is for]

---

## Template

[The actual template content with [VARIABLES]]

---

## Variables Reference

| Variable | Description | Example |
|----------|-------------|---------|
| `[VAR1]` | [What it is] | [Example value] |
| `[VAR2]` | [What it is] | [Example value] |

---

## Customization Notes

[Any special instructions for using this template]

---

## Examples

[One or more complete examples with variables filled in]
```

### Best Practices

1. **Clear Variable Names:** `[BUSINESS_NAME]` not `[X]`
2. **Include Examples:** Show completed versions
3. **Document Variables:** Table of all variables with descriptions
4. **Add Customization Notes:** Special instructions for specific uses
5. **Test Before Deploying:** Use with real scenarios

## Voice AI Template Specifics

Voice AI templates require special attention:

### Critical Elements
- One question at a time rule
- Number spelling (write out numbers)
- Emergency detection keywords
- Information boundaries
- Natural conversation flow

### Testing Voice AI Templates
1. Test happy path (normal conversation)
2. Test emergency keywords
3. Test edge cases (one-word responses, silence)
4. Test objection handling
5. Test AI reveal attempts

### Customization Checklist
- [ ] All `[VARIABLES]` replaced
- [ ] Industry-specific emergencies added
- [ ] Business hours accurate
- [ ] Service list complete
- [ ] FAQ relevant to business
- [ ] Personality matches brand

## Development Template Specifics

Development templates (Claude Code handoffs) need:

### Required Sections
- Mission (one sentence)
- Success criteria (testable)
- Non-goals (explicit scope limits)
- Current state (what exists)
- Technical specification
- Implementation instructions
- Verification checklist

### What Makes a Good Handoff
- Can be executed without clarifying questions
- Success criteria are specific and measurable
- Non-goals prevent scope creep
- Technical spec is detailed enough
- Verification checklist confirms completion
