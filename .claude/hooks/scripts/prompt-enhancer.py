#!/usr/bin/env python3
"""
Prompt enhancer for Claude Code.
Adds context and validates prompts for Svelte development.
"""
import json
import sys
import re
import datetime
import os

def add_svelte_context(prompt):
    """Add relevant Svelte context based on prompt content."""
    context_parts = []
    
    # Add timestamp
    context_parts.append(f"Current time: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Check for Svelte 5 keywords and add migration context
    if re.search(r'\b(rune|runes|\$state|\$derived|\$effect)\b', prompt, re.I):
        context_parts.append("Note: This project uses Svelte 5 with runes. Use $state(), $derived(), and $effect() syntax.")
    
    # Check for testing keywords
    if re.search(r'\b(test|testing|vitest|playwright|coverage)\b', prompt, re.I):
        context_parts.append("Testing setup: Vitest for unit tests, Playwright for E2E tests. Run 'npm test' for unit tests.")
    
    # Check for Storybook keywords
    if re.search(r'\b(story|stories|storybook)\b', prompt, re.I):
        context_parts.append("Storybook is configured with @storybook/sveltekit. Stories use Svelte CSF format.")
    
    # Check for performance keywords
    if re.search(r'\b(performance|optimize|bundle|speed|slow)\b', prompt, re.I):
        context_parts.append("Performance tips: Use $state.raw() for large objects, implement virtual scrolling for long lists.")
    
    # Check for accessibility keywords
    if re.search(r'\b(a11y|accessibility|aria|screen reader)\b', prompt, re.I):
        context_parts.append("Accessibility: Ensure WCAG 2.1 AA compliance. Use semantic HTML and ARIA attributes.")
    
    return "\n".join(context_parts) if context_parts else None

def validate_prompt(prompt):
    """Validate prompt for security and best practices."""
    # Check for sensitive information patterns
    sensitive_patterns = [
        (r'(?i)\b(password|secret|key|token|api[_-]?key)\s*[:=]\s*["\']?[\w-]+', "Contains potential secrets"),
        (r'(?i)\b(ssn|social security)\b.*\d{3}-?\d{2}-?\d{4}', "Contains SSN pattern"),
        (r'\b(?:pk|sk)_(?:test|live)_[\w]+\b', "Contains API key pattern"),
    ]
    
    for pattern, message in sensitive_patterns:
        if re.search(pattern, prompt):
            return False, f"Security warning: {message}. Please remove sensitive information."
    
    return True, None

def main():
    try:
        # Read input from stdin
        input_data = json.load(sys.stdin)
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON input: {e}", file=sys.stderr)
        sys.exit(1)

    prompt = input_data.get("prompt", "")
    
    # Validate prompt
    is_valid, error_message = validate_prompt(prompt)
    
    if not is_valid:
        # Block the prompt
        output = {
            "decision": "block",
            "reason": error_message
        }
        print(json.dumps(output))
        sys.exit(0)
    
    # Add context based on prompt content
    additional_context = add_svelte_context(prompt)
    
    # Check for common typos/corrections
    corrections = {
        r'\b(svelkit|sveltkit)\b': 'SvelteKit',
        r'\b(java script)\b': 'JavaScript',
        r'\b(type script)\b': 'TypeScript',
    }
    
    for pattern, correction in corrections.items():
        if re.search(pattern, prompt, re.I):
            additional_context = (additional_context or "") + f"\n(Auto-correction: '{pattern}' → '{correction}')"
    
    if additional_context:
        # Add context using JSON output
        output = {
            "hookSpecificOutput": {
                "hookEventName": "UserPromptSubmit",
                "additionalContext": additional_context
            }
        }
        print(json.dumps(output))
    else:
        # No additional context needed
        output = {
            "suppressOutput": True
        }
        print(json.dumps(output))
    
    sys.exit(0)

if __name__ == "__main__":
    main()