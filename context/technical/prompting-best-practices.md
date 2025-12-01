# Prompting Best Practices Reference Guide

## Quick Reference Cheatsheet

### The Golden Rules

1. **Be Specific** - Vague prompts get vague results
2. **Show Examples** - 2-4 examples beats lengthy explanations
3. **Structure Matters** - Use clear delimiters and organization
4. **Task First** - Lead with what you want, context second
5. **Test and Iterate** - First draft rarely perfect

### The Formula for Great Prompts

```
WHAT (task) + HOW (format) + WHY (context) + EXAMPLES = Success
```

## Do's and Don'ts

### DO: Be Specific and Direct

**DO:**
```
Extract the person's name, email, and phone number from this text. Format as JSON with keys: name, email, phone. If any field is missing, use null.
```

**DON'T:**
```
Get me the contact info from this.
```

---

### DO: Provide Examples (Few-Shot)

**DO:**
```
Classify sentiment as Positive, Negative, or Neutral.

"Great product!" → Positive
"Terrible experience." → Negative
"It's okay." → Neutral

"[NEW TEXT]" → ?
```

**DON'T:**
```
Classify the sentiment of this text.
```

---

### DO: Specify Output Format

**DO:**
```
Summarize in exactly 3 bullet points, each 10-15 words.
```

**DON'T:**
```
Summarize this.
```

---

### DO: Use Clear Delimiters

**DO:**
```xml
<text_to_analyze>
[User's text here]
</text_to_analyze>

<instructions>
Analyze sentiment
</instructions>
```

**DON'T:**
```
Analyze the sentiment of: [text] and make sure to consider context and also...
```

---

### DO: Break Complex Tasks into Steps

**DO:**
```
Step 1: Extract all dates from the text
Step 2: Convert dates to YYYY-MM-DD format
Step 3: Sort chronologically
Step 4: Return as JSON array
```

**DON'T:**
```
Process the dates in this text.
```

---

### DO: Set Role and Expertise Level

**DO:**
```
You are an expert Python developer with 10 years of experience. Review this code for security vulnerabilities and performance issues.
```

**DON'T:**
```
Look at this code.
```

---

### DO: Specify Constraints and Boundaries

**DO:**
```
Generate 5 product names. Requirements:
- 6-12 characters
- No special characters
- Memorable and professional
- Tech industry appropriate
- Not similar to existing brands: [list]
```

**DON'T:**
```
Generate some product names.
```

---

### DO: Use Chain-of-Thought for Complex Reasoning

**DO:**
```
Solve this problem step-by-step. Show your work.

Problem: [complex problem]

Let's think through this:
```

**DON'T:**
```
What's the answer to [complex problem]?
```

---

### DO: Provide Success Criteria

**DO:**
```
Write a product description that:
- Is 50-75 words
- Includes keywords: [list]
- Has persuasive tone
- Ends with call-to-action
- Avoids technical jargon
```

**DON'T:**
```
Write a good product description.
```

---

### DO: Handle Edge Cases Explicitly

**DO:**
```
Extract email addresses.

Rules:
- Return empty array if none found
- Validate format (must contain @ and domain)
- Remove duplicates
- Convert to lowercase
```

**DON'T:**
```
Find the emails.
```

## Common Mistakes to Avoid

### Mistake 1: Assuming Context

**Problem:**
```
Summarize it.
```

**Fix:**
```
Summarize the article below in 3 sentences:

[Article text]
```

**Why it matters:** Model needs explicit reference to what "it" is.

---

### Mistake 2: Ambiguous Instructions

**Problem:**
```
Make it better.
```

**Fix:**
```
Improve this text by:
1. Fixing grammar and spelling
2. Making sentences more concise
3. Using active voice
4. Removing jargon
```

**Why it matters:** "Better" is subjective; be specific about improvements.

---

### Mistake 3: Multiple Conflicting Instructions

**Problem:**
```
Write a detailed summary but keep it brief. Be formal but conversational. Include everything important but be concise.
```

**Fix:**
```
Write a 100-word executive summary in a professional but accessible tone. Focus on the top 3 key findings.
```

**Why it matters:** Conflicting instructions confuse the model.

---

### Mistake 4: Burying the Lead

**Problem:**
```
Here's background about my company [500 words]... oh by the way, write a blog post about AI.
```

