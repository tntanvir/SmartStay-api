from rest_framework.serializers import ModelSerializer
from .models import BookingModel

class BookingSerializers(ModelSerializer):
    class Meta:
        model = BookingModel
        fields =['id','user','room','start_date','end_date','status','payment_status','created_at','is_active','is_available','total_price']
