#!/usr/bin/env python3
"""Verify GitHub scraper installation."""

import sys
from pathlib import Path

def verify():
    """Verify all components are installed."""
    print("GitHub Scraper Installation Verification")
    print("=" * 50)
    
    checks = []
    
    # Check main scraper
    try:
        from github_scraper import GitHubScraper, AWESOME_LISTS, DEFAULT_TOPICS
        checks.append(("✓", "github_scraper.py imports successfully"))
        checks.append(("✓", f"{len(AWESOME_LISTS)} awesome lists configured"))
        checks.append(("✓", f"{len(DEFAULT_TOPICS)} default topics configured"))
    except Exception as e:
        checks.append(("✗", f"Import failed: {e}"))
        
    # Check data directory
    data_dir = Path(__file__).parent.parent.parent / "data" / "github"
    if data_dir.exists():
        checks.append(("✓", f"Data directory exists: {data_dir}"))
    else:
        checks.append(("✗", f"Data directory missing: {data_dir}"))
        
    # Check documentation
    docs = [
        "GITHUB_README.md",
        "GITHUB_QUICKSTART.md", 
        "GITHUB_SCRAPER_SUMMARY.md",
        "example_usage.py"
    ]
    for doc in docs:
        if Path(doc).exists():
            checks.append(("✓", f"{doc} exists"))
        else:
            checks.append(("✗", f"{doc} missing"))
            
    # Print results
    print()
    for status, message in checks:
        print(f"{status} {message}")
        
    # Summary
    passed = sum(1 for s, _ in checks if s == "✓")
    total = len(checks)
    print()
    print("=" * 50)
    print(f"Verification: {passed}/{total} checks passed")
    
    if passed == total:
        print("✓ Installation complete and verified!")
        print()
        print("Quick start:")
        print("  python github_scraper.py --awesome")
        return 0
    else:
        print("✗ Some components missing")
        return 1

if __name__ == "__main__":
    sys.exit(verify())
