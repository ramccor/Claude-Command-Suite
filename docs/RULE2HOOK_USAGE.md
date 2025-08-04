# Rule2Hook Command Usage Guide

This command is integrated from the excellent [claudecode-rule2hook](https://github.com/zxdxjtu/claudecode-rule2hook) repository created by [zxdxjtu](https://github.com/zxdxjtu). We've incorporated it into the Claude Command Suite to make it easily accessible for all users, maintaining full compatibility with the original implementation while respecting the MIT License.

The `rule2hook` command helps you convert natural language project rules into Claude Code hooks automatically.

## Installation
The command is already included in the Claude Command Suite under the `dev` namespace.

## Usage

### Basic Usage
```bash
# Convert a specific rule
/dev:rule2hook "Format Python files with black after editing"

# Analyze existing CLAUDE.md files for rules
/dev:rule2hook
```

### Examples

1. **Code Formatting Rule**
   ```bash
   /dev:rule2hook "Run prettier on JavaScript files after editing"
   ```
   Generates a PostToolUse hook for Edit|MultiEdit|Write tools

2. **Security Check**
   ```bash
   /dev:rule2hook "Check for hardcoded secrets before saving files"
   ```
   Generates a PreToolUse hook for Write|Edit|MultiEdit tools

3. **Git Workflow**
   ```bash
   /dev:rule2hook "Show git status when finishing tasks"
   ```
   Generates a Stop hook

4. **Testing Rule**
   ```bash
   /dev:rule2hook "Run tests after modifying test files"
   ```
   Generates a PostToolUse hook

## Output
The command will:
1. Analyze your rule
2. Generate the appropriate hook configuration
3. Save it to `~/.claude/hooks.json`
4. Show you what was configured

## Verification
Check your configured hooks:
```bash
cat ~/.claude/hooks.json
```

## Attribution
This command was created by [zxdxjtu](https://github.com/zxdxjtu/claudecode-rule2hook) and integrated into Claude Command Suite.