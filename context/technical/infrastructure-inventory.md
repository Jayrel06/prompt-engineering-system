# Infrastructure Inventory

## Docker Stack (n8n_stack)

Located at: `C:/Users/JRiel/jason/desktop/n8n_compose/n8n_stack/`

### Core Services

| Service | Image | Port | Purpose | Status |
|---------|-------|------|---------|--------|
| n8n | n8nio/n8n:latest | 5678 | Workflow orchestration | Running |
| postgres | pgvector/pgvector:pg16 | 5432 | Primary database + vectors | Running |
| redis | redis:alpine | 6379 | Queue backend, caching | Running |
| cloudflared | cloudflare/cloudflared | - | Secure tunnels | Running |
| grafana | grafana/grafana:latest | 3000 | Dashboards | Running |
| prometheus | prom/prometheus:latest | 9090 | Metrics collection | Running |
| portainer | portainer/portainer-ce | 9000/9443 | Container management | Running |
| jupyter | jupyter/minimal-notebook | 8888 | Data analysis | Running |
| langfuse | langfuse/langfuse:2 | 3002 | LLM observability | Running |
| playwright | mcr.microsoft.com/playwright | - | Web scraping | Running |
| python-ai | custom | - | LangChain + Claude | Running |
| mailserver | docker-mailserver | 25/587/993 | Email | Running |
| context7-mcp | mcp/context7 | 3001 | Documentation lookup | Running |
| workflow-api | custom | 3003 | Workflow API service | Running |

### Volumes
- n8n_postgres (database)
- n8n_data (n8n files)
- redis_data (cache)
- grafana_data (dashboards)
- prometheus_data (metrics)
- portainer_data (container config)
- jupyter_data (notebooks)
- context7_data, context7_cache

---

## MCP Servers

### Currently Configured (mcp.json)
```json
{
  "mcpServers": {
    "postgres-n8n": {
      "command": "mcp-server-postgres.cmd",
      "args": ["postgresql://n8n:***@localhost:5432/n8n"]
    }
  }
}
```

### Available in Stack
- Context7 (documentation lookup) - port 3001
- PostgreSQL MCP (database access)
- n8n-mcp (workflow management)
- Kapture (browser automation)

### Recommended Additions
- filesystem MCP (for prompt-engineering-system access)
- memory MCP (for persistent context)
- brave-search MCP (for web research)

---

## External Services

| Service | Purpose | Notes |
|---------|---------|-------|
| Cloudflare | DNS, tunnels | Secure access to n8n |
| GitHub | Version control | repos and CI/CD |
| VAPI | Voice AI platform | AI receptionist hosting |
| Retell | Voice AI platform | Alternative to VAPI |
| Anthropic API | Claude models | Primary LLM |
| OpenAI API | GPT models | Fallback/comparison |

---

## Development Environment

### Local Machine
- Windows 11 with WSL2
- Docker Desktop
- Git Bash
- VS Code / Cursor
- Claude Desktop
- Claude Code CLI

### Key Paths
- n8n stack: `C:/Users/JRiel/jason/desktop/n8n_compose/n8n_stack/`
- CoreReception: `C:/Users/JRiel/.corereception/`
- Projects: `C:/Users/JRiel/Projects/`
- Downloads (temp): `C:/Users/JRiel/Downloads/`

---

## Database Schema (PostgreSQL)

### n8n Tables
- workflow_entity
- execution_entity
- webhook_entity
- credentials_entity

### Custom Tables
- leads (texas-pt-leads)
- langfuse schema

### pgvector
- Extension enabled
- Ready for embeddings

---

## Network Configuration

### Docker Network
- prompt-system-network (new for this project)
- Default bridge network (existing services)

### Port Mapping
- 3000: Grafana
- 3001: Context7 MCP
- 3002: Langfuse
- 3003: Workflow API
- 4000: LiteLLM (to be added)
- 5432: PostgreSQL
- 5678: n8n
- 6333: Qdrant (to be added)
- 6379: Redis
- 8888: Jupyter
- 9000: Portainer
- 9090: Prometheus

---

## Backup Strategy

### Currently
- PostgreSQL volumes persistent
- n8n workflows exportable
- Manual backup process

### Recommended
- Automated PostgreSQL dumps
- n8n workflow version control
- Grafana dashboard exports
