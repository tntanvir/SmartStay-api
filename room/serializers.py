from rest_framework import serializers
from .models import RoomModel
from authsystem.serializers import UserSerializer


class RoomSerializers(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    types = serializers.ListField(child=serializers.ChoiceField(choices=RoomModel.ROOM_TYPES))
    class Meta:
        model = RoomModel
        fields = ['id','user','title','docs','image','location','bed','bath','sqft','country','types','max_capacity','price','created_at']

class CustomRoomSerializers(serializers.ModelSerializer):

    
    class Meta:
        model = RoomModel
        fields = ['id',  'title',  'image', 'location',  'country',  'max_capacity', 'price' ]

class TopRoomSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    total_bookings = serializers.IntegerField(read_only=True)
    
    class Meta:
        model = RoomModel
        fields = '__all__'