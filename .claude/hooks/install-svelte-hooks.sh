#!/bin/bash
# Svelte hooks installer for Claude Code

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}🚀 Svelte Hooks Installer for Claude Code${NC}"
echo "======================================"

# Check if we're in a project directory
if [[ ! -f "package.json" ]]; then
    echo -e "${RED}Error: No package.json found. Please run this from your Svelte project root.${NC}"
    exit 1
fi

# Check if it's a Svelte project
if ! grep -q "svelte" package.json; then
    echo -e "${YELLOW}Warning: This doesn't appear to be a Svelte project.${NC}"
    read -p "Continue anyway? (y/N) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# Get the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Create .claude directory if it doesn't exist
echo -e "${BLUE}Creating .claude directory structure...${NC}"
mkdir -p .claude/hooks/scripts

# Copy hook scripts
echo -e "${BLUE}Installing hook scripts...${NC}"
cp -r "$SCRIPT_DIR/scripts/"* .claude/hooks/scripts/
chmod +x .claude/hooks/scripts/*.{py,sh}

# Choose configuration
echo -e "\n${BLUE}Choose a configuration preset:${NC}"
echo "1) Minimal - Format and lint only"
echo "2) Comprehensive - All validations and checks"
echo "3) Team - Focus on collaboration and standards"
echo "4) Performance - Bundle size and performance monitoring"
echo "5) Storybook - Storybook integration"
echo "6) Custom - I'll configure manually"

read -p "Enter your choice (1-6): " choice

case $choice in
    1)
        config_file="settings-minimal.json"
        ;;
    2)
        config_file="settings-comprehensive.json"
        ;;
    3)
        config_file="settings-team.json"
        ;;
    4)
        config_file="settings-performance.json"
        ;;
    5)
        config_file="settings-storybook.json"
        ;;
    6)
        config_file=""
        ;;
    *)
        echo -e "${RED}Invalid choice. Using minimal configuration.${NC}"
        config_file="settings-minimal.json"
        ;;
esac

# Install chosen configuration
if [[ -n "$config_file" ]]; then
    echo -e "${BLUE}Installing $config_file configuration...${NC}"
    
    # Check if settings.json already exists
    if [[ -f ".claude/settings.json" ]]; then
        echo -e "${YELLOW}Warning: .claude/settings.json already exists.${NC}"
        read -p "Backup and replace? (y/N) " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            mv .claude/settings.json .claude/settings.json.backup
            echo -e "${GREEN}Backed up to .claude/settings.json.backup${NC}"
        else
            echo -e "${YELLOW}Skipping settings.json installation.${NC}"
            config_file=""
        fi
    fi
    
    if [[ -n "$config_file" ]]; then
        cp "$SCRIPT_DIR/examples/$config_file" .claude/settings.json
        echo -e "${GREEN}✓ Installed .claude/settings.json${NC}"
    fi
fi

# Check for required npm packages
echo -e "\n${BLUE}Checking dependencies...${NC}"

missing_deps=()

# Check for required tools
command -v npx >/dev/null 2>&1 || missing_deps+=("npx (install Node.js)")

# Check npm packages
npx sv --version >/dev/null 2>&1 || missing_deps+=("@sveltejs/cli")
npx prettier --version >/dev/null 2>&1 || missing_deps+=("prettier")
npx eslint --version >/dev/null 2>&1 || missing_deps+=("eslint")
npx tsc --version >/dev/null 2>&1 || missing_deps+=("typescript")

if [[ ${#missing_deps[@]} -gt 0 ]]; then
    echo -e "${YELLOW}Missing dependencies:${NC}"
    for dep in "${missing_deps[@]}"; do
        echo "  - $dep"
    done
    echo -e "\n${YELLOW}Install missing dependencies with:${NC}"
    echo "npm install -D @sveltejs/cli prettier eslint typescript"
fi

# Add .claude to .gitignore if needed
if [[ -f ".gitignore" ]] && ! grep -q "^\.claude/settings\.local\.json" .gitignore; then
    echo -e "\n${BLUE}Updating .gitignore...${NC}"
    echo -e "\n# Claude Code local settings\n.claude/settings.local.json" >> .gitignore
    echo -e "${GREEN}✓ Added .claude/settings.local.json to .gitignore${NC}"
fi

# Create example local settings
cat > .claude/settings.local.json <<EOF
{
  "// Note": "This file is for local overrides and should not be committed",
  "hooks": {}
}
EOF

# Summary
echo -e "\n${GREEN}✅ Installation complete!${NC}"
echo -e "\nInstalled files:"
echo "  - Hook scripts in .claude/hooks/scripts/"
if [[ -n "$config_file" ]]; then
    echo "  - Configuration in .claude/settings.json"
fi
echo "  - Local settings template in .claude/settings.local.json"

echo -e "\n${BLUE}Next steps:${NC}"
echo "1. Review the installed hooks in .claude/hooks/scripts/"
echo "2. Customize .claude/settings.json as needed"
echo "3. Test hooks with: claude --debug"
echo "4. Use /hooks command in Claude Code to manage hooks"

echo -e "\n${BLUE}Documentation:${NC}"
echo "  - Hook docs: .claude/hooks/README.md"
echo "  - Quick reference: .claude/hooks/svelte-hooks-quick-reference.md"

echo -e "\n${GREEN}Happy coding with Claude Code! 🚀${NC}"