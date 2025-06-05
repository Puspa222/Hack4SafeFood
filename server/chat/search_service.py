import os
import logging
from typing import List, Dict, Any
from langchain_community.tools import DuckDuckGoSearchRun
from .translation_service import TranslationService

logger = logging.getLogger(__name__)


class SearchService:
    def __init__(self):
        """Initialize the search service with DuckDuckGo Search."""
        self.translation_service = TranslationService()
        
        try:
            # DuckDuckGo doesn't require API key
            self.search_tool = DuckDuckGoSearchRun()
            self.is_available = True
            logger.info("DuckDuckGo Search service initialized successfully")
        except Exception as e:
            self.search_tool = None
            self.is_available = False
            logger.warning(f"Failed to initialize DuckDuckGo Search: {e}")    
            
            
    def search_farming_solutions(self, query: str, language: str = None) -> str:
        """
        Search for practical farming solutions using DuckDuckGo Search.
        
        Args:
            query: The user's query
            language: Detected language ('nepali' or 'english')
            
        Returns:
            Formatted search results as context string
        """
        if not self.is_available:
            logger.warning("Search service not available")
            return ""
        
        try:
            # Detect language if not provided
            if language is None:
                language = self.translation_service.detect_language(query)
            
            # Translate Nepali query to English for better search results
            search_query = query
            if language == 'nepali':
                search_query = self.translation_service.translate_to_english(query)
                logger.info(f"Translated query: {query} -> {search_query}")
            
            # Enhance search query with farming context
            enhanced_query = self._enhance_farming_query(search_query)
            
            # Perform search using DuckDuckGo
            search_results = self.search_tool.run(enhanced_query)
            
            # Format results for LLM context
            formatted_results = self._format_search_results(search_results, query)
            
            logger.info(f"Search completed for query: {enhanced_query}")
            return formatted_results
            
        except Exception as e:
            logger.error(f"Search error: {e}")
            return ""

    def _enhance_farming_query(self, query: str) -> str:
        """
        Enhance the search query with farming and Nepal-specific context.
        """
        # Add farming context keywords
        farming_keywords = [
            "farming", "agriculture", "crop", "pest", "disease", 
            "fertilizer", "pesticide", "organic farming", "Nepal farming"
        ]
        
        # Add Nepal-specific context if not already present
        nepal_context = "Nepal" if "nepal" not in query.lower() else ""
        
        # Create enhanced query
        if any(keyword.lower() in query.lower() for keyword in farming_keywords):
            # Query already has farming context
            enhanced_query = f"{query} {nepal_context}".strip()
        else:
            # Add farming context
            enhanced_query = f"{query} farming agriculture Nepal practical solution"
        
        return enhanced_query

    def _format_search_results(self, search_results: str, original_query: str) -> str:
        """
        Format search results for inclusion in LLM context.
        """
        if not search_results:
            return ""
        
        try:
            # Parse search results (they come as a string)
            results_text = search_results
            
            # Format for context
            formatted_context = f"""
### 🔍 Current Farming Solutions and Information (Related to: {original_query})

{results_text}
"""
            
            return formatted_context
            
        except Exception as e:
            logger.error(f"Error formatting search results: {e}")
            return ""

    def get_specific_farming_info(self, topic: str, location: str = "Nepal") -> str:
        """
        Get specific farming information for a topic and location.
        
        Args:
            topic: Specific farming topic (e.g., "potato disease", "organic fertilizer")
            location: Location context (default: "Nepal")
            
        Returns:
            Formatted search results
        """
        query = f"{topic} {location} farming practical guide solution"
        return self.search_farming_solutions(query, language='english')


# Global instance
search_service = SearchService()
