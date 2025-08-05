
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .serializers import RegisterUserSerializer,UserSerializer,PasswordChangeSerializer
from .models import CustomUser,EmailOTP
from django.contrib.auth import authenticate, login,logout
from rest_framework_simplejwt.tokens import RefreshToken
from .utils import send_otp_to_email
from django.conf import settings
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q
# Create your views here.




class RegisterUserView(APIView):
    def post(self, request):
        serializer = RegisterUserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            send_otp_to_email(user)
            return Response({"message": "Check your email for OPT"},status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginUserView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        
        user = authenticate( username=username, password=password)
        if user is not None:
            token = RefreshToken.for_user(user)
            login(request, user)
            return Response({
                "message": "Login successful",
                "user":{
                "username": user.username,
                "email": user.email,
                "name": user.name,
                "phone": user.phone,
                "address": user.address,
                "role": user.role,
                "profile": user.profile
                },
                "refresh": str(token),
                "access": str(token.access_token)
            }, status=status.HTTP_200_OK)
        return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)
    

class VerifyOTPView(APIView):
    def post(self, request):
        email = request.data.get("email")
        otp = request.data.get("otp")

        try:
            user = CustomUser.objects.get(email=email)  
        except CustomUser.DoesNotExist:
            return Response({"message": "ইমেইল সঠিক নয়।"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            otp_obj = EmailOTP.objects.filter(user=user, otp=otp).latest('created_at')
        except EmailOTP.DoesNotExist:
            return Response({"message": "OTP সঠিক নয়।"}, status=status.HTTP_400_BAD_REQUEST)

        if otp_obj.is_expired():
            return Response({"message": "OTP মেয়াদ শেষ হয়েছে।"}, status=status.HTTP_400_BAD_REQUEST)

        user.is_active = True
        user.save()
        otp_obj.delete()


        return Response({"message": "OTP সঠিক। অ্যাকাউন্ট একটিভ হয়েছে ✅"}, status=status.HTTP_200_OK)

class ResendOTPView(APIView):
    def post(self, request):
        email = request.data.get("email")

        try:
            user = CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            return Response({"message": "এই ইমেইলে কোন ইউজার নেই।"}, status=status.HTTP_400_BAD_REQUEST)

        if user.is_active:
            return Response({"message": "এই ইউজার ইতোমধ্যে একটিভ। OTP লাগবে না।"}, status=status.HTTP_400_BAD_REQUEST)

        send_otp_to_email(user)
        return Response({"message": "নতুন OTP ইমেইলে পাঠানো হয়েছে ✅"}, status=status.HTTP_200_OK)
    

    
class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]  

    def post(self, request, *args, **kwargs):
        serializer = PasswordChangeSerializer(data=request.data, context={'request': request})
        
        if serializer.is_valid():
            user = request.user  # Get the logged-in user
            new_password = serializer.validated_data['new_password']
            user.set_password(new_password)  # Update the user's password
            user.save()
            return Response({"message": "Password updated successfully."}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




    
class SingOUT(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        tokenr  = request.data.get('token')
        if tokenr:
            try:
                token = RefreshToken(tokenr)
                token.blacklist()
                logout(request)
                return Response({"message": "Logout successful"}, status=status.HTTP_200_OK)
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"error": "No token provided"}, status=status.HTTP_400_BAD_REQUEST)




class CustomPagination(PageNumberPagination):
    page_size = 20  
    page_size_query_param = 'page_size'  
    max_page_size = 100  

class AllUserViews(APIView):
    def get(self, request):
        filters = Q()
        username = request.query_params.get('username', None)
        if username:
            filters &= Q(username__icontains=username)
        email = request.query_params.get('email', None)
        if email:
            filters &= Q(email__icontains=email)
        role = request.query_params.get('role', None)
        if role:
            filters &= Q(role=role)

        users = CustomUser.objects.filter(filters)
        userCount = CustomUser.objects.filter(role='user').count()
        adminCount = CustomUser.objects.filter(role='admin').count()
        ownerCount = CustomUser.objects.filter(role='hotel owner').count()

        paginator = CustomPagination()
        paginated_users = paginator.paginate_queryset(users, request)
        serializer = UserSerializer(paginated_users, many=True)

        response_data = {
            "users": serializer.data,
            "userCount": userCount,
            "adminCount": adminCount,
            "ownerCount": ownerCount
        }

        return paginator.get_paginated_response(response_data)
