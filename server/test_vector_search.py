#!/usr/bin/env python3
"""
Test script to debug vector similarity search issues
"""
import requests
import json

BASE_URL = "http://127.0.0.1:8000/api"

def test_vectorstore_status():
    """Test vectorstore status"""
    print("=" * 50)
    print("Testing Vectorstore Status")
    print("=" * 50)
    
    try:
        response = requests.get(f"{BASE_URL}/vectorstore/status/")
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
    except Exception as e:
        print(f"Error: {e}")

def test_initialize_vectorstore():
    """Test vectorstore initialization"""
    print("\n" + "=" * 50)
    print("Testing Vectorstore Initialization")
    print("=" * 50)
    
    try:
        response = requests.post(f"{BASE_URL}/vectorstore/initialize/", json={"force_recreate": False})
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
    except Exception as e:
        print(f"Error: {e}")

def test_document_search():
    """Test document search"""
    print("\n" + "=" * 50)
    print("Testing Document Search")
    print("=" * 50)
    
    test_queries = [
        "pesticide safety",
        "food safety",
        "Nepal agriculture",
        "chemical pesticides",
        "farmer training"
    ]
    
    for query in test_queries:
        print(f"\nTesting query: '{query}'")
        print("-" * 30)
        
        try:
            response = requests.post(f"{BASE_URL}/documents/search/", json={
                "query": query,
                "max_docs": 3
            })
            print(f"Status Code: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                print(f"Total found: {data['total_found']}")
                for i, result in enumerate(data['results'], 1):
                    print(f"  Result {i}:")
                    print(f"    Source: {result['source']}")
                    print(f"    Score: {result['relevance_score']:.4f}")
                    print(f"    Content preview: {result['content'][:100]}...")
            else:
                print(f"Error: {response.text}")
                
        except Exception as e:
            print(f"Error: {e}")

def test_debug_search():
    """Test debug search endpoint"""
    print("\n" + "=" * 50)
    print("Testing Debug Search")
    print("=" * 50)
    
    query = "pesticide safety"
    print(f"Debug search for: '{query}'")
    
    try:
        response = requests.post(f"{BASE_URL}/documents/test-search/", json={
            "query": query,
            "max_docs": 5
        })
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"Total found: {data['total_found']}")
            for i, result in enumerate(data['results'], 1):
                print(f"  Result {i}:")
                print(f"    Source: {result['source']}")
                print(f"    Similarity Score: {result['similarity_score']:.6f}")
                print(f"    Content preview: {result['content'][:150]}...")
                print()
        else:
            print(f"Error: {response.text}")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    try:
        test_vectorstore_status()
        test_initialize_vectorstore()
        test_document_search()
        test_debug_search()
        
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to the server. Make sure Django is running on http://127.0.0.1:8000")
    except Exception as e:
        print(f"❌ An error occurred: {e}")
