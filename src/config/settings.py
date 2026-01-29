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

    class Config:
        env_file = BASE_DIR / ".env"
        extra = "allow"
settings = Settings()