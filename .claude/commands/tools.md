# /tools - Available Tools

## Primary Interface: Make Commands

### 📦 Context Generation
When you need broad codebase understanding:

```bash
make generate-context-full      # Complete codebase (~145K tokens)
make generate-context-code      # Code only, no docs/tests (~70K tokens)
make generate-context-python    # Python files only (~40K tokens)
make generate-context-small     # Compressed core code (~60K tokens)
make generate-context-from-files FILES="file1.py file2.py"  # Specific files
make claude-context            # Claude setup/config context
```
**When to use**: Architecture questions, understanding patterns, getting overview. Start with `python` or `small`.

### 🤖 AI Delegation & Analysis
Smart analysis without context pollution:

```bash
make ai-query PROMPT="question" [FILE=path]     # Auto-selects Claude/Gemini by size
make ai-analyze-project PROMPT="question" [SCOPE=python|code|full|small]
make analyze-file FILE="module.py"              # Single file analysis
make analyze-files FILES="file1.py file2.py"    # Multiple files
make review-diff                                # Review git changes
make project-status                             # Current state summary
make analyze-logs [LOG_FILE=path] [LINES=100]  # Log analysis
```
**When to use**: Need analysis but don't want to load everything into context.

### 🔍 Search & Discovery
Find patterns and information:

```bash
make code-search PATTERN="regex" [FILETYPE=py]  # Fast code search with ripgrep
make db-schema [TABLE=name]                     # Database schema inspection
```

### 🧪 Quality & Testing
Ensure code quality:

```bash
make test                    # Run all tests
make test-coverage          # Tests with coverage report
make lint                   # Check code issues
make lint-fix              # Auto-fix issues
make format                # Format code
```

### 🚀 Project Operations
```bash
make run-pipeline          # Run data pipeline
make clear-cache          # Clear all caches
make install              # Install dependencies
make sync                # Update dependencies
make clean               # Clean generated files
```

## Direct Tool Access



### 🔍 Other Direct Tools

**rg (ripgrep)** - When make code-search isn't enough:
```bash
rg "pattern" --type py -C 3      # With context lines
rg "TODO|FIXME" -A 2             # Show lines after match
```

**Direct AI delegation** - When make commands don't fit:
```bash
cat file.txt | claude -p "specific analysis"              # Small, quick
llm -m gemini-2.5-flash -a large.xml "analyze"          # Large context
```

**Python & Database**:
```bash
uv run python script.py    # Always use uv run
psql -c "\d tablename"     # Direct schema query when needed
```

### 🌐 MCP Servers
```bash
# Documentation lookup 
Context7: resolve-library-id     # Find library
Context7: get-library-docs      # Get latest docs

# Web search/research
Perplexity: perplexity_ask    # Research solutions

# 🎯 repoprompt - Surgical Code Operations
# When actively coding and need to inspect/modify specific files:

get_file_tree                    # See project structure
get_code_structure "file.py"     # Get signatures, imports, structure
read_file "path/to/file.py"      # Read full file
read_file "file.py" 50 100       # Read lines 50-100
search "pattern" --type python   # Search for patterns
apply_edits "file.py"           # Direct search-and-replace
file_actions create/delete/move  # File operations

**When to use**: During implementation when you need to read specific files, check exact implementations, or make targeted edits. More precise than loading whole contexts.

```

## Decision Tree

**Need broad understanding?** → make generate-context-*
**Need specific file content?** → repoprompt read_file
**Need analysis without loading?** → make ai-analyze-*
**Need to find something?** → make code-search or repoprompt search
**Need surgical multi file edits?** → repoprompt apply_edits
**Need external info?** → Context7/Perplexity

## Common Workflows

```bash
# Starting work on a feature
make project-status                           # Current state
repoprompt: get_file_tree                    # See structure
repoprompt: read_file "relevant_module.py"   # Inspect specific files

# Understanding architecture
make generate-context-python                  # Get Python overview
make ai-analyze-project PROMPT="explain X" SCOPE=code

# Making changes
repoprompt: get_code_structure "module.py"    # See what's there
repoprompt: read_file "module.py" 100 150     # Read specific section
# ... make changes ...
make test && make lint                        # Verify

# Debugging
make analyze-logs                             # What went wrong?
repoprompt: search "error_pattern"            # Find in code
make code-search PATTERN="ErrorClass"         # Broader search
```

Remember: Use make commands for breadth, repoprompt for depth, and ask Arthur when uncertain.