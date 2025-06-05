import { useState, useCallback } from 'react';
import { useLanguage } from '../contexts/LanguageContext';

// Extend Window interface to include SpeechRecognition
declare global {
  interface Window {
    SpeechRecognition: any;
    webkitSpeechRecognition: any;
  }
}

export interface SpeechRecognitionResult {
  transcript: string;
  confidence: number;
  isFinal: boolean;
}

export function useSpeechRecognition() {
  const [isListening, setIsListening] = useState(false);
  const [transcript, setTranscript] = useState('');
  const [error, setError] = useState<string | null>(null);
  const { language } = useLanguage();

  const startListening = useCallback((
    onResult?: (result: SpeechRecognitionResult) => void,
    options?: {
      continuous?: boolean;
      interimResults?: boolean;
      maxAlternatives?: number;
    }
  ) => {
    // Check for SpeechRecognition support (standard or webkit)
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    
    if (!SpeechRecognition) {
      setError('Speech recognition not supported in this browser');
      return null;
    }

    try {
      const recognition = new SpeechRecognition();
      
      // Configure recognition based on Web Speech API specification
      recognition.lang = language === 'ne' ? 'ne-NP' : 'en-US';
      recognition.continuous = options?.continuous ?? false;
      recognition.interimResults = options?.interimResults ?? false;
      recognition.maxAlternatives = options?.maxAlternatives ?? 1;

      // Event handlers as per Web Speech API spec
      recognition.onstart = () => {
        setIsListening(true);
        setError(null);
      };

      recognition.onend = () => {
        setIsListening(false);
      };

      recognition.onerror = (event: any) => {
        setIsListening(false);
        
        // Handle different error types as per spec
        switch (event.error) {
          case 'no-speech':
            setError('No speech was detected');
            break;
          case 'aborted':
            setError('Speech recognition was aborted');
            break;
          case 'audio-capture':
            setError('Audio capture failed');
            break;
          case 'network':
            setError('Network error occurred');
            break;
          case 'not-allowed':
            setError('Speech recognition not allowed');
            break;
          case 'service-not-allowed':
            setError('Speech service not allowed');
            break;
          case 'language-not-supported':
            setError('Language not supported');
            break;
          default:
            setError('Speech recognition error occurred');
        }
      };

      recognition.onresult = (event: any) => {
        let finalTranscript = '';
        let interimTranscript = '';

        // Process results as per SpeechRecognitionEvent specification
        for (let i = event.resultIndex; i < event.results.length; i++) {
          const result = event.results[i];
          const alternative = result[0]; // Get the best alternative
          
          if (result.isFinal) {
            finalTranscript += alternative.transcript;
          } else {
            interimTranscript += alternative.transcript;
          }

          // Call custom result handler if provided
          if (onResult) {
            onResult({
              transcript: alternative.transcript,
              confidence: alternative.confidence,
              isFinal: result.isFinal
            });
          }
        }

        // Update transcript state
        if (finalTranscript) {
          setTranscript(prev => prev + finalTranscript);
        }
      };

      recognition.onnomatch = () => {
        setError('No recognition result matched');
      };

      recognition.onsoundstart = () => {
        // Sound detected
      };

      recognition.onsoundend = () => {
        // Sound ended
      };

      recognition.onspeechstart = () => {
        // Speech detected
      };

      recognition.onspeechend = () => {
        // Speech ended
      };

      recognition.onaudiostart = () => {
        // Audio capture started
      };

      recognition.onaudioend = () => {
        // Audio capture ended
      };

      // Start recognition
      recognition.start();
      return recognition;

    } catch (err) {
      setError('Failed to initialize speech recognition');
      setIsListening(false);
      return null;
    }
  }, [language]);

  const stopListening = useCallback((recognition: any) => {
    if (recognition) {
      recognition.stop();
    }
  }, []);

  const abortListening = useCallback((recognition: any) => {
    if (recognition) {
      recognition.abort();
    }
  }, []);

  const clearTranscript = useCallback(() => {
    setTranscript('');
    setError(null);
  }, []);

  return {
    isListening,
    transcript,
    error,
    startListening,
    stopListening,
    abortListening,
    clearTranscript
  };
}