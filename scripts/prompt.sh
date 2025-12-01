#!/bin/bash

# Prompt Engineering System CLI with Cost Tracking
# Usage: prompt <command> [options]

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Cost tracking variables
TRACK_COST=false
COST_CATEGORY=""
COST_MODEL=""
COST_DESCRIPTION=""

# Detect clipboard command
detect_clipboard_cmd() {
    if command -v pbcopy &> /dev/null; then
        echo "pbcopy"
    elif command -v xclip &> /dev/null; then
        echo "xclip -selection clipboard"
    elif command -v clip.exe &> /dev/null; then
        echo "clip.exe"
    elif command -v xsel &> /dev/null; then
        echo "xsel --clipboard --input"
    else
        echo ""
    fi
}

show_help() {
    cat << EOF
Prompt Engineering System CLI

Usage: prompt [options] <command> [args]

Commands:
    plan <description>      Start planning session with full context
    quick <question>        Quick question with minimal context
    project <name> <task>   Load specific project context
    framework <name>        Use specific thinking framework
    handoff <description>   Generate Claude Code handoff prompt
    search <query>          Search knowledge base
    capture <file>          Capture output to knowledge base
    copy <command> [args]   Execute command and copy output to clipboard
    preview <command> [args] Show preview of command output without copying
    reflect [days]          Generate weekly reflection report (default: 7 days)
    reflect-prompts         Generate reflection prompts
    analyze [days]          Analyze patterns (default: 7 days)
    list-frameworks         List available thinking frameworks
    list-templates          List available templates
    status                  Check system status

Version Control:
    version save <file> [message]           Save new version of file
    version list <file>                     List version history
    version diff <file> <v1> <v2>           Show diff between versions
    version rollback <file> <version>       Rollback to specific version
    version tag <file> <version> <tag>      Tag a version
    version tags <file>                     List tags for file
    cost-report [opts]      Show cost tracking report
    cost-stats [opts]       Show quick cost statistics
    cost-export [opts]      Export cost data
    cost-init               Initialize cost tracking database

Options:
    -m, --model <model>     Override model selection (opus/sonnet/haiku)
    -v, --verbose           Show context assembly details
    -o, --output <file>     Write assembled prompt to file
    --track                 Enable cost tracking for this request
    --category <category>   Category for cost tracking (planning/technical/communication/analysis)
    --description <desc>    Description for cost tracking entry
    -h, --help              Show this help

Cost Report Options:
    --period <period>       Report period: daily/weekly/monthly (default: monthly)
    --start-date <date>     Start date (YYYY-MM-DD)
    --end-date <date>       End date (YYYY-MM-DD)
    --format <format>       Export format: csv/json (default: csv)

Examples:
    prompt plan "Q1 strategy for CoreReceptionAI"
    prompt quick "Best way to structure Docker networks"
    prompt framework first-principles "Should I add Langfuse?"
    prompt handoff "Build lead scoring system in n8n"
    prompt copy plan "Q1 strategy"
    prompt preview quick "Best Docker practice"
    prompt reflect
    prompt reflect-prompts
    prompt analyze 14
    prompt --track --category planning plan "Build Q1 roadmap"
    prompt cost-report --period weekly
    prompt cost-stats --model claude-sonnet-3.5
    prompt cost-export --format csv --output usage.csv

EOF
}

