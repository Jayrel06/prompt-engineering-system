# Chain-of-Thought (CoT) Prompting Framework

## Overview

Chain-of-Thought prompting encourages the model to show its reasoning process step-by-step before arriving at a final answer. This technique dramatically improves performance on complex reasoning tasks by making the model's thought process explicit and verifiable.

## Core Concepts

### What is Chain-of-Thought?

CoT prompting asks the model to break down problems into intermediate reasoning steps, similar to how humans solve complex problems. Instead of jumping directly to an answer, the model explains its logic, calculations, and decision-making process.

**Benefits:**
- Improved accuracy on complex reasoning tasks (math, logic, common sense)
- Transparency in how the model arrives at conclusions
- Easier to identify and correct errors in reasoning
- Better performance on multi-step problems
- Reduces hallucination by forcing logical progression

## Techniques

### 1. Zero-Shot CoT

The simplest approach: add "Let's think step by step" or similar prompts.

**Trigger Phrases:**
- "Let's think step by step"
- "Let's work through this carefully"
- "Let's break this down"
- "Think through this step-by-step"
- "Explain your reasoning"

**Example:**

```
Question: A store has 15 apples. They sell 40% of them in the morning and then receive a delivery of 8 more apples. How many apples do they have now?

Let's think step by step:
```

**Model Response:**
```
Let's think step by step:

1. Start with 15 apples
2. Calculate 40% of 15: 15 × 0.40 = 6 apples sold
3. Remaining after morning sales: 15 - 6 = 9 apples
4. Add the delivery: 9 + 8 = 17 apples
5. Final answer: 17 apples
```

**When to Use:**
- Quick implementation without needing examples
- Straightforward reasoning tasks
- When you want to minimize prompt length
- Testing if CoT helps before investing in few-shot examples

### 2. Few-Shot CoT

Provide examples that demonstrate step-by-step reasoning.

**Example Template:**

```
Solve these math problems by showing your work step-by-step.

Q: Roger has 5 tennis balls. He buys 2 more cans of tennis balls. Each can has 3 tennis balls. How many tennis balls does he have now?

A: Let me work through this step-by-step:
1. Roger starts with 5 tennis balls
2. He buys 2 cans, each with 3 balls
3. New balls from cans: 2 × 3 = 6 tennis balls
4. Total: 5 + 6 = 11 tennis balls
Answer: 11 tennis balls

Q: The cafeteria had 23 apples. If they used 20 to make lunch and bought 6 more, how many apples do they have?

A: Let me work through this step-by-step:
1. Starting apples: 23
2. Apples used for lunch: 20
3. Remaining: 23 - 20 = 3 apples
4. New apples bought: 6
5. Total: 3 + 6 = 9 apples
Answer: 9 apples

Q: [YOUR QUESTION HERE]

A:
```

**Best Practices for Few-Shot CoT:**
- Use 2-4 examples (quality over quantity)
- Make reasoning steps explicit and numbered
- Show all calculations
- Keep consistent formatting
- Include diverse problem types
- Match example complexity to target task

### 3. Self-Consistency CoT

Generate multiple reasoning paths and select the most consistent answer.

**Implementation:**

```
Question: [COMPLEX PROBLEM]

Generate 3 different reasoning paths to solve this problem. Then compare them and provide the most reliable answer.

Reasoning Path 1:
[Let the model generate first approach]

Reasoning Path 2:
[Let the model generate second approach]

Reasoning Path 3:
[Let the model generate third approach]

Final Answer:
[Model selects the most consistent answer across paths]
```

**When to Use:**
- High-stakes decisions requiring verification
- Problems with multiple valid approaches
- When you need higher confidence in the answer
- Complex reasoning where errors are likely

**Trade-offs:**
- Increased token usage (3-5x)
- Longer response time
- Significantly improved accuracy

### 4. Least-to-Most Prompting

Break complex problems into simpler sub-problems, solve sequentially.

**Structure:**

```
Problem: [COMPLEX PROBLEM]

Step 1: Break this into smaller sub-problems
[List sub-problems]

Step 2: Solve each sub-problem
Sub-problem 1: [Solution]
Sub-problem 2: [Solution]
Sub-problem 3: [Solution]

Step 3: Combine solutions
[Final integrated answer]
```

**Example:**

