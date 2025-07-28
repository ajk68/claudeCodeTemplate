# Export Chat for Analysis

Export recent Claude chat conversations for analysis using the tools/claude_chat_analyzer.py tool.

## Quick Start

1. **Run discovery to see projects** (I'll show 3 most recent first)
   ```bash
   uv run python make/tools/claude_chat_analyzer.py
   ```

2. **Export with proper formatting** (use `--projects=` with equals sign):
   ```bash
   # IMPORTANT: Use --projects= (with equals) for complex project names
   uv run python make/tools/claude_chat_analyzer.py --projects="[PROJECT-NAME]" --max-age="2d"
   ```

## Process

1. **Discover available projects**
   - Shows all projects with chat history
   - **NEW**: Top 3 most recently active projects highlighted
   - **NEW**: Suggests relevant projects based on activity
   - Project names, file counts, latest activity, total size

2. **Choose export parameters**
   - **Projects**: Use exact project name from discovery (copy-paste recommended)
   - **Time range**: How far back (e.g., "2h", "3d", "1w")
   
3. **Export conversations**
   
   **Critical formatting rules:**
   ```bash
   # For projects with special characters (dashes, spaces, etc.)
   # USE: --projects="PROJECT_NAME" (with equals sign)
   uv run python make/tools/claude_chat_analyzer.py --projects="[PROJECT-NAME]" --max-age="2d"
   
   # For simple project names
   # CAN USE: --projects "PROJECT_NAME" (space separated)
   uv run python make/tools/claude_chat_analyzer.py --projects "[SIMPLE-NAME]" --max-age "2d"
   ```
   
   More examples:
   ```bash
   # Export last 2 days from current project (complex name)
   uv run python make/tools/claude_chat_analyzer.py --projects="-Users-arthur-code-carv-ai-coach-research" --max-age="2d"
   
   # Export last week from multiple projects
   uv run python make/tools/claude_chat_analyzer.py --projects="ai-coach-research,ski-analytics" --max-age="1w"
   
   # Export last 6 hours for quick review
   uv run python make/tools/claude_chat_analyzer.py --projects="-Users-arthur-code-carv-ai-coach-research" --max-age="6h"
   ```

4. **Output location**
   **The tool will display the output file path prominently:**
   ```
   ✅ Analysis complete: /tmp/claude-chats-20250717-084609.txt
   ```
   Copy this path to use in analysis!

## Suggested Analysis Prompts

After export, use these prompts with the packed file:

### Pattern Analysis
```
Analyze the attached Claude chat export and identify:
1. Recurring problem-solving patterns
2. Common mistakes or inefficiencies
3. Successful strategies that worked well
4. Areas where I could improve my prompting
```

### Technical Learning
```
Review the attached chat export and extract:
1. Key technical concepts learned
2. Code patterns that were frequently used
3. Debugging approaches that succeeded/failed
4. Architectural decisions and their rationale
```

### Meta Documentation
```
Based on the attached chat export, create:
1. A summary of major accomplishments
2. Lessons learned and best practices discovered
3. Common pitfalls to avoid in future
4. Recommendations for CLAUDE.md updates
```

### Project Progress
```
Analyze the attached export to document:
1. Features implemented and their status
2. Technical debt introduced or resolved
3. Next logical steps for the project
4. Time estimates based on past velocity
```

## Common Use Cases

### Recent Debugging Session
Export the last few hours to review problem-solving approaches:
```bash
uv run python make/tools/claude_chat_analyzer.py --projects "ai-coach-research" --max-age 4h
```

### Weekly Progress Review
Export a week's worth of conversations:
```bash
uv run python make/tools/claude_chat_analyzer.py --projects "ai-coach-research" --max-age 1w
```

### Multi-Project Analysis
Compare work across projects:
```bash
uv run python make/tools/claude_chat_analyzer.py --projects "project1,project2,project3" --max-age 3d
```

## Next Steps

After export, you can:
1. Review the packed file manually
2. Use another Claude session to analyze patterns
3. Extract specific insights or learnings
4. Create meta documentation from the analysis

## Troubleshooting

- **"Project not found"**: Check exact project name from discovery mode
- **"No matching files"**: Try a larger time range (e.g., "1w" instead of "1d")
- **"Repomix not found"**: Install with `npm install -g repomix`
- **Converter errors**: Ensure claude2md is installed: `uv add --dev "claude2md @ git+https://github.com/ajk68/claude2md.git"`