# Reflection Agent Pattern - Generation and Critique Loop

## What is the Reflection Pattern?

The **Reflection Pattern** (also called **Generation-Reflection Loop**) uses two LLMs working together to iteratively improve content through a cycle of generation and critique.

---

## The Two Chains

### 1. Generation Chain

```python
generation_chain = generation_prompt | llm
```

**Role:** The Creator/Writer

- Generates initial content (tweet, essay, code, etc.)
- Takes user requests
- Receives critique and creates improved versions
- Responds with revised content based on feedback

**System Prompt:**

```
"You are a twitter techie influencer assistant tasked with writing excellent twitter posts.
Generate the best twitter post possible for the user's request.
If the user provides critique, respond with a revised version of your previous attempts."
```

### 2. Reflection Chain

```python
reflection_chain = reflection_prompt | llm
```

**Role:** The Critic/Editor

- Analyzes generated content
- Provides detailed critique and recommendations
- Suggests improvements for length, virality, style, etc.
- Acts as quality control

**System Prompt:**

```
"You are a viral twitter influencer grading a tweet. Generate critique and recommendations
for the user's tweet. Always provide detailed recommendations, including requests for
length, virality, style, etc."
```

---

## How the Pattern Works

### The Iterative Loop

```
User Request
    ↓
┌─────────────────────────────────────────────┐
│  STEP 1: GENERATION                         │
│  Generator creates first draft              │
│  "AI is changing the tech industry"         │
└─────────────┬───────────────────────────────┘
              ↓
┌─────────────────────────────────────────────┐
│  STEP 2: REFLECTION                         │
│  Critic analyzes and provides feedback:     │
│  "Too vague. Add specific stats.            │
│   Use emojis. Make it more engaging.        │
│   Current length too short for engagement." │
└─────────────┬───────────────────────────────┘
              ↓
┌─────────────────────────────────────────────┐
│  STEP 3: GENERATION (Revision)              │
│  Generator improves based on critique:      │
│  "🚀 AI adoption surged 340% in 2024!       │
│   Here's what developers need to know       │
│   about the 3 biggest changes..."           │
└─────────────┬───────────────────────────────┘
              ↓
        [Good enough?]
        ├─ No  → Back to REFLECTION (Step 2)
        └─ Yes → Final Output ✅
```

### Message Flow Example

When you run the reflection loop, the message history grows:

**Iteration 1:**

```python
messages = [
    ("user", "Write a tweet about AI trends")
]
# → Generation Chain produces first draft
```

**After First Generation:**

```python
messages = [
    ("user", "Write a tweet about AI trends"),
    ("ai", "AI is transforming how we work and live...")
]
# → Reflection Chain critiques this
```

**After First Reflection:**

```python
messages = [
    ("user", "Write a tweet about AI trends"),
    ("ai", "AI is transforming how we work and live..."),
    ("ai", "CRITIQUE: Too generic. Add specific examples and data...")
]
# → Generation Chain revises based on critique
```

**After Second Generation:**

```python
messages = [
    ("user", "Write a tweet about AI trends"),
    ("ai", "AI is transforming how we work and live..."),
    ("ai", "CRITIQUE: Too generic. Add specific examples..."),
    ("ai", "🚀 3 AI trends reshaping 2025: 1) GPT-4 adoption...")
]
# → Can continue or stop here
```

---

## Why Use MessagesPlaceholder?

```python
ChatPromptTemplate.from_messages([
    ("system", "You are a twitter assistant..."),
    MessagesPlaceholder(variable_name="messages"),  # ← Key component
])
```

### The Problem It Solves

**Without MessagesPlaceholder:**

- Can only handle fixed messages
- No conversation history
- Can't build iterative improvement

**With MessagesPlaceholder:**

- Accepts **dynamic list** of messages
- Maintains **full conversation history**
- Enables **iterative refinement**
- Context from all previous turns

### How It Works

`MessagesPlaceholder` is a **slot** that gets filled at runtime:

```python
# The placeholder is like a variable that accepts a list
chain.invoke({
    "messages": [
        ("user", "Write about AI"),
        ("ai", "First draft"),
        ("ai", "Critique: improve X"),
        ("ai", "Revised draft")
    ]
})

# All these messages get inserted where MessagesPlaceholder is
```

**Result:** The LLM sees the entire conversation history and can reference previous generations and critiques.

---

## Complete Flow Diagram

