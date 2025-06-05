import { Message } from '../types';
import { Volume2 } from 'lucide-react';
import { useSpeechSynthesis } from '../hooks/useSpeechSynthesis';
import { MarkdownRenderer } from './MarkdownRenderer';
import clsx from 'clsx';
import { useLanguage } from '../contexts/LanguageContext';

interface ChatMessageProps {
  message: Message;
}

export function ChatMessage({ message }: ChatMessageProps) {
  const { speak, isSpeaking, cancel } = useSpeechSynthesis();
  const { language } = useLanguage();

  const handleSpeakClick = () => {
    if (isSpeaking) {
      cancel();
    } else {
      speak(message.content);
    }
  };

  return (
    <div
      className={clsx(
        'flex w-full mb-4 animate-fade-in',
        message.role === 'assistant' ? 'justify-start' : 'justify-end'
      )}
    >
      <div
        className={clsx(
          'max-w-[80%] rounded-lg px-4 py-3 shadow-sm',
          message.role === 'assistant'
            ? 'bg-[#E8F5E9] text-gray-800'
            : 'bg-white text-gray-800'
        )}
      >        <div className="flex justify-between items-start gap-2">
          {message.role === 'assistant' ? (
            <MarkdownRenderer content={message.content} className="flex-1" />
          ) : (
            <p className="text-lg leading-relaxed flex-1">{message.content}</p>
          )}          {message.role === 'assistant' && (
            <button
              onClick={handleSpeakClick}
              className={clsx(
                "p-1.5 rounded-full flex-shrink-0 transition-all duration-300",
                isSpeaking 
                  ? "text-green-700 bg-green-100 animate-pulse scale-110" 
                  : "text-[#2E7D32] hover:text-[#1B5E20] hover:bg-[#F4FAF2]"
              )}
              title={isSpeaking 
                ? language === 'ne' ? "बोल्न रोक्नुहोस्" : "Stop speaking" 
                : language === 'ne' ? "सन्देश सुन्नुहोस्" : "Listen to message"
              }
              aria-label={isSpeaking ? "Stop speaking" : "Speak message"}
            >
              <Volume2 
                size={20} 
                className={clsx(
                  "transition-transform",
                  isSpeaking && "animate-[pulse_1.5s_ease-in-out_infinite]"
                )} 
              />
              {isSpeaking && (
                <span className="sr-only">
                  {language === 'ne' ? "बोल्दै..." : "Speaking..."}
                </span>
              )}
            </button>
          )}
        </div>
        <div className="text-xs text-gray-500 mt-1">
          {message.timestamp.toLocaleTimeString()}
        </div>
      </div>
    </div>
  );
}