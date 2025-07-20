# /status - Morning Status Check

Get a clear summary of the current project state without context pollution.

## Process:

Run this command:

```bash
make project-status
```

## ⚡ Quick Actions
Based on the status output, you might want to:
- Run 'uv run pytest tests/' to verify everything works
- Run 'uv run python clear_cache.py all' if seeing stale data
- Continue with '/plan [specific task]' for next steps
- Run 'make clean' to clear caches if needed
- Use 'make ai-analyze-project PROMPT="your question"' for codebase analysis

Keep it concise and actionable.