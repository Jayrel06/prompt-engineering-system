#!/bin/bash
# Model Orchestrator - Usage Examples
# Demonstrates various orchestration strategies and features

SCRIPT_DIR="C:/Users/JRiel/prompt-engineering-system/scripts"
cd "$SCRIPT_DIR"

echo "======================================"
echo "Model Orchestrator - Usage Examples"
echo "======================================"
echo ""

# Example 1: List available models
echo "1. LIST AVAILABLE MODELS"
echo "Command: python model_orchestrator.py --list-models"
echo ""
python model_orchestrator.py --list-models
echo ""
read -p "Press Enter to continue..."
echo ""

# Example 2: Simple query with cheapest strategy
echo "======================================"
echo "2. CHEAPEST STRATEGY (Auto-routing)"
echo "======================================"
echo "Command: python model_orchestrator.py --prompt 'What is 2+2?' --strategy cheapest"
echo ""
python model_orchestrator.py --prompt "What is 2+2?" --strategy cheapest
echo ""
read -p "Press Enter to continue..."
echo ""

# Example 3: Fallback chain for uncertain task
echo "======================================"
echo "3. FALLBACK CHAIN"
echo "======================================"
echo "Command: python model_orchestrator.py --prompt 'Explain quantum entanglement' --strategy fallback"
echo ""
python model_orchestrator.py --prompt "Explain quantum entanglement" --strategy fallback
echo ""
read -p "Press Enter to continue..."
echo ""

# Example 4: Ensemble for important decision
echo "======================================"
echo "4. ENSEMBLE STRATEGY"
echo "======================================"
echo "Command: python model_orchestrator.py --prompt 'Should I use microservices?' --strategy ensemble --ensemble-size 2"
echo ""
python model_orchestrator.py --prompt "Should I use microservices?" --strategy ensemble --ensemble-size 2
echo ""
read -p "Press Enter to continue..."
echo ""

# Example 5: Custom fallback chain
echo "======================================"
echo "5. CUSTOM FALLBACK CHAIN"
echo "======================================"
echo "Command: python model_orchestrator.py --prompt 'Design API' --strategy fallback --chain 'claude-haiku-3.5,claude-sonnet-3.5'"
echo ""
python model_orchestrator.py --prompt "Design a REST API for a blog" --strategy fallback --chain "claude-haiku-3.5,claude-sonnet-3.5"
echo ""
read -p "Press Enter to continue..."
echo ""

# Example 6: Cost budget enforcement
echo "======================================"
echo "6. COST BUDGET ENFORCEMENT"
echo "======================================"
echo "Command: python model_orchestrator.py --prompt 'Simple task' --strategy cheapest --max-cost 0.001"
echo ""
python model_orchestrator.py --prompt "What is the capital of France?" --strategy cheapest --max-cost 0.001
echo ""
read -p "Press Enter to continue..."
echo ""

# Example 7: JSON output
echo "======================================"
echo "7. JSON OUTPUT"
echo "======================================"
echo "Command: python model_orchestrator.py --prompt 'Test' --strategy cheapest --output result.json"
echo ""
python model_orchestrator.py --prompt "Test output" --strategy cheapest --output result.json
if [ -f result.json ]; then
    echo "Result saved to result.json:"
    cat result.json
    rm result.json
fi
echo ""
read -p "Press Enter to continue..."
echo ""

# Example 8: Verbose mode
echo "======================================"
echo "8. VERBOSE MODE"
echo "======================================"
echo "Command: python model_orchestrator.py --prompt 'Debug' --strategy fallback --verbose"
echo ""
python model_orchestrator.py --prompt "Explain debugging" --strategy fallback --verbose
echo ""
read -p "Press Enter to continue..."
echo ""

# Example 9: View orchestration costs
echo "======================================"
echo "9. VIEW COST TRACKING"
echo "======================================"
echo "Command: python cost_tracker.py stats --category orchestration"
echo ""
python cost_tracker.py stats --category orchestration
echo ""

echo "======================================"
echo "Examples completed!"
echo "======================================"
