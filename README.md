# Claude Code Development Template

> Transform Claude from a code generator into a reliable engineering partner

A battle-tested template for AI-assisted development that creates a cognitive exoskeleton around Claude, amplifying human decision-making while preventing common AI failure modes.

## 🚀 Quick Start

```bash
# 1. Use this template to create your repository
# 2. Clone and setup
git clone <your-repo-url>
cd <your-repo>
make install

# 3. Start Claude Code
claude

# 4. Try a workflow command
/status    # See project state without context pollution
```

## 🎯 Why This Template?

**Problem**: AI assistants get lost in large codebases, hallucinate functions that don't exist, and compound errors over time.

**Solution**: This template provides:
- **Intelligent Context Management** - Tiered context generation keeps Claude focused
- **Reality-Grounded Development** - Multiple verification layers prevent hallucination
- **Continuous Quality Feedback** - Automated checks catch problems immediately
- **Specialized Workflows** - Purpose-built commands for each development phase

## 📖 Documentation

See **[TEMPLATE_GUIDE.md](TEMPLATE_GUIDE.md)** for the comprehensive guide including:
- Detailed workflow explanations
- All available commands
- Customization instructions
- Philosophy and principles

## 🛠️ Key Features

### Smart AI Delegation
```bash
make ai-analyze-project   # Full project analysis
make code-search          # Fast pattern searching
make review-diff          # AI-powered change review
```

### Development Workflows
```
/brainstorm    # Explore ideas with data-driven insights
/architect     # Create technical implementation plans
/implement     # Execute code changes efficiently
/ship          # Finalize and commit with quality checks
```

### Quality Automation
- Auto-formatting and linting after edits
- Test execution at checkpoints
- Smart blockers for common mistakes
- Reality checks against actual files/docs/schemas

## 📁 What's Included

```
.claude/          # Claude-specific configurations
├── commands/     # Workflow command definitions
└── settings.json # Project settings

make/             # Modular Make automation
├── ai.mk        # AI delegation commands
├── context.mk   # Context generation
└── quality.mk   # Testing and linting
```

## 🔧 Requirements

- [Claude Code](https://claude.ai/code) CLI
- Python with `uv` package manager
- Node.js and npm
- ripgrep (`rg`)
- Git

## 🤝 Contributing

This template evolves through practice. When you discover patterns that work (or don't), consider contributing them back to help others.

## 📄 License

MIT - Use this template freely for any project

---

Ready to amplify your development? Check out **[TEMPLATE_GUIDE.md](TEMPLATE_GUIDE.md)** for the full documentation.