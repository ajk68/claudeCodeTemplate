# Setup Checklist

> ⚠️ **Note**: This checklist reflects my current workflow for setting up projects. It's an experimental approach that works for me - please adapt it to your needs!

This checklist helps you set up a new project from the Claude Code template, based on patterns I've been experimenting with.

## 🚀 Quick Setup (Recommended)

```bash
# One-line project creation
curl -sSL https://raw.githubusercontent.com/YOUR_USERNAME/claudeCodeTemplate/main/bootstrap.py | python3 - my-project

# Or download and run
wget https://raw.githubusercontent.com/YOUR_USERNAME/claudeCodeTemplate/main/bootstrap.py
python3 bootstrap.py my-project
```

This bootstrap script attempts to:
- ✅ Clone the template
- ✅ Remove template git history
- ✅ Update project name
- ✅ Initialize fresh git repo
- ✅ Run setup process

(I've found this approach helps avoid common setup mistakes, but your mileage may vary!)

## 📋 Prerequisites

Before using the bootstrap script, ensure you have:
- [ ] Python 3.x installed
- [ ] Git installed
- [ ] Make installed (for the setup process)

After bootstrap completes, you'll also need:
- [ ] [uv](https://github.com/astral-sh/uv) for Python package management
- [ ] Node.js and npm
- [ ] [ripgrep](https://github.com/BurntSushi/ripgrep) (`rg`)
- [ ] [Claude Code](https://claude.ai/code) CLI

## 🔄 Post-Bootstrap Steps

After the bootstrap script completes:

### 1. Environment Configuration
- [ ] Edit `.env` and add your API keys (see `.env-example` for details)

### 2. Project Personalization
- [ ] Update `CLAUDE.md`: fill in the project-specific instructions
- [ ] Add project-specific commands to `make/project.mk`
- [ ] Configure any additional tools or services

### 3. Optional Enhancements
- [ ] Add project-specific slash commands in `.claude/commands/`
- [ ] Configure hooks in `.claude/settings.json`
- [ ] Add custom Make targets in `make/project.mk`
- [ ] Set up CI/CD workflows in `.github/workflows/`
- [ ] Configure pre-commit hooks

## ✅ Verification

After setup is complete:
- [ ] Run `make help` to see available commands
- [ ] Run `make test` to verify test setup
- [ ] Run `make lint` to check code quality
- [ ] Run `make project-status` to see project state
- [ ] Try `/status` in Claude Code

## 🎯 Ready to Code!

Once setup is complete, here's the workflow I've been experimenting with:
1. Start Claude Code: `claude`
2. Use `/brainstorm` to explore ideas
3. Use `/architect` to plan implementation
4. Use `/implement` to write code
5. Use `/ship` to commit changes

These commands represent my attempt at creating a structured development flow - feel free to adapt or ignore them based on what works for you!

## 🔧 For Template Developers

If you're working on the template itself (not creating a new project):

```bash
# Clone the template repository directly
git clone https://github.com/YOUR_USERNAME/claudeCodeTemplate.git
cd claudeCodeTemplate
make install
```

## 📚 Resources

- [TEMPLATE_GUIDE.md](TEMPLATE_GUIDE.md) - My evolving template documentation
- [CLAUDE.md](CLAUDE.md) - AI collaboration principles I'm experimenting with
- `make help` - See all available automation commands
- `/tools` - See all Claude Code workflow commands

## 💡 Feedback Welcome

This setup process is constantly evolving based on what I learn. If you find better approaches or have suggestions, please share them! We're all figuring out these AI-assisted workflows together.
