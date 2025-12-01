# Prompt History System Architecture

## System Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                   Prompt History System                          │
│                                                                   │
│  ┌────────────────┐  ┌──────────────┐  ┌─────────────────┐     │
│  │   CLI Layer    │  │  Python API  │  │  Integration    │     │
│  │  (argparse)    │  │   (Public)   │  │    Hooks        │     │
│  └───────┬────────┘  └──────┬───────┘  └────────┬────────┘     │
│          │                  │                    │               │
│          └──────────────────┴────────────────────┘               │
│                             │                                    │
│                   ┌─────────▼─────────┐                         │
│                   │  PromptHistory    │                         │
│                   │  (High-level API) │                         │
│                   └─────────┬─────────┘                         │
│                             │                                    │
│                   ┌─────────▼──────────┐                        │
│                   │  PromptHistoryDB   │                        │
│                   │  (Database Layer)  │                        │
│                   └─────────┬──────────┘                        │
│                             │                                    │
│          ┌──────────────────┼──────────────────┐                │
│          │                  │                  │                │
│  ┌───────▼────────┐  ┌─────▼──────┐  ┌───────▼────────┐       │
│  │  Main Table    │  │  FTS5      │  │    Indexes     │       │
│  │   (history)    │  │  (Search)  │  │  (Performance) │       │
│  └────────────────┘  └────────────┘  └────────────────┘       │
│                                                                  │
│  ┌──────────────────────────────────────────────────────┐      │
│  │              SQLite Database                          │      │
│  │    (prompt_history.db)                               │      │
│  └──────────────────────────────────────────────────────┘      │
└─────────────────────────────────────────────────────────────────┘
```

## Component Architecture

### 1. CLI Layer (Command-Line Interface)

```
prompt_history.py --save "prompt" --output "response"
                    │
                    ├── Argument Parsing (argparse)
                    ├── Input Validation
                    └── Command Dispatch
                         │
                         ├── --save      → save_entry()
                         ├── --search    → search_history()
                         ├── --list      → get_recent()
                         ├── --export    → export_history()
                         └── --stats     → get_statistics()
```

### 2. Python API Layer

```
┌────────────────────────────────────────────────────┐
│           PromptHistory (High-level API)           │
├────────────────────────────────────────────────────┤
│  Methods:                                          │
│  • save(prompt, output, **kwargs) → int           │
│  • search(query) → List[HistoryEntry]             │
│  • get_by_tag(tag) → List[HistoryEntry]           │
│  • get_recent(limit) → List[HistoryEntry]         │
│  • get_today() → List[HistoryEntry]               │
│  • get_this_week() → List[HistoryEntry]           │
│  • export_json(path)                              │
│  • export_csv(path)                               │
│  • stats() → Dict[str, Any]                       │
└────────────────────────────────────────────────────┘
```

### 3. Database Layer

```
┌────────────────────────────────────────────────────┐
│         PromptHistoryDB (Database Manager)         │
├────────────────────────────────────────────────────┤
│  Internal Methods:                                 │
│  • _init_database() → Create schema               │
│  • _get_connection() → Context manager            │
│  • save_entry(entry) → int                        │
│  • search_history(query) → List[HistoryEntry]     │
│  • get_by_tag(tag) → List[HistoryEntry]           │
│  • get_by_date_range() → List[HistoryEntry]       │
│  • get_by_framework() → List[HistoryEntry]        │
│  • get_statistics() → Dict[str, Any]              │
│  • export_to_json(path)                           │
│  • export_to_csv(path)                            │
└────────────────────────────────────────────────────┘
```

## Data Flow

### Save Operation

```
User Input
    │
    ▼
CLI/API → HistoryEntry (dataclass)
              │
              ▼
    PromptHistory.save()
              │
              ▼
    PromptHistoryDB.save_entry()
              │
              ├─→ INSERT into history table
              │
              └─→ FTS5 trigger → INSERT into history_fts
                                       │
                                       ▼
                               Return entry_id
```

### Search Operation

```
Search Query
    │
    ▼
PromptHistory.search(query)
    │
    ▼
PromptHistoryDB.search_history(query)
    │
    ├─→ SELECT with FTS5 MATCH
    │   (Full-text search with ranking)
    │
    ├─→ Apply LIMIT and OFFSET
    │
    ├─→ Convert rows to HistoryEntry objects
    │
    └─→ Return List[HistoryEntry]
```

### Statistics Operation

```
stats() call
    │
    ├─→ COUNT(*) → total_entries
    ├─→ SUM(tokens) → total_tokens
    ├─→ SUM(cost) → total_cost
    ├─→ GROUP BY framework_used → top_frameworks
    ├─→ GROUP BY model → top_models
    ├─→ Parse tags → top_tags
    ├─→ COUNT by DATE → recent_activity
    └─→ Return aggregated statistics
