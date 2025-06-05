#!/usr/bin/env python3
"""
Simple test script to demonstrate the chat API functionality
"""
import requests
import json

BASE_URL = "http://127.0.0.1:8000/api"

def test_chat_api():
    print("Testing Chat API with Langchain Integration")
    print("=" * 50)
    
    # Test 1: Create a new chat
    print("\n1. Creating a new chat...")
    response = requests.post(f"{BASE_URL}/chat/create/")
    
    if response.status_code == 201:
        chat_data = response.json()
        chat_id = chat_data['chat_id']
        print(f"✅ Chat created successfully with ID: {chat_id}")
    else:
        print(f"❌ Failed to create chat: {response.status_code}")
        return
    
    # Test 2: Send a message to the chat
    print(f"\n2. Sending a message to chat {chat_id}...")
    message_data = {
        "message": "Hello! Can you tell me about food safety practices?",
        "role": "user",
        "chat": chat_id
    }
    
    response = requests.post(f"{BASE_URL}/message/send/", json=message_data)
    
    if response.status_code == 201:
        result = response.json()
        print("✅ Message sent and processed successfully!")
        print(f"User Message: {result['user_message']['message']}")
        print(f"AI Response: {result['ai_response']['message']}")
    else:
        print(f"❌ Failed to send message: {response.status_code}")
        print(response.text)
        return
    
    # Test 3: Send another message to test context
    print(f"\n3. Sending follow-up message...")
    message_data = {
        "message": "What about pesticide safety?",
        "role": "user",
        "chat": chat_id
    }
    
    response = requests.post(f"{BASE_URL}/message/send/", json=message_data)
    
    if response.status_code == 201:
        result = response.json()
        print("✅ Follow-up message processed!")
        print(f"User Message: {result['user_message']['message']}")
        print(f"AI Response: {result['ai_response']['message']}")
    else:
        print(f"❌ Failed to send follow-up message: {response.status_code}")
        return
    
    # Test 4: Retrieve all messages from the chat
    print(f"\n4. Retrieving all messages from chat {chat_id}...")
    response = requests.get(f"{BASE_URL}/chat/{chat_id}/messages/")
    
    if response.status_code == 200:
        messages = response.json()
        print(f"✅ Retrieved {len(messages)} messages:")
        for i, msg in enumerate(messages, 1):
            print(f"  {i}. [{msg['role']}]: {msg['message'][:100]}...")
    else:
        print(f"❌ Failed to retrieve messages: {response.status_code}")

if __name__ == "__main__":
    try:
        test_chat_api()
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to the server. Make sure Django is running on http://127.0.0.1:8000")
    except Exception as e:
        print(f"❌ An error occurred: {e}")
