from django.shortcuts import render
from rest_framework.generics import ListCreateAPIView, CreateAPIView, ListAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.db.models import Q
from .models import Server, ServerMember, ServerInvite
from .serializers import ServerSerializer

# Create your views here.
class CreateServerView(ListCreateAPIView):
    permission_classes= [IsAuthenticated]
    serializer_class= ServerSerializer

    def get_queryset(self):
        return Server.objects.filter(owner= self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(owner= self.request.user)

class JoinPubServerView(APIView):
    """Join Public Server a little more frontend and search option to add. 
    For discord-like feel."""
    permission_classes= [IsAuthenticated]

    def post(self, request, uid):
        try:
            server = Server.objects.get(uid=uid, is_public= True)
        except Server.DoesNotExist:
            return Response({"error": "Server Not Found or is Private"}, status=status.HTTP_404_NOT_FOUND)
        
        if ServerMember.objects.filter(user=request.user, server=server).exists():
            return Response({"error":"Already a member"}, status=status.HTTP_400_BAD_REQUEST)
        
        ServerMember.objects.create(user= request.user, server= server)
        return Response({"message":"Joined the server"}, status=status.HTTP_201_CREATED)
    
class JoinServerInviteView(APIView):
    """This for joining via the Permanent Invite Link, created during creation of server."""
    permission_classes= [IsAuthenticated]

    def post(self, request, code):
        try:
            invite = ServerInvite.objects.get(code= code)
        except ServerInvite.DoesNotExist:
            return Response({"error":"Invalid Invite Link"}, status=status.HTTP_404_NOT_FOUND)
        
        server = invite.server
        if ServerMember.objects.filter(user= request.user, server= server).exists():
            return Response({"error":"Already a member"}, status=status.HTTP_400_BAD_REQUEST)
        
        ServerMember.objects.create(user= request.user, server= server)
        return Response({"message":"Joined the Server"}, status=status.HTTP_201_CREATED)
    
class SearchPubServerView(ListAPIView):
    """Responsible for Searching the Public Servers. 
    Though you must click join to join them{frontend}."""
    permission_classes= [IsAuthenticated]
    serializer_class= ServerSerializer

    def get_queryset(self):
        query= self.request.query_params.get("q", "")
        joined= ServerMember.objects.filter(user= self.request.user).values_list("server_id", flat=True)

        return Server.objects.filter(is_public= True).filter(Q(name__icontains= query)|Q(about__icontains= query)).exclude(id__in= joined)
    

