from rest_framework import serializers
from .models import User, Profile
from django.utils.translation import gettext_lazy as _


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'role']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        user = User(
            username=validated_data['username'],
            email=validated_data['email'],
            role=validated_data['role']
        )
        user.set_password(validated_data['password'])
        user.save()
        Profile.objects.create(user=user)
        return user

class ProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    role = serializers.CharField(source='user.role', read_only=True)
    id = serializers.CharField(source='user.id', read_only=True)
    email = serializers.EmailField(source='user.email', read_only=True)
    class Meta:
        model = Profile
        fields = ['id','username', 'email', 'bio', 'location', 'birth_date', 'profile_picture','role']


# class PasswordResetRequestSerializer(serializers.Serializer):
#     email = serializers.EmailField()
#     def validate_email(self, value):
#         if not User.objects.filter(email=value).exists():
#             raise serializers.ValidationError(_("User with this email does not exist."))
#         return value
#
# class PasswordResetConfirmSerializer(serializers.Serializer):
#     password = serializers.CharField(write_only=True)
#     confirm_password = serializers.CharField(write_only=True)
#     def validate(self, attrs):
#         if attrs['password'] != attrs['confirm_password']:
#             raise serializers.ValidationError(_("Passwords do not match."))
#         return attrs
#
