# Claude Code Development Template

A structured workflow for AI-assisted development that prevents common pitfalls through specialized sub-agents and smart tooling.

## Quick Start

```bash
# Create new project
curl -sSL https://raw.githubusercontent.com/ajk68/claudeCodeTemplate/main/bootstrap.py | python3 - my-project
cd my-project
claude
```

## Why This Template?

1. **Context overload** → Sub-agents handle specific tasks in isolated contexts
2. **Hallucinations** → Tools verify against real files and documentation  
3. **Cascading bugs** → Unified logging and early detection
4. **Over-engineering** → Enforced simplicity and approval gates
5. **Wrong tool for the job** → Specialized agents for each development phase
6. **Repetitive instructions** → Pre-built commands with best practices

## Core Commands

```bash
# Development workflow
/brainstorm "idea"     # Explore with coordinator agent
/implement "feature"   # Execute with developer agent  
/fix "issue"          # Debug systematically
/project-status       # Current state summary

# Essential make commands
make dev              # Start all services with logging
make test            # Run test suite
make logs-analyze    # AI debugging of logs
make help            # See all commands
```

## Sub-Agents

Claude automatically uses specialized agents based on your task:

- **coordinator** - Multi-step task orchestration
- **developer** - Code implementation
- **tester** - High-impact test generation
- **reviewer** - Code review feedback
- **system-analyst** - Codebase understanding
- **quality-gate** - Deployment checks

Or invoke explicitly: `"Use the system-analyst to explore the caching layer"`

## Requirements

- Python 3.12+ with [uv](https://github.com/astral-sh/uv)
- Node.js & npm
- Git, Make, [ripgrep](https://github.com/BurntSushi/ripgrep)
- [Claude Desktop](https://claude.ai/download)

## Installation Modes

**Shared**: Uses `~/.claude/` and `~/ai_tools/` from dotfiles  
**Complete**: Self-contained with everything in project

## Documentation

- [TEMPLATE_GUIDE.md](TEMPLATE_GUIDE.md) - Complete reference
- [docs/AVAILABLE_TOOLS.md](docs/AVAILABLE_TOOLS.md) - Tool documentation
- `make help` - All available commands

## License

MIT
