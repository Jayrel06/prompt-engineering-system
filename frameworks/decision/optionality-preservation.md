# Optionality Preservation Framework

## Purpose
Evaluate decisions based on how they affect future choices. Sometimes the best decision is the one that keeps the most good options available.

## When to Use
- Early-stage decisions with high uncertainty
- Strategic choices about direction
- Technology/architecture decisions
- Resource allocation decisions
- When the future is unclear but commitment is required

---

## The Process

### Stage 1: Map Current Options
What choices are available right now?

**List all realistic options:**
| Option | Description | Appeal | Concerns |
|--------|-------------|--------|----------|
| A | | | |
| B | | | |
| C | | | |

**For each option, identify:**
- What does this enable?
- What does this foreclose?
- How reversible is it?
- What information would make this clearly right/wrong?

### Stage 2: Analyze Future Option Space
How does each choice affect what you can do next?

**For each current option:**

**Options it opens:**
- New paths available after this
- Capabilities gained
- Relationships/resources acquired

**Options it closes:**
- Paths no longer available
- Bridges burned
- Commitments that constrain

**Options it preserves:**
- Decisions you can still make later
- Flexibility maintained
- Multiple futures still possible

**Mapping template:**
```
If we choose [Option A]:
  → Enables: [Future option 1], [Future option 2]
  → Forecloses: [Future option 3], [Future option 4]
  → Preserves: [Future option 5], [Future option 6]
```

### Stage 3: Assess Cost of Keeping Options Open
What's the price of waiting or hedging?

**Delay costs:**
- Market opportunity lost
- Competitive disadvantage
- Team morale/momentum
- Literal cost (money, time)

**Hedging costs:**
- Resource split across options
- Lack of focus
- Increased complexity
- Reduced depth in any direction

**Information value:**
- What could we learn by waiting?
- How much would that information improve the decision?
- How long to get that information?

**Calculation:**
```
Value of waiting = (Expected value of better decision) - (Cost of delay)

If positive: Wait or hedge
If negative: Commit now
```

### Stage 4: Evaluate Option Value
What's each preserved option worth?

**For each option you could keep open:**

**Upside if it becomes right:**
- Best case value
- Probability it's the right choice
- Time horizon when you'd know

**Cost to keep available:**
- Resources required
- Opportunity cost
- Complexity added

**Expected value:**
```
Option value = (Upside if right × Probability) - (Cost to keep open)
```

**Prioritize:** Keep options open with highest expected value.

### Stage 5: Consider Timing
When must this decision be made?

**Decision timing:**
- Latest point we can decide
- Information we'll have then vs now
- Cost increase of deciding later
- Risk of being too late

**Commitment spectrum:**
```
Full Flexibility ← → Partial Commitment ← → Full Commitment

[Small reversible test] → [Pilot program] → [Full rollout]
```

**Staged commitment:**
- What's the minimum commitment now?
- What would trigger next stage?
- What would cause reversal?

### Stage 6: Design for Optionality
How can we structure the decision to preserve options?

**Strategies:**

**Modular architecture:**
- Build in swappable components
- Avoid deep integration
- Interface-based design

**Reversible first steps:**
- Start with what can be undone
- Delay irreversible parts
- Create off-ramps

**Parallel exploration:**
- Run small experiments simultaneously
- Learn before committing
- Kill losers early

**Flexible agreements:**
- Short contracts over long
- Pilot before scale
- Clear exit clauses

**Platform thinking:**
- Build foundation that supports multiple strategies
- Invest in capabilities, not just features
- Create composable pieces

### Stage 7: Make the Decision
Choose, but thoughtfully.

**Decision framework:**

**High value of optionality + Can afford to wait:**
→ **Preserve options, delay commitment**

**High value of optionality + Can't afford to wait:**
→ **Choose option that preserves most future options**

**Low value of optionality + Clear best choice:**
→ **Commit fully, move fast**

**Low value of optionality + Uncertain best choice:**
→ **Make smallest commitment that lets you learn**

**Document:**
- Decision made
- Options preserved
- Options foreclosed
- Trigger points for reconsideration
- What would change this decision

---

## Output Format

1. **Decision Context**
   - What we're deciding
   - Why it matters
   - Uncertainty factors

2. **Option Analysis**
   - Current options available
   - Future option space for each
   - Options opened/closed/preserved

3. **Optionality Value Assessment**
   - Cost of keeping options open
   - Value of preserved flexibility
   - Expected value calculation

4. **Timing Analysis**
   - Latest decision point
   - Information we'll gain by waiting
   - Cost of delay

5. **Recommendation**
   - Chosen approach
   - Commitment level (full/partial/minimal)
   - Optionality preserved
   - Future decision points

6. **Contingencies**
   - What would trigger reassessment
   - Exit strategies if needed
   - Hedging strategies if applicable

---

## Optionality Principles

### Real Options Thinking
Like financial options, strategic options have:
- **Value:** Upside if exercised
- **Cost:** Price to keep available
- **Expiration:** Window when decision must be made
- **Exercise price:** Cost to commit when ready

### When Optionality Matters Most
- **High uncertainty:** Future is unclear
- **Rapid change:** Environment evolving
- **Asymmetric outcomes:** Big upside, limited downside
- **Early stage:** Premature commitment is costly

### When to Ignore Optionality
- **Clear best choice:** One option obviously better
- **Cost of waiting high:** First-mover advantage
- **Commitment enables:** Can't learn without commitment
- **Team needs direction:** Analysis paralysis setting in

---

## Common Optionality Patterns

### Good: Preserving Options
- **Build platforms, not point solutions**
  - Platform enables multiple products
  - Point solution locks into one approach

- **Start with small reversible tests**
  - Learn before committing
  - Kill bad ideas cheap

- **Use standard technologies**
  - Easy to find help
  - Easy to switch if needed

- **Hire generalists early**
  - Can do multiple things
  - Flexibility as strategy emerges

### Bad: False Optionality
- **Keeping dead options alive**
  - "Maybe we'll need this someday"
  - Adds complexity, no real value

- **Paralysis disguised as optionality**
  - Can't decide, call it preserving options
  - Indecision is not strategy

- **Hedging when commitment needed**
  - Spreading too thin
  - Nothing gets done well

- **Ignoring opportunity cost**
  - Optionality has cost
  - Sometimes committing is better

---

## Examples

### High Optionality Value
**Situation:** Early startup choosing tech stack
- **Decision:** Use well-supported, standard technologies
- **Rationale:** Easier to hire, easier to change later
- **Options preserved:** Can pivot without rewrite

**Situation:** Growing company, potential big client
- **Decision:** Build flexible solution, not custom one-off
- **Rationale:** Client might churn, opportunity cost high
- **Options preserved:** Can serve other clients, not locked in

### Low Optionality Value
**Situation:** Clear product-market fit, ready to scale
- **Decision:** Commit fully to current market
- **Rationale:** Optionality less valuable than focus
- **Trade-off:** Foreclose other markets, win this one

**Situation:** Competitive market, first-mover advantage
- **Decision:** Launch now with current feature set
- **Rationale:** Cost of waiting exceeds value of perfecting
- **Trade-off:** Commit to direction, iterate in market

### Structured Optionality
**Situation:** Uncertain regulatory environment
- **Decision:** Modular compliance architecture
- **Rationale:** Regulations will change, don't know how
- **Options preserved:** Can adapt as regulations evolve

**Situation:** Might need to scale 100x, might not
- **Decision:** Build for 10x, architect for 100x
- **Rationale:** Pay small premium now for big option later
- **Options preserved:** Can scale if needed, not over-engineered if not
