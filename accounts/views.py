from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import (RegisterSerializer, ProfileSerializer)
                          # PasswordResetRequestSerializer,PasswordResetConfirmSerializer)
from .models import User, Profile
from django.utils.encoding import force_bytes
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from rest_framework import generics
from django.contrib.auth.tokens import default_token_generator
class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({"user": serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        if self.request.user.role == 'admin' or self.request.user.role == 'staff':
            serializer = ProfileSerializer(Profile.objects.all() ,many=True)
            return Response(serializer.data)
        profile_serializer = ProfileSerializer(request.user.profile)
        return Response(profile_serializer.data, status=status.HTTP_200_OK)

    def put(self, request, user_id=None):
        if request.user.role == 'admin' and user_id is not None:
            try:
                profile = Profile.objects.get(user__id=user_id)
                profile_serializer = ProfileSerializer(profile, data=request.data, partial=True)
            except Profile.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            profile_serializer = ProfileSerializer(request.user.profile, data=request.data, partial=True)

        if profile_serializer.is_valid():
            profile_serializer.save()
            return Response(profile_serializer.data, status=status.HTTP_200_OK)
        return Response(profile_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class PasswordResetRequestView(generics.GenericAPIView):
#     serializer_class = PasswordResetRequestSerializer
#
#     def post(self, request):
#         serializer = self.get_serializer(data=request.data)
#         if serializer.is_valid():
#             email = serializer.validated_data['email']
#             try:
#                 user = User.objects.get(email=email)
#
#                 # Generate token and uid
#                 token = default_token_generator.make_token(user)
#                 uid = urlsafe_base64_encode(force_bytes(user.pk))
#
#                 # Create a simple text email message
#                 reset_link = f"http://localhost:8000/reset-password/{uid}/{token}/"
#                 message = f"Hello,\n\nTo reset your password, click the link below:\n{reset_link}\n\nThank you!"
#
#                 send_mail(
#                     subject='Password Reset Request',
#                     message=message,
#                     from_email=settings.DEFAULT_FROM_EMAIL,
#                     recipient_list=[email],
#                     fail_silently=False,
#                 )
#                 return Response({"detail": "Password reset link has been sent."}, status=status.HTTP_200_OK)
#
#             except User.DoesNotExist:
#                 return Response({"detail": "User with this email does not exist."}, status=status.HTTP_404_NOT_FOUND)
#
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
# class PasswordResetConfirmView(generics.GenericAPIView):
#     serializer_class = PasswordResetConfirmSerializer
#
#     def post(self, request, uidb64, token):
#         try:
#             uid = urlsafe_base64_decode(uidb64).decode()
#             user = User.objects.get(pk=uid)
#         except (TypeError, ValueError, OverflowError, User.DoesNotExist):
#             user = None
#
#         if user is not None and default_token_generator.check_token(user, token):
#             serializer = self.get_serializer(data=request.data)
#             if serializer.is_valid():
#                 user.set_password(serializer.validated_data['password'])
#                 user.save()
#                 return Response({"detail": "Password has been reset."}, status=status.HTTP_200_OK)
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#         return Response({"detail": "Invalid token or user."}, status=status.HTTP_400_BAD_REQUEST)
