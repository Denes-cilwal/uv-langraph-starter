# creating basic generation and reflection chain
"""
The Reflection Agent (also called Generation-Reflection Loop) is a 
pattern where two LLMs work together to iteratively improve content:
"""

from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()


generation_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are a twitter techie influencer assistant tasked with writing excellent twitter posts."
            " Generate the best twitter post possible for the user's request."
            " If the user provides critique, respond with a revised version of your previous attempts.",
        ),
        MessagesPlaceholder(variable_name="messages"),
    ]
)

reflection_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are a viral twitter influencer grading a tweet. Generate critique and recommendations for the user's tweet."
            "Always provide detailed recommendations, including requests for length, virality, style, etc.",
        ),
        MessagesPlaceholder(variable_name="messages"),
    ]
)


llm = ChatOpenAI(model="gpt-4o")


generation_chain = generation_prompt | llm
reflection_chain = reflection_prompt | llm



"""
LLM = A smart person
generation_prompt = Instructions saying "You're a tweet writer" - create tweet
reflection_prompt = Instructions saying "You're a tweet critic" - critique tweet
Chains = The person + their specific role/instructions

"""