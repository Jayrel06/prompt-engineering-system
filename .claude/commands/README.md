# Claude Code Slash Commands

This directory contains custom slash commands for Claude Code that integrate with your prompt engineering system.

## Available Commands

### `/plan [description]`
**Purpose:** Strategic planning using first-principles and pre-mortem frameworks

**Usage:**
```
/plan build a new feature for customer notifications
```

**What it does:**
- Loads your core values and business context
- Applies first-principles thinking framework
- Runs pre-mortem analysis to identify potential failure points
- Provides structured planning guidance

### `/framework [framework-name]`
**Purpose:** Apply a specific framework from your collection

**Usage:**
```
/framework decision-matrix.md
/framework socratic-questioning.md
```

**What it does:**
- Reads the specified framework file from `frameworks/`
- Applies its structured thinking process to your current problem
- Guides you through the framework's methodology

### `/handoff [task-description]`
**Purpose:** Generate a comprehensive handoff specification for Claude Code

**Usage:**
```
/handoff implement user authentication system
```

**What it does:**
- Uses the Claude Code handoff template
- Creates a detailed specification with mission, success criteria, and implementation instructions
- Ensures clear communication of requirements and constraints
- Defines what's in and out of scope

### `/reflect`
**Purpose:** Conduct a structured weekly reflection

**Usage:**
```
/reflect
```

**What it does:**
- Uses the weekly reflection framework
- Guides you through analyzing recent work
- Helps identify learnings and areas for improvement
- Encourages meta-cognitive thinking

### `/context [task-description]`
**Purpose:** Load your full business and technical context

**Usage:**
```
/context help me design the database schema
```

**What it does:**
- Reads all context files (identity, business, technical, learnings)
- Provides Claude with comprehensive background about your work
- Ensures responses are aligned with your values and business needs
- Gives Claude awareness of your technical setup and preferences

## How Slash Commands Work

1. **Create a command:** Add a `.md` file to `.claude/commands/`
2. **Use `$ARGUMENTS`:** This placeholder gets replaced with what you type after the command
3. **Invoke it:** Type `/command-name your arguments here` in Claude Code
4. **Claude executes:** The markdown content becomes Claude's prompt

## Tips

- Commands can read files, load context, and instruct Claude on how to respond
- Use commands to create consistent workflows and apply your frameworks
- Combine commands: use `/context` first, then `/plan` or `/framework`
- Edit these commands to match your evolving workflow

## File Locations

All commands reference the prompt engineering system at:
```
C:/Users/JRiel/prompt-engineering-system/
```

Structure:
- `context/` - Your identity, business, and technical context
- `frameworks/` - Thinking frameworks and methodologies
- `templates/` - Reusable templates for common tasks

## Examples

**Planning a new feature:**
```
/context the new notifications system
/plan notifications feature with real-time updates
```

**Applying decision-making:**
```
/framework decision-matrix.md
```

**Creating a handoff for implementation:**
```
/handoff build REST API for customer management
```

## Customization

Feel free to:
- Edit existing commands to better fit your workflow
- Add new commands for frequently-used frameworks
- Modify file paths as your system evolves
- Combine multiple frameworks in a single command
