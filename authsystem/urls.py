from django.urls import path
from . import views
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)
urlpatterns = [
    path('singup', views.RegisterUserView.as_view(), name='signup'),
    path('singin', views.LoginUserView.as_view(), name='signup'),
    path('verify-otp', views.VerifyOTPView.as_view(), name='verify-otp'),
    path('resend-otp', views.ResendOTPView.as_view(), name='resend-otp'),
    path('alluser', views.AllUserViews.as_view(), name='alluser'),
    path('change-password', views.ChangePasswordView.as_view(), name='change-password'),
    path('singout', views.SingOUT.as_view(), name='singout'),
    path('refresh', TokenRefreshView.as_view(), name='token_refresh'),

]
