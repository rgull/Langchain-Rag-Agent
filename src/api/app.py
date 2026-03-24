"""
FastAPI app: one agent at startup, one route POST /api/chat.
Run from project root: uvicorn src.api.app:app --reload --port 8000
"""

import sys
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# So "agents", "rag", "memory" etc. resolve when running from project root
_base = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(_base))
sys.path.insert(0, str(_base / "src"))

from agents.agent import build_agent
from memory.sqlite_saver import close_sqlite_connection
from api.routes.chat import router as chat_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Create agent once when the server starts; close DB when it stops."""
    app.state.agent = await build_agent()
    yield
    await close_sqlite_connection()


app = FastAPI(lifespan=lifespan)

# Let Angular (localhost:4200) call this API from the browser
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200","https://ordervez.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(chat_router, prefix="/api")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("src.api.app:app", host="0.0.0.0", port=8001, reload=True)