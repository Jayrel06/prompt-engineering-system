@echo off
REM Quick Reddit Scraper Launcher for Windows
REM Usage: scrape.bat [preset]

setlocal

set SCRIPT_DIR=%~dp0
set PYTHON=python

if "%1"=="" (
    echo Usage: scrape.bat [preset]
    echo.
    echo Available presets:
    echo   daily      - Daily update from all subreddits
    echo   weekly     - Weekly update from all subreddits
    echo   monthly    - Monthly update from all subreddits
    echo   quick      - Quick scan without comments
    echo   claude     - Search for Claude content
    echo   chatgpt    - Search for ChatGPT content
    echo   techniques - Search for prompt techniques
    echo.
    echo Or use reddit_scraper.py directly for custom options:
    echo   python reddit_scraper.py --help
    exit /b 1
)

echo Running Reddit scraper with preset: %1
echo.

%PYTHON% "%SCRIPT_DIR%quick_scrape.py" %1

if errorlevel 1 (
    echo.
    echo Error: Scraper failed
    exit /b 1
)

echo.
echo Scraping complete!
echo Output saved to: %SCRIPT_DIR%..\..\data\reddit\
