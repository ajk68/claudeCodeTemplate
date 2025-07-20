# Claude Code Development Template

> ⚠️ **Experimental Setup**: This template reflects my evolving workflow, inspired by patterns I've learned from the developer community. Use at your own risk and please share your suggestions!

> My attempt at creating a more structured workflow with Claude, learning from community best practices

An experimental template exploring how to create a more structured workflow between developers and Claude, based on patterns I've learned from the community. This is my attempt at building a "cognitive exoskeleton" that might help amplify human decision-making while reducing common AI pitfalls.

## 🧪 About This Experimental Setup

This template is my personal experiment in AI-assisted development, heavily inspired by:
- Process management patterns from @mitsuhiko's minibb
- Context management strategies shared in the Claude community
- Workflow automation ideas from various open source projects

I'm continuously learning and iterating on these patterns. What works for me might not work for you - please adapt freely!

## 🚀 Quick Start

### Create a New Project

```bash
# One-line setup - downloads and runs bootstrap script
curl -sSL https://raw.githubusercontent.com/ajk68/claudeCodeTemplate/main/bootstrap.py | python3 - my-project

# Or if you prefer to review the script first:
wget https://raw.githubusercontent.com/ajk68/claudeCodeTemplate/main/bootstrap.py
python3 bootstrap.py my-project
```

This will:
1. Clone the template to a new directory
2. Remove template git history
3. Initialize fresh git repository
4. Run setup to configure your environment
5. Your project is ready to go!

### Start Development

```bash
cd my-project
claude              # Start Claude Code

# Try a workflow command
/status            # See project state without context pollution
```

## 🎯 Why I Created This Template

**What I noticed**: When working with AI assistants on larger codebases, I found they would often get lost, suggest functions that don't exist, or compound errors over time.

**What I'm trying**: This template experiments with:
- **Context Management** - Attempting to keep Claude focused through tiered context generation
- **Reality Grounding** - Testing multiple verification layers to reduce hallucination
- **Quality Feedback** - Exploring automated checks to catch issues early
- **Workflow Specialization** - Experimenting with purpose-built commands for different tasks

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

## 🤝 Contributing & Feedback

This template evolves through practice and community input. I'm learning as I go and would love to hear:
- What patterns work in your workflow?
- What doesn't work with this approach?
- Ideas for improvement

When you discover patterns that work (or don't), please share them! We're all figuring this out together.

## 🔧 Developing the Template

If you want to contribute to or customize the template itself:

```bash
# Clone the template repository directly
git clone https://github.com/ajk68/claudeCodeTemplate.git
cd claudeCodeTemplate
make install

# Make your changes, test, commit, push
# The bootstrap.py script ensures users won't accidentally modify the template
```

## 📄 License

MIT - Use this template freely for any project

---

Ready to amplify your development? Check out **[TEMPLATE_GUIDE.md](TEMPLATE_GUIDE.md)** for the full documentation.
