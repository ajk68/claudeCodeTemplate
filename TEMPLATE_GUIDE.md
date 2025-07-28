# Template Guide

Complete reference for the Claude Code Development Template.

## Overview

This template creates a structured workflow between developers and Claude. It addresses six core problems in AI-assisted development:

1. **Claude gets confused with too much context** - Smart tools keep it focused
2. **Claude makes things up** - Reality checks against actual files and docs
3. **Bugs compound over time** - Early problem detection through logging and reviews
4. **AI over-engineers** - Enforced simplicity and human approval gates
5. **Wrong tool for each job** - Specialized workflows for different phases
6. **Repeated instructions** - Pre-built commands with best practices

## Architecture

### Directory Structure

```
.claude/
├── agents/          # Specialized AI agents for different tasks
├── commands/        # Workflow prompts (/brainstorm, /implement, etc.)
│   ├── archive/     # Deprecated commands for reference
│   └── meta/        # Meta-level commands
├── hooks/           # Automation scripts (formatting, blocking bad patterns)
└── settings.json    # Project Claude configuration

make/
├── ai.mk           # AI delegation commands
├── context.mk      # Context generation  
├── logging.mk      # Centralized logging
├── quality.mk      # Testing and linting
└── tools/          # Utilities (shoreman.sh process manager)

logs/
├── frontend/       # Browser console logs
├── backend/        # Server logs
└── combined/       # Unified output
```

## Core Concepts

### 1. Keep Claude Focused on the Task

**Problem**: Claude gets confused when given too much information at once.

**Solution**: Tiered context generation based on what you need:

```bash
make generate-context-python    # Python only (~40K tokens)
make generate-context-small     # Compressed overview (~60K tokens)  
make generate-context-code      # Code without docs/tests (~70K tokens)
make generate-context-full      # Everything (~145K tokens)
```

Smart delegation automatically picks the right model:
- Small files (<70KB) → Claude (fast and focused)
- Large files (>70KB) → Gemini (handles big contexts)

### 2. Stop Claude from Making Things Up

**Problem**: Claude sometimes invents functions or patterns that don't exist.

**Solution**: Multiple verification layers:

- **mcp__repoprompt__*** - Read actual files from your project
- **mcp__context7__*** - Get real documentation for libraries
- **mcp__perplexity__*** - Search web for current best practices
- **make db-schema** - Check actual database structure
- **make code-search** - Find real patterns in your code

Commands emphasize real data: "Load only what you need - Use repoprompt for surgical file access"

### 3. Catch Problems Early

**Problem**: Bugs compound over time if not caught quickly.

**Solution**: Continuous feedback at multiple stages:

Unified logging system:
```bash
make dev           # Start with all logs in one place
make logs-watch    # Real-time monitoring
make logs-analyze  # AI analyzes patterns and issues
```

Review tools:
```bash
make review-diff    # Check changes before committing
make analyze-files  # Get structural feedback
/review            # Peer-style consultation
```

Automatic checks after every edit:
- Python formatting with ruff
- Command logging for audit trail
- Smart notifications when input needed

### 4. Keep Things Simple

**Problem**: AI tends to over-engineer and create unnecessary complexity.

**Solution**: Built-in constraints and approval gates:

Smart blockers prevent:
- Creating duplicate files (`file_v2.py`, `file_new.py`)
- Using outdated commands (`pip` → `uv`)
- Rewriting without permission

Human approval required for:
- Architectural plans (coordinator will pause for approval)
- Major refactoring (system-analyst presents ROI)
- Creating new abstractions

Core principles enforced:
- "No abstractions without 3+ existing uses"
- "Best code is no code"
- "Modify existing code over creating new"

### 5. Right Tool for Each Job

**Problem**: One AI trying to do everything leads to confusion.

**Solution**: Specialized AI agents and focused commands:

#### AI Agents (Automatic Specialization)
- **coordinator** - Coordinates complex multi-step tasks
- **system-analyst** - Understands codebase patterns and structure
- **developer** - Executes code changes with precision
- **analyst** - Plans implementation steps before coding
- **searcher** - Searches and analyzes code intelligently
- **documenter** - Manages project knowledge over time
- **documentation-writer** - Maintains evergreen documentation
- **tester** - Pragmatic testing focused on high-impact scenarios
- **reviewer** - Peer review observations
- **quality-gate** - Final deployment checks

#### Active Commands
- `/brainstorm` - Explore problems using coordinator agent
- `/implement` - Execute focused implementation tasks
- `/project-status` - Get oriented without context pollution
- `/fix` - Debug and resolve issues systematically