**Fix:**
```
Write a 500-word blog post about AI in healthcare.

Company context: [relevant info]
Target audience: Healthcare professionals
```

**Why it matters:** Task should come first (primacy effect).

---

### Mistake 5: No Format Specification

**Problem:**
```
List the pros and cons.
```

**Fix:**
```
List pros and cons in this format:

**Pros:**
- [Pro 1]
- [Pro 2]

**Cons:**
- [Con 1]
- [Con 2]
```

**Why it matters:** Explicit formatting ensures consistency.

---

### Mistake 6: Overloading in Single Prompt

**Problem:**
```
Analyze sentiment, extract entities, summarize, translate to Spanish, and generate keywords.
```

**Fix:**
```
[Separate into 5 distinct prompts or use structured steps]

Task 1: Analyze sentiment
Task 2: Extract entities
[etc.]
```

**Why it matters:** Too many tasks leads to errors and incomplete results.

---

### Mistake 7: Ignoring Token Limits

**Problem:**
```
[Provides 50,000 words of context]
Analyze all of this.
```

**Fix:**
```
[Break into chunks]
Analyze this section focusing on [specific aspects]
```

**Why it matters:** Context window limits cause truncation.

---

### Mistake 8: Not Handling Uncertainty

**Problem:**
```
What is the answer?
```

**Fix:**
```
What is the answer? If you're not certain, indicate your confidence level and explain your reasoning.
```

**Why it matters:** Models should acknowledge uncertainty vs. hallucinating.

---

### Mistake 9: Inconsistent Example Formatting

**Problem:**
```
"hello" -> HELLO
goodbye => GOODBYE
world = WORLD
```

**Fix:**
```
Input: "hello"
Output: "HELLO"

Input: "goodbye"
Output: "GOODBYE"
```

**Why it matters:** Inconsistent formatting confuses pattern recognition.

---

### Mistake 10: No Validation Instructions

**Problem:**
```
Generate an email address.
```

**Fix:**
```
Generate a valid email address that:
- Contains @ symbol
- Has a domain (.com, .org, etc.)
- Uses only valid characters
- Follows standard email format
```

**Why it matters:** Without validation criteria, outputs may be invalid.

## Claude-Specific Techniques

### XML Tags

Claude excels with XML structure:

```xml
<documents>
  <document index="1">
    <source>report.pdf</source>
    <content>
      [Document text]
    </content>
  </document>
</documents>

<question>
Based on document 1, what are the key findings?
</question>
```

**Benefits:**
- Clear boundaries
- Handles complex nested structures
- Easy to reference specific sections
- Better parsing of multi-part inputs

---

### Prefilling

Control Claude's response start:

```python
# API example
messages = [
    {"role": "user", "content": "Generate JSON user data"},
    {"role": "assistant", "content": "{"} # Prefill
]
```

**Use cases:**
- Force JSON output (start with `{`)
- Skip preambles
- Ensure specific format
- Direct thinking process (`<thinking>`)

---

### Extended Thinking

For complex reasoning, use thinking tags:

```xml
<task>
Solve this complex problem: [problem]
</task>

First, think through your approach:
<thinking>
[Model works through reasoning]
</thinking>

Then provide your answer:
<answer>
```

---

### Document Indexing

For multiple documents:

```xml
<documents>
  <document index="1">[Doc 1]</document>
  <document index="2">[Doc 2]</document>
  <document index="3">[Doc 3]</document>
</documents>

<question>
Compare the approaches in documents 1 and 3.
</question>
```

---

### Prompt Caching (Enterprise)

For repeated content, structure for caching:

```python
# Put stable content first
system_prompt = """
[Large, rarely-changing instructions]
[Examples]
[Reference material]
"""

# Variable content last
user_prompt = """
[Specific task that changes each time]
"""
```

**Savings:** Up to 90% cost reduction on cached content.

## Temperature Settings Guide

Temperature controls randomness (0.0 to 1.0).

### Temperature by Use Case

| Temperature | Use Case | Examples |
|-------------|----------|----------|
| 0.0 - 0.3 | Deterministic tasks | Data extraction, classification, formatting |
| 0.3 - 0.5 | Balanced tasks | Summarization, Q&A, analysis |
| 0.5 - 0.7 | Creative with guidance | Marketing copy, emails, technical writing |
| 0.7 - 0.9 | Creative tasks | Brainstorming, creative writing, ideation |
| 0.9 - 1.0 | Highly creative | Fiction, poetry, experimental content |

