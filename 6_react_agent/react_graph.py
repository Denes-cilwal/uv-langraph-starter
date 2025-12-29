from dotenv import load_dotenv
load_dotenv()

from langchain_core.agents import AgentFinish
from langgraph.graph import END, StateGraph
from nodes import reason_node, act_node
from agent_state import AgentState

# Node names
REASON_NODE = "reason_node"
ACT_NODE = "act_node"

def should_continue(state: AgentState) -> str:
    """
    Routing function: decides where to go next.
    """
    if isinstance(state["agent_outcome"], AgentFinish):
        print("\n🎯 Agent has finished reasoning!")
        return END
    else:
        print(f"\n🤔 Agent decided to use a tool: {state['agent_outcome'].tool}")
        return ACT_NODE


# Build the graph
graph = StateGraph(AgentState)

# Add nodes
graph.add_node(REASON_NODE, reason_node)
graph.add_node(ACT_NODE, act_node)

# Set entry point
graph.set_entry_point(REASON_NODE)

# Add conditional edge from reason node
graph.add_conditional_edges(
    REASON_NODE,
    should_continue,
    {
        ACT_NODE: ACT_NODE,
        END: END
    }
)

# Add edge from act back to reason
graph.add_edge(ACT_NODE, REASON_NODE)

# Compile the graph
app = graph.compile()

# Run the agent
if __name__ == "__main__":
    print("🚀 Starting ReAct Agent")
    
    result = app.invoke({
        "input": "How many days ago was the latest SpaceX launch?",
        "agent_outcome": None,
        "intermediate_steps": []
    })
    
    print("🎉 FINAL RESULT")
    print(result["agent_outcome"].return_values["output"])
