#!/usr/bin/env python3
"""
Svelte validation hook for Claude Code.
Validates Svelte files after editing using sv check.
"""
import json
import sys
import subprocess
import os
import re
from pathlib import Path

def main():
    try:
        # Read input from stdin
        input_data = json.load(sys.stdin)
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON input: {e}", file=sys.stderr)
        sys.exit(1)

    # Extract relevant data
    tool_name = input_data.get("tool_name", "")
    tool_input = input_data.get("tool_input", {})
    file_path = tool_input.get("file_path", "")
    
    # Only process Svelte files and editing tools
    if tool_name not in ["Write", "Edit", "MultiEdit"]:
        sys.exit(0)
    
    if not file_path.endswith(".svelte"):
        sys.exit(0)
    
    # Change to project directory if available
    project_dir = os.environ.get("CLAUDE_PROJECT_DIR", os.getcwd())
    os.chdir(project_dir)
    
    # Check if file exists (for Edit operations)
    if not os.path.exists(file_path):
        # File doesn't exist yet (new file), skip validation
        sys.exit(0)
    
    # Run sv check on the file
    try:
        result = subprocess.run(
            ["npx", "sv", "check", "--file", file_path],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        if result.returncode != 0:
            # Parse errors from sv check output
            errors = []
            warnings = []
            
            for line in result.stdout.split('\n'):
                if 'Error:' in line:
                    errors.append(line.strip())
                elif 'Warning:' in line:
                    warnings.append(line.strip())
            
            # If we have errors, block the operation
            if errors:
                error_msg = f"Svelte validation failed for {os.path.basename(file_path)}:\n"
                for error in errors[:5]:  # Limit to first 5 errors
                    error_msg += f"  • {error}\n"
                if len(errors) > 5:
                    error_msg += f"  ... and {len(errors) - 5} more errors\n"
                
                print(error_msg, file=sys.stderr)
                sys.exit(2)  # Block with exit code 2
            
            # If only warnings, show them but don't block
            if warnings:
                warning_msg = f"Svelte warnings for {os.path.basename(file_path)}:\n"
                for warning in warnings[:3]:
                    warning_msg += f"  ⚠️  {warning}\n"
                print(warning_msg, file=sys.stderr)
                sys.exit(0)  # Don't block for warnings
        
        # Success - optionally return success message
        output = {
            "suppressOutput": True  # Don't show success message in transcript
        }
        print(json.dumps(output))
        sys.exit(0)
        
    except subprocess.TimeoutExpired:
        print("Error: Svelte validation timed out", file=sys.stderr)
        sys.exit(1)
    except FileNotFoundError:
        print("Error: sv (Svelte CLI) not found. Install with: npm install -g @sveltejs/cli", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error running sv check: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()