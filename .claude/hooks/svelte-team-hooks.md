# Svelte Team Collaboration Hooks

Hooks designed to maintain consistency, documentation, and communication in team Svelte projects.

## Code Ownership and Documentation

### 1. Component Author Tracking
Automatically adds author information to new components.

```json
{
  "hooks": {
    "post-write": {
      "add-author": {
        "command": "if [[ \"$FILE_PATH\" =~ \\.svelte$ ]] && [[ ! -f \"$FILE_PATH\" ]]; then sed -i '1i<!--\\n  @component\\n  @author '$(git config user.name)' <'$(git config user.email)'>\\n  @created '$(date +%Y-%m-%d)'\\n-->' \"$FILE_PATH\"; fi",
        "description": "Adds author metadata to new components",
        "blocking": false
      }
    }
  }
}
```

### 2. TODO/FIXME Tracker
Tracks and reports TODOs and FIXMEs in modified files.

```json
{
  "hooks": {
    "post-edit": {
      "todo-tracker": {
        "command": "if [[ \"$FILE_PATH\" =~ \\.(svelte|ts|js)$ ]]; then TODOS=$(grep -n 'TODO\\|FIXME\\|HACK\\|XXX' \"$FILE_PATH\" 2>/dev/null | wc -l); if [ $TODOS -gt 0 ]; then echo \"📝 Found $TODOS TODO/FIXME items:\"; grep -n 'TODO\\|FIXME\\|HACK\\|XXX' \"$FILE_PATH\" | head -3; fi; fi",
        "description": "Reports TODOs in modified files",
        "blocking": false
      }
    }
  }
}
```

### 3. Component Documentation Enforcer
Ensures components have proper documentation.

```json
{
  "hooks": {
    "pre-commit": {
      "doc-enforcer": {
        "command": "git diff --cached --name-only | grep '\\.svelte$' | while read f; do grep -q '@component' \"$f\" || echo \"❌ Missing @component doc: $f\"; done",
        "description": "Enforces component documentation",
        "blocking": true,
        "blockingMessage": "All components must have @component JSDoc"
      }
    }
  }
}
```

## Naming Convention Enforcement

### 4. File Naming Convention Check
Ensures consistent file naming across the team.

```json
{
  "hooks": {
    "post-write": {
      "naming-convention": {
        "command": "if [[ \"$FILE_PATH\" =~ \\.svelte$ ]]; then BASE=$(basename \"$FILE_PATH\" .svelte); if [[ ! \"$BASE\" =~ ^[A-Z][a-zA-Z0-9]*$ ]]; then echo \"❌ Component names must be PascalCase: $BASE\"; fi; fi",
        "description": "Enforces PascalCase component names",
        "blocking": false
      }
    }
  }
}
```

### 5. Route Naming Validator
Ensures SvelteKit routes follow team conventions.

```json
{
  "hooks": {
    "post-write": {
      "route-naming": {
        "command": "if [[ \"$FILE_PATH\" =~ routes/ ]]; then if [[ \"$FILE_PATH\" =~ [A-Z] ]] && [[ ! \"$FILE_PATH\" =~ \\[.*\\] ]]; then echo \"⚠️  Route paths should be lowercase\"; fi; fi",
        "description": "Validates route naming conventions",
        "blocking": false
      }
    }
  }
}
```

## Code Review Helpers

### 6. Complexity Warning for Review
Flags complex components that need careful review.

```json
{
  "hooks": {
    "post-edit": {
      "complexity-flag": {
        "command": "if [[ \"$FILE_PATH\" =~ \\.svelte$ ]]; then LINES=$(wc -l < \"$FILE_PATH\"); if [ $LINES -gt 200 ]; then echo \"🔍 Large component ($LINES lines) - consider splitting\"; fi; PROPS=$(grep -c 'export let' \"$FILE_PATH\"); if [ $PROPS -gt 10 ]; then echo \"🔍 Many props ($PROPS) - consider composition\"; fi; fi",
        "description": "Flags complex components for review",
        "blocking": false
      }
    }
  }
}
```

### 7. Breaking Change Detector
Warns about potential breaking changes in components.

```json
{
  "hooks": {
    "post-edit": {
      "breaking-change": {
        "command": "if [[ \"$FILE_PATH\" =~ \\.svelte$ ]] && git diff \"$FILE_PATH\" | grep -E '^-\\s*export let' > /dev/null; then echo \"⚠️  BREAKING: Removed or renamed props detected\"; git diff \"$FILE_PATH\" | grep -E '^-\\s*export let'; fi",
        "description": "Detects breaking changes in component APIs",
        "blocking": false
      }
    }
  }
}
```

## Team Communication

### 8. Component Change Notifier
Creates a change log entry for significant component changes.

```bash
#!/bin/bash
# Save as .claude/scripts/component-changelog.sh

COMPONENT=$(basename "$1" .svelte)
CHANGE_LOG=".claude/component-changes.log"

if git diff "$1" | grep -E '^[+-]\s*export let' > /dev/null; then
    echo "[$(date +%Y-%m-%d)] $COMPONENT - API changed by $(git config user.name)" >> "$CHANGE_LOG"
    git diff "$1" | grep -E '^[+-]\s*export let' | sed 's/^/  /' >> "$CHANGE_LOG"
    echo "" >> "$CHANGE_LOG"
    echo "📝 Component API change logged"
fi
```

```json
{
  "hooks": {
    "post-edit": {
      "api-changelog": {
        "command": "if [[ \"$FILE_PATH\" =~ \\.svelte$ ]]; then .claude/scripts/component-changelog.sh \"$FILE_PATH\"; fi",
        "description": "Logs component API changes",
        "blocking": false
      }
    }
  }
}
```

