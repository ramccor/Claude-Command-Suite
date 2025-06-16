# Claude Code Custom Slash Commands

![Total Commands](https://img.shields.io/badge/Total%20Commands-81%20and%20growing!-brightgreen?style=for-the-badge)
<!-- Dynamic badge (will work after PR merge): ![Total Commands](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/qdhenry/Claude-Command-Suite/main/.github/badges/command-count.json&style=for-the-badge) -->

> **Inspired by Anthropic's Claude Code Best Practices**: These custom commands are designed following the principles and recommendations outlined in [Anthropic's Claude Code Best Practices](https://www.anthropic.com/engineering/claude-code-best-practices) to maximize effectiveness and provide structured workflows for software development.

Custom slash commands for Claude Code that provide structured workflows for common software development tasks. Get comprehensive analysis, feature development, and code maintenance with simple `/project:command-name` commands.

## Quick Start

1. **Install the commands:**
   ```bash
   git clone https://github.com/qdhenry/Claude-Command-Suite.git
   cd Claude-Command-Suite
   chmod +x install.sh
   ./install.sh
   ```

2. **Start using commands:**
   ```bash
   claude code
   /project:code-review           # Review your entire codebase
   /project:create-feature login  # Build a new feature
   /project:security-audit        # Check for security issues
   ```

## Available Commands

🚀 **81 Total Commands and Growing!** - From code analysis to project management, we've got you covered.

### 🔍 Analysis Commands
- `/project:ultra-think` - Engage ultra-deep thinking mode for complex problem-solving
- `/project:architecture-review` - Analyze system architecture and design patterns
- `/project:code-review` - Complete code quality and security review
- `/project:security-audit` - Security vulnerability assessment
- `/project:performance-audit` - Find performance bottlenecks
- `/project:dependency-audit` - Check dependency security and updates
- `/project:explain-code` - Explain complex code sections and architecture
- `/project:test-coverage` - Analyze and improve test coverage

### 🛠️ Development Commands
- `/project:create-feature` - Complete feature development workflow
- `/project:fix-issue` - Structured GitHub issue resolution
- `/project:refactor-code` - Safe refactoring with testing
- `/project:debug-error` - Systematic debugging approach
- `/project:optimize-build` - Build system improvements
- `/project:optimize-bundle-size` - Reduce application bundle size
- `/project:write-tests` - Generate comprehensive test suites

### 🚀 Project Setup Commands
- `/project:init-project [type] [framework]` - Initialize new project with industry best practices
- `/project:setup-monorepo [tool]` - Configure monorepo structure with workspace management
- `/project:add-package [name] [type]` - Add new package/module with proper structure
- `/project:setup-development-environment` - Configure development environment and tools
- `/project:migrate-to-typescript` - Convert JavaScript project to TypeScript
- `/project:setup-linting` - Configure code linting and quality tools
- `/project:setup-formatting` - Set up code formatting standards
- `/project:ci-setup` - Configure continuous integration pipelines

### 🧪 Testing Commands
- `/project:setup-comprehensive-testing` - Set up complete testing stack (unit, integration, e2e, visual)
- `/project:generate-test-cases [file/function]` - Auto-generate test cases for existing code
- `/project:setup-visual-testing` - Configure visual regression testing for UI components
- `/project:add-property-based-testing` - Set up property-based testing framework
- `/project:setup-load-testing` - Configure performance and load testing infrastructure
- `/project:add-mutation-testing` - Set up mutation testing to verify test quality
- `/project:e2e-setup` - Configure end-to-end testing infrastructure

### 📚 Documentation Commands
- `/project:generate-api-documentation` - Auto-generate comprehensive API documentation
- `/project:create-architecture-documentation` - Generate system architecture diagrams and docs
- `/project:create-onboarding-guide` - Generate comprehensive getting-started guide
- `/project:doc-api` - Create detailed API documentation
- `/project:add-changelog` - Set up automated changelog generation
- `/project:migration-guide` - Create migration guides for major changes
- `/project:troubleshooting-guide` - Generate troubleshooting documentation

### 🔒 Security Commands  
- `/project:security-hardening` - Apply comprehensive security best practices
- `/project:add-authentication-system` - Implement robust authentication and authorization
- `/project:setup-rate-limiting` - Configure API rate limiting and protection

### 🐳 DevOps Commands
- `/project:containerize-application` - Create optimal Docker configuration
- `/project:setup-kubernetes-deployment` - Generate Kubernetes manifests for deployment
- `/project:setup-monitoring-observability` - Add comprehensive monitoring, logging, and tracing
- `/project:add-performance-monitoring` - Implement detailed performance monitoring
- `/project:setup-cdn-optimization` - Configure CDN and asset optimization
- `/project:hotfix-deploy` - Deploy critical fixes with validation
- `/project:rollback-deploy` - Safely rollback deployments
- `/project:prepare-release` - Prepare production releases with validation
- `/project:clean-branches` - Clean up merged and stale branches

### 🗄️ Database Commands
- `/project:design-database-schema` - Design and validate database schemas
- `/project:create-database-migrations` - Generate safe database migrations
- `/project:optimize-database-performance` - Optimize database queries and performance

### 🌐 API Commands
- `/project:design-rest-api` - Design RESTful API endpoints
- `/project:implement-graphql-api` - Implement GraphQL API layer
- `/project:implement-caching-strategy` - Add intelligent caching systems

### 🔄 Maintenance Commands
- `/project:modernize-deps` - Update and modernize dependencies safely

### 📋 Project Management Commands

#### Sprint Planning & Analysis
- `/project:sprint-planning` - Analyze current Linear tasks and help plan sprints with optimal capacity allocation
- `/project:standup-report` - Generate daily standup reports from git commits and Linear task updates
- `/project:project-health-check` - Assess project health with metrics on velocity, quality, and team performance
- `/project:retrospective-analyzer` - Facilitate sprint retrospectives with data-driven insights and action items
- `/project:milestone-tracker` - Track project milestones and deliverables with predictive analytics

#### Task Management
- `/project:project-to-linear` - Analyze project requirements and create comprehensive task lists in Linear
- `/project:task-from-pr` - Convert pull requests into Linear tasks with automatic metadata extraction
- `/project:dependency-mapper` - Visualize and manage task dependencies with critical path analysis
- `/project:estimate-assistant` - Provide data-driven task estimation based on historical velocity
- `/project:code-to-task` - Generate tasks from TODO/FIXME comments and technical debt markers
- `/project:team-workload-balancer` - Optimize team task distribution based on capacity and expertise

#### GitHub-Linear Synchronization
- `/project:sync-issues-to-linear` - One-way sync GitHub Issues to Linear with field mapping
- `/project:sync-linear-to-issues` - One-way sync Linear tasks to GitHub Issues  
- `/project:bidirectional-sync` - Full two-way synchronization with conflict resolution
- `/project:issue-to-linear-task` - Convert specific GitHub issue to Linear task
- `/project:linear-task-to-issue` - Convert specific Linear task to GitHub issue
- `/project:sync-pr-to-task` - Link pull requests with Linear tasks and update status
- `/project:sync-status` - Monitor synchronization health and consistency
- `/project:bulk-import-issues` - Mass import GitHub issues to Linear with progress tracking
- `/project:issue-triage` - Intelligently triage GitHub issues into Linear projects
- `/project:sync-automation-setup` - Configure automated synchronization with webhooks

#### Advanced Synchronization
- `/project:cross-reference-manager` - Maintain and verify references between GitHub and Linear
- `/project:sync-conflict-resolver` - Handle synchronization conflicts with smart resolution
- `/project:migration-assistant` - Enterprise-ready migration between GitHub and Linear

## How It Works

Commands are available as `/project:command-name` in Claude Code. Each command follows a structured workflow that Claude executes automatically, ensuring consistent and thorough results across different projects.

**Example workflow:**
- `/project:code-review` analyzes your entire codebase for quality, security, and performance
- `/project:create-feature dashboard` plans, implements, and tests a new dashboard feature
- `/project:fix-issue 123` systematically resolves GitHub issue #123 with testing

## Common Workflows

**New Feature Development:**
```bash
/project:code-review                    # Assess current state
/project:create-feature user-dashboard  # Implement feature
/project:security-audit                 # Verify security
```

**Bug Fixing:**
```bash
/project:fix-issue 456                  # Fix the specific issue
/project:code-review                    # Verify fix quality
```

**Code Maintenance:**
```bash
/project:dependency-audit               # Check for outdated dependencies
/project:performance-audit              # Identify bottlenecks
/project:refactor-code legacy-module    # Improve problematic areas
```

## Need More Details?

- **[Installation Guide](docs/INSTALLATION.md)** - Detailed installation methods, troubleshooting, and configuration
- **[Customization Guide](docs/CUSTOMIZATION.md)** - How to modify commands and create new ones
- **[Development Guide](docs/DEVELOPMENT.md)** - Contributing, testing, and best practices

## Contributing

This repository exists to collect and share useful slash commands for Claude Code. **Contributions are welcome!**

### Ways to Contribute

- **Share new commands** - Create commands for workflows you find useful
- **Improve existing commands** - Enhance commands with better practices
- **Add language-specific variants** - Adapt commands for specific tech stacks
- **Fix bugs** - Resolve issues with existing commands
- **Improve documentation** - Make guides clearer and more helpful

### Quick Contribution

1. Fork this repository
2. Add or modify commands in `.claude/commands/`
3. Test your changes thoroughly
4. Submit a pull request with a clear description

See **[Development Guide](docs/DEVELOPMENT.md)** for detailed contribution guidelines, testing practices, and quality standards.

## Automated Changelog

This project features automated changelog generation to track command additions and updates:

### 🤖 **Automatic Updates**
- **GitHub Actions Integration**: Automatically detects when new commands are added
- **Smart Detection**: Tracks both new command files and modifications to existing ones
- **Formatted Entries**: Generates properly formatted changelog entries with command descriptions
- **PR Comments**: Provides summary comments on pull requests with changelog updates

### 📝 **Manual Updates**
For manual changelog updates, use the provided script:
```bash
./scripts/update-changelog.sh
```

This script will:
- Scan all command files in `.claude/commands/`
- Extract command names and descriptions
- Update `CHANGELOG.md` with categorized command listings
- Create a backup of the existing changelog

### 📊 **Changelog Features**
- **Command Categorization**: Automatically groups commands by type (Analysis, Development, Testing, etc.)
- **Total Count Tracking**: Maintains accurate count of total available commands  
- **Description Extraction**: Pulls descriptions directly from command files
- **Backup Safety**: Creates backups before making changes

## Requirements

- Claude Code version 1.0 or later
- Commands work with any programming language or framework

---

*Inspired by [Anthropic's Claude Code Best Practices](https://www.anthropic.com/engineering/claude-code-best-practices)*