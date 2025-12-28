from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
import datetime
from langchain_openai import ChatOpenAI
from schema import AnswerQuestion
from langchain_core.output_parsers.openai_tools import PydanticToolsParser
from langchain_core.messages import HumanMessage
from dotenv import load_dotenv

load_dotenv()



pydantic_parser = PydanticToolsParser(tools=[AnswerQuestion])

# Actor Agent Prompt - generates initial answer with self-critique
# This agent answers questions, then critiques its own answer to identify improvements
actor_prompt_template = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """You are expert AI researcher.
Current time: {time}

1. {first_instruction}
2. Reflect and critique your answer. Be severe to maximize improvement.
3. After the reflection, **list 1-3 search queries separately** for researching improvements. Do not include them inside the reflection.
""",
        ),
        # Placeholder for conversation history (user questions, previous messages)
        MessagesPlaceholder(variable_name="messages"),
        
        # Reminder to use structured output format (AnswerQuestion schema)
        ("system", "Answer the user's question above using the required format."),
    ]
).partial(
    # .partial() pre-fills template variables before runtime
    # Inject current timestamp dynamically when the prompt is used
    # Lambda ensures fresh timestamp on each invocation, not when template is created
    time=lambda: datetime.datetime.now().isoformat(),
)

# Create specialized prompt for first response by filling in the instruction
# .partial() again to bind first_instruction, leaving only 'messages' to be filled later
# This creates a reusable template specifically for initial answers
first_responder_prompt_template = actor_prompt_template.partial(
    first_instruction="Provide a detailed ~250 word answer"
)

# Initialize the LLM that will power the agent
# Can be chained with prompt: first_responder_prompt_template | llm.with_structured_output(AnswerQuestion)
llm = ChatOpenAI(model="gpt-4o")


# first_responsder_chain
first_responder_chain = first_responder_prompt_template | llm.bind_tools(tools=[AnswerQuestion], tool_choice='AnswerQuestion') |  pydantic_parser  # ← Parses AIMessage → AnswerQuestion object

# now invoke the chain
response = first_responder_chain.invoke({
    "messages": [HumanMessage("AI Agents taking over content creation")]
})

print(response)