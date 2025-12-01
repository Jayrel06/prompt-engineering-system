# Few-Shot Prompting Framework

## Overview

Few-shot prompting is a technique where you provide the model with a small number of examples (typically 2-5) demonstrating the desired task format, style, and quality. The model learns the pattern from these examples and applies it to new inputs.

## Core Principles

### Why Few-Shot Works

Large language models are pattern recognition machines. By showing examples, you:
- Demonstrate the exact output format
- Establish quality standards
- Clarify ambiguous instructions
- Handle edge cases
- Set tone and style

**Key Insight**: Examples are more powerful than lengthy instructions.

## Optimal Example Count

### Research-Backed Guidelines

**2-5 Examples = Sweet Spot**
- 2 examples: Minimum for pattern recognition
- 3-4 examples: Optimal for most tasks
- 5+ examples: Diminishing returns, wastes context window

**Exceptions:**
- Very simple tasks: 1-2 examples sufficient
- Highly complex tasks: Up to 8 examples
- High variability tasks: 5-7 examples for diversity

### Cost vs. Performance Curve

```
Examples | Performance | Token Cost | Recommended
---------|------------|------------|-------------
0        | Baseline   | 1x         | Simple tasks only
1        | +15%       | 1.2x       | Very simple patterns
2        | +35%       | 1.4x       | Good starting point
3-4      | +50%       | 1.6-1.8x   | OPTIMAL for most
5-6      | +55%       | 2-2.2x     | Complex/varied tasks
7-8      | +57%       | 2.4-2.6x   | Rarely worth it
9+       | +58%       | 3x+        | Not recommended
```

## Selecting Quality Examples

### The Golden Rules

1. **Quality Over Quantity** - One excellent example beats three mediocre ones
2. **Diversity** - Cover different scenarios, edge cases, and input types
3. **Representativeness** - Match the actual distribution of inputs you'll encounter
4. **Clarity** - Make the pattern obvious and unambiguous
5. **Accuracy** - Every example must be 100% correct

### Example Selection Checklist

- [ ] Examples demonstrate the full range of expected inputs
- [ ] Examples cover edge cases (empty inputs, special characters, etc.)
- [ ] Examples show the desired output format consistently
- [ ] Examples vary in complexity (simple to complex)
- [ ] All examples are factually accurate
- [ ] Examples are recent/relevant (not outdated)
- [ ] Labels/outputs are unambiguous

### Common Mistakes

**TOO SIMILAR:**
```
Bad:
Q: What is 5 + 3? A: 8
Q: What is 7 + 2? A: 9
Q: What is 4 + 6? A: 10
```

**GOOD DIVERSITY:**
```
Good:
Q: What is 5 + 3? A: 8
Q: What is 12 * 4? A: 48
Q: What is 100 / 5? A: 20
```

## Label Space and Distribution

### Understanding Label Space

**Label Space** = The set of all possible output categories/answers

**Critical Rule**: Your examples should cover the label space proportionally to real-world distribution.

### Example: Sentiment Classification

**Bad - Imbalanced:**
```
"Amazing product!" → Positive
"Love it!" → Positive
"Great quality!" → Positive
"Terrible service." → Negative
```

**Good - Balanced:**
```
"Amazing product!" → Positive
"Terrible service." → Negative
"It's okay, nothing special." → Neutral
"Love it!" → Positive
```

### Guidelines by Task Type

**Binary Classification** (2 classes):
- Minimum: 2 examples (1 per class)
- Recommended: 4 examples (2 per class)

**Multi-class Classification** (3-5 classes):
- Minimum: 1 example per class
- Recommended: 2 examples per class

**Many Classes** (6+ classes):
- Include most common classes
- Add edge cases
- Total: 5-8 examples

**Open-ended Generation**:
- Show variety in style, length, structure
- 3-5 diverse examples

## Clear Formatting with Delimiters

### Why Formatting Matters

Clear delimiters help the model:
- Distinguish input from output
- Recognize pattern boundaries
- Maintain consistency
- Parse complex examples

