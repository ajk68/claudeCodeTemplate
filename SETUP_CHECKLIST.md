# Setup Checklist

This checklist helps you set up a new project from the Claude Code template.

## 🚀 Quick Setup

```bash
# Clone the template and run setup
git clone <template-url> my-project
cd my-project
make setup
```

## 📋 Manual Setup Checklist

### 1. Prerequisites
- [ ] Install [uv](https://github.com/astral-sh/uv) for Python package management with `curl -LsSf https://astral.sh/uv/install.sh | sh`
- [ ] Install Node.js and npm with  with `brew install node`
- [ ] Install [ripgrep](https://github.com/BurntSushi/ripgrep) (`rg`) with `brew install ripgrep`
- [ ] Install [Claude Code](https://claude.ai/code) CLI with `npm install -g @anthropic-ai/claude-code`
- [ ] Install Git with `brew install git`

### 2. Environment Configuration
- [ ] Copy `.env-example` to `.env` (or let setup create it)
- [ ] Add your API keys to `.env` (see `.env-example` for details)

### 3. Project Personalization
- [ ] Update `pyproject.toml`: change `name` and `description`
- [ ] Update `CLAUDE.md`: fill in the project-specific placeholders
- [ ] Update git remote URL to your repository

### 4. Setup
- [ ] Run `make setup` to configure MCP servers and verify setup

### 5. Optional Enhancements
- [ ] Add project-specific slash commands in `.claude/commands/`
- [ ] Configure hooks in `.claude/settings.json`
- [ ] Add custom Make targets in `make/` directory
- [ ] Set up CI/CD workflows in `.github/workflows/`
- [ ] Configure pre-commit hooks

### 6. Verification
- [ ] Run `make help` to see available commands
- [ ] Run `make test` to verify test setup
- [ ] Run `make lint` to check code quality
- [ ] Run `make project-status` to see project state
- [ ] Try `/status` in Claude Code

## 🎯 Ready to Code!

Once setup is complete:
1. Start Claude Code: `claude`
2. Use `/brainstorm` to explore ideas
3. Use `/architect` to plan implementation
4. Use `/implement` to write code
5. Use `/ship` to commit changes

## 📚 Resources

- [TEMPLATE_GUIDE.md](TEMPLATE_GUIDE.md) - Comprehensive template documentation
- [CLAUDE.md](CLAUDE.md) - AI collaboration principles and project instructions
- `make help` - See all available automation commands
- `/tools` - See all Claude Code workflow commands