from django.db import models
from django.conf import settings
from room.models import RoomModel
import uuid
from django.utils import timezone

User = settings.AUTH_USER_MODEL
# Create your models here.

class BookingModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(RoomModel, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    status = models.CharField(
        max_length=20, 
        choices=[('pending', 'Pending'), ('confirmed', 'Confirmed'), ('cancelled', 'Cancelled')],
        default='pending'
    )
    payment_status = models.CharField(
        max_length=20,
        choices=[('paid', 'Paid'), ('unpaid', 'Unpaid')],
        default='unpaid'
    )
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)
    
    # def is_active(self):
    #     return timezone.now().date() <= self.end_date and self.status == 'confirmed'


    # room availability and room a jaoya jabe ki na
    def is_available(self):
        bookings = BookingModel.objects.filter(room=self.room)
        for booking in bookings:
            if (timezone.now().date() <= booking.end_date and self.end_date >= timezone.now().date() and timezone.now().date() >=self.start_date and  self.status == 'confirmed' ):
                return True
        return False
    def total_days(self):
        return (self.end_date - self.start_date).days
    def total_price(self):
        return ((self.end_date-self.start_date).days)*self.room.price

    def checkOut(self):
        return timezone.now().date() > self.end_date and self.status == 'confirmed' and self.payment_status == 'paid'
    def auto_delete_unpaid_if_expired(self):
        if (
            timezone.now().date() > self.end_date and
            self.payment_status == 'unpaid'
        ):
            self.delete()
    class Meta:
        ordering = ['-created_at']