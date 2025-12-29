import operator
from typing import Annotated, TypedDict, Union
from langchain_core.agents import AgentAction, AgentFinish

class AgentState(TypedDict):
    input: str
    #  initially it will None but it can be AgentAction or Finish
    agent_outcome: Union[AgentAction, AgentFinish, None]
    intermediate_steps: Annotated[list[tuple[AgentAction, str]], operator.add]




"""Think of it as
create_react_agent = The decision-maker (returns AgentAction/AgentFinish)
should_continue function = The inspector (looks at what was returned)
add_conditional_edges = The router (defines where to go based on the inspection)


1. Schema Structure:

It's a list of tuples: [(action1, result1), (action2, result2), ...]
Each tuple pairs what the agent tried with what it got back
This creates a complete history of the agent's journey

2. The operator.add Magic:

Without it: Each update would replace the entire list (losing history)
With it: Each update appends to the list (building memory)
It literally does: old_list + new_list

3. Three Critical Roles:

Memory: Prevents the agent from forgetting what it already tried
LLM Input: Gets formatted into the prompt so the LLM sees its history
Audit Trail: Documents the complete reasoning chain

"""

""" intermediate_steps
reason sees: []
reason decides: search for capital
act executes: gets "Paris"
act updates: intermediate_steps = [(search, "Paris")]

reason sees: [(search, "Paris")]
reason decides: search for population  
act executes: gets "2.1M"
act updates: intermediate_steps = [(search, "Paris"), (search population, "2.1M")]


"""