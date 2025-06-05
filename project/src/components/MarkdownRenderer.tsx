import React from 'react';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import rehypeRaw from 'rehype-raw';
import rehypeHighlight from 'rehype-highlight';
import { Copy, ExternalLink, Info, AlertTriangle, CheckCircle, XCircle } from 'lucide-react';
import clsx from 'clsx';
import 'highlight.js/styles/github-dark.css';

interface MarkdownRendererProps {
  content: string;
  className?: string;
}

export function MarkdownRenderer({ content, className }: MarkdownRendererProps) {
  const copyToClipboard = (text: string) => {
    navigator.clipboard.writeText(text);
  };

  return (
    <div className={clsx('prose prose-lg max-w-none', className)}>
      <ReactMarkdown
        remarkPlugins={[remarkGfm]}
        rehypePlugins={[rehypeRaw, rehypeHighlight]}
        components={{
          // Headings with enhanced styling
          h1: ({ node, ...props }) => (
            <h1 
              className="text-3xl font-bold text-[#2E7D32] mb-6 mt-8 pb-3 border-b-2 border-[#E8F5E9]" 
              {...props} 
            />
          ),
          h2: ({ node, ...props }) => (
            <h2 
              className="text-2xl font-semibold text-[#2E7D32] mb-4 mt-6 pb-2 border-b border-[#E8F5E9]" 
              {...props} 
            />
          ),
          h3: ({ node, ...props }) => (
            <h3 
              className="text-xl font-medium text-[#2E7D32] mb-3 mt-5" 
              {...props} 
            />
          ),
          h4: ({ node, ...props }) => (
            <h4 
              className="text-lg font-medium text-[#2E7D32] mb-2 mt-4" 
              {...props} 
            />
          ),

          // Enhanced paragraphs
          p: ({ node, ...props }) => (
            <p 
              className="text-gray-700 leading-relaxed mb-4 text-base" 
              {...props} 
            />
          ),

          // Styled links with external link indicator
          a: ({ node, href, children, ...props }) => (
            <a
              className="text-[#2E7D32] hover:text-[#1B5E20] underline decoration-2 underline-offset-2 hover:decoration-[#FF9800] transition-colors duration-200 inline-flex items-center gap-1"
              href={href}
              target={href?.startsWith('http') ? '_blank' : undefined}
              rel={href?.startsWith('http') ? 'noopener noreferrer' : undefined}
              {...props}
            >
              {children}
              {href?.startsWith('http') && (
                <ExternalLink size={14} className="text-[#FF9800]" />
              )}
            </a>
          ),

          // Enhanced lists
          ul: ({ node, ...props }) => (
            <ul 
              className="list-none space-y-2 mb-4 ml-6" 
              {...props} 
            />
          ),
          ol: ({ node, ...props }) => (
            <ol 
              className="list-decimal list-inside space-y-2 mb-4 ml-6 marker:text-[#2E7D32] marker:font-semibold" 
              {...props} 
            />
          ),
          li: ({ node, children, ...props }) => (
            <li 
              className="flex items-start gap-2 text-gray-700" 
              {...props}
            >
              <span className="w-2 h-2 bg-[#2E7D32] rounded-full mt-2 flex-shrink-0"></span>
              <span>{children}</span>
            </li>
          ),

          // Enhanced blockquotes with different types
          blockquote: ({ node, children, ...props }) => {
            const content = React.Children.toArray(children).join('');
            let icon = <Info size={20} />;
            let bgColor = 'bg-blue-50';
            let borderColor = 'border-l-blue-500';
            let iconColor = 'text-blue-600';

            if (content.includes('⚠️') || content.includes('warning')) {
              icon = <AlertTriangle size={20} />;
              bgColor = 'bg-yellow-50';
              borderColor = 'border-l-yellow-500';
              iconColor = 'text-yellow-600';
            } else if (content.includes('✅') || content.includes('success')) {
              icon = <CheckCircle size={20} />;
              bgColor = 'bg-green-50';
              borderColor = 'border-l-green-500';
              iconColor = 'text-green-600';
            } else if (content.includes('❌') || content.includes('error')) {
              icon = <XCircle size={20} />;
              bgColor = 'bg-red-50';
              borderColor = 'border-l-red-500';
              iconColor = 'text-red-600';
            }

            return (
              <blockquote
                className={clsx(
                  'border-l-4 p-4 my-4 rounded-r-lg',
                  bgColor,
                  borderColor
                )}
                {...props}
              >
                <div className="flex items-start gap-3">
                  <div className={iconColor}>
                    {icon}
                  </div>
                  <div className="flex-1 text-gray-700">
                    {children}
                  </div>
                </div>
              </blockquote>
            );
          },

          // Enhanced code blocks with copy functionality
          code: ({
            inline,
            className,
            children,
            ...props
          }: {
            inline?: boolean;
            className?: string;
            children?: React.ReactNode;
          }) => {
            const codeString = React.Children.toArray(children).join('');
            
            if (inline) {
              return (
                <code
                  className="bg-[#E8F5E9] text-[#1B5E20] px-2 py-1 rounded text-sm font-mono border border-[#C8E6C9]"
                  {...props}
                >
                  {children}
                </code>
              );
            }

            return (
              <div className="relative group my-4">
                <button
                  onClick={() => copyToClipboard(codeString)}
                  className="absolute top-3 right-3 p-2 bg-gray-700 hover:bg-gray-600 text-white rounded opacity-0 group-hover:opacity-100 transition-opacity duration-200 z-10"
                  title="Copy code"
                >
                  <Copy size={16} />
                </button>
                <pre
                  className="bg-gray-900 text-white p-4 rounded-lg overflow-x-auto border border-gray-700"
                  {...props}
                >
                  <code className={className}>{children}</code>
                </pre>
              </div>
            );
          },

          // Enhanced tables
          table: ({ node, ...props }) => (
            <div className="overflow-x-auto my-6 rounded-lg border border-[#E8F5E9] shadow-sm">
              <table
                className="w-full border-collapse"
                {...props}
              />
            </div>
          ),
          thead: ({ node, ...props }) => (
            <thead className="bg-[#2E7D32] text-white" {...props} />
          ),
          tbody: ({ node, ...props }) => (
            <tbody className="bg-white" {...props} />
          ),
          tr: ({ node, ...props }) => (
            <tr className="border-b border-[#E8F5E9] hover:bg-[#F4FAF2] transition-colors" {...props} />
          ),
          th: ({ node, ...props }) => (
            <th className="text-left p-4 font-semibold text-white" {...props} />
          ),
          td: ({ node, ...props }) => (
            <td className="p-4 text-gray-700" {...props} />
          ),

          // Enhanced horizontal rule
          hr: ({ node, ...props }) => (
            <hr 
              className="my-8 border-0 h-px bg-gradient-to-r from-transparent via-[#E8F5E9] to-transparent" 
              {...props} 
            />
          ),

          // Text formatting
          strong: ({ node, ...props }) => (
            <strong className="font-bold text-[#2E7D32]" {...props} />
          ),
          em: ({ node, ...props }) => (
            <em className="italic text-gray-600" {...props} />
          ),

          // Enhanced images
          img: ({ node, src, alt, ...props }) => (
            <div className="my-6">
              <img
                className="max-w-full h-auto rounded-lg shadow-md border border-[#E8F5E9] mx-auto"
                src={src}
                alt={alt || 'Image'}
                {...props}
              />
              {alt && (
                <p className="text-center text-sm text-gray-500 mt-2 italic">
                  {alt}
                </p>
              )}
            </div>
          ),

          // Line break
          br: () => <br className="my-2" />,

          // Task lists (GitHub flavored markdown)
          input: ({ node, type, checked, ...props }) => {
            if (type === 'checkbox') {
              return (
                <input
                  type="checkbox"
                  checked={checked}
                  readOnly
                  className="mr-2 accent-[#2E7D32] cursor-default"
                  {...props}
                />
              );
            }
            return <input type={type} {...props} />;
          },
        }}
      >
        {content}
      </ReactMarkdown>
    </div>
  );
}
