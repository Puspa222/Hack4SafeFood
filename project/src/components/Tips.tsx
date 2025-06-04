import React from 'react';
import { useLanguage } from '../contexts/LanguageContext';
import { Leaf } from 'lucide-react';

export function Tips() {
  const { language } = useLanguage();

  const tips = {
    en: [
      {
        title: "Seasonal Planting Guide",
        content: "Learn the best times to plant different crops based on Nepal's climate zones."
      },
      {
        title: "Water Conservation",
        content: "Simple techniques to save water while maintaining healthy crops."
      },
      {
        title: "Pest Management",
        content: "Natural ways to protect your crops from common pests."
      }
    ],
    ne: [
      {
        title: "मौसमी रोपाई मार्गदर्शन",
        content: "नेपालको जलवायु क्षेत्रहरूमा आधारित विभिन्न बालीहरू रोप्ने उत्तम समय जान्नुहोस्।"
      },
      {
        title: "पानी संरक्षण",
        content: "स्वस्थ बाली कायम राख्दै पानी बचत गर्ने सरल तरिकाहरू।"
      },
      {
        title: "कीट व्यवस्थापन",
        content: "सामान्य कीराहरूबाट आफ्नो बालीको सुरक्षा गर्ने प्राकृतिक तरिकाहरू।"
      }
    ]
  };

  return (
    <div className="space-y-6">
      {tips[language].map((tip, index) => (
        <div key={index} className="bg-white rounded-lg shadow-lg p-6 hover:shadow-xl transition-shadow">
          <div className="flex items-center space-x-3 mb-4">
            <div className="bg-[#E8F5E9] p-3 rounded-full">
              <Leaf size={24} className="text-[#2E7D32]" />
            </div>
            <h2 className="text-xl font-bold text-[#2E7D32]">{tip.title}</h2>
          </div>
          <p className="text-gray-700 text-lg leading-relaxed">{tip.content}</p>
        </div>
      ))}
    </div>
  );
}