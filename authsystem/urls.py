from django.urls import path
from . import views

urlpatterns = [
    path('singup', views.RegisterUserView.as_view(), name='signup'),
    path('singin', views.LoginUserView.as_view(), name='signup'),
    path('verify-otp', views.VerifyOTPView.as_view(), name='verify-otp'),
    path('resend-otp', views.ResendOTPView.as_view(), name='resend-otp'),
    path('alluser', views.AllUserViews.as_view(), name='alluser'),
    path('change-password', views.ChangePasswordView.as_view(), name='change-password'),

]
