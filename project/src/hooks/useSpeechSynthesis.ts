import { useCallback, useState } from 'react';
import { useLanguage } from '../contexts/LanguageContext';

export function useSpeechSynthesis() {
  const { language } = useLanguage();
  const [isSpeaking, setIsSpeaking] = useState(false);
  const [isPaused, setIsPaused] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const speak = useCallback((
    text: string,
    options?: {
      voice?: SpeechSynthesisVoice;
      rate?: number;
      pitch?: number;
      volume?: number;
    }
  ) => {
    if (!('speechSynthesis' in window)) {
      setError('Speech synthesis not supported in this browser');
      return;
    }

    window.speechSynthesis.cancel();

    try {
      const utterance = new SpeechSynthesisUtterance(text);
      
      utterance.lang = language === 'ne' ? 'ne-NP' : 'en-US';
      utterance.rate = options?.rate ?? 1.0; 
      utterance.pitch = options?.pitch ?? 1.0; 
      utterance.volume = options?.volume ?? 1.0; 
      
      if (options?.voice) {
        utterance.voice = options.voice;
      }

      utterance.onstart = () => {
        setIsSpeaking(true);
        setIsPaused(false);
        setError(null);
      };

      utterance.onend = () => {
        setIsSpeaking(false);
        setIsPaused(false);
      };

      utterance.onerror = (event) => {
        setIsSpeaking(false);
        setIsPaused(false);
        
        switch (event.error) {
          case 'canceled':
            setError('Speech was canceled');
            break;
          case 'interrupted':
            setError('Speech was interrupted');
            break;
          case 'audio-busy':
            setError('Audio output device is busy');
            break;
          case 'audio-hardware':
            setError('Audio hardware error');
            break;
          case 'network':
            setError('Network error during synthesis');
            break;
          case 'synthesis-unavailable':
            setError('Speech synthesis not available');
            break;
          case 'synthesis-failed':
            setError('Speech synthesis failed');
            break;
          case 'language-unavailable':
            setError('Language not available for synthesis');
            break;
          case 'voice-unavailable':
            setError('Voice not available');
            break;
          case 'text-too-long':
            setError('Text is too long to synthesize');
            break;
          case 'invalid-argument':
            setError('Invalid synthesis parameters');
            break;
          case 'not-allowed':
            setError('Speech synthesis not allowed');
            break;
          default:
            setError('Speech synthesis error occurred');
        }
      };

      utterance.onpause = () => {
        setIsPaused(true);
      };

      utterance.onresume = () => {
        setIsPaused(false);
      };

      utterance.onmark = (event) => {
        console.log('Mark reached:', event.name);
      };

      utterance.onboundary = (event) => {
        console.log('Boundary reached:', event.name, 'at character', event.charIndex);
      };

      window.speechSynthesis.speak(utterance);

    } catch (err) {
      setError('Failed to initialize speech synthesis');
      setIsSpeaking(false);
      setIsPaused(false);
    }
  }, [language]);

  const pause = useCallback(() => {
    if (window.speechSynthesis && isSpeaking) {
      window.speechSynthesis.pause();
    }
  }, [isSpeaking]);

  const resume = useCallback(() => {
    if (window.speechSynthesis && isPaused) {
      window.speechSynthesis.resume();
    }
  }, [isPaused]);

  const cancel = useCallback(() => {
    if (window.speechSynthesis) {
      window.speechSynthesis.cancel();
      setIsSpeaking(false);
      setIsPaused(false);
    }
  }, []);

  const getVoices = useCallback(() => {
    if (window.speechSynthesis) {
      return window.speechSynthesis.getVoices();
    }
    return [];
  }, []);

  return {
    speak,
    pause,
    resume,
    cancel,
    getVoices,
    isSpeaking,
    isPaused,
    error,
    isSupported: 'speechSynthesis' in window
  };
}