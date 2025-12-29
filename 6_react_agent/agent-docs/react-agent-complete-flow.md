# Complete ReAct Agent Flow: Step-by-Step Execution Trace

## 🎬 The Journey: From User Input to Final Answer

Let's trace EXACTLY what happens when you run:
```python
result = app.invoke({
    "input": "How many days ago was the latest SpaceX launch?",
    "agent_outcome": None,
    "intermediate_steps": []
})
```

---

## 📍 STEP 0: Initialization (Before User Input)

### What exists in memory:

```python
# 1. LLM is initialized
llm = ChatOpenAI(model="gpt-4")

# 2. Tools are created
tools = [
    get_system_time,  # Tool that returns current date/time
    search_tool       # Tool that searches the web
]

# 3. Agent runnable is created
react_agent_runnable = create_react_agent(llm, tools, react_prompt)
# This runnable knows:
# - How to format prompts with tool descriptions
# - How to parse LLM responses
# - How to detect AgentAction vs AgentFinish

# 4. Graph is compiled
graph = StateGraph(AgentState)
graph.add_node("reason_node", reason_node)
graph.add_node("act_node", act_node)
# ... (edges defined)
app = graph.compile()

# The graph structure in memory:
#     START
#       ↓
#   reason_node ←─────┐
#       ↓              │
#   (conditional)      │
#    ↙     ↘          │
#  END    act_node ───┘
```

---

## 📍 STEP 1: User Invokes the Graph

```python
result = app.invoke({
    "input": "How many days ago was the latest SpaceX launch?",
    "agent_outcome": None,
    "intermediate_steps": []
})
```

### What happens internally:

**1.1 LangGraph receives the initial state:**
```python
state = {
    "input": "How many days ago was the latest SpaceX launch?",
    "agent_outcome": None,
    "intermediate_steps": []
}
```

**1.2 LangGraph looks at the graph structure:**
```
Entry point = "reason_node"
```

**1.3 LangGraph executes:** `reason_node(state)`

---

## 📍 STEP 2: First `reason_node` Execution

### Code being executed:
```python
def reason_node(state: AgentState):
    agent_input = {
        "input": state["input"],
        "intermediate_steps": state["intermediate_steps"]
    }
    agent_outcome = react_agent_runnable.invoke(agent_input)
    return {"agent_outcome": agent_outcome}
```

### What happens step by step:

**2.1 Extract input from state:**
```python
agent_input = {
    "input": "How many days ago was the latest SpaceX launch?",
    "intermediate_steps": []  # Empty on first run
}
```

**2.2 Invoke `react_agent_runnable`:**
```python
agent_outcome = react_agent_runnable.invoke(agent_input)
```

**2.3 Inside `react_agent_runnable`:**

The runnable does this:

**2.3.1 Format the prompt:**
```python
# The prompt template gets filled with:
prompt = f"""Answer the following questions as best you can. You have access to the following tools:

get_system_time: Returns the current date and time in the specified format.
tavily_search_results_json: A search engine. Useful for when you need to answer questions about current events.

Use the following format:

Question: the input question you must answer
Thought: you should always think about what to do
Action: the action to take, should be one of [get_system_time, tavily_search_results_json]
Action Input: the input to the action
Observation: the result of the action
... (this Thought/Action/Action Input/Observation can repeat N times)
Thought: I now know the final answer
Final Answer: the final answer to the original input question

Begin!

Question: How many days ago was the latest SpaceX launch?
Thought: """
```

**2.3.2 Send to GPT-4:**
```python
llm.invoke(prompt)
```

**2.3.3 GPT-4 thinks and responds:**
```
Thought: To answer this question, I need to know today's date and the date of the latest SpaceX launch. Let me first get the current date.
Action: get_system_time
Action Input: {"format": "%Y-%m-%d"}
```

**2.3.4 Parse GPT-4's response:**
```python
# The agent runnable detects "Action: get_system_time"
# It creates an AgentAction object:
agent_outcome = AgentAction(
    tool="get_system_time",
    tool_input={"format": "%Y-%m-%d"},
    log="Thought: To answer this question, I need to know today's date..."
)
```

**2.4 Return from `reason_node`:**
```python
return {"agent_outcome": agent_outcome}
```

### State after `reason_node`:
```python
state = {
    "input": "How many days ago was the latest SpaceX launch?",
    "agent_outcome": AgentAction(
        tool="get_system_time",
        tool_input={"format": "%Y-%m-%d"},
        log="Thought: To answer this question..."
    ),
    "intermediate_steps": []
}
```

---

## 📍 STEP 3: Conditional Edge Evaluation