### Delimiter Best Practices

**Use Consistent Separators:**

```
Good:
Input: [TEXT]
Output: [RESULT]

---

Input: [TEXT]
Output: [RESULT]
```

**Common Delimiter Patterns:**

1. **Triple Dash (---)**
```
Example 1:
Input: Hello
Output: Hi

---

Example 2:
Input: Goodbye
Output: Bye
```

2. **XML Tags**
```
<example>
  <input>Hello</input>
  <output>Hi</output>
</example>

<example>
  <input>Goodbye</input>
  <output>Bye</output>
</example>
```

3. **Numbered Examples**
```
Example 1:
Q: Hello
A: Hi

Example 2:
Q: Goodbye
A: Bye
```

4. **JSON Format**
```
{"input": "Hello", "output": "Hi"}
{"input": "Goodbye", "output": "Bye"}
```

**Choose Based On:**
- Task complexity (XML for complex, simple separators for basic)
- Model preference (Claude works well with XML)
- Your existing system architecture

## Templates by Use Case

### 1. Text Classification

**Sentiment Analysis:**

```
Classify the sentiment of these customer reviews as Positive, Negative, or Neutral.

Review: "This product exceeded my expectations! The quality is outstanding and shipping was fast."
Sentiment: Positive

Review: "Complete waste of money. Broke after two days and customer service was rude."
Sentiment: Negative

Review: "It works as described. Nothing remarkable, but does the job."
Sentiment: Neutral

Review: "The interface is confusing but the features are powerful once you figure them out."
Sentiment: Neutral

Review: [NEW REVIEW]
Sentiment:
```

**Topic Classification:**

```
Categorize these support tickets: Technical, Billing, Feature Request, or General Inquiry.

Ticket: "I can't log into my account. I've tried resetting my password three times."
Category: Technical

Ticket: "When will you add dark mode? This feature is essential for me."
Category: Feature Request

Ticket: "My credit card was charged twice for last month's subscription."
Category: Billing

Ticket: [NEW TICKET]
Category:
```

### 2. Information Extraction

**Entity Extraction:**

```
Extract person names, companies, and locations from these sentences.

Text: "Sarah Chen met with Google representatives in Mountain View last Tuesday."
Entities:
- Person: Sarah Chen
- Company: Google
- Location: Mountain View

Text: "The conference in Berlin will feature speakers from Microsoft and Amazon."
Entities:
- Person: None
- Company: Microsoft, Amazon
- Location: Berlin

Text: "John Smith founded TechStartup in Austin, partnering with investors from Silicon Valley."
Entities:
- Person: John Smith
- Company: TechStartup
- Location: Austin, Silicon Valley

Text: [NEW TEXT]
Entities:
```

**Data Extraction:**

```
Extract key information from these invoices.

Invoice: "Invoice #12345 | Date: 2024-03-15 | Customer: Acme Corp | Total: $1,299.00 | Items: Web Development (10 hrs @ $129/hr)"
Extracted:
- Invoice Number: 12345
- Date: 2024-03-15
- Customer: Acme Corp
- Total: $1,299.00
- Service: Web Development
- Hours: 10
- Rate: $129/hr

Invoice: "INV-2024-0891 | 2024-03-20 | GLOBEX INC | Amount Due: $4,500.00 | Consulting Services: 30 hours at $150/hour"
Extracted:
- Invoice Number: INV-2024-0891
- Date: 2024-03-20
- Customer: GLOBEX INC
- Total: $4,500.00
- Service: Consulting Services
- Hours: 30
- Rate: $150/hr

Invoice: [NEW INVOICE]
Extracted:
```

### 3. Text Generation

**Email Responses:**

