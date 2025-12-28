# LangChain Tool Calling Explained (With and Without PydanticToolsParser)

This README explains how **LangChain tool calling works**, what `bind_tools` does, and **why `PydanticToolsParser` is needed**, using a clear side-by-side comparison.

---

## The Problem

Large Language Models (LLMs) normally return **plain text**.  
For real applications, you often need:

- Structured JSON
- Strong typing
- Schema validation
- Predictable outputs

---

## The Solution: Tool (Function) Calling

LangChain allows you to define tools using **Pydantic schemas** and force the LLM to respond using them.

This is done with:

- `bind_tools()` → forces structured tool-call output
- `PydanticToolsParser` → converts tool-call JSON into a validated Python object

---

## Example Schema

```python
class AnswerQuestion(BaseModel):
    answer: str
    search_queries: List[str]
    reflection: Dict[str, str]
```

---

## High-Level Data Flow

```
Prompt
  ↓
LLM (bind_tools)
  ↓
AIMessage (tool_calls JSON)
  ↓
PydanticToolsParser
  ↓
AnswerQuestion (Pydantic object)
```

---

## Case 1: Using bind_tools + PydanticToolsParser ✅ (Recommended)

```python
chain = (
    prompt
    | llm.bind_tools(tools=[AnswerQuestion], tool_choice="AnswerQuestion")
    | PydanticToolsParser(tools=[AnswerQuestion])
)

result = chain.invoke({"messages": [...]})
```

### Output You Receive

**A real Pydantic object**

```python
AnswerQuestion(
  answer="Python is a programming language...",
  search_queries=["Python history", "Python use cases"],
  reflection={
    "missing": "Performance details",
    "superfluous": "None"
  }
)
```

---

## Case 2: Using bind_tools Only ❌ (No Parser)

```python
chain = (
    prompt
    | llm.bind_tools(tools=[AnswerQuestion], tool_choice="AnswerQuestion")
)

msg = chain.invoke({"messages": [...]})
```

### Output You Receive

**An AIMessage**

**Structured data is embedded inside tool_calls**

```python
msg.tool_calls == [
  {
    "name": "AnswerQuestion",
    "args": {
      "answer": "Python is a programming language...",
      "search_queries": ["Python history", "Python use cases"],
      "reflection": {
        "missing": "Performance details",
        "superfluous": "None"
      }
    }
  }
]
```


```
When to Use Each Approach:

- Use bind_tools + PydanticToolsParser when:
- You need correctness
- You want strict schema guarantees
- You are building agent pipelines
- You want production reliability

# Use bind_tools only when:

- You want raw JSON
- You are experimenting or debugging
- You plan to handle validation manually

```