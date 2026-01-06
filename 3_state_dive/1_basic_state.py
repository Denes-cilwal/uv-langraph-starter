from typing import TypedDict
from langgraph.graph import END, StateGraph

# assume this as global state 
class SimpleState(TypedDict):
    count: int


def increment(state: SimpleState) -> SimpleState: 
    return {
        "count": state["count"] + 1
    }

def should_continue(state):
    if(state["count"] < 5): 
        return "continue"
    else: 
        return "stop"


# create graph - we need to provide a blue print here for state graph   
graph = StateGraph(SimpleState)

graph.add_node("increment", increment)

graph.set_entry_point("increment")

graph.add_conditional_edges(
    "increment", 
    should_continue, 
    {
        "continue": "increment", 
        "stop": END
    }
)

app = graph.compile()

state = {
    "count": 0
}

result = app.invoke(state)
print(result)


"""

State Definition (SimpleState): A TypedDict with a single field count that tracks an integer value.


Graph Structure

StateGraph is initialized with SimpleState as the state schema
Node "increment" is added with the increment function
Entry point is set to start at the increment node
Conditional edges create a loop:
If should_continue returns "continue" → loops back to "increment"
If returns "stop" → goes to END

What is StateGraph?

In LangGraph, a StateGraph treats your application like a state machine. 
It works by maintaining a central "State" object—in your code, that's SimpleState—which acts as the system's shared memory.

Nodes (functions like increment) receive the current state, perform a task, and return updates to that state.

Edges use the information in the state to decide where to 
go next (like your should_continue function).

Why use StateGraph instead of MessageGraph?
While MessageGraph exists, it is a specialized and restricted version 
of a StateGraph. Here is why you chose StateGraph for your code:

1. Custom Data Types

StateGraph: Can track any data you want (integers, strings, booleans, or complex objects). 
In your example, you are tracking a simple count: int, which MessageGraph cannot do easily.

MessageGraph: Is strictly limited to an append-only list of chat messages. It cannot track a separate count variable natively.

2. Deprecation Warning
MessageGraph is now deprecated as of LangGraph v1.0.0.

The LangGraph team now recommends using StateGraph for everything.
 Even for chatbots, they suggest using a StateGraph with a specific messages key rather than using the old MessageGraph class.

"""