### 9. Shared Component Usage Alert
Alerts when modifying widely-used components.

```json
{
  "hooks": {
    "pre-edit": {
      "usage-alert": {
        "command": "if [[ \"$FILE_PATH\" =~ lib/components/.*\\.svelte$ ]]; then USAGE=$(grep -r \"$(basename \"$FILE_PATH\" .svelte)\" --include=\"*.svelte\" . | wc -l); if [ $USAGE -gt 10 ]; then echo \"⚠️  This component is used in $USAGE places - changes will have wide impact\"; fi; fi",
        "description": "Warns about widely-used component modifications",
        "blocking": false
      }
    }
  }
}
```

## Style Guide Enforcement

### 10. Import Order Checker
Ensures consistent import ordering.

```json
{
  "hooks": {
    "post-edit": {
      "import-order": {
        "command": "if [[ \"$FILE_PATH\" =~ \\.(svelte|ts|js)$ ]]; then awk '/^import/ {imports[NR]=$0} /^[^i]/ && imports[1] {for(i in imports) print imports[i] | \"sort -k2\"; exit}' \"$FILE_PATH\" > /tmp/sorted_imports && if ! diff -q <(awk '/^import/ {print}' \"$FILE_PATH\") /tmp/sorted_imports > /dev/null; then echo \"💡 Consider sorting imports alphabetically\"; fi; fi",
        "description": "Suggests import ordering",
        "blocking": false
      }
    }
  }
}
```

### 11. Event Handler Naming
Ensures consistent event handler naming.

```json
{
  "hooks": {
    "post-edit": {
      "event-naming": {
        "command": "if [[ \"$FILE_PATH\" =~ \\.svelte$ ]] && grep -E 'on:[a-z]+=[\"'\"']{' \"$FILE_PATH\" | grep -v 'on:[a-z]+=[\"'\"']{handle' > /dev/null; then echo \"💡 Consider prefixing event handlers with 'handle'\"; fi",
        "description": "Suggests consistent event handler naming",
        "blocking": false
      }
    }
  }
}
```

## Dependency Management

### 12. New Dependency Alert
Alerts team when new dependencies are added.

```json
{
  "hooks": {
    "post-edit": {
      "dep-alert": {
        "command": "if [[ \"$FILE_PATH\" = \"package.json\" ]] && git diff \"$FILE_PATH\" | grep '^+.*\"dependencies\"\\|^+.*\"devDependencies\"' -A 5 | grep '^+' | grep -v '^+++' > /dev/null; then echo \"📦 New dependencies added - ensure team approval:\"; git diff \"$FILE_PATH\" | grep '^+' | grep '\":' | grep -v dependencies; fi",
        "description": "Alerts about new dependencies",
        "blocking": false
      }
    }
  }
}
```

## Design System Compliance

### 13. Design Token Usage
Encourages use of design tokens over hard-coded values.

```json
{
  "hooks": {
    "post-edit": {
      "design-tokens": {
        "command": "if [[ \"$FILE_PATH\" =~ \\.svelte$ ]]; then HARDCODED=$(grep -E 'color:\\s*#[0-9a-fA-F]{3,6}|font-size:\\s*[0-9]+px' \"$FILE_PATH\" | wc -l); if [ $HARDCODED -gt 0 ]; then echo \"🎨 Found $HARDCODED hard-coded design values. Use design tokens instead.\"; fi; fi",
        "description": "Encourages design token usage",
        "blocking": false
      }
    }
  }
}
```

## Complete Team Configuration

Here's a recommended team configuration combining the most useful hooks:

```json
{
  "hooks": {
    "post-edit": {
      "team-standards": {
        "command": "if [[ \"$FILE_PATH\" =~ \\.(svelte|ts|js)$ ]]; then echo '👥 Team Standards Check:'; grep -q '@component' \"$FILE_PATH\" || echo '  ❌ Missing @component JSDoc'; TODOS=$(grep -c 'TODO\\|FIXME' \"$FILE_PATH\"); [ $TODOS -gt 0 ] && echo \"  📝 $TODOS TODOs found\"; grep -E 'console\\.(log|error|warn)' \"$FILE_PATH\" > /dev/null && echo '  ⚠️  Console statements detected'; fi",
        "description": "Comprehensive team standards check",
        "blocking": false
      }
    },
    "pre-commit": {
      "team-review": {
        "command": "echo '👥 Pre-commit Team Checks:'; git diff --cached --name-only | grep '\\.svelte$' | while read f; do grep -q '@component' \"$f\" || echo \"  ❌ Missing docs: $f\"; done; git diff --cached --name-only | grep -E '\\.(test|spec)\\.(ts|js)$' | wc -l | awk '{if($1==0) print \"  ⚠️  No test files in commit\"}'",
        "description": "Team review checklist",
        "blocking": false
      }
    }
  }
}
```

## Git Integration for Teams

### 14. Branch Protection Reminder
Reminds about branch naming conventions.

```json
{
  "hooks": {
    "pre-commit": {
      "branch-check": {
        "command": "BRANCH=$(git branch --show-current); if [[ ! \"$BRANCH\" =~ ^(feature|fix|chore|docs)/.+ ]]; then echo \"⚠️  Branch name should follow pattern: feature/*, fix/*, chore/*, or docs/*\"; fi",
        "description": "Checks branch naming convention",
        "blocking": false
      }
    }
  }
}
```

### 15. PR Template Reminder
Reminds to follow PR template when committing.

```json
{
  "hooks": {
    "pre-commit": {
      "pr-reminder": {
        "command": "if [ -f .github/pull_request_template.md ]; then echo \"📋 Remember to follow PR template when creating pull request\"; fi",
        "description": "Reminds about PR template",
        "blocking": false
      }
    }
  }
}
```