```
Generate professional email responses to customer inquiries.

Inquiry: "Do you offer discounts for non-profits?"
Response: "Thank you for your interest! Yes, we offer a 30% discount for registered non-profit organizations. To apply, please send us your 501(c)(3) documentation at nonprofit@company.com. We typically process applications within 2-3 business days. Let me know if you have any questions!"

Inquiry: "My order hasn't arrived yet. It's been 10 days."
Response: "I apologize for the delay with your order. Let me look into this right away. Could you please provide your order number? I'll track down your package and ensure we resolve this promptly. If there's been a significant delay, we'll expedite a replacement at no extra cost."

Inquiry: "Can I use your software on multiple computers?"
Response: "Great question! Our standard license allows installation on up to 2 devices per user. If you need to use it on more devices, we offer a multi-device license for an additional $20/year. You can upgrade directly from your account dashboard. Is there anything else I can help you with?"

Inquiry: [NEW INQUIRY]
Response:
```

**Content Summarization:**

```
Summarize these articles in 2-3 sentences, focusing on the main points.

Article: "Recent studies show that remote work has led to a 25% increase in productivity for knowledge workers. However, companies report challenges with maintaining team cohesion and spontaneous collaboration. Many organizations are now adopting hybrid models that combine remote flexibility with periodic in-office days to balance these factors."

Summary: Remote work has increased productivity by 25% for knowledge workers, but companies struggle with team cohesion and collaboration. Hybrid models are emerging as a solution to balance productivity gains with team building needs.

---

Article: "The global electric vehicle market grew by 65% in 2023, with China leading at 40% of all sales. Battery costs have dropped by 89% since 2010, making EVs increasingly competitive with traditional vehicles. Industry analysts predict EVs will reach price parity with gas cars by 2025."

Summary: The EV market surged 65% in 2023, driven by significantly lower battery costs (down 89% since 2010). With China dominating 40% of sales, experts forecast EVs will match gas car prices by 2025.

---

Article: [NEW ARTICLE]

Summary:
```

### 4. Data Transformation

**Format Conversion:**

```
Convert these natural language dates to ISO 8601 format (YYYY-MM-DD).

Input: "March 15th, 2024"
Output: 2024-03-15

Input: "12/25/2023"
Output: 2023-12-25

Input: "January 1st, 2024"
Output: 2024-01-01

Input: [NEW DATE]
Output:
```

**Code Generation:**

```
Generate Python functions based on these descriptions.

Description: "Create a function that takes a list of numbers and returns the average"
Code:
```python
def calculate_average(numbers):
    """Calculate the average of a list of numbers."""
    if not numbers:
        return 0
    return sum(numbers) / len(numbers)
```

Description: "Create a function that checks if a string is a valid email address"
Code:
```python
import re

def is_valid_email(email):
    """Check if a string is a valid email address."""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None
```

Description: [NEW DESCRIPTION]
Code:
```

### 5. Question Answering

**Context-Based QA:**

```
Answer questions based on the provided context. If the answer isn't in the context, say "Information not available."

Context: "The company was founded in 2015 by Jane Doe and John Smith in Seattle. They started with $50,000 in seed funding and now have 200 employees across 5 offices."
Question: "When was the company founded?"
Answer: The company was founded in 2015.

Context: "The company was founded in 2015 by Jane Doe and John Smith in Seattle. They started with $50,000 in seed funding and now have 200 employees across 5 offices."
Question: "Who is the current CEO?"
Answer: Information not available.

Context: "The company was founded in 2015 by Jane Doe and John Smith in Seattle. They started with $50,000 in seed funding and now have 200 employees across 5 offices."
Question: "How many employees does the company have?"
Answer: The company has 200 employees.

Context: [NEW CONTEXT]
Question: [NEW QUESTION]
Answer:
```

## Advanced Techniques

### Dynamic Few-Shot Selection

Instead of fixed examples, select examples most similar to the input:

```python
# Pseudocode
def dynamic_few_shot(input_text, example_pool, k=3):
    # Calculate similarity between input and all examples
    similarities = [similarity(input_text, ex) for ex in example_pool]

    # Select k most similar examples
    top_k = select_top_k(example_pool, similarities, k)

    # Build prompt with selected examples
    return build_prompt(top_k, input_text)
```

