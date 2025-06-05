from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Chat, Message
from .serializers import ChatSerializer, MessageSerializer, CreateMessageSerializer


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
    """Send a message to a chat"""
    serializer = CreateMessageSerializer(data=request.data)
    if serializer.is_valid():
        try:
            # Verify chat exists
            chat = Chat.objects.get(chat_id=serializer.validated_data['chat'].chat_id)
            message = serializer.save()
            response_serializer = MessageSerializer(message)
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)
        except Chat.DoesNotExist:
            return Response({'error': 'Chat not found'}, status=status.HTTP_404_NOT_FOUND)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
