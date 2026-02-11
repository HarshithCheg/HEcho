from django.db import models
from django.contrib.auth.models import AbstractUser #has all field like user but can additional fields
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
import phonenumbers, uuid


# Create your models here.
def avatar_path(instance, filename):
    return f"avatar/{instance.uid}/{filename}"

def banner_path(instance, filename):
    return f"banner/{instance.uid}/{filename}"

username_valid = RegexValidator(    #condition for username using regex
    regex=r'^[a-zA-Z][A-Za-z0-9_.]{2,20}$',
    message="""Username must start with letters. 
        Username can include letters, numbers, underscores and periods.
        Username must be under 20 characters."""
)


class User(AbstractUser):

    country_choice = (('IN', 'India'), ('US', 'United States of America'), ('AUS', 'Australia'), ('UK', 'United Kingdom'))
    
    
    username = models.CharField(max_length=20, unique=True, validators=[username_valid])
    display_name = models.CharField(max_length=50, default=username)
    uid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    country_code = models.CharField(max_length=3, choices=country_choice)
    phone = models.CharField(max_length=15, blank=True)
    avatar = models.ImageField(upload_to=avatar_path, blank=True, null=True)
    banner = models.ImageField(upload_to=banner_path, blank=True, null=True)


    class Meta: #for naming the table (By default: appName_className)
        pass
    
    def __str__(self):
        return self.username
    
    def set_phone(self, phone_no):
        try:
            parsed = phonenumbers.parse(phone_no, self.country_code)
            if not phonenumbers.is_valid_number(parsed):
                raise ValidationError("Invalid Phone Number for the Selected Country.")
            
            self.phone = phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.E164)

        except phonenumbers.NumberParseException:
            raise ValidationError("Invalid Phone Number Format")


class FriendRequest(models.Model):
    FRNDSTAT = [
        ("PENDING", "Pending"),
        ("ACCEPTED", "Accepted"),
        ("REJECTED", "Rejected"),
    ]
    uid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    user1 = models.ForeignKey(User, on_delete=models.CASCADE, related_name="friends")
    user2 = models.ForeignKey(User, on_delete=models.CASCADE, related_name="friend_of")
    status = models.CharField(max_length=10, choices=FRNDSTAT, default="PENDING")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user1', 'user2')