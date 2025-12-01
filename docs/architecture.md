# System Architecture

## Overview

The Prompt Engineering System is designed to enhance AI interactions by dynamically assembling context based on task type.

```
┌─────────────────────────────────────────────────────────────┐
│                      User Request                            │
│              "Plan Q1 strategy for business"                 │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                    Context Loader                            │
│  1. Classify task type (planning/technical/etc)              │
│  2. Load relevant context files                              │
│  3. Select appropriate framework                             │
│  4. Assemble into single prompt                              │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                  Assembled Prompt                            │
│  - Task description                                          │
│  - Relevant context (identity, business, technical)          │
│  - Thinking framework                                        │
│  - Output format guidance                                    │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                    LLM Gateway (LiteLLM)                     │
│  - Route to appropriate model based on task                  │
│  - Handle fallbacks                                          │
│  - Track costs                                               │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                    AI Response                               │
└─────────────────────────────────────────────────────────────┘
```

## Components

### Context Repository (`/context`)

Stores structured knowledge in markdown files:

- **Identity:** Core values, expertise, communication style
- **Business:** Company overview, services, target markets
- **Technical:** Infrastructure, tools, patterns
- **Projects:** Active and archived project contexts
- **Learnings:** What works, what doesn't, insights

### Thinking Frameworks (`/frameworks`)

Reusable thinking patterns organized by type:

- **Planning:** First principles, pre-mortem, constraints
- **Analysis:** Steelman, assumptions, root cause
- **Decision:** Reversibility, regret minimization, matrix
- **Technical:** Architecture design, debugging
- **Communication:** Audience adaptation

### Context Loader (`/scripts/context-loader.py`)

The assembly engine:

1. Receives task description
2. Determines task type (planning, technical, etc.)
3. Looks up context rules for that type
4. Loads relevant files
5. Assembles into single prompt

### LiteLLM Gateway (`/infrastructure/litellm`)

Unified API for multiple LLMs:

- **Claude Opus:** Complex analysis, strategic thinking
- **Claude Sonnet:** Day-to-day tasks, coding
- **Claude Haiku:** Simple tasks, classification
- **GPT-4o:** Fallback for Claude models

## Data Flow

### Full Planning Request

```
User: "prompt plan 'Q1 strategy'"
                │
                ▼
Context Loader detects mode=full
                │
                ▼
Loads context files:
  - identity/core-values.md
  - identity/expertise-areas.md
  - business/corereceptionai-overview.md
  - technical/infrastructure-inventory.md
  - learnings/what-works.md
                │
                ▼
Assembles prompt with:
  - Task section
  - Context sections
  - (Optional) Framework section
                │
                ▼
Output: Complete prompt ready for Claude
```

### Framework-Specific Request

```
User: "prompt framework first-principles 'Build vs buy?'"
                │
                ▼
Context Loader loads:
  - frameworks/planning/first-principles.md
                │
                ▼
Assembles prompt with:
  - Task section
  - Framework section only
                │
                ▼
Output: Task + First Principles framework
```

## Context Rules

Defined in `context-loader.py`:

```python
CONTEXT_RULES = {
    "planning": {
        "context_files": [
            "identity/core-values.md",
            "identity/decision-frameworks.md",
            "business/corereceptionai-overview.md",
            "learnings/what-works.md"
        ],
        "frameworks": ["planning/first-principles.md"],
        "include_projects": True
    },
    "technical": {
        "context_files": [
            "technical/infrastructure-inventory.md",
            "technical/coding-standards.md",
            ...
        ],
        "frameworks": ["technical/architecture-design.md"],
        "include_projects": True
    },
    ...
}
```

## Infrastructure Services

### LiteLLM (Port 4000)

- Provides unified OpenAI-compatible API
- Routes to appropriate model
- Handles fallbacks when primary model fails
- Tracks costs (if database configured)

### Qdrant (Port 6333)

- Vector database for semantic search
- Stores embeddings of past outputs
- Enables "similar past work" retrieval
- Optional enhancement

## Integration with Existing Stack

Designed to work alongside existing n8n infrastructure:

```
Existing Stack                 Prompt System
┌─────────────┐               ┌─────────────┐
│ PostgreSQL  │◄──────────────│ pgvector    │
│ (n8n DB)    │               │ embeddings  │
└─────────────┘               └─────────────┘

┌─────────────┐               ┌─────────────┐
│ Langfuse    │◄──────────────│ LiteLLM     │
│ (existing)  │  observability│ (new)       │
└─────────────┘               └─────────────┘

┌─────────────┐               ┌─────────────┐
│ n8n         │◄──────────────│ Webhooks    │
│ (workflows) │  triggers     │ (context)   │
└─────────────┘               └─────────────┘
```

## Future Enhancements

1. **Vector Search:** Semantic retrieval of similar past work
2. **n8n Integration:** Webhook triggers for context assembly
3. **Learning Loop:** Automatic capture of successful outputs
4. **Custom MCP:** MCP server for context access
