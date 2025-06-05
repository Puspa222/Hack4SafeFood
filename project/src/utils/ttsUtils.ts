import { Language } from '../types';

/**
 * Utility functions for Text-to-Speech functionality
 */

/**
 * Get the best available voice for the given language
 */
export function getBestVoice(language: Language): SpeechSynthesisVoice | null {
  if (!('speechSynthesis' in window)) return null;
  
  const voices = window.speechSynthesis.getVoices();
  
  if (language === 'ne') {
    // Look for Nepali voice first
    let voice = voices.find(v => 
      v.lang.includes('ne') || 
      v.name.toLowerCase().includes('nepali')
    );
    
    // Fallback to Hindi if no Nepali voice
    if (!voice) {
      voice = voices.find(v => 
        v.lang.includes('hi') || 
        v.name.toLowerCase().includes('hindi')
      );
    }
    
    // Further fallback to any Indian language
    if (!voice) {
      voice = voices.find(v => 
        v.lang.includes('hi-IN') || 
        v.lang.includes('en-IN')
      );
    }
    
    return voice || null;
  } else {
    // For English, prefer local/high-quality voices
    let voice = voices.find(v => 
      v.lang.includes('en') && v.localService
    );
    
    if (!voice) {
      voice = voices.find(v => v.lang.includes('en'));
    }
    
    return voice || null;
  }
}

/**
 * Get optimal TTS settings for the given language
 */
export function getOptimalTTSSettings(language: Language) {
  return {
    rate: language === 'ne' ? 1.0 : 1.0, // Slower for Nepali
    pitch: 1.0,
    volume: 1.0
  };
}

/**
 * Clean text for better TTS pronunciation
 */
export function cleanTextForTTS(text: string, language: Language): string {
  // Remove markdown formatting
  let cleaned = text
    .replace(/\*\*(.*?)\*\*/g, '$1') // Bold
    .replace(/\*(.*?)\*/g, '$1') // Italic
    .replace(/`(.*?)`/g, '$1') // Code
    .replace(/\[(.*?)\]\(.*?\)/g, '$1') // Links
    .replace(/#+\s/g, '') // Headers
    .replace(/>\s/g, '') // Blockquotes
    .replace(/\n+/g, ' ') // Multiple newlines
    .replace(/\s+/g, ' ') // Multiple spaces
    .trim();
  
  // Language-specific cleaning
  if (language === 'ne') {
    // Add pauses for better Nepali pronunciation
    cleaned = cleaned
      .replace(/([।])/g, '$1. ') // Add pause after Devanagari full stop
      .replace(/([,])/g, '$1 ') // Add pause after commas
      .replace(/(\d+)/g, (match) => {
        // Spell out numbers with spaces between digits for better pronunciation
        return match.split('').join(' ');
      });
      
    // Add slight pauses for better phrase separation in Nepali
    cleaned = cleaned
      .replace(/([^\s।,]+\s[^\s।,]+\s[^\s।,]+\s[^\s।,]+)/g, '$1, ')
      .replace(/\s,\s,\s/g, ', '); // Clean up double commas
  }
  
  return cleaned;
}

/**
 * Check if TTS is supported and voices are available
 */
export function checkTTSSupport(): {
  isSupported: boolean;
  hasVoices: boolean;
  nepaliSupported: boolean;
} {
  const isSupported = 'speechSynthesis' in window;
  
  if (!isSupported) {
    return { isSupported: false, hasVoices: false, nepaliSupported: false };
  }
  
  const voices = window.speechSynthesis.getVoices();
  const hasVoices = voices.length > 0;
  const nepaliSupported = voices.some(v => 
    v.lang.includes('ne') || 
    v.lang.includes('hi') ||
    v.name.toLowerCase().includes('nepali') ||
    v.name.toLowerCase().includes('hindi')
  );
  
  return { isSupported, hasVoices, nepaliSupported };
}
