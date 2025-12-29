# LangGraph ReAct Agent: Complete State Flow Guide

## Graph Structure

### **Nodes**
1. **`reason` node** - The agent's "brain" that decides what to do next
2. **`act` node** - Executes the tool the agent chose
3. **`START`** - Entry point (implicit)
4. **`END`** - Exit point when done

### **Edges**
1. **START → reason** - Solid edge: Always starts at reason node
2. **reason → act** - Solid edge: When `agent_outcome` is `AgentAction`
3. **reason → END** - Dotted edge: When `agent_outcome` is `AgentFinish`
4. **act → reason** - Curved edge: Always loops back after tool execution

---

## State Changes Through the Graph

### **Initial State (at START)**
```python
{
    "input": "What's the capital of France and its population?",
    "agent_outcome": None,
    "intermediate_steps": []
}
```

---

### **Step 1: First Reason Node Execution**

**What happens:**
- Agent receives the input and empty intermediate_steps
- LLM reasons: "I need to search for France's capital"
- Returns an `AgentAction`

**State after reason node:**
```python
{
    "input": "What's the capital of France and its population?",
    "agent_outcome": AgentAction(
        tool="search",
        tool_input="capital of France",
        log="I need to find the capital first"
    ),
    "intermediate_steps": []  # Still empty
}
```

**Edge taken:** reason → act (because `agent_outcome` is `AgentAction`)

---

### **Step 2: First Act Node Execution**

**What happens:**
- Extracts the tool name and input from `agent_outcome`
- Executes: `search("capital of France")`
- Gets observation: "Paris"
- Appends to intermediate_steps

**State after act node:**
```python
{
    "input": "What's the capital of France and its population?",
    "agent_outcome": AgentAction(
        tool="search",
        tool_input="capital of France",
        log="I need to find the capital first"
    ),
    "intermediate_steps": [
        (
            AgentAction(tool="search", tool_input="capital of France", log="..."),
            "Paris"  # observation
        )
    ]
}
```

**Edge taken:** act → reason (always loops back)

---

### **Step 3: Second Reason Node Execution**

**What happens:**
- Agent now sees the previous action and observation
- LLM reasons: "I know the capital is Paris, now I need population"
- Returns another `AgentAction`

**State after reason node:**
```python
{
    "input": "What's the capital of France and its population?",
    "agent_outcome": AgentAction(
        tool="search",
        tool_input="population of Paris",
        log="Now I need to find Paris population"
    ),
    "intermediate_steps": [
        (AgentAction(tool="search", tool_input="capital of France", log="..."), "Paris")
    ]
}
```

**Edge taken:** reason → act

---

### **Step 4: Second Act Node Execution**

**What happens:**
- Executes: `search("population of Paris")`
- Gets observation: "2.1 million"
- Appends to intermediate_steps (thanks to `operator.add`)

**State after act node:**
```python
{
    "input": "What's the capital of France and its population?",
    "agent_outcome": AgentAction(
        tool="search",
        tool_input="population of Paris",
        log="Now I need to find Paris population"
    ),
    "intermediate_steps": [
        (AgentAction(tool="search", tool_input="capital of France", log="..."), "Paris"),
        (AgentAction(tool="search", tool_input="population of Paris", log="..."), "2.1 million")
    ]
}
```

**Edge taken:** act → reason

---

### **Step 5: Third Reason Node Execution**

**What happens:**
- Agent sees both previous actions and observations
- LLM reasons: "I have all the information needed"
- Returns `AgentFinish`

**State after reason node:**
```python
{
    "input": "What's the capital of France and its population?",
    "agent_outcome": AgentFinish(
        return_values={
            "output": "The capital of France is Paris, with a population of 2.1 million."
        },
        log="I have enough information to answer"
    ),
    "intermediate_steps": [
        (AgentAction(tool="search", tool_input="capital of France", log="..."), "Paris"),
        (AgentAction(tool="search", tool_input="population of Paris", log="..."), "2.1 million")
    ]
}
```

**Edge taken:** reason → END (dotted edge, because `agent_outcome` is `AgentFinish`)

---

## How Conditional Edges Work

The conditional edge from the reason node uses a function like:

```python
def should_continue(state: AgentState):
    if isinstance(state["agent_outcome"], AgentFinish):
        return "end"
    else:
        return "continue"
```

