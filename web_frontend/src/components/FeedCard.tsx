import React from "react";

interface FeedCardProps {
  title: string;
  content: string;
  author: string;
}

const FeedCard: React.FC<FeedCardProps> = ({ title, content, author }) => {
  return (
    <div className="bg-[#fcff9a] p-6 rounded-3xl shadow-lg hover:shadow-2xl transition-all duration-300 border border-[#DDEFA6]">
      <h2 className="text-2xl font-bold text-[#2C2C2C] mb-2">{title}</h2>
      <p className="text-gray-800 leading-relaxed mb-4">{content}</p>
      <div className="text-sm text-gray-600 italic text-right">- {author}</div>
    </div>
  );
};

export default FeedCard;
