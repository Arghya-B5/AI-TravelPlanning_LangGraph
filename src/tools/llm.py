import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq

load_dotenv(override=True)

GROQ_API_KEY = os.getenv("GROQ_API_KEY")


def get_llm():

    if not GROQ_API_KEY:
        raise ValueError("GROQ_API_KEY is missing from .env")

    return ChatGroq(
        model="openai/gpt-oss-120b",
        groq_api_key=GROQ_API_KEY,
        temperature=0.3,
        max_tokens=1500,
        model_kwargs={
            "tool_choice": "none"
        }
    )
