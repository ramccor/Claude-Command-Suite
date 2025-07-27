# Svelte Project Hooks for Claude Code

This document provides example hooks configurations for Svelte/SvelteKit projects. These hooks help maintain code quality, catch errors early, and automate common development tasks.

## Installation

Add these hooks to your Claude Code settings file (`~/.config/claude/settings.json` or project-specific `.claude/settings.json`):

```json
{
  "hooks": {
    // Add hooks configurations here
  }
}
```

## Pre-Edit Hooks

### 1. Svelte File Validation Hook
Validates Svelte files before editing to ensure they're properly formatted and compilable.

```json
{
  "hooks": {
    "pre-edit": {
      "svelte-validate": {
        "command": "test \"${FILE_PATH##*.}\" = \"svelte\" && npx sv check --file \"$FILE_PATH\" || true",
        "description": "Validates Svelte files before editing",
        "blocking": false
      }
    }
  }
}
```

### 2. Component Documentation Check
Ensures components have proper documentation before editing.

```json
{
  "hooks": {
    "pre-edit": {
      "check-component-docs": {
        "command": "test \"${FILE_PATH##*.}\" = \"svelte\" && grep -q '@component' \"$FILE_PATH\" || echo '⚠️  Component lacks @component JSDoc'",
        "description": "Checks for component documentation",
        "blocking": false
      }
    }
  }
}
```

## Post-Edit Hooks

### 3. Svelte Compilation Check
Runs after editing Svelte files to ensure they compile correctly.

```json
{
  "hooks": {
    "post-edit": {
      "svelte-compile-check": {
        "command": "test \"${FILE_PATH##*.}\" = \"svelte\" && (npx sv check --file \"$FILE_PATH\" || echo '❌ Svelte compilation failed')",
        "description": "Checks Svelte compilation after edits",
        "blocking": true,
        "blockingMessage": "Svelte compilation errors detected. Fix before proceeding."
      }
    }
  }
}
```

### 4. Rune Usage Validator (Svelte 5)
Validates proper usage of Svelte 5 runes.

```json
{
  "hooks": {
    "post-edit": {
      "validate-runes": {
        "command": "test \"${FILE_PATH##*.}\" = \"svelte\" && (grep -E '\\$(state|derived|effect)' \"$FILE_PATH\" | grep -v 'let.*=.*\\$' || true) && echo '✅ Rune usage looks correct' || echo '⚠️  Check rune declarations'",
        "description": "Validates Svelte 5 rune usage",
        "blocking": false
      }
    }
  }
}
```

### 5. Accessibility Checker
Runs accessibility checks on modified Svelte components.

```json
{
  "hooks": {
    "post-edit": {
      "a11y-check": {
        "command": "test \"${FILE_PATH##*.}\" = \"svelte\" && npx svelte-check --compiler-warnings 'a11y-*:error' \"$FILE_PATH\" || echo '⚠️  Accessibility issues detected'",
        "description": "Checks for accessibility issues",
        "blocking": false
      }
    }
  }
}
```

## Test-Related Hooks

### 6. Auto-Run Component Tests
Automatically runs tests for modified components.

```json
{
  "hooks": {
    "post-edit": {
      "run-component-tests": {
        "command": "if [[ \"$FILE_PATH\" =~ \\.svelte$ ]] && [[ -f \"${FILE_PATH%.svelte}.test.ts\" ]]; then npm test -- \"${FILE_PATH%.svelte}.test.ts\" --run; fi",
        "description": "Runs tests for modified components",
        "blocking": false
      }
    }
  }
}
```

### 7. Test Coverage Guard
Prevents edits if test coverage drops below threshold.

```json
{
  "hooks": {
    "post-edit": {
      "coverage-guard": {
        "command": "if [[ \"$FILE_PATH\" =~ \\.(svelte|ts|js)$ ]]; then npm run test:coverage -- --silent | grep -E 'Statements.*:.*[8-9][0-9]\\.|100\\.' || echo '⚠️  Coverage below 80%'; fi",
        "description": "Ensures test coverage remains high",
        "blocking": false
      }
    }
  }
}
```

