# Chat API with Langchain Integration

This Django backend provides a simple chat API that processes messages through Langchain and saves conversations to the database.

## Features

- ✅ CORS enabled for all origins
- ✅ Django REST Framework for API endpoints
- ✅ Chat and Message models with UUID primary keys
- ✅ Langchain integration for AI responses
- ✅ Conversation history context
- ✅ Admin interface for managing chats and messages

## API Endpoints

### 1. Create New Chat
**POST** `/api/chat/create/`

Creates a new chat session.

**Response:**
```json
{
    "chat_id": "uuid-string",
    "created_at": "timestamp",
    "updated_at": "timestamp",
    "messages": []
}
```

### 2. Send Message
**POST** `/api/message/send/`

Sends a message to a chat and gets an AI response.

**Request Body:**
```json
{
    "message": "Your message here",
    "role": "user",
    "chat": "chat-uuid"
}
```

**Response:**
```json
{
    "user_message": {
        "message_id": "uuid",
        "message": "Your message",
        "role": "user",
        "chat": "chat-uuid",
        "created_at": "timestamp",
        "updated_at": "timestamp"
    },
    "ai_response": {
        "message_id": "uuid",
        "message": "AI response",
        "role": "assistant", 
        "chat": "chat-uuid",
        "created_at": "timestamp",
        "updated_at": "timestamp"
    }
}
```

### 3. Get Chat Messages
**GET** `/api/chat/{chat_id}/messages/`

Retrieves all messages from a specific chat.

**Response:**
```json
[
    {
        "message_id": "uuid",
        "message": "Message content",
        "role": "user|assistant",
        "chat": "chat-uuid",
        "created_at": "timestamp",
        "updated_at": "timestamp"
    }
]
```

## Setup

1. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure Environment:**
   Create a `.env` file and add your OpenAI API key:
   ```
   OPENAI_API_KEY=your_openai_api_key_here
   ```

3. **Run Migrations:**
   ```bash
   python manage.py migrate
   ```

4. **Start Server:**
   ```bash
   python manage.py runserver
   ```

5. **Test API:**
   ```bash
   python test_api.py
   ```

## Models

### Chat Model
- `chat_id`: UUID primary key
- `created_at`: Auto timestamp
- `updated_at`: Auto timestamp

### Message Model  
- `message_id`: UUID primary key
- `message`: Text content
- `role`: "user" or "assistant"
- `chat`: Foreign key to Chat
- `created_at`: Auto timestamp
- `updated_at`: Auto timestamp

## Admin Interface

Access the admin interface at `/admin/` to manage chats and messages.

## Langchain Integration

The system uses Langchain to process messages:
- Supports OpenAI GPT models (with API key)
- Falls back to mock responses for development
- Maintains conversation context using chat history
- Customizable system prompts for domain-specific responses

## Development Notes

- CORS is configured to allow all origins for development
- The system automatically saves both user messages and AI responses
- Chat history is included as context for better AI responses
- Error handling with fallback responses
- UUID-based IDs for all records