### Code being executed:
```python
def should_continue(state: AgentState) -> str:
    if isinstance(state["agent_outcome"], AgentFinish):
        return END
    else:
        return ACT_NODE
```

### What happens:

**3.1 LangGraph calls `should_continue(state)`**

**3.2 Check the type:**
```python
isinstance(state["agent_outcome"], AgentFinish)  # False
isinstance(state["agent_outcome"], AgentAction)  # True
```

**3.3 Return:**
```python
return ACT_NODE  # Which equals "act_node"
```

**3.4 LangGraph routes:**
```
reason_node → act_node
```

---

## 📍 STEP 4: First `act_node` Execution

### Code being executed:
```python
def act_node(state: AgentState):
    agent_action = state["agent_outcome"]
    tool_name = agent_action.tool
    tool_input = agent_action.tool_input
    
    # Find the tool
    tool_function = None
    for tool in tools:
        if tool.name == tool_name:
            tool_function = tool
            break
    
    # Execute the tool
    output = tool_function.invoke(tool_input)
    
    # Return as tuple
    return {"intermediate_steps": [(agent_action, str(output))]}
```

### What happens step by step:

**4.1 Extract the action:**
```python
agent_action = state["agent_outcome"]
# AgentAction(tool="get_system_time", tool_input={"format": "%Y-%m-%d"})

tool_name = "get_system_time"
tool_input = {"format": "%Y-%m-%d"}
```

**4.2 Find the tool function:**
```python
for tool in tools:
    if tool.name == "get_system_time":
        tool_function = get_system_time  # Found it!
        break
```

**4.3 Execute the tool:**
```python
output = tool_function.invoke({"format": "%Y-%m-%d"})
# This calls: get_system_time(format="%Y-%m-%d")
```

**4.4 Inside `get_system_time`:**
```python
@tool
def get_system_time(format: str = "%Y-%m-%d %H:%M:%S"):
    current_time = datetime.datetime.now()  # Gets: 2025-12-29 14:30:00
    formatted_time = current_time.strftime(format)  # Formats: "2025-12-29"
    return formatted_time  # Returns: "2025-12-29"
```

**4.5 Create the tuple:**
```python
new_step = (agent_action, "2025-12-29")
```

**4.6 Return from `act_node`:**
```python
return {"intermediate_steps": [(agent_action, "2025-12-29")]}
```

**4.7 LangGraph merges with existing state:**
```python
# Old state:
old_intermediate_steps = []

# New update:
new_intermediate_steps = [(agent_action, "2025-12-29")]

# Merged (thanks to operator.add):
final_intermediate_steps = [] + [(agent_action, "2025-12-29")]
# Result: [(agent_action, "2025-12-29")]
```

### State after `act_node`:
```python
state = {
    "input": "How many days ago was the latest SpaceX launch?",
    "agent_outcome": AgentAction(tool="get_system_time", ...),
    "intermediate_steps": [
        (
            AgentAction(tool="get_system_time", tool_input={"format": "%Y-%m-%d"}),
            "2025-12-29"
        )
    ]
}
```

**4.8 LangGraph checks edges:**
```
act_node has unconditional edge to: reason_node
```

**4.9 LangGraph routes:**
```
act_node → reason_node
```

---

## 📍 STEP 5: Second `reason_node` Execution

### Same code executes again:
```python
def reason_node(state: AgentState):
    agent_input = {
        "input": state["input"],
        "intermediate_steps": state["intermediate_steps"]
    }
    agent_outcome = react_agent_runnable.invoke(agent_input)
    return {"agent_outcome": agent_outcome}
```

### What happens:

**5.1 Extract input from state:**
```python
agent_input = {
    "input": "How many days ago was the latest SpaceX launch?",
    "intermediate_steps": [
        (AgentAction(tool="get_system_time", ...), "2025-12-29")
    ]
}
```

**5.2 Format the prompt (now with history):**
```python
prompt = f"""Answer the following questions as best you can. You have access to the following tools:

get_system_time: Returns the current date and time in the specified format.
tavily_search_results_json: A search engine...

Use the following format:
Question: the input question you must answer
Thought: you should always think about what to do
Action: the action to take
Action Input: the input to the action
Observation: the result of the action

Begin!

Question: How many days ago was the latest SpaceX launch?
Thought: To answer this question, I need to know today's date...
Action: get_system_time
Action Input: {{"format": "%Y-%m-%d"}}
Observation: 2025-12-29  ← THIS IS NEW!
Thought: """
```

**5.3 GPT-4 sees the observation and thinks:**
```
Thought: Now I know today's date is 2025-12-29. I need to find out when the latest SpaceX launch was.
Action: tavily_search_results_json
Action Input: {"query": "latest SpaceX launch date December 2024"}
```

