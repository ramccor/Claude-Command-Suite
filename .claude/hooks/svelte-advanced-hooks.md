# Svelte Advanced Integration Hooks

Advanced hooks for CI/CD integration, monitoring, and sophisticated development workflows.

## CI/CD Integration Hooks

### 1. Pre-Deploy Validation Suite
Comprehensive validation before deployment.

```bash
#!/bin/bash
# Save as .claude/scripts/pre-deploy-check.sh

echo "🚀 Pre-deployment validation..."

# Type checking
if ! npx tsc --noEmit; then
    echo "❌ TypeScript errors found"
    exit 1
fi

# Svelte checking
if ! npx sv check; then
    echo "❌ Svelte errors found"
    exit 1
fi

# Tests
if ! npm test -- --run; then
    echo "❌ Tests failed"
    exit 1
fi

# Build
if ! npm run build; then
    echo "❌ Build failed"
    exit 1
fi

# Bundle size check
MAX_SIZE=500000  # 500KB
ACTUAL_SIZE=$(du -b dist/app.js | cut -f1)
if [ $ACTUAL_SIZE -gt $MAX_SIZE ]; then
    echo "❌ Bundle too large: ${ACTUAL_SIZE} bytes"
    exit 1
fi

echo "✅ All pre-deployment checks passed!"
```

```json
{
  "hooks": {
    "pre-commit": {
      "deploy-ready": {
        "command": ".claude/scripts/pre-deploy-check.sh",
        "description": "Full deployment validation",
        "blocking": true,
        "blockingMessage": "Fix all issues before deploying"
      }
    }
  }
}
```

### 2. Semantic Version Suggester
Suggests version bumps based on changes.

```json
{
  "hooks": {
    "pre-commit": {
      "version-suggest": {
        "command": "if git diff --cached --name-only | grep -E '\\.(svelte|ts|js)$' > /dev/null; then BREAKING=$(git diff --cached | grep -c '^-.*export' || true); FEATURES=$(git diff --cached | grep -c '^+.*export' || true); if [ $BREAKING -gt 0 ]; then echo '💔 Breaking changes detected - suggest MAJOR version bump'; elif [ $FEATURES -gt 0 ]; then echo '✨ New features detected - suggest MINOR version bump'; else echo '🔧 Bug fixes/improvements - suggest PATCH version bump'; fi; fi",
        "description": "Suggests semantic version bump",
        "blocking": false
      }
    }
  }
}
```

## Monitoring and Analytics Hooks

### 3. Component Performance Tracking
Tracks component render performance over time.

```bash
#!/bin/bash
# Save as .claude/scripts/perf-tracker.sh

PERF_LOG=".claude/performance.log"
COMPONENT=$(basename "$1" .svelte)

# Run performance test
RESULT=$(npm run test:performance -- --component="$COMPONENT" 2>/dev/null | grep "Render time" | awk '{print $3}')

if [ -n "$RESULT" ]; then
    echo "[$(date +%Y-%m-%d_%H:%M:%S)] $COMPONENT: ${RESULT}ms" >> "$PERF_LOG"
    
    # Check if performance degraded
    PREV=$(grep "$COMPONENT:" "$PERF_LOG" | tail -2 | head -1 | awk -F': ' '{print $2}' | sed 's/ms//')
    if [ -n "$PREV" ]; then
        DIFF=$(echo "$RESULT - $PREV" | bc)
        if (( $(echo "$DIFF > 10" | bc -l) )); then
            echo "⚠️  Performance regression: ${COMPONENT} render time increased by ${DIFF}ms"
        fi
    fi
fi
```

```json
{
  "hooks": {
    "post-edit": {
      "perf-track": {
        "command": "if [[ \"$FILE_PATH\" =~ \\.svelte$ ]]; then .claude/scripts/perf-tracker.sh \"$FILE_PATH\"; fi",
        "description": "Tracks component performance",
        "blocking": false
      }
    }
  }
}
```

### 4. Error Tracking Integration
Integrates with error tracking services.

