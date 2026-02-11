from django.urls import path
from . import views

urlpatterns = [
    path('chat/<uuid:message_uid>/', views.ChatListCreateView.as_view()),
]
