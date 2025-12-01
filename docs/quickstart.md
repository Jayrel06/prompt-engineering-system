# Quickstart Guide

Get up and running with the Prompt Engineering System in 5 minutes.

## Prerequisites

- Python 3.8+
- (Optional) Docker for infrastructure services
- (Optional) API keys for Anthropic/OpenAI

## Step 1: Clone and Configure

```bash
# Clone the repo
git clone https://github.com/YOUR_USERNAME/prompt-engineering-system.git
cd prompt-engineering-system

# Create environment file
cp .env.example .env

# Edit .env with your API keys (optional for basic use)
```

## Step 2: Setup CLI

```bash
# Make script executable
chmod +x scripts/prompt.sh

# Add alias to your shell profile (.bashrc, .zshrc, etc.)
echo "alias prompt='$(pwd)/scripts/prompt.sh'" >> ~/.bashrc
source ~/.bashrc

# Or just use directly
./scripts/prompt.sh status
```

### Optional: Enable Shell Completion

Shell completion provides auto-complete for commands, frameworks, and options.

**For Bash:**
```bash
# Add to ~/.bashrc
echo "source $(pwd)/scripts/prompt-completion.bash" >> ~/.bashrc
source ~/.bashrc

# Or for system-wide completion
sudo cp scripts/prompt-completion.bash /etc/bash_completion.d/prompt
```

**For Zsh:**
```bash
# Add to ~/.zshrc
echo "source $(pwd)/scripts/prompt-completion.zsh" >> ~/.zshrc
source ~/.zshrc
```

**For Fish:**
```bash
# Copy to Fish completions directory
mkdir -p ~/.config/fish/completions
cp scripts/prompt-completion.fish ~/.config/fish/completions/
```

**Set Project Root (Optional):**
For better completion support, set the project root in your shell profile:
```bash
# Add to ~/.bashrc, ~/.zshrc, or ~/.config/fish/config.fish
export PROMPT_PROJECT_ROOT="/path/to/prompt-engineering-system"
```

## Step 3: Test It

```bash
# Check system status
prompt status

# List available frameworks
prompt list-frameworks

# Generate a context-enriched prompt
prompt plan "What should my Q1 priorities be?"
```

## Step 4: Customize (Important!)

The system comes with example content. Make it yours:

### Edit Your Identity
```bash
# Open and edit with your values, style, expertise
nano context/identity/core-values.md
nano context/identity/expertise-areas.md
```

### Edit Your Business
```bash
# Update with your actual business info
nano context/business/corereceptionai-overview.md
```

### Edit Your Infrastructure
```bash
# Document your actual setup
nano context/technical/infrastructure-inventory.md
```

## Step 5: Use It

### For Planning Tasks
```bash
prompt plan "Should I expand into the HVAC market?"
```
Outputs a prompt with your business context + planning frameworks.

### For Technical Tasks
```bash
prompt framework architecture-design "Design a lead scoring system"
```
Outputs task + Architecture Design framework.

### For Quick Questions
```bash
prompt quick "What's the best way to handle n8n errors?"
```
Outputs just the task, minimal context.

### For Claude Code Handoffs
```bash
prompt handoff "Build an n8n workflow for appointment reminders"
```
Outputs task + technical context + handoff template.

## Optional: Start Infrastructure

If you want LiteLLM and vector search:

```bash
cd infrastructure
docker-compose up -d

# Verify services are running
curl http://localhost:4000/health  # LiteLLM
curl http://localhost:6333/        # Qdrant
```

## Next Steps

1. **Customize context files** with your actual information
2. **Read the frameworks** to understand available thinking tools
3. **Create templates** for your recurring tasks
4. **Add to learnings** as you discover what works

## Common Commands

```bash
# Full context planning
prompt plan "description"

# Minimal context quick question
prompt quick "question"

# Specific framework
prompt framework first-principles "decision"

# Claude Code handoff
prompt handoff "implementation task"

# Copy output to clipboard
prompt copy plan "Q1 strategy"
prompt copy framework first-principles "Should I add X?"

# Preview without copying
prompt preview quick "Best practice"

# List resources
prompt list-frameworks
prompt list-templates

# System status
prompt status
```

## Troubleshooting

### "Python not found"
Install Python 3.8+ and ensure it's in your PATH.

### "Permission denied"
Run `chmod +x scripts/prompt.sh`

### "Module not found"
The context loader uses only standard library. No pip install needed.

### Infrastructure services not starting
Check Docker is running: `docker ps`
Check port conflicts: `netstat -an | grep 4000`