This checks the type of `agent_outcome` and routes accordingly:
- `AgentAction` → go to act node
- `AgentFinish` → go to END

---

## Key Points About State Updates

### **`intermediate_steps` with `operator.add`**
```python
Annotated[list[tuple[AgentAction, str]], operator.add]
```

This annotation is crucial:
- **Without it:** Each node would overwrite the list
- **With it:** Each node appends to the existing list

**Example:**
```python
# Act node returns:
{"intermediate_steps": [(new_action, new_observation)]}

# LangGraph automatically combines with existing state:
# old_state["intermediate_steps"] + new_update["intermediate_steps"]
```

### **`agent_outcome` without annotation**
This field gets **replaced** each time, not appended. The reason node always sets a new decision.

---

## Complete Node Implementation Examples

### **Reason Node**
```python
def run_agent_reasoning(state: AgentState):
    agent = create_react_agent(llm, tools)
    
    # Agent sees input and all intermediate_steps
    result = agent.invoke({
        "input": state["input"],
        "intermediate_steps": state["intermediate_steps"]
    })
    
    # Returns AgentAction or AgentFinish
    return {"agent_outcome": result}
```

### **Act Node**
```python
def execute_tools(state: AgentState):
    agent_action = state["agent_outcome"]
    
    # Find and execute the tool
    tool_name = agent_action.tool
    tool_input = agent_action.tool_input
    
    observation = tool_executor.execute(tool_name, tool_input)
    
    # Return a tuple to append to intermediate_steps
    return {
        "intermediate_steps": [(agent_action, observation)]
    }
```

### **Conditional Edge Function**
```python
def should_continue(state: AgentState) -> str:
    if isinstance(state["agent_outcome"], AgentFinish):
        return "end"
    return "continue"
```

---

## Building the Graph

```python
from langgraph.graph import StateGraph, END

workflow = StateGraph(AgentState)

# Add nodes
workflow.add_node("reason", run_agent_reasoning)
workflow.add_node("act", execute_tools)

# Set entry point
workflow.set_entry_point("reason")

# Add conditional edge from reason
workflow.add_conditional_edges(
    "reason",
    should_continue,
    {
        "continue": "act",
        "end": END
    }
)

# Add edge from act back to reason
workflow.add_edge("act", "reason")

# Compile
app = workflow.compile()
```

---

## Execution Timeline

| Step | Node | Input State | Output State | Edge Taken |
|------|------|-------------|--------------|------------|
| 1 | reason | `agent_outcome=None`<br>`intermediate_steps=[]` | `agent_outcome=AgentAction`<br>`intermediate_steps=[]` | reason→act |
| 2 | act | `agent_outcome=AgentAction`<br>`intermediate_steps=[]` | `intermediate_steps=[(action1, obs1)]` | act→reason |
| 3 | reason | `intermediate_steps=[(action1, obs1)]` | `agent_outcome=AgentAction` | reason→act |
| 4 | act | `agent_outcome=AgentAction` | `intermediate_steps=[(action1, obs1), (action2, obs2)]` | act→reason |
| 5 | reason | `intermediate_steps=[(action1, obs1), (action2, obs2)]` | `agent_outcome=AgentFinish` | reason→END |

---

## Why This Pattern is Powerful

1. **Transparency:** You can see exactly what the agent tried and what results it got
2. **Debuggability:** You can inspect state at each step
3. **Modifiability:** You can customize the reason or act nodes
4. **Memory:** `intermediate_steps` gives the agent context of its entire journey
5. **Control:** You decide the routing logic and can add custom conditions

This makes the "black box" of AgentExecutor completely transparent and hackable!


```
┌─────────────────────────────────────────────────────┐
│ reason node executes                                │
│ ├─ Calls create_react_agent(...)                   │
│ └─ Returns: {"agent_outcome": AgentAction/Finish}  │
└─────────────────────────────────────────────────────┘
                       ↓
┌─────────────────────────────────────────────────────┐
│ LangGraph checks conditional edges                  │
│ ├─ Calls should_continue(state)                     │
│ └─ Looks at state["agent_outcome"]                  │
└─────────────────────────────────────────────────────┘
                       ↓
              ┌────────┴────────┐
              ↓                 ↓
    isinstance(AgentFinish)?   isinstance(AgentAction)?
              ↓                 ↓
         return "end"      return "continue"
              ↓                 ↓
      Maps to END         Maps to "act" node


```