```

## Database Schema

```
┌─────────────────────────────────────────────────────────┐
│                    history (Main Table)                  │
├─────────────────┬───────────┬───────────────────────────┤
│ Column          │ Type      │ Constraints               │
├─────────────────┼───────────┼───────────────────────────┤
│ id              │ INTEGER   │ PRIMARY KEY AUTOINCREMENT │
│ prompt          │ TEXT      │ NOT NULL                  │
│ output          │ TEXT      │ NOT NULL                  │
│ timestamp       │ TIMESTAMP │ DEFAULT CURRENT_TIMESTAMP │
│ framework_used  │ TEXT      │ NULL                      │
│ template_used   │ TEXT      │ NULL                      │
│ model           │ TEXT      │ NULL                      │
│ tokens          │ INTEGER   │ NULL                      │
│ cost            │ REAL      │ NULL                      │
│ tags            │ TEXT      │ NULL (comma-separated)    │
│ metadata        │ TEXT      │ NULL (JSON string)        │
└─────────────────┴───────────┴───────────────────────────┘

┌─────────────────────────────────────────────────────────┐
│              history_fts (FTS5 Virtual Table)            │
├─────────────────┬───────────┬───────────────────────────┤
│ Column          │ Type      │ Source                    │
├─────────────────┼───────────┼───────────────────────────┤
│ rowid           │ INTEGER   │ history.id                │
│ prompt          │ TEXT      │ history.prompt            │
│ output          │ TEXT      │ history.output            │
│ tags            │ TEXT      │ history.tags              │
└─────────────────┴───────────┴───────────────────────────┘

Indexes:
• idx_timestamp  ON history(timestamp DESC)
• idx_framework  ON history(framework_used)
• idx_model      ON history(model)
• idx_tags       ON history(tags)

Triggers:
• history_ai (AFTER INSERT)  → Sync to FTS
• history_au (AFTER UPDATE)  → Sync to FTS
• history_ad (AFTER DELETE)  → Sync to FTS
```

## Integration Patterns

### Pattern 1: Direct Import

```
┌──────────────┐
│ Your Script  │
└──────┬───────┘
       │ import
       ▼
┌──────────────────┐
│ PromptHistory    │
│ .save()          │
└──────────────────┘
```

### Pattern 2: Decorator

```
┌──────────────┐
│ @track_prompt│ (Decorator)
└──────┬───────┘
       │ wraps
       ▼
┌──────────────┐
│ Your Function│
└──────┬───────┘
       │ calls
       ▼
┌──────────────────┐
│ PromptHistory    │
│ .save()          │
└──────────────────┘
```

### Pattern 3: Context Manager

```
┌─────────────────────┐
│ with track_execution│
└──────┬──────────────┘
       │
   ┌───▼────┐
   │Execute │
   └───┬────┘
       │ finally
       ▼
┌──────────────────┐
│ PromptHistory    │
│ .save()          │
└──────────────────┘
```

### Pattern 4: Callback

```
┌──────────────┐
│ AI Client    │
└──────┬───────┘
       │ event
       ▼
┌──────────────┐
│ Callback     │
└──────┬───────┘
       │
       ▼
┌──────────────────┐
│ PromptHistory    │
│ .save()          │
└──────────────────┘
```

## Integration with System Components

```
┌─────────────────────────────────────────────────────────┐
│             Prompt Engineering System                    │
├─────────────────────────────────────────────────────────┤
│                                                           │
│  ┌────────────────┐         ┌─────────────────┐         │
│  │ prompt_        │◄────────┤ Prompt History  │         │
│  │ optimizer.py   │  Track  │                 │         │
│  └────────────────┘         │  ┌───────────┐  │         │
│                             │  │  SQLite   │  │         │
│  ┌────────────────┐         │  │  + FTS5   │  │         │
│  │ model_         │◄────────┤  └───────────┘  │         │
│  │ orchestrator.py│  Track  │                 │         │
│  └────────────────┘         │  ┌───────────┐  │         │
│                             │  │ Search &  │  │         │
│  ┌────────────────┐         │  │ Analytics │  │         │
│  │ feedback_      │◄────────┤  └───────────┘  │         │
│  │ system.py      │  Track  │                 │         │
│  └────────────────┘         │  ┌───────────┐  │         │
│                             │  │  Export   │  │         │
│  ┌────────────────┐         │  │ JSON/CSV  │  │         │
│  │ cache_         │◄────────┤  └───────────┘  │         │
│  │ manager.py     │  Track  └─────────────────┘         │
│  └────────────────┘                                      │
│                                                           │
│  ┌────────────────┐                                      │
│  │ Any Custom     │                                      │
│  │ Script         │◄─────────────────────────────────────┤
│  └────────────────┘         Easy Integration             │
│                                                           │
└─────────────────────────────────────────────────────────┘
```

## Query Performance

```
Query Type          Index Used        Time Complexity
─────────────────────────────────────────────────────
Full-text search    FTS5             O(log n + k)
Recent entries      idx_timestamp    O(log n)
By tag             idx_tags          O(log n + m)
By framework       idx_framework     O(log n + m)
By model           idx_model         O(log n + m)
Date range         idx_timestamp     O(log n + m)
Statistics         All indexes       O(n) aggregate

