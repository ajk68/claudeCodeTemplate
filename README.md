# Claude Code Development Template

A template for structured AI-assisted development with Claude. It helps prevent common AI pitfalls through context management, reality checks, and workflow specialization.

## Quick Start

```bash
# Create new project from template
curl -sSL https://raw.githubusercontent.com/ajk68/claudeCodeTemplate/main/bootstrap.py | python3 - my-project
cd my-project
claude
```

That's it. The bootstrap script handles everything.

## What This Does

- **Context Management** - Keeps Claude focused by delegating analysis to other models
- **Reality Checks** - Prevents hallucination by verifying against actual files/docs/schemas  
- **Quality Gates** - Automated linting, testing, and review at key points
- **Workflow Commands** - Specialized prompts for planning, coding, and shipping
- **Unified Logging** - All services log to one place for easier debugging

## Key Commands

```bash
# Development workflows
/brainstorm     # Explore ideas with real data
/architect      # Create minimal technical plans
/implement      # Execute changes efficiently
/ship          # Commit with quality checks

# Analysis tools
make ai-analyze-project    # Analyze codebase
make code-search          # Find patterns fast
make logs-analyze         # Debug from logs
```

## Requirements

- Python 3.x with [uv](https://github.com/astral-sh/uv)
- Node.js and npm
- [Claude Code](https://claude.ai/code) CLI
- Git, Make, ripgrep

## Documentation

- [SETUP_CHECKLIST.md](SETUP_CHECKLIST.md) - Detailed setup instructions
- [TEMPLATE_GUIDE.md](TEMPLATE_GUIDE.md) - Complete reference guide
- Run `make help` for all available commands

## Status

This is an experimental template based on patterns from the Claude community. It evolves through practice. Your mileage may vary.

## License

MIT