from django.shortcuts import render
from django.http import HttpResponse
from .models import FeedPost, ChatMessage
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt





@csrf_exempt  # Use this decorator if you want to allow POST requests without CSRF token
def FeedPostViewSet(request):
    feed_posts = FeedPost.objects.all()
    response_data = {
        'feed_posts': list(feed_posts.values('post_id', 'post_title', 'post_content', 'author_name'))
    }
    return JsonResponse(response_data)

 

@csrf_exempt  # Use this decorator if you want to allow POST requests without CSRF token

def ChatMessageViewSet(request):
    # This view will handle the chat messages
    chat_messages = ChatMessage.objects.all()
    # return the response as a list of chat messages
    response_data = {
        'chat_messages': list(chat_messages.values('message_id', 'message_content', 'chat_id', 'role'))
    }
    return HttpResponse(response_data)

# Create your views here.
