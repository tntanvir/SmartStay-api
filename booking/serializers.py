from rest_framework.serializers import ModelSerializer,ValidationError
from rest_framework import serializers
from .models import BookingModel
from datetime import date

# class BookingSerializers(ModelSerializer):
#     start_date = serializers.DateField(input_formats=['%d-%m-%Y'])
#     end_date = serializers.DateField(input_formats=['%d-%m-%Y'])
#     class Meta:
#         model = BookingModel
#         fields =['id','user','room','start_date','end_date','status','payment_status','created_at','is_active','is_available','total_price']

#     def validate(self, data):
#         today = date.today()
#         start_date = data.get('start_date')
#         end_date = data.get('end_date')

#         if start_date < today:
#             raise ValidationError("You cannot book a room in the past.")
        
#         if end_date < start_date:
#             raise ValidationError("End date cannot be before start date.")

#         return data


class BookingSerializers(serializers.ModelSerializer):
    start_date = serializers.DateField(input_formats=['%d-%m-%Y'], format='%d-%m-%Y')
    end_date = serializers.DateField(input_formats=['%d-%m-%Y'], format='%d-%m-%Y')

    class Meta:
        model = BookingModel
        fields = [
            'id', 'user', 'room', 'start_date', 'end_date', 'status',
            'payment_status', 'created_at', 'is_active', 'is_available', 'total_price'
        ]
        read_only_fields = [
            'id', 'user', 'status', 'payment_status', 'created_at', 
            'is_active', 'is_available', 'total_price'
        ]
        extra_kwargs = {
            'room': {'required': True},
        }

    def validate(self, data):
        today = date.today()
        start_date = data.get('start_date')
        end_date = data.get('end_date')

        if start_date < today:
            raise serializers.ValidationError("You cannot book a room in the past.")

        if end_date < start_date:
            raise serializers.ValidationError("End date cannot be before start date.")
        
        return data