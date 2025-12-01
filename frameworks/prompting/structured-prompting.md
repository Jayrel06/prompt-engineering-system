# Structured Prompting Framework

## Overview

Structured prompting is the practice of organizing prompt components in a clear, consistent format that helps the model understand context, task requirements, and expected outputs. Well-structured prompts significantly improve response quality, consistency, and reliability.

## Why Structure Matters

**Unstructured Prompt Problems:**
- Model misunderstands the task
- Ignores important context
- Produces inconsistent formats
- Misses critical requirements

**Structured Prompt Benefits:**
- Clear task boundaries
- Predictable output format
- Higher success rate
- Easier debugging
- Better maintainability

**Performance Impact:**
- 30-40% improvement in task completion
- 50% reduction in format errors
- 2x better instruction following

## Core Frameworks

### 1. CARE Framework

**C**ontext - **A**ction - **R**esult - **E**valuate

The CARE framework provides a complete prompt structure that guides the model through understanding, execution, and verification.

#### Components

**Context**: Background information the model needs
- Who is involved
- What situation/domain
- Relevant constraints
- Important background facts

**Action**: What the model should do
- Specific task description
- Step-by-step instructions
- Processing requirements
- Edge case handling

**Result**: What the output should look like
- Format specification
- Required components
- Quality criteria
- Length/scope

**Evaluate**: How to verify success
- Success criteria
- Common mistakes to avoid
- Validation checks
- Quality indicators

#### Template

```
CONTEXT:
[Provide relevant background]

ACTION:
[Describe what to do]

RESULT:
[Specify expected output]

EVALUATE:
[Define success criteria]
```

#### Example: Customer Support Response

```
CONTEXT:
You are a customer support agent for TechCo, a software company. Our return policy allows returns within 30 days with proof of purchase. We prioritize customer satisfaction and professional communication.

ACTION:
Respond to this customer inquiry about returns. Be empathetic, provide clear instructions, and offer solutions. If information is missing, politely ask for it.

Customer Message: "I want to return my purchase but I lost the receipt."

RESULT:
Provide a professional email response that:
- Acknowledges the customer's situation
- Explains our return policy
- Offers alternative solutions (e.g., looking up purchase via email)
- Maintains a helpful, friendly tone
- Ends with clear next steps

EVALUATE:
The response should:
- Be empathetic (not dismissive)
- Offer at least one alternative solution
- Not violate company policy
- Be 100-150 words
- Include a clear call-to-action
```

#### Example: Code Review

```
CONTEXT:
You are reviewing a Python function for a production web application. The codebase follows PEP 8 style guidelines and prioritizes readability and error handling.

ACTION:
Review this code for:
1. Bugs and logical errors
2. Security vulnerabilities
3. Performance issues
4. Style and readability
5. Missing error handling

CODE:
[code snippet here]

RESULT:
Provide:
1. Overall assessment (Approve / Request Changes / Reject)
2. Critical issues (must fix before merge)
3. Suggestions (nice-to-have improvements)
4. Positive highlights (what's done well)

Format each finding as:
- **Type**: [Bug/Security/Performance/Style]
- **Severity**: [Critical/High/Medium/Low]
- **Issue**: [Description]
- **Fix**: [Specific suggestion]

EVALUATE:
A good review:
- Identifies actual issues (not nitpicking)
- Provides actionable feedback
- Includes code examples for fixes
- Balances criticism with praise
- Prioritizes by severity
```

### 2. RTF Framework

**R**ole - **T**ask - **F**ormat

A simpler framework for straightforward tasks where context is minimal.

#### Components

**Role**: Who the model should act as
- Defines expertise level
- Sets tone and style
- Establishes perspective
- Clarifies limitations

**Task**: What needs to be done
- Clear, specific objective
- Any constraints or requirements
- Input data/context
- Success criteria

**Format**: How to structure the output
- Output structure
- Required sections
- Data format (JSON, markdown, etc.)
- Length and style

#### Template

```
ROLE:
You are a [specific role with expertise].

TASK:
[Specific task description and requirements]

FORMAT:
[Expected output structure]
```

#### Example: Content Creation

