# Tool Preferences

## Workflow Automation

### Primary: n8n
- **Why:** Visual, self-hosted, powerful
- **When:** Any multi-step automation, integrations
- **Strengths:** Flexibility, debugging, community

### Alternative: Python Scripts
- **When:** Complex logic, ML tasks, data processing
- **Strengths:** Full programming power, libraries

### Avoid: Zapier/Make
- **Why:** Cost at scale, limited control, vendor lock-in
- **Exception:** Quick client demos

---

## Databases

### Primary: PostgreSQL
- **Why:** Robust, pgvector support, familiar
- **When:** Structured data, relational needs
- **Extensions:** pgvector for embeddings

### Cache: Redis
- **Why:** Fast, queue support, session storage
- **When:** Caching, job queues, real-time features

### Vector Search: pgvector (primary) / Qdrant (scale)
- **Why:** Leverage existing Postgres, or scale with Qdrant
- **When:** Semantic search, RAG, similarity matching

---

## AI/LLM

### Primary: Claude (Anthropic)
- **Why:** Best reasoning, coding, safety
- **Models:**
  - Opus: Complex analysis
  - Sonnet: Daily work
  - Haiku: Simple tasks

### Fallback: OpenAI GPT
- **When:** Claude unavailable, comparison testing
- **Models:** GPT-4o, GPT-4o-mini

### Gateway: LiteLLM
- **Why:** Unified API, fallbacks, cost tracking
- **When:** All LLM calls should route through

---

## Voice AI

### Primary: VAPI
- **Why:** Flexible, good quality, API-first
- **When:** Custom voice agents

### Alternative: Retell
- **Why:** Good for simpler use cases
- **When:** Quick deployments

---

## Infrastructure

### Containers: Docker + Docker Compose
- **Why:** Reproducible, portable, standard
- **When:** All services

### Reverse Proxy: Cloudflare Tunnel
- **Why:** Secure, no port forwarding, free tier
- **When:** Exposing services externally

### Monitoring: Prometheus + Grafana
- **Why:** Industry standard, flexible
- **When:** System metrics, alerting

### LLM Observability: Langfuse
- **Why:** Self-hosted, comprehensive
- **When:** All LLM interactions

---

## Development

### Editor: VS Code / Cursor
- **Why:** Extensions, AI integration, familiar
- **When:** All coding

### AI Assistant: Claude Code
- **Why:** Best for complex tasks, codebase understanding
- **When:** Development, debugging, architecture

### Version Control: Git + GitHub
- **Why:** Standard, CI/CD integration
- **When:** All code projects

---

## Languages & Frameworks

### Python
- **When:** AI/ML, data processing, scripts
- **Libraries:** LangChain, pandas, requests

### JavaScript/TypeScript
- **When:** Web frontends, n8n custom nodes
- **Frameworks:** React (if needed), Node.js

### Bash
- **When:** System automation, Docker scripts
- **Keep it simple:** Complex logic goes in Python

---

## Anti-Preferences (Avoid)

| Tool | Reason | Alternative |
|------|--------|-------------|
| Zapier | Cost, lock-in | n8n |
| Make | Same as Zapier | n8n |
| Airtable | Cost at scale | PostgreSQL + Metabase |
| Notion API | Limited, slow | Custom solutions |
| AWS Lambda | Complexity | Docker on VPS |
| Kubernetes | Overkill for scale | Docker Compose |
