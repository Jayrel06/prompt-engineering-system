#!/usr/bin/env python3
"""
Cost Tracker - Track token usage and costs for LLM requests.

Usage:
    cost_tracker.py log --model <model> --input-tokens <n> --output-tokens <n> [--category <cat>] [--description <desc>]
    cost_tracker.py report [--period daily|weekly|monthly] [--model <model>] [--category <cat>] [--start-date YYYY-MM-DD] [--end-date YYYY-MM-DD]
    cost_tracker.py export [--format csv|json] [--output <file>] [--start-date YYYY-MM-DD] [--end-date YYYY-MM-DD]
    cost_tracker.py stats [--model <model>] [--period daily|weekly|monthly]
    cost_tracker.py init

Examples:
    cost_tracker.py log --model claude-sonnet-3.5 --input-tokens 1000 --output-tokens 500 --category planning
    cost_tracker.py report --period weekly --model claude-sonnet-3.5
    cost_tracker.py export --format csv --output usage_report.csv
"""

import argparse
import sqlite3
import json
import csv
import sys
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
from decimal import Decimal

# Get project paths
SCRIPT_DIR = Path(__file__).parent
PROJECT_ROOT = SCRIPT_DIR.parent
DATA_DIR = PROJECT_ROOT / "data"
DB_PATH = DATA_DIR / "usage.db"

# Model pricing (per million tokens)
MODEL_PRICING = {
    "claude-sonnet-3.5": {
        "input": Decimal("3.00"),
        "output": Decimal("15.00"),
        "alias": ["sonnet", "claude-3.5-sonnet", "claude-3-5-sonnet-20241022"]
    },
    "claude-haiku-3": {
        "input": Decimal("0.25"),
        "output": Decimal("1.25"),
        "alias": ["haiku", "claude-3-haiku", "claude-3-haiku-20240307"]
    },
    "gpt-4o": {
        "input": Decimal("2.50"),
        "output": Decimal("10.00"),
        "alias": ["gpt4o", "gpt-4o-2024-11-20"]
    },
    "gpt-4o-mini": {
        "input": Decimal("0.15"),
        "output": Decimal("0.60"),
        "alias": ["gpt4mini", "gpt-4o-mini-2024-07-18"]
    }
}

# Build reverse lookup for aliases
MODEL_ALIAS_MAP = {}
for canonical, config in MODEL_PRICING.items():
    MODEL_ALIAS_MAP[canonical] = canonical
    for alias in config.get("alias", []):
        MODEL_ALIAS_MAP[alias.lower()] = canonical


def normalize_model_name(model: str) -> str:
    """Normalize model name to canonical form."""
    model_lower = model.lower()
    return MODEL_ALIAS_MAP.get(model_lower, model)


def get_db_connection() -> sqlite3.Connection:
    """Get database connection."""
    DATA_DIR.mkdir(exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_database():
    """Initialize the database schema."""
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS usage_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            model TEXT NOT NULL,
            input_tokens INTEGER NOT NULL,
            output_tokens INTEGER NOT NULL,
            total_tokens INTEGER NOT NULL,
            input_cost REAL NOT NULL,
            output_cost REAL NOT NULL,
            total_cost REAL NOT NULL,
            category TEXT,
            description TEXT,
            metadata TEXT
        )
    """)

    cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_timestamp ON usage_log(timestamp)
    """)

    cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_model ON usage_log(model)
    """)

    cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_category ON usage_log(category)
    """)

    conn.commit()
    conn.close()

    print(f"Database initialized at: {DB_PATH}")


def calculate_cost(model: str, input_tokens: int, output_tokens: int) -> Tuple[Decimal, Decimal, Decimal]:
    """Calculate costs for token usage."""
    model = normalize_model_name(model)

    if model not in MODEL_PRICING:
        raise ValueError(f"Unknown model: {model}. Supported models: {', '.join(MODEL_PRICING.keys())}")

    pricing = MODEL_PRICING[model]

    # Cost per million tokens
    input_cost = (Decimal(input_tokens) / Decimal(1_000_000)) * pricing["input"]
    output_cost = (Decimal(output_tokens) / Decimal(1_000_000)) * pricing["output"]
    total_cost = input_cost + output_cost

    return input_cost, output_cost, total_cost


