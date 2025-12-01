# Prompt Engineering System - Testing Suite

Comprehensive automated testing for the prompt engineering system, including unit tests, prompt quality tests, and regression tests.

## Overview

This testing suite validates:
- **Context assembly logic** - Ensures context-loader.py works correctly
- **Prompt structure** - Validates frameworks and templates follow best practices
- **Prompt quality** - Tests actual LLM outputs against expected behaviors
- **Regression prevention** - Catches known issues before they reoccur

## Test Structure

```
tests/
├── test_context_loader.py      # Unit tests for context assembly
├── test_prompts.py              # Prompt structure and quality tests
├── promptfoo.yaml               # Base LLM evaluation tests
├── promptfoo-extended.yaml      # Extended regression tests
├── fixtures/                    # Test data
│   ├── sample_context.md        # Sample business context
│   ├── sample_framework.md      # Sample decision framework
│   └── sample_template.md       # Sample voice AI template
└── results/                     # Test outputs (auto-generated)
```

## Quick Start

### Install Dependencies

```bash
# Python dependencies
pip install pytest

# Node.js dependencies (for promptfoo)
npm install -g promptfoo
```

### Run All Tests

```bash
# Linux/Mac
./scripts/run_tests.sh

# Windows
scripts\run_tests.bat
```

### Run Specific Test Suites

```bash
# Only Python unit tests
./scripts/run_tests.sh --unit-only

# Only prompt quality tests
./scripts/run_tests.sh --prompt-only

# Include extended regression tests
./scripts/run_tests.sh --extended

# Verbose output
./scripts/run_tests.sh --verbose
```

## Test Categories

### 1. Unit Tests (Python)

**File:** `test_context_loader.py`

Tests the context assembly system:
- File loading and error handling
- Framework discovery
- Context mode selection
- Project context injection
- Template loading

**Run manually:**
```bash
cd tests
pytest test_context_loader.py -v
```

### 2. Prompt Structure Tests (Python)

**File:** `test_prompts.py`

Validates prompt quality without LLM calls:
- Required sections present
- Proper markdown formatting
- Consistent structure
- No broken links
- No placeholder text
- Adequate documentation

**Run manually:**
```bash
cd tests
pytest test_prompts.py -v
```

### 3. Prompt Quality Tests (Promptfoo)

**File:** `promptfoo.yaml`

Tests actual LLM outputs:
- Framework behavior (first principles, pre-mortem, etc.)
- Voice AI responses (emergency handling, appointments, etc.)
- Context assembly effectiveness
- Edge case handling
- Tone and style consistency

**Run manually:**
```bash
npx promptfoo eval -c tests/promptfoo.yaml
```

**View results:**
```bash
npx promptfoo view
```

### 4. Extended Regression Tests (Promptfoo)

**File:** `promptfoo-extended.yaml`

Additional tests for known issues:
- Over-apologizing
- Hallucinated information
- False urgency
- Response length

**Run manually:**
```bash
npx promptfoo eval -c tests/promptfoo-extended.yaml
```

## Test Fixtures

Sample test data in `fixtures/`:

- **sample_context.md** - Realistic business context for testing context injection
- **sample_framework.md** - Example decision framework for testing framework loading
- **sample_template.md** - Voice AI template for testing template assembly

## Writing New Tests

### Adding Unit Tests

Add to `test_context_loader.py` or `test_prompts.py`:

```python
def test_new_feature(self):
    """Test description."""
    result = function_to_test()
    assert expected_condition, "Error message"
```

### Adding Prompt Quality Tests

Add to `promptfoo.yaml`:

```yaml
- description: "Should handle new scenario"
  vars:
    customer_input: "Test input"
  assert:
    - type: llm-rubric
      value: "Response should demonstrate expected behavior"
    - type: contains
      value: "expected phrase"
```

### Test Assertion Types

Promptfoo supports various assertion types:

- `contains` - Output contains specific text
- `not-contains` - Output doesn't contain text
- `contains-any` - Output contains any of multiple options
- `llm-rubric` - LLM judges output against criteria
- `javascript` - Custom validation logic
- `regex` - Pattern matching

## Continuous Integration

To run tests in CI/CD:

```bash
# Exit on first failure
./scripts/run_tests.sh

# Check exit code
if [ $? -eq 0 ]; then
  echo "All tests passed"
else
  echo "Tests failed"
  exit 1
fi
```

## Interpreting Results

### Unit Test Results

```
test_context_loader.py::TestLoadFile::test_load_existing_file PASSED
test_context_loader.py::TestLoadFile::test_load_nonexistent_file PASSED
```

- **PASSED** - Test succeeded
- **FAILED** - Test failed (details shown)
- **SKIPPED** - Test skipped (conditional)

### Promptfoo Results

Results saved to `tests/results/`:
- `latest-eval.json` - Machine-readable results
- `latest-eval.html` - Human-readable report

**View interactive results:**
```bash
npx promptfoo view
```

## Common Issues

### pytest not found
```bash
pip install pytest
```

### promptfoo not found
```bash
npm install -g promptfoo
```

### Import errors in tests
```bash
# Ensure you're running from the tests directory
cd tests
pytest test_context_loader.py
```

### API rate limits
```bash
# Run with lower concurrency
npx promptfoo eval -c tests/promptfoo.yaml --max-concurrency 2
```

## Performance Benchmarks

Typical run times:
- Unit tests: ~5-10 seconds
- Prompt structure tests: ~5-10 seconds
- Base promptfoo tests: ~2-5 minutes (API calls)
- Extended tests: ~5-10 minutes (API calls)

## Best Practices

1. **Run unit tests frequently** - They're fast and catch basic errors
2. **Run promptfoo before committing** - Catches regression in prompt behavior
3. **Add tests for bugs** - When fixing a bug, add a test to prevent recurrence
4. **Keep fixtures realistic** - Use actual business context in test data
5. **Review failing LLM tests carefully** - LLM outputs vary, adjust thresholds as needed

## Maintenance

### Updating Test Data

Update fixtures when:
- Business context changes
- New frameworks added
- Templates evolve

### Updating Assertions

Review and update assertions when:
- Prompt behavior intentionally changes
- False positives detected
- New edge cases discovered

### Cleaning Results

```bash
# Remove old test results
rm -rf tests/results/*
```

## Resources

- [pytest documentation](https://docs.pytest.org/)
- [promptfoo documentation](https://www.promptfoo.dev/docs/intro)
- [LLM testing best practices](https://www.promptfoo.dev/docs/guides/llm-testing)

## Support

For issues or questions:
1. Check existing test output in `tests/results/`
2. Run with `--verbose` for detailed output
3. Review test fixtures for accuracy
4. Ensure dependencies are up to date
