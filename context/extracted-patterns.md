# Extracted Patterns

Patterns discovered from existing projects and workflows.

---

## From n8n Stack (docker-compose.yml)

### Service Architecture Pattern
- Core services (PostgreSQL, Redis, n8n) form foundation
- Support services (Grafana, Prometheus) for observability
- Tunnel service (Cloudflared) for secure external access
- All services use `restart: unless-stopped`

### Health Check Pattern
```yaml
healthcheck:
  test: ["CMD-SHELL", "pg_isready -U ${USER} -d ${DB}"]
  interval: 10s
  timeout: 5s
  retries: 10
```

### Environment Variable Pattern
- Credentials always via environment variables
- Use `.env` file for local values
- Reference with `${VAR_NAME}` syntax
- Document all required vars in `.env.example`

### Volume Pattern
- Named volumes for data persistence
- Mount files for configuration
- Separate volumes for data vs config

---

## From CoreReception Directory

### Spec-to-Build Pattern
```
/specs → /builds → /agent_runner
```
1. Write spec in markdown
2. Claude Code implements to /builds
3. Agent runner executes result

### Naming Convention
- Specs: `YYYY-MM-DD-project-name.md`
- Clear date prefix for chronology
- Descriptive name for content

---

## From texas-pt-leads Project

### Lead Gen Pipeline Pattern
```
Scrape → Enrich → Score → Store → Outreach
```
1. Web scraping for raw data
2. Enrichment APIs for additional info
3. Scoring based on criteria
4. Database storage
5. Outreach automation

### Data Validation Pattern
- Validate at ingestion
- Log validation failures
- Manual review for initial batches
- Automated only after validation

### Report Generation Pattern
- Markdown reports for status
- Include metrics and counts
- Clear success/failure indicators

---

## Technical Patterns

### Docker Networking
- Use Docker networks for inter-service communication
- Reference services by container name
- Expose only necessary ports externally

### Database Connection
- Connection string via environment variable
- Use PostgreSQL for primary data
- pgvector extension for embeddings
- Redis for caching and queues

### API Integration
- Retry with exponential backoff
- Log all requests and responses
- Handle rate limits gracefully
- Validate responses before use

---

## Workflow Patterns

### Webhook Handler
```
Webhook → Validate → Process → Respond
```
- Always validate incoming data
- Process can be sync or async
- Always return appropriate status code

### Scheduled Job
```
Cron → Check State → Process Changed → Update State
```
- Track last run timestamp
- Process only changes since last run
- Handle "nothing to do" gracefully

### Error Notification
```
Error → Format → Notify → Log
```
- Include error details
- Include context (workflow, timestamp)
- Multiple notification channels (Slack, email)

---

## Prompt Patterns

### Voice AI Identity
```
You are [NAME], the [adjective] [role] for [BUSINESS].
You speak at a [pace] pace.
You genuinely [care statement].
```

### Rule Formatting
```
## CRITICAL RULES
1. **Rule Name**
   Explanation of rule.

2. **Rule Name**
   Explanation of rule.
```

### Flow Definition
```
### [Flow Name] Flow
1. [Action]: "[Script]"
2. [Action]: "[Script]"
...
```

---

## Business Patterns

### Service Pricing
- Project-based for implementations
- Monthly for ongoing services
- Tiered based on complexity
- Clear scope boundaries

### Client Communication
- Lead with value/outcomes
- ROI calculation when possible
- Clear next steps
- Confirm understanding

### Sales Discovery
- Understand problem before solution
- Quantify impact of problem
- Identify decision maker
- Assess budget and timeline