Where:
n = total entries
k = matching entries (FTS)
m = matching entries (filter)
```

## Storage Characteristics

```
Entry Size Breakdown:
┌────────────────────────────────┐
│ Field         │ Avg Size       │
├───────────────┼────────────────┤
│ Prompt        │ ~200 bytes     │
│ Output        │ ~500 bytes     │
│ Metadata      │ ~100 bytes     │
│ Other fields  │ ~50 bytes      │
├───────────────┼────────────────┤
│ Total/entry   │ ~850 bytes     │
│ With FTS      │ ~1KB/entry     │
└────────────────────────────────┘

Database Growth:
• 1,000 entries   ≈ 1 MB
• 10,000 entries  ≈ 10 MB
• 100,000 entries ≈ 100 MB
```

## Error Handling Flow

```
Operation
    │
    ├─→ Try execution
    │       │
    │       ├─→ Success → Return result
    │       │
    │       └─→ Exception
    │               │
    │               ├─→ Rollback transaction
    │               ├─→ Log error
    │               ├─→ Clean up resources
    │               └─→ Raise or return None
    │
    └─→ Finally: Close connections
```

## Export Architecture

```
Export Request
    │
    ├─→ Format selection (JSON/CSV)
    │
    ├─→ Query entries
    │       │
    │       ├─→ All entries or
    │       └─→ Filtered subset
    │
    ├─→ Convert to format
    │       │
    │       ├─→ JSON: to_dict() → json.dump()
    │       └─→ CSV: to_dict() → csv.writer()
    │
    └─→ Write to file
            │
            ├─→ Success → Return path
            └─→ Error → Raise exception
```

## Security Model

```
┌──────────────────────────────────┐
│     Security Considerations       │
├──────────────────────────────────┤
│                                   │
│ ✓ Local storage only             │
│ ✓ No external connections        │
│ ✓ No authentication required     │
│ ✓ SQL injection: Parameterized   │
│ ✓ Path traversal: Validated      │
│ ✓ JSON injection: Escaped        │
│                                   │
│ User Responsibilities:            │
│ • Protect database file          │
│ • Encrypt exports if needed      │
│ • Sanitize metadata              │
│ • Don't store secrets            │
└──────────────────────────────────┘
```

## Scalability

```
Scale Factor     Performance Notes
──────────────────────────────────
< 10K entries    Instant queries
10K - 100K       Fast with indexes
100K - 1M        Consider archiving
> 1M             Partition by date

Optimization Options:
1. Archive old entries
2. Separate DBs by project
3. Regular VACUUM
4. Index-only queries
5. Batch operations
```

## Development Workflow

```
Development Flow:
┌─────────────┐
│   Develop   │
│   Prompt    │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│   Execute   │ ──→ Auto-track to history
└──────┬──────┘
       │
       ▼
┌─────────────┐
│   Analyze   │ ──→ Search/filter history
└──────┬──────┘
       │
       ▼
┌─────────────┐
│   Refine    │ ──→ Learn from past
└──────┬──────┘
       │
       ▼
┌─────────────┐
│   Repeat    │
└─────────────┘

Analysis Tools:
• Search: Find similar
• Stats: Measure usage
• Export: Deep analysis
• Filter: Focus on subset
```

## Deployment

```
Deployment Options:

1. Single User
   └─→ Default location
       └─→ Auto-created database

2. Project-Specific
   └─→ Custom db_path
       └─→ Per-project tracking

3. Team Shared
   └─→ Network drive (read-only safe)
       └─→ Regular exports

4. Production
   └─→ Automated backups
       └─→ Monitoring
       └─→ Archival strategy
```

## Summary

The Prompt History system provides:

- **Modular Design**: Clear separation of concerns
- **Extensible**: Easy to add new features
- **Performant**: Optimized queries with proper indexing
- **Reliable**: ACID transactions, error handling
- **Scalable**: Handles 100K+ entries efficiently
- **Flexible**: Multiple integration patterns
- **Simple**: Zero configuration required

Ready for production use!
