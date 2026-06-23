# UUID vs String Type Consistency Fix

## Problem
Type mismatch between UUID and string for `topic_id` across the codebase caused runtime errors when:
- Calling `set_active_context()` which expects `topic_id: str`
- But receiving `UUID` objects from database models or parameters

## Root Cause
Function signature inconsistency:
- `set_active_context(topic_id: str, ...)` expects string
- But callers were passing `UUID` objects from:
  - `complete_lesson(topic_id: UUID, ...)` parameter
  - `next_topic.id` from database query
  - Orchestrator params (could be either type)

## Files Fixed

### 1. app/services/topic_service.py
**Line ~235**: `complete_lesson()` → C3 auto-activate next lesson
```python
# BEFORE
await self.set_active_context(
    topic_id=topic_id,  # UUID passed to function expecting str
    ...
)

# AFTER
await self.set_active_context(
    topic_id=str(topic_id),  # Convert UUID to string
    ...
)
```

**Line ~410**: `submit_quiz()` → C3 auto-activate next topic
```python
# BEFORE
await self.set_active_context(
    topic_id=next_topic.id,  # UUID from model
    ...
)

# AFTER
await self.set_active_context(
    topic_id=str(next_topic.id),  # Convert UUID to string
    ...
)
```

### 2. app/routers/learning_path.py
**Line ~295**: `execute_action()` → COMPLETE_LESSON handler
```python
# BEFORE
result = await _svc.complete_lesson(
    UUID(topic_id),  # Could fail if topic_id is already UUID
    ...
)

# AFTER
topic_uuid = UUID(topic_id) if isinstance(topic_id, str) else topic_id
result = await _svc.complete_lesson(
    topic_uuid,  # Handle both string and UUID
    ...
)
```

**Line ~350**: `execute_action()` → GO_TO_LESSON handler
```python
# BEFORE
await _svc.set_active_context(
    topic_id=UUID(topic_id),  # UUID passed to function expecting str
    ...
)

# AFTER
topic_uuid = UUID(topic_id) if isinstance(topic_id, str) else topic_id
await _svc.set_active_context(
    topic_id=str(topic_uuid),  # Convert to string
    ...
)
```

## Pattern Established
**Golden Rule**: 
- `set_active_context()` ALWAYS receives `topic_id` as **string**
- Before calling, convert UUID to string: `str(topic_id)`
- When receiving from params/dict, handle both types:
  ```python
  topic_uuid = UUID(topic_id) if isinstance(topic_id, str) else topic_id
  await _svc.set_active_context(topic_id=str(topic_uuid), ...)
  ```

## Why String for set_active_context()?
The function stores `topic_id` in `UserProfile.active_topic_id` which is a **VARCHAR** column in PostgreSQL, not UUID. The function already has conversion logic:
```python
profile.active_topic_id = str(topic_id) if topic_id else None
```

So the signature correctly expects string input.

## Impact
✅ C3 auto-activate next lesson now works without type errors
✅ C3 auto-activate next topic after quiz works without type errors  
✅ Orchestrator execute-action handlers work with both UUID/string params
✅ No more "UUID object expected string" runtime errors

## Status: ✅ FIXED
All UUID/string type mismatches resolved. System consistent across all `set_active_context()` calls.
