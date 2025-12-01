# Fish completion script for prompt CLI
# Install: Copy to ~/.config/fish/completions/prompt.fish

# Remove old completions
complete -c prompt -e

# Helper function to get project root
function __prompt_project_root
    if set -q PROMPT_PROJECT_ROOT
        echo $PROMPT_PROJECT_ROOT
    else
        # Try to detect from common locations
        set -l script_dir (dirname (status --current-filename))
        echo (dirname $script_dir)
    end
end

# Helper function to list frameworks
function __prompt_list_frameworks
    set -l project_root (__prompt_project_root)
    if test -d $project_root/frameworks
        find $project_root/frameworks -type f -name "*.md" -exec basename {} .md \; 2>/dev/null | sort -u
    end
end

# Helper function to list templates
function __prompt_list_templates
    set -l project_root (__prompt_project_root)
    if test -d $project_root/templates
        find $project_root/templates -type f -name "*.md" -exec basename {} .md \; 2>/dev/null | sort -u
    end
end

# Main commands
complete -c prompt -n "not __fish_seen_subcommand_from plan quick project framework handoff search capture copy preview reflect reflect-prompts analyze list-frameworks list-templates status version cost-init cost-report cost-stats cost-export help" -a "plan" -d "Start planning session with full context"
complete -c prompt -n "not __fish_seen_subcommand_from plan quick project framework handoff search capture copy preview reflect reflect-prompts analyze list-frameworks list-templates status version cost-init cost-report cost-stats cost-export help" -a "quick" -d "Quick question with minimal context"
complete -c prompt -n "not __fish_seen_subcommand_from plan quick project framework handoff search capture copy preview reflect reflect-prompts analyze list-frameworks list-templates status version cost-init cost-report cost-stats cost-export help" -a "project" -d "Load specific project context"
complete -c prompt -n "not __fish_seen_subcommand_from plan quick project framework handoff search capture copy preview reflect reflect-prompts analyze list-frameworks list-templates status version cost-init cost-report cost-stats cost-export help" -a "framework" -d "Use specific thinking framework"
complete -c prompt -n "not __fish_seen_subcommand_from plan quick project framework handoff search capture copy preview reflect reflect-prompts analyze list-frameworks list-templates status version cost-init cost-report cost-stats cost-export help" -a "handoff" -d "Generate Claude Code handoff prompt"
complete -c prompt -n "not __fish_seen_subcommand_from plan quick project framework handoff search capture copy preview reflect reflect-prompts analyze list-frameworks list-templates status version cost-init cost-report cost-stats cost-export help" -a "search" -d "Search knowledge base"
complete -c prompt -n "not __fish_seen_subcommand_from plan quick project framework handoff search capture copy preview reflect reflect-prompts analyze list-frameworks list-templates status version cost-init cost-report cost-stats cost-export help" -a "capture" -d "Capture output to knowledge base"
complete -c prompt -n "not __fish_seen_subcommand_from plan quick project framework handoff search capture copy preview reflect reflect-prompts analyze list-frameworks list-templates status version cost-init cost-report cost-stats cost-export help" -a "copy" -d "Execute command and copy to clipboard"
complete -c prompt -n "not __fish_seen_subcommand_from plan quick project framework handoff search capture copy preview reflect reflect-prompts analyze list-frameworks list-templates status version cost-init cost-report cost-stats cost-export help" -a "preview" -d "Show preview without copying"
complete -c prompt -n "not __fish_seen_subcommand_from plan quick project framework handoff search capture copy preview reflect reflect-prompts analyze list-frameworks list-templates status version cost-init cost-report cost-stats cost-export help" -a "reflect" -d "Generate weekly reflection report"
complete -c prompt -n "not __fish_seen_subcommand_from plan quick project framework handoff search capture copy preview reflect reflect-prompts analyze list-frameworks list-templates status version cost-init cost-report cost-stats cost-export help" -a "reflect-prompts" -d "Generate reflection prompts"
complete -c prompt -n "not __fish_seen_subcommand_from plan quick project framework handoff search capture copy preview reflect reflect-prompts analyze list-frameworks list-templates status version cost-init cost-report cost-stats cost-export help" -a "analyze" -d "Analyze patterns"
complete -c prompt -n "not __fish_seen_subcommand_from plan quick project framework handoff search capture copy preview reflect reflect-prompts analyze list-frameworks list-templates status version cost-init cost-report cost-stats cost-export help" -a "list-frameworks" -d "List available frameworks"
complete -c prompt -n "not __fish_seen_subcommand_from plan quick project framework handoff search capture copy preview reflect reflect-prompts analyze list-frameworks list-templates status version cost-init cost-report cost-stats cost-export help" -a "list-templates" -d "List available templates"
complete -c prompt -n "not __fish_seen_subcommand_from plan quick project framework handoff search capture copy preview reflect reflect-prompts analyze list-frameworks list-templates status version cost-init cost-report cost-stats cost-export help" -a "status" -d "Check system status"
complete -c prompt -n "not __fish_seen_subcommand_from plan quick project framework handoff search capture copy preview reflect reflect-prompts analyze list-frameworks list-templates status version cost-init cost-report cost-stats cost-export help" -a "version" -d "Version control operations"
complete -c prompt -n "not __fish_seen_subcommand_from plan quick project framework handoff search capture copy preview reflect reflect-prompts analyze list-frameworks list-templates status version cost-init cost-report cost-stats cost-export help" -a "cost-init" -d "Initialize cost tracking"
complete -c prompt -n "not __fish_seen_subcommand_from plan quick project framework handoff search capture copy preview reflect reflect-prompts analyze list-frameworks list-templates status version cost-init cost-report cost-stats cost-export help" -a "cost-report" -d "Show cost report"
complete -c prompt -n "not __fish_seen_subcommand_from plan quick project framework handoff search capture copy preview reflect reflect-prompts analyze list-frameworks list-templates status version cost-init cost-report cost-stats cost-export help" -a "cost-stats" -d "Show cost statistics"
complete -c prompt -n "not __fish_seen_subcommand_from plan quick project framework handoff search capture copy preview reflect reflect-prompts analyze list-frameworks list-templates status version cost-init cost-report cost-stats cost-export help" -a "cost-export" -d "Export cost data"
complete -c prompt -n "not __fish_seen_subcommand_from plan quick project framework handoff search capture copy preview reflect reflect-prompts analyze list-frameworks list-templates status version cost-init cost-report cost-stats cost-export help" -a "help" -d "Show help message"