```json
{
  "hooks": {
    "post-edit": {
      "error-tracking": {
        "command": "if [[ \"$FILE_PATH\" =~ \\.(svelte|ts|js)$ ]] && grep -E 'throw new Error|console\\.error' \"$FILE_PATH\" > /dev/null; then echo '🚨 Error handling detected - ensure proper error tracking:'; echo '  - Wrap in try/catch'; echo '  - Report to Sentry/Rollbar'; echo '  - Add user-friendly fallback'; fi",
        "description": "Reminds about error tracking",
        "blocking": false
      }
    }
  }
}
```

## Database and API Integration Hooks

### 5. GraphQL Schema Sync
Ensures GraphQL queries match schema.

```json
{
  "hooks": {
    "post-edit": {
      "graphql-validate": {
        "command": "if [[ \"$FILE_PATH\" =~ \\.(svelte|ts|js)$ ]] && grep -q 'gql\\`\\|graphql(' \"$FILE_PATH\"; then npx graphql-codegen --check || echo '❌ GraphQL schema mismatch'; fi",
        "description": "Validates GraphQL queries",
        "blocking": false
      }
    }
  }
}
```

### 6. API Contract Validation
Validates API calls against OpenAPI spec.

```bash
#!/bin/bash
# Save as .claude/scripts/api-contract-check.sh

