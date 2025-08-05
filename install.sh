#!/bin/bash

# Claude Code Custom Commands Installer
# This script helps install custom Claude Code commands for your projects

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
COMMANDS_DIR="$SCRIPT_DIR/.claude/commands"
AGENTS_DIR="$SCRIPT_DIR/.claude/agents"
HOOKS_DIR="$SCRIPT_DIR/.claude/hooks"

# Function to print colored output
print_info() {
    echo -e "${BLUE}ℹ${NC} $1"
}

print_success() {
    echo -e "${GREEN}✅${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}⚠${NC} $1"
}

print_error() {
    echo -e "${RED}❌${NC} $1"
}

# Function to check if Claude Code is installed
check_claude_code() {
    # Skip Claude Code check in CI environments
    if [ "${CI_TESTING:-}" = "true" ] || [ "${CI:-}" = "true" ]; then
        print_warning "Skipping Claude Code check in CI environment"
        return 0
    fi
    
    if ! command -v claude &> /dev/null; then
        print_error "Claude Code is not installed or not in PATH"
        echo "Please install Claude Code first: https://claude.ai/code"
        exit 1
    fi
    
    print_success "Claude Code is installed"
}

# Function to verify commands directory exists
check_commands_dir() {
    if [ ! -d "$COMMANDS_DIR" ]; then
        print_error "Commands directory not found: $COMMANDS_DIR"
        exit 1
    fi
    
    local command_count=$(find "$COMMANDS_DIR" -name "*.md" | wc -l)
    if [ "$command_count" -eq 0 ]; then
        print_error "No command files found in $COMMANDS_DIR"
        exit 1
    fi
    
    print_success "Found $command_count command files"
}

# Function to handle existing directory with smart merging
handle_existing_directory() {
    local dir=$1
    local component_name=$2
    
    if [ -d "$dir" ]; then
        local backup_dir="${dir}.backup.$(date +%Y%m%d_%H%M%S)"
        print_warning "Directory $dir already exists"
        echo "Options:"
        echo "  [M] Merge with existing files (recommended)"
        echo "  [B] Backup existing and install fresh"
        echo "  [C] Cancel installation"
        echo
        read -p "Choose action (M/b/c): " -n 1 -r
        echo
        
        case ${REPLY^^} in
            B)
                cp -r "$dir" "$backup_dir"
                print_success "Backed up existing $component_name to $backup_dir"
                rm -rf "$dir"
                mkdir -p "$dir"
                ;;
            C)
                print_error "Installation cancelled"
                exit 1
                ;;
            *)
                print_info "Merging with existing $component_name files..."
                # Directory will be merged during cp -r operation
                ;;
        esac
    else
        mkdir -p "$dir"
    fi
}

# Function to install commands only
install_commands_to_project() {
    local target_dir="./.claude"
    
    print_info "Installing commands to current project directory..."
    
    # Handle existing installation
    handle_existing_directory "$target_dir/commands" "commands"
    
    # Copy command files (preserving directory structure)
    cp -r "$COMMANDS_DIR"/* "$target_dir/commands/"
    
    print_success "Commands installed to $target_dir/commands"
    
    # Count and list installed commands
    local command_count=$(find "$target_dir/commands" -name "*.md" -not -path "*/README.md" | wc -l)
    print_info "Installed $command_count commands"
}

# Function to install agents only
install_agents_to_project() {
    local target_dir="./.claude"
    
    print_info "Installing agents to current project directory..."
    
    # Handle existing installation
    handle_existing_directory "$target_dir/agents" "agents"
    
    # Copy agent files (preserving directory structure)
    cp -r "$AGENTS_DIR"/* "$target_dir/agents/"
    
    print_success "Agents installed to $target_dir/agents"
    
    # Count installed agents
    local agent_count=$(find "$target_dir/agents" -name "*.md" -not -path "*/README.md" -not -path "*/ATTRIBUTION.md" -not -path "*/WORKFLOW_EXAMPLES.md" | wc -l)
    print_info "Installed $agent_count agents"
}

# Function to install hooks only
install_hooks_to_project() {
    local target_dir="./.claude"
    
    print_info "Installing hooks to current project directory..."
    
    # Handle existing installation
    handle_existing_directory "$target_dir/hooks" "hooks"
    
    # Copy hook files (preserving directory structure)
    cp -r "$HOOKS_DIR"/* "$target_dir/hooks/"
    
    print_success "Hooks installed to $target_dir/hooks"
    
    # Count hook configuration files
    local hook_count=$(find "$target_dir/hooks" -name "*.md" -not -path "*/README.md" -not -path "*/IMPLEMENTATION.md" | wc -l)
    print_info "Installed $hook_count hook configurations"
}

# Function to install to current project (backward compatibility)
install_to_project() {
    install_commands_to_project
    
    # List installed commands
    echo
    print_info "Installed commands:"
    find "./.claude/commands" -name "*.md" -not -path "*/README.md" | sed 's|.*/||' | sed 's/\.md$//' | sed 's/^/  \/project:/' | sort
    
    echo
    print_info "To use these commands, run 'claude code' in this directory and type /project:command-name"
}

