import React from 'react';
import { Mic } from 'lucide-react';
import { useSpeechRecognition } from '../hooks/useSpeechRecognition';
import clsx from 'clsx';

interface VoiceButtonProps {
  onTranscript: (text: string) => void;
  disabled?: boolean;
}

export function VoiceButton({ onTranscript, disabled = false }: VoiceButtonProps) {
  const { isListening, startListening } = useSpeechRecognition();

  const handleVoiceInput = () => {
    if (disabled) return;
    
    const recognition = startListening();
    if (recognition) {
      recognition.onresult = (event: any) => {
        const transcript = event.results[0][0].transcript;
        onTranscript(transcript);
      };
    }
  };
  return (
    <button
      onClick={handleVoiceInput}
      disabled={disabled}
      className={clsx(
        'p-4 sm:p-6 rounded-full transition-all transform shadow-lg',
        disabled 
          ? 'bg-gray-300 text-gray-500 cursor-not-allowed'
          : isListening
          ? 'bg-red-500 text-white animate-pulse'
          : 'bg-[#FF9800] text-white hover:bg-[#FB8C00] hover:scale-105'
      )}
    >
      <Mic className="size-6 sm:size-8" />
    </button>
  );
}