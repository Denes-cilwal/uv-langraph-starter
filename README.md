# 🚀 UV LangGraph Starter

A comprehensive learning project exploring LangGraph and LangChain patterns for building AI agents. This repository contains practical examples and implementations of various agent architectures, from basic LLM interactions to advanced reflection patterns.

## 📚 Learning Path

This repository is structured as a progressive learning journey, starting from basic concepts and advancing to complex agent systems. Each folder builds upon concepts from the previous sections.

---

## 📁 Folder Structure & Contents

### **1️⃣ Introduction** (`1_introduction/`)
> **Foundation: Understanding LLM Basics and ReAct Pattern**

Learn the fundamentals of working with LLMs and the ReAct (Reasoning + Acting) agent pattern.

**Files:**
- `basic_llm.py` - Simple LLM interaction examples
- `react_agent_basic.py` - Basic ReAct agent implementation
- `react_agent_flow.md` - Detailed explanation of ReAct flow
- `draw-backs.md` - Limitations and challenges
- `README.md` - Complete ReAct pattern documentation
- Diagrams: ReAct pattern visualizations

**Key Concepts:**
- LLM setup and configuration
- Tool binding and execution
- ReAct cycle: Thought → Action → Observation
- Agent prompt engineering

---

### **2️⃣ Chains** (`2_chains/`)
> **Building Sequential Workflows with Message Graphs**

Explore chain patterns and message-based agent architectures, including reflection patterns.

**Files:**
- `basic.py` - Simple chain implementations
- `chains.py` - Advanced chain patterns
- `reflection-agent/` - Reflection agent implementation
  - Complete reflection agent pattern documentation
  - Message graph flow diagrams
  - Execution flow examples

**Key Concepts:**
- Sequential chains
- Message graphs
- Reflection pattern: Generate → Reflect → Revise
- Message history management
- Chain composition

---

### **3️⃣ Structured Outputs** (`3_structured_outputs/`)
> **Type-Safe LLM Responses with Pydantic**

Master structured output generation using Pydantic models for predictable LLM responses.

**Files:**
- `types.ipynb` - Jupyter notebook with interactive examples
- `pydantic.json` - Schema definitions
- Diagrams: Structured output visualizations

**Key Concepts:**
- Pydantic model integration with LLMs
- Schema-based output validation
- Type safety in AI responses
- JSON schema generation
- Field validation and parsing

---

### **4️⃣ Reflexion System** (`4_Reflexion_system/`)
> **Advanced Self-Improving Agent Architecture**

Implement sophisticated reflection systems where agents can analyze and improve their own outputs.

**Files:**
- `reflexion_graph.py` - Main reflexion graph implementation
- `schema.py` - State and message schemas
- `chains.py` - Reflexion chain components
- `execute_tools.py` - Tool execution logic
- `reflexion-system-agent/` - Complete documentation
  - Reflexion system architecture
  - Think → Search → Write loop
  - LLM response parsing system
- `tool-binding-n-pydantic/` - Tool binding patterns
  - Tool calling with/without Pydantic parser
- `tool-execution-component/` - Tool execution deep dive

**Key Concepts:**
- Reflexion architecture (Think → Act → Reflect → Revise)
- Tool binding with Pydantic
- Response parsing and validation
- Self-improving agent loops
- State management in complex workflows
- Error handling and retry logic

---

### **5️⃣ State Deep Dive** (`5_state_dive/`)
> **Mastering State Management in LangGraph**

Deep exploration of state management, reducers, and declarative state annotations.

**Files:**
- `1_basic_state.py` - Simple state graph with counter
- `2_complex_state.py` - Complex state with reducers
- `state_graph/` - State management documentation
  - `README.md` - Complete guide to Annotated State
  - Declarative state transformation patterns

**Key Concepts:**
- StateGraph fundamentals
- Basic vs Annotated state fields
- Reducer functions (`operator.add`, `operator.concat`)
- State accumulation patterns
- Conditional edges and loops
- Declarative state transformation
- State merging strategies

---

## 🎯 Learning Progression

```
1. Introduction (ReAct Pattern)
   ↓
2. Chains (Sequential Workflows)
   ↓
3. Structured Outputs (Type Safety)
   ↓
4. Reflexion System (Self-Improvement)
   ↓
5. State Management (Advanced Patterns)
```

---

## 🛠️ Setup

### Prerequisites
- Python 3.10+
- UV package manager

### Installation

```bash
# Clone the repository
git clone <repository-url>
cd uv-langraph-starter

# Create virtual environment with UV
uv venv

# Activate virtual environment
source .venv/bin/activate  # On macOS/Linux
# or
.venv\Scripts\activate     # On Windows

# Install dependencies
uv pip install -r pyproject.toml
```

### Environment Configuration

Copy `.env.example` to `.env` and add your API keys:

```bash
cp .env.example .env
```

Edit `.env` with your credentials:
```
OPENAI_API_KEY=your_openai_api_key_here
TAVILY_API_KEY=your_tavily_api_key_here  # For search functionality
```

---

