#compdef prompt
# Zsh completion script for prompt CLI
# Install: Copy to a directory in your $fpath or add to ~/.zshrc

_prompt() {
    local -a commands version_cmds cost_options main_options
    local project_root

    # Define commands
    commands=(
        'plan:Start planning session with full context'
        'quick:Quick question with minimal context'
        'project:Load specific project context'
        'framework:Use specific thinking framework'
        'handoff:Generate Claude Code handoff prompt'
        'search:Search knowledge base'
        'capture:Capture output to knowledge base'
        'copy:Execute command and copy to clipboard'
        'preview:Show preview without copying'
        'reflect:Generate weekly reflection report'
        'reflect-prompts:Generate reflection prompts'
        'analyze:Analyze patterns'
        'list-frameworks:List available thinking frameworks'
        'list-templates:List available templates'
        'status:Check system status'
        'version:Version control operations'
        'cost-init:Initialize cost tracking database'
        'cost-report:Show cost tracking report'
        'cost-stats:Show cost statistics'
        'cost-export:Export cost data'
        'help:Show help message'
    )

    version_cmds=(
        'save:Save new version of file'
        'list:List version history'
        'diff:Show diff between versions'
        'rollback:Rollback to specific version'
        'tag:Tag a version'
        'tags:List tags for file'
    )

    cost_options=(
        '--period:Report period (daily/weekly/monthly)'
        '--model:Filter by model'
        '--category:Filter by category'
        '--start-date:Start date (YYYY-MM-DD)'
        '--end-date:End date (YYYY-MM-DD)'
        '--format:Export format (csv/json)'
        '--output:Output file path'
    )

    main_options=(
        '-m[Override model selection]:model:(opus sonnet haiku)'
        '--model[Override model selection]:model:(opus sonnet haiku)'
        '-v[Show context assembly details]'
        '--verbose[Show context assembly details]'
        '-o[Write assembled prompt to file]:file:_files'
        '--output[Write assembled prompt to file]:file:_files'
        '--track[Enable cost tracking]'
        '--category[Category for cost tracking]:category:(planning technical communication analysis)'
        '--description[Description for cost tracking]:description:'
        '-h[Show help]'
        '--help[Show help]'
    )

    # Find project root
    if [[ -n "$PROMPT_PROJECT_ROOT" ]]; then
        project_root="$PROMPT_PROJECT_ROOT"
    else
        # Try to find it relative to the script
        local script_dir="${0:A:h}"
        project_root="${script_dir:h}"
    fi

    _arguments -C \
        '1: :->command' \
        '*:: :->args' \
        && return 0

    case $state in
        command)
            _describe -t commands 'prompt commands' commands
            ;;
        args)
            case $words[1] in
                version)
                    case $CURRENT in
                        2)
                            _describe -t version-commands 'version commands' version_cmds
                            ;;
                        3)
                            _files
                            ;;
                        *)
                            _files
                            ;;
                    esac
                    ;;
                framework)
                    case $CURRENT in
                        2)
                            # Complete framework names
                            local -a frameworks
                            if [[ -d "$project_root/frameworks" ]]; then
                                frameworks=(${(f)"$(find "$project_root/frameworks" -type f -name "*.md" -exec basename {} .md \; 2>/dev/null | sort -u)"})
                                _describe -t frameworks 'frameworks' frameworks
                            fi
                            ;;
                    esac
                    ;;
                copy|preview)
                    case $CURRENT in
                        2)
                            local -a copy_cmds
                            copy_cmds=(
                                'plan:Start planning session'
                                'quick:Quick question'
                                'project:Load project context'
                                'framework:Use thinking framework'
                                'handoff:Generate handoff prompt'
                            )
                            _describe -t copy-commands 'commands' copy_cmds
                            ;;
                        3)
                            if [[ $words[2] == "framework" ]]; then
                                local -a frameworks
                                if [[ -d "$project_root/frameworks" ]]; then
                                    frameworks=(${(f)"$(find "$project_root/frameworks" -type f -name "*.md" -exec basename {} .md \; 2>/dev/null | sort -u)"})
                                    _describe -t frameworks 'frameworks' frameworks
                                fi
                            fi
                            ;;
                    esac
                    ;;
                cost-report|cost-stats|cost-export)
                    _arguments \
                        '--period[Report period]:period:(daily weekly monthly)' \
                        '--model[Filter by model]:model:' \
                        '--category[Filter by category]:category:(planning technical communication analysis)' \
                        '--start-date[Start date]:date:' \
                        '--end-date[End date]:date:' \
                        '--format[Export format]:format:(csv json)' \
                        '--output[Output file]:file:_files'
                    ;;
            esac
            ;;
    esac
}

_prompt "$@"
