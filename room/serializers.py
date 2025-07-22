from rest_framework import serializers
from .models import RoomModel
from authsystem.serializers import UserSerializer


class RoomSerializers(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    types = serializers.ListField(child=serializers.ChoiceField(choices=RoomModel.ROOM_TYPES))
    class Meta:
        model = RoomModel
        fields = ['id','user','title','docs','image','location','district','types','max_capacity','price','is_booking','created_at']