# Function to install all components to project
install_all_to_project() {
    local target_dir="./.claude"
    
    print_info "Installing all components to current project directory..."
    
    # Install each component
    install_commands_to_project
    install_agents_to_project
    install_hooks_to_project
    
    # Summary
    echo
    print_success "All components installed to $target_dir"
    echo
    print_info "Installed:"
    echo "  • Commands: Use /project:command-name"
    echo "  • Agents: Available for delegation"
    echo "  • Hooks: Configure in ~/.claude/settings.json"
}

# Function to install commands globally
install_commands_globally() {
    local target_dir="$HOME/.claude/commands"
    
    print_info "Installing commands globally..."
    
    # Handle existing installation
    handle_existing_directory "$target_dir" "commands"
    
    # Copy command files (preserving directory structure)
    cp -r "$COMMANDS_DIR"/* "$target_dir/"
    
    print_success "Commands installed globally to $target_dir"
    
    # Count installed commands
    local command_count=$(find "$target_dir" -name "*.md" -not -path "*/README.md" | wc -l)
    print_info "Installed $command_count commands"
}

# Function to install agents globally
install_agents_globally() {
    local target_dir="$HOME/.claude/agents"
    
    print_info "Installing agents globally..."
    
    # Handle existing installation
    handle_existing_directory "$target_dir" "agents"
    
    # Copy agent files (preserving directory structure)
    cp -r "$AGENTS_DIR"/* "$target_dir/"
    
    print_success "Agents installed globally to $target_dir"
    
    # Count installed agents
    local agent_count=$(find "$target_dir" -name "*.md" -not -path "*/README.md" -not -path "*/ATTRIBUTION.md" -not -path "*/WORKFLOW_EXAMPLES.md" | wc -l)
    print_info "Installed $agent_count agents"
}

# Function to install hooks globally
install_hooks_globally() {
    local target_dir="$HOME/.claude/hooks"
    
    print_info "Installing hooks globally..."
    
    # Handle existing installation
    handle_existing_directory "$target_dir" "hooks"
    
    # Copy hook files (preserving directory structure)
    cp -r "$HOOKS_DIR"/* "$target_dir/"
    
    print_success "Hooks installed globally to $target_dir"
    
    # Count hook configurations
    local hook_count=$(find "$target_dir" -name "*.md" -not -path "*/README.md" -not -path "*/IMPLEMENTATION.md" | wc -l)
    print_info "Installed $hook_count hook configurations"
}

# Function to install globally (backward compatibility)
install_globally() {
    install_commands_globally
    
    # List installed commands
    echo
    print_info "Installed commands:"
    find "$HOME/.claude/commands" -name "*.md" -not -path "*/README.md" | sed 's|.*/||' | sed 's/\.md$//' | sed 's/^/  \/user:/' | sort
    
    echo
    print_info "These commands are now available as /user:command-name in all your projects"
}

# Function to install all components globally
install_all_globally() {
    print_info "Installing all components globally..."
    
    # Install each component
    install_commands_globally
    install_agents_globally
    install_hooks_globally
    
    # Summary
    echo
    print_success "All components installed globally"
    echo
    print_info "Installed:"
    echo "  • Commands: Use /user:command-name in all projects"
    echo "  • Agents: Available for delegation in all projects"
    echo "  • Hooks: Configure in ~/.claude/settings.json"
}

# Function to create symbolic link
install_symlink() {
    local target_dir="./.claude"
    
    print_info "Creating symbolic link to this repository..."
    
    if [ -e "$target_dir" ]; then
        print_warning "Target already exists: $target_dir"
        read -p "Remove it and create symlink? (y/N): " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            rm -rf "$target_dir"
        else
            print_info "Installation cancelled"
            return
        fi
    fi
    
    # Create symbolic link to the .claude directory
    ln -s "$SCRIPT_DIR/.claude" "$target_dir"
    
    print_success "Symbolic link created: $target_dir -> $SCRIPT_DIR/.claude"
    print_info "Commands will stay updated with this repository"
    
    # List available commands
    echo
    print_info "Available commands:"
    ls "$COMMANDS_DIR" | sed 's/\.md$//' | sed 's/^/  \/project:/'
}

# Function to list available commands
list_commands() {
    echo
    print_info "Available commands:"
    echo
    
    for file in "$COMMANDS_DIR"/*.md; do
        if [ -f "$file" ]; then
            local basename=$(basename "$file" .md)
            local description=$(head -n 5 "$file" | grep -v "^#" | head -n 1 | sed 's/^[[:space:]]*//')
            printf "  ${GREEN}/project:%-20s${NC} %s\n" "$basename" "$description"
        fi
    done
    
    echo
}

