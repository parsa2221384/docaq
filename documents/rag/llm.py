import os
from pathlib import Path

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI


BASE_DIR = Path(__file__).resolve().parents[2]

load_dotenv(BASE_DIR / ".env")


OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"

LLM_MODEL_NAME = "openrouter/free"


api_key = os.getenv("OPENROUTER_API_KEY")

if not api_key:
    raise RuntimeError(
        "OPENROUTER_API_KEY is not configured."
    )


llm = ChatOpenAI(
    model=LLM_MODEL_NAME,
    api_key=api_key,
    base_url=OPENROUTER_BASE_URL,
    temperature=0,
)