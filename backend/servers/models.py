from django.db import models
import uuid
from accounts.models import User

# Create your models here.
def server_icon_path(instance, filename):
    return f"server_icons/{instance.uid}/{filename}"

class Server(models.Model):
    id = models.BigAutoField(primary_key=True)
    uid = models.UUIDField(default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=50, unique=True)
    server_icon = models.ImageField(upload_to=server_icon_path, blank=True, null=True)
    about = models.TextField(max_length=300, blank=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="owned_server")
    is_public = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
class ServerMember(models.Model):
    ROLE_CHOICES = [
        ('owner', 'Owner'),
        ('member', 'Member'),
        ('admin', 'Admin'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='server_membership')
    server = models.ForeignKey(Server, on_delete=models.CASCADE, related_name='members')
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='member')
    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        # meta class is used for configuration in DB level
        # unique user per server:
        unique_together = ('user', 'server')

    def __str__(self):
        return f"{self.user} ({self.role})->{self.server}"

class ServerInvite(models.Model):
    server = models.OneToOneField(Server, on_delete=models.CASCADE, related_name="invite")
    code = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Invite for {self.server}"