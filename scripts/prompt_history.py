#!/usr/bin/env python3
"""
Prompt History and Search System

A production-ready system for storing, searching, and analyzing prompt engineering history.
Features SQLite with FTS5 full-text search, tagging, categorization, and export capabilities.

Usage:
    python prompt_history.py --save "My prompt" --output "Response" --tags "test,dev"
    python prompt_history.py --search "keyword"
    python prompt_history.py --list-recent 10
    python prompt_history.py --export history.json
    python prompt_history.py --stats
"""

import sqlite3
import json
import csv
import argparse
import sys
from dataclasses import dataclass, field, asdict
from datetime import datetime, timedelta
from typing import List, Optional, Dict, Any, Union
from pathlib import Path
from contextlib import contextmanager
import re


@dataclass
class HistoryEntry:
    """Data class representing a single prompt history entry."""
    id: Optional[int] = None
    prompt: str = ""
    output: str = ""
    timestamp: Optional[datetime] = None
    framework_used: Optional[str] = None
    template_used: Optional[str] = None
    model: Optional[str] = None
    tokens: Optional[int] = None
    cost: Optional[float] = None
    tags: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        """Initialize timestamp if not provided."""
        if self.timestamp is None:
            self.timestamp = datetime.now()
        elif isinstance(self.timestamp, str):
            self.timestamp = datetime.fromisoformat(self.timestamp)

    def to_dict(self) -> Dict[str, Any]:
        """Convert entry to dictionary for serialization."""
        data = asdict(self)
        data['timestamp'] = self.timestamp.isoformat() if self.timestamp else None
        data['tags'] = ','.join(self.tags) if isinstance(self.tags, list) else self.tags
        data['metadata'] = json.dumps(self.metadata) if isinstance(self.metadata, dict) else self.metadata
        return data

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'HistoryEntry':
        """Create entry from dictionary."""
        if 'tags' in data and isinstance(data['tags'], str):
            data['tags'] = [t.strip() for t in data['tags'].split(',') if t.strip()]
        if 'metadata' in data and isinstance(data['metadata'], str):
            try:
                data['metadata'] = json.loads(data['metadata']) if data['metadata'] else {}
            except json.JSONDecodeError:
                data['metadata'] = {}
        return cls(**data)


