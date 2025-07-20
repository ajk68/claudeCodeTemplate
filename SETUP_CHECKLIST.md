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
- [ ] Install [uv](https://github.com/astral-sh/uv) for Python package management
- [ ] Install Node.js and npm
- [ ] Install [ripgrep](https://github.com/BurntSushi/ripgrep) (`rg`)
- [ ] Install [Claude Code](https://claude.ai/code) CLI
- [ ] Install Git

### 2. Environment Configuration
- [ ] Copy `.env-example` to `.env` (or let setup create it)
- [ ] Add your API keys to `.env`:
  - [ ] `PERPLEXITY_API_KEY` - For web search via MCP
  - [ ] `ANTHROPIC_API_KEY` - For AI delegation commands
  - [ ] `OPENAI_API_KEY` - Optional, for GPT models
  - [ ] `GOOGLE_API_KEY` / `LLM_GEMINI_KEY` - For Gemini models
  - [ ] `GH_TOKEN` - For GitHub operations

### 3. Project Personalization
- [ ] Update `pyproject.toml`:
  - [ ] Change `name` from "claude-dev-template"
  - [ ] Update `description`
  - [ ] Add project-specific dependencies
- [ ] Update `CLAUDE.md`:
  - [ ] Fill in "Project Specific Instructions" section
  - [ ] Add project overview (tech stack, components)
  - [ ] Document architecture decisions
  - [ ] Add development workflow notes
- [ ] Update repository settings:
  - [ ] Change git remote URL to your repository
  - [ ] Update LICENSE if needed

### 4. MCP Server Setup
- [ ] Run `make setup-mcp` to see MCP commands
- [ ] Or run `make setup-mcp-auto` to configure automatically
- [ ] Restart Claude Code after MCP setup
- [ ] Verify MCP servers with `/mcp` command

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