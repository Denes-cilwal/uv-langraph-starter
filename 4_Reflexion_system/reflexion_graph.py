from typing import List

from langchain_core.messages import BaseMessage, ToolMessage
from langgraph.graph import END, MessageGraph

from chains import revisor_chain, first_responder_chain
from execute_tools import execute_tools

graph = MessageGraph()

DRAFT = "draft"
EXECUTE_TOOLS = "execute_tools"
REVISOR = "revisor"


MAX_ITERATIONS = 3

# Create draft, execute and revisor node
# once node is ready, add it to the graph
# then connects to node together 

# now, add this nodes to graph
graph.add_node(DRAFT, first_responder_chain)
graph.add_node(EXECUTE_TOOLS, execute_tools)
graph.add_node(REVISOR, revisor_chain)



# add edges (no conditional edges)

graph.add_edge("draft", "execute_tools")
graph.add_edge("execute_tools", "revisor")


# after connection edge from execute tools to revisor we have two condtion either revise or end 
"""
# After the 'revisor' node runs, call 'event_loop' to decide what's next
workflow.add_conditional_edges(
    "revisor",      # The "source" node
    event_loop,     # The "routing" function
    {
        "execute_tools": "execute_tools", # If function returns "execute_tools", go to that node
        END: END                          # If function returns END, stop the graph
    }
)


The Core Check: isinstance(item, ToolMessage)
- The isinstance() function checks if a variable matches a specific "class" or type.
- In your LangGraph code, every time a tool runs, it adds a ToolMessage to the state.
- This part of the code asks: "Is this specific item in the list a ToolMessage?"

It returns True if it is, and False if it is not.

count_tool_visits = 0
for item in state:
    if isinstance(item, ToolMessage):
        count_tool_visits += 1

"""
def event_loop(state:List[BaseMessage]) -> str:
    count_tool_visits = sum(isinstance(item, ToolMessage) for item in state)
    num_iterations = count_tool_visits
    if num_iterations > MAX_ITERATIONS:
        return END
    return EXECUTE_TOOLS


# right after revisor fo to event loop check 
graph.add_conditional_edges(REVISOR, event_loop)
graph.set_entry_point(DRAFT)


app = graph.compile()

print(app.get_graph().draw_mermaid())

response = app.invoke(
    "Write about how small business can leverage AI to grow"
)

# get last message in the history which is going to be AI message 
print(response[-1].tool_calls[0]["args"]["answer"])
print(response, "response")