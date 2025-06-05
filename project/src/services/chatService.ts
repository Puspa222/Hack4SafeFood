// Chat API service for connecting to Django backend
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:8000/api';
const CHAT_STORAGE_KEY = import.meta.env.VITE_CHAT_STORAGE_KEY || 'hack4safefood_chat_id';

export interface ChatResponse {
  chat_id: string;
  created_at: string;
  updated_at: string;
  messages: any[];
}

export interface MessageResponse {
  user_message: {
    message_id: string;
    message: string;
    role: string;
    chat: string;
    created_at: string;
    updated_at: string;
  };
  ai_response: {
    message_id: string;
    message: string;
    role: string;
    chat: string;
    created_at: string;
    updated_at: string;
  };
}

export interface ApiMessage {
  message_id: string;
  message: string;
  role: string;
  chat: string;
  created_at: string;
  updated_at: string;
}

class ChatService {
  private chatId: string | null = null;

  constructor() {
    // Load existing chat ID from localStorage on initialization
    this.loadChatFromStorage();
  }

  private loadChatFromStorage(): void {
    try {
      const storedChatId = localStorage.getItem(CHAT_STORAGE_KEY);
      if (storedChatId) {
        this.chatId = storedChatId;
      }
    } catch (error) {
      console.warn('Failed to load chat ID from storage:', error);
    }
  }

  private saveChatToStorage(chatId: string): void {
    try {
      localStorage.setItem(CHAT_STORAGE_KEY, chatId);
    } catch (error) {
      console.warn('Failed to save chat ID to storage:', error);
    }
  }

  private clearChatFromStorage(): void {
    try {
      localStorage.removeItem(CHAT_STORAGE_KEY);
    } catch (error) {
      console.warn('Failed to clear chat ID from storage:', error);
    }
  }

  async createChat(): Promise<string> {
    try {
      const response = await fetch(`${API_BASE_URL}/chat/create/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data: ChatResponse = await response.json();
      this.chatId = data.chat_id;
      this.saveChatToStorage(data.chat_id);
      return data.chat_id;
    } catch (error) {
      console.error('Error creating chat:', error);
      throw error;
    }
  }

  async sendMessage(message: string): Promise<MessageResponse> {
    if (!this.chatId) {
      await this.createChat();
    }

    try {
      const response = await fetch(`${API_BASE_URL}/message/send/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          message,
          role: 'user',
          chat: this.chatId,
        }),
      });

      if (!response.ok) {
        // If chat not found, create a new one and retry
        if (response.status === 404) {
          this.clearChatFromStorage();
          this.chatId = null;
          await this.createChat();
          
          // Retry with new chat ID
          const retryResponse = await fetch(`${API_BASE_URL}/message/send/`, {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
            },
            body: JSON.stringify({
              message,
              role: 'user',
              chat: this.chatId,
            }),
          });
          
          if (!retryResponse.ok) {
            throw new Error(`HTTP error! status: ${retryResponse.status}`);
          }
          
          const retryData: MessageResponse = await retryResponse.json();
          return retryData;
        }
        
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data: MessageResponse = await response.json();
      return data;
    } catch (error) {
      console.error('Error sending message:', error);
      throw error;
    }
  }

  async getChatMessages(): Promise<ApiMessage[]> {
    if (!this.chatId) {
      return [];
    }

    try {
      const response = await fetch(`${API_BASE_URL}/chat/${this.chatId}/messages/`);

      if (!response.ok) {
        if (response.status === 404) {
          // Chat not found, clear stored ID
          this.clearChatFromStorage();
          this.chatId = null;
          return [];
        }
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data: ApiMessage[] = await response.json();
      return data;
    } catch (error) {
      console.error('Error fetching messages:', error);
      throw error;
    }
  }

  getCurrentChatId(): string | null {
    return this.chatId;
  }

  resetChat(): void {
    this.chatId = null;
    this.clearChatFromStorage();
  }

  // Load existing conversation when app starts
  async loadExistingConversation(): Promise<ApiMessage[]> {
    if (this.chatId) {
      return await this.getChatMessages();
    }
    return [];
  }
}

export const chatService = new ChatService();
