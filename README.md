# Claude Code Development Template

> ⚠️ **Experimental Setup**: This template reflects my evolving workflow, inspired by patterns I've learned from the developer community. Use at your own risk and please share your suggestions!

> My attempt at creating a more structured workflow with Claude, learning from community best practices

An experimental template exploring how to create a more structured workflow between developers and Claude, based on patterns I've learned from the community. This is my attempt at building a "cognitive exoskeleton" that might help amplify human decision-making while reducing common AI pitfalls.

## 🧪 About This Experimental Setup

This template is my personal experiment in AI-assisted development, heavily inspired by:
- Process management and unified logging patterns from the developer community
- Context management strategies shared in the Claude community
- Workflow automation ideas from various open source projects
- Lessons learned from debugging AI failure modes

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
5. Clean up the bootstrap script (no longer needed)
6. Your project is ready to go!

### Start Development

```bash
cd my-project
claude              # Start Claude Code

# Try a workflow command
/status            # See project state without context pollution
```

## 🎯 Why I Created This Template

When working with AI assistants on larger codebases, I noticed they would often get lost, suggest functions that don't exist, or compound errors over time. This template is my attempt to create a systematic approach to human-AI collaboration that prevents these failure modes.

## 🎯 Goals of This Claude Code Setup

### 1. Preserve Context Through Intelligent Delegation
* **Problem**: Claude's context window fills up with irrelevant information, leading to confusion and mistakes
* **Solution**: Main agent stays focused on the task while delegating information gathering to specialized agents
* **Implementation**: Make commands that auto-select models based on content size, separate commands for different context scopes

### 2. Ground AI in Reality (Anti-Hallucination)
* **Problem**: AI makes assumptions, invents patterns, or creates unnecessary abstractions
* **Solution**: Always check against real codebase, real docs, real database schemas
* **Implementation**:
  * repoprompt for surgical file reading
  * Context7 for actual documentation
  * `make db-schema` for real database state
  * Perplexity for current best practices

### 3. Enable Continuous Feedback Loops
* **Problem**: AI goes down rabbit holes, creates bugs, or builds the wrong thing
* **Solution**: Fresh eyes review at multiple stages, not just at the end
* **Implementation**:
  * **Unified Logging**: All services log to one place, AI can analyze with `make logs-analyze`
  * **Consultative Reviews**: `/review` for peer-style feedback, not just pass/fail gates
  * `make review-diff` before shipping
  * `make analyze-files` during implementation
  * `make lint/test` for immediate verification
  * Hooks that block bad patterns in real-time

### 4. Enforce Pragmatic Development Discipline
* **Problem**: AI tendency to over-engineer, rewrite, or add unnecessary complexity
* **Solution**: Systematic bias toward modification over creation, simplicity over cleverness
* **Implementation**:
  * Decision points requiring human approval
  * "Best code is no code" philosophy baked into commands
  * Smart blockers preventing version proliferation

### 5. Create a Cognitive Exoskeleton for AI
* **Problem**: Single AI agent trying to be architect, coder, reviewer, and debugger all at once
* **Solution**: Specialized workflows that guide AI through each phase with appropriate tools
* **Implementation**:
  * `/architect` for planning (with full context)
  * `/implement` for execution (with focused context)
  * `/ship` for finalization (with quality gates)
  * Each phase has its own toolkit and success criteria

### 6. Maximize Human-AI Collaboration Efficiency
* **Problem**: Humans repeating instructions, AI missing context, both wasting time
* **Solution**: Codified workflows that embed best practices and lessons learned
* **Implementation**:
  * Slash commands that guide conversations
  * Make commands that automate repetitive patterns
  * Clear decision points for human input
  * "Arthur is the most powerful tool" philosophy

## 🚀 The Meta Goal

Transform Claude from a "smart autocomplete" into a reliable engineering partner by:
* Preventing known failure modes (context pollution, hallucination, over-engineering)
* Amplifying strengths (pattern matching, code generation, analysis)
* Creating reproducible, efficient workflows
* Building trust through verification and feedback

This isn't just about making Claude more productive - it's about making the human-AI team more effective than either could be alone.

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

### Unified Logging & Debugging
```bash
make dev              # Start all services with centralized logging
make logs-watch       # Watch all logs in real-time
make logs-analyze     # AI analysis of log patterns and issues
```

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