class PromptHistoryDB:
    """SQLite database manager for prompt history with FTS5 full-text search."""

    def __init__(self, db_path: Optional[Path] = None):
        """
        Initialize database connection.

        Args:
            db_path: Path to SQLite database file. If None, uses default location.
        """
        if db_path is None:
            db_path = Path(__file__).parent.parent / "data" / "prompt_history.db"

        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._init_database()

    @contextmanager
    def _get_connection(self):
        """Context manager for database connections."""
        conn = sqlite3.connect(str(self.db_path))
        conn.row_factory = sqlite3.Row
        try:
            yield conn
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()

    def _init_database(self):
        """Initialize database schema with tables and indexes."""
        with self._get_connection() as conn:
            cursor = conn.cursor()

            # Main history table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    prompt TEXT NOT NULL,
                    output TEXT NOT NULL,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    framework_used TEXT,
                    template_used TEXT,
                    model TEXT,
                    tokens INTEGER,
                    cost REAL,
                    tags TEXT,
                    metadata TEXT
                )
            """)

            # Create indexes for fast queries
            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_timestamp
                ON history(timestamp DESC)
            """)

            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_framework
                ON history(framework_used)
            """)

            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_model
                ON history(model)
            """)

            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_tags
                ON history(tags)
            """)

            # FTS5 virtual table for full-text search
            cursor.execute("""
                CREATE VIRTUAL TABLE IF NOT EXISTS history_fts USING fts5(
                    prompt,
                    output,
                    tags,
                    content=history,
                    content_rowid=id
                )
            """)

            # Triggers to keep FTS table in sync
            cursor.execute("""
                CREATE TRIGGER IF NOT EXISTS history_ai AFTER INSERT ON history BEGIN
                    INSERT INTO history_fts(rowid, prompt, output, tags)
                    VALUES (new.id, new.prompt, new.output, new.tags);
                END
            """)

            cursor.execute("""
                CREATE TRIGGER IF NOT EXISTS history_ad AFTER DELETE ON history BEGIN
                    DELETE FROM history_fts WHERE rowid = old.id;
                END
            """)

            cursor.execute("""
                CREATE TRIGGER IF NOT EXISTS history_au AFTER UPDATE ON history BEGIN
                    UPDATE history_fts
                    SET prompt = new.prompt, output = new.output, tags = new.tags
                    WHERE rowid = new.id;
                END
            """)

    def save_entry(self, entry: HistoryEntry) -> int:
        """
        Save a history entry to the database.

        Args:
            entry: HistoryEntry object to save

        Returns:
            ID of the inserted entry
        """
        with self._get_connection() as conn:
            cursor = conn.cursor()

            data = entry.to_dict()
            data.pop('id', None)  # Remove id if present

            columns = ', '.join(data.keys())
            placeholders = ', '.join(['?' for _ in data])

            cursor.execute(
                f"INSERT INTO history ({columns}) VALUES ({placeholders})",
                list(data.values())
            )

            return cursor.lastrowid

    def search_history(
        self,
        query: str,
        limit: int = 50,
        offset: int = 0
    ) -> List[HistoryEntry]:
        """
        Full-text search across prompt history.

        Args:
            query: Search query string (FTS5 syntax supported)
            limit: Maximum number of results
            offset: Number of results to skip

        Returns:
            List of matching HistoryEntry objects
        """
        with self._get_connection() as conn:
            cursor = conn.cursor()

            # Use FTS5 MATCH for full-text search
            cursor.execute("""
                SELECT h.*
                FROM history h
                JOIN history_fts fts ON h.id = fts.rowid
                WHERE history_fts MATCH ?
                ORDER BY rank, h.timestamp DESC
                LIMIT ? OFFSET ?
            """, (query, limit, offset))

            return [self._row_to_entry(row) for row in cursor.fetchall()]

    def get_by_tag(
        self,
        tag: str,
        limit: int = 50,
        offset: int = 0
    ) -> List[HistoryEntry]:
        """
        Get entries by tag.

        Args:
            tag: Tag to filter by
            limit: Maximum number of results
            offset: Number of results to skip

        Returns:
            List of HistoryEntry objects
        """
        with self._get_connection() as conn:
            cursor = conn.cursor()

            # Search for tag in comma-separated tags field
            cursor.execute("""
                SELECT * FROM history
                WHERE tags LIKE ?
                ORDER BY timestamp DESC
                LIMIT ? OFFSET ?
            """, (f'%{tag}%', limit, offset))

            return [self._row_to_entry(row) for row in cursor.fetchall()]

    def get_by_date_range(
        self,
        start_date: datetime,
        end_date: Optional[datetime] = None,
        limit: int = 1000
    ) -> List[HistoryEntry]:
        """
        Get entries within a date range.

        Args:
            start_date: Start of date range
            end_date: End of date range (defaults to now)
            limit: Maximum number of results

        Returns:
            List of HistoryEntry objects
        """
        if end_date is None:
            end_date = datetime.now()

        with self._get_connection() as conn:
            cursor = conn.cursor()

            cursor.execute("""
                SELECT * FROM history
                WHERE timestamp BETWEEN ? AND ?
                ORDER BY timestamp DESC
                LIMIT ?
            """, (start_date.isoformat(), end_date.isoformat(), limit))

            return [self._row_to_entry(row) for row in cursor.fetchall()]

    def get_recent(self, limit: int = 10) -> List[HistoryEntry]:
        """
        Get most recent entries.

        Args:
            limit: Number of entries to retrieve

        Returns:
            List of HistoryEntry objects
        """
        with self._get_connection() as conn:
            cursor = conn.cursor()

            cursor.execute("""
                SELECT * FROM history
                ORDER BY timestamp DESC
                LIMIT ?
            """, (limit,))

            return [self._row_to_entry(row) for row in cursor.fetchall()]

    def get_by_framework(self, framework: str, limit: int = 50) -> List[HistoryEntry]:
        """Get entries by framework."""
        with self._get_connection() as conn:
            cursor = conn.cursor()

            cursor.execute("""
                SELECT * FROM history
                WHERE framework_used = ?
                ORDER BY timestamp DESC
                LIMIT ?
            """, (framework, limit))

            return [self._row_to_entry(row) for row in cursor.fetchall()]

    def get_by_model(self, model: str, limit: int = 50) -> List[HistoryEntry]:
        """Get entries by model."""
        with self._get_connection() as conn:
            cursor = conn.cursor()

            cursor.execute("""
                SELECT * FROM history
                WHERE model = ?
                ORDER BY timestamp DESC
                LIMIT ?
            """, (model, limit))

            return [self._row_to_entry(row) for row in cursor.fetchall()]

    def get_statistics(self) -> Dict[str, Any]:
        """
        Get statistics about prompt history.

        Returns:
            Dictionary containing various statistics
        """
        with self._get_connection() as conn:
            cursor = conn.cursor()

            stats = {}

            # Total entries
            cursor.execute("SELECT COUNT(*) FROM history")
            stats['total_entries'] = cursor.fetchone()[0]

            # Total tokens
            cursor.execute("SELECT SUM(tokens) FROM history WHERE tokens IS NOT NULL")
            result = cursor.fetchone()[0]
            stats['total_tokens'] = result if result else 0

            # Total cost
            cursor.execute("SELECT SUM(cost) FROM history WHERE cost IS NOT NULL")
            result = cursor.fetchone()[0]
            stats['total_cost'] = round(result, 4) if result else 0.0

            # Most used frameworks
            cursor.execute("""
                SELECT framework_used, COUNT(*) as count
                FROM history
                WHERE framework_used IS NOT NULL
                GROUP BY framework_used
                ORDER BY count DESC
                LIMIT 5
            """)
            stats['top_frameworks'] = [
                {'framework': row[0], 'count': row[1]}
                for row in cursor.fetchall()
            ]

            # Most used models
            cursor.execute("""
                SELECT model, COUNT(*) as count
                FROM history
                WHERE model IS NOT NULL
                GROUP BY model
                ORDER BY count DESC
                LIMIT 5
            """)
            stats['top_models'] = [
                {'model': row[0], 'count': row[1]}
                for row in cursor.fetchall()
            ]

            # Most common tags
            cursor.execute("SELECT tags FROM history WHERE tags IS NOT NULL AND tags != ''")
            all_tags = []
            for row in cursor.fetchall():
                all_tags.extend([t.strip() for t in row[0].split(',') if t.strip()])

            from collections import Counter
            tag_counts = Counter(all_tags)
            stats['top_tags'] = [
                {'tag': tag, 'count': count}
                for tag, count in tag_counts.most_common(10)
            ]

            # Entries per day (last 7 days)
            cursor.execute("""
                SELECT DATE(timestamp) as date, COUNT(*) as count
                FROM history
                WHERE timestamp >= datetime('now', '-7 days')
                GROUP BY DATE(timestamp)
                ORDER BY date DESC
            """)
            stats['recent_activity'] = [
                {'date': row[0], 'count': row[1]}
                for row in cursor.fetchall()
            ]

            # Date range
            cursor.execute("""
                SELECT MIN(timestamp), MAX(timestamp)
                FROM history
            """)
            min_date, max_date = cursor.fetchone()
            stats['date_range'] = {
                'earliest': min_date,
                'latest': max_date
            }

            return stats

    def export_to_json(self, output_path: Path, entries: Optional[List[HistoryEntry]] = None):
        """
        Export entries to JSON file.

        Args:
            output_path: Path to output JSON file
            entries: Specific entries to export (if None, exports all)
        """
        if entries is None:
            entries = self.get_recent(limit=10000)  # Get all entries

        data = [entry.to_dict() for entry in entries]

        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    def export_to_csv(self, output_path: Path, entries: Optional[List[HistoryEntry]] = None):
        """
        Export entries to CSV file.

        Args:
            output_path: Path to output CSV file
            entries: Specific entries to export (if None, exports all)
        """
        if entries is None:
            entries = self.get_recent(limit=10000)  # Get all entries

        if not entries:
            return

        fieldnames = list(entries[0].to_dict().keys())

        with open(output_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            for entry in entries:
                writer.writerow(entry.to_dict())

    def delete_entry(self, entry_id: int) -> bool:
        """
        Delete an entry by ID.

        Args:
            entry_id: ID of entry to delete

        Returns:
            True if deleted, False if not found
        """
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM history WHERE id = ?", (entry_id,))
            return cursor.rowcount > 0

    def _row_to_entry(self, row: sqlite3.Row) -> HistoryEntry:
        """Convert database row to HistoryEntry object."""
        data = dict(row)
        return HistoryEntry.from_dict(data)


class PromptHistory:
    """
    High-level interface for prompt history management.
    Use this class for integration with other scripts.
    """

    def __init__(self, db_path: Optional[Path] = None):
        """Initialize with database path."""
        self.db = PromptHistoryDB(db_path)

    def save(
        self,
        prompt: str,
        output: str,
        framework: Optional[str] = None,
        template: Optional[str] = None,
        model: Optional[str] = None,
        tokens: Optional[int] = None,
        cost: Optional[float] = None,
        tags: Optional[List[str]] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> int:
        """
        Save a prompt/output pair to history.

        Args:
            prompt: The prompt text
            output: The output/response text
            framework: Framework used (e.g., 'chain-of-thought', 'few-shot')
            template: Template used (if any)
            model: Model name (e.g., 'gpt-4', 'claude-3')
            tokens: Token count
            cost: Cost in dollars
            tags: List of tags
            metadata: Additional metadata dictionary

        Returns:
            ID of the saved entry
        """
        entry = HistoryEntry(
            prompt=prompt,
            output=output,
            framework_used=framework,
            template_used=template,
            model=model,
            tokens=tokens,
            cost=cost,
            tags=tags or [],
            metadata=metadata or {}
        )

        return self.db.save_entry(entry)

    def search(self, query: str, limit: int = 50) -> List[HistoryEntry]:
        """Search prompts and outputs."""
        return self.db.search_history(query, limit=limit)

    def get_by_tag(self, tag: str, limit: int = 50) -> List[HistoryEntry]:
        """Get entries by tag."""
        return self.db.get_by_tag(tag, limit=limit)

    def get_recent(self, limit: int = 10) -> List[HistoryEntry]:
        """Get recent entries."""
        return self.db.get_recent(limit=limit)

    def get_today(self) -> List[HistoryEntry]:
        """Get entries from today."""
        start = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        return self.db.get_by_date_range(start)

    def get_this_week(self) -> List[HistoryEntry]:
        """Get entries from this week."""
        start = datetime.now() - timedelta(days=7)
        return self.db.get_by_date_range(start)

    def export_json(self, output_path: Union[str, Path]):
        """Export all history to JSON."""
        self.db.export_to_json(Path(output_path))

    def export_csv(self, output_path: Union[str, Path]):
        """Export all history to CSV."""
        self.db.export_to_csv(Path(output_path))

    def stats(self) -> Dict[str, Any]:
        """Get statistics."""
        return self.db.get_statistics()


# CLI Functions

def print_entry(entry: HistoryEntry, verbose: bool = False):
    """Print a history entry in a readable format."""
    print(f"\n{'='*80}")
    print(f"ID: {entry.id}")
    print(f"Timestamp: {entry.timestamp.strftime('%Y-%m-%d %H:%M:%S')}")

    if entry.framework_used:
        print(f"Framework: {entry.framework_used}")
    if entry.template_used:
        print(f"Template: {entry.template_used}")
    if entry.model:
        print(f"Model: {entry.model}")
    if entry.tokens:
        print(f"Tokens: {entry.tokens:,}")
    if entry.cost:
        print(f"Cost: ${entry.cost:.4f}")
    if entry.tags:
        print(f"Tags: {', '.join(entry.tags)}")

    print(f"\n--- PROMPT ---")
    print(entry.prompt[:500] + ('...' if len(entry.prompt) > 500 else ''))

    if verbose:
        print(f"\n--- OUTPUT ---")
        print(entry.output[:1000] + ('...' if len(entry.output) > 1000 else ''))

        if entry.metadata:
            print(f"\n--- METADATA ---")
            print(json.dumps(entry.metadata, indent=2))


def print_stats(stats: Dict[str, Any]):
    """Print statistics in a readable format."""
    print("\n" + "="*80)
    print("PROMPT HISTORY STATISTICS")
    print("="*80)

    print(f"\nTotal Entries: {stats['total_entries']:,}")
    print(f"Total Tokens: {stats['total_tokens']:,}")
    print(f"Total Cost: ${stats['total_cost']:.2f}")

    if stats['date_range']['earliest']:
        print(f"\nDate Range:")
        print(f"  Earliest: {stats['date_range']['earliest']}")
        print(f"  Latest: {stats['date_range']['latest']}")

    if stats['top_frameworks']:
        print(f"\nTop Frameworks:")
        for item in stats['top_frameworks']:
            print(f"  {item['framework']}: {item['count']} entries")

    if stats['top_models']:
        print(f"\nTop Models:")
        for item in stats['top_models']:
            print(f"  {item['model']}: {item['count']} entries")

    if stats['top_tags']:
        print(f"\nTop Tags:")
        for item in stats['top_tags'][:10]:
            print(f"  #{item['tag']}: {item['count']} uses")

    if stats['recent_activity']:
        print(f"\nRecent Activity (Last 7 Days):")
        for item in stats['recent_activity']:
            print(f"  {item['date']}: {item['count']} entries")

    print("\n" + "="*80)


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description='Prompt History and Search System',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Save a new entry
  %(prog)s --save "Explain quantum computing" --output "Quantum computing uses..." --tags "science,education"

  # Search history
  %(prog)s --search "quantum"

  # List recent entries
  %(prog)s --list-recent 5

  # Get statistics
  %(prog)s --stats

  # Export to JSON
  %(prog)s --export history.json

  # Export to CSV
  %(prog)s --export history.csv

  # Filter by tag
  %(prog)s --tag "science"

  # Filter by framework
  %(prog)s --framework "chain-of-thought"
        """
    )

    # Database options
    parser.add_argument('--db', type=str, help='Path to database file')

    # Save options
    parser.add_argument('--save', type=str, help='Save a new prompt')
    parser.add_argument('--output', type=str, help='Output/response for the prompt')
    parser.add_argument('--framework', type=str, help='Framework used')
    parser.add_argument('--template', type=str, help='Template used')
    parser.add_argument('--model', type=str, help='Model name')
    parser.add_argument('--tokens', type=int, help='Token count')
    parser.add_argument('--cost', type=float, help='Cost in dollars')
    parser.add_argument('--tags', type=str, help='Comma-separated tags')
    parser.add_argument('--metadata', type=str, help='JSON metadata')

    # Query options
    parser.add_argument('--search', type=str, help='Search query')
    parser.add_argument('--tag', type=str, help='Filter by tag')
    parser.add_argument('--list-recent', type=int, metavar='N', help='List N recent entries')
    parser.add_argument('--today', action='store_true', help='Show today\'s entries')
    parser.add_argument('--week', action='store_true', help='Show this week\'s entries')

    # Export options
    parser.add_argument('--export', type=str, help='Export to file (JSON or CSV based on extension)')

    # Stats
    parser.add_argument('--stats', action='store_true', help='Show statistics')

    # Display options
    parser.add_argument('-v', '--verbose', action='store_true', help='Verbose output')
    parser.add_argument('--limit', type=int, default=10, help='Limit number of results')

    args = parser.parse_args()

    # Initialize history manager
    db_path = Path(args.db) if args.db else None
    history = PromptHistory(db_path)

    # Handle save operation
    if args.save:
        if not args.output:
            print("Error: --output is required when using --save", file=sys.stderr)
            sys.exit(1)

        tags = [t.strip() for t in args.tags.split(',') if t.strip()] if args.tags else []
        metadata = json.loads(args.metadata) if args.metadata else {}

        entry_id = history.save(
            prompt=args.save,
            output=args.output,
            framework=args.framework,
            template=args.template,
            model=args.model,
            tokens=args.tokens,
            cost=args.cost,
            tags=tags,
            metadata=metadata
        )

        print(f"Entry saved with ID: {entry_id}")
        return

    # Handle search operation
    if args.search:
        entries = history.search(args.search, limit=args.limit)
        print(f"\nFound {len(entries)} matching entries:")
        for entry in entries:
            print_entry(entry, verbose=args.verbose)
        return

    # Handle tag filter
    if args.tag:
        entries = history.get_by_tag(args.tag, limit=args.limit)
        print(f"\nFound {len(entries)} entries with tag '{args.tag}':")
        for entry in entries:
            print_entry(entry, verbose=args.verbose)
        return

    # Handle framework filter
    if args.framework:
        entries = history.db.get_by_framework(args.framework, limit=args.limit)
        print(f"\nFound {len(entries)} entries using framework '{args.framework}':")
        for entry in entries:
            print_entry(entry, verbose=args.verbose)
        return

    # Handle list recent
    if args.list_recent:
        entries = history.get_recent(limit=args.list_recent)
        print(f"\nShowing {len(entries)} most recent entries:")
        for entry in entries:
            print_entry(entry, verbose=args.verbose)
        return

    # Handle today filter
    if args.today:
        entries = history.get_today()
        print(f"\nFound {len(entries)} entries from today:")
        for entry in entries:
            print_entry(entry, verbose=args.verbose)
        return

    # Handle week filter
    if args.week:
        entries = history.get_this_week()
        print(f"\nFound {len(entries)} entries from this week:")
        for entry in entries:
            print_entry(entry, verbose=args.verbose)
        return

    # Handle export
    if args.export:
        export_path = Path(args.export)
        if export_path.suffix.lower() == '.json':
            history.export_json(export_path)
            print(f"Exported to {export_path}")
        elif export_path.suffix.lower() == '.csv':
            history.export_csv(export_path)
            print(f"Exported to {export_path}")
        else:
            print("Error: Export file must have .json or .csv extension", file=sys.stderr)
            sys.exit(1)
        return

    # Handle stats
    if args.stats:
        stats = history.stats()
        print_stats(stats)
        return

    # Default: show recent entries
    entries = history.get_recent(limit=5)
    print(f"\nShowing {len(entries)} most recent entries (use --help for more options):")
    for entry in entries:
        print_entry(entry, verbose=False)


if __name__ == '__main__':
    main()
