import os
from pathlib import Path
from typing import List, Dict, Any, Optional
import logging

from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_chroma import Chroma
from langchain.schema import Document

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
            chunk_size=1000,
            chunk_overlap=200,
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
                logger.info(f"Loading {pdf_file.name}")
                loader = PyPDFLoader(str(pdf_file))
                docs = loader.load()
                
                # Add metadata to documents
                for doc in docs:
                    doc.metadata.update({
                        'source': pdf_file.name,
                        'file_path': str(pdf_file)
                    })
                
                documents.extend(docs)
                logger.info(f"Loaded {len(docs)} pages from {pdf_file.name}")
                
            except Exception as e:
                logger.error(f"Error loading {pdf_file.name}: {str(e)}")
                continue
        
        logger.info(f"Total documents loaded: {len(documents)}")
        return documents

    def split_documents(self, documents: List[Document]) -> List[Document]:
        """Split documents into smaller chunks for better retrieval."""
        return self.text_splitter.split_documents(documents)

    def load_existing_vectorstore(self) -> bool:
        """Load existing vectorstore without re-embedding documents."""
        if not self.embeddings:
            logger.error("No embeddings available. Cannot load vectorstore.")
            return False
        
        try:
            if self.persist_directory.exists():
                logger.info("Loading existing vectorstore from disk...")
                self.vectorstore = Chroma(
                    persist_directory=str(self.persist_directory),
                    embedding_function=self.embeddings
                )
                
                # Check if vectorstore has documents
                collection = self.vectorstore._collection
                doc_count = collection.count()
                if doc_count > 0:
                    logger.info(f"Vectorstore loaded successfully with {doc_count} documents")
                    return True
                else:
                    logger.warning("Existing vectorstore is empty")
                    return False
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
                
                # Check if vectorstore has documents
                collection = self.vectorstore._collection
                if collection.count() > 0:
                    logger.info(f"Vectorstore loaded with {collection.count()} documents")
                    return True
                else:
                    logger.info("Existing vectorstore is empty, recreating...")
                    force_recreate = True
            
            if force_recreate or not self.persist_directory.exists():
                logger.info("Creating new vectorstore from documents")
                
                # Load and process documents
                documents = self.load_documents()
                if not documents:
                    logger.error("No documents found to process")
                    return False
                
                # Split documents into chunks
                text_chunks = self.split_documents(documents)
                logger.info(f"Created {len(text_chunks)} text chunks")
                
                # Create vectorstore
                self.vectorstore = Chroma.from_documents(
                    documents=text_chunks,
                    embedding=self.embeddings,
                    persist_directory=str(self.persist_directory)
                )
                
                logger.info("Vectorstore created successfully")
                return True
                
        except Exception as e:
            logger.error(f"Error creating vectorstore: {str(e)}")
            return False
        
        return False

    def similarity_search(self, query: str, k: int = 4) -> List[Document]:
        """Perform similarity search on the vectorstore."""
        if not self.vectorstore:
            logger.warning("Vectorstore not initialized, attempting to load existing...")
            if not self.load_existing_vectorstore():
                logger.error("Failed to load vectorstore")
                return []
        
        try:
            results = self.vectorstore.similarity_search(query, k=k)
            logger.info(f"Found {len(results)} similar documents for query: {query[:50]}...")
            return results
        except Exception as e:
            logger.error(f"Error performing similarity search: {str(e)}")
            return []

    def similarity_search_with_score(self, query: str, k: int = 4) -> List[tuple]:
        """Perform similarity search with relevance scores."""
        if not self.vectorstore:
            logger.warning("Vectorstore not initialized, attempting to load existing...")
            if not self.load_existing_vectorstore():
                logger.error("Failed to load vectorstore")
                return []
        
        try:
            results = self.vectorstore.similarity_search_with_score(query, k=k)
            logger.info(f"Found {len(results)} similar documents with scores for query: '{query[:50]}...'")
            
            # Log the scores for debugging
            for i, (doc, score) in enumerate(results):
                logger.debug(f"Result {i+1}: Score={score:.4f}, Content preview: {doc.page_content[:100]}...")
            
            return results
        except Exception as e:
            logger.error(f"Error performing similarity search with scores: {str(e)}")
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
