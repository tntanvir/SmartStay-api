from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import PaymentModel
from .tasks import send_payment_success_email_task
from booking.models import BookingModel

@receiver(post_save, sender=PaymentModel)
def send_payment_emails(sender, instance, created, **kwargs):
    if created:  
        try:
            booking = BookingModel.objects.get(id=instance.booking_id)

            # Email to user
            user_subject = "💳 Payment Successful - Booking Confirmed"
            user_message = (
                f"Hello {booking.user.username},\n\n"
                f"Your payment of {instance.amount} {instance.currency.upper()} "
                f"for booking ID {booking.id} has been successfully processed.\n\n"
                f"Thank you for choosing us!"
            )

            # Email to room owner
            owner_subject = "📢 New Payment Received"
            owner_message = (
                f"Hello {booking.room.user.username},\n\n"
                f"The user {booking.user.username} has completed a payment of "
                f"{instance.amount} {instance.currency.upper()} for room '{booking.room}'.\n\n"
                f"Booking ID: {booking.id}"
            )

            
            send_payment_success_email_task.delay(user_subject, user_message, [booking.user.email])
            send_payment_success_email_task.delay(owner_subject, owner_message, [booking.room.user.email])

        except BookingModel.DoesNotExist:
            pass
