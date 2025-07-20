from rest_framework.serializers import ModelSerializer
from .models import RoomReviews
from authsystem.serializers import UserSerializer

class ReviewSerializer(ModelSerializer):
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = RoomReviews
        fields = ('id','user','room','rating','reviews','create_at')