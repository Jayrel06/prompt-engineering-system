# n8n Workflow Patterns

## Trigger Patterns

### Webhook Trigger
```
Webhook → Validate Input → Process → Response
```
- Always validate incoming data
- Return appropriate HTTP status
- Log for debugging

### Schedule Trigger
```
Cron → Check Conditions → Process → Notify
```
- Idempotent operations
- Handle "nothing to do" gracefully
- Notification on completion/failure

### Manual Trigger
```
Manual → Test Mode Check → Process → Log
```
- Good for testing and ad-hoc runs
- Can include test data

---

## Error Handling Patterns

### Try-Catch Pattern
```
Trigger → Set Variables → [
  Try Branch → Main Process
  Catch Branch → Error Handler
] → Merge → Continue
```

### Retry with Backoff
- Enable retry on node settings
- Exponential backoff for API calls
- Max 3 retries typically

### Error Notification
```
Error Trigger → Format Error → Send Alert (Slack/Email)
```
- Include workflow name
- Include error details
- Include timestamp

---

## Data Transformation Patterns

### Array Processing
```
Get Items → Split In Batches → Process Each → Aggregate
```
- Batch size based on rate limits
- Aggregate results at end

### Data Enrichment
```
Get Base Data → Loop [
  Call API → Merge Data
] → Output Enriched
```
- Handle API failures gracefully
- Cache when possible

### Filtering
```
Get All → IF Node → Match Path / No Match Path
```
- Clear filter conditions
- Log filtered counts

---

## Integration Patterns

### CRM Update
```
Trigger → Get Existing Record → IF Exists [
  Yes → Update
  No → Create
] → Confirm Success
```
- Always check existence first
- Handle both paths

### Webhook to API
```
Webhook → Transform Data → Call API → Return Response
```
- Transform to API format
- Handle API errors
- Return meaningful response

### Multi-System Sync
```
Source → Transform → [
  System A
  System B
  System C
] → Aggregate Results → Log
```
- Parallel when possible
- Independent error handling

---

## Best Practices

### Variables and Expressions
- Use `$json.field` for current item
- Use `$('NodeName').item.json.field` for other nodes
- Store constants in Set node at start

### Credentials
- Always use credential manager
- Environment variables for URLs
- Never hardcode secrets

### Performance
- Batch API calls when possible
- Use wait nodes for rate limiting
- Split large data sets

### Debugging
- Add sticky notes explaining logic
- Use Set nodes to inspect data
- Enable execution saving during dev

---

## Common Workflows

### Lead Intake
```
Webhook (Form) → Validate → Enrich Data →
Score Lead → Route [
  Hot → Notify Sales
  Warm → Add to Nurture
  Cold → Store for Later
]
```

### Appointment Reminder
```
Schedule (Daily) → Get Tomorrow's Appointments →
Split → Send Reminder (Email/SMS) → Log Sent
```

### Data Sync
```
Schedule → Get Changes Since Last Run →
Transform → Upsert to Target → Update Last Run Time
```

### Alert Monitor
```
Schedule (5min) → Check Condition →
IF Problem → Send Alert + Log →
ELSE → No Action
```

---

## Anti-Patterns to Avoid

### Too Many Nodes
- If workflow > 30 nodes, consider splitting
- Use sub-workflows for reusable sections

### No Error Handling
- Every external call can fail
- Always have fallback paths

### Hardcoded Values
- Use variables and credentials
- Environment-specific configs

### Tight Coupling
- Workflows should be independent
- Use webhooks for workflow-to-workflow

### No Logging
- Can't debug what you can't see
- Log key decision points
