from django.db import models
import uuid
from servers.models import Server

# Create your models here.
class Channel(models.Model):
    CHANNEL_TYPE= [
        ("text", "Text"),
    ]
    id = models.BigAutoField(primary_key=True)
    uid= models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    server = models.ForeignKey(Server, on_delete=models.CASCADE, related_name="channels")
    name= models.CharField(max_length=30)
    type = models.CharField(max_length=10, choices=CHANNEL_TYPE, default="text")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together= ("server", "name")
    
    def __str__(self):
        return f"#{self.name} ({self.server.name})"