# Function to show help
show_help() {
    echo "Claude Code Custom Commands Installer"
    echo
    echo "Usage: $0 [OPTION]"
    echo
    echo "Options:"
    echo "  -p, --project     Install commands to current project"
    echo "  -g, --global      Install commands globally for all projects"
    echo "  -a, --all         Install all components (commands, agents, hooks)"
    echo "                    Can be combined with -p or -g"
    echo "  -s, --symlink     Create symbolic link (for development)"
    echo "  -l, --list        List available commands"
    echo "  -h, --help        Show this help message"
    echo
    echo "Examples:"
    echo "  $0 -p              Install commands to current project"
    echo "  $0 -g -a           Install all components globally"
    echo "  $0 -p -a           Install all components to current project"
    echo
    echo "Interactive mode (no options): Shows installation wizard"
}

# Function to show interactive component selection
show_component_wizard() {
    local scope=$1  # "project" or "global"
    
    echo
    echo "==================================="
    echo "Component Selection Wizard"
    echo "==================================="
    echo
    echo "Select components to install:"
    echo
    echo "[C] Commands (custom slash commands)"
    echo "[A] Agents (specialized AI agents)"
    echo "[H] Hooks (event-driven scripts)"
    echo "[X] All components"
    echo "[Q] Cancel"
    echo
    
    read -p "Enter your choices (e.g., 'CA' for Commands and Agents): " choices
    
    choices=$(echo "$choices" | tr '[:lower:]' '[:upper:]')
    
    local install_commands=false
    local install_agents=false
    local install_hooks=false
    
    if [[ "$choices" == *"Q"* ]]; then
        print_info "Installation cancelled"
        return 1
    fi
    
    if [[ "$choices" == *"X"* ]]; then
        install_commands=true
        install_agents=true
        install_hooks=true
    else
        [[ "$choices" == *"C"* ]] && install_commands=true
        [[ "$choices" == *"A"* ]] && install_agents=true
        [[ "$choices" == *"H"* ]] && install_hooks=true
    fi
    
    if ! $install_commands && ! $install_agents && ! $install_hooks; then
        print_warning "No components selected"
        return 1
    fi
    
    echo
    print_info "Installing selected components..."
    
    if [ "$scope" == "project" ]; then
        $install_commands && install_commands_to_project
        $install_agents && install_agents_to_project
        $install_hooks && install_hooks_to_project
    else
        $install_commands && install_commands_globally
        $install_agents && install_agents_globally
        $install_hooks && install_hooks_globally
    fi
    
    # Summary
    echo
    print_success "Installation complete!"
    echo
    print_info "Installed components:"
    $install_commands && echo "  • Commands: Use /$scope:command-name"
    $install_agents && echo "  • Agents: Available for delegation"
    $install_hooks && echo "  • Hooks: Configure in ~/.claude/settings.json"
    
    return 0
}

# Function to show interactive menu
show_menu() {
    echo
    echo "==================================="
    echo "Claude Code Custom Commands Installer"
    echo "==================================="
    echo
    echo "Choose installation method:"
    echo
    echo "1) Install to current project (commands only)"
    echo "   Creates ./.claude/commands/ in current directory"
    echo
    echo "2) Install to current project (select components)"
    echo "   Choose which components to install locally"
    echo
    echo "3) Install globally (commands only)"
    echo "   Available as /user:command-name in all projects"
    echo
    echo "4) Install globally (select components)"
    echo "   Choose which components to install globally"
    echo
    echo "5) Create symbolic link (for development)"
    echo "   Links to this repository, stays updated"
    echo
    echo "6) List available commands"
    echo
    echo "7) Exit"
    echo
}

# Main function
main() {
    # Check prerequisites
    check_claude_code
    check_commands_dir
    
    # Parse arguments
    local install_all=false
    local install_project=false
    local install_global=false
    
    while [[ $# -gt 0 ]]; do
        case "$1" in
            -p|--project)
                install_project=true
                shift
                ;;
            -g|--global)
                install_global=true
                shift
                ;;
            -a|--all)
                install_all=true
                shift
                ;;
            -s|--symlink)
                install_symlink
                exit 0
                ;;
            -l|--list)
                list_commands
                exit 0
                ;;
            -h|--help)
                show_help
                exit 0
                ;;
            *)
                print_error "Unknown option: $1"
                show_help
                exit 1
                ;;
        esac
    done
    
    # Handle combined flags
    if $install_project && $install_all; then
        install_all_to_project
        exit 0
    elif $install_global && $install_all; then
        install_all_globally
        exit 0
    elif $install_project; then
        install_to_project
        exit 0
    elif $install_global; then
        install_globally
        exit 0
    fi
    
    # Interactive mode
    while true; do
        show_menu
        read -p "Enter your choice (1-7): " choice
        
        case $choice in
            1)
                install_to_project
                break
                ;;
            2)
                show_component_wizard "project"
                break
                ;;
            3)
                install_globally
                break
                ;;
            4)
                show_component_wizard "global"
                break
                ;;
            5)
                install_symlink
                break
                ;;
            6)
                list_commands
                echo
                read -p "Press Enter to continue..."
                ;;
            7)
                print_info "Installation cancelled"
                exit 0
                ;;
            *)
                print_error "Invalid choice. Please enter 1-7."
                echo
                ;;
        esac
    done
}

# Run main function
main "$@"