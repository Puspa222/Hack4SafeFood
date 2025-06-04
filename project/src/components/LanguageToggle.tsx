import React from 'react';
import { Languages } from 'lucide-react';
import { useLanguage } from '../contexts/LanguageContext';
import { Language } from '../types';

export function LanguageToggle() {
  const { language, setLanguage } = useLanguage();

  const toggleLanguage = () => {
    setLanguage(language === 'en' ? 'ne' : 'en');
  };

  return (
    <button
      onClick={toggleLanguage}
      className="flex items-center gap-2 px-3 py-2 rounded-lg bg-white shadow-sm hover:bg-gray-50 text-sm sm:text-base"
    >
      <Languages size={18} className="sm:size-5 text-[#2E7D32]" />
      <span className="font-medium">
        {language === 'en' ? '🇳🇵 नेपाली' : '🇬🇧 English'}
      </span>
    </button>
  );
}