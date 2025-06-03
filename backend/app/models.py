from django.db import models

# Create your models he
# making a model for feedposts
class FeedPost(models.Model):
    post_id=models.CharField(max_length=100, primary_key=True)
    post_title=models.CharField(max_length=200)
    post_content=models.TextField()
    author_name=models.CharField(max_length=100)


    def __str__(self):
        return f"{self.post_title} by {self.author_name}"
# making model for chat mesaages 
class ChatMessage(models.Model):
    message_id = models.CharField(max_length=100, primary_key=True)
    messaes=models.TextField()
    chat_id=models.CharField(max_length=100)
    role_choices=[('human','Human'),('ai','AI')]
    role=models.CharField(max_length=10, choices=role_choices)

    def __str__(self):
        return f"{self.chat_id} - {self.role}: {self.messaes[:50]}..."