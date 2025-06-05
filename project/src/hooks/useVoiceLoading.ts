import { useEffect, useState } from 'react';

/**
 * Utility hook to ensure voices are loaded properly for speech synthesis
 * This is important since voices might not be available immediately when the page loads
 */
export function useVoiceLoading() {
  const [voicesLoaded, setVoicesLoaded] = useState(false);
  const [voices, setVoices] = useState<SpeechSynthesisVoice[]>([]);
  
  useEffect(() => {
    // Check if SpeechSynthesis is supported
    if (!('speechSynthesis' in window)) {
      return;
    }
    
    // Get voices that might already be loaded
    const loadedVoices = window.speechSynthesis.getVoices();
    if (loadedVoices.length > 0) {
      setVoices(loadedVoices);
      setVoicesLoaded(true);
    }
    
    // Set up event handler for when voices are loaded
    const handleVoicesChanged = () => {
      const updatedVoices = window.speechSynthesis.getVoices();
      setVoices(updatedVoices);
      setVoicesLoaded(true);
    };
    
    // Add event listener
    window.speechSynthesis.onvoiceschanged = handleVoicesChanged;
    
    // Clean up
    return () => {
      window.speechSynthesis.onvoiceschanged = null;
    };
  }, []);
  
  return { 
    voicesLoaded, 
    voices,
    isSupported: 'speechSynthesis' in window
  };
}
