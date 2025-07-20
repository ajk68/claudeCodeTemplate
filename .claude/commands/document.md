# /document - Update Docs to Reflect Reality

You are documenting: **$ARGUMENTS**

## Why This Command Exists
Code changes faster than docs. Outdated docs waste time. Keep docs minimal, accurate, and evergreen.

## Process

### 1. Find the Right Existing Doc
```bash
# Quick search for where this belongs
make code-search PATTERN="$ARGUMENTS" FILETYPE=md

# Get overview of documentation structure
make ai-analyze-project PROMPT="Where should documentation for $ARGUMENTS go?" SCOPE=full

# If not found, check our standard locations:
ls -la *.md docs/*/*.md .env.example 2>/dev/null
```

### 2. Standard Documentation Locations

**Project Level:**
- `README.md` - What it does, why, quickstart
- `CLAUDE.md` - AI workflow, tools, project patterns
- `SETUP.md` - Developer setup, dependencies, gotchas
- `.env.example` - All env vars with comments

**Technical References** (`docs/technical/`):
- `database.md` - Current schema, indexes, relationships
- `architecture.md` - How components connect, data flow
- `configuration.md` - All config options, defaults, impacts
- `api.md` - Endpoints, auth, examples (if we have an API)

**Planning/Decisions** (`docs/`):
- `PRD-*.md` - Product decisions (already created via /prd)
- `implementation_plan-*.md` - Technical plans (via /architect)
- `decisions/YYYY-MM-DD-*.md` - Why we chose X over Y

**Meta/Learning** (`docs/meta/`):
- `success_patterns.md` - What works well
- `failed_patterns.md` - What to avoid

### 3. Update, Don't Create

**Before creating ANY new doc:**
```bash
# Check if content belongs in existing docs
make ai-query PROMPT="Should documentation for $ARGUMENTS go in an existing file or new file? Check: README, CLAUDE, SETUP, technical docs" 

# Usually the answer is to update existing docs
```

**If you must create a new doc:**
- Get Arthur's approval first
- Use standard locations above
- Keep it focused on one topic

### 4. Write Evergreen Content

❌ **Avoid temporal language:**
- "Previously...", "Recently updated...", "New feature..."
- "Changed from X to Y", "As of version..."

✅ **Write timelessly:**
- State what IS, not what WAS
- Put historical context in decision docs only
- Focus on current behavior

Example:
```markdown
❌ BAD: "We recently switched to PostgreSQL from MySQL"
✅ GOOD: "Uses PostgreSQL for persistence (see docs/decisions/2024-01-15-database-choice.md)"
```

### 5. Documentation Checklist

For any update:
- [ ] Is it accurate? (test examples)
- [ ] Is it findable? (in the right file)
- [ ] Is it evergreen? (no temporal refs)
- [ ] Is it minimal? (just enough)

```bash
# After updating, verify accuracy
make test  # If docs include code examples
make lint  # If docs include code snippets
```

## Quick Reference

**What goes where:**
- User-facing feature → README.md
- Dev setup issue → SETUP.md  
- AI workflow learning → CLAUDE.md
- Config/env var → .env.example + configuration.md
- Database change → database.md (then: `make db-schema` to verify)
- Architecture decision → decisions/YYYY-MM-DD-*.md
- Why we built X → Find the PRD
- How we built X → Find the implementation plan

## Remember

The best documentation:
- Lives where people look for it
- Explains what IS, not what WAS  
- Gets updated immediately after shipping
- Stays minimal - if no one needs it, don't write it

When in doubt, update an existing doc rather than creating a new one.