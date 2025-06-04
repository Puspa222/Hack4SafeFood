export type Language = 'en' | 'ne';

export interface Message {
  id: string;
  content: string;
  role: 'user' | 'assistant';
  timestamp: Date;
}

export interface Translation {
  [key: string]: {
    en: string;
    ne: string;
  };
}

export interface Report {
  id: string;
  type: 'suggestion' | 'issue' | 'other';
  content: string;
  contact?: string;
  timestamp: Date;
}