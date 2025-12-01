# Code Generation Chain

A 5-stage prompt chain that transforms requirements into production-ready code.

## Overview

```
[Requirements] → Stage 1: Clarify → Stage 2: Architecture → Stage 3: Implement → Stage 4: Review → Stage 5: Test → [Production Code]
```

## Stage 1: Requirements Clarification

**Purpose:** Ensure complete understanding before writing any code.

```xml
<role>You are a senior software architect who excels at requirements analysis.</role>

<task>
Analyze these requirements and identify gaps:

Requirements:
{{requirements}}

Produce:
1. **Restated Requirements** - In your own words, what needs to be built?

2. **Clarifying Questions** - What's ambiguous or missing?
   - Mark as [BLOCKING] if we can't proceed without answer
   - Mark as [ASSUMPTION] if we can proceed with stated assumption

3. **Scope Boundaries**
   - What's IN scope
   - What's explicitly OUT of scope

4. **Technical Constraints**
   - Language/framework: {{tech_stack}}
   - Performance requirements
   - Security considerations

5. **Success Criteria**
   - How do we know this is "done"?
</task>

<output_format>
If there are [BLOCKING] questions, stop and list them.
Otherwise, state assumptions and proceed.
End with: "Requirements clear. Core deliverable: [one sentence]"
</output_format>
```

---

## Stage 2: Architecture Design

**Purpose:** Design the solution before implementation.

```xml
<role>You are a software architect designing for maintainability and scalability.</role>

<context>
{{stage_1_output}}
</context>

<task>
Design the architecture:

1. **High-Level Design**
   - Components and their responsibilities
   - How they interact (data flow)

2. **File Structure**
   ```
   /proposed/structure/here
   ```

3. **Key Interfaces**
   - Public APIs/functions
   - Data structures/types

4. **Dependencies**
   - External libraries needed
   - Why each is necessary

5. **Edge Cases**
   - What could go wrong?
   - How will we handle it?

6. **Alternative Approaches Considered**
   - What else could work?
   - Why this approach is better
</task>

<output_format>
Include code snippets for interfaces/types.
End with: "Architecture ready. Starting with: [first component]"
</output_format>
```

---

## Stage 3: Implementation

**Purpose:** Write the actual code.

```xml
<role>You are a senior developer who writes clean, documented code.</role>

<context>
Architecture:
{{stage_2_output}}

Standards:
- Follow {{coding_style}} conventions
- Include type hints/annotations
- Add docstrings for public functions
- Handle errors explicitly
</context>

<task>
Implement the solution:

1. Write each file completely (no placeholders like "// TODO" or "...")
2. Include all imports
3. Add inline comments for complex logic
4. Follow the DRY principle but don't over-abstract

For each file, use this format:
```{{language}}
# filename: path/to/file.ext

[complete code here]
```
</task>

<output_format>
Produce complete, runnable code.
End with: "Implementation complete. Files created: [list]"
</output_format>
```

---

## Stage 4: Code Review

**Purpose:** Self-review for quality and issues.

```xml
<role>You are a code reviewer focused on bugs, security, and best practices.</role>

<context>
{{stage_3_output}}
</context>

<task>
Review this code for:

1. **Bugs & Logic Errors**
   - Off-by-one errors
   - Null/undefined handling
   - Race conditions

2. **Security Issues**
   - Input validation
   - Injection vulnerabilities
   - Sensitive data exposure

3. **Performance**
   - Unnecessary loops
   - Memory leaks
   - N+1 queries

4. **Best Practices**
   - Code organization
   - Naming clarity
   - Error handling

5. **Maintainability**
   - Is it readable?
   - Would a new developer understand it?

For each issue found:
- Severity: [CRITICAL/HIGH/MEDIUM/LOW]
- Location: [file:line]
- Issue: [description]
- Fix: [code snippet]
</task>

<output_format>
If CRITICAL issues found, provide fixed code.
End with: "Review complete. Issues found: X critical, Y high, Z medium"
</output_format>
```

---

## Stage 5: Test Generation

**Purpose:** Create comprehensive tests.

```xml
<role>You are a QA engineer who writes thorough, maintainable tests.</role>

<context>
Final code:
{{stage_4_output}}
</context>

<task>
Generate tests covering:

1. **Unit Tests**
   - Each public function
   - Edge cases identified in architecture
   - Error conditions

2. **Integration Tests** (if applicable)
   - Component interactions
   - External service mocking

3. **Test Cases Format**
   - Arrange: Setup
   - Act: Execute
   - Assert: Verify

Include:
- Happy path tests
- Error/exception tests
- Boundary condition tests
</task>

<output_format>
```{{language}}
# filename: tests/test_[module].ext

[complete test code]
```

End with:
**Test Coverage:** [estimate]
**Confidence:** [HIGH/MEDIUM/LOW]
**Run tests with:** [command]
</output_format>
```

---

## Usage Example

```bash
prompt chain code-generation \
  --requirements "Build a rate limiter middleware for Express.js" \
  --tech-stack "Node.js, TypeScript, Redis" \
  --coding-style "Airbnb" \
  --language "typescript"
```

## Chain Configuration

```json
{
  "name": "code-generation",
  "stages": 5,
  "variables": {
    "requirements": "required",
    "tech_stack": "required",
    "coding_style": "optional, default: 'standard'",
    "language": "required"
  },
  "pass_full_context": false,
  "pass_previous_stage": true,
  "model_recommendations": {
    "stage_1": "claude-sonnet-4-20250514",
    "stage_2": "claude-sonnet-4-20250514",
    "stage_3": "claude-sonnet-4-20250514",
    "stage_4": "claude-sonnet-4-20250514",
    "stage_5": "claude-sonnet-4-20250514"
  }
}
```
