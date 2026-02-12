"""
RAG tool for the LangChain agent to search documents.
"""
import sys
from pathlib import Path

# Add src to path for imports
BASE_DIR = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(BASE_DIR / "src"))

from langchain.tools import tool

# Import vector store - will be initialized as singleton
_vector_store_instance = None


def _get_vector_store():
    """Get or create the vector store singleton instance."""
    global _vector_store_instance
    if _vector_store_instance is None:
        from rag.vector_store.faiss_store import FAISSVectorStore
        _vector_store_instance = FAISSVectorStore()
    return _vector_store_instance


@tool
def rag_search_tool(query: str) -> str:
    """
    Search internal documents for relevant information.
    
    Use this tool when you need to find information from documents that have been
    loaded into the system. This tool searches through all available documents
    and returns the most relevant content based on the query.
    
    Args:
        query: The search query describing what information you're looking for.
               Be specific and descriptive for better results.
    
    Returns:
        A string containing relevant document excerpts and their sources.
        Returns an empty string if no documents are found or the vector store
        is not initialized.
    
    Examples:
        - "What is the company's refund policy?"
        - "How do I configure the API authentication?"
        - "What are the system requirements?"
    """

    print("="*500)

    vector_store = _get_vector_store()
    
    if not vector_store.is_initialized():
        return "No documents have been loaded into the system yet. Please load documents first."
    
    # Search for relevant documents
    docs = vector_store.search(query)
    
    if not docs:
        return f"No relevant documents found for query: '{query}'"
    
    # Format the results
    results = []
    for i, doc in enumerate(docs, 1):
        source = doc.metadata.get("source", "Unknown source")
        content = doc.page_content
        
        results.append(
            f"[Document {i} - Source: {source}]\n{content}\n"
        )
    
    return "\n---\n".join(results)

