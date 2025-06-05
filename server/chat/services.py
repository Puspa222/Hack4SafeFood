import os
from typing import List, Dict, Any

from langchain.schema import HumanMessage, AIMessage, SystemMessage
from langchain_google_genai import ChatGoogleGenerativeAI


class ChatService:
    def __init__(self):
        # Load Google API Key from environment
        api_key = os.getenv('GOOGLE_API_KEY')

        if api_key:
            # Initialize Gemini model (Google Generative AI)
            self.llm = ChatGoogleGenerativeAI(
                model="gemini-1.5-flash-002",  
                temperature=0.5, 
                google_api_key=api_key
            )
            self.provider = "google"
        else:
            # Development mode with mock responses
            self.llm = None
            self.provider = "mock"

    def get_system_prompt(self) -> str:
        """
        Return the system prompt defining AI behavior and tone.
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

    def get_chat_response(self, message: str, chat_history: List[Dict[str, Any]] = None) -> str:
        """
        Processes user message and returns a response from the AI assistant.
        Includes system prompt and chat history for context.
        """
        try:
            if self.provider == "google" and self.llm:
                messages = []

                # Add system prompt first
                messages.append(SystemMessage(content=self.get_system_prompt()))

                # Add last 10 messages from history for context
                if chat_history:
                    for msg in chat_history[-10:]:
                        if msg['role'] == 'user':
                            messages.append(HumanMessage(content=msg['message']))
                        elif msg['role'] == 'assistant':
                            messages.append(AIMessage(content=msg['message']))

                # Add current user message
                messages.append(HumanMessage(content=message))

                # Invoke the model with full message list
                response = self.llm.invoke(messages)
                return response.content

            else:
                # Fallback for local development
                return f"यो '{message}' को लागि mock response हो। कृपया .env फाइलमा GOOGLE_API_KEY राखेर असली उत्तर पाउनुहोस्।"

        except Exception as e:
            return f"माफ गर्नुहोस्, तपाईंको सन्देश प्रक्रियामा त्रुटि भयो। त्रुटि: {str(e)}"


chat_service = ChatService()
