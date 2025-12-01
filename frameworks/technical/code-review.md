# Code Review Framework

## Purpose
Systematically review code for correctness, security, performance, maintainability, and style to improve code quality and share knowledge.

## When to Use
- Before merging any code changes
- When reviewing pull requests
- During pair programming sessions
- For knowledge transfer
- Quality assurance checkpoints

---

## The Process

### Stage 1: Context Understanding
Understand what you're reviewing and why.

**Read first:**
- PR/commit description
- Related issue or ticket
- Design documents if available
- Previous related changes

**Questions to answer:**
- What problem does this solve?
- What approach was taken?
- Why this approach vs alternatives?
- What's the scope of changes?

**Scope check:**
- Changes are focused on stated goal
- No unrelated modifications
- Appropriate size (not too large)

**Red flags:**
- PR description is vague or missing
- Mixing unrelated changes
- Massive PR (>500 lines without good reason)

### Stage 2: Correctness Review
Does the code do what it's supposed to do?

**Functional correctness:**
- [ ] Implements the stated requirements
- [ ] Handles expected inputs correctly
- [ ] Edge cases are covered
- [ ] Error conditions are handled
- [ ] No obvious logic errors

**Test coverage:**
- [ ] Tests exist for new code
- [ ] Tests cover happy path
- [ ] Tests cover error cases
- [ ] Tests cover edge cases
- [ ] Tests are meaningful (not just coverage theater)

**Integration:**
- [ ] Works with existing code
- [ ] Doesn't break existing functionality
- [ ] APIs used correctly
- [ ] Dependencies are appropriate

**Data handling:**
- [ ] Data validation is present
- [ ] Data transformations are correct
- [ ] No data loss
- [ ] Preserves data integrity

**Questions to ask:**
- What happens if this input is null/empty/invalid?
- What happens if this API call fails?
- Are all return paths handled?
- Could this cause race conditions?

### Stage 3: Security Review
Could this introduce vulnerabilities?

**Input validation:**
- [ ] All user input is validated
- [ ] Input sanitization where needed
- [ ] Size/length limits enforced
- [ ] Type checking is strict

**Authentication & Authorization:**
- [ ] Authentication is required where needed
- [ ] Authorization checks are present
- [ ] Permissions are verified
- [ ] No privilege escalation possible

**Data protection:**
- [ ] Sensitive data is encrypted
- [ ] No secrets in code
- [ ] No logging of sensitive information
- [ ] SQL injection prevented (parameterized queries)
- [ ] XSS prevented (output encoding)

**Common vulnerabilities (OWASP Top 10):**
- [ ] No injection flaws
- [ ] No broken authentication
- [ ] No sensitive data exposure
- [ ] No XXE (XML External Entities)
- [ ] No broken access control
- [ ] No security misconfiguration
- [ ] No XSS
- [ ] No insecure deserialization
- [ ] No components with known vulnerabilities
- [ ] Logging and monitoring present

**Cryptography:**
- [ ] Using standard libraries, not custom crypto
- [ ] Appropriate algorithms
- [ ] Proper key management
- [ ] No hardcoded keys

### Stage 4: Performance Review
Will this perform well at scale?

**Algorithmic efficiency:**
- [ ] Appropriate algorithm choice
- [ ] Time complexity is reasonable
- [ ] Space complexity is reasonable
- [ ] No unnecessary iterations

**Database queries:**
- [ ] No N+1 queries
- [ ] Proper indexing considered
- [ ] Query limits are set
- [ ] Batch operations where appropriate

**Resource usage:**
- [ ] No memory leaks
- [ ] Resources are freed/closed
- [ ] Connection pooling used
- [ ] Caching where beneficial

**Scalability concerns:**
- [ ] Will this work with 10x data?
- [ ] Will this work with 10x users?
- [ ] Are there bottlenecks?
- [ ] Can this be parallelized if needed?

**Anti-patterns:**
- Loading entire tables into memory
- Synchronous operations that should be async
- Polling instead of event-driven
- Redundant database calls
- Excessive logging in hot paths

**Note:** Premature optimization is bad, but obvious performance issues should be caught.

### Stage 5: Maintainability Review
Can others (including future you) work with this?

**Code clarity:**
- [ ] Code is self-explanatory
- [ ] Variable names are clear
- [ ] Function names describe what they do
- [ ] Complex logic has comments
- [ ] No magic numbers (use named constants)

**Code structure:**
- [ ] Functions are focused (do one thing)
- [ ] Appropriate abstraction level
- [ ] No deeply nested logic
- [ ] No excessive function length
- [ ] Proper separation of concerns

**Error handling:**
- [ ] Errors have clear messages
- [ ] Appropriate error types used
- [ ] Stack traces preserved
- [ ] Recovery is possible where appropriate

**Documentation:**
- [ ] Public APIs are documented
- [ ] Complex algorithms explained
- [ ] Non-obvious decisions justified
- [ ] Update relevant docs (README, etc.)

**Dependencies:**
- [ ] Dependencies are necessary
- [ ] Dependencies are maintained
- [ ] Versions are pinned appropriately
- [ ] License compatibility

**Testability:**
- [ ] Code is testable
- [ ] No hidden dependencies
- [ ] Proper dependency injection
- [ ] Mocking is possible where needed

