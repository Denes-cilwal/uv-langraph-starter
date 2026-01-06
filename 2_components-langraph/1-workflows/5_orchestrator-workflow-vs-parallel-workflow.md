# Orchestrator Workflow vs Parallel Workflow

A comprehensive guide to understanding the key differences between Orchestrator and Parallel workflow patterns in LangGraph.

---

## 🎯 Overview

This document breaks down the key differences between Orchestrator workflows and Parallel workflows, helping you choose the right pattern for your use case.

---

## 🔀 Orchestrator Workflow

### Architecture Diagram

```
In → Orchestrator → LLM Call 1 ↘
                  → LLM Call 2 → Synthesizer → Out
                  → LLM Call 3 ↗
```

### Key Characteristics

Sequential Decision Making: The Orchestrator runs FIRST, then decides which LLM calls to make
Dynamic Routing: The Orchestrator can choose which workers to call based on the input (might call only 1, or all 3, or any combination)
Conditional Execution: Workers only execute if the Orchestrator decides they're needed
Workers are Parallel: Once orchestrator decides, LLM Call 1, 2, 3 run in parallel (dotted lines show this)
Smart Coordination: The Orchestrator analyzes the task and delegates intelligently

Example flow:
User: "Book a flight and hotel"

Orchestrator analyzes → Decides to call:

- LLM Call 1 (Flight Booking Agent) ✓
- LLM Call 2 (Hotel Booking Agent) ✓
- LLM Call 3 (Car Rental Agent) ✗ (not needed)

Only 2 workers execute, then Synthesizer combines results

Parallel Workflow
→ Worker 1 ↘
In → Splitter → Worker 2 → Aggregator → Out
→ Worker 3 ↗
Key characteristics:

Always Executes All Branches: Every worker ALWAYS runs, no decision making
No Intelligence in Routing: A simple splitter just distributes work
Static Structure: Same branches execute every time
Independent Processing: Each worker processes the same input independently
Simple Aggregation: Results are combined mechanically (no smart synthesis)

Example flow:
User: "Analyze this document"

Splitter sends document to ALL workers (always):

- Worker 1 (Sentiment Analysis) ✓
- Worker 2 (Entity Extraction) ✓
- Worker 3 (Summary Generation) ✓

All 3 always run, Aggregator just merges results

Visual Difference

```
Orchestrator (your diagram):

Orchestrator = 🧠 Brain that decides
├─ Might call only LLM 1
├─ Might call LLM 1 + 2
└─ Might call all 3 (context-dependent)

Pure Parallel:

Splitter = 📤 Just broadcasts
├─ Always calls Worker 1
├─ Always calls Worker 2
└─ Always calls Worker 3 (no decision)
```

The Loop in Your Diagram
Notice the loop arrow (🔄) in your diagram? That's another orchestrator feature - it can iterate and refine:
Out → Evaluator Optimizer → back to Orchestrator

This allows:

- Quality checking results
- Re-running with different workers if needed
- Iterative improvement
  A simple parallel workflow typically doesn't have this feedback loop.

When to Use Each?
Use Orchestrator when:

Tasks require different handling based on input
You want to save compute (only run what's needed)
Need intelligent routing and decision making
Example: Customer support, complex query handling

Use Parallel when:

Same input needs multiple independent analyses
All processing steps are always needed
Maximum speed is priority (truly parallel)
Example: Document analysis with multiple extractors
