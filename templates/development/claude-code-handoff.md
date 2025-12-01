# Claude Code Handoff Template

## Purpose
Create comprehensive, copy-paste-ready prompts for Claude Code that result in production-quality implementations without back-and-forth clarification.

---

## Template Structure

```markdown
# [PROJECT_NAME] - Claude Code Implementation

## Mission
[One sentence describing what Claude Code will build]

## Success Criteria
- [ ] [Specific, measurable outcome 1]
- [ ] [Specific, measurable outcome 2]
- [ ] [Specific, measurable outcome 3]

## Non-Goals (Explicitly Out of Scope)
- [Thing that might seem related but shouldn't be built]
- [Another thing to avoid]

---

## Current State

### Existing Infrastructure
[What's already running that this integrates with]

### Relevant Files to Read First
- `path/to/file1.py` - [What it contains]
- `path/to/file2.json` - [What it contains]

### Constraints
- **Technical:** [Stack requirements, versions]
- **Time:** [Deadline or time budget]
- **Dependencies:** [What this depends on / what depends on this]

---

## Technical Specification

### Architecture Overview
[Describe the system design - use ASCII diagrams if helpful]

```
[Source] → [Processing] → [Output]
```

### Components to Build

#### 1. [Component Name]
- **Purpose:** [What it does]
- **Inputs:** [What it receives]
- **Outputs:** [What it produces]
- **Location:** [Where it lives in codebase]

#### 2. [Component Name]
- **Purpose:** [What it does]
- **Inputs:** [What it receives]
- **Outputs:** [What it produces]
- **Location:** [Where it lives in codebase]

### Data Flow
[Describe how data moves through the system]

### Error Handling
[How errors should be handled at each stage]

---

## Implementation Instructions

### Phase 1: [Setup/Foundation]
1. [Specific step]
2. [Specific step]

### Phase 2: [Core Implementation]
1. [Specific step]
2. [Specific step]

### Phase 3: [Integration/Testing]
1. [Specific step]
2. [Specific step]

---

## Verification Checklist

Before marking complete, verify:
- [ ] [Specific test or check]
- [ ] [Specific test or check]
- [ ] [Specific test or check]

---

## Reference Material

### Code Examples
[Include working examples of similar patterns if available]

### Documentation Links
[Links to relevant docs Claude Code should reference]

### Known Issues to Avoid
[Gotchas from past experience]
```

---

## Template Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `[PROJECT_NAME]` | Clear, descriptive name | "Lead Scoring Workflow" |
| `[TECH_STACK]` | Technologies involved | "n8n, PostgreSQL, Claude API" |
| `[INTEGRATION_POINTS]` | What it connects to | "CRM webhook, email service" |
| `[OUTPUT_LOCATION]` | Where to put results | "/workflows/lead-scoring/" |

---

## Best Practices

### Be Specific, Not Vague
**Bad:** "Build a lead scoring system"
**Good:** "Build an n8n workflow that receives webhook data from our CRM, scores leads 1-100 based on company size and industry, and stores results in PostgreSQL"

### Define Success Criteria
- Make them testable
- Include edge cases
- Specify error handling

### Provide Context
- What exists already
- What shouldn't be changed
- Why this is being built

### Include Non-Goals
- Prevents scope creep
- Clarifies boundaries
- Saves clarification time

---

## Example: Complete Handoff

```markdown
# Lead Scoring System - Claude Code Implementation

## Mission
Build an n8n workflow that scores incoming leads from 1-100 based on company characteristics and notifies sales for high-scoring leads.

## Success Criteria
- [ ] Webhook receives lead data and returns 200 within 2 seconds
- [ ] Lead score calculated based on: company size, industry, location
- [ ] Scores saved to PostgreSQL leads table
- [ ] Slack notification sent for leads scoring >80
- [ ] Error handling logs failures without crashing workflow

## Non-Goals
- Don't modify existing CRM integration
- Don't build a UI for viewing scores
- Don't implement machine learning (rule-based only)

---

## Current State

### Existing Infrastructure
- n8n running at localhost:5678
- PostgreSQL with leads table (id, email, company, created_at)
- Slack webhook configured in n8n credentials

### Relevant Files
- `/n8n_stack/docker-compose.yml` - Docker configuration
- `existing-workflow.json` - Similar workflow for reference

### Constraints
- Must work with n8n latest version
- PostgreSQL connection via n8n credential "postgres-main"
- Complete by end of week

---

## Technical Specification

### Architecture
```
Webhook → Validate → Score → Store → Notify (if high)
```

### Scoring Rules
- Company size > 100 employees: +30 points
- Industry in [healthcare, HVAC, home services]: +25 points
- Location in target states [TX, CA, FL]: +20 points
- Has phone number: +15 points
- Has website: +10 points

### Components

#### 1. Webhook Receiver
- Receives POST with JSON body
- Validates required fields (email, company)
- Returns 200 with lead_id

#### 2. Scoring Engine
- Applies rules above
- Returns score 0-100

#### 3. Database Writer
- Upserts to leads table
- Adds score and scored_at columns

#### 4. Notifier
- If score > 80, sends Slack message
- Message includes: company, score, email

---

## Implementation Instructions

### Phase 1: Setup
1. Create new workflow "Lead Scoring"
2. Add Webhook node with path /score-lead
3. Add Set node for validation

### Phase 2: Core
1. Add Function node with scoring logic
2. Add Postgres node for upsert
3. Add IF node for score > 80

### Phase 3: Integration
1. Add Slack node for notifications
2. Add error handling with Error Trigger
3. Test with sample data

---

## Verification Checklist
- [ ] POST to webhook returns 200 with valid data
- [ ] Score appears in database
- [ ] High-score lead triggers Slack message
- [ ] Invalid data returns 400
- [ ] Errors are logged, not silent
```
