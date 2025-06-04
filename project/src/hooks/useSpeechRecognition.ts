import { useState, useCallback } from 'react';
import { useLanguage } from '../contexts/LanguageContext';

export function useSpeechRecognition() {
  const [isListening, setIsListening] = useState(false);
  const { language } = useLanguage();

  const startListening = useCallback(() => {
    if ('webkitSpeechRecognition' in window) {
      const recognition = new (window as any).webkitSpeechRecognition();
      recognition.continuous = false;
      recognition.lang = language === 'ne' ? 'ne-NP' : 'en-US';

      recognition.onstart = () => setIsListening(true);
      recognition.onend = () => setIsListening(false);

      recognition.start();
      return recognition;
    }
    return null;
  }, [language]);

  return { isListening, startListening };
}