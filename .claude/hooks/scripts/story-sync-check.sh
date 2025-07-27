#!/bin/bash
# Story sync checker for Svelte components
# Ensures components have corresponding Storybook stories

# Read JSON input from stdin
input=$(cat)

# Extract file path and tool name
if command -v jq &> /dev/null; then
    tool_name=$(echo "$input" | jq -r '.tool_name // ""')
    file_path=$(echo "$input" | jq -r '.tool_input.file_path // ""')
else
    # Fallback to python
    tool_name=$(echo "$input" | python3 -c "import sys, json; print(json.load(sys.stdin).get('tool_name', ''))")
    file_path=$(echo "$input" | python3 -c "import sys, json; print(json.load(sys.stdin).get('tool_input', {}).get('file_path', ''))")
fi

# Only process Write tool for new Svelte components
if [[ "$tool_name" != "Write" ]] || [[ ! "$file_path" =~ \.svelte$ ]]; then
    exit 0
fi

# Skip if not a component (pages, layouts, etc.)
if [[ "$file_path" =~ \+page\.svelte$ ]] || [[ "$file_path" =~ \+layout\.svelte$ ]]; then
    exit 0
fi

# Only check components in lib directory
if [[ ! "$file_path" =~ (lib|components)/ ]]; then
    exit 0
fi

# Change to project directory if available
cd "${CLAUDE_PROJECT_DIR:-$(pwd)}"

# Get component name and directory
component_dir=$(dirname "$file_path")
component_name=$(basename "$file_path" .svelte)

# Look for story file
story_patterns=(
    "${component_dir}/${component_name}.stories.svelte"
    "${component_dir}/${component_name}.stories.ts"
    "${component_dir}/${component_name}.stories.js"
    "src/stories/${component_name}.stories.svelte"
)

story_exists=false
for pattern in "${story_patterns[@]}"; do
    if [[ -f "$pattern" ]]; then
        story_exists=true
        break
    fi
done

if [[ "$story_exists" == "false" ]]; then
    cat <<EOF >&2
📚 Storybook Reminder:
No story file found for component: $component_name

Consider creating: ${component_dir}/${component_name}.stories.svelte

Example story:
<script>
  import { defineMeta } from '@storybook/addon-svelte-csf';
  import $component_name from './$component_name.svelte';

  const { Story } = defineMeta({
    component: $component_name,
    title: 'Components/$component_name',
    tags: ['autodocs']
  });
</script>

<Story name="Default" />
EOF
fi

# Always allow the operation
echo '{"suppressOutput": true}'
exit 0