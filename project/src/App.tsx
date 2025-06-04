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

function App() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [currentView, setCurrentView] = useState<'chat' | 'tips' | 'faq' | 'report'>('chat');

  const handleSendMessage = (content: string) => {
    const userMessage: Message = {
      id: Date.now().toString(),
      content,
      role: 'user',
      timestamp: new Date(),
    };

    setMessages((prev) => [...prev, userMessage]);

    // Simulate AI response
    setTimeout(() => {
      const aiMessage: Message = {
        id: (Date.now() + 1).toString(),
        content: 'This is a simulated AI response. The actual AI integration will be implemented later.',
        role: 'assistant',
        timestamp: new Date(),
      };
      setMessages((prev) => [...prev, aiMessage]);
    }, 1000);
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