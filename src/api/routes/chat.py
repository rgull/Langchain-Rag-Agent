"""Single endpoint: POST /api/chat — send a message, get the agent's reply."""

from fastapi import APIRouter, Request

from rag.rag_wrapper import rag_enhanced_agent_invoke
from api.schemas import ChatRequest, ChatResponse

router = APIRouter()


@router.post("/chat", response_model=ChatResponse)
async def chat(request: Request, body: ChatRequest) -> ChatResponse:
    # Same flow as the CLI in main.py: one agent, RAG-enhanced invoke, thread_id for memory
    agent = request.app.state.agent
    thread_id = body.thread_id or "default"
    config = {"configurable": {"thread_id": thread_id}}
    inputs = {"messages": [("human", body.message)]}

    response = await rag_enhanced_agent_invoke(agent, inputs, config)

    # Agent returns {"messages": [...]}; we need the last message's text
    messages = response.get("messages", [])
    last = messages[-1] if messages else None
    reply_text = getattr(last, "content", None) if last else None
    if reply_text is None and isinstance(last, dict):
        reply_text = last.get("content", "")
    return ChatResponse(reply=reply_text or "")
