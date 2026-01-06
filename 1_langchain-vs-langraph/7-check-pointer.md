# Human-in-the-Loop with LangGraph

## Checkpointer in LangGraph

A checkpointer is a persistence layer that saves the state of your graph at each step. Think of it like a save game feature - it stores snapshots of your application's state so you can:

- **Resume interrupted workflows** - If your application crashes, you can pick up where you left off
- **Time travel** - Go back to any previous state in the execution
- **Enable human-in-the-loop** - Pause execution, wait for human input, then continue
- **Debug** - Inspect what happened at each step

### Common Checkpointer Implementations

- **MemorySaver** - Stores checkpoints in memory (temporary)
- **SqliteSaver** - Stores in SQLite database (persistent)
- **PostgresSaver** - Stores in PostgreSQL (production-ready)

```python
from langgraph.checkpoint.memory import MemorySaver

checkpointer = MemorySaver()
graph = graph.compile(checkpointer=checkpointer)
```

## Snapshots and Storing

Snapshots are the actual saved states captured by the checkpointer. Each snapshot contains:

The current values of all state variables
Which node was just executed
Metadata about the execution

The checkpointer stores these snapshots using a thread_id (conversation/session identifier) so you can have multiple independent execution threads.
python# Each invocation with same thread_id continues from last checkpoint
config = {"configurable": {"thread_id": "conversation-1"}}
result = graph.invoke(input, config)
Human-in-the-Loop
Human-in-the-loop means pausing the graph execution to wait for human input before continuing. This is useful for:

Getting approval before taking actions
Collecting additional information
Reviewing AI decisions

You implement this by:

Using interrupt_before or interrupt_after when compiling:

pythongraph = graph.compile(
checkpointer=checkpointer,
interrupt_before=["human_review_node"]
)

The graph pauses at that node and returns control to you
You can then:

Inspect the current state
Modify the state if needed
Resume execution with graph.invoke(None, config)

Example flow:
python# Initial run - stops before human_review_node
config = {"configurable": {"thread_id": "1"}}
result = graph.invoke({"input": "data"}, config)

# Check current state

state = graph.get_state(config)
print(state.values) # See what the AI did

# Optionally update state

graph.update_state(config, {"approved": True})

# Resume execution

result = graph.invoke(None, config) # Continues from checkpoint
The key is that checkpointers make all of this possible by preserving state between invocations, allowing you to stop, inspect, modify, and resume your graph execution at any point.
