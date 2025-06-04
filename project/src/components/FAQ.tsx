import React from 'react';
import { useLanguage } from '../contexts/LanguageContext';
import { HelpCircle } from 'lucide-react';

export function FAQ() {
  const { language } = useLanguage();

  const faqs = {
    en: [
      {
        question: "How can Farm AI help me?",
        answer: "Farm AI provides personalized farming advice, weather updates, and crop management tips in your preferred language."
      },
      {
        question: "Can I use voice commands?",
        answer: "Yes! Click the microphone button to ask questions using your voice in either Nepali or English."
      },
      {
        question: "How accurate is the advice?",
        answer: "Our AI is trained on verified agricultural data and local farming practices to provide reliable, region-specific advice."
      }
    ],
    ne: [
      {
        question: "फार्म एआई ले मलाई कसरी मद्दत गर्न सक्छ?",
        answer: "फार्म एआई ले तपाईंको रोजाइको भाषामा व्यक्तिगत कृषि सल्लाह, मौसम अपडेट, र बाली व्यवस्थापन सुझावहरू प्रदान गर्दछ।"
      },
      {
        question: "के म भ्वाइस कमाण्ड प्रयोग गर्न सक्छु?",
        answer: "हो! नेपाली वा अंग्रेजी भाषामा आफ्नो आवाजमा प्रश्नहरू सोध्न माइक्रोफोन बटन क्लिक गर्नुहोस्।"
      },
      {
        question: "सल्लाह कति सटीक छ?",
        answer: "हाम्रो एआई विश्वसनीय, क्षेत्र-विशिष्ट सल्लाह प्रदान गर्न प्रमाणित कृषि डाटा र स्थानीय कृषि अभ्यासहरूमा प्रशिक्षित छ।"
      }
    ]
  };

  return (
    <div className="space-y-6">
      {faqs[language].map((faq, index) => (
        <div key={index} className="bg-white rounded-lg shadow-lg p-6 hover:shadow-xl transition-shadow">
          <div className="flex items-center space-x-3 mb-4">
            <div className="bg-[#E8F5E9] p-3 rounded-full">
              <HelpCircle size={24} className="text-[#2E7D32]" />
            </div>
            <h2 className="text-xl font-bold text-[#2E7D32]">{faq.question}</h2>
          </div>
          <p className="text-gray-700 text-lg leading-relaxed">{faq.answer}</p>
        </div>
      ))}
    </div>
  );
}