#### Archived Commands (moved to .claude/commands/archive/)
- `/PRD`, `/architect`, `/test`, `/review`, `/ship`, `/document`, `/tools`, `/refactor`
- These workflows are now handled by specialized agents

### 6. Make Collaboration Efficient

**Problem**: Repeating instructions wastes time and causes errors.

**Solution**: Pre-built commands and automation:

Each command includes:
- Clear steps and best practices
- Consistent workflow patterns
- No need to repeat instructions

Automation handles repetitive tasks:
```bash
make project-status      # Quick summary
make ai-analyze-project  # Full analysis
make test               # Run all tests
```

Clear human-AI roles:
- You decide WHAT to build (product intuition)
- Claude handles HOW to build it (implementation)
- Defined checkpoints for your input

## Command Reference

### Make Commands

**Context Generation**
- `generate-context-full` - Complete codebase
- `generate-context-code` - Code only
- `generate-context-python` - Python files
- `generate-context-small` - Compressed
- `generate-context-from-files FILES="..."` - Specific files

**AI Analysis**
- `ai-query PROMPT="..." [FILE=...]` - Smart model selection
- `ai-analyze-project PROMPT="..." SCOPE=...` - Full analysis
- `analyze-file FILE="..."` - Single file review
- `review-diff` - Check git changes
- `project-status` - Current state summary

**Quality & Testing**
- `test` - Run tests
- `test-coverage` - With coverage report
- `lint` - Check issues
- `lint-fix` - Auto-fix safe issues
- `format` - Format code

**Development**
- `dev` - Start all services
- `code-search PATTERN="..."` - Fast search
- `db-schema [TABLE=...]` - Database info
- `clean` - Remove caches

### Workflow Commands

Run these inside Claude Code:

**Active Commands**
- `/brainstorm` - Explore ideas with AI coordinator
- `/implement` - Execute implementation with smart agents
- `/project-status` - Get current state without context pollution
- `/fix` - Debug issues systematically

**Agent Invocation**
Agents work proactively based on your task, or invoke explicitly:
```
> Use the system-analyst to understand the caching system
> Have the analyst create implementation steps for the new feature
```

## Customization

### Using the Install Script

The `install.py` script allows selective installation of framework components:

```bash
# Install all components
./install.py

# Install specific components
./install.py agents commands

# Available components:
# - agents: AI agent definitions
# - commands: Workflow commands
# - hooks: Automation scripts
# - settings: Claude configuration
# - makefile: Make commands
# - docs: Documentation
# - claudemd: CLAUDE.md file
```

### Add Project Commands

Create new workflow commands:
```bash
echo "Your prompt here" > .claude/commands/my-command.md
# Use as: /my-command
```

Add Make targets to `make/project.mk`:
```makefile
.PHONY: my-command
my-command: ## Description
	your command here
```

### Configure Hooks

Edit `.claude/settings.json`:
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

### Personal Settings

Your `~/.claude/` directory (not in git) can contain:
- Personal hooks
- Custom commands  
- User preferences

## MCP Servers

The template configures these MCP servers:

- **repoprompt** - Surgical file operations and code exploration
- **perplexity** - Web search and research (replaces Brave Search)
- **context7** - Up-to-date library documentation
- **snap-happy** - Screenshot tools
- Additional servers can be configured based on project needs

Configure with: `make setup-mcp`

## Philosophy

### Principles

1. **AI as partner, not replacement** - Amplify human decisions
2. **Modify over create** - Best code is no code
3. **Reality over memory** - Always verify against actual state
4. **Specialization over generalization** - Right tool for each phase
5. **Continuous verification** - Catch errors early and often

### Decision Points

These require human approval:
- Architectural plans from coordinator agent
- Refactoring proposals from system-analyst agent
- Any file rewrites vs modifications
- Creating new abstractions

### Anti-Patterns

The template actively prevents:
- Creating `_v2.py` duplicate files
- Using `pip` instead of `uv`
- Hallucinating functions that don't exist
- Over-engineering simple solutions

## Troubleshooting

**Claude gets confused about code**
- Use smaller context: `make generate-context-python`
- Delegate analysis: `make ai-analyze-project`

**Tests failing after changes**
- Check hooks ran: `make format`
- Review changes: `make review-diff`

**Can't find functionality**
- Search codebase: `make code-search PATTERN="..."`
- Check structure: `mcp__repoprompt__get_file_tree`

## Attribution

This template synthesizes patterns from:
- shoreman.sh from @mitsuhiko's minibb
- Context strategies from Claude Discord community
- Logging approach from @mitsuhiko's workflows
- Many developers sharing AI-assisted development experiences

## Further Reading

- Run `make help` for all commands
- Check `.claude/commands/` for workflow examples
- See `CLAUDE.md` for collaboration principles