list_frameworks() {
    echo -e "${GREEN}Available Thinking Frameworks:${NC}"
    echo ""
    echo "Planning:"
    ls -1 "$PROJECT_ROOT/frameworks/planning/" 2>/dev/null | sed 's/.md$//' | sed 's/^/  - /'
    echo ""
    echo "Analysis:"
    ls -1 "$PROJECT_ROOT/frameworks/analysis/" 2>/dev/null | sed 's/.md$//' | sed 's/^/  - /'
    echo ""
    echo "Decision:"
    ls -1 "$PROJECT_ROOT/frameworks/decision/" 2>/dev/null | sed 's/.md$//' | sed 's/^/  - /'
    echo ""
    echo "Technical:"
    ls -1 "$PROJECT_ROOT/frameworks/technical/" 2>/dev/null | sed 's/.md$//' | sed 's/^/  - /'
    echo ""
    echo "Communication:"
    ls -1 "$PROJECT_ROOT/frameworks/communication/" 2>/dev/null | sed 's/.md$//' | sed 's/^/  - /'
}
    echo ""
    echo "Meta:"
    ls -1 "$PROJECT_ROOT/frameworks/meta/" 2>/dev/null | sed 's/.md$//' | sed 's/^/  - /'

list_templates() {
    echo -e "${GREEN}Available Templates:${NC}"
    echo ""
    echo "Voice AI:"
    ls -1 "$PROJECT_ROOT/templates/voice-ai/" 2>/dev/null | sed 's/.md$//' | sed 's/^/  - /'
    echo ""
    echo "Development:"
    ls -1 "$PROJECT_ROOT/templates/development/" 2>/dev/null | sed 's/.md$//' | sed 's/^/  - /'
    echo ""
    echo "Outreach:"
    ls -1 "$PROJECT_ROOT/templates/outreach/" 2>/dev/null | sed 's/.md$//' | sed 's/^/  - /'
    echo ""
    echo "Client:"
    ls -1 "$PROJECT_ROOT/templates/client/" 2>/dev/null | sed 's/.md$//' | sed 's/^/  - /'
}

check_status() {
    echo -e "${GREEN}System Status:${NC}"
    echo ""

    # Check if Python is available
    if command -v python3 &> /dev/null; then
        echo -e "  Python3: ${GREEN}Available${NC}"
    else
        echo -e "  Python3: ${RED}Not found${NC}"
    fi

    # Check clipboard tool
    CLIPBOARD_CMD=$(detect_clipboard_cmd)
    if [ -n "$CLIPBOARD_CMD" ]; then
        echo -e "  Clipboard: ${GREEN}Available ($CLIPBOARD_CMD)${NC}"
    else
        echo -e "  Clipboard: ${YELLOW}Not available${NC}"
    fi

    # Check if LiteLLM is running
    if curl -s http://localhost:4000/health > /dev/null 2>&1; then
        echo -e "  LiteLLM: ${GREEN}Running${NC}"
    else
        echo -e "  LiteLLM: ${YELLOW}Not running${NC}"
    fi

    # Check if Qdrant is running
    if curl -s http://localhost:6333/ > /dev/null 2>&1; then
        echo -e "  Qdrant:  ${GREEN}Running${NC}"
    else
        echo -e "  Qdrant:  ${YELLOW}Not running${NC}"
    fi

    # Check cost tracking database
    if [ -f "$PROJECT_ROOT/data/usage.db" ]; then
        echo -e "  Cost DB: ${GREEN}Initialized${NC}"
    else
        echo -e "  Cost DB: ${YELLOW}Not initialized (run 'prompt cost-init')${NC}"
    fi

    # Count resources
    echo ""
    echo "Resources:"
    echo "  Frameworks: $(find "$PROJECT_ROOT/frameworks" -name "*.md" 2>/dev/null | wc -l)"
    echo "  Templates:  $(find "$PROJECT_ROOT/templates" -name "*.md" 2>/dev/null | wc -l)"
    echo "  Context:    $(find "$PROJECT_ROOT/context" -name "*.md" 2>/dev/null | wc -l)"
}


