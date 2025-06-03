import React from "react";

interface FeedCardProps {
  title: string;
  content: string;
  author: string;
}

const FeedCard: React.FC<FeedCardProps> = ({ title, content, author }) => {
  return (
    <div className="bg-[#f3fa9a] p-6 rounded-3xl shadow-xl hover:shadow-2xl transition-all duration-300 border border-[#DDEFA6] transform hover:scale-[1.02]">
      <h2 className="text-2xl font-extrabold text-[#2c3e50] mb-3 leading-snug">
        {title}
      </h2>
      <p className="text-gray-800 leading-relaxed mb-4 text-[15px]">
        {content}
      </p>
      <div className="text-sm text-[#374151] font-medium text-right">
        Author: <span className="italic">{author}</span>
      </div>
    </div>
  );
};

export default FeedCard;
