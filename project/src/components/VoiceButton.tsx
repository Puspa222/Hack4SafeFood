import React from 'react';
import { Mic } from 'lucide-react';
import { useSpeechRecognition } from '../hooks/useSpeechRecognition';
import clsx from 'clsx';

interface VoiceButtonProps {
  onTranscript: (text: string) => void;
}

export function VoiceButton({ onTranscript }: VoiceButtonProps) {
  const { isListening, startListening } = useSpeechRecognition();

  const handleVoiceInput = () => {
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
      className={clsx(
        'p-4 sm:p-6 rounded-full transition-all transform hover:scale-105 shadow-lg',
        isListening
          ? 'bg-red-500 text-white animate-pulse'
          : 'bg-[#FF9800] text-white hover:bg-[#FB8C00]'
      )}
    >
      <Mic className="size-6 sm:size-8" />
    </button>
  );
}