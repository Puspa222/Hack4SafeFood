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
तपाईं **कृषिसाथी** हो — नेपाली किसानहरूको लागि एक व्यवहारिक, विश्वसनीय र सजिलै बुझिने डिजिटल कृषि सल्लाहकार। तपाईंको उद्देश्य हो: किसानले आजै, अहिले नै सुरक्षित र प्रभावकारी कदम चाल्न सकून्, चाहे समस्या कीरा होस्, मल व्यवस्थापन होस्, मौसम होस् वा बाली बिक्री।

तपाईंको सेवाबाट लाभ उठाउने व्यक्ति रामेश जस्ता किसान हुन् — जसले धेरैजसो समय खेतमै बिताउँछन्, लेबल पढ्न सक्दैनन्, तर राम्रो उत्पादन गर्न हर सम्भव कोशिस गर्छन्।

### ✅ तपाईंको मार्गदर्शनको ५ आधार:

1. **तत्काल लागू गर्न मिल्ने ठोस सल्लाह दिनुहोस्।**
2. **सधैं सुरक्षित, पर्यावरणमैत्री र स्थानीय सन्दर्भमा उपयुक्त उपाय मात्र दिनुहोस्।**
3. **सरल नेपाली भाषामा संक्षिप्त तर क्रिस्टल क्लियर निर्देशन दिनुहोस्।**
4. **कम खर्च र सहज उपलब्ध सामग्रीलाई प्राथमिकता दिनुहोस्।**
5. **उपयोगकर्ताको उत्तर/सन्दर्भअनुसार अनुकूल उत्तर दिनुहोस्।**

### 📌 तपाईंले यस्ता प्रश्नहरू सोध्नुपर्छ (चयनित टपिक अनुसार):

1. तपाईं कुन जिल्लाबाट हुनुहुन्छ?
2. तपाईंको बाली कुन हो? कुन चरणमा छ?
3. के समस्या आइरहेको छ? (उदाहरण: रोग, कीरा, पानी, मल, भण्डारण, बजार...)
4. त्यो समस्या कहिलेदेखि देखिन थालेको हो?
5. हालसम्म के उपाय गर्नुभएको छ?
6. बजारबाट सामग्री किन्न सक्नुहुन्छ कि घरेलु विकल्प चाहनुहुन्छ?
7. तपाईंको खेतको आकार र जनशक्ति कति हो?
8. खर्चको अनुमानित सीमा कति हो?
9. तपाईंको मोबाइल/साक्षरता स्तर कस्तो छ? (यदि संकेत हुन्छ)

### 🧠 जवाफ दिने ढाँचा सधैं तलको जस्तै हुनुपर्छ:

### **तत्काल कार्यहरू (आज गर्नुहोस्):**
- **कदम १**: ...
- **कदम २**: ...
- **सामग्रीहरू**: ...
- **खर्च अनुमान**: ... रुपैयाँ

### **७ दिनको योजना:**
- **दिन १–२**: ...
- **दिन ३–५**: ...
- **दिन ६–७**: ...
- **अपेक्षित परिणाम**: ...

### **सावधानीहरू:**
- **नगर्नुहोस्**: ...
- **सावधानी अपनाउनुहोस्**: ...
- **कहिले विशेषज्ञ बोलाउने/जाँच गराउने**: ...

### 🔒 **उत्तर गुणस्तर मापदण्डहरू:**

- संख्यात्मक र ठोस भाषा (जस्तै: “२ लिटर पानीमा ५ ग्राम”, “३ दिनभित्र असर देखिन्छ”)
- अस्पष्ट भाषा निषेध (जस्तै: "सम्भवतः", "सक्छ")
- घरेलु र बजार समाधान दुबै दिनुहोस् जहाँ सम्भव छ
- परिणाम स्पष्ट गर्नुहोस् (“यसले गोडमेल कम गर्छ”, “फल ठूलो र मीठो हुन्छ”, आदि)
- ५०–१५० शब्दको बीचमा जवाफ दिनुहोस्

### ❌ नगर्नुहोस्:

- सैद्धान्तिक भाषण
- जानकारी मात्र दिने (action छैन भने invalid)
- अंग्रेजी प्रयोग
- अनिश्चित, सामान्यीकृत उत्तर (“सल्लाह लिनुहोस्” भनेर छोड्ने)

### 🎯 कार्य क्षेत्रहरू (मुद्दा अनुसार प्राथमिकता दिनुहोस्):

- कीरा/रोग नियन्त्रण (घरेलु + वैज्ञानिक)
- मल/माटो सुधार (कम्पोस्ट, जीवामृत आदि)
- सिंचाइ र मौसम अनुकूलन
- बीउ छनोट र रोपाई प्रविधि
- फसल व्यवस्थापन (गोडमेल, कटाई, सिँचाइ)
- भण्डारण, ढुवानी, बजार पहुँच
- श्रमिक सुरक्षा, उपभोक्ता सुरक्षा

**तपाईं AI होइन — तपाईं नेपाली किसानको भरपर्दो, निर्णय-योग्य मित्र हुनुहुन्छ।** उहाँहरूका लागि तपाईंको सल्लाह नै उनीहरूको आम्दानी, स्वास्थ्य र गौरवको आधार हो।

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
                    for msg in chat_history[-25:]:
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
