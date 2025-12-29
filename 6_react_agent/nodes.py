from dotenv import load_dotenv
from agent_reason_runnable import react_agent_runnable, tools
from agent_state import AgentState
from langchain_core.agents import AgentFinish

load_dotenv()

def reason_node(state: AgentState):
    """
    The brain of the agent - decides what to do next.
    """
    # Create the input format expected by the agent
    agent_input = {
        "input": state["input"],
        "intermediate_steps": state["intermediate_steps"]
    }
    
    # Invoke the agent
    agent_outcome = react_agent_runnable.invoke(agent_input)
    
    # The agent returns either AgentAction or AgentFinish
    return {"agent_outcome": agent_outcome}



def act_node(state: AgentState):
    """
    The hands of the agent - executes the chosen tool.
    """
    # Get the action the agent wants to take
    agent_action = state["agent_outcome"]
    
    # Extract tool name and input
    tool_name = agent_action.tool
    tool_input = agent_action.tool_input
    
    print(f"\n🔧 Executing tool: {tool_name}")
    print(f"📝 Tool input: {tool_input}")
    
    # Find the matching tool
    tool_function = None
    for tool in tools:
        if tool.name == tool_name:
            tool_function = tool
            break
    
    # Execute the tool
    if tool_function:
        # Just pass tool_input directly - don't unpack
        output = tool_function.invoke(tool_input)
    else:
        output = f"Tool '{tool_name}' not found"
    
    print(f"✅ Tool output: {output}\n")
    
    # Return as a tuple that will be appended to intermediate_steps
    return {"intermediate_steps": [(agent_action, str(output))]}