def log_usage(
    model: str,
    input_tokens: int,
    output_tokens: int,
    category: Optional[str] = None,
    description: Optional[str] = None,
    metadata: Optional[Dict] = None
) -> int:
    """Log a usage entry and return the entry ID."""
    model = normalize_model_name(model)

    # Calculate costs
    input_cost, output_cost, total_cost = calculate_cost(model, input_tokens, output_tokens)
    total_tokens = input_tokens + output_tokens

    # Store metadata as JSON
    metadata_json = json.dumps(metadata) if metadata else None

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO usage_log
        (model, input_tokens, output_tokens, total_tokens,
         input_cost, output_cost, total_cost, category, description, metadata)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        model, input_tokens, output_tokens, total_tokens,
        float(input_cost), float(output_cost), float(total_cost),
        category, description, metadata_json
    ))

    entry_id = cursor.lastrowid
    conn.commit()
    conn.close()

    print(f"Logged usage entry #{entry_id}")
    print(f"Model: {model}")
    print(f"Tokens: {input_tokens:,} input + {output_tokens:,} output = {total_tokens:,} total")
    print(f"Cost: ${input_cost:.6f} + ${output_cost:.6f} = ${total_cost:.6f}")
    if category:
        print(f"Category: {category}")

    return entry_id


def generate_report(
    period: str = "daily",
    model: Optional[str] = None,
    category: Optional[str] = None,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None
) -> None:
    """Generate usage report."""
    conn = get_db_connection()
    cursor = conn.cursor()

    # Build query
    where_clauses = []
    params = []

    if model:
        model = normalize_model_name(model)
        where_clauses.append("model = ?")
        params.append(model)

    if category:
        where_clauses.append("category = ?")
        params.append(category)

    # Handle date range
    if start_date:
        where_clauses.append("DATE(timestamp) >= ?")
        params.append(start_date)

    if end_date:
        where_clauses.append("DATE(timestamp) <= ?")
        params.append(end_date)
    elif period:
        # Set default end date to today and calculate start date based on period
        end_dt = datetime.now()
        if period == "daily":
            start_dt = end_dt.replace(hour=0, minute=0, second=0, microsecond=0)
        elif period == "weekly":
            start_dt = end_dt - timedelta(days=7)
        elif period == "monthly":
            start_dt = end_dt - timedelta(days=30)
        else:
            start_dt = None

        if start_dt:
            where_clauses.append("timestamp >= ?")
            params.append(start_dt.isoformat())

    where_sql = " AND ".join(where_clauses) if where_clauses else "1=1"

    # Get summary statistics
    cursor.execute(f"""
        SELECT
            COUNT(*) as request_count,
            SUM(input_tokens) as total_input_tokens,
            SUM(output_tokens) as total_output_tokens,
            SUM(total_tokens) as total_tokens,
            SUM(input_cost) as total_input_cost,
            SUM(output_cost) as total_output_cost,
            SUM(total_cost) as total_cost
        FROM usage_log
        WHERE {where_sql}
    """, params)

    summary = cursor.fetchone()

    # Get breakdown by model
    cursor.execute(f"""
        SELECT
            model,
            COUNT(*) as request_count,
            SUM(input_tokens) as input_tokens,
            SUM(output_tokens) as output_tokens,
            SUM(total_tokens) as total_tokens,
            SUM(total_cost) as total_cost
        FROM usage_log
        WHERE {where_sql}
        GROUP BY model
        ORDER BY total_cost DESC
    """, params)

    by_model = cursor.fetchall()

    # Get breakdown by category
    cursor.execute(f"""
        SELECT
            COALESCE(category, 'uncategorized') as category,
            COUNT(*) as request_count,
            SUM(total_tokens) as total_tokens,
            SUM(total_cost) as total_cost
        FROM usage_log
        WHERE {where_sql}
        GROUP BY category
        ORDER BY total_cost DESC
    """, params)

    by_category = cursor.fetchall()

    # Get daily breakdown
    cursor.execute(f"""
        SELECT
            DATE(timestamp) as date,
            COUNT(*) as request_count,
            SUM(total_tokens) as total_tokens,
            SUM(total_cost) as total_cost
        FROM usage_log
        WHERE {where_sql}
        GROUP BY DATE(timestamp)
        ORDER BY date DESC
        LIMIT 30
    """, params)

    by_date = cursor.fetchall()

    conn.close()

    # Print report
    print("\n" + "=" * 80)
    print(f"USAGE REPORT - {period.upper() if period else 'ALL TIME'}")
    if model:
        print(f"Model Filter: {model}")
    if category:
        print(f"Category Filter: {category}")
    if start_date or end_date:
        print(f"Date Range: {start_date or 'start'} to {end_date or 'end'}")
    print("=" * 80)

    print("\nOVERALL SUMMARY")
    print("-" * 80)
    print(f"Total Requests:      {summary['request_count']:,}")
    print(f"Total Input Tokens:  {summary['total_input_tokens']:,}")
    print(f"Total Output Tokens: {summary['total_output_tokens']:,}")
    print(f"Total Tokens:        {summary['total_tokens']:,}")
    print(f"Total Input Cost:    ${summary['total_input_cost']:.6f}")
    print(f"Total Output Cost:   ${summary['total_output_cost']:.6f}")
    print(f"TOTAL COST:          ${summary['total_cost']:.2f}")

    if by_model:
        print("\n\nBREAKDOWN BY MODEL")
        print("-" * 80)
        print(f"{'Model':<30} {'Requests':>10} {'Tokens':>15} {'Cost':>12}")
        print("-" * 80)
        for row in by_model:
            print(f"{row['model']:<30} {row['request_count']:>10,} {row['total_tokens']:>15,} ${row['total_cost']:>11.2f}")

    if by_category:
        print("\n\nBREAKDOWN BY CATEGORY")
        print("-" * 80)
        print(f"{'Category':<30} {'Requests':>10} {'Tokens':>15} {'Cost':>12}")
        print("-" * 80)
        for row in by_category:
            print(f"{row['category']:<30} {row['request_count']:>10,} {row['total_tokens']:>15,} ${row['total_cost']:>11.2f}")

    if by_date:
        print("\n\nDAILY BREAKDOWN (Last 30 days)")
        print("-" * 80)
        print(f"{'Date':<15} {'Requests':>10} {'Tokens':>15} {'Cost':>12}")
        print("-" * 80)
        for row in by_date:
            print(f"{row['date']:<15} {row['request_count']:>10,} {row['total_tokens']:>15,} ${row['total_cost']:>11.2f}")

    print("\n" + "=" * 80 + "\n")


