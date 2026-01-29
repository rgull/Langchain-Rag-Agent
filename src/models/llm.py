from langchain_groq import ChatGroq
from config.settings import settings

def get_llm():
    return ChatGroq(
        model=settings.MODEL_NAME,
        api_key=settings.GROQ_API_KEY,
        temperature=0.0,
        max_tokens=1024,
    )