import os
from pathlib import Path
from typing import List, Dict, Any, Optional
import logging

from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_chroma import Chroma
from langchain.schema import Document
from .translation_service import translation_service

logger = logging.getLogger(__name__)


class VectorService:
    def __init__(self):
        """Initialize the vector service with ChromaDB and Google embeddings."""
        self.data_dir = Path(__file__).resolve().parent.parent.parent / 'data'
        self.persist_directory = Path(__file__).resolve().parent.parent / 'chroma_db'
        
        # Initialize embeddings
        api_key = os.getenv('GOOGLE_API_KEY')
        if api_key:
            self.embeddings = GoogleGenerativeAIEmbeddings(
                model="models/embedding-001",
                google_api_key=api_key
            )
        else:
            self.embeddings = None
            logger.warning("No GOOGLE_API_KEY found. Vector store functionality will be limited.")
        
        self.vectorstore = None
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=3000,
            chunk_overlap=500,
            length_function=len,
        )

    def load_documents(self) -> List[Document]:
        """Load all PDF documents from the data directory."""
        documents = []
        
        if not self.data_dir.exists():
            logger.error(f"Data directory {self.data_dir} does not exist")
            return documents
        
        pdf_files = list(self.data_dir.glob("*.pdf"))
        logger.info(f"Found {len(pdf_files)} PDF files to process")
        
        for pdf_file in pdf_files:
            try:
                logger.info(f"Loading PDF: {pdf_file.name}")
                loader = PyPDFLoader(str(pdf_file))
                docs = loader.load()
                
                # Add source metadata
                for doc in docs:
                    doc.metadata['source'] = pdf_file.name
                
                documents.extend(docs)
                logger.info(f"Loaded {len(docs)} pages from {pdf_file.name}")
                
            except Exception as e:
                logger.error(f"Error loading {pdf_file.name}: {str(e)}")
                continue
        
        logger.info(f"Total documents loaded: {len(documents)}")
        return documents

    def split_documents(self, documents: List[Document]) -> List[Document]:
        """Split documents into smaller chunks."""
        if not documents:
            logger.warning("No documents to split")
            return []
        
        try:
            chunks = self.text_splitter.split_documents(documents)
            logger.info(f"Split {len(documents)} documents into {len(chunks)} chunks")
            return chunks
        except Exception as e:
            logger.error(f"Error splitting documents: {str(e)}")
            return []

    def load_existing_vectorstore(self) -> bool:
        """Load existing vectorstore from disk."""
        if not self.embeddings:
            logger.error("No embeddings available. Cannot load vectorstore.")
            return False
        
        try:
            if self.persist_directory.exists():
                self.vectorstore = Chroma(
                    persist_directory=str(self.persist_directory),
                    embedding_function=self.embeddings
                )
                logger.info("Existing vectorstore loaded successfully")
                return True
            else:
                logger.warning("No existing vectorstore found. Run initialization to create one.")
                return False
                
        except Exception as e:
            logger.error(f"Error loading existing vectorstore: {str(e)}")
            return False

    def create_vectorstore(self, force_recreate: bool = False) -> bool:
        """Create or load the ChromaDB vectorstore."""
        if not self.embeddings:
            logger.error("No embeddings available. Cannot create vectorstore.")
            return False
        
        try:
            # Check if vectorstore already exists
            if self.persist_directory.exists() and not force_recreate:
                logger.info("Loading existing vectorstore")
                self.vectorstore = Chroma(
                    persist_directory=str(self.persist_directory),
                    embedding_function=self.embeddings
                )
                logger.info("Existing vectorstore loaded successfully")
                return True
            
            # Create new vectorstore
            logger.info("Creating new vectorstore...")
            
            # Load and process documents
            documents = self.load_documents()
            if not documents:
                logger.error("No documents found to create vectorstore")
                return False
            
            # Split documents into chunks
            chunks = self.split_documents(documents)
            if not chunks:
                logger.error("No chunks created from documents")
                return False
            
            # Create vectorstore
            logger.info(f"Creating vectorstore with {len(chunks)} document chunks...")
            self.vectorstore = Chroma.from_documents(
                documents=chunks,
                embedding=self.embeddings,
                persist_directory=str(self.persist_directory)
            )
            
            logger.info("Vectorstore created successfully")
            return True
            
        except Exception as e:
            logger.error(f"Error creating vectorstore: {str(e)}")
            return False

    def similarity_search(self, query: str, k: int = 3) -> List[Document]:
        """Perform similarity search on the vectorstore."""
        if not self.vectorstore:
            logger.warning("Vectorstore not initialized, attempting to load existing...")
            if not self.load_existing_vectorstore():
                logger.error("Failed to load vectorstore")
                return []

        # Translate query to English for RAG search
        translated_query = translation_service.translate_query_for_rag(query)
        if translated_query != query:
            logger.info(f"Using translated query for search: '{translated_query[:50]}...'")
        
        try:
            results = self.vectorstore.similarity_search(translated_query, k=k)
            logger.info(f"Found {len(results)} similar documents for query: {query[:50]}...")
            return results
        except Exception as e:
            logger.error(f"Error performing similarity search: {str(e)}")
            return []

    def similarity_search_with_score(self, query: str, k: int = 3) -> List[tuple]:
        """Perform similarity search with relevance scores."""
        if not self.vectorstore:
            logger.warning("Vectorstore not initialized, attempting to load existing...")
            if not self.load_existing_vectorstore():
                logger.error("Failed to load vectorstore")
                return []

        # Translate query to English for RAG search
        translated_query = translation_service.translate_query_for_rag(query)
        if translated_query != query:
            logger.info(f"Using translated query for search: '{translated_query[:50]}...'")
        
        try:
            results = self.vectorstore.similarity_search_with_score(translated_query, k=k)
            logger.info(f"Found {len(results)} similar documents with scores for query: '{query[:50]}...'")
            
            # Log the scores for debugging
            for i, (doc, score) in enumerate(results):
                logger.debug(f"Result {i+1}: Score={score:.4f}, Content preview: {doc.page_content[:100]}...")
            
            return results
        except Exception as e:
            logger.error(f"Error performing similarity search with scores: {str(e)}")
            return []

    def test_search(self, query: str, k: int = 5) -> List[tuple]:
        """Test search with detailed logging for debugging."""
        logger.info(f"Testing search with query: '{query}'")
        
        if not self.vectorstore:
            logger.warning("Vectorstore not initialized, attempting to load...")
            if not self.load_existing_vectorstore():
                logger.error("Failed to load vectorstore")
                return []

        # Translate query to English for RAG search
        translated_query = translation_service.translate_query_for_rag(query)
        if translated_query != query:
            logger.info(f"Using translated query for test search: '{translated_query[:50]}...'")
        
        try:
            # Get all results without score filtering
            results = self.vectorstore.similarity_search_with_score(translated_query, k=k)
            logger.info(f"Raw search returned {len(results)} results")
            
            for i, (doc, score) in enumerate(results):
                logger.info(f"Result {i+1}:")
                logger.info(f"  Score: {score:.6f}")
                logger.info(f"  Source: {doc.metadata.get('source', 'Unknown')}")
                logger.info(f"  Content (first 200 chars): {doc.page_content[:200]}...")
                logger.info("  ---")
            
            return results
        except Exception as e:
            logger.error(f"Error in test search: {str(e)}")
            return []

    def get_retriever(self, search_kwargs: Optional[Dict[str, Any]] = None):
        """Get a retriever object for use with chains."""
        if not self.vectorstore:
            logger.warning("Vectorstore not initialized, attempting to load existing...")
            if not self.load_existing_vectorstore():
                logger.error("Failed to load vectorstore")
                return None
        
        if search_kwargs is None:
            search_kwargs = {"k": 4}
        
        return self.vectorstore.as_retriever(search_kwargs=search_kwargs)

    def get_relevant_context(self, query: str, max_docs: int = 3) -> str:
        """Get relevant context as a formatted string for chat integration."""
        docs = self.similarity_search(query, k=max_docs)
        
        if not docs:
            return ""
        
        context_parts = []
        for i, doc in enumerate(docs, 1):
            source = doc.metadata.get('source', 'Unknown')
            content = doc.page_content.strip()
            context_parts.append(f"Source {i} ({source}):\n{content}")
        
        return "\n\n---\n\n".join(context_parts)

    def initialize(self, force_recreate: bool = False) -> bool:
        """Initialize the vector service."""
        logger.info("Initializing Vector Service...")
        return self.create_vectorstore(force_recreate=force_recreate)


# Global instance
vector_service = VectorService()
