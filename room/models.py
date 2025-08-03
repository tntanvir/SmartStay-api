from django.db import models
from django.conf import settings
import uuid
from multiselectfield import MultiSelectField
from django.apps import apps

User = settings.AUTH_USER_MODEL

class RoomModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=300)
    docs = models.TextField(max_length=900)
    image = models.URLField(max_length=700)
    location = models.CharField(max_length=700)
    country = models.CharField(max_length=300,blank=True,null=True)
    price = models.FloatField()
    bed = models.IntegerField(blank=True,null=True)
    bath = models.IntegerField(blank=True,null=True)
    sqft = models.IntegerField(blank=True,null=True)
     
    ROOM_TYPES = (
        ('ac', 'AC'),
        ('wifi', 'WIFI'),
        ('tv', 'TV'),
        ('geyser', 'Geyser'),
        ('breakfast', 'Breakfast'),
    )
    types = MultiSelectField(choices=ROOM_TYPES, max_length=100)
    max_capacity = models.CharField(
        max_length=100,
        choices=[
            ('single', 'SINGLE'),
            ('double', 'DOUBLE'),
            ('triple', 'TRIPLE'),
        ],
        null=True,
        blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True,blank=True,null=True)
    
    
    def __str__(self):
        return self.title
    class Meta:
        ordering = ['-created_at']
    def booking_data(self):
        BookingModel = apps.get_model('booking', 'BookingModel')  
        bookings = BookingModel.objects.filter(room=self)
        booking_list = []
        for booking in bookings:
            booking_list.append({
                'start': booking.start_date.strftime('%-d-%-m-%y'),  
                'end': booking.end_date.strftime('%-d-%-m-%y')
            })
        return booking_list