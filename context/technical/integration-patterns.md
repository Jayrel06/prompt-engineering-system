# Integration Patterns

## API Integration Fundamentals

### Authentication Patterns

#### API Key (Header)
```
Headers: { "Authorization": "Bearer {API_KEY}" }
```
- Simple, common
- Store in credentials manager
- Rotate periodically

#### API Key (Query Parameter)
```
URL: https://api.example.com/data?api_key={KEY}
```
- Less secure (visible in logs)
- Use only when required

#### OAuth 2.0
```
1. Redirect to auth URL
2. User authorizes
3. Receive code
4. Exchange for token
5. Use token for requests
6. Refresh when expired
```
- More complex but more secure
- Required for many platforms

---

## Webhook Patterns

### Receiving Webhooks
```
Webhook URL → Validate Signature → Parse Payload →
Process → Return 200 OK
```

**Key Points:**
- Always validate signature/token
- Return 200 quickly (process async if needed)
- Log all incoming webhooks
- Handle duplicates idempotently

### Sending Webhooks
```
Event Occurs → Format Payload →
POST to URL → Handle Response [
  Success → Log
  Failure → Retry with backoff
]
```

**Key Points:**
- Include timestamp and event ID
- Retry failed deliveries
- Allow webhook URL configuration

---

## Data Sync Patterns

### One-Way Sync (Push)
```
Source Change → Transform → Push to Target
```
- Simplest pattern
- Good for notifications, logs

### One-Way Sync (Pull)
```
Schedule → Query Source for Changes →
Transform → Update Target → Store Checkpoint
```
- Good for batch processing
- Need to track "last sync" point

### Two-Way Sync
```
Source A Change → [
  Check for conflicts → [
    No conflict → Update Source B
    Conflict → Resolution logic
  ]
]
Source B Change → (same in reverse)
```
- Complex, avoid if possible
- Clear conflict resolution rules required

---

## Error Handling

### Retry Strategy
```python
max_retries = 3
backoff_seconds = [1, 5, 30]

for attempt in range(max_retries):
    try:
        response = make_request()
        break
    except TransientError:
        if attempt < max_retries - 1:
            sleep(backoff_seconds[attempt])
        else:
            raise
```

### Circuit Breaker
```
Normal State → Track Failures →
If failures > threshold → Open Circuit →
After timeout → Half-Open (try one) →
If success → Close Circuit
If failure → Back to Open
```
- Prevents cascading failures
- Gives systems time to recover

### Dead Letter Queue
```
Failed Message → Retry Queue →
After X retries → Dead Letter Queue →
Alert for manual review
```

---

## Rate Limiting

### Client-Side Throttling
```python
from ratelimit import limits, sleep_and_retry

@sleep_and_retry
@limits(calls=100, period=60)  # 100 calls per minute
def call_api():
    return requests.get(url)
```

### Handling 429 (Too Many Requests)
```
Request → Response [
  429 → Wait (Retry-After header or exponential backoff) → Retry
  200 → Process
]
```

---

## Common Integration Recipes

### CRM → n8n → Action
```
CRM Webhook (new lead) →
n8n receives → Enrich data →
Route based on criteria →
Update CRM with enrichment
```

### Form → Processing → Multiple Destinations
```
Form Webhook → Validate →
[Parallel]
  → CRM (create contact)
  → Email (send confirmation)
  → Slack (notify team)
  → Sheet (backup)
```

### Scheduled Data Pull
```
Cron (hourly) →
Query API (changes since last run) →
Transform → Upsert to DB →
Update last_run timestamp
```

### Event-Driven Pipeline
```
Source Event → Queue (Redis/RabbitMQ) →
Worker picks up → Process →
Emit completion event →
Next stage picks up
```

---

## Best Practices

### Always
- Validate inputs
- Log requests and responses (sanitized)
- Handle timeouts explicitly
- Use idempotency keys when available
- Store credentials securely

### Never
- Hardcode credentials
- Ignore rate limits
- Trust incoming webhook data without validation
- Block on long-running API calls
- Assume APIs are always available

### Testing
- Mock external APIs in tests
- Test error scenarios
- Verify retry logic works
- Load test critical integrations
