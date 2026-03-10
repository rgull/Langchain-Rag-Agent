"""
FAISS vector store manager for document storage and retrieval.
"""
import os
import sys
from pathlib import Path
from typing import List, Optional

# Add src to path for imports
BASE_DIR = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(BASE_DIR / "src"))

from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

from config.settings import settings


class FAISSVectorStore:
    """
    Manages a FAISS vector store for document retrieval.
    """
    
    def __init__(
        self,
        embedding_model: Optional[str] = None,
        chunk_size: Optional[int] = None,
        chunk_overlap: Optional[int] = None,
        vector_store_path: Optional[str] = None,
    ):
        """
        Initialize the FAISS vector store.
        
        Args:
            embedding_model: Name of the embedding model to use
            chunk_size: Size of text chunks for splitting
            chunk_overlap: Overlap between chunks
            vector_store_path: Path to save/load the vector store
        """
        self.embedding_model = embedding_model or settings.RAG_EMBEDDING_MODEL
        self.chunk_size = chunk_size or settings.RAG_CHUNK_SIZE
        self.chunk_overlap = chunk_overlap or settings.RAG_CHUNK_OVERLAP
        self.vector_store_path = vector_store_path or settings.RAG_VECTOR_STORE_PATH
        
        # Initialize embeddings
        self.embeddings = HuggingFaceEmbeddings(
            model_name=self.embedding_model
        )
        
        # Initialize text splitter
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.chunk_size,
            chunk_overlap=self.chunk_overlap,
            length_function=len,
        )
        
        # Vector store instance (will be initialized when needed)
        self.vector_store: Optional[FAISS] = None
        
        # Try to load existing vector store
        self._load_if_exists()
    
    def _load_if_exists(self) -> None:
        """Load vector store from disk if it exists."""
        if os.path.exists(self.vector_store_path) and os.path.isdir(self.vector_store_path):
            try:
                self.vector_store = FAISS.load_local(
                    self.vector_store_path,
                    self.embeddings,
                    allow_dangerous_deserialization=True
                )
            except Exception as e:
                print(f"Warning: Could not load existing vector store: {e}")
                self.vector_store = None
    
    def load_documents(self, documents: List[Document]) -> List[Document]:
        """
        Load and split documents into chunks.
        
        Args:
            documents: List of Document objects to process
            
        Returns:
            List of split Document chunks
        """
        if not documents:
            return []
        
        # Split documents into chunks
        split_docs = self.text_splitter.split_documents(documents)
        return split_docs
    
    def add_documents(self, documents: List[Document]) -> None:
        """
        Add documents to the vector store.
        
        Args:
            documents: List of Document objects to add
        """
        if not documents:
            return
        
        # Split documents into chunks
        split_docs = self.load_documents(documents)
        
        if not split_docs:
            return
        
        # If vector store doesn't exist, create it
        if self.vector_store is None:
            self.vector_store = FAISS.from_documents(
                split_docs,
                self.embeddings
            )
        else:
            # Add to existing vector store
            self.vector_store.add_documents(split_docs)
    
    def search(
        self,
        query: str,
        k: Optional[int] = None
    ) -> List[Document]:
        """
        Search for relevant documents.
        
        Args:
            query: Search query string
            k: Number of documents to retrieve (defaults to RAG_TOP_K)
            
        Returns:
            List of relevant Document objects
        """
        if self.vector_store is None:
            return []
        
        k = k or settings.RAG_TOP_K
        
        try:
            # Perform similarity search
            docs = self.vector_store.similarity_search(query, k=k)
            return docs
        except Exception as e:
            print(f"Error during search: {e}")
            return []
    
    def save(self) -> None:
        """Save the vector store to disk."""
        if self.vector_store is None:
            print("Warning: No vector store to save.")
            return
        
        # Create directory if it doesn't exist
        vector_store_dir = Path(self.vector_store_path).parent
        vector_store_dir.mkdir(parents=True, exist_ok=True)
        
        try:
            self.vector_store.save_local(
                self.vector_store_path
            )
        except Exception as e:
            print(f"Error saving vector store: {e}")
            raise
    
    def load(self) -> bool:
        """
        Load the vector store from disk.
        
        Returns:
            True if loaded successfully, False otherwise
        """
        if not os.path.exists(self.vector_store_path):
            return False
        
        try:
            self.vector_store = FAISS.load_local(
                self.vector_store_path,
                self.embeddings,
                allow_dangerous_deserialization=True
            )
            return True
        except Exception as e:
            print(f"Error loading vector store: {e}")
            return False
    
    def is_initialized(self) -> bool:
        """Check if the vector store is initialized."""
        return self.vector_store is not None
    
    def get_document_count(self) -> int:
        """Get the number of documents in the vector store."""
        if self.vector_store is None:
            return 0
        return self.vector_store.index.ntotal if hasattr(self.vector_store.index, 'ntotal') else 0

    def clear(self, delete_from_disk: bool = True) -> None:
        """
        Clear the in-memory vector store. Optionally delete the saved index from disk.
        After calling this, add_documents() will create a fresh index.

        Args:
            delete_from_disk: If True, remove the index files from disk so the next
                load also starts empty. Default True.
        """
        self.vector_store = None
        if delete_from_disk:
            import shutil
            path = Path(self.vector_store_path)
            if path.exists():
                if path.is_dir():
                    shutil.rmtree(path)
                else:
                    path.unlink(missing_ok=True)

