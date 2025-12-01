# Prompt Engineering Research

## Key Techniques

### 1. Chain-of-Thought (CoT) Prompting

**Description:** Encouraging the model to show its reasoning step-by-step before providing a final answer. This improves accuracy on complex reasoning tasks.

**When to Use:**
- Math problems and calculations
- Multi-step logical reasoning
- Complex analysis requiring intermediate steps
- Tasks where showing work improves accuracy

**Example Pattern:**
```
Let's approach this step-by-step:
1. First, identify the key elements of the problem
2. Then, analyze each element
3. Consider how they interact
4. Finally, synthesize into a conclusion
```

**Variants:**
- **Zero-shot CoT:** Add "Let's think step by step" to any prompt
- **Few-shot CoT:** Provide examples with reasoning chains
- **Auto-CoT:** Let the model generate its own reasoning chains
- **Self-Consistency:** Generate multiple reasoning paths and take majority answer

**Source:** Wei et al., "Chain-of-Thought Prompting Elicits Reasoning in Large Language Models" (2022)

---

### 2. Few-Shot vs Zero-Shot Optimization

**Description:** Providing examples (few-shot) vs relying on instruction-following alone (zero-shot).

**When to Use Few-Shot:**
- Specific output format requirements
- Domain-specific tasks
- When examples clarify intent better than instructions
- Tasks with nuanced style requirements

**When to Use Zero-Shot:**
- Simple, clear tasks
- When context window is limited
- Exploratory tasks where examples might constrain
- Tasks where model's default behavior is acceptable

**Optimization Strategy:**
1. Start with zero-shot
2. If quality insufficient, add 2-3 high-quality examples
3. Ensure examples are diverse and representative
4. Place examples near the end of prompt (recency effect)

**Source:** Brown et al., "Language Models are Few-Shot Learners" (2020)

---

### 3. Meta-Prompting

**Description:** Using prompts to generate or improve other prompts. The model becomes a prompt engineer.

**When to Use:**
- Building prompt libraries at scale
- Optimizing existing prompts
- Generating task-specific variations
- Self-improving systems

**Example Pattern:**
```
You are an expert prompt engineer. Given this task description:
[TASK]

Generate an optimized prompt that:
1. Clearly defines the role and context
2. Specifies the exact output format
3. Includes relevant constraints
4. Anticipates edge cases
```

**Advanced Techniques:**
- **APE (Automatic Prompt Engineer):** Generate candidates, evaluate, select best
- **OPRO:** Use optimization trajectory as context for generating better prompts
- **DSPy:** Programmatic prompt optimization with automatic tuning

**Source:** Zhou et al., "Large Language Models Are Human-Level Prompt Engineers" (2022)

---

### 4. Constitutional AI Principles

**Description:** Training AI to follow a set of principles that guide behavior, enabling self-critique and improvement.

**When to Use:**
- Building safety-conscious systems
- Self-improving prompt chains
- Creating consistent AI personalities
- Establishing behavioral guardrails

**Implementation Pattern:**
```
Before responding, evaluate your answer against these principles:
1. Is it helpful and accurate?
2. Does it avoid harm?
3. Is it honest about uncertainty?
4. Does it respect the user's intent?

If any principle is violated, revise your response.
```

**Source:** Anthropic, "Constitutional AI: Harmlessness from AI Feedback" (2022)

---

### 5. DSPy Framework

**Description:** A programmatic framework for building and optimizing LLM pipelines. Treats prompts as code, not strings.

**Key Concepts:**
- **Signatures:** Declarative specifications of input/output
- **Modules:** Reusable prompt components
- **Optimizers:** Automatic prompt tuning (COPRO, MIPROv2, SIMBA)
- **Assertions:** Runtime constraints on outputs

**When to Use:**
- Complex multi-step pipelines
- Systems requiring optimization over time
- Production systems needing reliability
- Research and experimentation

**Example:**
```python
class GenerateAnswer(dspy.Signature):
    """Answer questions with detailed explanations."""
    context = dspy.InputField(desc="relevant context")
    question = dspy.InputField()
    answer = dspy.OutputField(desc="detailed answer")

class RAG(dspy.Module):
    def __init__(self):
        self.retrieve = dspy.Retrieve(k=3)
        self.generate = dspy.ChainOfThought(GenerateAnswer)

    def forward(self, question):
        context = self.retrieve(question).passages
        return self.generate(context=context, question=question)
```

**Source:** DSPy Documentation, Stanford NLP

---

### 6. OPRO (Optimization by PROmpting)

**Description:** Using LLMs as optimizers. The model receives a trajectory of previous attempts and their scores, then generates improved prompts.

**When to Use:**
- Systematic prompt improvement
- When you can measure prompt quality
- Iterative refinement workflows
- A/B testing at scale

