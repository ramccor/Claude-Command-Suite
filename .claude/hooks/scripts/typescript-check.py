#!/usr/bin/env python3
"""
TypeScript type checking hook for Claude Code.
Runs incremental type checking on TypeScript and Svelte files.
"""
import json
import sys
import subprocess
import os
import tempfile
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
    
    # Only process editing tools
    if tool_name not in ["Write", "Edit", "MultiEdit"]:
        sys.exit(0)
    
    # Only process TypeScript and Svelte files
    if not file_path.endswith((".ts", ".tsx", ".svelte", ".js", ".jsx")):
        sys.exit(0)
    
    # Change to project directory if available
    project_dir = os.environ.get("CLAUDE_PROJECT_DIR", os.getcwd())
    os.chdir(project_dir)
    
    # Check if TypeScript is configured
    if not os.path.exists("tsconfig.json"):
        # No TypeScript configuration, skip
        sys.exit(0)
    
    # Create a temporary file for incremental compilation info
    build_info_file = os.path.join(tempfile.gettempdir(), f"claude-tsc-{os.path.basename(project_dir)}.tsbuildinfo")
    
    # Run TypeScript with incremental compilation
    try:
        cmd = [
            "npx", "tsc",
            "--noEmit",
            "--incremental",
            "--tsBuildInfoFile", build_info_file,
            "--pretty", "false"  # Easier to parse output
        ]
        
        # For specific file checking (faster)
        if file_path and os.path.exists(file_path):
            # Create a temporary tsconfig that includes only this file
            temp_config = {
                "extends": "./tsconfig.json",
                "include": [file_path],
                "exclude": []
            }
            
            with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
                json.dump(temp_config, f)
                temp_config_path = f.name
            
            cmd.extend(["--project", temp_config_path])
        
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=60
        )
        
        # Clean up temp config if created
        if 'temp_config_path' in locals():
            try:
                os.unlink(temp_config_path)
            except:
                pass
        
        if result.returncode != 0:
            # Parse TypeScript errors
            errors = []
            current_error = None
            
            for line in result.stdout.split('\n'):
                if line and ': error TS' in line:
                    if current_error:
                        errors.append(current_error)
                    # Extract file, line, and error message
                    parts = line.split(': error TS')
                    if len(parts) == 2:
                        file_info = parts[0]
                        error_code_msg = parts[1]
                        
                        # Parse error code and message
                        if ':' in error_code_msg:
                            code, msg = error_code_msg.split(':', 1)
                            current_error = {
                                'file': file_info,
                                'code': f"TS{code}",
                                'message': msg.strip()
                            }
                elif line.strip() and current_error:
                    # Additional error context
                    current_error['message'] += f"\n  {line.strip()}"
            
            if current_error:
                errors.append(current_error)
            
            # Filter to show only errors for the current file
            relevant_errors = [e for e in errors if file_path in e['file']]
            
            if relevant_errors:
                error_msg = f"TypeScript errors in {os.path.basename(file_path)}:\n\n"
                for err in relevant_errors[:5]:  # Limit to first 5 errors
                    error_msg += f"• {err['code']}: {err['message']}\n"
                    if '\n' not in err['message']:  # Add location if not multi-line
                        error_msg += f"  at {err['file']}\n"
                    error_msg += "\n"
                
                if len(relevant_errors) > 5:
                    error_msg += f"... and {len(relevant_errors) - 5} more errors\n"
                
                # For PostToolUse hooks, we return JSON to inform Claude
                output = {
                    "decision": "block",
                    "reason": error_msg.strip()
                }
                print(json.dumps(output))
                sys.exit(0)
            
            # If errors are in other files, just warn
            if errors:
                other_files = set(e['file'].split('(')[0] for e in errors)
                print(f"Note: TypeScript errors exist in other files: {', '.join(list(other_files)[:3])}", file=sys.stderr)
        
        # Success
        output = {
            "suppressOutput": True
        }
        print(json.dumps(output))
        sys.exit(0)
        
    except subprocess.TimeoutExpired:
        print("Warning: TypeScript checking timed out", file=sys.stderr)
        sys.exit(0)  # Don't block on timeout
    except FileNotFoundError:
        print("Warning: TypeScript not found. Install with: npm install -D typescript", file=sys.stderr)
        sys.exit(0)
    except Exception as e:
        print(f"Warning: Error running TypeScript: {e}", file=sys.stderr)
        sys.exit(0)

if __name__ == "__main__":
    main()