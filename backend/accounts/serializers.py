from rest_framework import serializers
from .models import User, FriendRequest

class SignUpSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields= ('id', 'uid', 'email', 'username', 'display_name', 'password', 'country_code', 'phone', 'avatar', 'banner', 'date_joined')
        read_only_fields= ('date_joined',)
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        phone = validated_data.pop('phone', None)
    
        user = User(**validated_data)

        if phone:
            user.set_phone(phone)
            user.save()
    
        return user
    
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only= True)

    def validate(self, data):
        username = data['username']
        password = data['password']

        try:
            user = User.objects.get(username = username)
        except User.DoesNotExist:
            raise serializers.ValidationError("Invalid credentials")

        if not user.check_password(password):
            raise serializers.ValidationError("Invalid credentials")

        if not user.is_active:
            raise serializers.ValidationError("Account disabled")

        data['user'] = user
        return data

class FriendSerializer(serializers.ModelSerializer):
    friend_username = serializers.CharField(source= "user2.username", read_only= True)
    class Meta:
        model = FriendRequest
        fields = ["id", "uid", "user2", "friend_username", "status", "created_at"]
