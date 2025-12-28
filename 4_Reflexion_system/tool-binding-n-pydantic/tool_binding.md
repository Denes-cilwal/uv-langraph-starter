# Returning Structured Data from an LLM using Function / Tool Calling

## The Problem

By default, Large Language Models (LLMs) return unstructured text.  
This becomes a problem when your application needs predictable, machine-readable output such as JSON or Python objects.

Example requirement:
- You want the LLM to return structured data (like a Python object), not just text.

---

## The Solution: Function / Tool Calling

OpenAI models support **function (tool) calling**, which allows you to:

- Define a function signature (name + parameters)
- Expose that function to the LLM
- Force the LLM to respond by calling the function
- Receive structured JSON output that matches a schema

This is commonly implemented using **Pydantic models** in Python.

---

## Core Mechanism: `bind_tools`

Example usage:

llm.bind_tools(tools=[AnswerQuestion], tool_choice="AnswerQuestion")

### What This Means

- `tools=[AnswerQuestion]`  
  Registers a tool named `AnswerQuestion`.  
  The parameters are inferred automatically from the Pydantic schema (e.g. `answer`, `search_queries`, `reflection`).

- `tool_choice="AnswerQuestion"`  
  Forces the LLM to always use this tool.  
  The model cannot return free-form text and must respond with structured arguments.

---

## Example Tool Schema (Conceptual)

AnswerQuestion includes:
- `answer`: string
- `search_queries`: list of strings
- `reflection`: object containing evaluation details

This schema defines exactly how the LLM must respond.

---

## Example Flow

### Without Tool Binding

Input:
What is Python?

Output:
Python is a programming language...

Problems:
- Unstructured
- Hard to parse
- Not schema-safe

---

### With Tool Binding

Input:
What is Python?  
(Available tool: AnswerQuestion)

Output:
- Tool called: AnswerQuestion
- Arguments returned as JSON:
  - answer: "Python is a programming language..."
  - search_queries: ["Python history", "Python use cases"]
  - reflection:
      - missing: "Performance details"
      - superfluous: "None"

Benefits:
- Fully structured
- Predictable
- Validated
- Easy to consume programmatically

---

## Why This Matters

Function / tool calling enables:

- Deterministic outputs
- Strong typing and validation
- Safer production usage
- Easier integration with APIs, databases, and agents
- Removal of fragile text parsing logic

---

## When to Use Tool Calling

Use tool calling when you need:
- Structured JSON responses
- Reliable automation
- Agent workflows
- Search + reasoning pipelines
- Production-grade LLM behavior

---

## Summary

Without tool calling:
- Free text
- Low reliability
- Manual parsing

With tool calling:
- Structured JSON
- High reliability
- Schema enforcement
- Production-ready

Tool calling transforms LLMs from chat generators into dependable system components.