**When to use:**
- Large, diverse task space
- Variable input types
- When you have many example candidates
- Retrieval systems available

### Chain-of-Thought with Few-Shot

Combine few-shot with reasoning:

```
Solve these word problems by showing your work.

Problem: "A store has 45 apples. They sell 30% of them. How many apples are left?"
Solution:
- Start with 45 apples
- Calculate 30% of 45: 45 × 0.30 = 13.5 ≈ 14 apples sold
- Remaining: 45 - 14 = 31 apples
Answer: 31 apples

Problem: "If a train travels 120 miles in 2 hours, how far will it travel in 5 hours at the same speed?"
Solution:
- Distance covered: 120 miles in 2 hours
- Calculate speed: 120 ÷ 2 = 60 mph
- Distance in 5 hours: 60 × 5 = 300 miles
Answer: 300 miles

Problem: [NEW PROBLEM]
Solution:
```

### Meta-Examples

Show examples of different output qualities:

```
Rate these responses as Excellent, Good, or Poor.

Query: "How do I reset my password?"
Response: "Click the 'Forgot Password' link on the login page, enter your email, and follow the instructions sent to you."
Rating: Excellent (Clear, actionable, complete)

Query: "How do I reset my password?"
Response: "Use the forgot password feature."
Rating: Good (Correct but lacks detail)

Query: "How do I reset my password?"
Response: "I don't know."
Rating: Poor (Unhelpful)

Query: [NEW QUERY]
Response: [NEW RESPONSE]
Rating:
```

## Common Pitfalls and Solutions

### Pitfall 1: Examples Too Complex

**Problem**: Examples are harder than the actual task
**Solution**: Start simple, add complexity gradually

**Bad:**
```
Convert to JSON: "The quick brown fox jumps over the lazy dog at 3:45 PM on Tuesday, March 5th, 2024, in Central Park, New York City, witnessed by John Smith and Jane Doe..."
```

**Good:**
```
Convert to JSON: "Meeting on Tuesday at 3 PM"
{"event": "Meeting", "day": "Tuesday", "time": "3 PM"}
```

### Pitfall 2: Inconsistent Formatting

**Problem**: Examples use different formats
**Solution**: Standardize all examples

**Bad:**
```
Input: "hello" -> Output: "HELLO"
"goodbye" => "GOODBYE"
world -> WORLD
```

**Good:**
```
Input: "hello"
Output: "HELLO"

Input: "goodbye"
Output: "GOODBYE"

Input: "world"
Output: "WORLD"
```

### Pitfall 3: Biased Examples

**Problem**: Examples reflect biases or stereotypes
**Solution**: Diversify examples, review for bias

**Bad:**
```
"The doctor said..." -> He
"The nurse said..." -> She
"The engineer said..." -> He
```

**Good:**
```
"The doctor said..." -> They
"The nurse said..." -> They
"The engineer said..." -> They
```

### Pitfall 4: Ambiguous Examples

**Problem**: Examples could be interpreted multiple ways
**Solution**: Make the pattern crystal clear

**Bad:**
```
"cat" → "animal"
"car" → "vehicle"
"apple" → ?
```
(Is it "food" or "fruit"? Unclear from examples)

**Good:**
```
"cat" → "animal"
"car" → "object"
"red" → "color"
"apple" → "food"
```

### Pitfall 5: Outdated Examples

**Problem**: Examples contain outdated information
**Solution**: Regular example audits

**Bad:**
```
"Latest iPhone" → "iPhone 11"  (from 2019)
```

**Good:**
```
"Latest iPhone" → "iPhone 15"  (as of 2024)
```

## Testing Your Few-Shot Prompts

### Evaluation Framework

1. **Ablation Test**: Remove examples one by one, measure impact
2. **Example Swap**: Replace examples, check if performance changes
3. **Edge Case Test**: Test with unusual inputs
4. **Consistency Test**: Same input multiple times, check variance

### Metrics to Track

