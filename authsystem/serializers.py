
from rest_framework import serializers
from .models import CustomUser






class RegisterUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'name' ,'phone', 'role', 'address', 'profile','password']

    def create(self, validated_data):
        user = CustomUser(
            username=validated_data['username'],
            email=validated_data['email'],
            name=validated_data.get('name', ''),
            phone=validated_data.get('phone', ''),
            role=validated_data.get('role', ''),
            address=validated_data.get('address', ''),
            profile=validated_data.get('profile', ''),
        )
        user.set_password(validated_data['password'])   
        user.is_active=False
        user.save()
        return user