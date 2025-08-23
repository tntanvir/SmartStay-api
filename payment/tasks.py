from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings

@shared_task
def send_payment_success_email_task(subject, message, recipients):
    send_mail(
        subject=subject,
        message=message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=recipients,  
        fail_silently=False,
    )