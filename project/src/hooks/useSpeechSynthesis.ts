import { useCallback } from 'react';
import { useLanguage } from '../contexts/LanguageContext';

export function useSpeechSynthesis() {
  const { language } = useLanguage();

  const speak = useCallback((text: string) => {
    if ('speechSynthesis' in window) {
      const utterance = new SpeechSynthesisUtterance(text);
      utterance.lang = language === 'ne' ? 'ne-NP' : 'en-US';
      window.speechSynthesis.speak(utterance);
    }
  }, [language]);

  return { speak };
}