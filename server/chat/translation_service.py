import os
import logging
from typing import Optional
from langchain_google_genai import ChatGoogleGenerativeAI

logger = logging.getLogger(__name__)


class TranslationService:
    def __init__(self):
        """Initialize the translation service with Google Gemini."""
        api_key = os.getenv('GOOGLE_API_KEY')
        
        if api_key:
            self.llm = ChatGoogleGenerativeAI(
                model="gemini-1.5-flash-002",
                temperature=0.1,  # Low temperature for consistent translation
                google_api_key=api_key
            )
            self.is_available = True
        else:
            self.llm = None
            self.is_available = False
            logger.warning("No GOOGLE_API_KEY found. Translation service will be disabled.")

    def detect_language(self, text: str) -> str:
        """
        Simple language detection based on script.
        Returns 'nepali' if Nepali script is detected, 'english' otherwise.
        """
        # Check for Devanagari script (Nepali)
        nepali_chars = any('\u0900' <= char <= '\u097F' for char in text)
        return 'nepali' if nepali_chars else 'english'

    def translate_to_english(self, text: str) -> str:
        """
        Translate Nepali text to English using Google Gemini.
        Returns original text if it's already in English or if translation fails.
        """
        if not self.is_available:
            logger.warning("Translation service not available, returning original text")
            return text

        # Check if text is already in English
        if self.detect_language(text) == 'english':
            logger.debug("Text is already in English, no translation needed")
            return text

        try:
            prompt = f"""Translate the following Nepali text to English. Focus on agricultural and farming context. Only provide the English translation, nothing else:

Nepali text: {text}

English translation:"""

            response = self.llm.invoke(prompt)
            translated_text = response.content.strip()
            
            logger.info(f"Translated '{text[:50]}...' to '{translated_text[:50]}...'")
            return translated_text

        except Exception as e:
            logger.error(f"Translation failed: {str(e)}")
            # Return original text if translation fails
            return text

    def translate_query_for_rag(self, query: str) -> str:
        """
        Translate query for RAG search if needed.
        This is the main method to use for translating user queries before RAG search.
        """
        if not query.strip():
            return query

        # Detect language and translate if Nepali
        if self.detect_language(query) == 'nepali':
            logger.info(f"Detected Nepali query, translating: '{query[:50]}...'")
            return self.translate_to_english(query)
        else:
            logger.debug("Query is in English, no translation needed")
            return query


# Global instance
translation_service = TranslationService()
