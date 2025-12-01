"""
Scrapers package for collecting prompt engineering content.

Available scrapers:
- github_scraper: Scrapes GitHub repositories for prompt engineering content
"""

from pathlib import Path

# Package metadata
__version__ = "1.0.0"
__author__ = "Prompt Engineering System"

# Shared configuration
SCRAPERS_DIR = Path(__file__).parent
DATA_DIR = SCRAPERS_DIR.parent.parent / "data"
