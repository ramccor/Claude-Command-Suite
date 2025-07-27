#!/usr/bin/env python3
"""
Component complexity analyzer for Svelte components.
Analyzes components for potential performance and maintainability issues.
"""
import json
import sys
import re
import os
from pathlib import Path

# Thresholds for complexity warnings
THRESHOLDS = {
    "max_lines": 200,
    "max_props": 10,
    "max_effects": 5,
    "max_state_vars": 15,
    "max_each_blocks": 3,
    "max_nested_each": 2,
    "max_dom_nodes": 50,  # Approximate
}

def analyze_svelte_component(file_path):
    """Analyze a Svelte component for complexity metrics."""
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except:
        return None
    
    metrics = {
        "lines": len(content.splitlines()),
        "props": 0,
        "state_vars": 0,
        "derived_vars": 0,
        "effects": 0,
        "each_blocks": 0,
        "nested_each": 0,
        "event_handlers": 0,
        "dom_nodes": 0,
        "issues": [],
        "suggestions": []
    }
    
    # Count props (export let)
    metrics["props"] = len(re.findall(r'export\s+let\s+\w+', content))
    
    # Count state variables ($state)
    metrics["state_vars"] = len(re.findall(r'\$state\s*\(', content))
    
    # Count derived values ($derived)
    metrics["derived_vars"] = len(re.findall(r'\$derived\s*\(', content))
    
    # Count effects ($effect)
    metrics["effects"] = len(re.findall(r'\$effect\s*\(', content))
    
    # Count each blocks
    each_matches = re.findall(r'\{#each\s+', content)
    metrics["each_blocks"] = len(each_matches)
    
    # Check for nested each blocks
    each_block_pattern = r'\{#each[\s\S]*?\{/each\}'
    each_blocks = re.findall(each_block_pattern, content)
    for block in each_blocks:
        inner_each = len(re.findall(r'\{#each\s+', block)) - 1
        metrics["nested_each"] = max(metrics["nested_each"], inner_each)
    
    # Count event handlers
    metrics["event_handlers"] = len(re.findall(r'on:\w+', content))
    
    # Approximate DOM node count (very rough estimate)
    html_tags = re.findall(r'<\w+', content)
    metrics["dom_nodes"] = len(html_tags)
    
    # Check for specific patterns that might indicate issues
    
    # Large arrays in state
    if re.search(r'\$state\s*\(\s*\[[^\]]{100,}\]', content):
        metrics["issues"].append("Large array in $state - consider using $state.raw()")
    
    # Filter/map in reactive statements
    if re.search(r'\$:\s*\w+\s*=.*\.(filter|map|reduce)\s*\(', content):
        metrics["issues"].append("Array operations in reactive statements - consider $derived")
    
    # Memory leak patterns
    if re.search(r'addEventListener|setInterval|setTimeout', content) and not re.search(r'removeEventListener|clearInterval|clearTimeout|onDestroy', content):
        metrics["issues"].append("Event listeners or timers without cleanup - add cleanup in onDestroy")
    
    # Global styles
    global_styles = len(re.findall(r':global\s*\(', content))
    if global_styles > 5:
        metrics["issues"].append(f"Many global styles ({global_styles}) - prefer scoped styles")
    
    # Inline styles
    inline_styles = len(re.findall(r'style\s*=\s*["\']', content))
    if inline_styles > 10:
        metrics["issues"].append(f"Many inline styles ({inline_styles}) - consider CSS classes")
    
    return metrics

def generate_report(metrics, file_path):
    """Generate a complexity report with recommendations."""
    
    warnings = []
    
    # Check against thresholds
    if metrics["lines"] > THRESHOLDS["max_lines"]:
        warnings.append(f"Component is large ({metrics['lines']} lines) - consider splitting")
        metrics["suggestions"].append("Extract reusable parts into separate components")
    
    if metrics["props"] > THRESHOLDS["max_props"]:
        warnings.append(f"Many props ({metrics['props']}) - consider composition")
        metrics["suggestions"].append("Group related props into objects or use slots")
    
    if metrics["state_vars"] > THRESHOLDS["max_state_vars"]:
        warnings.append(f"Many state variables ({metrics['state_vars']}) - consider consolidation")
        metrics["suggestions"].append("Group related state into objects")
    
    if metrics["effects"] > THRESHOLDS["max_effects"]:
        warnings.append(f"Many effects ({metrics['effects']}) - review for optimization")
        metrics["suggestions"].append("Consider if some effects can be converted to $derived")
    
    if metrics["each_blocks"] > THRESHOLDS["max_each_blocks"]:
        warnings.append(f"Multiple each blocks ({metrics['each_blocks']}) - check render performance")
        metrics["suggestions"].append("Consider virtualization for large lists")
    
    if metrics["nested_each"] >= THRESHOLDS["max_nested_each"]:
        warnings.append(f"Deeply nested each blocks - O(n²) complexity risk")
        metrics["suggestions"].append("Flatten data structure or memoize computations")
    
    return warnings

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
    
    # Only process Svelte files
    if not file_path.endswith(".svelte"):
        sys.exit(0)
    
    # Only process on PostToolUse
    if hook_event != "PostToolUse" or tool_name not in ["Write", "Edit", "MultiEdit"]:
        sys.exit(0)
    
    # Change to project directory if available
    project_dir = os.environ.get("CLAUDE_PROJECT_DIR", os.getcwd())
    os.chdir(project_dir)
    
    # Check if file exists
    if not os.path.exists(file_path):
        sys.exit(0)
    
    # Analyze the component
    metrics = analyze_svelte_component(file_path)
    
    if not metrics:
        sys.exit(0)
    
    # Generate warnings
    warnings = generate_report(metrics, file_path)
    
    # Create summary
    component_name = os.path.basename(file_path)
    
    if warnings or metrics["issues"]:
        summary = f"📊 Component Analysis for {component_name}:\n\n"
        
        # Show metrics
        summary += "Metrics:\n"
        summary += f"  • Lines: {metrics['lines']}\n"
        summary += f"  • Props: {metrics['props']}\n"
        summary += f"  • State variables: {metrics['state_vars']}\n"
        summary += f"  • Effects: {metrics['effects']}\n"
        summary += f"  • Each blocks: {metrics['each_blocks']}"
        if metrics['nested_each'] > 0:
            summary += f" (max nesting: {metrics['nested_each'] + 1})"
        summary += "\n\n"
        
        if warnings:
            summary += "⚠️  Complexity Warnings:\n"
            for warning in warnings:
                summary += f"  • {warning}\n"
            summary += "\n"
        
        if metrics["issues"]:
            summary += "🔍 Potential Issues:\n"
            for issue in metrics["issues"]:
                summary += f"  • {issue}\n"
            summary += "\n"
        
        if metrics["suggestions"]:
            summary += "💡 Suggestions:\n"
            for suggestion in metrics["suggestions"]:
                summary += f"  • {suggestion}\n"
        
        # For PostToolUse, we can inform but not block
        print(summary.strip(), file=sys.stderr)
        
        # If component is very complex, suggest refactoring via Claude
        if len(warnings) >= 3:
            output = {
                "decision": "block",
                "reason": f"Component has high complexity ({len(warnings)} warnings). Consider refactoring for better maintainability and performance.\n\n{summary}"
            }
            print(json.dumps(output))
            sys.exit(0)
    
    # Success - component is reasonably simple
    output = {
        "suppressOutput": True
    }
    print(json.dumps(output))
    sys.exit(0)

if __name__ == "__main__":
    main()