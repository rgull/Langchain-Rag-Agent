"""
Unified document loader for multiple file formats.
"""
from pathlib import Path
from typing import List

from langchain_community.document_loaders import (
    PyPDFLoader,
    TextLoader,
)
from langchain_core.documents import Document


def load_documents_from_directory(directory_path: str) -> List[Document]:
    """
    Load documents from a directory, supporting multiple file formats.
    
    Args:
        directory_path: Path to the directory containing documents
        
    Returns:
        List of Document objects loaded from the directory
        
    Supported formats:
        - PDF files (.pdf)
        - Text files (.txt)
        - Markdown files (.md, .markdown)
    """
    directory = Path(directory_path)
    if not directory.exists():
        raise ValueError(f"Directory does not exist: {directory_path}")
    
    if not directory.is_dir():
        raise ValueError(f"Path is not a directory: {directory_path}")
    
    documents = []
    supported_extensions = {".pdf", ".txt", ".md", ".markdown"}
    
    # Get all supported files
    files = [
        f for f in directory.rglob("*")
        if f.is_file() and f.suffix.lower() in supported_extensions
    ]
    
    for file_path in files:
        try:
            if file_path.suffix.lower() == ".pdf":
                loader = PyPDFLoader(str(file_path))
            else:  # .txt, .md, .markdown
                loader = TextLoader(str(file_path), encoding="utf-8")
            
            loaded_docs = loader.load()
            
            # Add metadata about source file
            for doc in loaded_docs:
                doc.metadata["source"] = str(file_path)
                doc.metadata["file_name"] = file_path.name
                doc.metadata["file_type"] = file_path.suffix.lower()
            
            documents.extend(loaded_docs)
        except Exception as e:
            print(f"Error loading {file_path}: {e}")
            continue
    
    return documents

