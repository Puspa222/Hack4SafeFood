from django.contrib import admin
from .models import Chat, Message


@admin.register(Chat)
class ChatAdmin(admin.ModelAdmin):
    list_display = ['chat_id', 'created_at', 'updated_at']
    list_filter = ['created_at', 'updated_at']
    readonly_fields = ['chat_id', 'created_at', 'updated_at']
    search_fields = ['chat_id']


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ['message_id', 'role', 'chat', 'created_at']
    list_filter = ['role', 'created_at', 'chat']
    readonly_fields = ['message_id', 'created_at', 'updated_at']
    search_fields = ['message_id', 'message', 'role']
    raw_id_fields = ['chat']
