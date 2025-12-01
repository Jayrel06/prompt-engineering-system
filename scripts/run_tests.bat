@echo off
REM Comprehensive Test Runner for Prompt Engineering System (Windows)
REM Runs all tests: unit tests, prompt quality tests, and integration tests

setlocal enabledelayedexpansion

REM Get script directory
set SCRIPT_DIR=%~dp0
set PROJECT_ROOT=%SCRIPT_DIR%..
set TESTS_DIR=%PROJECT_ROOT%\tests

REM Create results directory
if not exist "%TESTS_DIR%\results" mkdir "%TESTS_DIR%\results"

echo ========================================
echo Prompt Engineering System - Test Suite
echo ========================================
echo.

REM Parse command line arguments
set RUN_UNIT=true
set RUN_PROMPT=true
set RUN_EXTENDED=false
set VERBOSE=false

:parse_args
if "%1"=="" goto end_parse
if /i "%1"=="--unit-only" (
    set RUN_PROMPT=false
    shift
    goto parse_args
)
if /i "%1"=="--prompt-only" (
    set RUN_UNIT=false
    shift
    goto parse_args
)
if /i "%1"=="--extended" (
    set RUN_EXTENDED=true
    shift
    goto parse_args
)
if /i "%1"=="--verbose" (
    set VERBOSE=true
    shift
    goto parse_args
)
if /i "%1"=="-v" (
    set VERBOSE=true
    shift
    goto parse_args
)
if /i "%1"=="--help" goto show_help
if /i "%1"=="-h" goto show_help
echo Unknown option: %1
echo Use --help for usage information
exit /b 1

:show_help
echo Usage: %0 [OPTIONS]
echo.
echo Options:
echo   --unit-only     Run only unit tests (Python)
echo   --prompt-only   Run only prompt quality tests (promptfoo)
echo   --extended      Include extended test suite
echo   --verbose, -v   Verbose output
echo   --help, -h      Show this help message
echo.
echo Examples:
echo   %0                    # Run all standard tests
echo   %0 --unit-only        # Only Python unit tests
echo   %0 --extended         # Run all tests including extended suite
echo   %0 --verbose          # Run with detailed output
exit /b 0

:end_parse

REM Track overall success
set ALL_PASSED=true

REM ==========================================
REM 1. Python Unit Tests
REM ==========================================

if "%RUN_UNIT%"=="true" (
    echo [1/3] Running Python Unit Tests...
    echo.

    REM Check if pytest is installed
    where pytest >nul 2>&1
    if errorlevel 1 (
        echo Error: pytest not found. Install with: pip install pytest
        set ALL_PASSED=false
    ) else (
        cd /d "%TESTS_DIR%"

        set PYTEST_ARGS=-v
        if "%VERBOSE%"=="true" set PYTEST_ARGS=-v -s

        echo Testing context-loader.py...
        pytest test_context_loader.py !PYTEST_ARGS! --tb=short
        if errorlevel 1 (
            echo X Context loader tests failed
            set ALL_PASSED=false
        ) else (
            echo + Context loader tests passed
        )

        echo.

        echo Testing prompt structure and quality...
        pytest test_prompts.py !PYTEST_ARGS! --tb=short
        if errorlevel 1 (
            echo X Prompt quality tests failed
            set ALL_PASSED=false
        ) else (
            echo + Prompt quality tests passed
        )

        echo.
    )
)

REM ==========================================
REM 2. Promptfoo Quality Tests
REM ==========================================

if "%RUN_PROMPT%"=="true" (
    echo [2/3] Running Promptfoo Quality Tests...
    echo.

    cd /d "%PROJECT_ROOT%"

    REM Check if npx is available
    where npx >nul 2>&1
    if errorlevel 1 (
        echo Error: npx not found. Install Node.js first.
        set ALL_PASSED=false
    ) else (
        REM Check if promptfoo is installed
        npx promptfoo --version >nul 2>&1
        if errorlevel 1 (
            echo Installing promptfoo...
            call npm install -g promptfoo
        )

        echo Running prompt evaluations...

        set PROMPTFOO_ARGS=
        if not "%VERBOSE%"=="true" set PROMPTFOO_ARGS=--no-progress-bar

        REM Run base promptfoo tests
        npx promptfoo eval -c tests\promptfoo.yaml !PROMPTFOO_ARGS!
        if errorlevel 1 (
            echo X Base prompt tests failed
            set ALL_PASSED=false
        ) else (
            echo + Base prompt tests passed
        )

        echo.
    )
)

REM ==========================================
REM 3. Extended Test Suite (Optional)
REM ==========================================

if "%RUN_EXTENDED%"=="true" (
    echo [3/3] Running Extended Test Suite...
    echo.

    cd /d "%PROJECT_ROOT%"

    where npx >nul 2>&1
    if not errorlevel 1 (
        echo Running extended evaluations...

        npx promptfoo eval -c tests\promptfoo-extended.yaml
        if errorlevel 1 (
            echo X Extended tests failed
            set ALL_PASSED=false
        ) else (
            echo + Extended tests passed
        )
    ) else (
        echo Skipping extended tests (npx not available)
    )

    echo.
)

REM ==========================================
REM Summary
REM ==========================================

echo ========================================
echo Test Summary
echo ========================================
echo.

if "%ALL_PASSED%"=="true" (
    echo + All tests passed!
    echo.
    echo Test results saved to: %TESTS_DIR%\results\
    exit /b 0
) else (
    echo X Some tests failed
    echo.
    echo Check detailed results in: %TESTS_DIR%\results\
    exit /b 1
)