def export_data(
    format: str = "csv",
    output: Optional[str] = None,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    model: Optional[str] = None,
    category: Optional[str] = None
) -> None:
    """Export usage data to CSV or JSON."""
    conn = get_db_connection()
    cursor = conn.cursor()

    # Build query
    where_clauses = []
    params = []

    if model:
        model = normalize_model_name(model)
        where_clauses.append("model = ?")
        params.append(model)

    if category:
        where_clauses.append("category = ?")
        params.append(category)

    if start_date:
        where_clauses.append("DATE(timestamp) >= ?")
        params.append(start_date)

    if end_date:
        where_clauses.append("DATE(timestamp) <= ?")
        params.append(end_date)

    where_sql = " AND ".join(where_clauses) if where_clauses else "1=1"

    cursor.execute(f"""
        SELECT
            id, timestamp, model, input_tokens, output_tokens, total_tokens,
            input_cost, output_cost, total_cost, category, description
        FROM usage_log
        WHERE {where_sql}
        ORDER BY timestamp DESC
    """, params)

    rows = cursor.fetchall()
    conn.close()

    if not rows:
        print("No data to export")
        return

    # Prepare output
    if format == "csv":
        output_file = output or "usage_export.csv"
        with open(output_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow([
                'ID', 'Timestamp', 'Model', 'Input Tokens', 'Output Tokens', 'Total Tokens',
                'Input Cost', 'Output Cost', 'Total Cost', 'Category', 'Description'
            ])
            for row in rows:
                writer.writerow([
                    row['id'], row['timestamp'], row['model'],
                    row['input_tokens'], row['output_tokens'], row['total_tokens'],
                    f"${row['input_cost']:.6f}", f"${row['output_cost']:.6f}", f"${row['total_cost']:.6f}",
                    row['category'] or '', row['description'] or ''
                ])
        print(f"Exported {len(rows)} records to {output_file}")

    elif format == "json":
        output_file = output or "usage_export.json"
        data = []
        for row in rows:
            data.append({
                'id': row['id'],
                'timestamp': row['timestamp'],
                'model': row['model'],
                'input_tokens': row['input_tokens'],
                'output_tokens': row['output_tokens'],
                'total_tokens': row['total_tokens'],
                'input_cost': row['input_cost'],
                'output_cost': row['output_cost'],
                'total_cost': row['total_cost'],
                'category': row['category'],
                'description': row['description']
            })

        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)
        print(f"Exported {len(rows)} records to {output_file}")


