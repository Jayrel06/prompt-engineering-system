# Model-Specific Prompting Patterns

Different LLMs respond better to different prompting techniques. This guide covers optimizations for each major model family.

## Claude (Anthropic)

### Strengths
- Excellent at following complex, structured instructions
- Strong reasoning with chain-of-thought
- Handles long context well
- Good at maintaining persona/role consistency

### Optimal Patterns

#### 1. XML Tag Structure
Claude is trained to recognize and respect XML-like tags for structure.

```xml
<role>You are a senior software architect.</role>

<context>
We're building a microservices system for e-commerce.
Current stack: Node.js, PostgreSQL, Redis.
</context>

<task>
Design the authentication service architecture.
</task>

<constraints>
- Must handle 10K concurrent users
- Sub-100ms response time
- GDPR compliant
</constraints>

<output_format>
Provide:
1. Architecture diagram (text-based)
2. Key components and their responsibilities
3. Data flow for login process
4. Security considerations
</output_format>
```

#### 2. Prefilling (Claude API)
Start Claude's response to guide format and tone.

```python
# API call with prefilled assistant response
response = client.messages.create(
    model="claude-sonnet-4-20250514",
    messages=[
        {"role": "user", "content": "Analyze this code for bugs..."},
        {"role": "assistant", "content": "## Bug Analysis\n\n### Critical Issues\n1."}
    ]
)
```

#### 3. Explicit Thinking
Claude responds well to being asked to think explicitly.

```
Before answering, think through:
1. What are the key factors?
2. What could go wrong?
3. What's the simplest solution?

Then provide your recommendation.
```

#### 4. Role + Mission + Boundaries
```xml
<role>
You are a code reviewer for a fintech company.
</role>

<mission>
Review code for security vulnerabilities and best practices.
Prioritize issues by severity.
</mission>

<boundaries>
- Only comment on actual issues, not style preferences
- Don't rewrite code unless critical
- Flag but don't fix business logic concerns
</boundaries>
```

### Anti-patterns for Claude
- Don't use "ignore previous instructions" type prompts
- Avoid excessive flattery or manipulation attempts
- Don't ask Claude to pretend it has no guidelines

---

## GPT-4 / GPT-4o (OpenAI)

### Strengths
- Strong at creative tasks
- Good function calling / structured outputs
- Handles multi-turn conversation well
- Strong at code generation

### Optimal Patterns

#### 1. System Message Structure
GPT-4 heavily weighs the system message.

```
System: You are an expert Python developer specializing in FastAPI.
You write clean, well-documented code following PEP 8.
When generating code, always include type hints and docstrings.
For complex functions, add inline comments.

User: Create an authentication middleware...
```

#### 2. Markdown Formatting
GPT responds well to markdown structure in prompts.

```markdown
# Task
Build a rate limiter middleware

## Requirements
- Token bucket algorithm
- Redis backend
- Configurable limits per endpoint

## Constraints
- Must be async
- Thread-safe
- < 5ms latency overhead

## Output Format
```python
# Complete implementation
```
```

#### 3. Function Calling
Use structured function definitions for reliable output format.

```python
tools = [{
    "type": "function",
    "function": {
        "name": "analyze_sentiment",
        "description": "Analyze sentiment of text",
        "parameters": {
            "type": "object",
            "properties": {
                "sentiment": {"type": "string", "enum": ["positive", "negative", "neutral"]},
                "confidence": {"type": "number", "minimum": 0, "maximum": 1},
                "key_phrases": {"type": "array", "items": {"type": "string"}}
            },
            "required": ["sentiment", "confidence"]
        }
    }
}]
```

#### 4. Few-Shot with Markdown
```markdown
## Examples

### Input
"The product arrived damaged and customer service was unhelpful."

### Output
- Sentiment: negative
- Issues: [product quality, customer service]
- Priority: high

---

### Input
"Quick delivery, exactly as described. Will buy again!"

### Output
- Sentiment: positive
- Issues: []
- Priority: low

---

Now analyze this review:
"The item works fine but shipping took forever."
```