```
Problem: Plan a 3-day trip to Tokyo with a $1000 budget, including flights, hotel, and activities.

Step 1: Break this into sub-problems
- Find flight costs
- Research hotel options
- Identify free/cheap activities
- Calculate meal budget
- Build daily itinerary

Step 2: Solve each sub-problem
Flight costs: Research average roundtrip prices...
Hotel options: Budget hotels in central locations...
Activities: Free temples, parks, affordable museums...
Meal budget: Street food and convenience stores...

Step 3: Combine into a cohesive plan
Day 1: [Detailed itinerary with costs]
Day 2: [Detailed itinerary with costs]
Day 3: [Detailed itinerary with costs]
Total: $950 (within budget)
```

## When to Use CoT

### Ideal Use Cases

**Complex Reasoning:**
- Multi-step math problems
- Logical deduction
- Symbolic reasoning
- Word problems

**Analysis Tasks:**
- Code debugging
- Ethical dilemmas
- Strategic planning
- Causal reasoning

**Decision Making:**
- Comparing multiple options
- Risk assessment
- Trade-off analysis

### When NOT to Use CoT

- Simple factual retrieval ("What is the capital of France?")
- Creative writing (may constrain creativity)
- Tasks requiring brevity
- When reasoning steps aren't helpful (simple classification)
- High-volume, low-complexity tasks (increases cost)

## Claude-Specific Optimizations

### XML Tags for Structure

```xml
<problem>
Calculate the compound interest on $1000 at 5% annual rate for 3 years.
</problem>

<reasoning>
Let me solve this step-by-step:

<step number="1">
Identify the variables:
- Principal (P): $1000
- Rate (r): 5% = 0.05
- Time (t): 3 years
- Formula: A = P(1 + r)^t
</step>

<step number="2">
Substitute values:
A = 1000(1 + 0.05)^3
A = 1000(1.05)^3
</step>

<step number="3">
Calculate:
1.05^3 = 1.157625
A = 1000 × 1.157625 = $1,157.63
</step>

<step number="4">
Calculate interest earned:
Interest = A - P = $1,157.63 - $1,000 = $157.63
</step>
</reasoning>

<answer>
The compound interest earned is $157.63, and the total amount is $1,157.63.
</answer>
```

### Prefilling for Consistency

Start the assistant's response to ensure proper formatting:

```
User: Solve this problem: If a train travels 120 miles in 2 hours, then speeds up and travels 180 miles in the next 2 hours, what is the average speed for the entire trip?

Assistant (prefilled): Let me work through this step-by-step:

Step 1:
```

## Advanced Techniques

### Progressive Refinement

Ask the model to review and improve its reasoning:

```
Problem: [COMPLEX PROBLEM]

First, solve this problem showing your reasoning.

[Model provides initial solution]

Now, review your answer. Are there any errors in logic or calculation? Provide a refined answer if needed.
```

### Meta-Reasoning

Have the model evaluate its own reasoning approach:

```
Problem: [PROBLEM]

Before solving, explain:
1. What type of problem is this?
2. What reasoning strategy is most appropriate?
3. What are potential pitfalls?

Then solve using that strategy.
```

## Template Library

### Basic Math Problem Template

```
Problem: [MATH PROBLEM]

Let's solve this step-by-step:

Step 1: Identify what we know
- [Variable 1]: [Value]
- [Variable 2]: [Value]

Step 2: Identify what we need to find
- [Target variable]

Step 3: Choose the appropriate formula
- [Formula]

Step 4: Substitute and calculate
- [Show calculations]

Step 5: Verify the answer
- [Check if answer makes sense]

Final Answer: [ANSWER]
```

### Logic Problem Template

```
Problem: [LOGIC PROBLEM]

Analysis:

Step 1: List the facts
- [Fact 1]
- [Fact 2]
- [Fact 3]

Step 2: Identify constraints
- [Constraint 1]
- [Constraint 2]

Step 3: Apply logical deduction
- From facts 1 and 2: [Inference]
- From constraint 1: [Inference]

Step 4: Reach conclusion
- [Conclusion with justification]

Answer: [ANSWER]
```

### Code Debugging Template

