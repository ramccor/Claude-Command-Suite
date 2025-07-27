#!/usr/bin/env python3
"""
Bash command validator for Claude Code.
Validates bash commands before execution to encourage best practices.
"""
import json
import re
import sys

# Define validation rules as (pattern, message) tuples
VALIDATION_RULES = [
    # Performance rules
    (
        r"\bgrep\b(?!.*\|)",
        "Use 'rg' (ripgrep) instead of 'grep' for better performance"
    ),
    (
        r"\bfind\s+.*-name\b",
        "Use 'rg --files -g pattern' instead of 'find -name' for better performance"
    ),
    (
        r"\bcat\s+.*\|\s*grep\b",
        "Use 'rg pattern file' instead of 'cat file | grep pattern'"
    ),
    
    # Security rules
    (
        r"rm\s+-rf\s+/(?!\s|$)",
        "Dangerous rm -rf command detected. Double-check the path!"
    ),
    (
        r"curl.*\|\s*bash",
        "Piping curl to bash is dangerous. Download and review scripts first"
    ),
    (
        r"chmod\s+777",
        "chmod 777 is insecure. Use more restrictive permissions"
    ),
    
    # Best practices
    (
        r"\$\w+(?![\"'}])",
        "Unquoted variable detected. Use \"$VAR\" to prevent word splitting"
    ),
    (
        r"cd\s+&&\s+",
        "Use absolute paths or subshells instead of 'cd &&' patterns"
    ),
]

# Commands that should prompt for confirmation
DANGEROUS_COMMANDS = [
    "rm -rf",
    "git reset --hard",
    "git clean -fd",
    "npm install -g",
    "sudo",
]

def validate_command(command):
    """Validate a bash command and return issues."""
    issues = []
    warnings = []
    
    # Check validation rules
    for pattern, message in VALIDATION_RULES:
        if re.search(pattern, command):
            # Security issues are errors, others are warnings
            if any(word in message.lower() for word in ["dangerous", "insecure", "security"]):
                issues.append(message)
            else:
                warnings.append(message)
    
    # Check for dangerous commands
    for dangerous in DANGEROUS_COMMANDS:
        if dangerous in command:
            issues.append(f"Potentially dangerous command: {dangerous}")
    
    return issues, warnings

def main():
    try:
        # Read input from stdin
        input_data = json.load(sys.stdin)
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON input: {e}", file=sys.stderr)
        sys.exit(1)

    tool_name = input_data.get("tool_name", "")
    tool_input = input_data.get("tool_input", {})
    command = tool_input.get("command", "")

    if tool_name != "Bash" or not command:
        sys.exit(0)

    # Validate the command
    issues, warnings = validate_command(command)

    # If there are security issues, block with exit code 2
    if issues:
        print("❌ Security/safety issues detected:\n", file=sys.stderr)
        for issue in issues:
            print(f"  • {issue}", file=sys.stderr)
        
        # Ask user for confirmation instead of blocking
        output = {
            "hookSpecificOutput": {
                "hookEventName": "PreToolUse",
                "permissionDecision": "ask",
                "permissionDecisionReason": f"Command has potential issues:\n" + "\n".join(f"• {issue}" for issue in issues)
            }
        }
        print(json.dumps(output))
        sys.exit(0)
    
    # If there are warnings, show them but don't block
    if warnings:
        print("💡 Suggestions for better practices:\n", file=sys.stderr)
        for warning in warnings:
            print(f"  • {warning}", file=sys.stderr)
    
    # Allow the command
    output = {
        "suppressOutput": True
    }
    print(json.dumps(output))
    sys.exit(0)

if __name__ == "__main__":
    main()