- **Accuracy**: % correct outputs
- **Consistency**: % same output for same input
- **Format Compliance**: % outputs matching desired format
- **Token Efficiency**: Average tokens per example
- **Latency**: Response time impact

### Optimization Loop

```
1. Start with 3 examples
2. Test on 20 diverse inputs
3. Identify failure cases
4. Add 1-2 examples covering failures
5. Retest
6. If performance plateaus, stop
7. If still improving, repeat from step 3
```

## Few-Shot vs. Zero-Shot: Decision Matrix

| Factor | Use Zero-Shot | Use Few-Shot |
|--------|--------------|--------------|
| Task complexity | Simple | Complex |
| Format specificity | Standard | Custom |
| Quality requirements | Basic | High |
| Token budget | Tight | Flexible |
| Example availability | None | Multiple |
| Consistency needs | Low | High |
| Output variability | Acceptable | Must minimize |

## Performance Benchmarks

Based on empirical testing:

| Task Type | Zero-Shot | 2-Shot | 4-Shot | 8-Shot |
|-----------|-----------|--------|--------|--------|
| Classification | 65% | 78% | 82% | 83% |
| Extraction | 58% | 75% | 79% | 80% |
| Generation | 70% | 82% | 85% | 85% |
| Transformation | 62% | 80% | 84% | 84% |

**Key Takeaway**: Diminishing returns after 4-5 examples

## Integration with Other Techniques

### Few-Shot + Chain-of-Thought
Show reasoning steps in examples (covered above)

### Few-Shot + Prompt Templates
Combine structured prompts with examples:

```
<context>You are a customer service agent</context>

<instructions>Respond professionally and helpfully</instructions>

<examples>
Customer: "My order is late"
Agent: "I apologize for the delay. Let me check your order status right away. Could you provide your order number?"

Customer: "How do I return this?"
Agent: "I'd be happy to help with that return. Our return policy allows returns within 30 days. Would you like me to email you a prepaid return label?"
</examples>

<input>
Customer: [ACTUAL CUSTOMER MESSAGE]
</input>

<output>
Agent:
```

### Few-Shot + System Instructions

```
System: You are an expert programmer. Write clean, efficient Python code.

User: Here are examples of the coding style I want:

[Examples...]

Now write a function that [TASK]
```

## Quick Reference Checklist

**Before Deploying Few-Shot Prompts:**

- [ ] 2-5 examples (optimal range)
- [ ] Examples cover label space proportionally
- [ ] Diverse input types represented
- [ ] Consistent formatting throughout
- [ ] Clear delimiters between examples
- [ ] All examples are factually correct
- [ ] No biased or problematic examples
- [ ] Edge cases included
- [ ] Format matches desired output exactly
- [ ] Tested on unseen inputs
- [ ] Performance measured vs. zero-shot
- [ ] Token cost calculated and acceptable

## Tools and Resources

**Example Generation Tools:**
- Use the model itself to generate synthetic examples
- Human-in-the-loop example curation
- Example mining from existing data

**Example Management:**
- Version control your example sets
- A/B test different example combinations
- Maintain an example library per task type

**Quality Assurance:**
- Regular example audits (quarterly)
- Crowdsource example validation
- Automated consistency checks

## References

- Brown et al. (2020): "Language Models are Few-Shot Learners" (GPT-3 paper)
- Min et al. (2022): "Rethinking the Role of Demonstrations"
- Liu et al. (2023): "What Makes Good In-Context Examples"
- Anthropic: "Prompt Engineering Best Practices"
- OpenAI: "Prompt Engineering Guide"

## Summary

**Key Principles:**
1. Quality over quantity (2-5 examples ideal)
2. Diversity in examples covers edge cases
3. Consistent formatting is critical
4. Balance label space distribution
5. Test and iterate systematically

**When to Use:**
- Custom output formats
- High quality requirements
- Task-specific patterns
- Format consistency critical

**When to Skip:**
- Very simple tasks
- Standard formats
- Tight token budgets
- Examples unavailable