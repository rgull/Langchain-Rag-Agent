"""
Script to initialize the vector store from documents.
Run this script to load documents and build the FAISS index.
"""
import sys
from pathlib import Path

# Add src to path for imports
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR / "src"))

import rag
from rag.loaders.document_loader import load_documents_from_directory
from rag.loaders.web_loader import load_documents_from_urls
from rag.vector_store.faiss_store import FAISSVectorStore
from config.settings import settings


def initialize_from_directory(documents_dir: str = None) -> None:
    """
    Initialize vector store from documents in a directory.
    
    Args:
        documents_dir: Path to directory containing documents.
                      Defaults to rag/documents/
    """
    if documents_dir is None:
        documents_dir = str(BASE_DIR / "rag" / "documents")
    
    print(f"Loading documents from: {documents_dir}")
    documents = load_documents_from_directory(documents_dir)
    
    if not documents:
        print("No documents found. Please add documents to the directory.")
        return
    
    print(f"Loaded {len(documents)} documents")
    
    # Initialize vector store
    vector_store = FAISSVectorStore()
    
    # Add documents
    print("Adding documents to vector store...")
    vector_store.add_documents(documents)
    
    # Save vector store
    print("Saving vector store...")
    vector_store.save()
    
    print(f"Vector store initialized with {vector_store.get_document_count()} document chunks")
    print(f"Vector store saved to: {vector_store.vector_store_path}")


def initialize_from_urls(urls: list) -> None:
    """
    Initialize vector store from URLs.
    
    Args:
        urls: List of URLs to load content from
    """
    print(f"Loading documents from {len(urls)} URLs...")
    documents = load_documents_from_urls(urls)
    
    if not documents:
        print("No documents loaded from URLs.")
        return
    
    print(f"Loaded {len(documents)} documents")
    
    # Initialize vector store
    vector_store = FAISSVectorStore()
    
    # Add documents
    print("Adding documents to vector store...")
    vector_store.add_documents(documents)
    
    # Save vector store
    print("Saving vector store...")
    vector_store.save()
    
    print(f"Vector store initialized with {vector_store.get_document_count()} document chunks")
    print(f"Vector store saved to: {vector_store.vector_store_path}")


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Initialize RAG vector store")
    parser.add_argument(
        "--dir",
        type=str,
        default=None,
        help="Directory containing documents (default: rag/documents/)"
    )
    parser.add_argument(
        "--urls",
        nargs="+",
        help="URLs to load documents from"
    )
    
    args = parser.parse_args()
    
    if args.urls:
        initialize_from_urls(args.urls)
    else:
        initialize_from_directory(args.dir)

