# booking/signals.py
from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import BookingModel
from .tasks import send_booking_confirmation_email_task

# if booking status changes
@receiver(pre_save, sender=BookingModel)
def send_booking_confirmation_email(sender, instance, **kwargs):
    if not instance.pk:
        return

    try:
        old_instance = BookingModel.objects.get(pk=instance.pk)
    except BookingModel.DoesNotExist:
        return

    if old_instance.status != instance.status and instance.status == "confirmed":
        subject = "Your Booking is Confirmed "
        message = (
            f"Hello {instance.user.username},\n\n"
            f"Your booking for room '{instance.room}' "
            f"from {instance.start_date} to {instance.end_date} "
            f"has been confirmed.\n\n"
            f"Booking ID: {instance.id}"
        )
        send_booking_confirmation_email_task.delay(subject, message, instance.user.email)

    if old_instance.status != instance.status and instance.status == "cancelled":
        subject = "Your Booking is Cancelled "
        message = (
            f"Hello {instance.user.username},\n\n"
            f"Your booking for room '{instance.room}' "
            f"from {instance.start_date} to {instance.end_date} "
            f"has been cancelled.\n\n"
            f"Booking ID: {instance.id}"
        )
        send_booking_confirmation_email_task.delay(subject, message, instance.user.email)
