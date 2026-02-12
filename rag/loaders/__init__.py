"""
Document loaders for various file types and sources.
"""

from .document_loader import load_documents_from_directory
from .web_loader import load_documents_from_urls

__all__ = ["load_documents_from_directory", "load_documents_from_urls"]

