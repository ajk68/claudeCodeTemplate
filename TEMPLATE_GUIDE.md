# TEMPLATE_GUIDE.md

# Claude Code Development Template

> ⚠️ **Experimental Workflow**: This guide documents my evolving approach to AI-assisted development. I'm learning from many developers in the community and constantly refining these patterns. Your mileage may vary - please adapt to your needs and share what works for you!

An experimental template exploring how to create a more structured workflow between developers and Claude, based on patterns I've learned from the community.

## What This Template Provides

### 🎯 Context Management Experiments
- **My observation**: AI sometimes gets lost in large codebases, context window fills with irrelevant information
- **What I'm trying**: Tiered context generation and smart delegation to specialized AI models
- **Early results**: Seems to help Claude stay more focused, but still iterating

### 🔍 Reality-Grounding Attempts
- **What I've noticed**: AI can hallucinate functions, patterns, and "best practices" that don't exist
- **My approach**: Testing multiple verification layers - real files, real docs, real database schemas
- **Hope**: AI suggestions based more on what actually exists, not what it imagines

### 🔄 Quality Feedback Exploration
- **My concern**: I've seen bugs compound and bad patterns proliferate over time
- **Experiment**: Automated hooks, linting, and verification at various steps
- **Goal**: Catch problems earlier in the development process

### 🛠️ Workflow Specialization Tests
- **My experience**: One-size-fits-all AI interactions often lead to confusion
- **What I'm testing**: Purpose-built commands for each development phase
- **Aspiration**: Clearer progression from idea → planning → implementation → shipping

### 📊 Centralized Logging Experiments
- **My frustration**: Scattered logs across terminals, browser consoles, and files made debugging hard
- **What I'm trying**: A unified logging system that combines all sources with AI analysis
- **Hoping for**: Single source of truth for debugging with AI-powered log analysis

## Quick Start

### Method 1: GitHub Template (Recommended)
1. **Click "Use this template"** button on GitHub
2. **Clone your new repository**:
   ```bash
   git clone <your-new-repo-url> my-project
   cd my-project
   ```
3. **Run the setup wizard**:
   ```bash
   make setup   # Runs interactive setup
   ```

### Method 2: Manual Clone
1. **Clone the template**:
   ```bash
   git clone https://github.com/ajk68/claudeCodeTemplate my-project
   cd my-project
   ```
2. **Run setup** (will detect and protect template):
   ```bash
   make setup   # Will disconnect from template repo
   ```

### After Setup
1. **Start Claude Code**:
   ```bash
   claude
   ```
2. **Try a workflow command**:
   ```
   /status              # See current project state
   /brainstorm          # Start exploring an idea
   /implement           # Execute code changes
   ```

## Key Components

### 📁 Directory Structure
```
.claude/
├── commands/        # Slash commands for Claude workflows
├── hooks/           # Local project hooks (optional)
└── settings.json    # Project-specific Claude settings

make/
├── ai.mk           # AI delegation commands
├── context.mk      # Context generation commands
├── logging.mk      # Centralized logging commands
├── quality.mk      # Testing and linting
└── tools/          # Development utilities
    └── shoreman.sh # Process manager (from mitsuhiko/minibb)

logs/
├── frontend/       # Browser console logs
├── backend/        # Server application logs
└── combined/       # Unified process output


~/.claude/          # User-level configuration (not in template)
├── hooks/          # Personal automation scripts
└── settings.json   # Personal Claude settings
```

### 🔧 Make Commands

**Context & Analysis**:
- `make generate-context-python` - Python files only (~40K tokens)
- `make generate-context-small` - Compressed overview (~60K tokens)
- `make ai-analyze-project` - Full project analysis with AI
- `make code-search` - Fast pattern searching

**Quality & Testing**:
- `make test` - Run test suite
- `make lint` - Check code quality
- `make format` - Auto-format code

**Development**:
- `make project-status` - Current state summary
- `make dev` - Run all services with unified logging
- `make logs-watch` - Watch combined logs in real-time
- `make analyze-logs` - AI-powered log analysis
- `make review-diff` - Review pending changes

### 💬 Workflow Commands

**Strategic Planning**:
- `/brainstorm` - Explore ideas with data-driven insights
- `/architect` - Create technical implementation plans