## Build and Performance Hooks

### 8. Bundle Size Check
Monitors bundle size impact of changes.

```json
{
  "hooks": {
    "post-edit": {
      "bundle-size-check": {
        "command": "if [[ \"$FILE_PATH\" =~ \\.(svelte|ts|js)$ ]]; then npm run build -- --logLevel=error && du -sh ./dist | awk '{print \"Bundle size: \" $1}'; fi",
        "description": "Checks bundle size impact",
        "blocking": false
      }
    }
  }
}
```

### 9. Type Safety Guard
Ensures TypeScript types are valid after changes.

```json
{
  "hooks": {
    "post-edit": {
      "type-check": {
        "command": "if [[ \"$FILE_PATH\" =~ \\.(svelte|ts)$ ]]; then npx tsc --noEmit --skipLibCheck || echo '❌ Type errors detected'; fi",
        "description": "Validates TypeScript types",
        "blocking": true,
        "blockingMessage": "Type errors must be fixed before continuing."
      }
    }
  }
}
```

## Storybook Hooks

### 10. Story Sync Check
Ensures components have corresponding stories.

```json
{
  "hooks": {
    "post-write": {
      "story-sync": {
        "command": "if [[ \"$FILE_PATH\" =~ /components/.*\\.svelte$ ]] && [[ ! -f \"${FILE_PATH%.svelte}.stories.svelte\" ]]; then echo '📚 Remember to create a story for this component'; fi",
        "description": "Reminds to create Storybook stories",
        "blocking": false
      }
    }
  }
}
```

### 11. Storybook Build Validation
Validates that Storybook builds successfully.

```json
{
  "hooks": {
    "pre-commit": {
      "storybook-build": {
        "command": "if [[ -n $(git diff --cached --name-only | grep -E '\\.(stories\\.(svelte|ts)|storybook/)') ]]; then npm run build-storybook -- --quiet || echo '❌ Storybook build failed'; fi",
        "description": "Ensures Storybook builds correctly",
        "blocking": false
      }
    }
  }
}
```

## Code Quality Hooks

### 12. Linting Hook
Runs ESLint on modified files.

```json
{
  "hooks": {
    "post-edit": {
      "lint": {
        "command": "if [[ \"$FILE_PATH\" =~ \\.(svelte|ts|js)$ ]]; then npx eslint \"$FILE_PATH\" --fix; fi",
        "description": "Lints and fixes code style issues",
        "blocking": false
      }
    }
  }
}
```

### 13. Format on Save
Automatically formats Svelte files using Prettier.

```json
{
  "hooks": {
    "post-edit": {
      "format": {
        "command": "if [[ \"$FILE_PATH\" =~ \\.(svelte|ts|js|css)$ ]]; then npx prettier --write \"$FILE_PATH\"; fi",
        "description": "Formats code with Prettier",
        "blocking": false
      }
    }
  }
}
```

## Security Hooks

### 14. Security Audit
Checks for common security issues in Svelte components.

```json
{
  "hooks": {
    "post-edit": {
      "security-check": {
        "command": "if [[ \"$FILE_PATH\" =~ \\.svelte$ ]]; then grep -E '@html|innerHTML|dangerouslySetInnerHTML' \"$FILE_PATH\" && echo '⚠️  Potential XSS risk detected' || true; fi",
        "description": "Checks for potential security issues",
        "blocking": false
      }
    }
  }
}
```

### 15. Dependency Vulnerability Check
Checks for known vulnerabilities when package.json is modified.

```json
{
  "hooks": {
    "post-edit": {
      "dep-audit": {
        "command": "if [[ \"$FILE_PATH\" = \"package.json\" ]]; then npm audit --audit-level=moderate || echo '⚠️  Security vulnerabilities found'; fi",
        "description": "Audits dependencies for vulnerabilities",
        "blocking": false
      }
    }
  }
}
```

