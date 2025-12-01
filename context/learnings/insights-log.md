# Insights Log

## Format
```
## [Date] - [Topic]
**Context:** What I was working on
**Insight:** What I learned
**Application:** How to use this going forward
```

---

## 2024-11-27 - Prompt Engineering System Design

**Context:** Designing comprehensive prompt engineering system for CoreReceptionAI

**Insight:** The value isn't in having prompts, it's in having structured context that can be dynamically assembled. Frameworks for thinking are more reusable than templates for specific tasks.

**Application:**
- Organize context by type (identity, business, technical)
- Create thinking frameworks, not just task templates
- Build assembly logic that matches context to task

---

## 2024-11 - n8n Docker Stack Maturity

**Context:** Running n8n stack with multiple services

**Insight:** The stack has grown organically and now includes more services than originally planned. pgvector being in the same Postgres instance makes vector operations easy without new infrastructure.

**Application:**
- Use pgvector for embeddings before adding Qdrant
- Document all services and their purposes
- Consider consolidation where services overlap

---

## 2024-11 - Voice AI Emergency Handling

**Context:** Designing AI receptionist prompts

**Insight:** Emergency detection is non-negotiable for voice AI in service industries. A single missed gas leak report could be catastrophic. The emergency path must be bulletproof.

**Application:**
- Always include comprehensive emergency keywords
- Emergency path = immediate human escalation
- Test emergency scenarios explicitly
- Document liability considerations

---

## 2024-11 - Lead Generation Texas PT

**Context:** Building lead gen system for physical therapy clinics

**Insight:** Web scraping + enrichment + scoring is powerful but requires careful validation. Google Places data quality varies significantly. Manual review of initial batches is essential.

**Application:**
- Build validation into pipelines
- Start with manual review, then automate
- Track data quality metrics
- Multiple sources > single source

---

## [Template for New Entries]

## YYYY-MM-DD - Topic

**Context:**

**Insight:**

**Application:**
-
-
-
