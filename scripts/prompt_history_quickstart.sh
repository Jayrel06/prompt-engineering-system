#!/bin/bash
# Prompt History Quick Start Script
# Demonstrates common usage patterns

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
HISTORY_SCRIPT="$SCRIPT_DIR/prompt_history.py"

echo "=================================="
echo "Prompt History System Quick Start"
echo "=================================="
echo ""

# Function to run command with description
run_command() {
    local description="$1"
    shift
    echo ">>> $description"
    echo "Command: python prompt_history.py $*"
    python "$HISTORY_SCRIPT" "$@"
    echo ""
}

# Example 1: Save a prompt
echo "1. SAVING ENTRIES"
echo "-----------------"
run_command "Save a simple prompt" \
    --save "What is artificial intelligence?" \
    --output "AI is the simulation of human intelligence by machines" \
    --model "gpt-4" \
    --tags "AI,basics"

run_command "Save a chain-of-thought prompt" \
    --save "Solve: If x + 5 = 12, what is x?" \
    --output "Step 1: Subtract 5 from both sides: x = 12 - 5. Step 2: x = 7" \
    --framework "chain-of-thought" \
    --model "gpt-4" \
    --tokens 50 \
    --cost 0.0015 \
    --tags "math,step-by-step"

# Example 2: Search
echo "2. SEARCHING"
echo "------------"
run_command "Search for 'intelligence'" \
    --search "intelligence"

# Example 3: List recent
echo "3. LISTING RECENT ENTRIES"
echo "------------------------"
run_command "Show 3 most recent entries" \
    --list-recent 3

# Example 4: Filter by tag
echo "4. FILTERING BY TAG"
echo "------------------"
run_command "Show entries tagged 'AI'" \
    --tag "AI"

# Example 5: Statistics
echo "5. STATISTICS"
echo "-------------"
run_command "Show statistics" \
    --stats

# Example 6: Export
echo "6. EXPORTING"
echo "-----------"
export_dir="$SCRIPT_DIR/../data/exports"
mkdir -p "$export_dir"

run_command "Export to JSON" \
    --export "$export_dir/quickstart_export.json"

run_command "Export to CSV" \
    --export "$export_dir/quickstart_export.csv"

echo "=================================="
echo "Quick Start Complete!"
echo "=================================="
echo ""
echo "Next steps:"
echo "  • Try: python prompt_history.py --help"
echo "  • Read: PROMPT_HISTORY_README.md"
echo "  • Examples: python prompt_history_examples.py"
echo "  • Tests: python test_prompt_history.py"
echo ""
echo "Database location:"
echo "  $SCRIPT_DIR/../data/prompt_history.db"
echo ""
