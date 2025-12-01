# Coding Standards

## General Principles

### Readability Over Cleverness
- Code is read more than written
- Clear variable names
- Comments for "why", not "what"

### Simplicity Over Complexity
- Solve the problem, not theoretical future problems
- YAGNI (You Aren't Gonna Need It)
- Premature optimization is the root of evil

### Consistency
- Follow existing patterns in codebase
- Use linters and formatters
- Stick to one style per project

---

## Python

### Style
- PEP 8 compliance
- Black formatter
- Type hints for function signatures
- Docstrings for public functions

### Structure
```python
"""Module docstring explaining purpose."""

import standard_library
import third_party
import local_modules

CONSTANTS = "at_top"

class ClassName:
    """Class docstring."""

    def method_name(self, arg: str) -> bool:
        """Method docstring."""
        pass

def function_name(param: int) -> str:
    """Function docstring."""
    pass

if __name__ == "__main__":
    main()
```

### Naming
- `snake_case` for functions and variables
- `PascalCase` for classes
- `UPPER_CASE` for constants
- Descriptive names over short ones

---

## JavaScript/TypeScript

### Style
- ESLint + Prettier
- Prefer TypeScript for anything non-trivial
- Strict mode

### Naming
- `camelCase` for functions and variables
- `PascalCase` for classes and components
- `UPPER_CASE` for constants

### Best Practices
- Avoid `any` in TypeScript
- Use async/await over callbacks
- Destructure when it improves readability

---

## n8n Workflows

### Naming
- Workflow: `[Category] - Descriptive Name`
- Nodes: `Action - Target` (e.g., "Get - Customer Data")

### Structure
- Start with trigger node (clear entry point)
- Error handling on critical paths
- Notes explaining complex logic
- Sticky notes for section headers

### Best Practices
- One workflow, one purpose
- Use sub-workflows for reusable logic
- Environment variables for credentials
- Test with mock data before production

---

## Git

### Commit Messages
```
type: short description

Longer explanation if needed.
What changed and why.

Fixes #123
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation
- `refactor`: Code change without feature/fix
- `test`: Adding tests
- `chore`: Maintenance

### Branching
- `main`: Production-ready
- `feature/description`: New features
- `fix/description`: Bug fixes

### Pull Requests
- Clear description of changes
- Link to related issues
- Screenshots for UI changes
- Tests pass before merge

---

## Documentation

### README.md (Required)
- What it is
- How to install/setup
- How to use
- How to contribute

### Code Comments
- Explain "why", not "what"
- Document edge cases
- Mark TODOs with context

### API Documentation
- Request/response formats
- Error codes
- Authentication
- Examples

---

## Error Handling

### Principles
- Fail fast, fail loud
- Log errors with context
- Return meaningful error messages
- Don't swallow exceptions silently

### Pattern
```python
try:
    result = risky_operation()
except SpecificError as e:
    logger.error(f"Operation failed: {e}", extra={"context": data})
    raise UserFacingError("Something went wrong") from e
```

---

## Testing

### Philosophy
- Test behavior, not implementation
- Focus on critical paths
- Integration tests > unit tests for most cases

### When to Test
- Critical business logic
- Data transformations
- API contracts
- Regression prevention

### When Not to Over-Test
- Trivial getters/setters
- Framework code
- One-off scripts
