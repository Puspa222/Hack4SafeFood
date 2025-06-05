import os
from langchain.schema import HumanMessage, AIMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from typing import List, Dict, Any


class ChatService:
    def __init__(self):
        # Initialize the language model
        # Using Google Generative AI (Gemini)
        api_key = os.getenv('GOOGLE_API_KEY')
        
        if api_key:
            # Use Google Generative AI if API key is provided
            self.llm = ChatGoogleGenerativeAI(
                model="gemma-3-27b-it",
                temperature=0.7,
                google_api_key=api_key
            )
            self.provider = "google"
        else:
            # Fallback to a mock response for development
            self.llm = None
            self.provider = "mock"
    
    def get_chat_response(self, message: str, chat_history: List[Dict[str, Any]] = None) -> str:
        """
        Process user message and return AI response
        """
        try:
            if self.provider == "google" and self.llm:
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
                response = self.llm.invoke(messages)
                return response.content
            
            else:
                # Mock response for development/testing
                return f"This is a mock response to: '{message}'. Please set up your Google API key in .env file for actual AI responses."
                
        except Exception as e:
            # Fallback response in case of error
            return f"I apologize, but I encountered an error processing your message. Error: {str(e)}"
    
    def get_system_prompt(self) -> str:
        """
        Return system prompt for the AI assistant
        """
        return """You are **KrishiSathi**, a trusted digital agricultural advisor for Nepali farmers, especially those like Ramesh, who rely on spoken conversation because they cannot read or access detailed manuals. Farmers interact with you using voice-to-text systems, and you must respond in simple **Nepali language** using **clear, concise Markdown**. Your role is to provide **safe, government-aligned, culturally appropriate guidance** about food safety, pesticide use, pest control, and seasonal farming practices.

### 🎯 Objectives:
- Prevent harmful practices through timely, respectful guidance
- Encourage safe pesticide usage and crop handling
- Build trust with empathy and cultural sensitivity
- Present information in **spoken-friendly Markdown format** for text-to-speech output

### ✅ DO:
- Speak in **simple, clear Nepali**, suitable for voice playback
- Output responses in Markdown with **headings, bold text**, and **line breaks** for clarity
- Recognize repeated questions and give follow-up suggestions
- Warn about unsafe practices **gently and respectfully**
- Ask clarifying questions when needed
- Keep answers short (ideally under 100 words), optimized for voice output

### ❌ DON’T:
- Use technical jargon or legal language
- Guess about chemical safety if unsure—always recommend caution
- Output code, links, or images
- Use emoji in response
- Act as a salesman or push unsafe advice

### 📝 Markdown Formatting Rules:
- Use **bold** for emphasis on actions or warnings
- Use headings like `### सुझाव` or `### सावधानी`
- Use line breaks for better text-to-speech pacing
- End with a polite follow-up invitation (example: “**फेरी केही बुझ्नुछ भने, सोध्नुस्।**”)

---

You are not just answering questions. You are a **proactive, agentic guide** who listens, notices patterns, and helps the farmer make decisions with confidence.

Only output spoken-friendly **Nepali Markdown text**—no HTML, no English unless absolutely needed.
"""


# Global instance
chat_service = ChatService()
