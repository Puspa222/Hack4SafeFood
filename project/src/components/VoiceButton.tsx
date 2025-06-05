import { useState, useRef, useEffect } from 'react';
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
  const [autoMode, setAutoMode] = useState(false);
  const recognitionRef = useRef<any>(null);

  // Continuous voice chat loop
  useEffect(() => {
    let stopped = false;
    const loop = async () => {
      while (autoMode && !stopped) {
        await new Promise<void>(resolve => {
          const recognition = startListening((result) => {
            if (result.isFinal && result.transcript.trim()) {
              onTranscript(result.transcript.trim());
              resolve();
            }
          }, { continuous: false, interimResults: true, maxAlternatives: 1 });
          recognitionRef.current = recognition;
          if (recognition) {
            recognition.addEventListener('end', () => {
              recognitionRef.current = null;
            });
          }
        });
      }
    };
    if (autoMode) loop();
    return () => { stopped = true; if (recognitionRef.current) stopListening(recognitionRef.current); };
    // eslint-disable-next-line
  }, [autoMode]);

  const handleVoiceInput = () => {
    if (disabled) return;
    if (isRecording) {
      if (recognitionRef.current) {
        stopListening(recognitionRef.current);
        recognitionRef.current = null;
      }
      setIsRecording(false);
      setAutoMode(false);
    } else {
      setIsRecording(true);
      setAutoMode(true);
    }
  };

  useEffect(() => {
    if (!autoMode) setIsRecording(false);
  }, [autoMode]);

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
        title={isRecording ? 'Click to stop voice chat' : 'Click to start voice chat'}
      >
        {isRecording ? (
          <MicOff className="size-6 sm:size-8" />
        ) : (
          <Mic className="size-6 sm:size-8" />
        )}
      </button>
      <span className="text-xs text-gray-500">{isRecording ? 'Voice Chat On' : 'Voice Chat Off'}</span>
      {error && (
        <div className="text-red-500 text-xs max-w-32 text-center">
          {error}
        </div>
      )}
    </div>
  );
}