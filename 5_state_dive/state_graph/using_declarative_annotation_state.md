# Declarative Annotated State in LangGraph

## What is `Annotated` in Python?

In Python, `Annotated` is a way to attach extra metadata to a type hint. It comes from `typing` (or `typing_extensions` in older versions):

```python
from typing import Annotated

Age = Annotated[int, "must be >= 0"]
```

## Understanding `Annotated` in LangGraph

This is **not** just "type annotation for docs". In LangGraph and state-machine patterns, `Annotated[...]` is used to attach a **reducer/merge function** to a state field.

When you see things like `operator.add` or `operator.concat` inside `Annotated`, it means:

> **"If multiple updates happen to this field, combine them using this operator."**

### Example

```python
from typing import Annotated, TypedDict
import operator

class State(TypedDict):
    nums: Annotated[list[int], operator.add]
```

Your list updates accumulate instead of one overwriting the other:

```python
old = [1, 2]
new = [3, 4]
operator.add(old, new)   # => [1, 2, 3, 4]
```

---

## What is Annotated State?

`Annotated[Type, reducer_function]` tells LangGraph **how to merge/combine state updates** instead of just overwriting values.

### The Problem Without Annotation

- **Without `Annotated`**: When a node returns `{"sum": 5}`, it completely **replaces** the old sum value.
- **With `Annotated`**: LangGraph applies a **reducer function** to merge old and new values.

---

## Example: State Definition

```python
class SimpleState(TypedDict):
    count: int                                      # Normal: REPLACES old value
    sum: Annotated[int, operator.add]              # Annotated: ADDS to old value
    history: Annotated[List[int], operator.concat] # Annotated: CONCATENATES lists
```

### What Each Annotation Does

1. **`sum: Annotated[int, operator.add]`**

   - Uses `operator.add` to **add** new value to existing sum
   - Formula: `old_sum + new_value`

2. **`history: Annotated[List[int], operator.concat]`**
   - Uses `operator.concat` to **append** new list to existing list
   - Formula: `old_list + new_list`

---

## Complete Flow Execution

**Initial State**: `{"count": 0, "sum": 0, "history": []}`

### Iteration 1

- `increment` returns: `{"count": 1, "sum": 1, "history": [1]}`
- **count**: `1` (replaced)
- **sum**: `0 + 1 = 1` (added via `operator.add`)
- **history**: `[] + [1] = [1]` (concatenated)
- **Result**: `{"count": 1, "sum": 1, "history": [1]}`

### Iteration 2

- `increment` returns: `{"count": 2, "sum": 2, "history": [2]}`
- **count**: `2` (replaced)
- **sum**: `1 + 2 = 3` (added)
- **history**: `[1] + [2] = [1, 2]` (concatenated)
- **Result**: `{"count": 2, "sum": 3, "history": [1, 2]}`

### Iteration 3

- Returns: `{"count": 3, "sum": 3, "history": [3]}`
- **sum**: `3 + 3 = 6`
- **history**: `[1, 2] + [3] = [1, 2, 3]`

### Iteration 4

- Returns: `{"count": 4, "sum": 4, "history": [4]}`
- **sum**: `6 + 4 = 10`
- **history**: `[1, 2, 3] + [4] = [1, 2, 3, 4]`

### Iteration 5

- Returns: `{"count": 5, "sum": 5, "history": [5]}`
- **sum**: `10 + 5 = 15`
- **history**: `[1, 2, 3, 4] + [5] = [1, 2, 3, 4, 5]`
- **Condition**: `count >= 5` → **STOP**

**Final Result**: `{"count": 5, "sum": 15, "history": [1, 2, 3, 4, 5]}`

---

## Why Use Annotated State?

### Without Annotated State ❌

You'd have to manually write:

```python
return {
    "count": new_count,
    "sum": state["sum"] + new_count,              # Manual addition
    "history": state["history"] + [new_count]     # Manual concatenation
}
```

### With Annotated State ✅

You just return the new value and LangGraph handles the merging:

```python
return {
    "count": new_count,
    "sum": new_count,       # LangGraph auto-adds to existing sum
    "history": [new_count]  # LangGraph auto-concatenates to history
}
```

---

## Benefits

This is **declarative** because you declare **how** to merge values once in the state definition, not in every node function.

✅ **Cleaner code**  
✅ **Less error-prone**  
✅ **Scales better** for complex workflows
