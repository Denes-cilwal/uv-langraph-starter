

from langchain_openai import ChatOpenAI

# Import the tool decorator from langchain_core.tools
# - tool: A decorator to convert Python functions into tools the AI can use
from langchain_core.tools import tool

# Import create_agent from langchain.agents (modern API)
# - create_agent: Creates an agent that can use tools (replaces old create_react_agent)
from langchain.agents import create_agent

# Import Python's built-in datetime module for time operations
import datetime

# Import Tavily web search tool (like giving the AI access to Google search)
from langchain_community.tools import TavilySearchResults



# ============================================
# STEP 1: Initialize the LLM (AI Brain)
# ============================================

# Create an instance of GPT-4 - this is the "brain" that will do the reasoning
# This LLM will analyze questions, decide which tools to use, and generate answers
llm = ChatOpenAI(model="gpt-4")


# ============================================
# STEP 2: Create Custom Tools
# ============================================

# @tool decorator: Tells LangChain "this function is a tool the AI can call"
# The AI will read the docstring to understand what this tool does
@tool
def get_system_time(format: str = "%Y-%m-%d %H:%M:%S"):
    """ Returns the current date and time in the specified format """
    # Get the current date and time from the system
    current_time = datetime.datetime.now()
    
    # Format it according to the specified format string
    # Example: "2025-12-29 14:30:00"
    formatted_time = current_time.strftime(format)
    
    # Return the formatted time string
    return formatted_time


# ============================================
# STEP 3: Initialize Pre-built Tools
# ============================================

# Create a Tavily search tool that can search the web
# search_depth="basic" means it does a quick search (not deep research)
# The AI can call this when it needs current information from the internet
search_tool = TavilySearchResults(search_depth="basic")


# ============================================
# STEP 4: Bundle All Tools Together
# ============================================

# Create a list of all available tools
# The AI will know: "I have 2 tools I can choose from"
# - get_system_time: for getting current date/time
# - search_tool: for searching the web
tools = [get_system_time, search_tool]


# ============================================
# STEP 5: Create the ReAct Agent Runnable
# ============================================

# *** WHAT IS A RUNNABLE? ***
# A Runnable in LangChain is a chain of operations that:
# 1. Takes an input
# 2. Runs through a series of steps in LINEAR ORDER
# 3. Passes the output of each step to the next step
# 4. Returns a final output
#
# Example pipeline: Input → Format Prompt → Call LLM → Parse Output → Return Result
#                   (Step 1)     (Step 2)      (Step 3)   (Step 4)     (Step 5)
#
# Think of it like an assembly line in a factory - each station does its job
# and passes the result to the next station.

# create_agent builds a Runnable that creates the "thinking logic" chain:
# Step 1: Format the prompt with tools info and user input
# Step 2: Send formatted prompt to the LLM
# Step 3: Parse LLM's response to detect if it wants to use a tool or give final answer
# Step 4: Return structured output (tool call OR final answer)
#
# It combines:
# - model: The brain (LLM) that makes decisions
# - tools: What actions the AI can take
#
# Note: create_agent uses the modern LangChain API and works with message-based format
# What this Runnable DOES:
# ✅ Formats prompts correctly with tool descriptions
# ✅ Calls the LLM and gets a response
# ✅ Parses the response to understand what the LLM wants to do
# ✅ Returns structured output indicating the next action
# ✅ Can be invoked directly with messages format
#
# Usage: agent.invoke({"messages": [("user", "your question")]})
react_agent_runnable = create_agent(model=llm, tools=tools)