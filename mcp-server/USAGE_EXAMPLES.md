# MCP Server Usage Examples

Quick reference for using the Prompt Engineering MCP Server with Claude Desktop.

## Basic Usage Patterns

### 1. Context Assembly

#### Planning Mode
```
Assemble context for planning mode with task "Should I expand into HVAC market?"
```

Returns: Complete prompt with core values, decision frameworks, business context, and planning frameworks.

#### Technical Mode
```
Assemble context for technical mode with task "Build a webhook handler for lead capture in n8n"
```

Returns: Infrastructure inventory, coding standards, technical frameworks, n8n patterns.

#### Analysis Mode
```
Assemble context for analysis mode with task "Why did the last marketing campaign underperform?"
```

Returns: Expertise areas, learnings, analysis frameworks (steelman, assumptions).

#### Communication Mode
```
Assemble context for communication mode with task "Write a proposal for HVAC automation services"
```

Returns: Communication style, service offerings, target markets.

#### Minimal Mode
```
Assemble context for minimal mode with task "What's the best way to hash passwords in Node.js?"
```

Returns: Just the task, no additional context (useful for simple questions).

#### Full Mode (Default)
```
Assemble context with task "Design my Q1 strategy"
```

Returns: Comprehensive context from all major areas.

### 2. Browsing Resources

#### List All Frameworks
```
List all available thinking frameworks
```

Returns frameworks organized by category:
- planning/ (first-principles, pre-mortem, constraint-mapping)
- analysis/ (steelman-critique, assumption-surfacing, root-cause)
- decision/ (reversibility-assessment, regret-minimization)
- technical/ (architecture-design, debugging)
- communication/ (audience-adaptation)

#### List All Templates
```
Show me all available templates
```

Returns templates organized by category:
- voice-ai/ (receptionist-base, emergency-handling)
- development/ (claude-code-handoff, n8n-workflow-spec)
- outreach/ (cold-email-personalization)
- client/ (proposal-generation)

### 3. Getting Specific Resources

#### Get a Framework
```
Get the first-principles framework
```

Or with full path:
```
Get the planning/first-principles framework
```

Returns the complete markdown content of the framework.

#### Get a Template
```
Get the claude-code-handoff template
```

Or:
```
Get the development/claude-code-handoff template
```

Returns the complete template ready to customize.

### 4. Advanced Context Assembly

#### With Specific Framework
```
Assemble context for mode minimal with task "Should I build or buy a CRM?" and framework "first-principles"
```

Returns: Task + specified framework only (overrides mode defaults).

#### With Project Context
```
Assemble context for technical mode with task "Add lead routing to CoreReceptionAI" and project "corereceptionai"
```

Returns: Technical context + project-specific information from context/projects/active/corereceptionai.md.

### 5. Knowledge Search

#### Basic Search
```
Search knowledge for "n8n workflow patterns"
```

Returns relevant context files and snippets.

#### Limited Search
```
Search knowledge for "decision making" with limit 10
```

Returns up to 10 most relevant results.

### 6. Capturing Outputs

#### Save a Learning
```
Capture this workflow design with category "learning" and tags ["n8n", "lead-capture", "automation"]
```

Saves to: `context/learnings/captures/capture-[timestamp].md`

#### Save an Example
```
Capture this code snippet with category "example" and tags ["typescript", "mcp", "error-handling"]
```

#### Save a Framework
```
Capture this thinking process with category "framework" and tags ["decision-making", "product"]
```

## Common Workflows

### Workflow 1: Strategic Planning

1. List frameworks to see what's available:
   ```
   List all frameworks
   ```

2. Get a specific planning framework:
   ```
   Get the pre-mortem framework
   ```

3. Assemble full planning context:
   ```
   Assemble context for planning mode with task "Plan Q1 2024 strategy"
   ```

### Workflow 2: Technical Implementation

1. Search for relevant patterns:
   ```
   Search knowledge for "webhook handling" with limit 5
   ```

2. Get the technical template:
   ```
   Get the n8n-workflow-spec template
   ```

3. Assemble technical context:
   ```
   Assemble context for technical mode with task "Build lead scoring in n8n"
   ```

4. After implementation, capture the learning:
   ```
   Capture [the successful workflow] with category "example" and tags ["n8n", "lead-scoring"]
   ```

### Workflow 3: Client Communication

1. List available templates:
   ```
   List all templates
   ```

2. Get the proposal template:
   ```
   Get the proposal-generation template
   ```

3. Assemble communication context:
   ```
   Assemble context for communication mode with task "Write proposal for HVAC client"
   ```

### Workflow 4: Deep Analysis

1. Get analysis frameworks:
   ```
   Get the steelman-critique framework
   ```

2. Assemble with multiple perspectives:
   ```
   Assemble context for analysis mode with task "Analyze why our conversion rate dropped" and framework "root-cause-analysis"
   ```

3. Save insights:
   ```
   Capture [the analysis] with category "learning" and tags ["marketing", "conversion", "analysis"]
   ```

## Pro Tips

### Combining Tools for Complex Tasks

**Example: New Product Decision**
```
# Step 1: Get decision framework
Get the reversibility-assessment framework

# Step 2: Search for related context
Search knowledge for "product decisions" with limit 5

# Step 3: Assemble comprehensive context
Assemble context for planning mode with task "Should we build an HVAC-specific product?" and framework "first-principles"

# Step 4: After decision, capture reasoning
Capture [decision rationale] with category "learning" and tags ["product", "decision", "hvac"]
```

### Quick Reference Queries

Instead of memorizing names, just ask:
- "What frameworks do you have for decision making?"
- "Show me templates for client work"
- "Search for anything about n8n workflows"

### Mode Selection Guide

- **planning** - Strategy, roadmaps, priorities
- **technical** - Code, infrastructure, implementation
- **analysis** - Deep thinking, problem diagnosis
- **communication** - Writing, proposals, emails
- **minimal** - Quick questions, no context needed
- **full** - Comprehensive, when mode is unclear

### Framework Selection

Use `--framework` when:
- You know exactly which thinking approach you want
- You want just the framework + task (minimal context)
- The default frameworks for a mode aren't sufficient

### Project Context

Use `--project` when:
- Working on a specific active project
- Need project-specific constraints/context
- Want to include project background automatically

## Integration Patterns

### With Claude Code

```
# Get the handoff template
Get the claude-code-handoff template

# Then customize with context
Assemble context for technical mode with task "Build OAuth integration" and project "corereceptionai"
```

### With n8n

```
# Get the workflow spec template
Get the n8n-workflow-spec template

# Assemble technical context
Assemble context for technical mode with task "Design lead capture workflow"

# After building, capture the pattern
Capture [the workflow] with category "example" and tags ["n8n", "lead-capture", "webhook"]
```

### For Learning

After any successful interaction:
```
Capture [what worked] with category "learning" and tags [relevant, tags]
```

This builds your knowledge base over time.

## Error Handling

If you get "not found" errors:
1. Use `list_frameworks` or `list_templates` to see exact names
2. Try without the category prefix (e.g., "first-principles" instead of "planning/first-principles")
3. Check that files exist in the expected directories

If context assembly fails:
1. Verify Python is installed (`python --version`)
2. Check that context-loader.py exists
3. Verify context files exist in the expected locations

## Next Steps

- Explore all frameworks: `List all frameworks`
- Browse templates: `List all templates`
- Try different modes for the same task to see how context changes
- Build your knowledge base by capturing successful outputs