**5.4 Parse GPT-4's response:**
```python
agent_outcome = AgentAction(
    tool="tavily_search_results_json",
    tool_input={"query": "latest SpaceX launch date December 2024"},
    log="Thought: Now I know today's date..."
)
```

**5.5 Return from `reason_node`:**
```python
return {"agent_outcome": agent_outcome}
```

### State after second `reason_node`:
```python
state = {
    "input": "How many days ago was the latest SpaceX launch?",
    "agent_outcome": AgentAction(
        tool="tavily_search_results_json",
        tool_input={"query": "latest SpaceX launch date December 2024"}
    ),
    "intermediate_steps": [
        (AgentAction(tool="get_system_time", ...), "2025-12-29")
    ]
}
```

---

## 📍 STEP 6: Conditional Edge (Again)

```python
should_continue(state)
# Checks: isinstance(agent_outcome, AgentFinish)? → No
# Returns: ACT_NODE
```

**Routes to:** `act_node`

---

## 📍 STEP 7: Second `act_node` Execution

### What happens:

**7.1 Extract the action:**
```python
tool_name = "tavily_search_results_json"
tool_input = {"query": "latest SpaceX launch date December 2024"}
```

**7.2 Find and execute the tool:**
```python
tool_function = search_tool
output = search_tool.invoke({"query": "latest SpaceX launch date December 2024"})
```

**7.3 Tavily searches the web and returns:**
```python
output = [
    {
        "title": "SpaceX launches Starlink mission",
        "url": "https://...",
        "content": "SpaceX successfully launched a Falcon 9 rocket carrying Starlink satellites on December 21, 2024..."
    },
    # ... more results
]
```

**7.4 Convert to string:**
```python
str(output)
# "[{'title': 'SpaceX launches...', 'content': '...December 21, 2024...'}]"
```

**7.5 Return from `act_node`:**
```python
return {
    "intermediate_steps": [
        (
            AgentAction(tool="tavily_search...", ...),
            "[{'title': 'SpaceX...', 'content': '...December 21, 2024...'}]"
        )
    ]
}
```

**7.6 LangGraph merges:**
```python
old_steps = [(get_system_time action, "2025-12-29")]
new_steps = [(search action, "[{search results}]")]

merged = [
    (get_system_time action, "2025-12-29"),
    (search action, "[{search results}]")
]
```

### State after second `act_node`:
```python
state = {
    "input": "How many days ago was the latest SpaceX launch?",
    "agent_outcome": AgentAction(tool="tavily_search...", ...),
    "intermediate_steps": [
        (AgentAction(tool="get_system_time", ...), "2025-12-29"),
        (AgentAction(tool="tavily_search...", ...), "[{...December 21, 2024...}]")
    ]
}
```

**7.7 Routes to:** `reason_node`

---

## 📍 STEP 8: Third `reason_node` Execution

### What happens:

**8.1 Format the prompt with FULL history:**
```python
prompt = f"""Answer the following questions as best you can. You have access to the following tools:

get_system_time: Returns the current date and time...
tavily_search_results_json: A search engine...

Begin!

Question: How many days ago was the latest SpaceX launch?
Thought: To answer this question, I need to know today's date...
Action: get_system_time
Action Input: {{"format": "%Y-%m-%d"}}
Observation: 2025-12-29
Thought: Now I know today's date is 2025-12-29. I need to find out when the latest SpaceX launch was.
Action: tavily_search_results_json
Action Input: {{"query": "latest SpaceX launch date December 2024"}}
Observation: [{{'title': 'SpaceX launches...', 'content': '...December 21, 2024...'}}]
Thought: """
```

**8.2 GPT-4 thinks:**
```
Thought: Perfect! I now have all the information I need. Today is December 29, 2024, and the latest SpaceX launch was on December 21, 2024. That's 8 days ago.
Final Answer: The latest SpaceX launch was 8 days ago on December 21, 2024.
```

**8.3 Parse GPT-4's response:**
```python
# The agent runnable detects "Final Answer:"
# It creates an AgentFinish object:
agent_outcome = AgentFinish(
    return_values={
        "output": "The latest SpaceX launch was 8 days ago on December 21, 2024."
    },
    log="Thought: Perfect! I now have all the information..."
)
```

**8.4 Return from `reason_node`:**
```python
return {"agent_outcome": agent_outcome}
```

### State after third `reason_node`:
```python
state = {
    "input": "How many days ago was the latest SpaceX launch?",
    "agent_outcome": AgentFinish(
        return_values={"output": "The latest SpaceX launch was 8 days ago on December 21, 2024."}
    ),
    "intermediate_steps": [
        (AgentAction(tool="get_system_time", ...), "2025-12-29"),
        (AgentAction(tool="tavily_search...", ...), "[{...December 21, 2024...}]")
    ]
}
```