**Execution**:
- `/implement` - Write code (handles both features and fixes)
- `/test` - Verify functionality
- `/ship` - Finalize and commit changes

**Support**:
- `/status` - Quick orientation without context pollution
- `/review` - Get peer-review style feedback
- `/document` - Update documentation to match reality

## Core Principles

### 1. Context Preservation
- Main Claude instance stays focused on the task
- Information gathering delegated to specialized agents
- Smart model selection based on content size

### 2. Reality Anchoring
- Always read actual files, never rely on memory
- Check real documentation via Context7
- Verify against actual database schemas
- Research current practices via Perplexity

### 3. Continuous Verification
- Automated formatting and linting after edits
- Test execution at multiple checkpoints
- Smart blockers prevent common mistakes
- Human approval required for major decisions

### 4. Pragmatic Constraints
- Prefer modifying existing code over creating new files
- No abstractions without 3+ existing uses
- No mocks or fixtures - real data only
- Clear decision points, no implicit assumptions

## Customization Guide

### Setting Up Centralized Logging
1. **Configure your Procfile** - Copy `Procfile.example` to `Procfile` and list your services
2. **Frontend setup** - The template includes vite-console-forward-plugin pre-configured
3. **Run services** - Use `make dev` to start all processes with unified logging
4. **Monitor logs** - Use `make logs-watch` for real-time monitoring

**Attribution**: Process management via shoreman.sh (in make/tools/) from @mitsuhiko's minibb project. I've been inspired by mitsuhiko's workflows and many others in the community who share their development practices.

### Adding Project Commands

#### Slash Commands
Create markdown files in `.claude/commands/`:
```bash
echo "Your custom prompt here" > .claude/commands/my-command.md
# Use as: /my-command
```

#### Make Commands
Add project-specific make targets to `make/project.mk`:
```makefile
# Example: Development server
.PHONY: dev-server
dev-server: ## Start development server
	uv run python manage.py runserver

# Example: Database migrations
.PHONY: migrate
migrate: ## Run database migrations
	uv run python manage.py migrate
```

The template's `make/project.mk` file is intentionally empty - it's where you add commands specific to your project without modifying the core template files.

### Setting Up Hooks
Configure in `.claude/settings.json`:
```json
{
  "hooks": {
    "PostToolUse": [{
      "matcher": "Write|Edit",
      "hooks": [{
        "type": "command",
        "command": "make format"
      }]
    }]
  }
}
```

### Personal Configuration
Your personal settings in `~/.claude/` (not tracked in git):
- Custom hooks for your workflow
- Personal command shortcuts
- Notification preferences

## Philosophy

This template reflects my belief that **AI is most effective as a partner, not a replacement**. I'm trying to create what I think of as a "cognitive exoskeleton" that:

- Might amplify human decision-making with AI-powered information gathering
- Could help prevent common failure modes through systematic processes
- Attempts to maintain quality through continuous verification
- Explores scaling expertise through codified practices

My goal isn't to make Claude autonomous, but to experiment with making the human-AI team more capable than either could be alone.

## Inspirations & Attribution

This workflow draws heavily from patterns I've observed and learned:

- **Process Management**: Using shoreman.sh from @mitsuhiko's minibb project
- **Context Strategies**: Inspired by discussions in the Claude Discord community
- **Make Patterns**: Learned from various open source projects
- **Logging Approach**: Adapted from @mitsuhiko's development workflows
- **Workflow Ideas**: Influenced by many developers sharing their AI-assisted development experiences

I'm grateful to all the developers who share their workflows and tools openly. This template is my attempt to synthesize what I've learned and contribute back to the community.

## Requirements

- [Claude Code](https://claude.ai/code) CLI tool
- Python with `uv` package manager
- Node.js and npm
- ripgrep (`rg`) for fast searching
- Git for version control

## Getting Help

1. Check the built-in help: `/tools` command
2. Review workflow examples in `.claude/commands/`
3. See the Makefile for all available automation

Remember: The commands and workflows are guides, not rules. Adapt them to your needs and let the template evolve with your project.

## Feedback Welcome

This template is very much a work in progress. I'm learning as I go and would love to hear:
- What patterns work in your workflow?
- What doesn't work with this approach?
- Ideas for improvement
- Your own experiments with AI-assisted development

Feel free to open issues or reach out with suggestions. We're all figuring this out together!