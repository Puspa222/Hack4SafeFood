from rest_framework import serializers
from .models import Chat, Message


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['message_id', 'message', 'role', 'chat', 'created_at', 'updated_at']
        read_only_fields = ['message_id', 'created_at', 'updated_at']


class ChatSerializer(serializers.ModelSerializer):
    messages = MessageSerializer(many=True, read_only=True)
    
    class Meta:
        model = Chat
        fields = ['chat_id', 'created_at', 'updated_at', 'messages']
        read_only_fields = ['chat_id', 'created_at', 'updated_at']


class CreateMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['message', 'role', 'chat']
        
    def create(self, validated_data):
        return Message.objects.create(**validated_data)
