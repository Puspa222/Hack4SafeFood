from django.contrib import admin

# Register your models here.

from .models import FeedPost, ChatMessage

admin.site.register(FeedPost)
admin.site.register(ChatMessage)
# superadmin
