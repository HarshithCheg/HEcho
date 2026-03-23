from rest_framework import serializers
from .models import Channel

class ChannelSerializer(serializers.Serializer):
    class Meta:
        model = Channel
        fields = ['id', 'uid', 'server', 'name', 'type']
