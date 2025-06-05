import os
from langchain.schema import HumanMessage, AIMessage
from langchain_openai import ChatOpenAI
from typing import List, Dict, Any


class ChatService:
    def __init__(self):
        # Initialize the language model
        # You can replace this with other providers like Ollama for local models
        api_key = os.getenv('OPENAI_API_KEY')
        
        if api_key and api_key != 'your_openai_api_key_here':
            # Use OpenAI if API key is provided
            self.llm = ChatOpenAI(
                model="gpt-3.5-turbo",
                temperature=0.7,
                openai_api_key=api_key
            )
            self.provider = "openai"
        else:
            # Fallback to a mock response for development
            self.llm = None
            self.provider = "mock"
    
    def get_chat_response(self, message: str, chat_history: List[Dict[str, Any]] = None) -> str:
        """
        Process user message and return AI response
        """
        try:
            if self.provider == "openai" and self.llm:
                # Convert chat history to langchain format
                messages = []
                if chat_history:
                    for msg in chat_history[-10:]:  # Keep last 10 messages for context
                        if msg['role'] == 'user':
                            messages.append(HumanMessage(content=msg['message']))
                        elif msg['role'] == 'assistant':
                            messages.append(AIMessage(content=msg['message']))
                
                # Add current message
                messages.append(HumanMessage(content=message))
                
                # Get response from LLM
                response = self.llm(messages)
                return response.content
            
            else:
                # Mock response for development/testing
                return f"This is a mock response to: '{message}'. Please set up your OpenAI API key in .env file for actual AI responses."
                
        except Exception as e:
            # Fallback response in case of error
            return f"I apologize, but I encountered an error processing your message. Error: {str(e)}"
    
    def get_system_prompt(self) -> str:
        """
        Return system prompt for the AI assistant
        """
        return """You are a helpful AI assistant focused on food safety and agriculture. 
        You can help users with questions about pesticides, food safety practices, 
        agricultural methods, and related topics. Please provide accurate, helpful, 
        and concise responses."""


# Global instance
chat_service = ChatService()
