# Svelte Performance Monitoring Hooks

Specialized hooks for monitoring and maintaining performance in Svelte/SvelteKit applications.

## Performance Monitoring Hooks

### 1. Component Render Performance Check
Monitors component complexity and potential performance issues.

```json
{
  "hooks": {
    "post-edit": {
      "render-complexity": {
        "command": "if [[ \"$FILE_PATH\" =~ \\.svelte$ ]]; then echo \"Analyzing component complexity...\"; grep -c '{#each' \"$FILE_PATH\" | awk '{if($1>3) print \"⚠️  Multiple each blocks detected. Consider virtualization.\"}'; grep -c '$effect' \"$FILE_PATH\" | awk '{if($1>5) print \"⚠️  Many effects detected. Review for optimization.\"}'; fi",
        "description": "Checks for potential render performance issues",
        "blocking": false
      }
    }
  }
}
```

### 2. Bundle Size Impact Analysis
Tracks the impact of changes on bundle size.

```bash
#!/bin/bash
# Save as .claude/scripts/bundle-check.sh

BEFORE_SIZE=$(du -b dist/app.js 2>/dev/null | cut -f1 || echo 0)
npm run build -- --silent
AFTER_SIZE=$(du -b dist/app.js 2>/dev/null | cut -f1 || echo 0)
DIFF=$((AFTER_SIZE - BEFORE_SIZE))

if [ $DIFF -gt 10000 ]; then
    echo "⚠️  Bundle size increased by $(($DIFF / 1024))KB"
elif [ $DIFF -lt -10000 ]; then
    echo "✅ Bundle size decreased by $((-$DIFF / 1024))KB"
fi
```

```json
{
  "hooks": {
    "post-edit": {
      "bundle-impact": {
        "command": "if [[ \"$FILE_PATH\" =~ \\.(svelte|ts|js)$ ]]; then .claude/scripts/bundle-check.sh; fi",
        "description": "Analyzes bundle size impact",
        "blocking": false
      }
    }
  }
}
```

### 3. Reactive Statement Optimization Check
Identifies potentially expensive reactive statements.

```json
{
  "hooks": {
    "post-edit": {
      "reactive-optimization": {
        "command": "if [[ \"$FILE_PATH\" =~ \\.svelte$ ]]; then grep -n '\\$:.*\\.filter\\|\\$:.*\\.map\\|\\$:.*\\.reduce' \"$FILE_PATH\" | while read -r line; do echo \"⚠️  Line $line: Consider using $derived for expensive computations\"; done; fi",
        "description": "Checks for expensive reactive statements",
        "blocking": false
      }
    }
  }
}
```

### 4. Image Optimization Reminder
Ensures images are optimized when added to components.

```json
{
  "hooks": {
    "post-edit": {
      "image-optimization": {
        "command": "if [[ \"$FILE_PATH\" =~ \\.svelte$ ]] && grep -qE '<img|src=.*\\.(png|jpg|jpeg)' \"$FILE_PATH\"; then echo '📸 Remember to: 1) Use WebP format, 2) Add loading=\"lazy\", 3) Include width/height attributes'; fi",
        "description": "Reminds about image optimization",
        "blocking": false
      }
    }
  }
}
```

### 5. Memory Leak Detection
Checks for common memory leak patterns.

```json
{
  "hooks": {
    "post-edit": {
      "memory-leak-check": {
        "command": "if [[ \"$FILE_PATH\" =~ \\.svelte$ ]]; then grep -n 'addEventListener\\|setInterval\\|setTimeout' \"$FILE_PATH\" | grep -v 'removeEventListener\\|clearInterval\\|clearTimeout' && echo '⚠️  Ensure cleanup in onDestroy' || true; fi",
        "description": "Checks for potential memory leaks",
        "blocking": false
      }
    }
  }
}
```

### 6. Large Data Structure Warning
Warns about large data structures that should use $state.raw.

```json
{
  "hooks": {
    "post-edit": {
      "large-state-check": {
        "command": "if [[ \"$FILE_PATH\" =~ \\.svelte$ ]]; then awk '/\\$state\\(/ {getline; if(/Array\\(|\\[.*\\]/ && length($0) > 100) print \"⚠️  Consider using $state.raw() for large arrays\"}' \"$FILE_PATH\"; fi",
        "description": "Suggests $state.raw for large data",
        "blocking": false
      }
    }
  }
}
```

### 7. CSS Performance Check
Monitors CSS complexity and performance.

```json
{
  "hooks": {
    "post-edit": {
      "css-performance": {
        "command": "if [[ \"$FILE_PATH\" =~ \\.svelte$ ]]; then echo \"CSS Analysis:\"; grep -c ':global' \"$FILE_PATH\" | awk '{if($1>5) print \"⚠️  Many global styles. Consider scoped styles.\"}'; grep -c '!important' \"$FILE_PATH\" | awk '{if($1>0) print \"⚠️  Avoid !important for better performance.\"}'; fi",
        "description": "Analyzes CSS performance impact",
        "blocking": false
      }
    }
  }
}
```

## Lighthouse Integration Hook

### 8. Automated Lighthouse Check
Runs Lighthouse on affected routes after changes.

```bash
#!/bin/bash
# Save as .claude/scripts/lighthouse-check.sh

if [[ "$1" =~ routes/.*\+page\.svelte$ ]]; then
    ROUTE=$(echo "$1" | sed -E 's|src/routes||; s|/\+page\.svelte$||; s|\[([^]]+)\]|test-\1|g')
    
    # Start dev server in background
    npm run dev &
    DEV_PID=$!
    sleep 5
    
    # Run Lighthouse
    npx lighthouse "http://localhost:5173$ROUTE" \
        --output=json \
        --quiet \
        --chrome-flags="--headless" \
        --only-categories=performance \
        | jq -r '.categories.performance.score' \
        | awk '{
            score = $1 * 100;
            if (score < 50) print "❌ Performance score: " score "/100";
            else if (score < 90) print "⚠️  Performance score: " score "/100";
            else print "✅ Performance score: " score "/100";
        }'
    
    # Cleanup
    kill $DEV_PID 2>/dev/null
fi
```

```json
{
  "hooks": {
    "post-edit": {
      "lighthouse-perf": {
        "command": ".claude/scripts/lighthouse-check.sh \"$FILE_PATH\"",
        "description": "Runs Lighthouse performance check",
        "blocking": false
      }
    }
  }
}
```

## Complete Performance Hook Set

```json
{
  "hooks": {
    "post-edit": {
      "perf-suite": {
        "command": "if [[ \"$FILE_PATH\" =~ \\.(svelte|ts)$ ]]; then echo '🔍 Performance Analysis:'; grep -c '$state(' \"$FILE_PATH\" | awk '{if($1>20) print \"  ⚠️  Many state variables (\"$1\")\"}'; grep -E 'filter\\(|map\\(|reduce\\(' \"$FILE_PATH\" | wc -l | awk '{if($1>10) print \"  ⚠️  Many array operations (\"$1\")\"}'; grep -c '$effect' \"$FILE_PATH\" | awk '{if($1>5) print \"  ⚠️  Many effects (\"$1\")\"}'; fi",
        "description": "Comprehensive performance analysis",
        "blocking": false
      }
    }
  }
}
```