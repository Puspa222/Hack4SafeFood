from django.urls import path
from . import views

urlpatterns = [
    path('chat/create/', views.create_chat, name='create_chat'),
    path('chat/<str:chat_id>/messages/', views.get_chat_messages, name='get_chat_messages'),
    path('message/send/', views.send_message, name='send_message'),
]
