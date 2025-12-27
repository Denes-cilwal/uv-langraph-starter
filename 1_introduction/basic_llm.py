import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI


# Load variables from .env
load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("OPENAI_API_KEY not found. Check your .env file.")

# Initialize LLM
llm = ChatOpenAI(api_key=api_key)  # or ChatOpenAI(openai_api_key=api_key) depending on version

# Standard Invoke call
try:
    result = llm.invoke("Give me a tweet about today's weather in Kathmandu")
    print(f"\n{result}")  # result is a message object; use .content for just the text
except Exception as e:
    print(f"Error occurred: {e}")



"""
Questions 
Case : I 
- Give me a fact about cats

Case : II
forcing a llm with prompt give me a tweet about today's weather in sydney
- You’re seeing “hallucination” because ChatOpenAI().invoke() is only a text model call.
- It has no built-in access to live weather (or “today” in the real world) unless 
- you explicitly give it the weather data or connect it to a tool/API that fetches it.



"""

