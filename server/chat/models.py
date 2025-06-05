from django.db import models
import uuid


class Chat(models.Model):
    chat_id = models.CharField(max_length=255, primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Chat {self.chat_id}"

    class Meta:
        ordering = ['-created_at']


class Message(models.Model):
    message_id = models.CharField(max_length=255, primary_key=True, default=uuid.uuid4, editable=False)
    message = models.TextField()
    role = models.CharField(max_length=50)
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name='messages')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Message {self.message_id} - {self.role}"

    class Meta:
        ordering = ['created_at']
