from django.db import models
from accounts.models import User
from chnls.models import Channel
import uuid

# Create your models here.
def upload_path(instance, filename):
    return f"chat_uploads/{instance.uid}/{filename}"

class DMThread(models.Model):
    MESSAGE_TYPE = [
        ('TEXT', 'Text'),
        ('IMAGE', 'Image'),
        ('DOCUMENT', 'Document'),
        ('VIDEO', 'Video'),
        ('AUDIO', 'Audio')
    ]
    id = models.BigAutoField(primary_key=True)
    uid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    sender= models.ForeignKey(User, on_delete=models.CASCADE, related_name='dm_message')
    message_type= models.CharField(max_length=50, choices=MESSAGE_TYPE, default='TEXT')
    content = models.TextField(blank=True)
    file = models.FileField(upload_to= upload_path, blank=True, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender.username}: {self.content}"   

class Message(models.Model):
    MESSAGE_TYPE = [
        ('TEXT', 'Text'),
        ('IMAGE', 'Image'),
        ('DOCUMENT', 'Document'),
        ('VIDEO', 'Video'),
        ('AUDIO', 'Audio')
    ]
    id = models.BigAutoField(primary_key=True)
    uid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)

    channel= models.ForeignKey(Channel, on_delete=models.CASCADE, null=True, blank=True, related_name='message')
    dm_thread= models.ForeignKey(DMThread, on_delete=models.CASCADE, null=True, blank=True)

    sender= models.ForeignKey(User, on_delete=models.CASCADE, related_name='messages')
    message_type= models.CharField(max_length=50, choices=MESSAGE_TYPE, default='TEXT')
    content = models.TextField(blank=True)
    file = models.FileField(upload_to= upload_path, blank=True, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender.username}: {self.content}"
    
 
