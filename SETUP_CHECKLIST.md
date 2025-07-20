# Setup Checklist

Step-by-step instructions for setting up a new project from the Claude Code template.

## Prerequisites

## Why These Prerequisites

Each tool solves a specific problem:

- **Python 3.x** - Runs the automation scripts
- **Git** - Version control for your code
- **Make** - Runs all the helpful commands
- **[uv](https://github.com/astral-sh/uv)** - Fast Python package management (replaces pip)
- **Node.js and npm** - Required for MCP servers and some tools
- **[ripgrep](https://github.com/BurntSushi/ripgrep)** - Lightning-fast code search
- **[Claude Code](https://claude.ai/code)** - The AI coding assistant

## Create Your Project

### Option 1: Bootstrap Script (Recommended)

```bash
# Download and run in one line
curl -sSL https://raw.githubusercontent.com/ajk68/claudeCodeTemplate/main/bootstrap.py | python3 - my-project

# Or download first to review
wget https://raw.githubusercontent.com/ajk68/claudeCodeTemplate/main/bootstrap.py
python3 bootstrap.py my-project
```

The script will:
1. Clone the template
2. Remove template git history  
3. Update project name in pyproject.toml
4. Initialize fresh git repo
5. Run setup wizard
6. Delete bootstrap.py (no longer needed)

### Option 2: Manual Setup

```bash
# Clone template
git clone https://github.com/ajk68/claudeCodeTemplate.git my-project
cd my-project

# Remove template history
rm -rf .git
git init
git add .
git commit -m "Initial commit from template"

# Run setup
make setup
```

## Configure Your Project

After setup completes:

### 1. Environment Variables
```bash
# Edit .env file
cp .env-example .env
# Add your API keys:
# - PERPLEXITY_API_KEY (for web search)
# - ANTHROPIC_API_KEY (for AI delegation)
# - Other keys as needed
```

### 2. Project Details
- Update `pyproject.toml` with your project name and dependencies
- Fill in the "Project Specific Instructions" section in `CLAUDE.md`
- Add custom commands to `make/project.mk`

### 3. MCP Servers (Optional)
```bash
# Auto-configure Claude Code MCP servers
make setup-mcp
# Then restart Claude Code
```

## Verify Installation

Run these commands to check everything works:

```bash
make help           # See all commands
make test           # Run tests
make lint           # Check code quality
make project-status # View project state
```

In Claude Code:
```
/status            # Check from within Claude
/tools             # See available tools
```

## Start Development

```bash
claude              # Start Claude Code

# Try the workflow
/brainstorm "your idea"
/architect "feature name"
/implement "the changes"
/ship "commit message"
```

## Troubleshooting

**"command not found" errors**
- Check prerequisites are installed
- Restart your terminal after installing tools

**MCP server issues**
- Ensure API keys are set in .env
- Restart Claude Code after setup

**Python/uv issues**
- Make sure uv is installed: `curl -LsSf https://astral.sh/uv/install.sh | sh`
- Check Python version: `python3 --version` (needs 3.12+)

## For Template Developers

To modify the template itself (not create a project from it):

```bash
git clone https://github.com/ajk68/claudeCodeTemplate.git
cd claudeCodeTemplate
make install
# Make changes, test, commit, push
```