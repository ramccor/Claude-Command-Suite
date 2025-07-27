# Svelte Hooks Quick Reference

A quick reference guide for Claude Code hooks in Svelte projects.

## Essential Hooks (Recommended for All Projects)

```json
{
  "hooks": {
    "post-edit": {
      "svelte-validate": {
        "command": "test \"${FILE_PATH##*.}\" = \"svelte\" && npx sv check --file \"$FILE_PATH\" || true",
        "description": "Validates Svelte syntax",
        "blocking": false
      },
      "format-save": {
        "command": "if [[ \"$FILE_PATH\" =~ \\.(svelte|ts|js)$ ]]; then npx prettier --write \"$FILE_PATH\"; fi",
        "description": "Auto-format on save",
        "blocking": false
      },
      "type-check": {
        "command": "if [[ \"$FILE_PATH\" =~ \\.(svelte|ts)$ ]]; then npx tsc --noEmit --incremental || true; fi",
        "description": "TypeScript type checking",
        "blocking": false
      }
    }
  }
}
```

## Hook Categories

### 🛡️ Validation & Safety
- **svelte-validate**: Syntax validation
- **type-check**: TypeScript validation
- **a11y-check**: Accessibility validation
- **security-check**: XSS and security patterns

### 🎨 Code Quality
- **format-save**: Prettier formatting
- **lint**: ESLint checking
- **import-order**: Import organization
- **naming-convention**: File naming rules

### 🧪 Testing
- **run-component-tests**: Auto-run related tests
- **coverage-guard**: Maintain coverage threshold
- **test-reminder**: Remind to write tests
- **story-sync**: Ensure Storybook stories exist

### 📊 Performance
- **bundle-impact**: Monitor bundle size
- **render-complexity**: Component complexity
- **memory-leak-check**: Cleanup validation
- **lighthouse-perf**: Performance scoring

### 👥 Team Collaboration
- **todo-tracker**: Track TODOs/FIXMEs
- **doc-enforcer**: Require documentation
- **breaking-change**: Detect API changes
- **usage-alert**: Warn about high-impact changes

### 📚 Storybook
- **story-sync**: Component-story pairing
- **storybook-build**: Build validation
- **story-reminder**: Create story reminders

## Quick Setup Guide

### 1. Minimal Setup (Development Speed)
```json
{
  "hooks": {
    "post-edit": {
      "quick-fix": {
        "command": "if [[ \"$FILE_PATH\" =~ \\.(svelte|ts|js)$ ]]; then npx prettier --write \"$FILE_PATH\" && npx eslint \"$FILE_PATH\" --fix; fi",
        "description": "Format and fix",
        "blocking": false
      }
    }
  }
}
```

### 2. Quality Focused Setup
```json
{
  "hooks": {
    "post-edit": {
      "quality-check": {
        "command": "if [[ \"$FILE_PATH\" =~ \\.svelte$ ]]; then npx sv check --file \"$FILE_PATH\" && echo '✅ Valid Svelte' || echo '❌ Fix errors'; fi",
        "description": "Ensure quality",
        "blocking": true,
        "blockingMessage": "Fix Svelte errors before continuing"
      }
    },
    "pre-commit": {
      "test-suite": {
        "command": "npm test -- --run",
        "description": "Run tests before commit",
        "blocking": true
      }
    }
  }
}
```

### 3. Team Collaboration Setup
```json
{
  "hooks": {
    "post-edit": {
      "team-checks": {
        "command": "echo 'Checking team standards...' && grep -q '@component' \"$FILE_PATH\" || echo '📝 Add @component JSDoc'",
        "description": "Team standards",
        "blocking": false
      }
    }
  }
}
```

## Performance Considerations

### Fast Hooks (< 100ms)
- File existence checks
- Simple grep patterns
- Prettier formatting
- Basic validation

### Medium Hooks (100-500ms)
- TypeScript checking (incremental)
- ESLint with cache
- Bundle size checks
- Test execution (single file)

### Slow Hooks (> 500ms)
- Full project builds
- Complete test suites
- Lighthouse analysis
- Coverage reports

## Best Practices

1. **Start Small**: Add 2-3 hooks initially
2. **Monitor Performance**: Disable slow hooks during rapid development
3. **Use Blocking Sparingly**: Only for critical issues
4. **Cache When Possible**: Use incremental builds
5. **Team Agreement**: Ensure team consensus on hooks

## Debugging Hooks

### Test a Hook
```bash
# Test hook command directly
FILE_PATH="src/lib/Button.svelte" bash -c 'your-hook-command'
```

### Check Hook Logs
```bash
# View Claude Code logs
tail -f ~/.claude/logs/hooks.log
```

### Disable Temporarily
```json
{
  "hooks": {
    "post-edit": {
      "slow-hook": {
        "command": "true",  // Temporarily disabled
        "description": "Disabled for debugging"
      }
    }
  }
}
```

## Common Patterns

### Conditional Execution
```bash
# Only run on specific files
[[ "$FILE_PATH" =~ \\.svelte$ ]] && command

# Only in certain directories
[[ "$FILE_PATH" =~ ^src/lib/ ]] && command

# Skip test files
[[ ! "$FILE_PATH" =~ \\.test\\. ]] && command
```

### Error Handling
```bash
# Continue on error
command || true

# Show custom error message
command || echo "❌ Custom error message"

# Silent failure
command 2>/dev/null || true
```

### Output Formatting
```bash
# Colored output
echo -e "\\033[0;32m✅ Success\\033[0m"
echo -e "\\033[0;33m⚠️  Warning\\033[0m"
echo -e "\\033[0;31m❌ Error\\033[0m"
```

## Hook Combinations

### Development Workflow
1. **pre-edit**: Show component usage
2. **post-edit**: Validate and format
3. **post-write**: Check naming conventions
4. **pre-commit**: Run tests

### CI/CD Workflow
1. **post-edit**: Type checking
2. **pre-commit**: Full test suite
3. **pre-commit**: Build validation
4. **pre-commit**: Coverage check

### Team Workflow
1. **post-edit**: Documentation check
2. **post-edit**: TODO tracking
3. **pre-commit**: Standards enforcement
4. **post-write**: Change logging