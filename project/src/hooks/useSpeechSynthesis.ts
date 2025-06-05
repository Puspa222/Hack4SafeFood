import { useCallback, useState } from 'react';
import { useLanguage } from '../contexts/LanguageContext';
import { getBestVoice, getOptimalTTSSettings, cleanTextForTTS, checkTTSSupport } from '../utils/ttsUtils';

export function useSpeechSynthesis() {
  const { language } = useLanguage();
  const [isSpeaking, setIsSpeaking] = useState(false);
  const [isPaused, setIsPaused] = useState(false);
  const [error, setError] = useState<string | null>(null);  const speak = useCallback((
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

    // Cancel any ongoing speech
    window.speechSynthesis.cancel();

    try {
      // Clean and optimize text for better pronunciation
      const cleanedText = cleanTextForTTS(text, language);
      const utterance = new SpeechSynthesisUtterance(cleanedText);
      
      // Set language based on context
      utterance.lang = language === 'ne' ? 'ne-NP' : 'en-US';
      
      // Get optimal settings for the current language
      const optimalSettings = getOptimalTTSSettings(language);
      utterance.rate = options?.rate ?? optimalSettings.rate; 
      utterance.pitch = options?.pitch ?? optimalSettings.pitch; 
      utterance.volume = options?.volume ?? optimalSettings.volume;
      
      // Try to find the best voice for the language
      if (!options?.voice) {
        // Use the utility function to get the best voice
        const bestVoice = getBestVoice(language);
        if (bestVoice) {
          utterance.voice = bestVoice;
        }
      } else {
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
    if (!('speechSynthesis' in window)) {
      return [];
    }
    
    const voices = window.speechSynthesis.getVoices();
    
    // Filter and sort voices by relevance to the current language
    if (language === 'ne') {
      // For Nepali, prioritize voices in this order:
      // 1. Nepali voices
      // 2. Hindi voices
      // 3. Other Indian voices
      // 4. All other voices
      return [
        ...voices.filter(v => v.lang.includes('ne') || v.name.toLowerCase().includes('nepali')),
        ...voices.filter(v => v.lang.includes('hi') || v.name.toLowerCase().includes('hindi')),
        ...voices.filter(v => v.lang.includes('hi-IN') || v.lang.includes('en-IN')),
        ...voices.filter(v => !v.lang.includes('ne') && !v.lang.includes('hi') && !v.lang.includes('hi-IN') && !v.lang.includes('en-IN'))
      ];
    } else {
      // For English, prioritize English voices
      return [
        ...voices.filter(v => v.lang.includes('en') && v.localService),
        ...voices.filter(v => v.lang.includes('en') && !v.localService),
        ...voices.filter(v => !v.lang.includes('en'))
      ];
    }
  }, [language]);
  const { isSupported, hasVoices, nepaliSupported } = checkTTSSupport();

  return {
    speak,
    pause,
    resume,
    cancel,
    getVoices,
    isSpeaking,
    isPaused,
    error,
    isSupported,
    hasVoices,
    nepaliSupported
  };
}