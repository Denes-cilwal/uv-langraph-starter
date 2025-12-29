# ReAct Agent Pattern

The **ReAct (Reasoning and Acting)** agent pattern is a design framework that enables an AI to solve complex problems by alternating between thinking and taking actions. Unlike a standard chatbot that answers immediately, a ReAct agent follows a structured, iterative loop.

## The ReAct Flowchart

The workflow follows a continuous cycle often visualized as:

```
Goal → [Thought → Action → Observation] → Final Answer
```

## Core Components

### 1. The Reasoning Node (Thought)

The process starts with the LLM analyzing the user's request.

- **Purpose**: The AI breaks the main task into smaller sub-tasks.
- **Logic**: It asks itself, "Do I have enough information to answer this, or do I need to use a tool?".
- **Output**: It generates a verbal "Thought" that serves as its internal monologue and plan.

### 2. The Acting Node (Action)

If the AI decides it needs more information, it selects a specific tool (e.g., Google Search, a calculator, or a database).

- **Format**: It produces a structured command, such as `Action: Search["SpaceX launch date"]`.
- **Execution**: The system stops the LLM's generation and runs the actual code for that tool.

### 3. The Observation Step

The result of the tool execution is fed back into the agent's memory.

- **Feedback**: The AI "observes" the data returned by the tool (e.g., "The last launch was March 14").
- **Re-evaluation**: This observation is appended to the conversation history, and the flow loops back to the Reasoning Node.

### 4. The Exit Condition

The loop repeats until the LLM decides it has sufficient information.

- **Final Answer**: Instead of an `AgentAction`, it produces an `AgentFinish` (or "Final Answer") response, which is then delivered to the user.

## Transitioning to LangGraph

In traditional LangChain, this loop was a "black box" where you couldn't see or easily modify the steps. By using **LangGraph**, you explicitly define these steps as **Nodes** and the transitions as **Edges**:

| Component             | Role in ReAct Pattern                                                 |
| --------------------- | --------------------------------------------------------------------- |
| **State**             | The "memory" that stores all thoughts, actions, and observations.     |
| **Nodes**             | The functions where reasoning (LLM) or acting (Tools) happens.        |
| **Conditional Edges** | The "router" that decides whether to go to the Tools node or the End. |
