# What Works

## Prompt Engineering

### Clear Role Definition
Setting explicit role and context at the start dramatically improves output quality.
```
"You are a [specific role] with expertise in [domain]. Your task is to..."
```

### Output Format Specification
Specifying exact output format reduces need for reformatting and parsing errors.
- JSON for structured data
- Markdown for documentation
- Specific field names

### Chain-of-Thought for Complex Tasks
Adding "Let's think step by step" or explicit reasoning steps improves accuracy on multi-step problems.

### Few-Shot Examples
2-3 good examples often worth more than paragraphs of instructions.

---

## n8n Workflows

### Error Handling First
Building error paths before happy paths prevents production surprises.

### Sticky Notes for Documentation
Using sticky notes in workflows as section headers makes complex flows readable.

### Sub-Workflows for Reuse
Extracting common patterns into sub-workflows saves time and reduces bugs.

### Environment Variables
Using env vars for all credentials and URLs makes deployment easier.

---

## Voice AI

### One Question Rule
Strict adherence to one question per turn dramatically improves completion rates.

### Number Spelling
Spelling out numbers improves transcription accuracy.

### Emergency Detection
Clear emergency keywords with immediate escalation prevents liability issues.

### Natural Confirmations
"So that's [X], correct?" builds confidence and catches errors.

---

## Business/Sales

### ROI-First Conversations
Leading with ROI calculation makes the value obvious.
- "You're losing $X per week in missed calls"
- "This solution pays for itself in Y weeks"

### Show Don't Tell
Demos and examples beat abstract explanations every time.

### Discovery Before Solution
Understanding the specific problem before proposing solutions increases close rates.

### Clear Scope Boundaries
Explicit "what's included" and "what's not included" prevents scope creep.

---

## Technical

### Docker for Everything
Containerizing all services makes deployment and debugging consistent.

### PostgreSQL as Default
Starting with PostgreSQL and adding pgvector is simpler than multiple databases.

### Cloudflare Tunnels
Much simpler than managing SSL certs and port forwarding.

### Self-Hosted Observability
Langfuse + Grafana provides enough visibility without external dependencies.

---

## Process

### Write Specs First
Claude Code handoffs work much better with written specs than verbal descriptions.

### Test with Real Data
Synthetic test data misses edge cases that real data reveals.

### Ship Small, Iterate
Smaller deployments with faster feedback beats big-bang releases.

### Document as You Build
Writing docs during development is much easier than after.