**Process:**
1. Define evaluation metric
2. Generate initial prompt candidates
3. Evaluate each candidate
4. Feed results back to model as context
5. Generate new candidates based on trajectory
6. Repeat until convergence

**Source:** Yang et al., "Large Language Models as Optimizers" (Google DeepMind, 2023)

---

### 7. Structured Output Patterns

**Description:** Techniques for ensuring consistent, parseable outputs.

**Patterns:**
- **JSON Mode:** Request structured JSON output
- **XML Tags:** Use tags for clear section boundaries
- **Markdown:** Leverage headers and formatting
- **Schema Definition:** Provide exact output schema

**Example:**
```
Respond in this exact JSON format:
{
  "summary": "one sentence summary",
  "key_points": ["point 1", "point 2"],
  "confidence": 0.0-1.0,
  "next_steps": ["action 1", "action 2"]
}
```

---

## Testing Frameworks Comparison

| Feature | Promptfoo | LangSmith | Braintrust |
|---------|-----------|-----------|------------|
| **Open Source** | Yes | No | Partial |
| **Self-Hosted** | Yes | No | Yes |
| **CI/CD Integration** | Excellent | Good | Excellent |
| **Evaluation Types** | LLM-as-judge, deterministic, custom | LLM-as-judge, custom | LLM-as-judge, custom |
| **Red Teaming** | Built-in | Manual | Manual |
| **Cost** | Free | Paid | Freemium |
| **Best For** | Security testing, regression | LangChain users, observability | Production CI/CD |

### Promptfoo
- **Strengths:** Open source, excellent security testing, easy CI/CD integration
- **Weaknesses:** Less polished UI, requires more setup
- **Use When:** Need security testing, want self-hosted, budget-conscious

### LangSmith
- **Strengths:** Tight LangChain integration, good observability, managed service
- **Weaknesses:** Vendor lock-in, cost at scale
- **Use When:** Already using LangChain, want managed service

### Braintrust
- **Strengths:** Production-grade, excellent CI/CD, good UX
- **Weaknesses:** Less community, newer tool
- **Use When:** Need production deployment pipeline, CI/CD focus

---

## Context Management Strategies

### RAG Best Practices

1. **Hybrid Search:** Combine keyword (BM25) with semantic (vector) search
2. **Query Classification:** Route simple queries differently than complex ones
3. **Chunk Optimization:** 512-1024 tokens per chunk, with overlap
4. **Metadata Filtering:** Use structured metadata for pre-filtering
5. **Reranking:** Use cross-encoder for final ranking
6. **Context Compression:** Summarize or extract relevant portions
7. **Citation Tracking:** Maintain provenance for retrieved content

### Context Window Optimization

1. **Prompt Caching:** Reuse static context across calls
2. **Progressive Disclosure:** Start minimal, expand if needed
3. **Compression:** Use summarization for long documents
4. **Chunking Strategy:** Place most relevant content at end (recency)
5. **Token Budgeting:** Allocate tokens by importance

### Memory Systems

1. **Short-term:** Conversation history within session
2. **Long-term:** Vector database for persistent knowledge
3. **Working:** Scratchpad for intermediate reasoning
4. **Episodic:** Specific interaction memories
5. **Semantic:** Conceptual knowledge graph

---

## Anti-Patterns to Avoid

### 1. Vague Instructions
**Bad:** "Write something good about the topic"
**Good:** "Write a 200-word summary highlighting 3 key benefits for small business owners"

### 2. Overloaded Prompts
**Bad:** Trying to accomplish 5 things in one prompt
**Good:** Break into focused sub-tasks, chain results

### 3. No Output Format Specification
**Bad:** "Analyze this data"
**Good:** "Analyze this data. Return as JSON with fields: insights (array), confidence (0-1), recommendations (array)"

### 4. Ignoring Model Limitations
**Bad:** Expecting perfect math or real-time information
**Good:** Use tools for math, acknowledge knowledge cutoff

### 5. Not Iterating
**Bad:** Accept first output
**Good:** Build feedback loops, request revisions, use self-critique

### 6. Overly Complex Single Prompts
**Bad:** 2000-word prompt trying to cover everything
**Good:** Modular prompts with clear handoffs

### 7. Not Testing Edge Cases
**Bad:** Only testing happy path
**Good:** Test with adversarial inputs, edge cases, ambiguous queries

### 8. Treating AI as Infallible
**Bad:** Blindly trusting all outputs
**Good:** Build verification steps, especially for factual claims

---

## References

- Anthropic Prompt Engineering Guide: https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering
- DSPy Documentation: https://dspy-docs.vercel.app/
- Promptfoo Documentation: https://promptfoo.dev/docs
- "Chain-of-Thought Prompting" (Wei et al., 2022)
- "Constitutional AI" (Anthropic, 2022)
- "Large Language Models as Optimizers" (Google DeepMind, 2023)
