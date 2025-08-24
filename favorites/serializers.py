from rest_framework.serializers import ModelSerializer , PrimaryKeyRelatedField, ValidationError
from .models import Favorite
from authsystem.serializers import UserSerializer
from room.serializers import CustomRoomSerializers

class FavoriteSerializer(ModelSerializer):
    user = UserSerializer(read_only=True)
    room = CustomRoomSerializers(read_only=True)
    room_id = PrimaryKeyRelatedField(
        queryset=Favorite._meta.get_field("room").remote_field.model.objects.all(),
        source="room",
        write_only=True
    )
    class Meta:
        model = Favorite
        fields = ['id','user', 'room', 'room_id']
    
