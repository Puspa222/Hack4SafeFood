import React from 'react';
import { Message } from '../types';
import { Volume2 } from 'lucide-react';
import { useSpeechSynthesis } from '../hooks/useSpeechSynthesis';
import { MarkdownRenderer } from './MarkdownRenderer';
import clsx from 'clsx';

interface ChatMessageProps {
  message: Message;
}

export function ChatMessage({ message }: ChatMessageProps) {
  const { speak } = useSpeechSynthesis();

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
          )}
          {message.role === 'assistant' && (
            <button
              onClick={() => speak(message.content)}
              className="text-[#2E7D32] hover:text-[#1B5E20] p-1 rounded-full hover:bg-[#F4FAF2] flex-shrink-0"
            >
              <Volume2 size={20} />
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