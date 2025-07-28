# /refactor - Strategic Code Improvement

You are proposing refactoring for: **$ARGUMENTS**

## Why This Command Exists
LLMs are trained to always find something to improve - even perfect code. We need HIGH-ROI improvements that solve real pain, not busy work.

## Process

### 1. Understand the Why (Before Any Analysis)
**Ask Arthur first**:
- "What's the main issue with the current code?"
- "What should the improved version do better?"
- "Is this blocking something important?"

If vague ("make it cleaner"), probe deeper:
- "What specific pain does this cause?"
- "Where does this slow you down?"

### 2. Get External Perspective (If Proceeding)
```bash
# For focused refactoring (1-3 files)
make analyze-files FILES="file1.py file2.py file3.py"

# For broader architectural analysis
make ai-analyze-project PROMPT="Find HIGH-ROI refactoring opportunities in $ARGUMENTS. Focus on: duplication (3+ places), confusing logic, performance bottlenecks, files >1000 lines" SCOPE=python

# For very large scope analysis
make ai-analyze-project PROMPT="Identify major refactoring opportunities" SCOPE=code
```

### 3. Filter and Create Refactoring Plan

**High-ROI targets only**:
- Files >1000 lines that could be split logically
- Code duplication (same logic in 3+ places)
- File duplication (file, file_new, file_v2, etc.)
- Confusing logic that causes real errors
- Performance bottlenecks with measurable impact

**Skip vanity refactoring**:
- "Could be more elegant"
- "Might be useful to abstract"
- "Industry best practices suggest..."
- Additional abstraction layers

### 4. Present Refactoring Plan
```
## Refactoring Plan: [Description]

### Target 1: Split large file (user_service.py - 1450 lines)
- WHY: Hard to navigate, Claude struggles with large files
- WHAT: Split into user_auth.py, user_profile.py, user_admin.py
- IMPACT: Easier maintenance, faster comprehension
- EFFORT: 2 hours

### Target 2: Extract duplicate validation (in 4 places)
- WHY: Bug fixes must be applied 4 times
- WHAT: Create single validate_user_input() function
- IMPACT: Single source of truth
- EFFORT: 1 hour

Total effort: 3 hours
Proceed with this plan?
```

### 5. Check Test Coverage
```bash
# Check if we have tests for affected code
make test  # See overall test status

# For specific area coverage
make test-coverage  # Full coverage report
```

**If insufficient tests**:
```
"This refactoring affects code without adequate test coverage.
 
Should I:
1. Ask you to run /architect to create a safe refactoring plan?
2. Proceed carefully with manual verification?
3. Write tests first (adds ~2 hours)?

I recommend option 1 for safety."
```

### 6. If Tests Exist - Create Implementation Plan
Simple phased approach:
- Phase 1: Verify current tests pass (`make test`)
- Phase 2: Make the refactoring changes
- Phase 3: Verify tests still pass (`make test`)
- Phase 4: Clean up (remove old code, update imports)

**DECISION POINT**: "Ready to execute this refactoring plan?"

## Anti-Patterns to Avoid
❌ "While I'm here" additions  
❌ Premature abstraction  
❌ Style/formatting as "refactoring"  
❌ Renaming for "clarity" without real confusion  

## Remember
Refactoring is about solving real problems:
- Can't find things → Split large files
- Fixing bugs multiple places → Extract duplication  
- Getting wrong results → Simplify confusing logic
- Measurably slow → Optimize bottlenecks

Everything else is vanity.