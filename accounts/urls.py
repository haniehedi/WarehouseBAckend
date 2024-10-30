from django.db import router
from django.urls import path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import (UserView, RegisterView)
                    # PasswordResetRequestView, PasswordResetConfirmView)




urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('profile/', UserView.as_view(), name='user_profile'),
    path('profile/<int:user_id>', UserView.as_view(), name='update-profile'),
    # path('reset-password/', PasswordResetRequestView.as_view(), name='password_reset'),
    # path('reset-password/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
]


