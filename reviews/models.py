from django.db import models
from django.conf import settings
from room.models import RoomModel
import uuid
User = settings.AUTH_USER_MODEL

# Create your models here.
class RoomReviews(models.Model):
    id = models.UUIDField(primary_key=True,default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    room = models.ForeignKey(RoomModel,on_delete=models.CASCADE)
    rating = models.IntegerField(max_length=5,default=5)
    reviews = models.TextField(max_length=400)
    create_at = models.DateTimeField(auto_now_add=True)
    


