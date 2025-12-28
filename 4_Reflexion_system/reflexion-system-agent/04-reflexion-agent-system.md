# Reflexion Agent System

The flow of a Reflexion agent system is managed by a high-level "Actor" agent that coordinates a specific sequence of steps between three main sub-components: the Responder, the Execute Tools component, and the Reviser.

## Process Flow

The process follows this iterative cycle:

1. **Initial Request and Response**: The user provides a prompt (for example, a request for a 250-word blog post). The Responder agent generates an initial output in a JSON structure containing three properties:
    - **The Response**: The draft content based on the LLM's internal knowledge.
    - **Critique**: A self-reflection where the agent identifies gaps or redundancies in its own work.
    - **Search Keywords**: A list of suggested terms the agent needs to look up to provide more accurate or recent information.

2. **Tool Execution (Grounding)**: The suggested search keywords are passed to the Execute Tools component. This component uses an API, such as the Tavily Search tool, to scan the internet for live data related to those keywords. This step ensures the system is not limited by the model's training data cut-off date.

3. **Revision and Enrichment**: The Reviser agent receives both the original draft (with its critique) and the new live data fetched by the tools. It then produces a Revised Response that includes:
    - An updated version of the content.
    - A revised critique and a new list of search terms if more information is still needed.
    - **Citations**: Specific links or references that allow the user to verify where the information was sourced from.

4. **Iterative Looping**: The system does not necessarily stop after one revision. If the Reviser agent identifies new search keywords, the control flow loops back to the Execute Tools component. This cycle repeats several times, with each iteration enriching the content with more recent, verified facts without necessarily increasing the length of the final output.

5. **Final Output**: Once the looping process is complete, the final, grounded, and cited response is delivered to the user.

## Analogy

Think of the flow like a journalist writing a breaking news story. First, they write a quick draft based on what they already know (Responder). Then, they identify what facts are missing and send a researcher to check the latest wires (Tools). Finally, the journalist rewrites the story using the new evidence and adds footnotes to prove their sources (Reviser). They might repeat this several times as new information comes in before the story is finally published.
