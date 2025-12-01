# Testing Quick Start Guide

## Installation (One-Time Setup)

```bash
# Install Python dependencies
pip install -r tests/requirements.txt

# Install Node.js dependencies
npm install -g promptfoo

# Verify installation
pytest --version
npx promptfoo --version
```

## Running Tests

### All Tests (Recommended)

```bash
# Linux/Mac
./scripts/run_tests.sh

# Windows
scripts\run_tests.bat
```

### Quick Tests (No API Calls)

```bash
# Just Python unit tests (5-10 seconds)
./scripts/run_tests.sh --unit-only
```

### Full Evaluation (With API Calls)

```bash
# All tests including LLM evaluations (5-10 minutes)
./scripts/run_tests.sh --extended
```

## Common Commands

### Run Specific Test File

```bash
cd tests
pytest test_context_loader.py -v
pytest test_prompts.py -v
```

### Run Single Test

```bash
cd tests
pytest test_context_loader.py::TestLoadFile::test_load_existing_file -v
```

### Run Tests by Marker

```bash
cd tests
pytest -m unit -v           # Only unit tests
pytest -m integration -v    # Only integration tests
```

### Run with Coverage

```bash
cd tests
pytest --cov=. --cov-report=html
open htmlcov/index.html
```

### Run Promptfoo Tests

```bash
# Base test suite
npx promptfoo eval -c tests/promptfoo.yaml

# View results in browser
npx promptfoo view
```

## Understanding Output

### Pytest Output

```
test_context_loader.py::TestLoadFile::test_load_existing_file PASSED [20%]
test_context_loader.py::TestLoadFile::test_load_nonexistent_file PASSED [40%]
```

- `PASSED` ✓ - Test succeeded
- `FAILED` ✗ - Test failed (details below)
- `SKIPPED` - - Test skipped
- `[20%]` - Progress indicator

### Promptfoo Output

```
✓ Should handle emergency correctly - gas smell
✗ Should spell out numbers correctly
  Expected: spelled out numbers
  Actual: used "$100"
```

## Debugging Failed Tests

### Python Test Failed

```bash
# Run with verbose output and stop on first failure
cd tests
pytest test_context_loader.py -vsx

# Show full error details
pytest test_context_loader.py --tb=long

# Drop into debugger on failure
pytest test_context_loader.py --pdb
```

### Promptfoo Test Failed

```bash
# View detailed results
npx promptfoo view

# Run single test
npx promptfoo eval -c tests/promptfoo.yaml --filter "emergency"

# Show full output
npx promptfoo eval -c tests/promptfoo.yaml --verbose
```

## Typical Workflow

### Before Committing Changes

```bash
# Quick smoke test (unit tests only)
./scripts/run_tests.sh --unit-only

# If those pass, run prompt tests
./scripts/run_tests.sh
```

### After Major Changes

```bash
# Run everything including regression tests
./scripts/run_tests.sh --extended
```

### When Debugging

```bash
# Run failing test in isolation
cd tests
pytest test_context_loader.py::TestAssembleContext::test_minimal_assembly -vsx
```

## Tips

1. **Start with unit tests** - They're fast and catch most issues
2. **Use --verbose** - Shows which test is running
3. **Check fixtures** - Sample data might be outdated
4. **Review promptfoo in browser** - `npx promptfoo view` is easier than reading JSON
5. **Don't over-test LLM outputs** - They vary naturally, use rubrics not exact matches

## Troubleshooting

### "ModuleNotFoundError: No module named 'context_loader'"

```bash
# Make sure you're in the tests directory
cd tests
pytest test_context_loader.py
```

### "pytest: command not found"

```bash
pip install pytest
```

### "npx: command not found"

```bash
# Install Node.js first
# Then: npm install -g promptfoo
```

### "API rate limit exceeded"

```bash
# Reduce concurrency
npx promptfoo eval -c tests/promptfoo.yaml --max-concurrency 2
```

### Tests pass locally but fail in CI

```bash
# Check Python version
python --version

# Check dependencies
pip list | grep pytest

# Run in same environment as CI
./scripts/run_tests.sh --verbose
```

## Next Steps

- Read full [Testing README](README.md) for detailed documentation
- Review [test_context_loader.py](test_context_loader.py) for unit test examples
- Check [promptfoo.yaml](promptfoo.yaml) for LLM test examples
- Explore [fixtures/](fixtures/) for test data examples