```
┌─────────────────────────────────────────────────────────┐
│  USER INPUT                                              │
│  "Write a viral tweet about machine learning"           │
└─────────────────────┬───────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────┐
│  GENERATION CHAIN                                        │
│                                                          │
│  System: You are a twitter influencer assistant         │
│  Messages: [("user", "Write about ML")]                 │
│                                                          │
│  LLM Output (Draft 1):                                  │
│  "Machine learning is revolutionizing AI development    │
│   and enabling new possibilities"                       │
└─────────────────────┬───────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────┐
│  REFLECTION CHAIN                                        │
│                                                          │
│  System: You are a viral influencer grading tweets      │
│  Messages: [                                             │
│    ("user", "Write about ML"),                          │
│    ("ai", "Machine learning is revolutionizing...")     │
│  ]                                                       │
│                                                          │
│  LLM Output (Critique):                                 │
│  "CRITIQUE:                                              │
│   - Too generic, lacks specifics                        │
│   - No numbers or data points                           │
│   - Missing emojis for engagement                       │
│   - Too formal, needs casual tone                       │
│   - Add a hook to grab attention                        │
│   RECOMMENDATIONS:                                       │
│   - Start with surprising statistic                     │
│   - Use 2-3 relevant emojis                             │
│   - Include actionable insight                          │
│   - Keep under 280 characters"                          │
└─────────────────────┬───────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────┐
│  GENERATION CHAIN (Revision)                             │
│                                                          │
│  System: You are a twitter influencer assistant         │
│  Messages: [                                             │
│    ("user", "Write about ML"),                          │
│    ("ai", "Machine learning is revolutionizing..."),    │
│    ("ai", "CRITIQUE: Too generic, lacks specifics...")  │
│  ]                                                       │
│                                                          │
│  LLM Output (Draft 2):                                  │
│  "🤖 ML models trained 10x faster in 2024 vs 2023       │
│                                                          │
│   What changed? 3 breakthrough techniques every dev     │
│   should know about 🧵👇"                                │
└─────────────────────┬───────────────────────────────────┘
                      │
                      ▼
              [Quality Check]
                      │
        ┌─────────────┴─────────────┐
        │                           │
    Still needs                 Good enough
    improvement                     │
        │                           ▼
        │                    ┌─────────────┐
        │                    │   FINAL     │
        │                    │   OUTPUT    │
        │                    └─────────────┘
        │
        └──→ Loop back to REFLECTION CHAIN
```

---

## Key Benefits

### 1. Self-Improvement

- Content gets better with each iteration
- Automatic quality control
- Catches mistakes and weak points

### 2. Consistency

- Systematic feedback process
- Predictable quality standards
- Replicable results

### 3. Specialization

- Generator focuses on creation
- Reflector focuses on critique
- Each LLM optimized for its role

### 4. Context Awareness

- Full conversation history preserved
- Can reference previous attempts
- Learns from past critiques

---

## Comparison: With vs Without Reflection

### Without Reflection (Single Generation)

```
User: "Write a tweet about AI"
    ↓
LLM: "AI is cool and changing the world"
    ↓
Done ✅ (but mediocre quality)
```

**Problems:**

- No quality check
- First draft is final
- Inconsistent quality
- Misses opportunities for improvement

### With Reflection (Iterative Improvement)

```
User: "Write a tweet about AI"
    ↓
Generation: "AI is cool and changing the world"
    ↓
Reflection: "Too vague, add specifics, use data"
    ↓
Generation: "🚀 AI funding hit $200B in 2024, 3x higher than 2023"
    ↓
Reflection: "Much better! Add context for why it matters"
    ↓
Generation: "🚀 AI funding hit $200B in 2024 (3x vs 2023).
              This means more startups can compete with tech giants.
              The playing field is leveling 📊"
    ↓
Done ✅ (high quality, data-driven, engaging)
```

**Advantages:**

- Multiple quality passes
- Incorporates feedback
- Consistent high quality
- More engaging content

---

## Real-World Analogy

### Traditional Approach (No Reflection)

You write an essay and submit it immediately without proofreading.

### Reflection Pattern

1. **You (Generator):** Write first draft
2. **Teacher (Reflector):** Marks it up with suggestions
3. **You (Generator):** Revise based on feedback
4. **Teacher (Reflector):** Reviews again
5. **Repeat** until it's excellent

The pattern mimics how humans improve through iteration and feedback!

---

## Implementation Details

### The Code Structure

```python
# Define the two specialized chains
generation_chain = generation_prompt | llm  # Creator
reflection_chain = reflection_prompt | llm  # Critic

# To use them in a loop (conceptual):
messages = [("user", user_request)]

for iteration in range(max_iterations):
    # Generate
    draft = generation_chain.invoke({"messages": messages})
    messages.append(("ai", draft.content))

    # Reflect
    critique = reflection_chain.invoke({"messages": messages})
    messages.append(("ai", critique.content))

    # Check if good enough
    if quality_threshold_met(critique):
        break

final_output = messages[-2]  # Last generation before final critique
```

### Message History Growth

Each iteration adds 2 messages:

1. **Generation message** - New draft
2. **Reflection message** - Critique of that draft

This creates a rich context for continuous improvement.

---