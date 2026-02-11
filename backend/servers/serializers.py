from rest_framework import serializers
from .models import Server

class ServerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Server
        fields= ['id', 'uid', 'name', 'server_icon', 'about', 'owner', 'is_public', 'created_at']
        read_only_fields = ['uid', 'owner', 'created_at']
        