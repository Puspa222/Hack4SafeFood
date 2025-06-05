import React from 'react';
import { MarkdownRenderer } from './MarkdownRenderer';

interface MarkdownViewerProps {
  content: string;
  title?: string;
  className?: string;
}

export function MarkdownViewer({ content, title, className }: MarkdownViewerProps) {
  return (
    <div className={`bg-white rounded-lg shadow-sm border border-[#E8F5E9] p-6 ${className || ''}`}>
      {title && (
        <h2 className="text-2xl font-bold text-[#2E7D32] mb-6 pb-3 border-b-2 border-[#E8F5E9]">
          {title}
        </h2>
      )}
      <MarkdownRenderer content={content} />
    </div>
  );
}
