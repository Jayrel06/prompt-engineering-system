#!/bin/bash
# Quick Reddit Scraper Launcher
# Usage: ./scrape.sh [preset]

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PYTHON="${PYTHON:-python3}"

if [ $# -eq 0 ]; then
    echo "Usage: scrape.sh [preset]"
    echo ""
    echo "Available presets:"
    echo "  daily      - Daily update from all subreddits"
    echo "  weekly     - Weekly update from all subreddits"
    echo "  monthly    - Monthly update from all subreddits"
    echo "  quick      - Quick scan without comments"
    echo "  claude     - Search for Claude content"
    echo "  chatgpt    - Search for ChatGPT content"
    echo "  techniques - Search for prompt techniques"
    echo ""
    echo "Or use reddit_scraper.py directly for custom options:"
    echo "  python reddit_scraper.py --help"
    exit 1
fi

echo "Running Reddit scraper with preset: $1"
echo ""

"$PYTHON" "$SCRIPT_DIR/quick_scrape.py" "$1"

echo ""
echo "Scraping complete!"
echo "Output saved to: $SCRIPT_DIR/../../data/reddit/"
