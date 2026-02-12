"""
RAG wrapper for always-on document retrieval.
Automatically retrieves context before every query and enhances the prompt.
"""
import sys
from pathlib import Path
from typing import Any, Dict, Optional

# Add src to path for imports
BASE_DIR = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(BASE_DIR / "src"))

from rag.context_retriever import get_rag_context, is_rag_available
from config.settings import settings


def _extract_user_query(messages: list) -> Optional[str]:
    """
    Extract the user query from messages.
    
    Args:
        messages: List of message tuples or message objects
    
    Returns:
        User query string or None
    """
    if not messages:
        return None
    
    # Handle tuple format: ("human", "query")
    if isinstance(messages[-1], tuple):
        role, content = messages[-1]
        if role == "human":
            return content
    
    # Handle message objects
    last_message = messages[-1]
    if hasattr(last_message, 'content'):
        return last_message.content
    elif isinstance(last_message, dict) and 'content' in last_message:
        return last_message['content']
    
    return None


def _enhance_messages_with_context(messages: list, context: str) -> list:
    """
    Enhance messages with RAG context by integrating it into the user message.
    
    Args:
        messages: Original messages
        context: Retrieved document context
    
    Returns:
        Enhanced messages with context integrated into user query
    """
    if not context:
        return messages
    
    # If messages are tuples, enhance the last human message with context
    if isinstance(messages, list) and messages:
        if isinstance(messages[0], tuple):
            enhanced = []
            for i, msg in enumerate(messages):
                if isinstance(msg, tuple) and msg[0] == "human":
                    # Check if this is the last human message
                    is_last_human = True
                    for j in range(i + 1, len(messages)):
                        if isinstance(messages[j], tuple) and messages[j][0] == "human":
                            is_last_human = False
                            break
                    
                    if is_last_human:
                        # Enhance the user message with context
                        original_query = msg[1]
                        enhanced_query = f"""Relevant context from knowledge base:

{context}

User Question: {original_query}

Please answer the user's question using the provided context above. The context contains relevant document excerpts that should be your primary source of information. If the context contains the answer, use it directly. If you need additional information beyond what's in the context, you can use tools or your general knowledge."""
                        enhanced.append(("human", enhanced_query))
                    else:
                        enhanced.append(msg)
                else:
                    enhanced.append(msg)
            return enhanced
    
    # For message objects, enhance the last human message
    enhanced = list(messages)
    if enhanced:
        last_msg = enhanced[-1]
        if hasattr(last_msg, 'content'):
            original_query = last_msg.content
            enhanced_query = f"""Relevant context from knowledge base:

{context}

User Question: {original_query}

Please answer the user's question using the provided context above. The context contains relevant document excerpts that should be your primary source of information."""
            # Create a copy with updated content
            from copy import copy
            enhanced_msg = copy(last_msg)
            enhanced_msg.content = enhanced_query
            enhanced[-1] = enhanced_msg
        elif isinstance(last_msg, dict) and 'content' in last_msg:
            original_query = last_msg['content']
            enhanced_query = f"""Relevant context from knowledge base:

{context}

User Question: {original_query}

Please answer the user's question using the provided context above. The context contains relevant document excerpts that should be your primary source of information."""
            enhanced[-1] = {**last_msg, 'content': enhanced_query}
    
    return enhanced


async def rag_enhanced_agent_invoke(
    agent: Any,
    inputs: Dict[str, Any],
    config: Optional[Dict[str, Any]] = None,
    auto_retrieve: Optional[bool] = None
) -> Dict[str, Any]:
    """
    Enhanced agent invoke that automatically retrieves RAG context.
    
    Args:
        agent: The LangChain agent instance
        inputs: Agent inputs (must contain "messages")
        config: Agent configuration
        auto_retrieve: Override auto-retrieve setting (defaults to RAG_AUTO_RETRIEVE)
    
    Returns:
        Agent response with context-enhanced prompt
    """
    # Check if auto-retrieve is enabled
    should_retrieve = auto_retrieve if auto_retrieve is not None else settings.RAG_AUTO_RETRIEVE
    
    if not should_retrieve:
        # If auto-retrieve is disabled, call agent normally
        return await agent.ainvoke(inputs, config)
    
    # Check if RAG is available
    if not is_rag_available():
        # RAG not available, proceed without context
        return await agent.ainvoke(inputs, config)
    
    # Extract user query
    messages = inputs.get("messages", [])
    user_query = _extract_user_query(messages)
    
    if not user_query:
        # No query found, proceed normally
        return await agent.ainvoke(inputs, config)
    
    # Retrieve context
    context = get_rag_context(user_query)
    
    print("+"*100)
    print(context)
    print("+"*100)

    # Enhance messages with context
    enhanced_messages = _enhance_messages_with_context(messages, context)
    
    # Create enhanced inputs
    enhanced_inputs = {**inputs, "messages": enhanced_messages}
    
    # Call agent with enhanced prompt
    return await agent.ainvoke(enhanced_inputs, config)


def rag_enhanced_agent_invoke_sync(
    agent: Any,
    inputs: Dict[str, Any],
    config: Optional[Dict[str, Any]] = None,
    auto_retrieve: Optional[bool] = None
) -> Dict[str, Any]:
    """
    Synchronous version of rag_enhanced_agent_invoke.
    
    Args:
        agent: The LangChain agent instance
        inputs: Agent inputs (must contain "messages")
        config: Agent configuration
        auto_retrieve: Override auto-retrieve setting (defaults to RAG_AUTO_RETRIEVE)
    
    Returns:
        Agent response with context-enhanced prompt
    """
    import asyncio
    
    # Check if auto-retrieve is enabled
    should_retrieve = auto_retrieve if auto_retrieve is not None else settings.RAG_AUTO_RETRIEVE
    
    if not should_retrieve:
        # If auto-retrieve is disabled, call agent normally
        return agent.invoke(inputs, config)
    
    # Check if RAG is available
    if not is_rag_available():
        # RAG not available, proceed without context
        return agent.invoke(inputs, config)
    
    # Extract user query
    messages = inputs.get("messages", [])
    user_query = _extract_user_query(messages)
    
    if not user_query:
        # No query found, proceed normally
        return agent.invoke(inputs, config)
    
    # Retrieve context
    context = get_rag_context(user_query)
    
    # Enhance messages with context
    enhanced_messages = _enhance_messages_with_context(messages, context)
    
    # Create enhanced inputs
    enhanced_inputs = {**inputs, "messages": enhanced_messages}
    
    # Call agent with enhanced prompt
    return agent.invoke(enhanced_inputs, config)
