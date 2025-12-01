# Weekly Reflection Framework

This framework guides you through a structured weekly reflection on your prompt engineering practice.

## Purpose

Weekly reflections help you:
- Identify what's working and what isn't
- Capture learnings before they're forgotten
- Spot patterns across multiple interactions
- Refine your prompt engineering approach
- Build a knowledge base of effective techniques

---

## Reflection Structure

### 1. What Prompts Worked Well This Week?

**Prompt:** Review your captured outputs and identify 2-3 prompts that produced excellent results.

For each successful prompt, document:
- **The prompt or approach used**
- **What made it effective**
- **The context/task it was used for**
- **Key elements worth reusing**

**Example:**
```
Prompt: "You are an expert technical writer. Break down this complex system into a
simple explanation for non-technical stakeholders. Use analogies and avoid jargon."

What worked:
- Clear role definition (expert technical writer)
- Explicit audience specification (non-technical stakeholders)
- Specific techniques requested (analogies, no jargon)
- Output quality was excellent, required minimal editing

Reusable pattern: [Role] + [Audience] + [Techniques] for communication tasks
```

**Reflection Questions:**
- What do these successful prompts have in common?
- Were they similar in structure or approach?
- Did they use specific techniques (few-shot, chain-of-thought, etc.)?
- Can you extract a reusable template from them?

---

### 2. What Patterns Emerged?

**Prompt:** Look across all your interactions this week for recurring patterns.

Consider:
- **Task types:** What kinds of problems did you solve?
- **Techniques used:** Which prompt engineering techniques appeared most?
- **Output quality:** Where did you get best/worst results?
- **Iterations needed:** Which prompts needed multiple refinements?

**Pattern Categories to Explore:**

**Structural Patterns:**
- Role definitions that worked well
- Output format specifications
- Context-setting approaches
- Constraint statements

**Technique Patterns:**
- Use of examples (few-shot learning)
- Chain-of-thought reasoning
- Structured thinking frameworks
- Comparison or critique patterns

**Domain Patterns:**
- Technical tasks vs creative tasks
- Analysis vs generation
- Communication vs execution

**Reflection Questions:**
- What patterns led to better outcomes?
- What patterns led to wasted time or iterations?
- Are there patterns you should formalize into templates?
- Are there patterns you should avoid?

---

### 3. What Should Be Added to Learnings?

**Prompt:** Identify specific insights to capture in your learnings repository.

Review your week and extract:

**For what-works.md:**
- New techniques that proved effective
- Refinements to existing approaches
- Context where certain methods excel
- Unexpected successes worth documenting

**For what-doesnt.md:**
- Approaches that failed or underperformed
- Time-wasting patterns to avoid
- Limitations you discovered
- Anti-patterns to watch for

**For insights-log.md:**
- Surprising discoveries
- Connections between different techniques
- Meta-insights about prompt engineering
- Questions raised that need exploration

**Template for Learnings:**
```markdown
### [Technique/Pattern Name]

**What:** [Brief description]

**When it works:** [Context and conditions]

**Example:** [Concrete example]

**Why it works:** [Explanation of mechanism]

**Related to:** [Links to other techniques]
```

---

### 4. What Templates Need Updating?

**Prompt:** Review your existing templates against this week's learnings.

For each template category:

**Existing Templates to Refine:**
- Which templates did you use this week?
- What modifications did you make repeatedly?
- What's missing from current templates?
- What could be simplified or clarified?

**New Templates to Create:**
- What task types did you handle multiple times?
- What prompts did you reuse with minor variations?
- What successful patterns should be templatized?
- What workflows are now mature enough to template?

**Template Update Checklist:**
- [ ] Add newly discovered techniques
- [ ] Remove deprecated approaches
- [ ] Include recent examples
- [ ] Update context/role definitions
- [ ] Add output format specifications
- [ ] Include edge cases and error handling
- [ ] Add tags for easier discovery

---

### 5. Deeper Questions for Reflection

