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

## What Problems This Solves

1. **Claude gets confused in large codebases** → Smart context management keeps it focused
2. **Claude makes things up** → Reality checks verify against actual files/docs
3. **Bugs compound over time** → Catch problems early with unified logging and reviews
4. **AI over-engineers solutions** → Blockers enforce simplicity, require human approval
5. **Wrong tool for the job** → Specialized workflows for planning vs coding vs shipping
6. **Repeated instructions waste time** → Pre-built commands with best practices

## Key Features

### Smart Context Management
```bash
make generate-context-python    # Just Python files when that's all you need
make ai-analyze-project         # Delegate analysis to avoid confusion
```

### Reality Checks
```bash
repoprompt: read_file "api.py"  # Read actual files
make db-schema                  # Check real database
make code-search PATTERN="..."  # Find real patterns
```

### Early Problem Detection
```bash
make dev                        # All logs in one place
make logs-analyze               # AI spots issues
make review-diff                # Check before committing
```

### Enforced Simplicity
- Blocks creating `file_v2.py` duplicates
- Forces `uv` instead of `pip`
- Requires approval for big changes

### Specialized Workflows
```bash
/brainstorm     # Research and explore
/architect      # Plan with full context
/implement      # Code with focused context
/ship          # Quality checks and commit
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