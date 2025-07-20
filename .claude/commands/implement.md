# /implement - Execute Code Changes

You are implementing: **$ARGUMENTS**

## Core Purpose
Execute code changes efficiently while staying grounded in reality. You have powerful tools - use them.

## Your Implementation Toolkit

### 🎯 Before You Start - Get Grounded
```bash
# If there's a plan, load it
ls docs/implementation_plan_*.md
repoprompt: read_file "docs/implementation_plan_feature.md"

# Understand where this feature should go
repoprompt: get_file_tree                          # See overall structure
make generate-context-small && make ai-query FILE="/tmp/codebase-context-small.txt" PROMPT="Where in our codebase do we implement features similar to $ARGUMENTS? List specific files and modules."

# Understand the specific area you're working in
repoprompt: get_code_structure "target_module.py"  # See what exists
make analyze-file FILE="target_module.py"          # Understand patterns

# Find similar implementations
make code-search PATTERN="similar_feature" FILETYPE=py
make generate-context-from-files FILES="result1.py result2.py" && make ai-query FILE="/tmp/codebase-context-files.txt" PROMPT="What patterns do these files use for implementing similar features? What should I follow?"
```

### 🔍 During Implementation - Stay Factual

**Read specific code** (preserve context by loading only what you need):
```bash
repoprompt: read_file "module.py"              # Full file
repoprompt: read_file "module.py" 100 200      # Specific lines
repoprompt: search "ClassName"                 # Find usage patterns
```

**Need documentation or best practices?** (delegate to avoid hallucination):
```bash
# For library/framework documentation
claude -p "Use Context7 MCP server to get the latest FastAPI routing documentation. First use resolve-library-id to find FastAPI, then get-library-docs with topic='routing'. Return only the specific routing patterns and examples relevant to implementing REST endpoints."

# For approach validation  
claude -p "Use Perplexity MCP server to research: What are the current best practices for implementing caching in Python web applications in 2024? Focus on: 1) Redis vs file-based caching trade-offs, 2) Cache invalidation strategies, 3) Specific code patterns. Return a concise summary with code examples."

# For implementation patterns
make generate-context-small && claude -p "Using the attached codebase context, find all examples of how we implement data validation in our existing code. List the files and patterns used. Focus on: 1) Where validation happens, 2) What validation library/approach we use, 3) Common patterns to follow."

# For SQL/database patterns
make db-schema TABLE=relevant_table
```

**Check your work** (get feedback as you go):
```bash
# After each significant change
make lint                                      # Immediate feedback
make test                                      # Verify nothing broke

# Unsure about approach?
make ai-query PROMPT="Is this the right pattern for X?" FILE="my_changes.py"

# Complex implementation?
make analyze-files FILES="my_module.py related.py"  # Get architectural feedback
```

### 🐛 When Things Go Wrong

**Debugging tools**:
```bash
make analyze-logs                              # What do logs say?
make project-status                            # Overall health check
make code-search PATTERN="error_message"       # Find error source

# Get help analyzing a specific error
repoprompt: read_file "problematic_file.py"
make ai-query PROMPT="This file produces error: [paste error]. Looking at the code, what might cause this? Check: 1) Logic errors, 2) Type mismatches, 3) Missing error handling" FILE="problematic_file.py"

# Research the error if it's cryptic
claude -p "Use Perplexity MCP to search for: Python error '[exact error message]'. Find: 1) Common causes, 2) Stack Overflow solutions from 2023-2024, 3) Specific fixes. Return actionable solutions for our context."
```

**Quick fixes** (when you encounter issues):
- Simple fix (<20 lines)? Just do it
- Error seems systemic? Delegate analysis: `make ai-analyze-project PROMPT="Why is X failing?" SCOPE=python`
- Can't figure it out? Stop and explain the situation

## Implementation Patterns

### Pattern 1: Modify Existing Code
```bash
# 1. Find the right file
make code-search PATTERN="feature_to_modify"

# 2. Understand current implementation  
repoprompt: read_file "target.py"
make analyze-file FILE="target.py"

# 3. Make minimal changes
repoprompt: apply_edits "target.py"

# 4. Verify
make test && make lint
```

### Pattern 2: Add New Feature
```bash
# 1. Find where similar features live
repoprompt: get_file_tree
make generate-context-small && make ai-query FILE="/tmp/codebase-context-small.txt" PROMPT="I need to add $ARGUMENTS. Where do similar features live in our codebase? What's our pattern for organizing new features?"

# 2. Check patterns and conventions
make code-search PATTERN="similar_feature"
# Then read the specific files found:
repoprompt: read_file "similar_feature1.py"
repoprompt: read_file "similar_feature2.py"
make analyze-files FILES="similar1.py similar2.py"

# 3. Get current best practices if needed
claude -p "Use Context7 MCP to get documentation for [specific library] about [specific feature]. First resolve-library-id, then get-library-docs. Return concrete implementation examples and patterns."

claude -p "Use Perplexity MCP to find: How do modern Python applications implement $ARGUMENTS? Focus on: 1) Architecture patterns, 2) Common pitfalls, 3) Code examples from 2024. Return actionable patterns I can follow."

# 4. Implement following existing patterns
repoprompt: apply_edits "new_feature.py"

# 5. Continuous verification
make lint  # After each file change
make test  # After feature is complete
```

### Pattern 3: Bug Fix
```bash
# 1. Understand the error
make analyze-logs
make code-search PATTERN="error_location"

# 2. Get context
repoprompt: read_file "buggy_file.py"
make ai-query PROMPT="Why might this cause [error]?" FILE="buggy_file.py"

# 3. Fix with minimal changes

# 4. Verify fix
make test
```

## Remember

- **Load only what you need** - Use repoprompt for surgical file access
- **Delegate research** - Use Context7/Perplexity instead of guessing
- **Get continuous feedback** - Use make commands to verify as you go
- **Stay grounded** - Check database schema, read actual code, use real patterns

You're the coder, but you're not coding blind. Use your tools.