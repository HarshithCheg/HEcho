from django.shortcuts import render
from rest_framework.generics import ListCreateAPIView, DestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied, NotFound
from servers.models import Server, ServerMember
from .models import Channel
from .serializers import ChannelSerializer

# Create your views here.
class ChannelListCreateView(ListCreateAPIView):
    permission_classes= [IsAuthenticated]
    serializer_class= ChannelSerializer

    def get_server(self):
        try:
            s_uid= self.kwargs['server_uid']
            return Server.objects.get(uid= s_uid)
        except Server.DoesNotExist:
            raise NotFound("Server Not Found")
        

    def is_admin(self, server):
        return ServerMember.objects.filter(user= self.request.user, server= server, role__in= ['ADMIN', 'OWNER']).exists()
    
    def is_member(self, server):
        return ServerMember.objects.filter(user= self.request.user, server= server).exists()

    def get_queryset(self):
        server = self.get_server()
        if server.is_public or self.is_member(server):
            return Channel.objects.filter(server= server)
        raise PermissionDenied("Access Denied")
    
    def perform_create(self, serializer):
        server = self.get_server()
        if self.is_admin(server):
            serializer.save(server=server)
        else:
            raise PermissionDenied("Account does not have Required Permission.")

class ChannelDelView(DestroyAPIView):
    permission_classes= [IsAuthenticated]
    serializer_class= ChannelSerializer
    lookup_field= 'uid'
    lookup_url_kwarg= 'channel_uid'

    def get_server(self):
        try:
            s_uid= self.kwargs['server_uid']
            return Server.objects.get(uid= s_uid)
        except Server.DoesNotExist:
            raise NotFound("Server Not Found")
        

    def is_admin(self, server):
        return ServerMember.objects.filter(user= self.request.user, server= server, role__in= ['ADMIN', 'OWNER']).exists()
    
    def get_queryset(self):
        server = self.get_server()
        if self.is_admin(server):
            return Channel.objects.filter(server= server)
        return Channel.objects.none()
        
    def perform_destroy(self, instance):
        server = self.get_server()
        if self.is_admin(server):
            #delete
            instance.delete()
        raise PermissionDenied("Account does not have Required Permissions")