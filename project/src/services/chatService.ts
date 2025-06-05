// Chat API service for connecting to Django backend
const API_BASE_URL = 'http://127.0.0.1:8000/api';

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
  }
}

export const chatService = new ChatService();
