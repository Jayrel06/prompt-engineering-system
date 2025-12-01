#!/bin/bash
# Comprehensive Test Runner for Prompt Engineering System
# Runs all tests: unit tests, prompt quality tests, and integration tests

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Get script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
TESTS_DIR="$PROJECT_ROOT/tests"

# Create results directory
mkdir -p "$TESTS_DIR/results"

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}Prompt Engineering System - Test Suite${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""

# Parse command line arguments
RUN_UNIT=true
RUN_PROMPT=true
RUN_EXTENDED=false
VERBOSE=false

while [[ $# -gt 0 ]]; do
    case $1 in
        --unit-only)
            RUN_PROMPT=false
            shift
            ;;
        --prompt-only)
            RUN_UNIT=false
            shift
            ;;
        --extended)
            RUN_EXTENDED=true
            shift
            ;;
        --verbose|-v)
            VERBOSE=true
            shift
            ;;
        --help|-h)
            echo "Usage: $0 [OPTIONS]"
            echo ""
            echo "Options:"
            echo "  --unit-only     Run only unit tests (Python)"
            echo "  --prompt-only   Run only prompt quality tests (promptfoo)"
            echo "  --extended      Include extended test suite"
            echo "  --verbose, -v   Verbose output"
            echo "  --help, -h      Show this help message"
            echo ""
            echo "Examples:"
            echo "  $0                    # Run all standard tests"
            echo "  $0 --unit-only        # Only Python unit tests"
            echo "  $0 --extended         # Run all tests including extended suite"
            echo "  $0 --verbose          # Run with detailed output"
            exit 0
            ;;
        *)
            echo -e "${RED}Unknown option: $1${NC}"
            echo "Use --help for usage information"
            exit 1
            ;;
    esac
done

# Track overall success
ALL_PASSED=true

# ==========================================
# 1. Python Unit Tests
# ==========================================

if [ "$RUN_UNIT" = true ]; then
    echo -e "${YELLOW}[1/3] Running Python Unit Tests...${NC}"
    echo ""

    # Check if pytest is installed
    if ! command -v pytest &> /dev/null; then
        echo -e "${RED}Error: pytest not found. Install with: pip install pytest${NC}"
        ALL_PASSED=false
    else
        cd "$TESTS_DIR"

        if [ "$VERBOSE" = true ]; then
            PYTEST_ARGS="-v -s"
        else
            PYTEST_ARGS="-v"
        fi

        # Run context loader tests
        echo -e "${BLUE}Testing context-loader.py...${NC}"
        if pytest test_context_loader.py $PYTEST_ARGS --tb=short; then
            echo -e "${GREEN}✓ Context loader tests passed${NC}"
        else
            echo -e "${RED}✗ Context loader tests failed${NC}"
            ALL_PASSED=false
        fi

        echo ""

        # Run prompt quality tests
        echo -e "${BLUE}Testing prompt structure and quality...${NC}"
        if pytest test_prompts.py $PYTEST_ARGS --tb=short; then
            echo -e "${GREEN}✓ Prompt quality tests passed${NC}"
        else
            echo -e "${RED}✗ Prompt quality tests failed${NC}"
            ALL_PASSED=false
        fi

        echo ""
    fi
fi

# ==========================================
# 2. Promptfoo Quality Tests
# ==========================================

if [ "$RUN_PROMPT" = true ]; then
    echo -e "${YELLOW}[2/3] Running Promptfoo Quality Tests...${NC}"
    echo ""

    cd "$PROJECT_ROOT"

    # Check if promptfoo is available
    if ! command -v npx &> /dev/null; then
        echo -e "${RED}Error: npx not found. Install Node.js first.${NC}"
        ALL_PASSED=false
    else
        # Check if promptfoo is installed
        if ! npx promptfoo --version &> /dev/null; then
            echo -e "${YELLOW}Installing promptfoo...${NC}"
            npm install -g promptfoo
        fi

        echo -e "${BLUE}Running prompt evaluations...${NC}"

        if [ "$VERBOSE" = true ]; then
            PROMPTFOO_ARGS=""
        else
            PROMPTFOO_ARGS="--no-progress-bar"
        fi

        # Run base promptfoo tests
        if npx promptfoo eval -c tests/promptfoo.yaml $PROMPTFOO_ARGS; then
            echo -e "${GREEN}✓ Base prompt tests passed${NC}"
        else
            echo -e "${RED}✗ Base prompt tests failed${NC}"
            ALL_PASSED=false
        fi

        echo ""
    fi
fi

# ==========================================
# 3. Extended Test Suite (Optional)
# ==========================================

if [ "$RUN_EXTENDED" = true ]; then
    echo -e "${YELLOW}[3/3] Running Extended Test Suite...${NC}"
    echo ""

    cd "$PROJECT_ROOT"

    if command -v npx &> /dev/null; then
        echo -e "${BLUE}Running extended evaluations...${NC}"

        if npx promptfoo eval -c tests/promptfoo-extended.yaml; then
            echo -e "${GREEN}✓ Extended tests passed${NC}"
        else
            echo -e "${RED}✗ Extended tests failed${NC}"
            ALL_PASSED=false
        fi
    else
        echo -e "${YELLOW}Skipping extended tests (npx not available)${NC}"
    fi

    echo ""
fi

# ==========================================
# Summary
# ==========================================

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}Test Summary${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""

if [ "$ALL_PASSED" = true ]; then
    echo -e "${GREEN}✓ All tests passed!${NC}"
    echo ""
    echo "Test results saved to: $TESTS_DIR/results/"
    exit 0
else
    echo -e "${RED}✗ Some tests failed${NC}"
    echo ""
    echo "Check detailed results in: $TESTS_DIR/results/"
    exit 1
fi
