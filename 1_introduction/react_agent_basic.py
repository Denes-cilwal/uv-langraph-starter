import os
from dotenv import load_dotenv

from langchain_openai import ChatOpenAI
from langchain_tavily import TavilySearch
from langchain.agents import create_agent

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")

if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY not found. Check your .env file.")
if not TAVILY_API_KEY:
    raise ValueError("TAVILY_API_KEY not found. Add it to your .env file.")

llm = ChatOpenAI(
    api_key=OPENAI_API_KEY,
    model="gpt-4o-mini",
    temperature=0.7,
)

tavily_tool = TavilySearch(
    max_results=5,
    search_depth="basic",
)

# Create the ReAct agent using the latest create_agent function
# This is the modern approach from langchain.agents
# this create agent is providing tool to the llm
agent_executor = create_agent(
    model=llm,
    tools=[tavily_tool],
)

# Example usage:
response = agent_executor.invoke({"messages": [("user", "What is the weather in San Francisco?")]})
print("\n=== Agent Response ===")
for message in response["messages"]:
    print(f"{message.type}: {message.content}")
    print()

"""
ReAct pattern is all about - Reasoning, Action, and Observation

Thought (Reasoning)
    |
    Action - The agent decides which tool to use and what input to provide
    |
    Observation - The agent observes the result from the tool
    |
    Repeat until the task is complete


┌─────────────────────────────────────────────┐
│  LangChain/LangGraph Environment            │
│                                             │
│  1. User Question                           │
│     "What is the weather in SF?"            │
│          ↓                                  │
│  2. LLM (GPT-4o-mini) Reasoning             │
│     "I need current weather data"           │
│          ↓                                  │
│  3. LLM decides: Use TavilySearch           │
│     Generates tool call with parameters     │
│          ↓                                  │
├─────────────────────────────────────────────┤
│  Tool Execution (External API Call)         │
│  → Tavily API fetches weather data          │
│  → Returns JSON with temp, humidity, etc.   │
├─────────────────────────────────────────────┤
│  4. ⬅ COMES BACK to LangChain              │
│     Observation added to message history    │
│          ↓                                  │
│  5. LLM sees the observation                │
│     Reads the weather data                  │
│          ↓                                  │
│  6. LLM Reasoning Again                     │
│     "I have enough info now"                │
│          ↓                                  │
│  7. LLM generates final answer              │
│     (No more tool calls needed)             │
│          ↓                                  │
│  8. Returns complete response               │
└─────────────────────────────────────────────┘    
"""