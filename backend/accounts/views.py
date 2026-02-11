from django.shortcuts import render
from django.db.models import Q
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView, ListCreateAPIView, ListAPIView, UpdateAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError, PermissionDenied
from .serializers import SignUpSerializer, LoginSerializer, FriendSerializer
from .models import User, FriendRequest


# Create your views here.

class SignUpView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = SignUpSerializer

class LoginView(APIView):

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data['user']        
        refresh = RefreshToken.for_user(user)

        return Response({
            "access": str(refresh.access_token),
            "refresh": str(refresh),
            "uid": str(user.uid),
            "username": user.username,
        })
    
class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh = request.data["refresh"]
            token = RefreshToken(refresh)
            token.blacklist()
            return Response({"message": "Logged Out"}, status=status.HTTP_200_OK)
        except:
            return Response({"error": "Invalid Token"}, status= status.HTTP_400_BAD_REQUEST)



class FriendListView(ListAPIView):
    permission_classes= [IsAuthenticated]
    serializer_class= FriendSerializer
    
    def get_queryset(self):  
        return FriendRequest.objects.filter(status= "ACCEPTED").filter(Q(user1=self.request.user)|Q(user2=self.request.user))

class FriendIncListView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = FriendSerializer

    def get_queryset(self):
        return FriendRequest.objects.filter(status= "PENDING", user2= self.request.user)
    
class FriendOutListView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = FriendSerializer

    def get_queryset(self):
        return FriendRequest.objects.filter(status= "PENDING", user1= self.request.user)
    
class FriendSendReqView(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = FriendSerializer

    def perform_create(self, serializer):
        fromUser = self.request.user
        toUser_id = self.request.data.get("user_id")

        if not toUser_id:
            raise ValidationError("User ID is required")
        
        try:
            toUser = User.objects.get(user_id = toUser_id)
        except User.DoesNotExist:
            return Response({"error": "User Doesnot exist"}, status=status.HTTP_404_NOT_FOUND)
        
        if fromUser == toUser:
            raise ValidationError("Cannot Send Request to Yourself.")
        
        if FriendRequest.objects.filter(Q(user1= fromUser, user2= toUser) | Q(user1= toUser, user2= fromUser)).exists():
            raise ValidationError("Request exists or Already Friends")
        serializer.save(user1= fromUser, user2= toUser)

class FriendAccReqView(UpdateAPIView):
    permission_classes= [IsAuthenticated]
    serializer_class= FriendSerializer
    queryset = FriendRequest.objects.filter(status= "PENDING")
    lookup_field = "uid"

    def perform_update(self, serializer):
        friend_req = self.get_object()
        if friend_req.user2 != self.request.user:
            raise ValidationError("Cannot Accept this Request.")
        serializer.save(status= "ACCEPTED")

class FriendRejReqView(UpdateAPIView):
    permission_classes= [IsAuthenticated]
    serializer_class= FriendSerializer
    queryset = FriendRequest.objects.filter(status= "PENDING")
    lookup_field = "uid"

    def perform_update(self, serializer):
        friend_req = self.get_object()
        if friend_req.user2 != self.request.user:
            raise PermissionDenied("Cannot perform this Action.")
        serializer.save(status= "REJECTED")        