### Stage 6: Style and Conventions Review
Does it follow project standards?

**Code style:**
- [ ] Follows project style guide
- [ ] Consistent formatting
- [ ] Naming conventions followed
- [ ] Linter passes (if applicable)

**Project patterns:**
- [ ] Follows established patterns in codebase
- [ ] Architecture decisions consistent
- [ ] Similar problems solved similarly
- [ ] No unnecessary divergence

**Git hygiene:**
- [ ] Commit messages are clear
- [ ] Commits are logical units
- [ ] No secrets in commit history
- [ ] No debug code or commented-out code

**Minor issues:**
- Spelling errors in comments
- Inconsistent spacing
- Console.log statements left in
- TODO comments (should be tracked elsewhere)

**Note:** Style issues are lowest priority. Automate with formatters when possible.

### Stage 7: Provide Feedback
Give constructive, actionable feedback.

**Feedback principles:**
- Be kind and constructive
- Explain why, not just what
- Distinguish critical vs optional
- Suggest improvements, don't demand
- Praise good work

**Feedback format:**
```
**Critical:** [Issue that must be fixed]
Reason: [Why this is important]
Suggestion: [How to fix it]

**Question:** [Something unclear]
Context: [Why you're asking]

**Nit:** [Minor improvement]
Optional: [This is not blocking]

**Praise:** [Something done well]
Why it's good: [Learning opportunity]
```

**Priority labels:**
- 🔴 **Blocking:** Must fix before merge
- 🟡 **Important:** Should fix, can be follow-up
- 🔵 **Optional:** Nice to have, author decides
- 🟢 **Praise:** Highlight good work

**Example comments:**
- 🔴 "This SQL query is vulnerable to injection. Use parameterized queries instead."
- 🟡 "This could be more efficient with a hash map instead of linear search."
- 🔵 "Consider extracting this to a helper function for reusability."
- 🟢 "Nice error handling here - clear messages and proper recovery."

---

## Output Format

Provide review feedback as:

1. **Summary**
   - Overall assessment (Approve / Request Changes / Comment)
   - Key concerns or blockers
   - Estimated re-review time needed

2. **Critical Issues** (🔴 Blocking)
   - Security vulnerabilities
   - Correctness bugs
   - Major performance problems

3. **Important Issues** (🟡 Should fix)
   - Maintainability concerns
   - Missing tests
   - Unclear code

4. **Suggestions** (🔵 Optional)
   - Style improvements
   - Refactoring opportunities
   - Alternative approaches

5. **Positive Feedback** (🟢 Praise)
   - What was done well
   - Good patterns to encourage
   - Learning opportunities

---

## Code Review Best Practices

### For Reviewers

**Be thorough but efficient:**
- Focus on high-impact issues first
- Don't nitpick formatting (use auto-formatters)
- Review in reasonable time (<24 hours)

**Be constructive:**
- Assume good intent
- Ask questions, don't make accusations
- Teach, don't just critique
- Acknowledge constraints

**Be consistent:**
- Apply standards evenly
- Don't accept things you'd reject elsewhere
- Link to style guides/docs

**Know when to discuss offline:**
- Complex design discussions
- Philosophical disagreements
- When async comments pile up

### For Authors

**Make review easy:**
- Small, focused PRs
- Clear description and context
- Self-review first
- Respond to comments promptly

**Take feedback well:**
- Don't take it personally
- Ask for clarification if unclear
- Push back respectfully if you disagree
- Mark resolved comments

**Update and iterate:**
- Fix blocking issues first
- Communicate if you disagree
- Request re-review when ready

---

## Review Checklist

Quick checklist for reviewers:

**Correctness:**
- [ ] Does what it's supposed to
- [ ] Tests exist and pass
- [ ] Edge cases handled

**Security:**
- [ ] Input validated
- [ ] Auth/authz present
- [ ] No obvious vulnerabilities

**Performance:**
- [ ] No obvious bottlenecks
- [ ] Scales reasonably
- [ ] Resources managed properly

**Maintainability:**
- [ ] Code is clear
- [ ] Structure is good
- [ ] Documentation present

**Style:**
- [ ] Follows conventions
- [ ] Consistent with codebase
- [ ] Linter passes

**Ready to merge:**
- [ ] All blockers resolved
- [ ] Tests pass
- [ ] Documentation updated
- [ ] No merge conflicts

---

## When to Escalate

**Skip detailed review:**
- Trivial changes (typo fixes, formatting)
- Auto-generated code
- Emergency hotfixes (but review after)

**Request additional reviewers:**
- Security-critical changes
- Unfamiliar area of codebase
- Architectural changes
- Performance-critical code

**Escalate to team discussion:**
- Disagreement on approach
- New patterns being introduced
- Trade-offs that affect multiple areas
- Technical debt decisions

---

## Common Review Mistakes

**Reviewer mistakes:**
- Rubber-stamping without reading
- Focusing only on style, missing logic issues
- Being overly critical or pedantic
- Not providing actionable feedback
- Reviewing while tired/rushed

**Author mistakes:**
- PRs that are too large
- Missing context/description
- Not self-reviewing first
- Defensive responses to feedback
- Not testing before requesting review

**Process mistakes:**
- Reviews taking too long
- Unclear review standards
- Inconsistent enforcement
- No automation (linting, testing)
- Review bottlenecks
