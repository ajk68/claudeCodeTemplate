# Agent Superpowers Upgrade Plan

## Problem Statement

Our current agents are using inefficient basic tools (grep, read) when powerful make commands are available. The archived commands had access to specialized tools that made them extremely efficient. This plan outlines how to upgrade our agents with these same superpowers.

## Missing Superpowers Analysis

### 1. Context Generation Tools
**Current:** Agents use multiple grep/read operations, missing context
**Superpower:** `make generate-context-*` commands that provide:
- `generate-context-full` - Complete codebase (~145K tokens)
- `generate-context-code` - Code only, no docs/tests (~70K tokens)  
- `generate-context-python` - Python files only (~40K tokens)
- `generate-context-small` - Compressed core code (~60K tokens)
- `generate-context-from-files` - Specific files context

### 2. AI Delegation Tools
**Current:** Agents work in isolation, no external AI help
**Superpower:** `make ai-*` commands for intelligent analysis:
- `ai-query` - Smart model selection for file/code queries
- `ai-analyze-project` - Codebase-wide analysis
- `analyze-file` - Single file architecture review
- `analyze-files` - Multi-file architecture review
- `review-diff` - Git diff analysis

### 3. Database Tools
**Current:** Agents guess database structure
**Superpower:** `make db-schema` - Direct schema inspection

### 4. Testing & Quality Tools
**Current:** No testing integration
**Superpower:** Testing and quality commands:
- `make test` - Run all tests
- `make test-coverage` - Coverage reports
- `make lint` - Code quality checks
- `make lint-fix` - Auto-fix issues
- `make format` - Code formatting

### 5. Search & Navigation Tools
**Current:** Basic grep operations
**Superpower:** `make code-search` - Fast ripgrep-based search

### 6. Logging & Debugging Tools
**Current:** No log analysis capability
**Superpower:** Log analysis tools:
- `make analyze-logs` - AI analysis of logs
- `make logs-watch` - Real-time log monitoring
- `make dev` - Process management with logging

### 7. Project Status Tools
**Current:** Manual git commands
**Superpower:** `make project-status` - Comprehensive status summary

## Agent-Specific Upgrade Plan

### 1. Orchestrator Agent
**Add Tools:**
- `make generate-context-small` - For quick architectural overview
- `make ai-analyze-project` - For understanding implementation scope
- `make project-status` - For current state assessment
- `make db-schema` - When database work is involved

**Usage Pattern:**
```bash
# Start with project overview
make generate-context-small
make ai-query FILE="/tmp/codebase-context-small.txt" PROMPT="Architecture for: [task]"

# Check current state
make project-status
```

### 2. Smart-Implementer Agent
**Add Tools:**
- `make test` - Run tests after changes
- `make lint-fix` - Fix code issues
- `make format` - Ensure consistent formatting
- `make code-search` - Find similar patterns
- `make analyze-logs` - Debug failures

**Usage Pattern:**
```bash
# Before implementing
make code-search PATTERN="similar_function" FILETYPE=py

# After implementing
make test
make lint-fix
make format
```

### 3. Context-Keeper Agent
**Add Tools:**
- `make project-status` - Track git state
- `make generate-context-from-files` - Focus on changed files
- `make ai-analyze-project` - Extract patterns

**Usage Pattern:**
```bash
# Weekly distillation
make generate-context-code
make ai-analyze-project PROMPT="Extract recurring patterns" SCOPE=code
```

### 4. Code-Explorer Agent
**Add Tools:**
- `make generate-context-*` - All context generation variants
- `make code-search` - Primary search tool
- `make ai-query` - Analyze search results
- `make db-schema` - Database exploration

**Usage Pattern:**
```bash
# Efficient search
make code-search PATTERN="class.*Controller" FILETYPE=py
make generate-context-from-files FILES="found_files"
```

### 5. Planner Agent
**Add Tools:**
- `make generate-context-small` - Architectural overview
- `make ai-analyze-project` - Feasibility analysis
- `make db-schema` - Database planning

### 6. Context-Analyzer Agent
**Add Tools:**
- All `make generate-context-*` commands
- `make ai-analyze-project` - Deep analysis

## New Agents to Add

### 7. Code-Reviewer Agent (NEW)
**Purpose:** Peer review of code changes, not quality gate
**Tools:**
- `make review-diff` - Primary review tool
- `make analyze-files` - Deep dive on specific files
- `make test` - Verify functionality
- `make lint` - Check code quality
- `make ai-analyze-project` - Pattern comparison

**Personality:** Thoughtful colleague providing observations, not judgments

### 8. Shipper Agent (NEW)
**Purpose:** Final quality gate before deployment
**Tools:**
- `make review-diff` - Final review
- `make test` - Run all tests
- `make lint` - Quality check
- `make format` - Clean up code
- Git commands for committing

**Personality:** Pragmatic deployer balancing quality with shipping

## Implementation Strategy

### Phase 1: Tool Integration (2 hours)
1. Update each agent's system prompt to include make commands
2. Add usage examples showing when to use each tool
3. Emphasize efficiency: "Use make commands instead of manual operations"

### Phase 2: New Agents (1 hour)
1. Create code-reviewer agent with review tools
2. Create shipper agent with deployment tools
3. Update command structure to include new agents

### Phase 3: Testing & Refinement (1 hour)
1. Test each upgraded agent with real tasks
2. Measure efficiency improvement (fewer tool calls)
3. Refine tool selection patterns

## Success Metrics

1. **Efficiency:** 50% reduction in tool calls for same tasks
2. **Coverage:** No more "missing context" issues
3. **Quality:** Tests run automatically during implementation
4. **Speed:** Context generation in 1 command vs 20+ reads

## Anti-Patterns to Avoid

1. **Don't cascade make commands** - Each agent should use 2-3 strategic commands
2. **Don't duplicate context** - Generate once, analyze once
3. **Don't skip make for simple tasks** - Single file reads are still OK
4. **Don't over-delegate** - Agents should do work, not just call make

## Migration Checklist

- [ ] Update orchestrator with make tools
- [ ] Update smart-implementer with testing tools
- [ ] Update code-explorer with search tools
- [ ] Update context-keeper with analysis tools
- [ ] Update planner with planning tools
- [ ] Update context-analyzer with all context tools
- [ ] Create code-reviewer agent
- [ ] Create shipper agent
- [ ] Test all workflows with new tools
- [ ] Document best practices in AGENT_ARCHITECTURE.md

## Example: Before vs After

### Before (Code-Explorer searching for a pattern):
```
1. grep "class.*Controller"
2. read file1.py
3. read file2.py
4. grep "def.*init"
5. read file3.py
... (20+ operations)
```

### After (Code-Explorer with superpowers):
```
1. make code-search PATTERN="class.*Controller" FILETYPE=py
2. make generate-context-from-files FILES="controllers.py auth.py"
3. make ai-query FILE="/tmp/context.txt" PROMPT="Analyze controller patterns"
(3 operations, comprehensive results)
```

This upgrade will transform our agents from manual laborers to power users, leveraging all the sophisticated tooling that made the archived commands so effective.