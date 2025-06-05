import os
from typing import List, Dict, Any

from langchain.schema import HumanMessage, AIMessage, SystemMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from .vector_service_new import vector_service
from .search_service import search_service
from .translation_service import TranslationService


class ChatService:
    def __init__(self):
        # Load Google API Key from environment
        api_key = os.getenv('GOOGLE_API_KEY')
        
        # Initialize translation service
        self.translation_service = TranslationService()

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

    def get_system_prompt(self, context: str = "", search_context: str = "") -> str:
        """
        Return the enhanced system prompt defining AI behavior and tone.
        Includes relevant context from documents and real-time search results.
        """
        base_prompt = """
तपाईं **कृषिसाथी** हो — एक अत्यधिक व्यावहारिक र भरपर्दो डिजिटल कृषि सल्लाहकार, जसले नेपाली किसानहरूलाई ठोस, कार्यान्वयन योग्य समाधान प्रदान गर्छ। तपाईंको मुख्य उद्देश्य भनेको किसानहरूलाई तत्काल कार्य गर्न सकिने व्यावहारिक सल्लाह दिनु हो।

### 🎯 मुख्य सिद्धान्तहरू:
- **व्यावहारिक समाधान मात्र**: सिद्धान्त नभनेर ठोस कदमहरू बताउनुहोस्
- **तत्काल कार्यान्वयन**: किसानले आज नै गर्न सक्ने कामहरू सुझाउनुहोस्
- **स्थानीय उपलब्धता**: नेपालमा सजिलै पाइने सामग्री/विधिहरू बताउनुहोस्
- **लागत प्रभावी**: कम खर्चिला र प्रभावकारी समाधानहरूमा जोड दिनुहोस्
- **सुरक्षित अभ्यास**: सधैं स्वास्थ्य र वातावरण सुरक्षित तरिकाहरू सुझाउनुहोस्

### 🚀 व्यावहारिक उत्तर ढाँचा:
**तत्काल कार्यहरू (आज गर्नुहोस्):**
- स्पष्ट, क्रमबद्ध कदमहरू
- आवश्यक सामग्रीको सूची
- समय र मात्राको जानकारी

**७ दिनको योजना:**
- साप्ताहिक कार्यतालिका
- अपेक्षित परिणामहरू

**सावधानीहरू:**
- के नगर्ने
- कहिले विशेषज्ञसँग सल्लाह लिने

### 🎯 उत्तर गुणस्तर आवश्यकताहरू:
- **निर्णायक बनुन**: "सम्भवतः" जस्ता शब्द नप्रयोग गर्नुहोस्
- **संख्यामा बोल्नुहोस्**: "केही" भन्नुको सट्टा "२-३ चम्चा" भन्नुहोस्
- **समयसीमा दिनुहोस्**: "चाँडै" भन्नुको सट्टा "३ दिनमा" भन्नुहोस्
- **परिणाम बताउनुहोस्**: "यसले के हुन्छ" भनेर स्पष्ट पार्नुहोस्

### ✅ गर्नुहोस्:
- **तुरुन्त कार्य योग्य सल्लाह** दिनुहोस्
- **स्थानीय सामग्री** (नीम, बेसार, दही, आदि) को प्रयोग सुझाउनुहोस्
- **घरेलु उपचार** देखि **उन्नत प्राविधिक** सम्मका विकल्प दिनुहोस्
- **लागत अनुमान** दिनुहोस् जहाँ सम्भव छ
- Markdown प्रयोग गर्नुहोस्: `### शीर्षक`, **Bold**, bullet points
- **सरल नेपाली** मा ५०-१५० शब्दमा जवाफ दिनुहोस्

### ❌ नगर्नुहोस्:
- सामान्यीकृत सल्लाह नदिनुहोस्
- "सल्लाह लिनुहोस्" मात्र भनेर छोड्नुहोस्
- अनिश्चित भाषा प्रयोग नगर्नुहोस्
- HTML, emoji वा अंग्रेजी प्रयोग नगर्नुहोस्

### 🌾 विशेष फोकस क्षेत्रहरू:
- **कीरा/रोग नियन्त्रण**: तत्काल र दीर्घकालीन समाधान
- **माटो स्वास्थ्य**: घरेलु जैविक उर्वरक निर्माण
- **फसल व्यवस्थापन**: रोपाई देखि कटाई सम्म
- **पोस्ट हार्भेस्ट**: भण्डारण र बजारीकरण
- **मौसमी तयारी**: आगामी मौसमका लागि योजना

---
**तपाईं सिर्फ जानकारी दिने AI होइन, तपाईं समस्या समाधान गर्ने व्यावहारिक कृषि विशेषज्ञ हुनुहुन्छ।**
"""

        # Add document context if available
        if context:
            base_prompt += f"""

### 📚 अनुसन्धान आधारित जानकारी:
{context}
"""

        # Add real-time search context if available
        if search_context:
            base_prompt += f"""

### 🌐 हालको व्यावहारिक समाधानहरू:
{search_context}

माथिको जानकारीलाई स्थानीय नेपाली परिस्थितिमा अनुकूलन गरेर व्यावहारिक सल्लाह दिनुहोस्।
"""

        base_prompt += """

### 🎯 अन्तिम निर्देशन:
सबै उत्तरहरू **कार्यान्वयन योग्य, स्पष्ट र तत्काल लागू गर्न सकिने** हुनुपर्छ। किसानले तपाईंको सल्लाह सुनेपछि तुरुन्त काम गर्न सक्नुपर्छ।
"""
        
        return base_prompt

    def get_chat_response(self, message: str, chat_history: List[Dict[str, Any]] = None) -> str:
        """
        Processes user message and returns a response from the AI assistant.
        Includes system prompt, chat history, relevant document context, and real-time search results.
        """
        try:
            if self.provider == "google" and self.llm:
                # Detect language and translate if necessary
                detected_language = self.translation_service.detect_language(message)
                
                # Get relevant context from vector store
                context = ""
                try:
                    context = vector_service.get_relevant_context(message, max_docs=3)
                except Exception as e:
                    print(f"Vector search error: {e}")
                    # Continue without context if vector search fails
                
                # Get real-time search results for practical solutions
                search_context = ""
                try:
                    if search_service.is_available:
                        search_context = search_service.search_farming_solutions(message, detected_language)
                except Exception as e:
                    print(f"Search service error: {e}")
                    # Continue without search context if search fails
                
                messages = []

                # Add enhanced system prompt with both contexts
                messages.append(SystemMessage(content=self.get_system_prompt(context, search_context)))

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
