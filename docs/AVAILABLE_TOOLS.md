# Available Tools Documentation

This document provides comprehensive information about all tools available in the claudeCodeTemplate project, including MCP servers, Make commands, and direct tools.

## Table of Contents
- [RepoPrompt MCP Server](#repoprompt-mcp-server)
- [Make Commands](#make-commands)
- [Other MCP Servers](#other-mcp-servers)
- [Direct Tools](#direct-tools)
- [Decision Guide](#decision-guide)

## RepoPrompt MCP Server

The RepoPrompt MCP server provides surgical file operations and code exploration tools. These are excellent for precise, targeted operations on specific files.

**Exact Tool Names for Agent Configuration:**
- `mcp__repoprompt__get_file_tree`
- `mcp__repoprompt__read_file`
- `mcp__repoprompt__apply_edits` (for agents with write permissions)
- `mcp__repoprompt__search`
- `mcp__repoprompt__file_actions` (for agents with write permissions)
- `mcp__repoprompt__get_code_structure`

### 1. mcp__repoprompt__search
Search files and/or contents for literal or regex patterns.

**Use this to:**
- Find specific code patterns or implementations
- Locate files by name or content
- Surface data before making edits

**Parameters:**
- `pattern`: Text or regex pattern to search for
- `mode`: 'auto', 'path', 'content', or 'both' (default: auto-detects based on pattern)
- `regex`: Enable regular expression matching
- `filter`: File filtering options (extensions, exclude patterns, specific paths)
- `max_results`: Maximum total results returned (default: 250)
- `count_only`: Return only the count of matches, not the actual matches
- `context_lines`: Include N lines before/after each match (like grep -C)
- `whole_word`: Match whole words only (adds word boundaries)

**Auto-detection & smart defaults:**
- **Case-insensitive** by default (most intuitive)
- **Fuzzy space matching** auto-enabled for patterns with spaces
- **Mode detection**: "/" or "*" → path search, spaces → content search, short patterns → both

**Filter options (all optional):**
- `extensions`: [".js", ".ts"] - only search these file types
- `exclude`: ["node_modules", "*.log"] - skip matching patterns
- `paths`: ["src/", "lib/"] - limit to specific directories

### 2. mcp__repoprompt__apply_edits
Directly apply precise search-and-replace edits to files.

**Best for:**
- Simple, mechanical edits with exact text matches
- When you know exactly what to change
- Quick fixes without needing conversation

**Modes:**
- **Single Edit**: Provide 'search' (block to find) and 'content' (replacement)
  - Empty 'search' replaces entire file content
  - Non-empty 'search' replaces first exact match only
- **Multiple Edits**: Provide array of edits ('search', 'content' pairs)
  - Each edit is matched independently against original file content (not sequentially updated)

**Important:**
- Matches require exact content (whitespace, indentation, comments)
- Always verify original content with `mcp__repoprompt__read_file` first
- Set `verbose=true` to preview detailed unified diff before applying

### 3. mcp__repoprompt__get_code_structure
Retrieve concise structured representation of specified files (imports, class/function/method signatures).

**Use this to:**
- Understand code architecture before making changes
- Get quick overview of file structure
- Identify where to make edits

**Important:**
- Excludes implementation details and function bodies
- Only supports files with available code-structure data (codemaps)
- To check available files, first call `mcp__repoprompt__get_file_tree` with `type="code_structure"`

### 4. mcp__repoprompt__get_file_tree
Get ASCII representation of the project's directory tree.

**View types:**
- `files`: Standard file tree with filtering modes:
  - `auto`: Excludes common build artifacts (.o, .dll) and folders like .git, node_modules
  - `full`: Includes all files and folders
- `folders`: Directories only
- `selected`: Only selected files and their parent folders
- `code_structure`: Files with available code-structure (codemap) data
- `roots`: List root folder paths

**Note:**
- `mode` parameter only applies when `type` is set to 'files'
- Use `max_depth` to limit tree depth and `include_hidden` to show hidden files/folders

### 5. mcp__repoprompt__read_file
Read file contents, optionally specifying a line range.

**Details:**
- Line numbers are 1-based (first line is line 1)
- Without a range, returns entire file content
- Use this to examine files before editing or to answer questions about code

### 6. mcp__repoprompt__file_actions
Perform filesystem operations: create, delete, or move files.

**Actions:**
- `create`: New file with provided content (fails if file exists)
  - Created files are automatically added to selection
- `delete`: Delete existing file (requires absolute path for safety)
- `move`: Move or rename existing file (fails if destination exists)

**Parameters:**
- `action`: Operation to perform (create, delete, move)
- `path`: File path
- `content`: File content (for create)
- `new_path`: New path (for move)

## Make Commands

Make commands provide high-level workflows and batch operations. Use these for broader tasks and analysis.

### 📦 Context Generation
Generate different views of the codebase for AI analysis:

```bash
make generate-context-full       # All files in repo (~145K tokens)
make generate-context-code       # Code only, no docs/tests (~70K tokens)
make generate-context-python     # Python files only (~40K tokens)
make generate-context-small      # Compressed core code (~60K tokens)
make generate-context-from-files FILES="file1.py file2.py"  # Specific files
make claude-context             # Claude config files (user + project)
```

### 🤖 AI Delegation & Analysis
Delegate analysis tasks to AI without polluting context:

```bash
make ai-query PROMPT="question" [FILE=path]      # Auto-selects model by size
make ai-analyze-project PROMPT="question" [SCOPE=python|code|full|small]
make analyze-file FILE="module.py"               # Architecture review
make analyze-files FILES="file1.py file2.py"     # Multi-file analysis
make review-diff                                 # Review git changes
make project-status                              # Git status + commits summary
make analyze-logs [PROMPT="question"]            # Debug log analysis
```

### 🔍 Search & Discovery
Find patterns and database information:

```bash
make code-search PATTERN="regex" [FILETYPE=py]   # Fast regex search
make db-schema [TABLE=name]                      # Database schema (uses CARV_DB_URL)
```

### 🪵 Logging & Monitoring
Centralized logging suite for multi-service debugging:

```bash
make dev                      # Start all processes with unified logging
make logs-watch               # Tail all logs in real-time
make logs-analyze [PROMPT=""] # AI analysis of recent logs
make logs-clean              # Delete all log files
make logs-tail FILE=frontend # Tail specific log
make logs-stop               # Kill background processes
make logs-help               # Show logging setup guide
```

### 🧪 Testing & Quality
Code quality and testing commands:

```bash
make test                    # Run all tests (pytest via uv)
make test-coverage          # Tests with coverage report
make lint                   # Check code issues (ruff)
make lint-fix              # Auto-fix safe issues
make lint-fix-unsafe       # Fix all issues (use carefully)
make format                # Format code style
```

### 🧹 Development Setup & Cleanup
Project setup and maintenance:

```bash
make install               # Install all dependencies
make install-python        # Python dependencies only (uv sync)
make install-node         # Node.js dependencies only
make sync                 # Update Python dependencies
make sync-all            # Update all dependencies
make setup-mcp           # Auto-configure MCP servers
make clean               # Clean caches (keeps dependencies)
make clean-all          # Deep clean including node_modules
```

### 🛠️ Utility Scripts
Additional tools in `make/tools/`:

#### claude_chat_analyzer.py
Export and analyze Claude chat conversations:

```bash
# Discovery mode - see all projects
uv run python make/tools/claude_chat_analyzer.py

# Export specific project conversations
uv run python make/tools/claude_chat_analyzer.py --projects="project-name" --max-age="2d"
```

#### claude_code_setup.py
Pack Claude Code configuration files:

```bash
# Generate context of all Claude Code setup files
make claude-context  # Uses this script internally
```

#### setup_mcp_servers.py
Configure MCP servers for Claude Code:

```bash
# Generate commands to add MCP servers
make setup-mcp  # Uses this script internally
```

#### setup_project.py
Initial project setup (used by bootstrap):

```bash
# Called automatically by 'make setup'
# Handles prerequisites, dependencies, .env file
```

#### logger.py
Centralized logging utilities for Python scripts:

```python
from make.tools.logger import Logger
logger = Logger("my-script")
logger.info("Starting process...")
```

#### shoreman.sh
Process management for development (inspired by mitsuhiko):

```bash
# Used internally by 'make dev' to run Procfile
# Manages multiple processes with unified logging
```

## Other MCP Servers

### Context7 MCP Server - Library Documentation
Get up-to-date documentation for any library or framework.

**Exact Tool Names for Agent Configuration:**
- `mcp__context7__resolve-library-id`
- `mcp__context7__get-library-docs`

#### 1. mcp__context7__resolve-library-id
Resolves a package/product name to a Context7-compatible library ID.

**Features:**
- Required before using get-library-docs (unless user provides the ID directly)
- Returns a list of matching libraries with:
  - Name similarity scores
  - Description relevance
  - Documentation coverage (Code Snippet counts)
  - Trust scores (7-10 considered authoritative)
- Example: `resolve-library-id("react")` → `/facebook/react`

#### 2. mcp__context7__get-library-docs
Fetches up-to-date documentation for a library.

**Parameters:**
- `context7CompatibleLibraryID`: Required ID like `/mongodb/docs`, `/vercel/next.js`
- `tokens`: Max tokens to retrieve (default 10000)
- `topic`: Optional topic focus (e.g., 'hooks', 'routing')

**Returns:** Current documentation and code examples

**Usage Pattern:**
```bash
# First resolve library name to ID
mcp__context7__resolve-library-id("library-name")

# Then get documentation
mcp__context7__get-library-docs("/org/project", tokens=10000, topic="hooks")
```

These tools are ideal for getting the latest, accurate documentation for any library or framework.

### Perplexity MCP Server - Web Search & Research
Research solutions and current information using the Sonar API.

**Exact Tool Name for Agent Configuration:**
- `mcp__perplexity__perplexity_ask`

#### mcp__perplexity__perplexity_ask
Engages in a conversation using the Sonar API for web-informed responses.

**Parameters:**
- `messages`: Array of conversation messages, each with:
  - `role`: Message role (e.g., system, user, assistant)
  - `content`: The content of the message

**Usage:**
```bash
mcp__perplexity__perplexity_ask(messages=[
    {"role": "user", "content": "What are the latest React 18 features?"}
])
```

This tool provides AI-powered web search and research capabilities, ideal for finding current information, best practices, and solutions.

### Snap-Happy - Screenshot Tools
```bash
# List available windows (macOS)
ListWindows

# Take screenshot
TakeScreenshot [windowId=123]  # Specific window
TakeScreenshot                 # Full screen

# Get last screenshot
GetLastScreenshot
```

### IDE Integration
```bash
# Get language diagnostics
getDiagnostics [uri="file:///path/to/file"]

# Execute code in Jupyter kernel
executeCode code="print('hello')"
```

## Direct Tools

### Command Line Tools
```bash
# Always use uv for Python
uv run python script.py
uv add package-name
uv sync

# Git operations
gh pr create --title "Title" --body "Description"
gh api repos/owner/repo/pulls/123/comments

# Database
psql -c "\d tablename"  # When make db-schema isn't enough
```

### File Operations (via Claude)
- `Write`: Create new files
- `Edit`: Modify existing files
- `MultiEdit`: Multiple edits to same file
- `Read`: Read file contents
- `Bash`: Execute shell commands

## Decision Guide

### When to use RepoPrompt MCP Server:
- Surgical file operations
- Reading specific files or line ranges
- Understanding code structure
- Searching for specific patterns
- Making targeted edits

### When to use Make commands:
- Broad codebase analysis
- Running tests and quality checks
- Managing dependencies
- Debugging with centralized logs
- Generating context for AI analysis

### When to use other MCP servers:
- Context7: Latest library documentation
- Perplexity: Web research and current information
- Snap-Happy: Visual inspection of UI
- IDE: Language diagnostics and Jupyter execution

### Key Principles:
1. **Use Make for breadth**: Analysis, context generation, project-wide operations
2. **Use RepoPrompt for depth**: Specific files, surgical edits, targeted searches
3. **Delegate to avoid context pollution**: Use `make ai-*` commands for analysis
4. **Leverage existing infrastructure**: Use `make logs-analyze` instead of manual log inspection

## Examples

### Starting work on a feature:
```bash
make project-status                                   # Current state
mcp__repoprompt__get_file_tree                      # See structure
mcp__repoprompt__read_file "relevant_module.py"     # Inspect files
```

### Understanding architecture:
```bash
make generate-context-python                  # Python overview
make ai-analyze-project PROMPT="explain auth flow" SCOPE=code
```

### Debugging an issue:
```bash
make logs-analyze PROMPT="find errors"        # AI log analysis
mcp__repoprompt__search "error_pattern"      # Find in code
make code-search PATTERN="ErrorClass"        # Broader search
```

### Making changes:
```bash
mcp__repoprompt__get_code_structure "module.py"    # Understand structure
mcp__repoprompt__read_file "module.py" 100 150     # Read specific section
mcp__repoprompt__apply_edits                       # Make changes
make test && make lint                             # Verify
```

---

*This document serves as the single source of truth for tool usage in the project. When in doubt, refer to this guide or ask Arthur for clarification.*