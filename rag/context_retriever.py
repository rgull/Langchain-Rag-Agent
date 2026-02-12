"""
RAG context retriever for automatic document retrieval.
Provides direct access to vector store for context retrieval.
"""
import sys
from pathlib import Path
from typing import Optional

# Add src to path for imports
BASE_DIR = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(BASE_DIR / "src"))

from rag.vector_store.faiss_store import FAISSVectorStore
from config.settings import settings

# Singleton vector store instance
_vector_store_instance = None


def _get_vector_store():
    """Get or create the vector store singleton instance."""
    global _vector_store_instance
    if _vector_store_instance is None:
        _vector_store_instance = FAISSVectorStore()
    return _vector_store_instance


def get_rag_context(query: str, top_k: Optional[int] = None) -> str:
    """
    Retrieve relevant document context for a query.
    
    Args:
        query: The search query
        top_k: Number of documents to retrieve (defaults to RAG_AUTO_TOP_K)
    
    Returns:
        Formatted context string with retrieved documents, or empty string if no documents found
    """
    vector_store = _get_vector_store()
    
    # Check if vector store is initialized
    if not vector_store.is_initialized():
        return ""
    
    # Use configured top_k or provided value
    k = top_k or settings.RAG_AUTO_TOP_K
    
    # Search for relevant documents
    docs = vector_store.search(query, k=k)
    
    if not docs:
        return ""
    
    # Format the results as context
    context_parts = []
    for i, doc in enumerate(docs, 1):
        source = doc.metadata.get("source", "Unknown source")
        content = doc.page_content
        context_parts.append(
            f"[Document {i} - Source: {source}]\n{content}"
        )
    
    return "\n\n---\n\n".join(context_parts)


def is_rag_available() -> bool:
    """
    Check if RAG is available (vector store is initialized).
    
    Returns:
        True if vector store is initialized, False otherwise
    """
    vector_store = _get_vector_store()
    return vector_store.is_initialized()
