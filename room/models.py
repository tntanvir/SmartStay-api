from django.db import models
from django.conf import settings
import uuid
from multiselectfield import MultiSelectField

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
    )
    types = MultiSelectField(choices=ROOM_TYPES, max_length=100)
    max_capacity = models.CharField(
        max_length=100,
        choices=[
            ('single', 'SINGLE'),
            ('duble', 'DUBLE'),
            ('triple', 'TRIPLE'),
        ],
        null=True,
        blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True,blank=True,null=True)
    is_booking = models.BooleanField(default=False)
    
    def __str__(self):
        return self.title

