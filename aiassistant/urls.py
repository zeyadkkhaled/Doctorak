from django.urls import path
from . import views

urlpatterns = [
    path('ai/chatbot/', views.chatbot_handler, name='chatbot'),
    path('chatbot/', views.chatbot_handler, name='chatbot'),
    path('ai/chatbot/', views.chatbot_handler, name='chatbot_handler'),
]
