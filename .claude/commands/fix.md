# /fix - Something's Broken

You are fixing: **$ARGUMENTS**

## Process

### 1. Clarify the Crisis
**Quick questions** (pick what matters):
- "What's broken and how bad is it?"
- "What error are you seeing?"
- "When did this break?"

### 2. Find the Problem
Start small, expand as needed:
```bash
# Recent changes often = culprit
git log --oneline -5 --stat

# Search for the error
make code-search PATTERN="error message" FILETYPE=py

# Analyze logs for patterns
make analyze-logs  # Default: last 100 lines of logs/error.log
make analyze-logs LOG_FILE=app.log LINES=200  # Custom log file

# Get project status overview
make project-status
```

### 3. Fix Smart
**Your decision tree:**
- Simple fix (< 20 lines) → Just do it
- Touching 2-3 files → Proceed carefully  
- Major surgery needed → Stop: "This needs /architect first"
- Unclear approach → Use make commands for guidance:
  ```bash
  # Get architectural context for the area
  make analyze-file FILE="broken_module.py"
  
  # Or ask for specific guidance
  make ai-query PROMPT="Best way to fix $ARGUMENTS without breaking X?" FILE="broken_module.py"
  ```

**Remember:** Fix the problem, not the architecture. No refactoring during emergencies.

### 4. Ship It
```bash
# Test just what you fixed
make test  # Or if you need specific tests:
uv run pytest tests/ -k "relevant_test" -v

# Quick quality check
make lint  # Check for obvious issues
```

Then: "Fixed [problem] by [solution]. Ready to ship?"

## Escape Hatches

**If you're making it worse:**
```bash
git stash && git checkout HEAD -- .
```
"Fix attempt failed. Should we roll back the last deployment instead?"

**If it's architectural debt:**
"I can band-aid this now, but the real issue is [root cause]. 
Fix now and add tech debt ticket?"

## You Have Agency

Trust your judgment. If the human says "just make it work," you can:
- Apply quick fixes even if inelegant
- Skip tests if it's truly urgent (but say so)
- Suggest rolling back if that's faster
- Escalate to /architect if the "quick fix" is dangerous

The goal: Restore service fast, then fix properly later.