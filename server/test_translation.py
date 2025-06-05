#!/usr/bin/env python3

import os
import sys
import django
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).resolve().parent.parent
sys.path.append(str(project_root))

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'server.settings')
django.setup()

from chat.translation_service import translation_service
from chat.vector_service import vector_service

def test_translation():
    """Test the translation functionality."""
    
    print("=== Testing Translation Service ===")
    
    # Test Nepali text
    nepali_text = "कीटनाशक कसरी प्रयोग गर्ने?"
    print(f"Original Nepali: {nepali_text}")
    
    # Test language detection
    language = translation_service.detect_language(nepali_text)
    print(f"Detected language: {language}")
    
    # Test translation
    if translation_service.is_available:
        translated = translation_service.translate_to_english(nepali_text)
        print(f"Translated to English: {translated}")
        
        # Test query translation for RAG
        rag_query = translation_service.translate_query_for_rag(nepali_text)
        print(f"RAG query: {rag_query}")
    else:
        print("Translation service not available (missing GOOGLE_API_KEY)")
    
    print("\n" + "="*50)
    
    # Test English text (should not be translated)
    english_text = "How to use pesticides safely?"
    print(f"Original English: {english_text}")
    
    language = translation_service.detect_language(english_text)
    print(f"Detected language: {language}")
    
    rag_query = translation_service.translate_query_for_rag(english_text)
    print(f"RAG query: {rag_query}")
    
    print("\n=== Testing Vector Search with Translation ===")
    
    # Test vector search with Nepali query
    if vector_service.load_existing_vectorstore():
        print("Vector store loaded successfully")
        
        # Search with Nepali query
        nepali_query = "कीटनाशक"
        print(f"Searching with Nepali query: {nepali_query}")
        results = vector_service.similarity_search(nepali_query, k=2)
        print(f"Found {len(results)} results")
        
        for i, doc in enumerate(results):
            print(f"Result {i+1}: {doc.page_content[:100]}...")
    else:
        print("Vector store not available")

if __name__ == "__main__":
    test_translation()
