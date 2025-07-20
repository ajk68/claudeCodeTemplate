# Template Guide

Complete reference for the Claude Code Development Template.

## Overview

This template creates a structured workflow between developers and Claude. It addresses common problems in AI-assisted development:

- **Context pollution** - AI loses focus in large codebases
- **Hallucination** - AI invents functions or patterns that don't exist  
- **Error propagation** - Bugs compound over time
- **Over-engineering** - AI adds unnecessary complexity

## Architecture

### Directory Structure

```
.claude/
├── commands/        # Workflow prompts (/brainstorm, /implement, etc.)
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

### 1. Context Management

The template uses tiered context generation to keep Claude focused:

```bash
make generate-context-python    # Python only (~40K tokens)
make generate-context-small     # Compressed overview (~60K tokens)  
make generate-context-code      # Code without docs/tests (~70K tokens)
make generate-context-full      # Everything (~145K tokens)
```

Smart delegation based on size:
- Small files (<70KB) → Claude
- Large files (>70KB) → Gemini
- Codebase analysis → Delegated to fresh instance

### 2. Reality Grounding

Multiple verification layers prevent hallucination:

- **repoprompt MCP Server** - Read actual files, not from memory. You have to download from repoprompt.com (paid, but nice!)
- **Context7** - Get real documentation. Automatically installed. 
- **make db-schema** - Check actual database structure. Uses `psql` . please change Makefile in `/make/tools/database.mk` to change
- **Perplexity MCP Server** - Research current best practices. Will be automatically installed, but requires API key in .env

### 3. Workflow Commands

Each development phase has specialized commands:

#### Planning Phase
- `/brainstorm` - Explore with data-driven insights
- `/prd` - Create product requirements document
- `/architect` - Minimal technical implementation plan

#### Execution Phase  
- `/implement` - Execute changes with focused context
- `/test` - Verify functionality
- `/refactor` - Propose high-ROI improvements

#### Review Phase
- `/review` - Peer-style consultative feedback
- `/ship` - Final quality checks and commit
- `/document` - Update docs to match reality

### 4. Quality Automation

Hooks run automatically after edits:
- Python formatting with ruff
- Linting and error checking
- Smart blockers (prevent `_v2.py` files, enforce `uv` over `pip`)

Manual quality commands:
```bash
make test           # Run test suite
make lint           # Check issues
make format         # Fix formatting
make review-diff    # AI review of changes
```

### 5. Centralized Logging

All services log to one place:

```bash
make dev           # Start with unified logging
make logs-watch    # Real-time monitoring
make logs-analyze  # AI pattern analysis
```

Uses shoreman.sh (from mitsuhiko/minibb) for process management.

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

- `/brainstorm` - Explore ideas
- `/architect` - Plan implementation  
- `/implement` - Write code
- `/test` - Verify it works
- `/review` - Get feedback
- `/ship` - Commit changes
- `/document` - Update docs
- `/status` - Current state
- `/tools` - Command reference

## Customization

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

- **perplexity** - Web search and research
- **context7** - Documentation lookup
- **playwright** - Browser automation
- **repoprompt** - File operations

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
- Architectural plans from `/architect`
- Refactoring proposals from `/refactor`  
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
- Check structure: `repoprompt: get_file_tree`

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