```
ROLE:
You are a technical content writer specializing in developer documentation. You write clear, concise explanations with practical examples.

TASK:
Write a tutorial introduction for "Getting Started with REST APIs." The audience is developers new to APIs. Cover what REST is, why it matters, and a simple example. Target reading time: 3 minutes.

FORMAT:
Structure your response as:

# Title

## What is REST?
[2-3 sentence explanation]

## Why Use REST APIs?
[3-4 bullet points]

## Simple Example
[Basic code example with explanation]

## Next Steps
[2-3 actionable items]
```

#### Example: Data Analysis

```
ROLE:
You are a data analyst with expertise in business metrics and data visualization.

TASK:
Analyze this sales data and identify the top 3 insights that should concern the executive team. Focus on trends, anomalies, and actionable patterns.

DATA:
[sales data here]

FORMAT:
For each insight:

**Insight [N]: [Title]**
- **What**: [Description of the finding]
- **Why it matters**: [Business impact]
- **Data**: [Supporting numbers]
- **Recommendation**: [Specific action]
```

### 3. Task-First Ordering

Place the most important instruction first, followed by supporting details.

#### Why Order Matters

Models give more weight to:
1. Beginning of prompt (primacy effect)
2. End of prompt (recency effect)
3. Middle of prompt gets less attention

**Optimal Structure:**
1. Primary task (what to do)
2. Output format
3. Context and background
4. Examples
5. Edge cases and constraints

#### Bad Ordering

```
Here's some background about our company. We were founded in 2010 and have 500 employees. We value customer service. Our mission is to provide excellent products. Our return policy is 30 days. We ship worldwide.

By the way, please write a product description for our new coffee maker.

It should be engaging and highlight the features. Keep it under 100 words. Use a friendly tone. Make it SEO-friendly.
```

#### Good Ordering

```
Write a 100-word product description for our new coffee maker. Use a friendly, engaging tone and make it SEO-friendly.

REQUIRED ELEMENTS:
- Highlight key features (programmable timer, thermal carafe, auto-shutoff)
- Include keywords: "coffee maker," "programmable," "thermal carafe"
- End with a call-to-action

BRAND CONTEXT:
We value quality and customer satisfaction. Our products combine functionality with elegant design. Founded in 2010, we're known for reliable kitchen appliances.
```

#### Template

```
PRIMARY TASK: [Main instruction]

OUTPUT FORMAT: [How to structure response]

CONTEXT: [Background information]

EXAMPLES: [If needed]

CONSTRAINTS: [Limitations and edge cases]
```

### 4. Output Primers / Prefilling

Start the model's response with specific text to control format and direction.

#### How Prefilling Works

Instead of:
```
User: Write a JSON object with name and age.
```

Use:
```
User: Write a JSON object with name and age.
Assistant (prefilled): {
  "name":
```

The model will complete from where you left off, ensuring proper JSON format.

#### Benefits of Prefilling

1. **Format Control**: Forces specific output structure
2. **Reduces Errors**: Less chance of format deviations
3. **Skips Preamble**: Model jumps straight to content
4. **Consistent Style**: Maintains uniform tone/format

#### Common Prefill Patterns

**JSON Output:**
```
User: Generate user data.
Assistant: {
  "users": [
```

**Markdown Structure:**
```
User: Write a blog post about AI.
Assistant: # The Future of AI

## Introduction

```

**Code Generation:**
```
User: Write a Python function to calculate factorial.
Assistant: ```python
def factorial(n):
```

**Structured Analysis:**
```
User: Analyze this data.
Assistant: **Summary**: 

Key findings:
1.
```

**XML/Tagged Output:**
```
User: Extract entities.
Assistant: <entities>
  <person>
```

### 5. Delimiter Usage

Use clear markers to separate different prompt components.

#### Why Delimiters Matter

Without delimiters:
```
Translate this to French. Context: you're a professional translator. The text is: Hello, how are you? Make it formal.
```

**Problems:**
- Unclear boundaries
- Model might translate "Context: you're..."
- Ambiguous instructions

With delimiters:
```
<context>
You are a professional translator.
</context>

<instruction>
Translate the following text to French. Use formal register.
</instruction>

<text>
Hello, how are you?
</text>
```

## Quick Reference

**Frameworks:**
- CARE: Context-Action-Result-Evaluate (comprehensive)
- RTF: Role-Task-Format (simple)
- Task-First: Priority-based organization

**Key Principles:**
1. Task first
2. Clear delimiters
3. Explicit format
4. Context last
5. Test and iterate

**Impact:**
- 30-40% better completion
- 50% fewer format errors
- Easier debugging