---

## 📍 STEP 9: Final Conditional Edge

### What happens:

**9.1 LangGraph calls `should_continue(state)`:**
```python
isinstance(state["agent_outcome"], AgentFinish)  # TRUE!
```

**9.2 Return:**
```python
return END
```

**9.3 LangGraph routes:**
```
reason_node → END
```

---

## 📍 STEP 10: Graph Execution Completes

### What happens:

**10.1 LangGraph returns the final state:**
```python
result = {
    "input": "How many days ago was the latest SpaceX launch?",
    "agent_outcome": AgentFinish(
        return_values={"output": "The latest SpaceX launch was 8 days ago on December 21, 2024."}
    ),
    "intermediate_steps": [
        (AgentAction(tool="get_system_time", ...), "2025-12-29"),
        (AgentAction(tool="tavily_search...", ...), "[{...December 21, 2024...}]")
    ]
}
```

**10.2 User code extracts the answer:**
```python
print(result["agent_outcome"].return_values["output"])
# Prints: "The latest SpaceX launch was 8 days ago on December 21, 2024."
```

---

## 📊 Complete Flow Visualization

```
USER INPUT
    ↓
┌─────────────────────────────────────────────────────────┐
│ ITERATION 1                                             │
├─────────────────────────────────────────────────────────┤
│ reason_node:                                            │
│   State IN: {outcome: None, steps: []}                  │
│   LLM decides: Use get_system_time                      │
│   State OUT: {outcome: AgentAction(get_time), steps: []}│
│                          ↓                               │
│ should_continue: Returns ACT_NODE                       │
│                          ↓                               │
│ act_node:                                               │
│   Executes: get_system_time()                          │
│   Gets: "2025-12-29"                                    │
│   State OUT: {steps: [(get_time, "2025-12-29")]}       │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│ ITERATION 2                                             │
├─────────────────────────────────────────────────────────┤
│ reason_node:                                            │
│   State IN: {steps: [(get_time, "2025-12-29")]}        │
│   LLM sees: "Today is 2025-12-29"                      │
│   LLM decides: Search for SpaceX launch                │
│   State OUT: {outcome: AgentAction(search), ...}        │
│                          ↓                               │
│ should_continue: Returns ACT_NODE                       │
│                          ↓                               │
│ act_node:                                               │
│   Executes: search("SpaceX launch")                    │
│   Gets: "[{...Dec 21, 2024...}]"                       │
│   State OUT: {steps: [(get_time, "..."), (search, "...")]}│
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│ ITERATION 3                                             │
├─────────────────────────────────────────────────────────┤
│ reason_node:                                            │
│   State IN: {steps: [(get_time, "..."), (search, "...")]}│
│   LLM sees: "Today: Dec 29, Launch: Dec 21"           │
│   LLM calculates: 29 - 21 = 8 days                     │
│   LLM decides: I have the answer!                      │
│   State OUT: {outcome: AgentFinish("8 days ago"), ...}  │
│                          ↓                               │
│ should_continue: Returns END                            │
└─────────────────────────────────────────────────────────┘
                          ↓
                      FINAL ANSWER
           "8 days ago on December 21, 2024"
```

---

## 🔑 Key State Transitions Summary

| Step | Node | `agent_outcome` | `intermediate_steps` | Next Node |
|------|------|----------------|---------------------|-----------|
| 1 | reason | `AgentAction(get_time)` | `[]` | act |
| 2 | act | `AgentAction(get_time)` | `[(get_time, "2025-12-29")]` | reason |
| 3 | reason | `AgentAction(search)` | `[(get_time, "2025-12-29")]` | act |
| 4 | act | `AgentAction(search)` | `[(get_time, ...), (search, ...)]` | reason |
| 5 | reason | `AgentFinish("8 days ago")` | `[(get_time, ...), (search, ...)]` | END |

---

## 💡 The Magic Behind the Scenes

### **Why `intermediate_steps` grows:**
```python
# operator.add makes this happen automatically:
old_steps + new_steps = combined_steps
```

### **Why the loop continues:**
```python
# As long as agent_outcome is AgentAction:
should_continue(state) → ACT_NODE → act_node → reason_node → (repeat)

# When agent_outcome becomes AgentFinish:
should_continue(state) → END → (stop)
```

### **Why the agent remembers:**
```python
# Every time reason_node executes, it sees the full history:
prompt = f"""
Observation: 2025-12-29
Observation: [{search results}]
"""
# The LLM uses this to make informed decisions
```