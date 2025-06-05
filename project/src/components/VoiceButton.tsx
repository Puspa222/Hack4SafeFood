import { useState, useRef } from 'react';
import { Mic, MicOff } from 'lucide-react';
import { useSpeechRecognition } from '../hooks/useSpeechRecognition';
import clsx from 'clsx';

interface VoiceButtonProps {
  onTranscript: (text: string) => void;
  disabled?: boolean;
}

export function VoiceButton({ onTranscript, disabled = false }: VoiceButtonProps) {
  const { isListening, error, startListening, stopListening } = useSpeechRecognition();
  const [isRecording, setIsRecording] = useState(false);
  const recognitionRef = useRef<any>(null);

  const handleVoiceInput = () => {
    if (disabled) return;
    
    if (isRecording) {
      // Stop recording
      if (recognitionRef.current) {
        stopListening(recognitionRef.current);
        recognitionRef.current = null;
      }
      setIsRecording(false);
    } else {
      // Start recording
      setIsRecording(true);
      
      const recognition = startListening(
        (result) => {
          // Handle real-time results
          if (result.isFinal) {
            onTranscript(result.transcript);
            setIsRecording(false);
            recognitionRef.current = null;
          }
        },
        {
          continuous: false,
          interimResults: true,
          maxAlternatives: 1
        }
      );
      
      if (recognition) {
        recognitionRef.current = recognition;
        
        // Handle recognition end
        recognition.addEventListener('end', () => {
          setIsRecording(false);
          recognitionRef.current = null;
        });
      } else {
        setIsRecording(false);
      }
    }
  };

  return (
    <div className="flex flex-col items-center gap-2">
      <button
        onClick={handleVoiceInput}
        disabled={disabled}
        className={clsx(
          'p-4 sm:p-6 rounded-full transition-all transform shadow-lg',
          disabled 
            ? 'bg-gray-300 text-gray-500 cursor-not-allowed'
            : isListening || isRecording
            ? 'bg-red-500 text-white animate-pulse'
            : 'bg-[#FF9800] text-white hover:bg-[#FB8C00] hover:scale-105'
        )}
        title={isRecording ? 'Click to stop recording' : 'Click to start voice input'}
      >
        {isRecording ? (
          <MicOff className="size-6 sm:size-8" />
        ) : (
          <Mic className="size-6 sm:size-8" />
        )}
      </button>
      
      {error && (
        <div className="text-red-500 text-xs max-w-32 text-center">
          {error}
        </div>
      )}
    </div>
  );
}