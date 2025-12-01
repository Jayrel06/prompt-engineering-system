# Tools Integration Matrix

## LLM Gateways

| Tool | Self-Hosted | Complexity | Key Features | Recommendation |
|------|-------------|------------|--------------|----------------|
| **LiteLLM** | Yes | Medium | 100+ models, unified API, cost tracking, fallbacks | **Primary Choice** |
| **OpenRouter** | No (Cloud) | Low | 400+ models, simple API, pay-per-use | Fallback/Alternative |

### LiteLLM (Recommended)
- **Why:** Self-hosted, full control, excellent fallback chains, cost tracking
- **Setup:** Docker container, YAML config
- **Integration:** Drop-in OpenAI API replacement
- **Cost:** Free (self-hosted) + API costs

### OpenRouter
- **Why:** Zero infrastructure, massive model variety
- **Setup:** API key only
- **Integration:** OpenAI-compatible API
- **Cost:** Pay-per-use, slight markup

---

## Vector Databases

| Tool | Self-Hosted | Complexity | Key Features | Recommendation |
|------|-------------|------------|--------------|----------------|
| **pgvector** | Yes | Low | PostgreSQL extension, SQL filtering | **Primary (already have PG)** |
| **Qdrant** | Yes | Medium | High performance, rich filtering | Secondary/Scale |
| **Chroma** | Yes | Low | Python-native, easy prototyping | Development only |

### pgvector (Recommended for This Project)
- **Why:** Already have PostgreSQL running, no new infrastructure
- **Setup:** `CREATE EXTENSION vector;`
- **Performance:** Good for < 1M vectors
- **Best For:** Integrated SQL + vector queries

### Qdrant
- **Why:** Best performance at scale, advanced filtering
- **Setup:** Docker container
- **When to Use:** If pgvector becomes bottleneck
- **Best For:** Large-scale semantic search

### Chroma
- **Why:** Fastest to prototype
- **Setup:** `pip install chromadb`
- **Limitation:** Not production-ready at scale
- **Best For:** Local development, experiments

---

## Observability Tools

| Tool | Self-Hosted | Complexity | Key Features | Recommendation |
|------|-------------|------------|--------------|----------------|
| **Langfuse** | Yes | Medium | Full LLM observability, prompt management | **Primary Choice** |
| **Helicone** | Yes | Low | Lightweight, minimal integration | Alternative |
| **Prometheus+Grafana** | Yes | High | Infrastructure metrics | Complementary |

### Langfuse (Recommended)
- **Why:** Complete LLM observability, self-hosted, already in docker-compose
- **Features:**
  - Request/response logging
  - Cost tracking
  - Latency monitoring
  - Prompt versioning
  - Evaluation framework
- **Integration:** SDK for Python/JS, OpenAI-compatible proxy

### Helicone
- **Why:** Minimal setup, one-line integration
- **Setup:** Change base URL + add header
- **Best For:** Quick wins, less comprehensive needs

### Prometheus + Grafana (Complementary)
- **Why:** Already running, good for infrastructure metrics
- **Use For:** Container health, system resources
- **Not For:** LLM-specific observability

---

## MCP Servers

| Server | Purpose | Priority | Notes |
|--------|---------|----------|-------|
| **filesystem** | Context repo access | High | Access markdown files |
| **postgres** | Structured data | High | Already configured |
| **memory** | Persistent context | Medium | Knowledge graph storage |
| **brave-search** | Real-time research | Medium | Web search capability |

### Configuration (Already in mcp.json)
```json
{
  "mcpServers": {
    "postgres-n8n": {
      "command": "mcp-server-postgres.cmd",
      "args": ["postgresql://..."]
    }
  }
}
```

### Recommended Additions
1. **filesystem MCP** - For accessing prompt-engineering-system repo
2. **memory MCP** - For persistent conversation context
3. **Custom MCP** - For context assembly (future)

---

## Implementation Priority

### Tier 1: Critical (Week 1)
1. **LiteLLM** - Model gateway foundation
   - Unified API for all models
   - Fallback chains
   - Cost tracking

2. **pgvector** - Vector storage
   - Leverage existing PostgreSQL
   - Enable semantic search
   - No new infrastructure

### Tier 2: Enhanced (Week 2)
3. **Langfuse** - Observability
   - Already in docker-compose
   - Enable after core working
   - Track all LLM interactions

4. **MCP Servers** - Context access
   - filesystem for repo access
   - memory for persistence

### Tier 3: Optional (Week 3+)
5. **Qdrant** - If pgvector insufficient
6. **Custom MCP** - For advanced context assembly
7. **Promptfoo** - For systematic testing

---

## Architecture Recommendation

```
┌─────────────────────────────────────────────────────────────┐
│                    Claude Desktop / Code                      │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                    LiteLLM Gateway                           │
│  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐        │
│  │ Claude  │  │ Claude  │  │  GPT-4  │  │ Fallback│        │
│  │  Opus   │  │ Sonnet  │  │   Mini  │  │  Chain  │        │
│  └─────────┘  └─────────┘  └─────────┘  └─────────┘        │
└─────────────────────────────────────────────────────────────┘
                              │
              ┌───────────────┼───────────────┐
              ▼               ▼               ▼
     ┌──────────────┐ ┌──────────────┐ ┌──────────────┐
     │   Langfuse   │ │  PostgreSQL  │ │     n8n      │
     │ Observability│ │  + pgvector  │ │  Workflows   │
     └──────────────┘ └──────────────┘ └──────────────┘
```

---

## Cost Analysis

### Self-Hosted Stack (Monthly)
- **Server:** $20-50 (existing infrastructure)
- **API Costs:** Variable based on usage
- **Total:** ~$20-50 + API costs

### Cloud Alternative (Monthly)
- **OpenRouter:** Pay-per-use only
- **LangSmith:** $39-399/month
- **Managed Vector DB:** $25-100/month
- **Total:** ~$100-500/month

**Recommendation:** Self-hosted for control and cost at current scale. Cloud services make sense for rapid scaling or team use.

---

## Integration Checklist

### Immediate Setup
- [ ] Create LiteLLM config.yaml
- [ ] Add pgvector to PostgreSQL
- [ ] Configure Langfuse credentials
- [ ] Test filesystem MCP access

### Testing
- [ ] Verify model routing works
- [ ] Test fallback chains
- [ ] Confirm vector search performance
- [ ] Validate observability logging

### Documentation
- [ ] Document API endpoints
- [ ] Create troubleshooting guide
- [ ] Set up alerting thresholds
