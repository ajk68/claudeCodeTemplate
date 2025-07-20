# /test - Verify It Works Without Overthinking

You are testing: **$ARGUMENTS**

## Core Purpose
Ensure critical functionality works. Skip the rest.

## Quick Test Process

### 1. What Am I Testing?
```bash
# If no specific target given, run smoke test
make test

# If you need specific tests (when ARGUMENTS mentions specific area)
uv run pytest tests/ -k "$ARGUMENTS" -x -v

# For coverage analysis (only when explicitly needed)
make test-coverage
```

### 2. Handle Common Issues

**Numpy/pickle errors?**
```bash
# Regenerate data with current environment
make run-pipeline  # Runs both fetch and build features
```

**Import errors?**
```bash
# Ensure clean environment
make sync  # or make install-python
```

**Cache issues?**
```bash
# Clear all caches
make clear-cache
```

### 3. Quick Test Writing (Only if Critical)

```python
def test_critical_thing():
    """One-liner about what should work"""
    # Given: minimal setup
    # When: the action
    # Then: assert the outcome
    assert actual == expected
```

### 4. Pragmatic Test Results

**✅ All pass?** → "Tests pass. Ready to ship."

**❌ Failures?** → 
```
Test failed: [test_name]
Issue: [one line summary]

Fix with: /implement [specific fix]
Or ship anyway if non-critical.
```

**⚠️ No tests?** → "No tests for this. Ship if low-risk, add test if payment/auth/data."

## Test Only What Matters

**Always test:**
- Payment flows
- Auth/permissions  
- Data integrity
- Previously broken things

**Never test:**
- UI formatting
- Temporary code
- Internal helpers
- Obvious stuff

## Remember

Perfect test coverage = dead startup. Test enough to ship confidently, not comprehensively.

Quick formula: Can this break silently AND hurt users? Test it. Otherwise, ship it.