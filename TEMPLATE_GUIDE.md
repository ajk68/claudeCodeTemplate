# Template Guide

## Overview

This template creates a structured workflow using Claude's sub-agent system. Each agent specializes in one aspect of development, preventing context confusion and improving output quality.

## Quick Reference

### Commands
```bash
/brainstorm "idea"     # Explore problems
/implement "feature"   # Build features
/fix "issue"          # Debug issues
/project-status       # Check state
```

### Key Make Commands
```bash
# Context generation (choose based on need)
make generate-context-python    # Python only (~40K tokens)
make generate-context-code      # Code without tests/docs (~70K)  
make generate-context-full      # Everything (~145K)

# Analysis
make ai-analyze-project PROMPT="question" SCOPE=python
make review-diff               # Review changes
make logs-analyze             # Debug from logs

# Development
make dev                      # Start with logging
make test                     # Run tests
make code-search PATTERN="x"  # Fast search
```

## Sub-Agents

Claude automatically selects the right agent, or you can invoke explicitly.

### Core Agents

**coordinator**  
Orchestrates multi-step tasks. Knows when to involve other agents.
```
> "Build user authentication" 
# Coordinator breaks this down and engages analyst, developer, tester
```

**developer**  
Implements code changes. Has write access to files.
- Uses repomix for surgical edits
- Runs tests automatically
- Follows existing patterns

**tester**  
Creates high-impact tests. Focuses on critical paths only.
- Skips trivial tests
- Tests user journeys
- Deletes obsolete tests

**reviewer**  
Provides peer feedback. Read-only access.
- Pattern consistency
- Potential issues
- Not a gatekeeper

**quality-gate**  
Final deployment checks. Pragmatic about shipping.
- Security scan
- Test verification  
- Commit creation

### Analysis Agents

**system-analyst**  
Deep codebase understanding.
- Architecture analysis
- Pattern detection
- Context generation

**searcher**  
Code discovery specialist.
- Pattern matching
- External documentation
- Cross-reference analysis

**analyst**  
Strategic planning.
- PRDs
- Implementation plans
- Technical feasibility

### Documentation Agents

**context-keeper** (formerly documenter)  
Maintains project memory.
- Active task tracking
- Weekly pattern distillation
- Drift monitoring

**documentation-writer**  
Evergreen documentation.
- Always current state
- No temporal language
- Holistic updates

## Project Structure

```
.claude/
├── agents/          # Agent definitions
├── commands/        # Workflow commands
├── hooks/           # Automation (formatting, blocking)
└── settings.json    # Configuration

make/
├── ai.mk           # AI commands
├── context.mk      # Context generation  
├── logging.mk      # Centralized logging
└── tools/          # Utilities

logs/
├── frontend/       # Browser logs
├── backend/        # Server logs
└── combined/       # Unified output
```

## Key Patterns

### Context Management
Start small, expand as needed:
```bash
make generate-context-python  # Start here
make generate-context-code    # If need more
make generate-context-full    # Last resort
```

### Reality Checks
Always verify against actual state:
```bash
make db-schema                    # Real database
make code-search PATTERN="auth"   # Real patterns
repomix: read_file "config.py"    # Real files
```

### Early Detection
Unified logging catches issues fast:
```bash
make dev            # Everything logged
make logs-watch     # Real-time monitoring
make logs-analyze   # AI spots problems
```

## Customization

### Add Project Commands
```bash
echo "Your prompt" > .claude/commands/my-command.md
# Use as: /my-command
```

### Project Make Targets
Add to `make/project.mk`:
```makefile
deploy: ## Deploy to production
	./deploy.sh
```

### Configure Hooks
Edit `.claude/settings.json` for automation.

## Anti-Patterns Prevented

- ❌ Creating `file_v2.py` duplicates
- ❌ Using `pip` instead of `uv`  
- ❌ Rewriting without permission
- ❌ Abstractions without 3+ uses
- ❌ Over-engineering simple tasks

## Troubleshooting

**Context confusion**: Use smaller context or sub-agents
**Test failures**: Check `make lint-fix` ran
**Can't find code**: Use `make code-search`
**Logs missing**: Ensure `make dev` is running

## Installation Modes

**Shared Mode**
- Uses `~/.claude/` from dotfiles
- Uses `~/ai_tools/` for make commands
- Best for personal projects

**Complete Mode**
- Everything in project directory
- Portable and self-contained
- Best for team projects

