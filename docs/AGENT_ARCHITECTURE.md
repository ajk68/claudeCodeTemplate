# Agent Architecture

This document explains the AI agent system used in the Claude Code template.

## Overview

The template uses specialized AI agents to handle different aspects of software development. Each agent has specific tools, knowledge, and responsibilities, allowing Claude to work more effectively by using the right specialized context for each task.

## Core Agents

### coordinator
**Purpose**: Coordinates complex multi-step tasks across multiple domains  
**Tools**: Task, make project-status  
**When Used**: 
- Multi-step feature implementations
- Tasks requiring coordination between different parts of the system
- When you need high-level planning and execution
**Philosophy**: Stays lean on purpose - delegates analysis to specialized agents to maintain clean context for decision-making

### system-analyst  
**Purpose**: Understands codebase structure, patterns, and architecture  
**Tools**: Bash, get_file_tree, get_code_structure, search, read_file, all make generate-context-* commands, make ai-analyze-project  
**When Used**:
- Understanding existing code patterns
- Finding architectural conventions
- Analyzing project structure
- Comparing documentation against implementation
**Superpowers**: Instant context generation at any scale, AI-assisted pattern analysis, repomix tools for precise exploration

### developer
**Purpose**: Executes precise code changes with minimal context  
**Tools**: search, apply_edits, read_file, get_code_structure, Write, Edit, Bash, make test, make lint-fix, make format, make code-search, make analyze-logs, make db-schema  
**When Used**:
- Writing new code
- Modifying existing files
- Running tests and quality checks
- Database schema work
**Superpowers**: apply_edits for mechanical changes, repomix search for pattern discovery, auto-fixing code issues, log analysis for debugging

### analyst
**Purpose**: Creates detailed implementation plans before coding begins  
**Tools**: Task, get_code_structure, get_file_tree, read_file, Write, Bash, search, make generate-context-small, make ai-analyze-project, make db-schema  
**When Used**:
- Breaking down complex features into steps
- Creating technical specifications
- Planning refactoring efforts
**Superpowers**: get_code_structure for interface understanding, project navigation with get_file_tree, feasibility analysis

### searcher
**Purpose**: Searches and analyzes code across the codebase  
**Tools**: search, get_code_structure, get_file_tree, read_file, read_selected_files, all make generate-context-* commands, make code-search, make ai-query, make db-schema, WebSearch, perplexity, Context7  
**When Used**:
- Finding specific implementations
- Searching for usage patterns
- Looking up external documentation
- Understanding third-party libraries
**Superpowers**: Repomix search with regex/fuzzy/context, get_code_structure for quick architecture views, bulk file analysis with read_selected_files

### documenter
**Purpose**: Maintains project knowledge and wisdom over time  
**Tools**: read_file, Write, Edit, make project-status, make generate-context-from-files, make ai-analyze-project  
**When Used**:
- Updating project documentation
- Recording architectural decisions
- Maintaining CLAUDE.md and other context files
**Superpowers**: Pattern extraction from recent work, focused analysis of changes

### documentation-writer
**Purpose**: Maintains evergreen documentation that always reflects current system state  
**Tools**: read_file, Write, Edit, MultiEdit, search, get_code_structure, get_file_tree, make generate-context-full, make generate-context-code, make generate-context-from-files, make ai-analyze-project, make project-status, make code-search  
**When Used**:
- Updating developer documentation (README, API docs, architecture)
- Updating user documentation (guides, FAQs, troubleshooting)
- Ensuring documentation matches implementation
- Removing references to deprecated features
**Superpowers**: Holistic documentation updates, state-based writing (not diff-based), automated discrepancy detection

### reviewer (NEW)
**Purpose**: Peer review of code changes, not quality gate  
**Tools**: make review-diff, make analyze-files, make test, make lint, make ai-analyze-project, read_file, search  
**When Used**:
- Reviewing code changes before commit
- Providing feedback on implementations
- Checking pattern consistency
- Identifying potential issues
**Personality**: Thoughtful colleague providing observations, not judgments

### tester
**Purpose**: Pragmatic quality advocate focused on high-impact testing  
**Tools**: make test, make test-coverage, search, get_code_structure, read_file, Write, Edit, MultiEdit, make review-diff, make generate-context-from-files, make ai-analyze-project, Bash, make lint, make code-search  
**When Used**:
- Analyzing code changes to identify test needs
- Generating tests for critical paths
- Maintaining test suite as code evolves
- Removing tests when features are deleted
**Superpowers**: High-ROI test identification, 80/20 testing approach, fearless test deletion

### quality-gate (NEW)
**Purpose**: Final quality gate before deployment  
**Tools**: make review-diff, make test, make lint, make format, Bash, Git, read_file  
**When Used**:
- Final checks before committing
- Making pragmatic ship/don't ship decisions
- Ensuring code quality while maintaining momentum
**Personality**: Pragmatic deployer balancing quality with shipping

## Agent Selection

Agents are selected in two ways:

### Automatic Selection
Claude proactively uses agents based on the task:
- Planning a feature → coordinator or analyst
- Understanding code → system-analyst or searcher  
- Making changes → developer
- Updating docs → documenter or documentation-writer
- Ensuring docs match code → documentation-writer
- Writing or updating tests → tester
- Identifying test impact → tester

### Manual Invocation
You can explicitly request an agent:
```
> Use the system-analyst to understand the caching system
> Have the analyst break down the authentication feature
> Get the searcher to find all Redis usage
```

## Design Principles

### 1. Separation of Concerns
Each agent focuses on a specific domain, preventing context pollution and confusion.

