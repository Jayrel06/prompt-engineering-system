#!/usr/bin/env bash
# Bash completion script for prompt CLI
# Install: Source this file in your .bashrc or copy to /etc/bash_completion.d/

_prompt_completion() {
    local cur prev words cword
    _init_completion || return

    # Define all available commands
    local commands="plan quick project framework handoff search capture copy preview reflect reflect-prompts analyze list-frameworks list-templates status version cost-init cost-report cost-stats cost-export help"

    # Define version subcommands
    local version_subcommands="save list diff rollback tag tags"

    # Define cost report options
    local cost_options="--period --model --category --start-date --end-date --format --output"

    # Define main options
    local main_options="-m --model -v --verbose -o --output --track --category --description -h --help"

    # Get the script directory to find frameworks and templates
    local script_dir="${BASH_SOURCE[0]%/*}"
    local project_root="${script_dir%/*}"

    # If project_root is not valid, try to find it
    if [ ! -d "$project_root/frameworks" ]; then
        # Try to find the project root from common locations
        if [ -n "$PROMPT_PROJECT_ROOT" ]; then
            project_root="$PROMPT_PROJECT_ROOT"
        fi
    fi

    case $cword in
        1)
            # First argument: complete main commands
            COMPREPLY=( $(compgen -W "$commands" -- "$cur") )
            ;;
        2)
            # Second argument: depends on the command
            case ${words[1]} in
                version)
                    COMPREPLY=( $(compgen -W "$version_subcommands" -- "$cur") )
                    ;;
                framework)
                    # Complete framework names from all framework directories
                    local frameworks=""
                    if [ -d "$project_root/frameworks" ]; then
                        frameworks=$(find "$project_root/frameworks" -type f -name "*.md" -exec basename {} .md \; 2>/dev/null | sort -u)
                    fi
                    COMPREPLY=( $(compgen -W "$frameworks" -- "$cur") )
                    ;;
                copy|preview)
                    # Complete with subset of commands that support copy/preview
                    local copy_commands="plan quick project framework handoff"
                    COMPREPLY=( $(compgen -W "$copy_commands" -- "$cur") )
                    ;;
                cost-report|cost-stats|cost-export)
                    # Complete cost options
                    COMPREPLY=( $(compgen -W "$cost_options" -- "$cur") )
                    ;;
                *)
                    # For other commands, don't complete
                    COMPREPLY=()
                    ;;
            esac
            ;;
        3)
            # Third argument
            case ${words[1]} in
                version)
                    # For version commands, complete file paths
                    case ${words[2]} in
                        save|list|diff|rollback|tag|tags)
                            _filedir
                            ;;
                    esac
                    ;;
                framework)
                    # After framework name, no completion (free text for task)
                    COMPREPLY=()
                    ;;
                copy|preview)
                    # Complete framework names if the subcommand is 'framework'
                    if [ "${words[2]}" = "framework" ]; then
                        local frameworks=""
                        if [ -d "$project_root/frameworks" ]; then
                            frameworks=$(find "$project_root/frameworks" -type f -name "*.md" -exec basename {} .md \; 2>/dev/null | sort -u)
                        fi
                        COMPREPLY=( $(compgen -W "$frameworks" -- "$cur") )
                    else
                        COMPREPLY=()
                    fi
                    ;;
                *)
                    # Check if current word starts with --
                    if [[ "$cur" == --* ]]; then
                        case ${words[1]} in
                            cost-report|cost-stats|cost-export)
                                COMPREPLY=( $(compgen -W "$cost_options" -- "$cur") )
                                ;;
                        esac
                    fi
                    ;;
            esac
            ;;
        *)
            # For remaining arguments
            case ${words[1]} in
                version)
                    # File path completion for version commands
                    _filedir
                    ;;
                *)
                    # Check if current word starts with --
                    if [[ "$cur" == --* ]]; then
                        case ${words[1]} in
                            cost-report|cost-stats|cost-export)
                                COMPREPLY=( $(compgen -W "$cost_options" -- "$cur") )
                                ;;
                            *)
                                COMPREPLY=( $(compgen -W "$main_options" -- "$cur") )
                                ;;
                        esac
                    elif [[ "$cur" == -* ]]; then
                        COMPREPLY=( $(compgen -W "$main_options" -- "$cur") )
                    fi
                    ;;
            esac
            ;;
    esac
}

complete -F _prompt_completion prompt