**Strategic Questions:**
- What topics or skills am I developing through my prompts?
- Where am I spending the most prompt engineering effort?
- Is that effort aligned with my goals?
- What capabilities am I building vs what am I just using?

**Learning Questions:**
- What did I learn about the AI model's capabilities/limitations?
- What surprised me this week?
- What assumptions were challenged?
- What new questions emerged?

**Process Questions:**
- Am I capturing learnings consistently?
- Are my tags and categories helping or cluttering?
- Is my reflection cadence appropriate?
- What friction points slow down my work?

**Future-Oriented Questions:**
- What experiments do I want to run next week?
- What skills or techniques should I develop?
- What knowledge gaps became apparent?
- What tools or processes would help?

---

## Action Items Template

Based on your reflection, identify concrete next steps:

### Immediate Actions (This Week)
- [ ] Update specific template(s)
- [ ] Add learnings to what-works/what-doesnt
- [ ] Create new template for [specific use case]
- [ ] Document [specific pattern or technique]

### Near-Term Actions (Next 2-4 Weeks)
- [ ] Experiment with [new technique]
- [ ] Build framework for [domain/task]
- [ ] Research [specific topic]
- [ ] Refine [specific workflow]

### Long-Term Improvements
- [ ] Develop expertise in [area]
- [ ] Build comprehensive guide for [topic]
- [ ] Systematize [process]

---

## Reflection Cadence

**Weekly:** Use this framework (every Friday or Sunday)

**Daily:** Quick capture (5 minutes)
- What worked today?
- What didn't work?
- One insight to remember

**Monthly:** Meta-reflection (30-60 minutes)
- Review weekly reflections
- Identify month-long trends
- Assess progress toward goals
- Refine reflection process itself

**Quarterly:** Strategic review
- Evaluate prompt engineering capabilities
- Assess knowledge base quality
- Set learning goals for next quarter
- Identify knowledge gaps

---

## Tips for Effective Reflection

1. **Schedule it:** Block time for reflection, don't leave it to chance
2. **Review actual outputs:** Don't rely on memory, look at what you captured
3. **Be specific:** Vague reflections don't drive improvement
4. **Capture immediately:** Write down insights when they occur
5. **Look for patterns:** Individual cases are interesting, patterns are valuable
6. **Be honest:** Document failures and anti-patterns too
7. **Make it actionable:** Every reflection should produce action items
8. **Review past reflections:** See how your practice is evolving

---

## Example Reflection Entry

```markdown
# Weekly Reflection - Week of 2024-11-25

## What Worked Well

1. **Structured handoff prompts for Claude Code**
   - Template: Role + Context + Constraints + Expected Output
   - Used 3 times this week, all successful
   - Key: Explicit file paths and exact specifications
   - Added to templates/development/

2. **Few-shot examples for n8n workflows**
   - Showing 2 good examples dramatically improved output
   - Pattern: [Bad Example] → [Why It's Bad] → [Good Example]
   - Used in 5 different workflow designs

## Patterns Identified

- Upfront time spent on clear specifications saves 3x time on iterations
- Chain-of-thought works better for debugging than for generation
- Technical tasks benefit from explicit constraints more than creative tasks

## Added to Learnings

- what-works.md: "Specification-first Claude Code handoffs"
- what-doesnt.md: "Vague 'make it better' prompts waste tokens"

## Templates Updated

- Updated: templates/development/claude-code-handoff.md
  - Added explicit file path requirements
  - Added output format examples
  - Included common edge cases

## Next Week's Focus

- Experiment with meta-prompting for template generation
- Build framework for n8n workflow design patterns
- Document voice AI prompt structures
```

---

## Related Frameworks

- **frameworks/analysis/assumption-surfacing.md** - For questioning your assumptions
- **frameworks/planning/pre-mortem.md** - For identifying what could go wrong
- **frameworks/decision/trade-off-analysis.md** - For evaluating different approaches

---

## Meta-Reflection

As you use this framework over time, refine it:

- What questions consistently produce valuable insights?
- What questions feel like busywork?
- What's missing from this framework?
- How could the structure be improved?

The framework should evolve with your practice.