# Execute a command and optionally copy to clipboard
execute_and_copy() {
    local cmd="$1"
    shift
    local args=("$@")
    local should_copy="$SHOULD_COPY"

    # Create temp file for output
    local tmpfile=$(mktemp)

    # Execute the command and capture output
    case "$cmd" in
        plan)
            python3 "$SCRIPT_DIR/context-loader.py" --mode full --task "${args[*]}" > "$tmpfile"
            ;;
        quick)
            python3 "$SCRIPT_DIR/context-loader.py" --mode minimal --task "${args[*]}" > "$tmpfile"
            ;;
        project)
            project_name="${args[0]}"
            task="${args[@]:1}"
            python3 "$SCRIPT_DIR/context-loader.py" --mode project --project "$project_name" --task "$task" > "$tmpfile"
            ;;
        framework)
            framework_name="${args[0]}"
            task="${args[@]:1}"
            python3 "$SCRIPT_DIR/context-loader.py" --mode framework --framework "$framework_name" --task "$task" > "$tmpfile"
            ;;
        handoff)
            python3 "$SCRIPT_DIR/context-loader.py" --mode handoff --task "${args[*]}" > "$tmpfile"
            ;;
        *)
            echo -e "${RED}Cannot copy output from '$cmd' command${NC}" >&2
            rm "$tmpfile"
            return 1
            ;;
    esac

    local exit_code=$?

    if [ $exit_code -eq 0 ]; then
        if [ "$should_copy" = "true" ]; then
            # Copy to clipboard
            CLIPBOARD_CMD=$(detect_clipboard_cmd)
            if [ -n "$CLIPBOARD_CMD" ]; then
                cat "$tmpfile" | eval "$CLIPBOARD_CMD"
                echo -e "${GREEN}Output copied to clipboard!${NC}" >&2
                echo -e "${BLUE}Preview (first 10 lines):${NC}" >&2
                head -n 10 "$tmpfile" >&2
                local line_count=$(wc -l < "$tmpfile")
                if [ "$line_count" -gt 10 ]; then
                    echo -e "${BLUE}... ($((line_count - 10)) more lines)${NC}" >&2
                fi
            else
                echo -e "${RED}No clipboard tool found. Install pbcopy, xclip, or clip.exe${NC}" >&2
                echo -e "${YELLOW}Showing output instead:${NC}" >&2
                cat "$tmpfile"
            fi
        else
            # Just show preview
            cat "$tmpfile"
        fi
    fi

    rm "$tmpfile"
    return $exit_code
}

# Parse options first
COMMAND=""
COMMAND_ARGS=()
SHOULD_COPY=false

while [[ $# -gt 0 ]]; do
    case $1 in
        --track)
            TRACK_COST=true
            shift
            ;;
        --category)
            COST_CATEGORY="$2"
            shift 2
            ;;
        --description)
            COST_DESCRIPTION="$2"
            shift 2
            ;;
        -m|--model)
            COST_MODEL="$2"
            shift 2
            ;;
        -h|--help|help)
            show_help
            exit 0
            ;;
        *)
            if [ -z "$COMMAND" ]; then
                COMMAND="$1"
            else
                COMMAND_ARGS+=("$1")
            fi
            shift
            ;;
    esac
done

# If tracking is enabled, show notification
if [ "$TRACK_COST" = true ]; then
    echo -e "${BLUE}Cost tracking enabled${NC}" >&2
    [ -n "$COST_CATEGORY" ] && echo -e "${BLUE}Category: $COST_CATEGORY${NC}" >&2
fi

# Execute command

