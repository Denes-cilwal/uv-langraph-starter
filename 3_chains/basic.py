from typing import List, Sequence
from dotenv import load_dotenv
from langchain_core.messages import BaseMessage, HumanMessage
from langgraph.graph import END, MessageGraph
from chains import generation_chain, reflection_chain


load_dotenv()

graph = MessageGraph() # invoke a message graph class

# Create generate and reflect node
# once node is ready, add it to the graph
# then connects to node together

REFLECT = "reflect"
GENERATE = "generate"

# since we know every node recieves the entire state
# then we are invoking on the state using the chain we have created and 
# then we are appending that response to the history
# this generate and reflect is automatically by ai itself
# state is just a list of messages
def generate_node(state):
    # whatever the state has been generated that need to be sit in message placeholder
    # whatever going to be returned object of llm,it is just going to extract the content and it is going to append that message to existing state
    return generation_chain.invoke({
        "messages": state
        }
    )

def reflect_node(state):
    return reflection_chain.invoke({
        "messages": state
        }
    )



# now, add this nodes to graph
graph.add_node(GENERATE, generate_node) 
graph.add_node(REFLECT, reflect_node)


# set entry point
graph.set_entry_point(GENERATE)


# now need to create should continue function node

def should_continue(state):
    if (len(state) > 6):
        return END 
    # if not Goto Reflect    
    return REFLECT

# add conditional edges
# right after generation is done should_continue will go to branch of two different things reflect or end 
graph.add_conditional_edges(GENERATE, should_continue)

# if it goes to reflect then it should again go to generate with critics, merits
# connect from refect to generate
graph.add_edge(REFLECT, GENERATE)


app = graph.compile()

print(app.get_graph().draw_mermaid())
app.get_graph().print_ascii()


# whatever we add here it will added to message place | history list ()
response = app.invoke(HumanMessage(content="AI Agents taking over content creation"))

print(response)

"""
system message is going to different for each of the chains and both of those chains are going to share increasing getting message history
"""