## Git Hooks

### 16. Pre-Commit Validation
Comprehensive validation before committing Svelte files.

```json
{
  "hooks": {
    "pre-commit": {
      "svelte-pre-commit": {
        "command": "git diff --cached --name-only | grep '\\.svelte$' | xargs -I {} npx sv check --file {} || echo '❌ Fix Svelte errors before committing'",
        "description": "Validates all staged Svelte files",
        "blocking": true,
        "blockingMessage": "Svelte validation failed. Fix errors before committing."
      }
    }
  }
}
```

## Utility Hooks

### 17. Component Usage Finder
Finds where a component is used when editing it.

```json
{
  "hooks": {
    "pre-edit": {
      "find-usage": {
        "command": "if [[ \"$FILE_PATH\" =~ \\.svelte$ ]]; then echo \"Component used in:\"; grep -r \"$(basename \"$FILE_PATH\" .svelte)\" --include=\"*.svelte\" --include=\"*.ts\" . | head -5; fi",
        "description": "Shows where component is used",
        "blocking": false
      }
    }
  }
}
```

### 18. Route Guard
Validates SvelteKit route files follow conventions.

```json
{
  "hooks": {
    "post-write": {
      "route-validator": {
        "command": "if [[ \"$FILE_PATH\" =~ routes/.*\\+page\\.svelte$ ]] || [[ \"$FILE_PATH\" =~ routes/.*\\+layout\\.svelte$ ]]; then echo '✅ Valid SvelteKit route file'; else [[ \"$FILE_PATH\" =~ routes/ ]] && echo '⚠️  Use +page.svelte or +layout.svelte naming' || true; fi",
        "description": "Validates SvelteKit route naming",
        "blocking": false
      }
    }
  }
}
```

## Complete Example Configuration

Here's a complete example combining the most useful hooks:

```json
{
  "hooks": {
    "post-edit": {
      "svelte-validate": {
        "command": "test \"${FILE_PATH##*.}\" = \"svelte\" && npx sv check --file \"$FILE_PATH\" --output=machine | jq -r '.diagnostics[] | \"\\(.severity): \\(.message) at line \\(.range.start.line)\"' || true",
        "description": "Validates Svelte files after editing",
        "blocking": false
      },
      "format-on-save": {
        "command": "if [[ \"$FILE_PATH\" =~ \\.(svelte|ts|js)$ ]]; then npx prettier --write \"$FILE_PATH\" && npx eslint \"$FILE_PATH\" --fix; fi",
        "description": "Formats and lints on save",
        "blocking": false
      },
      "type-check": {
        "command": "if [[ \"$FILE_PATH\" =~ \\.(svelte|ts)$ ]]; then npx tsc --noEmit --incremental --tsBuildInfoFile .tsbuildinfo || echo '❌ Type errors detected'; fi",
        "description": "Checks TypeScript types",
        "blocking": false
      }
    },
    "pre-commit": {
      "test-suite": {
        "command": "npm test -- --run && npm run test:e2e -- --reporter=dot",
        "description": "Runs tests before commit",
        "blocking": true,
        "blockingMessage": "Tests must pass before committing"
      }
    }
  }
}
```

## Usage Tips

1. **Start Simple**: Begin with a few essential hooks and add more as needed
2. **Performance**: Keep hooks fast to avoid slowing down your workflow
3. **Blocking vs Non-blocking**: Use blocking hooks sparingly for critical checks
4. **Project-Specific**: Customize hooks based on your project's needs
5. **Team Coordination**: Share hook configurations with your team for consistency

## Troubleshooting

- If hooks are slow, consider using incremental checks or caching
- Use `|| true` to prevent non-critical hooks from failing
- Test hooks in isolation before adding to configuration
- Check Claude Code logs if hooks aren't firing as expected