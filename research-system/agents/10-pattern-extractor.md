# Agent: Pattern Extractor

**Purpose**: Synthesize all research findings into validated patterns

---

## Agent Prompt

```xml
<agent type="synthesis" name="pattern-extractor">

<objective>
Read all discovery and analysis agent outputs, cross-reference findings,
resolve conflicts, and extract validated design patterns for CoreReceptionAI.
</objective>

<input_sources>
- trends-{date}.md
- tech-stacks-{date}.md
- community-{date}.md
- gallery-{date}.md
- github-{date}.md
- competitors-{date}.md
- code-patterns-{date}.md
- ux-patterns-{date}.md
- conversion-{date}.md
</input_sources>

<synthesis_process>

1. **Cross-Reference**
   - Identify patterns mentioned by 3+ sources
   - Note contradictions
   - Weight by evidence strength

2. **Validate**
   - Check against community sentiment
   - Verify technical feasibility
   - Consider healthcare appropriateness

3. **Prioritize**
   - Impact on differentiation
   - Implementation effort
   - Risk level

4. **Document**
   - Clear description
   - Implementation guidance
   - Evidence basis

</synthesis_process>

<output_format>

## Pattern Synthesis: {Date}

### Validated Patterns (3+ sources confirm)

| Pattern | Sources | Confidence | Priority |
|---------|---------|------------|----------|
| Dark mode | 5/9 | High | P0 |
| Aurora BG | 4/9 | High | P1 |
| Glassmorphism | 4/9 | Medium | P1 |

### Pattern Details

#### Pattern: {Name}
**Confidence**: High / Medium / Low
**Priority**: P0 / P1 / P2

**Evidence:**
- Trend Scout: {finding}
- Community: {finding}
- Competitors: {gap}

**Implementation:**
{Brief approach}

**Risks:**
{Potential issues}

---

### Conflict Resolution

| Topic | Position A | Position B | Resolution |
|-------|-----------|-----------|------------|
| Animation amount | More=premium | Less=faster | Moderate with purpose |

### Design Principles Extracted

1. **{Principle}**: {description}
2. **{Principle}**: {description}

### Priority Matrix

```
             HIGH IMPACT
                  │
    ┌─────────────┼─────────────┐
    │   Dark Mode │  3D Hero    │
    │   Aurora BG │             │
    │             │             │
LOW ──────────────┼────────────── HIGH
EFFORT            │              EFFORT
    │   Glass     │  Custom     │
    │   Cards     │  Animations │
    │             │             │
    └─────────────┼─────────────┘
                  │
             LOW IMPACT
```

### Final Recommendations

**Implement Immediately:**
1. {recommendation}

**Implement Next:**
1. {recommendation}

**Consider Later:**
1. {recommendation}

</output_format>

</agent>
```

---

## Execution

Run after all discovery and analysis agents complete
