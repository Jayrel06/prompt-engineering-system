# Prompt Evolution

Tracking how prompts improve over iterations.

---

## Voice AI Receptionist

### V1 - Initial Attempt
```
You are a receptionist. Answer calls and schedule appointments.
```
**Problems:** Too vague, no personality, no constraints

### V2 - Added Structure
```
You are Sarah, a professional receptionist for ABC Company.
- Schedule appointments
- Answer questions about services
- Be friendly and helpful
```
**Problems:** Still missing critical rules, no emergency handling

### V3 - Production Ready
```
You are Sarah, the friendly receptionist for ABC Company...

CRITICAL RULES:
1. One question at a time
2. Spell out numbers
3. Never reveal AI nature
4. Emergency detection [list]
5. Information boundaries [list]

FLOWS:
[Detailed conversation flows]

BUSINESS INFO:
[Hours, services, FAQ]
```
**Result:** High completion rates, proper emergency handling

### Key Learnings
- Explicit rules > implicit expectations
- Structure matters more than word count
- Emergency handling is non-negotiable
- Test with edge cases before deploy

---

## Claude Code Handoff

### V1 - Minimal Context
```
Build a lead scoring system.
```
**Problems:** Too many clarifying questions, inconsistent results

### V2 - Added Requirements
```
Build a lead scoring system that:
- Takes lead data from webhook
- Scores based on company size, industry, location
- Stores in PostgreSQL
- Sends notification for high scores
```
**Problems:** Still missing tech stack, architecture decisions

### V3 - Full Spec Format
```
# Lead Scoring System - Claude Code Implementation

## Mission
[One sentence]

## Success Criteria
- [ ] Specific criterion 1
- [ ] Specific criterion 2

## Current State
[What exists]

## Technical Specification
[Architecture, components, data flow]

## Implementation Instructions
[Phase-by-phase steps]

## Verification Checklist
[How to confirm success]
```
**Result:** First-attempt success rate dramatically improved

### Key Learnings
- Success criteria = testable acceptance criteria
- Current state prevents breaking existing code
- Phase-by-phase prevents scope confusion
- Verification checklist ensures completeness

---

## Context Assembly Prompt

### V1 - Manual Selection
Manually copying relevant context files for each conversation.
**Problems:** Time-consuming, inconsistent, forgot important context

### V2 - Task-Type Rules
```python
CONTEXT_RULES = {
    "planning": ["core-values.md", "decision-frameworks.md", ...],
    "technical": ["infrastructure.md", "coding-standards.md", ...],
}
```
**Result:** Consistent context per task type

### V3 - Dynamic Assembly (Current)
- Classify task intent
- Load rule-based context
- Search vector DB for similar past work
- Assemble into single prompt

### Key Learnings
- Classification can be cheap (Haiku)
- Rules handle 80% of cases
- Vector search handles edge cases
- Assembly logic is where the value is

---

## Evolution Principles

1. **Start simple, add complexity as needed**
   - V1 is always too simple
   - V2 fixes obvious gaps
   - V3 handles edge cases

2. **Explicit > Implicit**
   - What's obvious to you isn't to the model
   - Write out every assumption
   - Rules beat guidelines

3. **Test with failure cases**
   - Happy path works easily
   - Edge cases reveal prompt weaknesses
   - Adversarial testing for production

4. **Document the "why"**
   - Future you won't remember
   - Each rule exists for a reason
   - Record the incidents that prompted changes
