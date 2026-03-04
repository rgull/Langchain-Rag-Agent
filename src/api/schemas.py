"""Request/response shapes for the chat API. FastAPI uses these to validate JSON in and out."""

from pydantic import BaseModel


class ChatRequest(BaseModel):
    message: str
    thread_id: str | None = None  # optional; if missing, all users share one "default" conversation


class ChatResponse(BaseModel):
    reply: str
