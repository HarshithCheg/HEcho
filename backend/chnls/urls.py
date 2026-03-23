from django.urls import path, include
from .views import ChannelListCreateView, ChannelDelView

urlpatterns = [
    path('', ChannelListCreateView.as_view()),
    path('channel/<uuid:channel_uid>/', ChannelDelView.as_view()),
]