### Temperature Examples

**Temperature 0 (Deterministic):**
```
Extract the date from: "Meeting on March 15th"
→ Always returns: "2024-03-15"
```

**Temperature 0.7 (Creative):**
```
Write a tagline for a coffee shop
→ Varies: "Where every cup tells a story" / "Brewing happiness daily" / "Your morning starts here"
```

### Decision Matrix

**Use LOW temperature (0-0.3) when:**
- Consistency is critical
- Extracting facts/data
- Classification tasks
- Mathematical calculations
- Code generation (mostly)
- Translations

**Use MEDIUM temperature (0.3-0.7) when:**
- Balanced creativity and accuracy
- Summaries and explanations
- Business writing
- Code with some flexibility
- General Q&A

**Use HIGH temperature (0.7-1.0) when:**
- Creativity is the goal
- Brainstorming ideas
- Multiple valid answers exist
- Exploring options
- Creative writing

### Other Parameters

**Top-P (Nucleus Sampling):**
- Alternative to temperature
- Range: 0-1
- Lower = more focused
- Use: 0.9 for most tasks

**Max Tokens:**
- Limits response length
- Set appropriately:
  - Short answers: 100-300
  - Medium responses: 500-1000
  - Long content: 1500-3000

**Stop Sequences:**
- End generation at specific text
- Useful for structured outputs
- Example: Stop at "\n\n" for single paragraph

## Prompt Optimization Workflow

### 1. Start Simple

```
Version 1: "Summarize this article"
```

### 2. Add Specificity

```
Version 2: "Summarize this article in 3 bullet points"
```

### 3. Add Format

```
Version 3:
Summarize in exactly 3 bullet points, each 15-20 words:
- [Point 1]
- [Point 2]
- [Point 3]
```

### 4. Add Context

```
Version 4:
Summarize this technical article for a non-technical audience.

Format: 3 bullet points, each 15-20 words
- [Point 1]
- [Point 2]
- [Point 3]
```

### 5. Add Examples

```
Version 5:
Summarize this technical article for a non-technical audience.

Example:
Technical: "The algorithm uses dynamic programming with memoization"
Non-technical: "The system remembers previous calculations to work faster"

Format: 3 bullet points, each 15-20 words
```

### 6. Test and Iterate

Run on 10+ diverse inputs, identify failure patterns, refine.

## Testing Your Prompts

### Evaluation Framework

**1. Define Success Metrics**
- Accuracy (factual correctness)
- Format compliance
- Consistency (same input → same output)
- Completeness (all requirements met)
- Efficiency (tokens used)

**2. Create Test Set**
- 10-20 diverse inputs
- Include edge cases
- Cover all input types
- Mix difficulty levels

**3. Establish Baseline**
- Test simple version first
- Measure current performance
- Identify failure modes

**4. Iterate**
- Make one change at a time
- Retest on full set
- Track improvements
- Document what works

### Test Case Template

```
Prompt Version: [v2]
Date: [2024-03-15]

Test Case 1:
Input: [test input]
Expected: [expected output]
Actual: [actual output]
Result: [Pass/Fail]
Notes: [observations]

Test Case 2:
[...]

Summary:
- Pass rate: 85% (17/20)
- Common failures: [pattern]
- Recommended changes: [list]
```

## Prompt Library Starter

### Classification

```
Classify the following [item] as [category A], [category B], or [category C].

Examples:
"[example 1]" → [category A]
"[example 2]" → [category B]

Item: [new item]
Category:
```

### Extraction

```
Extract [information] from the following text. Return as [format].

Rules:
- [Rule 1]
- [Rule 2]
- If not found, return [default]

Text: [input]
```

### Generation

```
Generate a [content type] about [topic].

Requirements:
- [Requirement 1]
- [Requirement 2]
- [Requirement 3]

Format:
[Structure description]
```

### Transformation

```
Transform the following [format A] to [format B].

Example:
Input: [example input]
Output: [example output]

Input: [new input]
Output:
```

### Analysis

```
Analyze [subject] for [aspects].

Provide:
1. [Analysis dimension 1]
2. [Analysis dimension 2]
3. [Analysis dimension 3]

Format each finding as:
- **Finding**: [description]
- **Evidence**: [supporting data]
- **Significance**: [why it matters]
```

