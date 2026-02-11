from rest_framework import serializers
from .models import Message
import magic


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['id', 'uid', 'sender', 'message_type', 'content', 'file', 'uploaded_at']
        read_only_fields = ['sender', 'uploaded_at', 'uid']

    def validate(self, data):
        msg_type = data.get("message_type", "TEXT")
        file = data.get("file")
        content = data.get("content")

        if msg_type == 'TEXT':
            if not content or content.strip():
                raise serializers.ValidationError({"detail":"EMPTY_MESSAGE"})
            data["file"] = None
            return data
        
        if not file:
            raise serializers.ValidationError("Must Upload a file to send a Message")

        mime = magic.from_buffer(file.read(2048),mime=True)
        file.seek(0)
        
        MAX_IMAGE_SIZE = 10 * 1024 * 1024       # 10MB
        MAX_VIDEO_SIZE = 25 * 1024 * 1024       # 25MB
        MAX_AUDIO_SIZE = 15 * 1024 * 1024       # 15MB
        MAX_DOCUMENT_SIZE = 10 * 1024 * 1024    # 10MB

        if msg_type == "IMAGE":
            if not mime.startswith("image/"):
                raise serializers.ValidationError("Upload an image file only")
            if file.size > MAX_IMAGE_SIZE:
                raise serializers.ValidationError("Image too large (max 10MB)")

        elif msg_type == "VIDEO":
            if not mime.startswith("video/"):
                raise serializers.ValidationError("Upload a video file only")
            if file.size > MAX_VIDEO_SIZE:
                raise serializers.ValidationError("Video too large (max 25MB)")

        elif msg_type == "AUDIO":
            if not mime.startswith("audio/"):
                raise serializers.ValidationError("Upload an audio file only")
            if file.size > MAX_AUDIO_SIZE:
                raise serializers.ValidationError("Audio too large (max 15MB)")

        elif msg_type == "DOCUMENT":
            if not (mime.startswith("text/") or mime.startswith("application/")):
                raise serializers.ValidationError("Upload a document file only")
            if file.size > MAX_DOCUMENT_SIZE:
                raise serializers.ValidationError("Document too large (max 10MB)")
            
        else:
            raise serializers.ValidationError("Invalid message type")

        return data

class DMSerializer(MessageSerializer):
    class Meta(MessageSerializer.Meta):
        model = Message
        fields = ['id', 'uid', 'sender', 'dm_thread', 'message_type', 'content', 'file', 'uploaded_at']

    def validate(self, data):
        data = super().validate(data) #re-uses MessageSerializer validations

        dm_thread = data.get("dm_thread")
        channel = data.get("channel")

        if channel:
            raise serializers.ValidationError("This serializer is only for DM Messages")
        if not dm_thread:
            raise serializers.ValidationError("DM Thread must be specified")

        return data

