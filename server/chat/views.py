from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Chat, Message
from .serializers import ChatSerializer, MessageSerializer, CreateMessageSerializer
from .services import chat_service


@api_view(['POST'])
def create_chat(request):
    """Create a new chat"""
    chat = Chat.objects.create()
    serializer = ChatSerializer(chat)
    return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['GET'])
def get_chat_messages(request, chat_id):
    """Get all messages from a specific chat"""
    try:
        chat = Chat.objects.get(chat_id=chat_id)
        messages = chat.messages.all()
        serializer = MessageSerializer(messages, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Chat.DoesNotExist:
        return Response({'error': 'Chat not found'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
def send_message(request):
    """Send a message to a chat and get AI response"""
    serializer = CreateMessageSerializer(data=request.data)
    if serializer.is_valid():
        try:
            # Verify chat exists
            chat = Chat.objects.get(chat_id=serializer.validated_data['chat'].chat_id)
            
            # Save user message
            user_message = serializer.save()
            
            # Get chat history for context
            chat_history = []
            previous_messages = chat.messages.filter(
                created_at__lt=user_message.created_at
            ).order_by('created_at')
            
            for msg in previous_messages:
                chat_history.append({
                    'role': msg.role,
                    'message': msg.message
                })
            
            # Process message with Langchain
            ai_response = chat_service.get_chat_response(
                message=user_message.message,
                chat_history=chat_history
            )
            
            # Save AI response
            ai_message = Message.objects.create(
                message=ai_response,
                role='assistant',
                chat=chat
            )
            
            # Return both messages
            user_serializer = MessageSerializer(user_message)
            ai_serializer = MessageSerializer(ai_message)
            
            return Response({
                'user_message': user_serializer.data,
                'ai_response': ai_serializer.data
            }, status=status.HTTP_201_CREATED)
            
        except Chat.DoesNotExist:
            return Response({'error': 'Chat not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': f'Failed to process message: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
