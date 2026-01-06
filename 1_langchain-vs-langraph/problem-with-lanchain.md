# 🧩 Problem with LangChain in Non-Linear Workflows

This repository explains a common architectural challenge when using **LangChain** for real-world workflows—especially those involving **conditional branching, loops, and control-flow jumps**.

---

## 📌 Context

LangChain is designed to help developers build **LLM-powered applications** by composing steps into **chains**:

Prompt → LLM → Output Parser → Next Step →

This works extremely well for **linear workflows**.

However, many real-world systems (like hiring pipelines, approval flows, or multi-step automations) are **not linear**.

---

## 🚨 The Core Problem

The workflow shown in this project (e.g. hiring pipeline) is **non-linear** and includes:

1. **Conditional Branches**
2. **Loops**
3. **Multiple Jumps in Control Flow**

These constructs do **not map cleanly** to LangChain’s original “chain” abstraction.

---

## 🔀 1. Conditional Branching (if / else)

Example from the workflow:

- **JD Approved?**
  - ❌ No → Go back to _Create JD_
  - ✅ Yes → _Post Job_

LangChain does not natively manage:

- branching logic
- selecting which chain to execute next

So you must write external Python logic to decide the path.

---

## 🔁 2. Loops (Repeat Until Condition Met)

Examples:

- Keep regenerating the JD **until approved**
- Keep monitoring applications **until enough candidates apply**

This requires constructs like:

```python
while not approved:
    jd = jd_chain.invoke(...)
    approved = approve_jd(jd)
```

# 🧪 Glue Code Problem in LangChain for Non-Linear Workflows

This document explains a key limitation of **LangChain** when applied to **real-world, non-linear workflows**, and why excessive **glue code** becomes a problem.

---

## 🧪 The Result: “Glue Code”

Because LangChain cannot directly express **non-linear control-flow patterns**, developers are forced to write **custom Python orchestration logic**, commonly referred to as **glue code**.

### What Glue Code Handles

Glue code is responsible for:

- `if / else` decision logic
- `while` and `for` loops
- State tracking
- Retries, waits, and delays
- Transitions between workflow steps

### Example

```python
if approved:
    post_jd(jd)
else:
    regenerate_jd()
```

Rule of Thumb

👉 Less glue code = cleaner, more scalable systems
LangChain is optimized for linear workflows, but real-world systems are non-linear.
When workflows include branches and loops, developers must write orchestration (“glue code”) in Python—and the more glue code required, the less elegant and maintainable the solution becomes