```
Problem: This code has a bug: [CODE]

Debugging Process:

Step 1: Understand the intended behavior
- [What should the code do?]

Step 2: Trace the execution
- Line X: [What happens]
- Line Y: [What happens]

Step 3: Identify the issue
- [Where the bug occurs]
- [Why it's a problem]

Step 4: Propose fix
- [Corrected code]
- [Explanation of why this fixes it]

Step 5: Verify
- [Test cases that now work]
```

### Decision Analysis Template

```
Decision: [DECISION TO MAKE]

Analysis:

Step 1: Define criteria
- [Criterion 1]: [Importance]
- [Criterion 2]: [Importance]
- [Criterion 3]: [Importance]

Step 2: Evaluate Option A
- [Criterion 1]: [Score/Rating + reasoning]
- [Criterion 2]: [Score/Rating + reasoning]
- [Criterion 3]: [Score/Rating + reasoning]

Step 3: Evaluate Option B
- [Criterion 1]: [Score/Rating + reasoning]
- [Criterion 2]: [Score/Rating + reasoning]
- [Criterion 3]: [Score/Rating + reasoning]

Step 4: Compare and recommend
- [Overall comparison]
- [Recommendation with justification]

Decision: [FINAL DECISION]
```

## Performance Benchmarks

Based on research and testing:

| Task Type | Baseline Accuracy | Zero-Shot CoT | Few-Shot CoT | Self-Consistency CoT |
|-----------|------------------|---------------|--------------|---------------------|
| Grade School Math | 45% | 65% | 78% | 85% |
| Logical Reasoning | 52% | 68% | 75% | 82% |
| Common Sense QA | 71% | 78% | 82% | 86% |
| Multi-hop Reasoning | 38% | 58% | 72% | 79% |

## Cost Considerations

**Token Usage:**
- Zero-shot CoT: 1.5-2x baseline
- Few-shot CoT: 2-3x baseline (due to examples)
- Self-consistency: 3-5x baseline (multiple generations)

**Optimization Tips:**
- Start with zero-shot CoT
- Use few-shot only when zero-shot underperforms
- Reserve self-consistency for critical decisions
- Cache common reasoning examples
- Use shorter reasoning steps when appropriate

## Common Pitfalls

1. **Over-engineering simple tasks** - Don't use CoT for "What is 2+2?"
2. **Inconsistent formatting** - Keep step structure uniform
3. **Too many examples** - 2-4 is optimal; more isn't better
4. **Skipping verification** - Always include a sense-check step
5. **Ignoring context window** - Long reasoning chains can hit limits
6. **Not adapting to model** - Different models have different strengths

## Testing Your CoT Prompts

### Checklist

- [ ] Does the prompt clearly request step-by-step reasoning?
- [ ] Are examples (if used) diverse and representative?
- [ ] Is the reasoning format consistent?
- [ ] Does it work on edge cases?
- [ ] Is it worth the increased token cost?
- [ ] Can errors in reasoning be easily spotted?

### A/B Testing Template

Test with and without CoT on a sample set:

```
Task: [TASK]
Sample size: 20 test cases

Without CoT:
- Accuracy: X%
- Avg tokens: Y
- Cost per 1000 queries: $Z

With CoT:
- Accuracy: X%
- Avg tokens: Y
- Cost per 1000 queries: $Z

Decision: [Worth it? / Not worth it?]
```

## Related Techniques

- **Tree of Thoughts**: Explores multiple reasoning branches
- **ReAct**: Combines reasoning with action-taking
- **Reflexion**: Adds self-reflection and learning
- **Chain-of-Verification**: Adds verification steps to reduce hallucination

## References and Further Reading

- Wei et al. (2022): "Chain-of-Thought Prompting Elicits Reasoning in Large Language Models"
- Wang et al. (2023): "Self-Consistency Improves Chain of Thought Reasoning"
- Zhou et al. (2023): "Least-to-Most Prompting"
- Anthropic Claude Prompt Engineering Guide
- OpenAI Prompt Engineering Best Practices

## Quick Reference

**When to use:**
- Complex multi-step problems
- Math, logic, reasoning tasks
- When transparency matters
- Debugging and analysis

**When to avoid:**
- Simple queries
- Creative writing
- Cost-sensitive, high-volume tasks
- Time-sensitive responses

**Best phrase:** "Let's think step by step"

**Optimal examples:** 2-4 for few-shot

**Cost multiplier:** 1.5x-5x depending on technique