def show_stats(model: Optional[str] = None, period: str = "monthly") -> None:
    """Show quick statistics."""
    conn = get_db_connection()
    cursor = conn.cursor()

    # Calculate date range for period
    end_dt = datetime.now()
    if period == "daily":
        start_dt = end_dt.replace(hour=0, minute=0, second=0, microsecond=0)
    elif period == "weekly":
        start_dt = end_dt - timedelta(days=7)
    elif period == "monthly":
        start_dt = end_dt - timedelta(days=30)
    else:
        start_dt = None

    where_clauses = []
    params = []

    if start_dt:
        where_clauses.append("timestamp >= ?")
        params.append(start_dt.isoformat())

    if model:
        model = normalize_model_name(model)
        where_clauses.append("model = ?")
        params.append(model)

    where_sql = " AND ".join(where_clauses) if where_clauses else "1=1"

    cursor.execute(f"""
        SELECT
            COUNT(*) as requests,
            SUM(total_tokens) as tokens,
            SUM(total_cost) as cost,
            AVG(total_cost) as avg_cost_per_request
        FROM usage_log
        WHERE {where_sql}
    """, params)

    stats = cursor.fetchone()
    conn.close()

    print(f"\n{period.upper()} STATS" + (f" - {model}" if model else ""))
    print("-" * 40)
    print(f"Requests:           {stats['requests']:,}")
    print(f"Total Tokens:       {stats['tokens'] or 0:,}")
    print(f"Total Cost:         ${stats['cost'] or 0:.2f}")
    print(f"Avg Cost/Request:   ${stats['avg_cost_per_request'] or 0:.4f}")
    print()


def main():
    parser = argparse.ArgumentParser(
        description="LLM Cost Tracker - Track token usage and costs",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )

    subparsers = parser.add_subparsers(dest="command", help="Command to run")

    # Init command
    init_parser = subparsers.add_parser("init", help="Initialize database")

    # Log command
    log_parser = subparsers.add_parser("log", help="Log a usage entry")
    log_parser.add_argument("--model", required=True, help="Model name")
    log_parser.add_argument("--input-tokens", type=int, required=True, help="Input token count")
    log_parser.add_argument("--output-tokens", type=int, required=True, help="Output token count")
    log_parser.add_argument("--category", help="Usage category (e.g., planning, technical, communication)")
    log_parser.add_argument("--description", help="Description of the request")

    # Report command
    report_parser = subparsers.add_parser("report", help="Generate usage report")
    report_parser.add_argument("--period", choices=["daily", "weekly", "monthly"], default="monthly",
                              help="Report period")
    report_parser.add_argument("--model", help="Filter by model")
    report_parser.add_argument("--category", help="Filter by category")
    report_parser.add_argument("--start-date", help="Start date (YYYY-MM-DD)")
    report_parser.add_argument("--end-date", help="End date (YYYY-MM-DD)")

    # Export command
    export_parser = subparsers.add_parser("export", help="Export usage data")
    export_parser.add_argument("--format", choices=["csv", "json"], default="csv", help="Export format")
    export_parser.add_argument("--output", help="Output file path")
    export_parser.add_argument("--start-date", help="Start date (YYYY-MM-DD)")
    export_parser.add_argument("--end-date", help="End date (YYYY-MM-DD)")
    export_parser.add_argument("--model", help="Filter by model")
    export_parser.add_argument("--category", help="Filter by category")

    # Stats command
    stats_parser = subparsers.add_parser("stats", help="Show quick statistics")
    stats_parser.add_argument("--model", help="Filter by model")
    stats_parser.add_argument("--period", choices=["daily", "weekly", "monthly"], default="monthly",
                            help="Stats period")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    try:
        if args.command == "init":
            init_database()

        elif args.command == "log":
            log_usage(
                model=args.model,
                input_tokens=args.input_tokens,
                output_tokens=args.output_tokens,
                category=args.category,
                description=args.description
            )

        elif args.command == "report":
            generate_report(
                period=args.period,
                model=args.model,
                category=args.category,
                start_date=args.start_date,
                end_date=args.end_date
            )

        elif args.command == "export":
            export_data(
                format=args.format,
                output=args.output,
                start_date=args.start_date,
                end_date=args.end_date,
                model=args.model,
                category=args.category
            )

        elif args.command == "stats":
            show_stats(
                model=args.model,
                period=args.period
            )

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
