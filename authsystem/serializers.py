
from rest_framework import serializers
from .models import CustomUser
from django.contrib.auth import password_validation
from django.core.exceptions import ValidationError


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
    
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'name', 'phone', 'role', 'address', 'profile', 'is_active' , 'activity','last_login','date_joined']
        read_only_fields = ['id', 'username', 'email', 'is_active','last_login','date_joined']




class PasswordChangeSerializer(serializers.Serializer): 
    old_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = self.context['request'].user
        
        # Check if the old password is correct
        if not user.check_password(data['old_password']):
            raise serializers.ValidationError("The old password is incorrect.")
        
        # Check if the new password matches the confirmation
        if data['new_password'] != data['confirm_password']:
            raise serializers.ValidationError("The new passwords do not match.")
        
        # Validate the new password strength using Django's built-in password validation
        try:
            password_validation.validate_password(data['new_password'], user)
        except ValidationError as e:
            raise serializers.ValidationError({"new_password": e.messages})
        
        return data