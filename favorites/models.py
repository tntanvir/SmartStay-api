from django.db import models
from django.conf import settings

# Create your models here.

class Favorite(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    room = models.ForeignKey('room.RoomModel', on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'room')
