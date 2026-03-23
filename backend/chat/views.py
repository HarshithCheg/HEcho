from django.shortcuts import render
from django.db.models import Q
from rest_framework.generics import ListCreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import NotFound, PermissionDenied
from accounts.models import FriendRequest, User
from servers.models import Server
from chnls.models import Channel
from .models import Message
from .serializers import MessageSerializer, DMSerializer

# Create your views here.
class ChatListCreateView(ListCreateAPIView):
    permission_classes= [IsAuthenticated]
    serializer_class= MessageSerializer

    def get_server(self):
        s_uid = self.kwargs["server_uid"]
        try:
            return Server.objects.get(uid = s_uid)
        except Server.DoesNotExist:
            raise NotFound("Server Not Found")
    
    def get_channel(self, server):
        channel_uid = self.kwargs["channel_uid"]
        try:
            return Channel.objects.get(uid= channel_uid, server= server)
        except Channel.DoesNotExist:
            raise NotFound("Channel Not Found")
        
    def is_member(self, server):
        return Server.objects.filter(user= self.request.user, server= server).exists()

    def get_queryset(self):
        server = self.get_server()
        channel = self.get_channel(server)
        if not self.is_member(server):
            raise PermissionDenied("Must be a Member of Server to send message")
        return Message.objects.get(channel= channel)
    
class DMListCreateView(ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = DMSerializer

    def is_friend(self):
        u_uid = self.kwargs["uid"]
        frnd = User.objects.get(uid= u_uid)
        return FriendRequest.objects.filter(status= "ACCEPTED").filter(Q(user1= self.request.user, user2= frnd)|Q(user1= frnd, user1= self.request.user)).exists()


    def get_queryset(self):
        if not self.is_friend():
            raise PermissionDenied("Must be a Friend or User Doesn't Exists")
        return Message.objects.get(sender= self.kwargs["uid"])