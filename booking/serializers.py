from rest_framework.serializers import ModelSerializer,ValidationError
from rest_framework import serializers
from .models import BookingModel
from datetime import date
from authsystem.serializers import UserSerializer
from room.serializers import CustomRoomSerializers
from room.models import RoomModel


class BookingSerializers(serializers.ModelSerializer):
    start_date = serializers.DateField(format='%d-%m-%Y')
    end_date = serializers.DateField(format='%d-%m-%Y')
    user = UserSerializer(read_only=True)
    room = CustomRoomSerializers(read_only=True)

    class Meta:
        model = BookingModel
        fields = [
            'id', 'user', 'room', 'start_date', 'end_date', 'status',
            'payment_status', 'created_at', 'is_available', 'total_days', 'total_price', 'checkOut'
        ]
        read_only_fields = fields

class BookingUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookingModel
        fields = [
             'status'
        ]

class BookingCreateSerializer(serializers.ModelSerializer):
    start_date = serializers.DateField(input_formats=['%d-%m-%Y'], format='%d-%m-%Y')
    end_date = serializers.DateField(input_formats=['%d-%m-%Y'], format='%d-%m-%Y')
    room = serializers.UUIDField()  

    class Meta:
        model = BookingModel
        fields = ['start_date', 'end_date', 'room']

    def validate(self, data):
        today = date.today()
        start_date = data.get('start_date')
        end_date = data.get('end_date')

        if start_date < today:
            raise serializers.ValidationError("You cannot book a room in the past.")

        if end_date < start_date:
            raise serializers.ValidationError("End date cannot be before start date.")
        
        

        return data

    def create(self, validated_data):
        room_id = validated_data.pop('room')
        try:
            room_instance = RoomModel.objects.get(id=room_id)
        except RoomModel.DoesNotExist:
            raise serializers.ValidationError({"room": "Room not found with the given ID."})

        booking = BookingModel.objects.create(room=room_instance, **validated_data)
        return booking