# Svelte Hooks for Claude Code

This directory contains comprehensive hook configurations for Svelte/SvelteKit projects using Claude Code. Hooks provide automated guards, validations, and utilities that enhance your development workflow.

## 📁 Available Hook Collections

### [svelte-hooks.md](./svelte-hooks.md)
**Core Svelte Development Hooks**
- Pre/post-edit validation
- Compilation checking
- Accessibility validation
- Code formatting
- Test automation
- Git integration

### [svelte-performance-hooks.md](./svelte-performance-hooks.md)
**Performance Monitoring & Optimization**
- Bundle size tracking
- Render complexity analysis
- Memory leak detection
- Lighthouse integration
- CSS performance checks

### [svelte-team-hooks.md](./svelte-team-hooks.md)
**Team Collaboration & Standards**
- Documentation enforcement
- Naming conventions
- Code review helpers
- Breaking change detection
- Design system compliance

### [svelte-advanced-hooks.md](./svelte-advanced-hooks.md)
**Advanced Integrations & Workflows**
- CI/CD validation
- Error tracking integration
- API contract validation
- Security compliance
- Feature flag management

### [svelte-hooks-quick-reference.md](./svelte-hooks-quick-reference.md)
**Quick Reference Guide**
- Essential hooks overview
- Common patterns
- Performance tips
- Debugging guide

## 🚀 Quick Start

### 1. Basic Setup
Add to your Claude Code settings (`~/.config/claude/settings.json`):

```json
{
  "hooks": {
    "post-edit": {
      "svelte-check": {
        "command": "test \"${FILE_PATH##*.}\" = \"svelte\" && npx sv check --file \"$FILE_PATH\" || true",
        "description": "Validate Svelte files",
        "blocking": false
      }
    }
  }
}
```

### 2. Recommended Starter Set
```json
{
  "hooks": {
    "post-edit": {
      "format-and-lint": {
        "command": "if [[ \"$FILE_PATH\" =~ \\.(svelte|ts|js)$ ]]; then npx prettier --write \"$FILE_PATH\" && npx eslint \"$FILE_PATH\" --fix; fi",
        "description": "Format and lint on save",
        "blocking": false
      },
      "type-check": {
        "command": "if [[ \"$FILE_PATH\" =~ \\.(svelte|ts)$ ]]; then npx tsc --noEmit --incremental || echo '❌ Type errors'; fi",
        "description": "Check TypeScript types",
        "blocking": false
      }
    },
    "pre-commit": {
      "test": {
        "command": "npm test -- --run",
        "description": "Run tests before commit",
        "blocking": true
      }
    }
  }
}
```

## 📋 Hook Types

### Pre-Edit Hooks
Run before editing a file:
- Show component usage
- Validate environment setup
- Display warnings for high-impact files

### Post-Edit Hooks
Run after editing a file:
- Syntax validation
- Code formatting
- Type checking
- Test execution

### Post-Write Hooks
Run after creating new files:
- Enforce naming conventions
- Add boilerplate code
- Create accompanying test files

### Pre-Commit Hooks
Run before Git commits:
- Run test suites
- Validate build
- Check code coverage
- Enforce team standards

## 🎯 Use Case Examples

### For Solo Developers
Focus on code quality and automation:
```json
{
  "hooks": {
    "post-edit": {
      "auto-everything": {
        "command": "if [[ \"$FILE_PATH\" =~ \\.(svelte|ts|js)$ ]]; then npx prettier --write \"$FILE_PATH\" && npx sv check --file \"$FILE_PATH\"; fi",
        "description": "Format and validate",
        "blocking": false
      }
    }
  }
}
```

### For Teams
Enforce standards and communication:
```json
{
  "hooks": {
    "post-edit": {
      "team-standards": {
        "command": "grep -q '@component' \"$FILE_PATH\" || echo '📝 Add @component documentation'",
        "description": "Documentation check",
        "blocking": false
      }
    },
    "pre-commit": {
      "review-checklist": {
        "command": "echo '✅ Code reviewed? ✅ Tests written? ✅ Docs updated?'",
        "description": "Pre-commit checklist",
        "blocking": false
      }
    }
  }
}
```

### For Performance-Critical Apps
Monitor and optimize performance:
```json
{
  "hooks": {
    "post-edit": {
      "perf-guard": {
        "command": ".claude/scripts/bundle-check.sh && .claude/scripts/render-complexity.sh",
        "description": "Performance monitoring",
        "blocking": false
      }
    }
  }
}
```

## 🛠️ Creating Custom Hooks

### Hook Anatomy
```json
{
  "hook-name": {
    "command": "shell command to execute",
    "description": "What this hook does",
    "blocking": true/false,
    "blockingMessage": "Message shown when blocking"
  }
}
```

### Best Practices
1. **Keep hooks fast** - Aim for < 200ms execution
2. **Use `|| true`** - Prevent non-critical failures
3. **Provide feedback** - Use echo for user communication
4. **Cache when possible** - Use incremental builds
5. **Test thoroughly** - Validate hooks before team adoption

### Common Patterns
```bash
# File type checking
[[ "$FILE_PATH" =~ \\.svelte$ ]] && command

# Directory filtering
[[ "$FILE_PATH" =~ ^src/lib/ ]] && command

# Error handling
command || echo "❌ Error message"

# Conditional execution
if condition; then command; fi
```

## 📊 Performance Guidelines

### Hook Performance Tiers

**Instant (< 50ms)**
- File existence checks
- Simple grep patterns
- Echo statements

**Fast (50-200ms)**
- Prettier formatting
- Single file linting
- Small script execution

**Acceptable (200-500ms)**
- TypeScript checking (incremental)
- Component testing
- Bundle size checks

**Slow (> 500ms)**
- Full builds
- Complete test suites
- Coverage analysis

### Optimization Tips
1. Use incremental builds where possible
2. Cache results between runs
3. Run expensive checks only on commit
4. Parallelize independent checks
5. Use file filtering to limit scope

## 🐛 Troubleshooting

### Hook Not Firing
```bash
# Check Claude Code logs
tail -f ~/.claude/logs/claude.log

# Test hook directly
FILE_PATH="test.svelte" bash -c 'your-hook-command'
```

### Hook Too Slow
- Add timing: `time your-hook-command`
- Use incremental options
- Move to pre-commit instead
- Consider async execution

### Hook Failing
- Add `|| true` for non-critical hooks
- Check error output
- Validate prerequisites
- Test in isolation

## 🔧 Utility Scripts

Create a `.claude/scripts/` directory for reusable scripts:

```bash
mkdir -p .claude/scripts
chmod +x .claude/scripts/*.sh
```

Example utility script:
```bash
#!/bin/bash
# .claude/scripts/component-check.sh

echo "🔍 Checking component: $1"
# Add your checks here
```

## 📚 Additional Resources

- [Claude Code Settings Documentation](https://docs.anthropic.com/claude-code/settings)
- [Svelte Documentation](https://svelte.dev/docs)
- [SvelteKit Documentation](https://kit.svelte.dev/docs)
- [Hook Examples Repository](https://github.com/anthropic/claude-code-hooks)

## 🤝 Contributing

To contribute new hooks:
1. Test thoroughly in your project
2. Document usage and performance impact
3. Add to appropriate category file
4. Update this README if needed

## 📄 License

These hook configurations are provided as examples and can be freely used and modified for your projects.