# Version subcommands
complete -c prompt -n "__fish_seen_subcommand_from version; and not __fish_seen_subcommand_from save list diff rollback tag tags" -a "save" -d "Save new version"
complete -c prompt -n "__fish_seen_subcommand_from version; and not __fish_seen_subcommand_from save list diff rollback tag tags" -a "list" -d "List version history"
complete -c prompt -n "__fish_seen_subcommand_from version; and not __fish_seen_subcommand_from save list diff rollback tag tags" -a "diff" -d "Show diff between versions"
complete -c prompt -n "__fish_seen_subcommand_from version; and not __fish_seen_subcommand_from save list diff rollback tag tags" -a "rollback" -d "Rollback to version"
complete -c prompt -n "__fish_seen_subcommand_from version; and not __fish_seen_subcommand_from save list diff rollback tag tags" -a "tag" -d "Tag a version"
complete -c prompt -n "__fish_seen_subcommand_from version; and not __fish_seen_subcommand_from save list diff rollback tag tags" -a "tags" -d "List tags"

# Framework name completion
complete -c prompt -n "__fish_seen_subcommand_from framework" -a "(__prompt_list_frameworks)" -d "Framework"

# Copy/preview subcommands
complete -c prompt -n "__fish_seen_subcommand_from copy preview; and not __fish_seen_subcommand_from plan quick project framework handoff" -a "plan" -d "Plan command"
complete -c prompt -n "__fish_seen_subcommand_from copy preview; and not __fish_seen_subcommand_from plan quick project framework handoff" -a "quick" -d "Quick command"
complete -c prompt -n "__fish_seen_subcommand_from copy preview; and not __fish_seen_subcommand_from plan quick project framework handoff" -a "project" -d "Project command"
complete -c prompt -n "__fish_seen_subcommand_from copy preview; and not __fish_seen_subcommand_from plan quick project framework handoff" -a "framework" -d "Framework command"
complete -c prompt -n "__fish_seen_subcommand_from copy preview; and not __fish_seen_subcommand_from plan quick project framework handoff" -a "handoff" -d "Handoff command"

# Framework completion for copy/preview framework
complete -c prompt -n "__fish_seen_subcommand_from copy preview; and __fish_seen_subcommand_from framework" -a "(__prompt_list_frameworks)" -d "Framework"

# Global options
complete -c prompt -s m -l model -d "Override model selection" -a "opus sonnet haiku"
complete -c prompt -s v -l verbose -d "Show context assembly details"
complete -c prompt -s o -l output -d "Write output to file" -r
complete -c prompt -l track -d "Enable cost tracking"
complete -c prompt -l category -d "Category for cost tracking" -a "planning technical communication analysis"
complete -c prompt -l description -d "Description for cost tracking"
complete -c prompt -s h -l help -d "Show help message"

# Cost report options
complete -c prompt -n "__fish_seen_subcommand_from cost-report cost-stats cost-export" -l period -d "Report period" -a "daily weekly monthly"
complete -c prompt -n "__fish_seen_subcommand_from cost-report cost-stats cost-export" -l model -d "Filter by model"
complete -c prompt -n "__fish_seen_subcommand_from cost-report cost-stats cost-export" -l category -d "Filter by category" -a "planning technical communication analysis"
complete -c prompt -n "__fish_seen_subcommand_from cost-report cost-stats cost-export" -l start-date -d "Start date (YYYY-MM-DD)"
complete -c prompt -n "__fish_seen_subcommand_from cost-report cost-stats cost-export" -l end-date -d "End date (YYYY-MM-DD)"
complete -c prompt -n "__fish_seen_subcommand_from cost-export" -l format -d "Export format" -a "csv json"
complete -c prompt -n "__fish_seen_subcommand_from cost-export" -l output -d "Output file" -r
