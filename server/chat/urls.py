from django.urls import path
from . import views

urlpatterns = [
    path('chat/create/', views.create_chat, name='create_chat'),
    path('chat/<str:chat_id>/messages/', views.get_chat_messages, name='get_chat_messages'),
    path('message/send/', views.send_message, name='send_message'),
    path('documents/search/', views.search_documents, name='search_documents'),
    path('documents/test-search/', views.test_search, name='test_search'),
    path('vectorstore/initialize/', views.initialize_vectorstore, name='initialize_vectorstore'),
    path('vectorstore/status/', views.vectorstore_status, name='vectorstore_status'),
]
