# n8n Workflow Specification Template

## Purpose
Standardized template for specifying n8n workflows before building.

---

## Template

```markdown
# Workflow: [WORKFLOW_NAME]

## Overview
**Purpose:** [One sentence describing what this workflow does]
**Trigger:** [What starts this workflow]
**Output:** [What this workflow produces]

---

## Trigger Configuration

### Type: [Webhook / Schedule / Manual / Event]

**Webhook:**
- Path: `/[path]`
- Method: [POST/GET]
- Authentication: [None/Header/Query]
- Expected payload:
```json
{
  "field1": "type",
  "field2": "type"
}
```

**Schedule:**
- Cron: `[expression]`
- Timezone: [timezone]
- Description: [human readable]

---

## Workflow Steps

### Step 1: [Name]
- **Node type:** [e.g., HTTP Request, Function, IF]
- **Purpose:** [What this step does]
- **Input:** [What it receives]
- **Output:** [What it produces]
- **Configuration:**
  - [Key setting 1]
  - [Key setting 2]

### Step 2: [Name]
[Same structure...]

### Step N: [Name]
[Same structure...]

---

## Data Transformations

### Input → Processing
```javascript
// Example transformation
const output = {
  processedField: $json.inputField.toUpperCase(),
  timestamp: new Date().toISOString()
};
return output;
```

### Processing → Output
[Describe final data shape]

---

## Error Handling

### Expected Errors
| Error | Cause | Handling |
|-------|-------|----------|
| [Error 1] | [Why it happens] | [What to do] |
| [Error 2] | [Why it happens] | [What to do] |

### Error Workflow
- Log to: [Where errors are logged]
- Alert via: [Notification method]
- Retry policy: [X retries with Y backoff]

---

## External Dependencies

### APIs
| Service | Endpoint | Auth Type | Rate Limit |
|---------|----------|-----------|------------|
| [Service] | [URL] | [Type] | [Limit] |

### Databases
| Database | Table/Collection | Operations |
|----------|------------------|------------|
| [DB name] | [Table] | [Read/Write/Both] |

### Credentials Required
- [ ] [Credential name 1]
- [ ] [Credential name 2]

---

## Testing Plan

### Test Cases
1. **Happy path:** [Description]
   - Input: [Sample input]
   - Expected output: [Expected result]

2. **Error case:** [Description]
   - Input: [Sample input]
   - Expected output: [Expected error handling]

3. **Edge case:** [Description]
   - Input: [Sample input]
   - Expected output: [Expected result]

### Test Data
```json
{
  "testCase1": {...},
  "testCase2": {...}
}
```

---

## Deployment Notes

### Environment Variables
| Variable | Purpose | Example |
|----------|---------|---------|
| [VAR_NAME] | [What it's for] | [Example value] |

### Activation Checklist
- [ ] All credentials configured
- [ ] Environment variables set
- [ ] Test in staging
- [ ] Error handling verified
- [ ] Monitoring/alerts configured
- [ ] Documentation updated

---

## Maintenance

### Monitoring
- Success metric: [What indicates success]
- Alert threshold: [When to alert]
- Dashboard: [Where to view stats]

### Common Issues
| Issue | Symptoms | Solution |
|-------|----------|----------|
| [Issue 1] | [What you see] | [How to fix] |

### Update Procedure
[How to safely update this workflow]
```

---

## Example: Lead Intake Workflow

```markdown
# Workflow: Lead Intake from Website

## Overview
**Purpose:** Receive lead form submissions and route to CRM
**Trigger:** Webhook from website form
**Output:** Lead created in CRM, confirmation email sent

---

## Trigger Configuration

### Type: Webhook
- Path: `/lead-intake`
- Method: POST
- Authentication: Header (X-API-Key)
- Expected payload:
```json
{
  "name": "string",
  "email": "string",
  "phone": "string",
  "message": "string",
  "source": "string"
}
```

---

## Workflow Steps

### Step 1: Validate Input
- **Node type:** IF
- **Purpose:** Check required fields present
- **Input:** Webhook payload
- **Output:** Valid/Invalid branch

### Step 2: Enrich Data
- **Node type:** HTTP Request
- **Purpose:** Get company info from Clearbit
- **Input:** Email domain
- **Output:** Company data

### Step 3: Create CRM Record
- **Node type:** HubSpot
- **Purpose:** Create contact in CRM
- **Input:** Merged lead + enrichment data
- **Output:** Contact ID

### Step 4: Send Confirmation
- **Node type:** Email
- **Purpose:** Send confirmation to lead
- **Input:** Lead email, template data
- **Output:** Email sent confirmation

### Step 5: Notify Sales
- **Node type:** Slack
- **Purpose:** Alert sales team
- **Input:** Lead summary
- **Output:** Slack message

---

## Error Handling

### Expected Errors
| Error | Cause | Handling |
|-------|-------|----------|
| Invalid email | Bad form input | Return 400, log |
| CRM API down | HubSpot outage | Retry 3x, queue for later |
| Enrichment fail | Clearbit limit | Continue without enrichment |

---

## Testing Plan

### Test Cases
1. **Happy path:** Valid lead creates contact and sends emails
2. **Invalid email:** Returns 400, no CRM record created
3. **No enrichment:** Creates record without company data
```