## Debugging Prompts

### Problem: Inconsistent Outputs

**Solutions:**
1. Lower temperature (0-0.3)
2. Add more specific constraints
3. Use examples to show exact format
4. Add validation rules

### Problem: Wrong Format

**Solutions:**
1. Explicitly specify format
2. Use prefilling
3. Add examples in target format
4. Use delimiters

### Problem: Hallucinations

**Solutions:**
1. Add "only use provided information" instruction
2. Ask for citations
3. Request confidence levels
4. Use chain-of-thought reasoning

### Problem: Missing Information

**Solutions:**
1. Be more specific about requirements
2. Provide relevant context
3. Use structured format with all fields
4. Add "if missing, return [default]" rules

### Problem: Too Verbose

**Solutions:**
1. Set word/sentence limits
2. Ask for concise answers
3. Use prefilling to control format
4. Set max_tokens parameter

### Problem: Too Brief

**Solutions:**
1. Request specific details
2. Ask for explanations
3. Require minimum length
4. Ask for examples

### Problem: Off-Topic Responses

**Solutions:**
1. Lead with task (task-first ordering)
2. Be very specific about scope
3. Add "Do not include" instructions
4. Use focused examples

## Advanced Patterns

### Iterative Refinement

```
[Initial task instruction]

After generating, review your output and:
1. Check for [criterion 1]
2. Verify [criterion 2]
3. Improve [aspect]

Then provide your revised version.
```

### Multi-Perspective Analysis

```
Analyze this issue from three perspectives:

<perspective name="technical">
[Technical analysis]
</perspective>

<perspective name="business">
[Business analysis]
</perspective>

<perspective name="user">
[User analysis]
</perspective>

Then synthesize: [combined insight]
```

### Constrained Creativity

```
Generate [creative content] that:

MUST HAVE:
- [Hard constraint 1]
- [Hard constraint 2]

SHOULD HAVE:
- [Soft constraint 1]
- [Soft constraint 2]

AVOID:
- [Exclusion 1]
- [Exclusion 2]
```

### Self-Verification

```
[Task instruction]

After completing, verify:
1. Did I follow all requirements?
2. Is the format correct?
3. Are there any errors?

If any issues found, correct them before responding.
```

## Cost Optimization Tips

1. **Use shorter system prompts** - Every token costs
2. **Cache repeated content** - Saves 90% on cached tokens
3. **Choose right model** - Haiku for simple tasks
4. **Batch requests** - Process multiple items together
5. **Optimal examples** - 2-4 is sweet spot, not 10
6. **Trim unnecessary context** - Only include what's needed
7. **Stream responses** - Show progress, stop if wrong direction
8. **Use lower temperature** - More consistent = fewer retries

## Quick Prompt Checklist

Before sending any prompt, verify:

- [ ] Task is clearly stated in first sentence
- [ ] Output format is explicitly specified
- [ ] Examples are included (if needed)
- [ ] Delimiters separate distinct sections
- [ ] Edge cases are handled
- [ ] Success criteria are defined
- [ ] Context is provided (but not excessive)
- [ ] Temperature is appropriate for task
- [ ] Prompt is under context window limit
- [ ] No conflicting instructions

## Resources for Deep Dive

- **Anthropic Prompt Engineering Guide**: https://docs.anthropic.com/claude/docs/prompt-engineering
- **OpenAI Best Practices**: https://platform.openai.com/docs/guides/prompt-engineering
- **Prompt Engineering Guide**: https://www.promptingguide.ai/
- **Papers**: Wei et al. (Chain-of-Thought), Brown et al. (Few-Shot Learning)

## Summary

**The 5 Commandments of Prompting:**

1. **Be Specific** - Say exactly what you want
2. **Show Examples** - Demonstrate the pattern
3. **Structure Clearly** - Use delimiters and organization
4. **Format Explicitly** - Specify exact output structure
5. **Test Thoroughly** - Iterate based on results

**Remember:**
- Task first, context second
- 2-4 examples is optimal
- Use XML tags for Claude
- Lower temperature for consistency
- One task per prompt (usually)
- Test on edge cases
- Iterate systematically

**Quick Formula:**
```
TASK + FORMAT + EXAMPLES + CONTEXT = Great Prompt
```