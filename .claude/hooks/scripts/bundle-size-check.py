#!/usr/bin/env python3
"""
Bundle size checker hook for Claude Code.
Monitors bundle size impact of changes to prevent bloat.
"""
import json
import sys
import subprocess
import os
import tempfile
import shutil
from pathlib import Path

# Configuration
MAX_BUNDLE_SIZE_KB = 500  # Maximum bundle size in KB
MAX_INCREASE_KB = 50      # Maximum allowed increase in KB
CACHE_DIR = os.path.join(tempfile.gettempdir(), "claude-bundle-cache")

def get_bundle_size(build_output_dir="dist"):
    """Calculate total size of build output."""
    total_size = 0
    
    if not os.path.exists(build_output_dir):
        return 0
    
    for root, dirs, files in os.walk(build_output_dir):
        for file in files:
            if file.endswith(('.js', '.css', '.wasm')):
                file_path = os.path.join(root, file)
                total_size += os.path.getsize(file_path)
    
    return total_size

def format_size(size_bytes):
    """Format size in human-readable format."""
    kb = size_bytes / 1024
    if kb < 1024:
        return f"{kb:.1f}KB"
    else:
        mb = kb / 1024
        return f"{mb:.2f}MB"

def save_baseline_size(project_name, size):
    """Save baseline bundle size."""
    os.makedirs(CACHE_DIR, exist_ok=True)
    cache_file = os.path.join(CACHE_DIR, f"{project_name}_bundle_size.json")
    
    data = {"size": size, "timestamp": os.path.getmtime("package.json")}
    
    with open(cache_file, 'w') as f:
        json.dump(data, f)

def get_baseline_size(project_name):
    """Get cached baseline bundle size."""
    cache_file = os.path.join(CACHE_DIR, f"{project_name}_bundle_size.json")
    
    if not os.path.exists(cache_file):
        return None
    
    try:
        with open(cache_file, 'r') as f:
            data = json.load(f)
            
        # Check if package.json has been modified
        if os.path.getmtime("package.json") > data.get("timestamp", 0):
            return None  # Baseline is outdated
            
        return data.get("size")
    except:
        return None

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
    hook_event = input_data.get("hook_event_name", "")
    
    # Only check for JS/TS/Svelte files
    if not file_path.endswith((".js", ".ts", ".jsx", ".tsx", ".svelte", ".mjs", ".cjs")):
        sys.exit(0)
    
    # Skip test files
    if ".test." in file_path or ".spec." in file_path:
        sys.exit(0)
    
    # Change to project directory if available
    project_dir = os.environ.get("CLAUDE_PROJECT_DIR", os.getcwd())
    os.chdir(project_dir)
    
    # Get project name for caching
    project_name = os.path.basename(project_dir)
    
    # Check if this is a significant file (in src or lib)
    if not any(part in file_path for part in ["src/", "lib/", "components/"]):
        sys.exit(0)
    
    # For PreToolUse, just get baseline
    if hook_event == "PreToolUse":
        baseline = get_baseline_size(project_name)
        if baseline is None:
            # Try to build and get baseline
            print("📦 Measuring baseline bundle size...", file=sys.stderr)
            try:
                subprocess.run(["npm", "run", "build"], 
                             capture_output=True, 
                             timeout=120,
                             check=False)
                baseline = get_bundle_size()
                save_baseline_size(project_name, baseline)
            except:
                pass
        sys.exit(0)
    
    # For PostToolUse, check bundle size impact
    if hook_event == "PostToolUse" and tool_name in ["Write", "Edit", "MultiEdit"]:
        # Get baseline size
        baseline = get_baseline_size(project_name)
        
        print("📦 Checking bundle size impact...", file=sys.stderr)
        
        # Run build
        try:
            result = subprocess.run(
                ["npm", "run", "build"],
                capture_output=True,
                text=True,
                timeout=120
            )
            
            if result.returncode != 0:
                print("Warning: Build failed, skipping bundle size check", file=sys.stderr)
                sys.exit(0)
            
            # Get new bundle size
            new_size = get_bundle_size()
            
            # Save as new baseline
            save_baseline_size(project_name, new_size)
            
            # Check absolute size
            if new_size > MAX_BUNDLE_SIZE_KB * 1024:
                output = {
                    "decision": "block",
                    "reason": f"Bundle size ({format_size(new_size)}) exceeds maximum allowed size ({MAX_BUNDLE_SIZE_KB}KB). Consider code splitting or removing unused dependencies."
                }
                print(json.dumps(output))
                sys.exit(0)
            
            # Check size increase if we have baseline
            if baseline is not None:
                increase = new_size - baseline
                increase_kb = increase / 1024
                
                if increase_kb > MAX_INCREASE_KB:
                    # Try to identify what caused the increase
                    import_analysis = ""
                    
                    # Check for new imports in the file
                    if os.path.exists(file_path):
                        with open(file_path, 'r') as f:
                            content = f.read()
                            
                        # Look for heavy imports
                        heavy_libs = ["lodash", "moment", "jquery", "three", "chart.js", "d3"]
                        found_libs = [lib for lib in heavy_libs if f'from "{lib}"' in content or f"from '{lib}'" in content]
                        
                        if found_libs:
                            import_analysis = f"\n\nDetected heavy libraries: {', '.join(found_libs)}. Consider using lighter alternatives or importing only what you need."
                    
                    output = {
                        "decision": "block",
                        "reason": f"Bundle size increased by {format_size(increase)} (from {format_size(baseline)} to {format_size(new_size)}). Maximum allowed increase is {MAX_INCREASE_KB}KB.{import_analysis}"
                    }
                    print(json.dumps(output))
                    sys.exit(0)
                elif increase_kb > 10:
                    print(f"ℹ️  Bundle size increased by {format_size(increase)} to {format_size(new_size)}", file=sys.stderr)
                elif increase_kb < -10:
                    print(f"✅ Bundle size decreased by {format_size(-increase)} to {format_size(new_size)}", file=sys.stderr)
            else:
                print(f"📦 Bundle size: {format_size(new_size)}", file=sys.stderr)
            
        except subprocess.TimeoutExpired:
            print("Warning: Build timed out", file=sys.stderr)
        except Exception as e:
            print(f"Warning: Bundle size check failed: {e}", file=sys.stderr)
    
    # Success
    output = {
        "suppressOutput": True
    }
    print(json.dumps(output))
    sys.exit(0)

if __name__ == "__main__":
    main()