import React, { useState } from 'react';
import { SendHorizontal } from 'lucide-react';
import { VoiceButton } from './VoiceButton';
import { useLanguage } from '../contexts/LanguageContext';
import { translations } from '../utils/translations';

interface ChatInputProps {
  onSend: (message: string) => void;
}

export function ChatInput({ onSend }: ChatInputProps) {
  const [input, setInput] = useState('');
  const { language } = useLanguage();

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (input.trim()) {
      onSend(input);
      setInput('');
    }
  };

  return (
    <form onSubmit={handleSubmit} className="bg-white shadow-lg p-3 sm:p-4 rounded-t-xl">
      <div className="max-w-4xl mx-auto flex items-end gap-2 sm:gap-4">
        <div className="flex-1 relative">
          <textarea
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder={translations.inputPlaceholder[language]}
            className="w-full p-3 sm:p-4 pr-12 rounded-xl border border-gray-200 focus:border-[#2E7D32] focus:ring-1 focus:ring-[#2E7D32] resize-none text-base sm:text-lg"
            rows={2}
          />
          <button
            type="submit"
            className="absolute right-3 sm:right-4 bottom-3 sm:bottom-4 text-[#2E7D32] hover:text-[#1B5E20]"
          >
            <SendHorizontal size={24} />
          </button>
        </div>
        <VoiceButton onTranscript={setInput} />
      </div>
    </form>
  );
}