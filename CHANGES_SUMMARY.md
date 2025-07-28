# Summary of Changes

## New Features Added

### 1. AI Agents System
Added 10 specialized AI agents in `.claude/agents/`:
- **coordinator** - Coordinates complex multi-step tasks
- **system-analyst** - Codebase analysis and pattern detection
- **developer** - Executes code changes with precision
- **analyst** - Strategic planning and PRD creation
- **searcher** - Intelligent code discovery and analysis
- **documenter** - Maintains project institutional memory
- **documentation-writer** - Evergreen documentation maintenance
- **tester** - Pragmatic high-impact testing
- **reviewer** - Peer review observations
- **quality-gate** - Final deployment checks

### 2. Command Reorganization
- Archived old commands to `.claude/commands/archive/`
- Added new commands:
  - `/fix` - Debug and resolve issues systematically
  - `/project-status` - Replaces `/status` for better clarity
- Updated existing commands to use agent system

### 3. MCP Server Tools
- Added exact MCP tool names for all agents
- Configured RepoPrompt tools with `mcp__repoprompt__` prefix
- Added Context7 tools for library documentation
- Added Perplexity for web search (replacing Brave)
- Proper tool access control (read-only for reviewers, write for developers)

### 4. Install Script
- Created `install.py` for selective component installation
- Supports diff viewing before overwriting
- Allows selective installation of agents, commands, etc.

### 5. Documentation Updates
- Created `docs/AVAILABLE_TOOLS.md` with comprehensive tool reference
- Created `docs/AGENT_ARCHITECTURE.md` explaining agent system
- Updated all references to use exact MCP tool names
- Added proper agent descriptions in template guide

## Updated Files

### Documentation
- `TEMPLATE_GUIDE.md` - Updated with agent system, new commands, install script
- `README.md` - Updated command references and tool examples
- `SETUP_CHECKLIST.md` - Updated workflow examples

### Configuration
- `.env-example` - Added new API keys
- `CLAUDE.md` - Updated with agent system references

### Commands
- Updated `/brainstorm` and `/implement` to use agents
- Archived old commands that are now handled by agents

## Key Improvements

1. **Better Specialization** - Each agent has specific tools and responsibilities
2. **Tool Access Control** - Write tools only for agents that need them
3. **Clearer Documentation** - Exact tool names prevent confusion
4. **Selective Installation** - Install only what you need with install.py
5. **Agent-Based Workflows** - Commands now delegate to specialized agents

## Migration Notes

- `/status` is now `/project-status`
- Archived commands are in `.claude/commands/archive/` for reference
- Use exact MCP tool names (e.g., `mcp__repoprompt__search` not `search`)
- Agents handle most workflows that previously required specific commands