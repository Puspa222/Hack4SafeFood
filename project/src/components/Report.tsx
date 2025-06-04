import React, { useState } from 'react';
import { ClipboardList, Send } from 'lucide-react';
import { useLanguage } from '../contexts/LanguageContext';
import { translations } from '../utils/translations';
import { Report as ReportType } from '../types';
import clsx from 'clsx';

export function Report() {
  const { language } = useLanguage();
  const [submitted, setSubmitted] = useState(false);
  const [report, setReport] = useState<Partial<ReportType>>({
    type: 'suggestion',
    content: '',
    contact: ''
  });

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    // Here you would typically send the report to your backend
    console.log('Report submitted:', report);
    setSubmitted(true);
    setTimeout(() => {
      setSubmitted(false);
      setReport({ type: 'suggestion', content: '', contact: '' });
    }, 3000);
  };

  return (
    <div className="max-w-2xl mx-auto">
      <div className="bg-white rounded-lg shadow-lg p-6 mb-6">
        <div className="flex items-center space-x-3 mb-6">
          <div className="bg-[#E8F5E9] p-3 rounded-full">
            <ClipboardList size={24} className="text-[#2E7D32]" />
          </div>
          <h2 className="text-2xl font-bold text-[#2E7D32]">
            {translations.reportTitle[language]}
          </h2>
        </div>

        <form onSubmit={handleSubmit} className="space-y-6">
          <div>
            <label className="block text-gray-700 font-medium mb-2">
              {translations.reportType[language]}
            </label>
            <div className="flex space-x-4">
              {['suggestion', 'issue', 'other'].map((type) => (
                <button
                  key={type}
                  type="button"
                  onClick={() => setReport({ ...report, type })}
                  className={clsx(
                    'px-4 py-2 rounded-lg font-medium transition-colors',
                    report.type === type
                      ? 'bg-[#2E7D32] text-white'
                      : 'bg-[#E8F5E9] text-[#2E7D32] hover:bg-[#C8E6C9]'
                  )}
                >
                  {translations[type][language]}
                </button>
              ))}
            </div>
          </div>

          <div>
            <label className="block text-gray-700 font-medium mb-2">
              {translations.reportContent[language]}
            </label>
            <textarea
              value={report.content}
              onChange={(e) => setReport({ ...report, content: e.target.value })}
              className="w-full p-4 rounded-lg border border-gray-200 focus:border-[#2E7D32] focus:ring-1 focus:ring-[#2E7D32] min-h-[150px]"
              required
            />
          </div>

          <div>
            <label className="block text-gray-700 font-medium mb-2">
              {translations.contact[language]}
            </label>
            <input
              type="text"
              value={report.contact}
              onChange={(e) => setReport({ ...report, contact: e.target.value })}
              className="w-full p-4 rounded-lg border border-gray-200 focus:border-[#2E7D32] focus:ring-1 focus:ring-[#2E7D32]"
            />
          </div>

          <button
            type="submit"
            className={clsx(
              'w-full py-4 rounded-lg font-medium flex items-center justify-center space-x-2 transition-all transform hover:scale-105',
              submitted
                ? 'bg-green-500 text-white'
                : 'bg-[#FF9800] text-white hover:bg-[#FB8C00]'
            )}
          >
            <Send size={20} />
            <span>
              {submitted
                ? translations.success[language]
                : translations.submit[language]}
            </span>
          </button>
        </form>
      </div>
    </div>
  );
}