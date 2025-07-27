#!/bin/bash
# Test runner hook for Svelte components
# Automatically runs tests for modified components

# Read JSON input from stdin
input=$(cat)

# Extract file path and tool name
if command -v jq &> /dev/null; then
    tool_name=$(echo "$input" | jq -r '.tool_name // ""')
    file_path=$(echo "$input" | jq -r '.tool_input.file_path // ""')
    hook_event=$(echo "$input" | jq -r '.hook_event_name // ""')
else
    # Fallback to python
    tool_name=$(echo "$input" | python3 -c "import sys, json; d=json.load(sys.stdin); print(d.get('tool_name', ''))")
    file_path=$(echo "$input" | python3 -c "import sys, json; d=json.load(sys.stdin); print(d.get('tool_input', {}).get('file_path', ''))")
    hook_event=$(echo "$input" | python3 -c "import sys, json; d=json.load(sys.stdin); print(d.get('hook_event_name', ''))")
fi

# Change to project directory if available
cd "${CLAUDE_PROJECT_DIR:-$(pwd)}"

# Function to find test file for a component
find_test_file() {
    local component_file="$1"
    local base_name="${component_file%.*}"
    
    # Common test file patterns
    local test_patterns=(
        "${base_name}.test.ts"
        "${base_name}.test.js"
        "${base_name}.spec.ts"
        "${base_name}.spec.js"
        "tests/${base_name}.test.ts"
        "__tests__/${base_name}.test.ts"
    )
    
    for pattern in "${test_patterns[@]}"; do
        if [[ -f "$pattern" ]]; then
            echo "$pattern"
            return 0
        fi
    done
    
    return 1
}

# Handle different hook events
case "$hook_event" in
    "PreToolUse")
        # For PreToolUse, we might want to run tests before allowing edits
        if [[ "$tool_name" =~ ^(Write|Edit|MultiEdit)$ ]] && [[ "$file_path" =~ \.(svelte|ts|js)$ ]]; then
            test_file=$(find_test_file "$file_path")
            if [[ -n "$test_file" ]]; then
                echo "🧪 Running tests for $file_path before edit..." >&2
                
                # Run the specific test file
                if npm test -- "$test_file" --run &>/dev/null; then
                    echo '{"decision": "approve", "reason": "Tests passed", "suppressOutput": true}'
                else
                    # Tests failed, ask for confirmation
                    cat <<EOF
{
  "hookSpecificOutput": {
    "hookEventName": "PreToolUse",
    "permissionDecision": "ask",
    "permissionDecisionReason": "Tests are currently failing for this component. Do you want to proceed with editing?"
  }
}
EOF
                fi
                exit 0
            fi
        fi
        ;;
    
    "PostToolUse")
        # For PostToolUse, run tests after edits
        if [[ "$tool_name" =~ ^(Write|Edit|MultiEdit)$ ]] && [[ "$file_path" =~ \.(svelte|ts|js)$ ]]; then
            test_file=$(find_test_file "$file_path")
            if [[ -n "$test_file" ]]; then
                echo "🧪 Running tests for modified component..." >&2
                
                # Run the test with more detailed output
                test_output=$(npm test -- "$test_file" --run 2>&1)
                test_exit_code=$?
                
                if [ $test_exit_code -ne 0 ]; then
                    # Parse test output for failures
                    failed_tests=$(echo "$test_output" | grep -E "✓|✗|FAIL|PASS" | grep -v "✓" | head -5)
                    
                    # Create detailed error message
                    error_msg="Tests failed for ${file_path}:\n\n"
                    if [[ -n "$failed_tests" ]]; then
                        error_msg+="Failed tests:\n$failed_tests\n\n"
                    fi
                    error_msg+="Run 'npm test $test_file' to see full output."
                    
                    cat <<EOF
{
  "decision": "block",
  "reason": "$error_msg"
}
EOF
                    exit 0
                else
                    echo "✅ All tests passed!" >&2
                fi
            else
                # No test file found - remind to create one
                if [[ "$file_path" =~ \.(svelte)$ ]] && [[ "$file_path" =~ lib/components/ ]]; then
                    echo "📝 No test file found for this component. Consider creating ${file_path%.svelte}.test.ts" >&2
                fi
            fi
        fi
        ;;
    
    "Stop")
        # Run all tests when Claude stops
        echo "🧪 Running test suite..." >&2
        if npm test -- --run &>/dev/null; then
            echo "✅ All tests passed!" >&2
        else
            echo "⚠️  Some tests are failing. Run 'npm test' to see details." >&2
        fi
        ;;
esac

# Default success response
echo '{"suppressOutput": true}'
exit 0