# Architecture Design Framework

## Purpose
Design technical systems that are appropriate for the problem, maintainable, and avoid over-engineering.

## When to Use
- Starting new technical projects
- Refactoring existing systems
- Evaluating proposed architectures
- Technical decision-making

---

## The Process

### Stage 1: Understand Requirements

**Functional Requirements:**
- What must the system do?
- What are the core use cases?
- What data flows through the system?

**Non-Functional Requirements:**
- Performance (latency, throughput)
- Scalability (users, data volume)
- Reliability (uptime, error tolerance)
- Security (authentication, data protection)
- Maintainability (who maintains this?)

**Constraints:**
- Budget
- Timeline
- Team skills
- Existing systems
- Compliance requirements

### Stage 2: Identify Components

What are the major building blocks?

**Common patterns:**
- Frontend / Backend / Database
- API Gateway / Services / Storage
- Ingestion / Processing / Output
- Trigger / Logic / Action

**For each component:**
| Component | Responsibility | Inputs | Outputs |
|-----------|----------------|--------|---------|
| | | | |

### Stage 3: Design Data Flow

How does data move through the system?

```
[Source] → [Ingestion] → [Processing] → [Storage] → [Output]
```

**Consider:**
- Synchronous vs asynchronous
- Batch vs streaming
- Push vs pull
- Error handling at each step

### Stage 4: Choose Technologies

For each component, select appropriate technology.

| Component | Options | Selection | Rationale |
|-----------|---------|-----------|-----------|
| | | | |

**Selection criteria:**
- Does it solve the problem?
- Can the team use it effectively?
- Is it maintained and supported?
- Does it integrate with existing stack?
- What's the operational overhead?

### Stage 5: Plan for Failure

What happens when things go wrong?

**For each component:**
- What if it fails?
- How do we detect failure?
- How do we recover?
- What data could be lost?

### Stage 6: Consider Evolution

How will this change over time?

- What's the most likely scaling need?
- What features might be added?
- What would require major rework?

---

## Output Format

1. **Requirements Summary:** Functional, non-functional, constraints
2. **Component Diagram:** Visual representation
3. **Data Flow:** How information moves
4. **Technology Choices:** With rationale
5. **Failure Modes:** What can go wrong and how we handle it
6. **Future Considerations:** How this might evolve

---

## Architecture Principles

### Simplicity
- Start with the simplest thing that could work
- Add complexity only when required
- If you can't explain it simply, it's too complex

### Separation of Concerns
- Each component does one thing well
- Clear interfaces between components
- Changes isolated to relevant components

### Fail Gracefully
- Assume everything can fail
- Degrade gracefully rather than crash completely
- Make failures visible

### Evolution Over Perfection
- Design for current needs + reasonable growth
- Don't optimize for hypothetical scale
- Make it easy to change later
