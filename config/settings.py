import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

if not GOOGLE_API_KEY:
    raise EnvironmentError(
        "GOOGLE_API_KEY not found. Please create a .env file with your Gemini API key."
    )

MODEL_NAME = "gemini-2.5-flash"


def get_llm(temperature: float = 0.7) -> ChatGoogleGenerativeAI:
    """Return a configured Gemini LLM instance."""
    return ChatGoogleGenerativeAI(
        model=MODEL_NAME,
        google_api_key=GOOGLE_API_KEY,
        temperature=temperature,
    )