### 2. Right-Sized Context
Agents only have access to tools they need, keeping them fast and focused. The orchestrator intentionally has minimal tools to maintain clarity for decision-making.

### 3. Preservation of Main Context
Using agents via the Task tool preserves the main conversation context, allowing for longer, more complex workflows.

### 4. Specialized Knowledge
Each agent has tailored instructions for their specific role, improving quality and consistency.

### 5. Lean Coordination
The coordinator stays lean on purpose - it delegates analysis to specialized agents rather than trying to understand everything itself. This prevents the exact context overflow problem that sub-agents were designed to solve.

## Command Integration

Some commands use agents internally:
- `/brainstorm` → Uses coordinator for exploration
- `/implement` → Coordinates multiple agents for execution
- `/status` → Uses specialized context without pollution

## Implementation Details

### Agent Definition
Agents are defined in `.claude/agents/` as markdown files with:
- Name and description
- Available tools
- Specific instructions and patterns
- Example workflows

### Agent Invocation
Agents are invoked through the Task tool with:
```python
Task(
    description="Short task description",
    prompt="Detailed instructions for the agent",
    subagent_type="agent-name"
)
```

### Context Management
- Agents run in isolated contexts
- Results are returned to the main conversation
- Main context remains unpolluted

## Benefits

1. **Better Quality**: Specialized agents produce better results in their domains
2. **Faster Execution**: Focused context means less confusion and faster completion
3. **Scalability**: Easy to add new agents for new specialized tasks
4. **Maintainability**: Agent behaviors can be tuned independently

## Agent Superpowers

The agents have been upgraded with powerful make commands and repomix MCP tools that dramatically improve their efficiency:

### Repomix MCP Tools
The repomix tools provide sophisticated code exploration capabilities:

1. **search** - Advanced pattern matching with:
   - Regex support
   - Fuzzy space matching
   - Context lines (like grep -C)
   - File filtering by extension/path
   - Whole word matching
   - Case-insensitive by default

2. **apply_edits** - Direct search-and-replace for mechanical changes:
   - Single or multiple edits
   - Precise text matching
   - No need for complex Edit tool operations

3. **get_code_structure** - Architecture without implementation:
   - See all functions/classes/methods
   - No function bodies
   - Perfect for understanding interfaces

4. **get_file_tree** - Navigate project structure:
   - Multiple view types (files, folders, code_structure)
   - Filter modes (auto, full, selected)
   - Understand project layout instantly

5. **read_file** - Precise file reading:
   - Line range support
   - More efficient than generic Read tool

6. **read_selected_files** - Bulk file operations:
   - Read multiple files efficiently
   - Structured format output

### Before vs After Example
**Before (Searcher searching for a pattern)**:
```
1. grep "class.*Controller"
2. read file1.py
3. read file2.py
4. grep "def.*init"
5. read file3.py
... (20+ operations)
```

**After (Searcher with superpowers)**:
```
1. make code-search PATTERN="class.*Controller" FILETYPE=py
2. make generate-context-from-files FILES="controllers.py auth.py"
3. make ai-query FILE="/tmp/context.txt" PROMPT="Analyze controller patterns"
(3 operations, comprehensive results)
```

### Key Efficiency Gains
1. **Context Generation**: One command generates comprehensive context instead of dozens of reads
2. **Intelligent Search**: `make code-search` with ripgrep is 10x faster than multiple greps
3. **AI Delegation**: `make ai-analyze-project` provides deep insights without context pollution
4. **Automated Quality**: `make lint-fix` and `make format` fix issues automatically
5. **Smart Analysis**: `make analyze-logs` debugs failures intelligently

## Best Practices

### 1. Use Make Commands First
Agents should prefer make commands over manual operations:
- `make code-search` instead of grep
- `make generate-context-*` instead of multiple reads
- `make ai-analyze-project` instead of manual analysis

### 2. Right-Size Context Generation
- **Full** (~145K tokens): Complete analysis tasks
- **Code** (~70K tokens): Implementation understanding
- **Python** (~40K tokens): Language-specific patterns
- **Small** (~60K tokens): Quick architectural overview
- **From-files**: Focused analysis of specific files

### 3. Efficiency Patterns
- Start broad with context generation
- Use AI delegation for complex analysis
- Batch operations when possible
- Cache results to avoid regeneration

### 4. Anti-Patterns to Avoid
- Don't cascade make commands unnecessarily
- Don't duplicate context generation
- Don't skip make for simple tasks (single file reads are OK)
- Don't over-delegate (agents should do work, not just call make)

## Workflow Examples

### Feature Implementation Flow
```bash
# Coordinator starts
make generate-context-small
make ai-analyze-project PROMPT="Architecture for notification system"

# Developer executes
make code-search PATTERN="similar_notification"
# ... implement code ...
make test
make lint-fix
make format

# Tester ensures coverage
make review-diff
make ai-analyze-project PROMPT="Critical paths for notification feature"
# ... write high-impact tests ...

# Reviewer checks
make review-diff
make analyze-files FILES="notification.py"

# Quality-gate deploys
make test
make lint
git commit -m "feat: Add notification system"
```

### Debugging Flow
```bash
# When tests fail
make analyze-logs

# When performance issues
make ai-analyze-project PROMPT="Performance bottlenecks" SCOPE=code

# When understanding needed
make generate-context-from-files FILES="problem_area.py"
```

## Future Enhancements

- Additional specialized agents (e.g., test-writer, performance-analyzer)
- Agent composition for complex workflows
- Learning from successful patterns to improve agents
- Project-specific agent customization
- Further make command integration
- Metrics tracking for agent efficiency