### Anti-patterns for GPT-4
- Very long system messages can get truncated in importance
- Avoid contradictory instructions (it picks one arbitrarily)
- Don't rely on "memory" of much earlier in long conversations

---

## Gemini (Google)

### Strengths
- Excellent multimodal capabilities
- Strong at grounded/factual responses
- Good at structured data extraction
- Native Google Search integration

### Optimal Patterns

#### 1. Grounding with Sources
```
Search for and provide the latest information on [topic].

For each claim, indicate:
- Source of information
- Date of information
- Confidence in accuracy

If information might be outdated, note this.
```

#### 2. Structured JSON Output
Gemini handles JSON output very reliably.

```
Analyze this text and return JSON:

{
  "entities": [{"name": "", "type": "", "relevance": 0.0}],
  "topics": [""],
  "sentiment": {"score": 0.0, "magnitude": 0.0},
  "language": ""
}

Text: [your text here]
```

#### 3. Multimodal Prompts
```
Look at this image and:
1. Describe what you see
2. Identify any text
3. Note any potential issues or concerns
4. Suggest improvements if applicable

Image: [image data]
```

#### 4. Step-by-Step with Verification
```
Solve this problem step by step.
After each step, verify your work before continuing.
If you find an error, correct it and continue.

Problem: [problem description]
```

### Anti-patterns for Gemini
- Avoid asking for real-time information without grounding
- Don't expect strong persona consistency across long conversations
- Avoid complex nested XML (JSON works better)

---

## Llama / Open Source Models

### Strengths
- Customizable via fine-tuning
- Can run locally for privacy
- Often good at specific domains after training
- No content restrictions (if desired)

### Optimal Patterns

#### 1. Clear Instruction Format
```
### Instruction:
{task description}

### Input:
{input data}

### Response:
```

#### 2. Alpaca Format
```
Below is an instruction that describes a task, paired with an input that provides further context. Write a response that appropriately completes the request.

### Instruction:
{instruction}

### Input:
{input}

### Response:
```

#### 3. ChatML Format
```
<|im_start|>system
You are a helpful coding assistant.
<|im_end|>
<|im_start|>user
Write a Python function to...
<|im_end|>
<|im_start|>assistant
```

#### 4. Keep It Simple
Open source models often perform better with simpler prompts.

```
Task: Summarize this article in 3 bullet points.

Article:
{article text}

Summary:
-
```

### Anti-patterns for Open Source
- Very complex multi-step instructions often fail
- Long context can degrade quality significantly
- Avoid expecting strong reasoning on smaller models

---

## Model Selection Guide

| Task Type | Best Model | Reason |
|-----------|------------|--------|
| Complex reasoning | Claude Opus | Best at multi-step logic |
| Code generation | GPT-4 / Claude Sonnet | Strong code capabilities |
| Structured extraction | Gemini | Reliable JSON output |
| Creative writing | GPT-4 / Claude | Strong creative abilities |
| Multimodal | Gemini / GPT-4o | Native multimodal training |
| Cost-sensitive | Claude Haiku / GPT-4o-mini | Good quality/cost ratio |
| Privacy-required | Llama (local) | No data leaves your system |
| Long documents | Claude | 200K context window |

---

## Temperature Guidelines

| Temperature | Use Case | Model Notes |
|-------------|----------|-------------|
| 0.0 | Factual extraction, code | All models: deterministic |
| 0.3-0.5 | Balanced tasks | Good default for most |
| 0.7 | Creative with structure | Claude/GPT: good variety |
| 1.0+ | Brainstorming | Can get incoherent |

---

## Quick Reference

### Claude
- Use XML tags for structure
- Prefill responses for format control
- Ask for explicit reasoning
- Works great with long context

### GPT-4
- Strong system message
- Markdown formatting
- Function calling for structure
- Good at creative tasks

### Gemini
- JSON output preferred
- Use grounding for facts
- Strong multimodal
- Step-by-step with verification

### Open Source
- Simple, clear instructions
- Use model-specific formats
- Keep prompts shorter
- Test extensively
