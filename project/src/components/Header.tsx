import React from 'react';
import { Sprout } from 'lucide-react';
import { useLanguage } from '../contexts/LanguageContext';
import { translations } from '../utils/translations';

export function Header() {
  const { language } = useLanguage();

  return (
    <header className="bg-[#2E7D32] text-white py-3 sm:py-4 px-4 sm:px-6 shadow-lg">
      <div className="flex items-center justify-between max-w-4xl mx-auto">
        <div className="flex items-center gap-2 sm:gap-3">
          <Sprout size={28} className="sm:size-8 text-[#FF9800]" />
          <div>
            <h1 className="text-xl sm:text-2xl font-bold">
              {translations.welcome[language]}
            </h1>
            <p className="text-xs sm:text-sm opacity-90">
              {translations.subtitle[language]}
            </p>
          </div>
        </div>
      </div>
    </header>
  );
}