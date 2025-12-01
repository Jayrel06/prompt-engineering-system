# What Doesn't Work

## Prompt Engineering

### Vague Instructions
"Make it better" or "improve this" without specifics wastes tokens and time.

### Over-Long Prompts
After ~2000 words, prompt effectiveness drops. Break into chains instead.

### Assuming Model Knows Context
Models don't remember previous conversations. Include necessary context each time.

### No Output Format
Without format specification, you get inconsistent outputs requiring manual cleanup.

### Too Many Examples
More than 5 examples often causes overfitting to example patterns.

---

## n8n Workflows

### No Error Handling
Silent failures in production are debugging nightmares.

### Tight Coupling
Workflows that depend on other workflows' internal state are fragile.

### Hardcoded Everything
Credentials and URLs in nodes make environment changes painful.

### Too Many Nodes
Workflows over 30-40 nodes become unmaintainable. Split them.

### No Logging
Can't debug what you can't see. Log key decision points.

---

## Voice AI

### Multiple Questions
"What's your name and phone number?" confuses callers and reduces completion.

### Numeric Digits
"Call us at 555-1234" gets transcribed poorly. Spell out or use words.

### Revealing AI Nature
"As an AI, I can't..." breaks immersion and reduces trust.

### Complex Decision Trees
Too many branches confuse the AI and callers. Simplify flows.

### No Fallback
AI without human escalation path frustrates callers on edge cases.

---

## Business/Sales

### Feature-First Pitches
"Our AI uses GPT-4" means nothing to business owners. Lead with outcomes.

### No Discovery
Proposing solutions without understanding the specific problem = missed sale.

### Under-Pricing for "Exposure"
Cheap projects attract cheap clients. Price reflects value.

### Scope Ambiguity
"We'll figure it out as we go" leads to scope creep and unhappy clients.

### Over-Promising Timelines
Better to under-promise and over-deliver.

---

## Technical

### Premature Optimization
Building for scale before validating the approach wastes time.

### New Tech for Everything
Using latest framework for simple tasks adds complexity without benefit.

### No Documentation
"The code is self-documenting" is never true.

### Skipping Backups
"It won't happen to me" until it does.

### Complex Before Simple
Always start with the simplest solution that could work.

---

## Process

### Building Without Specs
"I'll figure it out as I code" leads to rework.

### Big-Bang Deployments
Large changes are hard to debug. Ship incrementally.

### No Testing
Manual testing doesn't scale. Automate critical paths.

### Ignoring Feedback
Early user feedback is gold. Don't build in isolation.

### Perfect Before Shipping
Done is better than perfect. Ship, then iterate.

---

## Personal Anti-Patterns

### Shiny Object Syndrome
Starting new projects before finishing current ones.

### Tutorial Hell
Consuming content without applying it.

### Over-Engineering
Building for hypothetical future requirements.

### Isolation
Building alone without feedback or accountability.
