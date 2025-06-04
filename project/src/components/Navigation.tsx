import React from 'react';
import { Home, Lightbulb, HelpCircle, ClipboardList } from 'lucide-react';
import { useLanguage } from '../contexts/LanguageContext';
import { translations } from '../utils/translations';
import clsx from 'clsx';

interface NavigationProps {
  currentView: 'chat' | 'tips' | 'faq' | 'report';
  onViewChange: (view: 'chat' | 'tips' | 'faq' | 'report') => void;
}

export function Navigation({ currentView, onViewChange }: NavigationProps) {
  const { language } = useLanguage();

  const navItems = [
    { id: 'chat', icon: Home, label: translations.home },
    { id: 'tips', icon: Lightbulb, label: translations.tips },
    { id: 'faq', icon: HelpCircle, label: translations.faq },
    { id: 'report', icon: ClipboardList, label: translations.report }
  ] as const;

  return (
    <nav className="bg-white shadow-sm sticky top-0 z-10">
      <div className="max-w-3xl mx-auto px-2 sm:px-4">
        <div className="flex justify-between sm:justify-center gap-1 sm:gap-8 py-2 sm:py-3 overflow-x-auto">
          {navItems.map(({ id, icon: Icon, label }) => (
            <button 
              key={id}
              onClick={() => onViewChange(id)}
              className={clsx(
                'flex items-center gap-1 sm:gap-2 px-2 sm:px-4 py-2 rounded-lg transition-colors whitespace-nowrap min-w-fit',
                currentView === id 
                  ? 'bg-[#E8F5E9] text-[#1B5E20]' 
                  : 'text-[#2E7D32] hover:bg-[#F4FAF2]'
              )}
            >
              <Icon size={20} className="sm:size-6" />
              <span className="text-sm sm:text-base font-medium">{label[language]}</span>
            </button>
          ))}
        </div>
      </div>
    </nav>
  );
}