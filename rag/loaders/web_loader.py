"""
Web/URL content loader for retrieving documents from URLs.
"""
from typing import List

from langchain_community.document_loaders import WebBaseLoader
from langchain_core.documents import Document


def load_documents_from_urls(urls: List[str]) -> List[Document]:
    """
    Load documents from a list of URLs.
    
    Args:
        urls: List of URLs to load content from
        
    Returns:
        List of Document objects loaded from the URLs
    """
    documents = []
    
    for url in urls:
        try:
            loader = WebBaseLoader(url)
            loaded_docs = loader.load()
            
            # Add metadata about source URL
            for doc in loaded_docs:
                doc.metadata["source"] = url
                doc.metadata["source_type"] = "web"
            
            documents.extend(loaded_docs)
        except Exception as e:
            print(f"Error loading URL {url}: {e}")
            continue
    
    return documents

