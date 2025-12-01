#!/usr/bin/env python3
"""
Full pipeline: Scrape Reddit/GitHub data and ingest into Qdrant.

This script orchestrates the complete workflow:
1. Scrape data from Reddit and/or GitHub
2. Save to JSON files
3. Ingest into Qdrant vector database

Usage:
    python scrape_and_ingest.py --reddit --timeframe week
    python scrape_and_ingest.py --github --min-stars 100
    python scrape_and_ingest.py --reddit --github --timeframe month
    python scrape_and_ingest.py --all --timeframe week --min-stars 50
"""

import argparse
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import List, Optional


SCRIPT_DIR = Path(__file__).parent
REDDIT_SCRAPER = SCRIPT_DIR / "reddit_scraper.py"
GITHUB_SCRAPER = SCRIPT_DIR / "github_scraper.py"
INGEST_SCRIPT = SCRIPT_DIR / "ingest_to_vector.py"


class ScraperPipeline:
    """Orchestrates the scraping and ingestion pipeline."""

    def __init__(
        self,
        scrape_reddit: bool = False,
        scrape_github: bool = False,
        reddit_timeframe: str = "week",
        reddit_limit: int = 50,
        github_min_stars: int = 50,
        github_limit: int = 30,
        reddit_subreddit: Optional[str] = None,
        github_topic: Optional[str] = None,
        github_search: Optional[str] = None,
        skip_comments: bool = False,
        skip_ingestion: bool = False,
        dry_run: bool = False,
        verbose: bool = False
    ):
        """
        Initialize the pipeline.

        Args:
            scrape_reddit: Whether to scrape Reddit
            scrape_github: Whether to scrape GitHub
            reddit_timeframe: Reddit timeframe (day/week/month/year/all)
            reddit_limit: Number of Reddit posts per subreddit
            github_min_stars: Minimum stars for GitHub repos
            github_limit: Number of GitHub repos to scrape
            reddit_subreddit: Specific subreddit to scrape (or all)
            github_topic: GitHub topic to search
            github_search: GitHub search query
            skip_comments: Skip fetching Reddit comments
            skip_ingestion: Only scrape, don't ingest
            dry_run: Dry run mode
            verbose: Verbose output
        """
        self.scrape_reddit = scrape_reddit
        self.scrape_github = scrape_github
        self.reddit_timeframe = reddit_timeframe
        self.reddit_limit = reddit_limit
        self.github_min_stars = github_min_stars
        self.github_limit = github_limit
        self.reddit_subreddit = reddit_subreddit
        self.github_topic = github_topic
        self.github_search = github_search
        self.skip_comments = skip_comments
        self.skip_ingestion = skip_ingestion
        self.dry_run = dry_run
        self.verbose = verbose

        # Track execution
        self.start_time = None
        self.scraped_files: List[Path] = []
        self.errors: List[str] = []

    def _run_command(self, cmd: List[str], description: str) -> bool:
        """
        Run a command and handle errors.

        Args:
            cmd: Command and arguments
            description: Human-readable description

        Returns:
            True if successful, False otherwise
        """
        print(f"\n{'=' * 70}")
        print(f"{description}")
        print(f"{'=' * 70}")

        if self.verbose:
            print(f"Command: {' '.join(cmd)}")

        try:
            if self.dry_run:
                print(f"[DRY RUN] Would execute: {' '.join(cmd)}")
                return True

            result = subprocess.run(
                cmd,
                check=True,
                capture_output=not self.verbose,
                text=True
            )

            if not self.verbose and result.stdout:
                print(result.stdout)

            print(f"\n✓ {description} completed successfully")
            return True

        except subprocess.CalledProcessError as e:
            error_msg = f"✗ {description} failed with exit code {e.returncode}"
            print(f"\n{error_msg}")

            if e.stderr:
                print(f"Error output:\n{e.stderr}")

            self.errors.append(error_msg)
            return False

        except FileNotFoundError:
            error_msg = f"✗ Script not found: {cmd[0]}"
            print(f"\n{error_msg}")
            self.errors.append(error_msg)
            return False

    def scrape_reddit_data(self) -> bool:
        """Scrape Reddit data."""
        cmd = [
            sys.executable,
            str(REDDIT_SCRAPER),
            '--timeframe', self.reddit_timeframe,
            '--limit', str(self.reddit_limit)
        ]

        if self.reddit_subreddit:
            cmd.extend(['--subreddit', self.reddit_subreddit])
        else:
            cmd.append('--all')

        if self.skip_comments:
            cmd.append('--no-comments')

        return self._run_command(cmd, "SCRAPING REDDIT")

    def scrape_github_data(self) -> bool:
        """Scrape GitHub data."""
        cmd = [sys.executable, str(GITHUB_SCRAPER)]

        # Add search parameters
        if self.github_search:
            cmd.extend(['--search', self.github_search])
        elif self.github_topic:
            cmd.extend(['--topic', self.github_topic])
        else:
            # Default to prompt-engineering topic
            cmd.extend(['--topic', 'prompt-engineering'])

        cmd.extend(['--min-stars', str(self.github_min_stars)])
        cmd.extend(['--limit', str(self.github_limit)])

        return self._run_command(cmd, "SCRAPING GITHUB")

    def ingest_data(self, source: str) -> bool:
        """
        Ingest scraped data into Qdrant.

        Args:
            source: Data source (reddit/github/all)

        Returns:
            True if successful, False otherwise
        """
        cmd = [sys.executable, str(INGEST_SCRIPT)]

        if source == 'all':
            cmd.append('--all')
        else:
            cmd.extend(['--source', source])

        if self.dry_run:
            cmd.append('--dry-run')

        return self._run_command(cmd, f"INGESTING {source.upper()} DATA")

    def run(self) -> bool:
        """
        Run the complete pipeline.

        Returns:
            True if successful, False otherwise
        """
        self.start_time = datetime.now()

        print("\n" + "=" * 70)
        print("SCRAPE AND INGEST PIPELINE")
        print("=" * 70)
        print(f"Start time: {self.start_time.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Scrape Reddit: {self.scrape_reddit}")
        print(f"Scrape GitHub: {self.scrape_github}")
        print(f"Skip ingestion: {self.skip_ingestion}")
        print(f"Dry run: {self.dry_run}")
        print("=" * 70)

        success = True

        # Step 1: Scrape Reddit
        if self.scrape_reddit:
            if not self.scrape_reddit_data():
                success = False
                print("\nWARNING: Reddit scraping failed, continuing with pipeline...")

        # Step 2: Scrape GitHub
        if self.scrape_github:
            if not self.scrape_github_data():
                success = False
                print("\nWARNING: GitHub scraping failed, continuing with pipeline...")

        # Step 3: Ingest data
        if not self.skip_ingestion:
            # Wait a moment for files to be written
            if not self.dry_run:
                time.sleep(2)

            # Ingest based on what was scraped
            if self.scrape_reddit and self.scrape_github:
                # Ingest both
                if not self.ingest_data('all'):
                    success = False
            elif self.scrape_reddit:
                # Ingest only Reddit
                if not self.ingest_data('reddit'):
                    success = False
            elif self.scrape_github:
                # Ingest only GitHub
                if not self.ingest_data('github'):
                    success = False

        # Print summary
        self._print_summary()

        return success

    def _print_summary(self):
        """Print pipeline execution summary."""
        end_time = datetime.now()
        duration = end_time - self.start_time

        print("\n" + "=" * 70)
        print("PIPELINE SUMMARY")
        print("=" * 70)
        print(f"Start time:  {self.start_time.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"End time:    {end_time.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Duration:    {duration}")
        print()

        if self.errors:
            print(f"Errors encountered: {len(self.errors)}")
            for i, error in enumerate(self.errors, 1):
                print(f"  {i}. {error}")
            print("\nPipeline completed with errors.")
        else:
            print("Pipeline completed successfully!")

        print("=" * 70)


def main():
    """Main CLI interface."""
    parser = argparse.ArgumentParser(
        description="Full pipeline: Scrape and ingest Reddit/GitHub data",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Scrape and ingest Reddit data from the past week
  python scrape_and_ingest.py --reddit --timeframe week

  # Scrape and ingest GitHub repos with 100+ stars
  python scrape_and_ingest.py --github --min-stars 100

  # Scrape both Reddit and GitHub, then ingest
  python scrape_and_ingest.py --reddit --github --timeframe month

  # Scrape everything quickly (all sources, short timeframe)
  python scrape_and_ingest.py --all --timeframe day --reddit-limit 25

  # Scrape specific subreddit and GitHub topic
  python scrape_and_ingest.py --reddit --subreddit PromptEngineering --github --topic llm-prompts

  # Scrape only (skip ingestion)
  python scrape_and_ingest.py --reddit --github --skip-ingestion

  # Dry run to see what would happen
  python scrape_and_ingest.py --all --dry-run

Pipeline Steps:
  1. Scrape Reddit (if --reddit or --all)
  2. Scrape GitHub (if --github or --all)
  3. Ingest into Qdrant (unless --skip-ingestion)
        """
    )

    # Source selection
    parser.add_argument(
        '--reddit',
        action='store_true',
        help='Scrape Reddit data'
    )
    parser.add_argument(
        '--github',
        action='store_true',
        help='Scrape GitHub data'
    )
    parser.add_argument(
        '--all',
        action='store_true',
        help='Scrape both Reddit and GitHub'
    )

    # Reddit options
    reddit_group = parser.add_argument_group('Reddit options')
    reddit_group.add_argument(
        '--timeframe',
        choices=['hour', 'day', 'week', 'month', 'year', 'all'],
        default='week',
        help='Reddit timeframe (default: week)'
    )
    reddit_group.add_argument(
        '--reddit-limit',
        type=int,
        default=50,
        help='Number of Reddit posts per subreddit (default: 50)'
    )
    reddit_group.add_argument(
        '--subreddit',
        type=str,
        help='Specific subreddit to scrape (omit for all configured subreddits)'
    )
    reddit_group.add_argument(
        '--skip-comments',
        action='store_true',
        help='Skip fetching Reddit comments (faster)'
    )

    # GitHub options
    github_group = parser.add_argument_group('GitHub options')
    github_group.add_argument(
        '--min-stars',
        type=int,
        default=50,
        help='Minimum GitHub stars (default: 50)'
    )
    github_group.add_argument(
        '--github-limit',
        type=int,
        default=30,
        help='Number of GitHub repos to scrape (default: 30)'
    )
    github_group.add_argument(
        '--topic',
        type=str,
        help='GitHub topic to search (default: prompt-engineering)'
    )
    github_group.add_argument(
        '--search',
        type=str,
        help='GitHub search query (overrides --topic)'
    )

    # Pipeline options
    pipeline_group = parser.add_argument_group('Pipeline options')
    pipeline_group.add_argument(
        '--skip-ingestion',
        action='store_true',
        help='Only scrape, do not ingest into database'
    )
    pipeline_group.add_argument(
        '--dry-run',
        action='store_true',
        help='Dry run - show what would be done without executing'
    )
    pipeline_group.add_argument(
        '--verbose',
        action='store_true',
        help='Verbose output'
    )

    args = parser.parse_args()

    # Validate arguments
    if args.all:
        scrape_reddit = True
        scrape_github = True
    else:
        scrape_reddit = args.reddit
        scrape_github = args.github

    if not (scrape_reddit or scrape_github):
        parser.error("Must specify --reddit, --github, or --all")

    # Check if scripts exist
    if scrape_reddit and not REDDIT_SCRAPER.exists():
        print(f"ERROR: Reddit scraper not found: {REDDIT_SCRAPER}")
        sys.exit(1)

    if scrape_github and not GITHUB_SCRAPER.exists():
        print(f"ERROR: GitHub scraper not found: {GITHUB_SCRAPER}")
        sys.exit(1)

    if not args.skip_ingestion and not INGEST_SCRIPT.exists():
        print(f"ERROR: Ingestion script not found: {INGEST_SCRIPT}")
        sys.exit(1)

    # Create and run pipeline
    pipeline = ScraperPipeline(
        scrape_reddit=scrape_reddit,
        scrape_github=scrape_github,
        reddit_timeframe=args.timeframe,
        reddit_limit=args.reddit_limit,
        github_min_stars=args.min_stars,
        github_limit=args.github_limit,
        reddit_subreddit=args.subreddit,
        github_topic=args.topic,
        github_search=args.search,
        skip_comments=args.skip_comments,
        skip_ingestion=args.skip_ingestion,
        dry_run=args.dry_run,
        verbose=args.verbose
    )

    success = pipeline.run()

    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()
