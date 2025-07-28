# Established Project Patterns
Last Updated: 2025-07-27 by context-keeper
Next Review: 2025-02-03

## Core Conventions

### File Organization
- **Pattern**: Files start with short description comment
- **Example**: `# User authentication and session management`
- **Why**: Easy grepping and context understanding

### Code Style
- **Pattern**: Match existing style over external standards
- **Example**: If codebase uses `snake_case`, continue with `snake_case`
- **Why**: Consistency reduces cognitive load

### Change Philosophy
- **Pattern**: Modify existing code before creating new
- **Example**: Extend existing function rather than create wrapper
- **Why**: Prevents codebase bloat and maintains simplicity

## Architectural Patterns

### API Design
```python
# Standard endpoint structure
def endpoint():
    validate_input()    # Fail fast
    check_permissions() # Security second
    execute_logic()     # Core business logic
    log_activity()      # Audit trail
    return response()   # Consistent format
```
**Used in**: All API endpoints
**Why**: Predictable flow, easier debugging

### Error Handling
```python
# Consistent error responses
try:
    result = operation()
except SpecificError as e:
    log.warning(f"Expected error: {e}")
    return error_response(code="KNOWN_ERROR", message=str(e))
except Exception as e:
    log.error(f"Unexpected error: {e}")
    return error_response(code="INTERNAL_ERROR", message="Something went wrong")
```
**Used in**: All service layers
**Why**: Graceful degradation, clear error tracking

### Data Access
```python
# Repository pattern for data access
class UserRepository:
    def get_by_id(self, user_id: int) -> Optional[User]:
        # Single responsibility: data access only
        pass
```
**Used in**: All database operations
**Why**: Separation of concerns, testability

## Testing Patterns

### Test Structure
```python
# Arrange-Act-Assert pattern
def test_user_creation():
    # Arrange
    user_data = {"name": "Test User", "email": "test@example.com"}
    
    # Act
    user = create_user(user_data)
    
    # Assert
    assert user.name == "Test User"
    assert user.email == "test@example.com"
```
**Used in**: All test files
**Why**: Clear test intent, easy to understand failures

### Mock Strategy
- **Pattern**: Mock external services, not internal components
- **Example**: Mock API calls, not database queries
- **Why**: Tests remain close to production behavior

## Development Workflow Patterns

### Feature Development
1. Create feature branch from main
2. Implement with existing patterns
3. Add tests for new functionality
4. Update documentation if behavior changes
5. Request review before merging

### Code Review Focus
- Correctness first
- Pattern adherence second
- Performance only if measured
- Style consistency last

## Anti-Patterns to Avoid

### ❌ Premature Abstraction
**Don't**: Create generic solution for single use case
**Do**: Wait for 3+ similar cases before abstracting

### ❌ Comment Noise
**Don't**: `# increment i by 1`
**Do**: `# User IDs start at 1000 for legacy compatibility`

### ❌ Kitchen Sink PRs
**Don't**: Fix unrelated issues "while you're there"
**Do**: Keep PRs focused on single concern

### ❌ Test Implementation Details
**Don't**: Test private methods or internal state
**Do**: Test public interface and behavior

## Pattern Evolution

New patterns are promoted from PROJECT-WISDOM after:
- Being used successfully 3+ times
- Proving their value in production
- Team consensus on adoption

Patterns are deprecated when:
- Better alternative emerges
- Original use case no longer exists
- Maintenance burden exceeds value