handle_version_command() {
    local subcommand="$1"
    shift

    case "$subcommand" in
        save)
            if [ -z "$1" ]; then
                echo -e "${RED}Error: File path required${NC}"
                echo "Usage: prompt version save <file> [message]"
                exit 1
            fi
            local file="$1"
            shift
            local message="$*"
            if [[ ! "$file" = /* ]]; then
                file="$PROJECT_ROOT/$file"
            fi
            if [ -n "$message" ]; then
                python3 "$SCRIPT_DIR/version_manager.py" save "$file" "$message"
            else
                python3 "$SCRIPT_DIR/version_manager.py" save "$file"
            fi
            ;;
        list)
            if [ -z "$1" ]; then
                echo -e "${RED}Error: File path required${NC}"
                echo "Usage: prompt version list <file>"
                exit 1
            fi
            local file="$1"
            if [[ ! "$file" = /* ]]; then
                file="$PROJECT_ROOT/$file"
            fi
            python3 "$SCRIPT_DIR/version_manager.py" list "$file"
            ;;
        diff)
            if [ -z "$1" ] || [ -z "$2" ] || [ -z "$3" ]; then
                echo -e "${RED}Error: File path and two versions required${NC}"
                echo "Usage: prompt version diff <file> <v1> <v2>"
                exit 1
            fi
            local file="$1"
            local v1="$2"
            local v2="$3"
            if [[ ! "$file" = /* ]]; then
                file="$PROJECT_ROOT/$file"
            fi
            python3 "$SCRIPT_DIR/version_manager.py" diff "$file" "$v1" "$v2"
            ;;
        rollback)
            if [ -z "$1" ] || [ -z "$2" ]; then
                echo -e "${RED}Error: File path and version required${NC}"
                echo "Usage: prompt version rollback <file> <version>"
                exit 1
            fi
            local file="$1"
            local version="$2"
            if [[ ! "$file" = /* ]]; then
                file="$PROJECT_ROOT/$file"
            fi
            python3 "$SCRIPT_DIR/version_manager.py" rollback "$file" "$version"
            ;;
        tag)
            if [ -z "$1" ] || [ -z "$2" ] || [ -z "$3" ]; then
                echo -e "${RED}Error: File path, version, and tag name required${NC}"
                echo "Usage: prompt version tag <file> <version> <tag>"
                exit 1
            fi
            local file="$1"
            local version="$2"
            local tag="$3"
            if [[ ! "$file" = /* ]]; then
                file="$PROJECT_ROOT/$file"
            fi
            python3 "$SCRIPT_DIR/version_manager.py" tag "$file" "$version" "$tag"
            ;;
        tags)
            if [ -z "$1" ]; then
                echo -e "${RED}Error: File path required${NC}"
                echo "Usage: prompt version tags <file>"
                exit 1
            fi
            local file="$1"
            if [[ ! "$file" = /* ]]; then
                file="$PROJECT_ROOT/$file"
            fi
            python3 "$SCRIPT_DIR/version_manager.py" tags "$file"
            ;;
        *)
            echo -e "${RED}Unknown version subcommand: $subcommand${NC}"
            echo ""
            echo "Available version commands:"
            echo "  save <file> [message]       - Save new version"
            echo "  list <file>                 - List version history"
            echo "  diff <file> <v1> <v2>       - Show diff between versions"
            echo "  rollback <file> <version>   - Rollback to version"
            echo "  tag <file> <version> <tag>  - Tag a version"
            echo "  tags <file>                 - List tags for file"
            exit 1
            ;;
    esac
}

case "$COMMAND" in
    copy)
        SHOULD_COPY=true
        subcmd="${COMMAND_ARGS[0]}"
        execute_and_copy "$subcmd" "${COMMAND_ARGS[@]:1}"
        ;;
    preview)
        SHOULD_COPY=false
        subcmd="${COMMAND_ARGS[0]}"
        execute_and_copy "$subcmd" "${COMMAND_ARGS[@]:1}"
        ;;
    plan)
        python3 "$SCRIPT_DIR/context-loader.py" --mode full --task "${COMMAND_ARGS[*]}"
        ;;
    quick)
        python3 "$SCRIPT_DIR/context-loader.py" --mode minimal --task "${COMMAND_ARGS[*]}"
        ;;
    project)
        project_name="${COMMAND_ARGS[0]}"
        task="${COMMAND_ARGS[@]:1}"
        python3 "$SCRIPT_DIR/context-loader.py" --mode project --project "$project_name" --task "$task"
        ;;
    framework)
        framework_name="${COMMAND_ARGS[0]}"
        task="${COMMAND_ARGS[@]:1}"
        python3 "$SCRIPT_DIR/context-loader.py" --mode framework --framework "$framework_name" --task "$task"
        ;;
    handoff)
        python3 "$SCRIPT_DIR/context-loader.py" --mode handoff --task "${COMMAND_ARGS[*]}"
        ;;
    search)
        echo -e "${YELLOW}Search not yet implemented. Use grep for now:${NC}"
        echo "grep -r '${COMMAND_ARGS[*]}' $PROJECT_ROOT/context/"
        ;;
    capture)
        echo -e "${YELLOW}Capture not yet implemented.${NC}"
        ;;
    reflect)
        days="${COMMAND_ARGS[0]:-7}"
        output_file="$PROJECT_ROOT/context/learnings/reflection-$(date +%Y-%m-%d).md"
        echo -e "${GREEN}Generating weekly reflection report for last $days days...${NC}"
        python3 "$SCRIPT_DIR/reflection.py" --report --days "$days" --output "$output_file"
        if [ $? -eq 0 ]; then
            echo -e "${GREEN}Report saved to: $output_file${NC}"
            echo ""
            echo "Next steps:"
            echo "  1. Review the report"
            echo "  2. Update context/learnings/what-works.md"
            echo "  3. Update context/learnings/what-doesnt.md"
            echo "  4. Copy insights to context/learnings/reflection-log.md"
        fi
        ;;
    reflect-prompts)
        echo -e "${GREEN}Generating reflection prompts...${NC}"
        python3 "$SCRIPT_DIR/reflection.py" --prompts
        ;;
    analyze)
        days="${COMMAND_ARGS[0]:-7}"
        echo -e "${GREEN}Analyzing patterns from last $days days...${NC}"
        python3 "$SCRIPT_DIR/reflection.py" --analyze --days "$days"
        ;;
    list-frameworks)
        list_frameworks
        ;;
    list-templates)
        list_templates
        ;;
    status)
        check_status
        ;;
    version)
        handle_version_command "${COMMAND_ARGS[@]}"
        ;;
    cost-init)
        python3 "$SCRIPT_DIR/cost_tracker.py" init
        ;;
    cost-report)
        # Parse cost report options
        report_args=""
        i=0
        while [ $i -lt ${#COMMAND_ARGS[@]} ]; do
            arg="${COMMAND_ARGS[$i]}"
            case $arg in
                --period|--model|--category|--start-date|--end-date)
                    report_args="$report_args $arg ${COMMAND_ARGS[$((i+1))]}"
                    i=$((i+2))
                    ;;
                *)
                    i=$((i+1))
                    ;;
            esac
        done
        python3 "$SCRIPT_DIR/cost_tracker.py" report $report_args
        ;;
    cost-stats)
        # Parse cost stats options
        stats_args=""
        i=0
        while [ $i -lt ${#COMMAND_ARGS[@]} ]; do
            arg="${COMMAND_ARGS[$i]}"
            case $arg in
                --period|--model)
                    stats_args="$stats_args $arg ${COMMAND_ARGS[$((i+1))]}"
                    i=$((i+2))
                    ;;
                *)
                    i=$((i+1))
                    ;;
            esac
        done
        python3 "$SCRIPT_DIR/cost_tracker.py" stats $stats_args
        ;;
    cost-export)
        # Parse export options
        export_args=""
        i=0
        while [ $i -lt ${#COMMAND_ARGS[@]} ]; do
            arg="${COMMAND_ARGS[$i]}"
            case $arg in
                --format|--output|--start-date|--end-date|--model|--category)
                    export_args="$export_args $arg ${COMMAND_ARGS[$((i+1))]}"
                    i=$((i+2))
                    ;;
                *)
                    i=$((i+1))
                    ;;
            esac
        done
        python3 "$SCRIPT_DIR/cost_tracker.py" export $export_args
        ;;
    "")
        show_help
        ;;
    *)
        echo -e "${RED}Unknown command: $COMMAND${NC}"
        echo ""
        show_help
        exit 1
        ;;
esac
