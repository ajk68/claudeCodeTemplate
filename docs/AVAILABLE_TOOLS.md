# Available Tools

Quick reference for all tools available to Claude and sub-agents.

## Make Commands

### Context Generation
```bash
make generate-context-python      # Python only 
make generate-context-code        # Code only  
make generate-context-full        # Everything 
make generate-context-small       # Compressed 
make generate-context-from-files FILES="file1.py file2.py"
```

### AI Analysis  
```bash
make ai-query PROMPT="?" [FILE=path]      # Smart model selection
make ai-analyze-project PROMPT="?" SCOPE=python|code|full
make analyze-file FILE="module.py"        # Architecture review
make review-diff                          # Review changes
make project-status                       # Current state
make logs-analyze                         # Debug logs
```

### Development
```bash
make dev                # Start all services  
make test              # Run tests
make lint-fix          # Fix code issues
make code-search PATTERN="regex"
make db-schema [TABLE=name]
```

### Logging
```bash
make logs-watch        # Real-time logs
make logs-analyze      # AI analysis
make logs-clean        # Clear logs
```

## MCP Tools

### RepoPrompt (mcp__repoprompt__)
File operations and code exploration.

**Available to agents**: All except reviewer (read-only)

```bash
mcp__repoprompt__search           # Smart pattern search
  pattern: "text"                 # Supports regex
  filter: {extensions: [".py"]}   # File filtering
  context_lines: 3                # Like grep -C

mcp__repoprompt__read_file        # Read files
  path: "file.py"
  start_line: 50                  # Optional range
  end_line: 100

mcp__repoprompt__get_code_structure  # Architecture without implementation
  paths: ["module.py"]

mcp__repoprompt__apply_edits      # Search and replace
  path: "file.py"
  edits: [{search: "old", content: "new"}]

mcp__repoprompt__file_actions     # Create/delete/move
  action: "create|delete|move"
  path: "file.py"
```

### Context7 (mcp__context7__)
Library documentation lookup.

**Available to**: searcher, system-analyst

```bash
mcp__context7__resolve-library-id   # Find library
  libraryName: "react"

mcp__context7__get-library-docs     # Get docs
  context7CompatibleLibraryID: "/facebook/react"
  topic: "hooks"                    # Optional focus
```

### Perplexity (mcp__perplexity__)
Web search and research.

**Available to**: searcher

```bash
mcp__perplexity__perplexity_ask
  messages: [{role: "user", content: "question"}]
```

## Direct Tools

### Command Line
```bash
uv run python script.py    # Always use uv
uv add package            # Install packages
git operations            # Version control
gh operations
psql                     # Direct database access
```

### Claude Native
- `Write` - Create files
- `Edit` - Modify files  
- `Read` - Read files
- `Bash` - Run commands

## Tool Selection Guide

**Broad understanding**: `make generate-context-*`  
**Specific files**: `mcp__repoprompt__read_file`  
**Pattern search**: `make code-search` or `mcp__repoprompt__search`  
**Analysis without loading**: `make ai-analyze-project`  
**Library docs**: `mcp__context7__*`  
**Web search**: `mcp__perplexity__*`  
**Quick edits**: `mcp__repoprompt__apply_edits`

## Common Workflows

### Starting a feature
```bash
make project-status
mcp__repoprompt__get_file_tree
mcp__repoprompt__read_file "relevant.py"
```

### Understanding architecture  
```bash
make generate-context-python
make ai-analyze-project PROMPT="explain auth" SCOPE=code
```

### Debugging
```bash
make logs-analyze
mcp__repoprompt__search "error_pattern"
make code-search PATTERN="ErrorClass"
```

### Making changes
```bash
mcp__repoprompt__get_code_structure "module.py"
mcp__repoprompt__apply_edits path="module.py"
make test && make lint-fix
```
