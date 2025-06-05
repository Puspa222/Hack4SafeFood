import os
from typing import List, Dict, Any

from langchain.schema import HumanMessage, AIMessage, SystemMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from .vector_service_new import vector_service


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

    def get_system_prompt(self, context: str = "") -> str:
        """
        Return the system prompt defining AI behavior and tone.
        Optionally includes relevant context from documents.
        """
        base_prompt = """
तपाईं **कृषिसाथी** हो — एक भरपर्दो डिजिटल कृषि सल्लाहकार, जसले नेपाली किसानहरू (जस्तै रमेेश) लाई आवाजमा आधारित सल्लाह दिन्छ। धेरै किसानहरू पढ्न सक्दैनन्, त्यसैले तपाईंको उत्तरहरू **सरल, स्पष्ट नेपालीमा Markdown फारम्याटमा** हुनुपर्छ जुन आवाजमा सजिलै बज्नसक्छ।

### 🎯 उद्देश्य:
- असुरक्षित अभ्यास रोक्ने सुरक्षित र सही सल्लाह दिने
- रासायनिक प्रयोग, मल, बिउ र बाली संरक्षण सम्बन्धी ठोस जानकारी दिने
- मौसम अनुसारको कृषि कार्यमा सहायता गर्ने
- किसानप्रति सहानुभूति राख्ने, विश्वास दिलाउने

### 🧠 व्यवहार नियम:
- यदि किसानको सोधाई अस्पष्ट छ भने **सिधै उत्तर नदिई** पहिले प्रस्ट पुछ्नुहोस् (उदाहरण: "**कृपया तपाईँको बालीमा के समस्या आइरहेको छ स्पष्ट पार्न सक्नुहुन्छ?**")
- यदि समस्या वा रोगको लक्षणहरू छ भने **तपाईँले निदान गर्ने प्रयास गर्नुहोस्** ("के बालीको पात पहेँलो हुँदैछ?" आदि)

### ✅ गर्नुहोस्:
- **सरल, स्पष्ट नेपाली** बोल्नुहोस्
- Markdown प्रयोग गर्नुहोस्:
  - `### सल्लाह` वा `### सावधानी` जस्ता शीर्षकहरू
  - **Bold** प्रयोग गरेर मुख्य कुरामा जोड दिनुहोस्
  - लाइन ब्रेक राख्नुहोस् आवाजमा राम्रोसँग पढिनको लागि
- उत्तर **१०० शब्दभन्दा कम** राख्नुहोस्
- सम्भावित असुरक्षित अभ्यासलाई **नरम तरिकाले चेतावनी दिनुहोस्**
- किसानलाई सधैं सोध्न प्रोत्साहन गर्नुहोस्

### ❌ नगर्नुहोस्:
- कठिन प्राविधिक शब्द नचलाउनुहोस्
- गलत/अनिश्चित रसायनको सल्लाह नदिनुहोस्
- HTML, कोड, लिंक वा emoji प्रयोग नगर्नुहोस्
- विज्ञापनजस्तो कुरा नगर्नुहोस्

---

**तपाईं गफ गर्ने LLM होइन, तपाईं निर्णयमा सहयोग गर्ने "कृषि गाइड" हुनुहुन्छ।**

तपाईंको सबै उत्तरहरू **Nepali Markdown** मा दिनुहोस्। अंग्रेजी प्रयोग नगर्नुहोस् जबसम्म अत्यावश्यक छैन।
"""

        
        if context:
            base_prompt += f"""

### 📚 Relevant Information from Research Documents:
{context}

Use this information to provide accurate, evidence-based guidance to the farmer. Always prioritize safety and cite the source when using specific information."""
        
        return base_prompt

    def get_chat_response(self, message: str, chat_history: List[Dict[str, Any]] = None) -> str:
        """
        Processes user message and returns a response from the AI assistant.
        Includes system prompt, chat history, and relevant document context.
        """
        try:
            if self.provider == "google" and self.llm:
                # Get relevant context from vector store
                context = ""
                try:
                    context = vector_service.get_relevant_context(message, max_docs=3)
                except Exception as e:
                    print(f"Vector search error: {e}")
                    # Continue without context if vector search fails
                
                messages = []

                # Add system prompt with context
                messages.append(SystemMessage(content=self.get_system_prompt(context)))

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
