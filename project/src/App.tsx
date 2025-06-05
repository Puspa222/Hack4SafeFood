import React, { useState } from 'react';
import { Header } from './components/Header';
import { Navigation } from './components/Navigation';
import { LanguageToggle } from './components/LanguageToggle';
import { ChatMessage } from './components/ChatMessage';
import { ChatInput } from './components/ChatInput';
import { LanguageProvider } from './contexts/LanguageContext';
import { Message } from './types';
import { Tips } from './components/Tips';
import { FAQ } from './components/FAQ';
import { Report } from './components/Report';
import { chatService } from './services/chatService';

function App() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [currentView, setCurrentView] = useState<'chat' | 'tips' | 'faq' | 'report'>('chat');
  const [isLoading, setIsLoading] = useState(false);

  const handleSendMessage = async (content: string) => {
    const userMessage: Message = {
      id: Date.now().toString(),
      content,
      role: 'user',
      timestamp: new Date(),
    };

    setMessages((prev) => [...prev, userMessage]);
    setIsLoading(true);

    try {
      const response = await chatService.sendMessage(content);
      
      const aiMessage: Message = {
        id: response.ai_response.message_id,
        content: response.ai_response.message,
        role: 'assistant',
        timestamp: new Date(response.ai_response.created_at),
      };
      
      setMessages((prev) => [...prev, aiMessage]);
    } catch (error) {
      console.error('Error sending message:', error);
      
      // Fallback error message
      const errorMessage: Message = {
        id: (Date.now() + 1).toString(),
        content: 'Sorry, I encountered an error while processing your message. Please make sure the backend server is running and try again.',
        role: 'assistant',
        timestamp: new Date(),
      };
      
      setMessages((prev) => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <LanguageProvider>
      <div className="min-h-screen bg-[#F4FAF2]">
        <Header />
        <Navigation currentView={currentView} onViewChange={setCurrentView} />
        <main className="max-w-3xl mx-auto px-3 sm:px-4 py-4 sm:py-6">
          <div className="flex justify-end mb-4">
            <LanguageToggle />
          </div>
          {currentView === 'chat' && (
            <>
              <div className="bg-white rounded-lg shadow-lg p-4 sm:p-6 mb-4 min-h-[60vh] sm:min-h-[500px] flex flex-col">
                <div className="flex-1 overflow-y-auto space-y-4">
                  {messages.map((message) => (
                    <ChatMessage key={message.id} message={message} />
                  ))}
                </div>
              </div>
              <ChatInput onSend={handleSendMessage} />
            </>
          )}
          {currentView === 'tips' && <Tips />}
          {currentView === 'faq' && <FAQ />}
          {currentView === 'report' && <Report />}
        </main>
      </div>
    </LanguageProvider>
  );
}

export default App