if grep -E 'fetch\\(|\\$app/data' "$1" > /dev/null; then
    # Extract API endpoints
    ENDPOINTS=$(grep -oE '(fetch\\([\"'\"']|url: [\"'\"'])[^\"'\"']+' "$1" | sed 's/fetch(.//' | sed 's/url: .//')
    
    for endpoint in $ENDPOINTS; do
        if [[ $endpoint =~ ^/api/ ]]; then
            # Validate against OpenAPI spec
            npx openapi-validator validate "$endpoint" --spec=./openapi.yaml 2>/dev/null || \
                echo "⚠️  API endpoint not in spec: $endpoint"
        fi
    done
fi
```

```json
{
  "hooks": {
    "post-edit": {
      "api-contract": {
        "command": ".claude/scripts/api-contract-check.sh \"$FILE_PATH\"",
        "description": "Validates API usage against contract",
        "blocking": false
      }
    }
  }
}
```

## Security and Compliance Hooks

### 7. GDPR Compliance Check
Checks for personal data handling.

```json
{
  "hooks": {
    "post-edit": {
      "gdpr-check": {
        "command": "if [[ \"$FILE_PATH\" =~ \\.(svelte|ts|js)$ ]] && grep -iE 'email|phone|address|birth|ssn|passport' \"$FILE_PATH\" > /dev/null; then echo '🔒 Personal data detected - ensure GDPR compliance:'; echo '  - Add consent mechanisms'; echo '  - Implement data retention policies'; echo '  - Enable data export/deletion'; fi",
        "description": "GDPR compliance reminder",
        "blocking": false
      }
    }
  }
}
```

### 8. License Header Enforcement
Ensures all files have proper license headers.

```json
{
  "hooks": {
    "post-write": {
      "license-header": {
        "command": "if [[ \"$FILE_PATH\" =~ \\.(svelte|ts|js)$ ]] && ! head -5 \"$FILE_PATH\" | grep -q 'Copyright\\|License'; then sed -i '1i/*\\n * Copyright (c) $(date +%Y) Your Company\\n * Licensed under MIT License\\n */\\n' \"$FILE_PATH\"; echo '📄 Added license header'; fi",
        "description": "Adds license headers",
        "blocking": false
      }
    }
  }
}
```

## Development Environment Hooks

### 9. Environment Variable Validator
Ensures required environment variables are set.

```bash
#!/bin/bash
# Save as .claude/scripts/env-check.sh

REQUIRED_VARS=(
    "PUBLIC_API_URL"
    "PUBLIC_APP_NAME"
    "PUBLIC_FEATURE_FLAGS"
)

MISSING=()
for var in "${REQUIRED_VARS[@]}"; do
    if [[ -z "${!var}" ]]; then
        MISSING+=("$var")
    fi
done

if [ ${#MISSING[@]} -gt 0 ]; then
    echo "❌ Missing environment variables:"
    printf '  - %s\n' "${MISSING[@]}"
    echo "Add them to .env or .env.local"
    exit 1
fi
```

```json
{
  "hooks": {
    "pre-edit": {
      "env-check": {
        "command": "if [[ \"$FILE_PATH\" =~ ^src/ ]]; then .claude/scripts/env-check.sh; fi",
        "description": "Validates environment setup",
        "blocking": true,
        "blockingMessage": "Set up required environment variables"
      }
    }
  }
}
```

### 10. Docker Integration
Ensures Docker environment is in sync.

```json
{
  "hooks": {
    "post-edit": {
      "docker-sync": {
        "command": "if [[ \"$FILE_PATH\" = \"package.json\" ]] && [ -f Dockerfile ]; then echo '🐳 package.json changed - remember to:'; echo '  - Rebuild Docker image'; echo '  - Update docker-compose.yml if needed'; echo '  - Test in container environment'; fi",
        "description": "Docker sync reminder",
        "blocking": false
      }
    }
  }
}
```

## Feature Flag Integration

### 11. Feature Flag Usage Tracker
Tracks and validates feature flag usage.

```json
{
  "hooks": {
    "post-edit": {
      "feature-flags": {
        "command": "if [[ \"$FILE_PATH\" =~ \\.(svelte|ts|js)$ ]] && grep -E 'featureFlag\\(|PUBLIC_FEATURE_' \"$FILE_PATH\" > /dev/null; then FLAGS=$(grep -oE 'featureFlag\\([\"'\"'][^\"'\"']+|PUBLIC_FEATURE_[A-Z_]+' \"$FILE_PATH\" | sort -u); echo '🚩 Feature flags in use:'; echo \"$FLAGS\" | sed 's/^/  - /'; echo 'Ensure flags are documented in README'; fi",
        "description": "Tracks feature flag usage",
        "blocking": false
      }
    }
  }
}
```

## Database Migration Hooks

### 12. Migration Reminder
Reminds to create migrations for schema changes.

```json
{
  "hooks": {
    "post-edit": {
      "migration-check": {
        "command": "if [[ \"$FILE_PATH\" =~ schema\\.(prisma|sql)$ ]] || [[ \"$FILE_PATH\" =~ migrations/ ]]; then echo '🗄️  Database schema changed - remember to:'; echo '  1. Create migration: npm run db:migrate:create'; echo '  2. Apply migration: npm run db:migrate:up'; echo '  3. Update seed data if needed'; fi",
        "description": "Database migration reminder",
        "blocking": false
      }
    }
  }
}
```

## Internationalization Hooks

### 13. i18n Key Validator
Ensures all text is internationalized.

```json
{
  "hooks": {
    "post-edit": {
      "i18n-check": {
        "command": "if [[ \"$FILE_PATH\" =~ \\.svelte$ ]]; then HARDCODED=$(grep -E '>\\s*[A-Z][a-zA-Z\\s]+\\s*<' \"$FILE_PATH\" | grep -v '{\\$t\\|{t(' | wc -l); if [ $HARDCODED -gt 0 ]; then echo \"🌍 Found $HARDCODED potentially untranslated strings\"; fi; fi",
        "description": "Checks for untranslated text",
        "blocking": false
      }
    }
  }
}
```

## Complete Advanced Setup

```json
{
  "hooks": {
    "post-edit": {
      "advanced-suite": {
        "command": "if [[ \"$FILE_PATH\" =~ \\.(svelte|ts|js)$ ]]; then echo '🔍 Advanced checks:'; grep -q 'TODO\\|FIXME' \"$FILE_PATH\" && echo '  📝 TODOs found'; grep -E 'fetch\\(|\\$app/data' \"$FILE_PATH\" > /dev/null && echo '  🌐 API calls detected'; grep -iE 'email|phone|address' \"$FILE_PATH\" > /dev/null && echo '  🔒 Personal data handling'; fi",
        "description": "Comprehensive advanced checks",
        "blocking": false
      }
    }
  }
}
```