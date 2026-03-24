"""Single endpoint: POST /api/chat — send a message, get the agent's reply."""

from typing import Any

from fastapi import APIRouter, Request

from rag.rag_wrapper import rag_enhanced_agent_invoke
from api.schemas import ChatRequest, ChatResponse

router = APIRouter()


def _content_to_text(content: Any) -> str:
    """Convert provider-specific content payloads into a plain string."""
    if content is None:
        return ""
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        parts: list[str] = []
        for item in content:
            if isinstance(item, str):
                parts.append(item)
            elif isinstance(item, dict):
                # Common formats include {"text": "..."} or {"type": "text", "text": "..."}.
                text = item.get("text") or item.get("content")
                if text is not None:
                    parts.append(str(text))
            else:
                parts.append(str(item))
        return "\n".join(p for p in parts if p).strip()
    return str(content)


def _extract_reply_text(response: dict[str, Any]) -> str:
    """Safely extract the final assistant message text from agent output."""
    messages = response.get("messages", [])
    if not isinstance(messages, list) or not messages:
        return ""

    last = messages[-1]
    if isinstance(last, dict):
        return _content_to_text(last.get("content"))

    return _content_to_text(getattr(last, "content", None))


@router.post("/chat", response_model=ChatResponse)
async def chat(request: Request, body: ChatRequest) -> ChatResponse:
    # Same flow as the CLI in main.py: one agent, RAG-enhanced invoke, thread_id for memory
    agent = request.app.state.agent
    thread_id = body.thread_id or "default"
    config = {"configurable": {"thread_id": thread_id}}
    inputs = {"messages": [("human", body.message)]}

    response = await rag_enhanced_agent_invoke(agent, inputs, config)
    reply_text = _extract_reply_text(response)
    if not reply_text:
        reply_text = "I could not generate a response right now. Please try again."
    return ChatResponse(reply=reply_text)
