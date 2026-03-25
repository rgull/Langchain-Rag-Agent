# from dotenv import load_dotenv
# import os

# load_dotenv()

# GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# if not GROQ_API_KEY:
#     raise RuntimeError("API_KEY is missing")

from pathlib import Path
from pydantic_settings import BaseSettings

BASE_DIR = Path(__file__).resolve().parent.parent.parent

class Settings(BaseSettings):
    GROQ_API_KEY: str
    MODEL_NAME: str
    
    # RAG Configuration
    RAG_EMBEDDING_MODEL: str = "sentence-transformers/all-MiniLM-L6-v2"
    RAG_CHUNK_SIZE: int = 1000
    RAG_CHUNK_OVERLAP: int = 200
    RAG_TOP_K: int = 4
    RAG_VECTOR_STORE_PATH: str = str(BASE_DIR / "rag" / "vector_store" / "faiss_index")
    
    # RAG Auto-Retrieve Configuration
    RAG_AUTO_RETRIEVE: bool = False  # Automatically retrieve context before every query
    RAG_AUTO_TOP_K: int = 4  # Number of documents to retrieve for auto-RAG

    # SMTP Configuration
    SMTP_HOST: str
    SMTP_PORT: int
    SMTP_USERNAME: str
    SMTP_PASSWORD: str
    SMTP_SENDER_EMAIL: str | None = None

    class Config:
        env_file = BASE_DIR / ".env"
        extra = "allow"
        
settings = Settings()