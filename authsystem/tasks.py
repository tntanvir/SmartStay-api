from celery import shared_task
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from .models import EmailOTP, CustomUser,ForgetPasswordOTP
import random

def generate_otp():
    return str(random.randint(100000, 999999))

@shared_task
def send_otp_to_email(user_id):
    try:
        
        otp = generate_otp()
        user = CustomUser.objects.get(id=user_id)
        EmailOTP.objects.filter(user=user).delete()
        EmailOTP.objects.create(user=user, otp=otp)

        subject = 'আপনার OTP কোড'
        to_email = user.email
        context = {'user': user, 'otp': otp}

        text_content = f"আপনার OTP কোড হলো: {otp}"
        html_content = render_to_string('emails/otp_email.html', context)

        msg = EmailMultiAlternatives(subject, text_content, '', [to_email])
        msg.attach_alternative(html_content, "text/html")
        msg.send()
    except Exception as e:
        print("Error sending email:", e)

@shared_task
def ForgetPasswordSendOTP(user_id):
    try:
        otp = generate_otp()
        user = CustomUser.objects.get(id=user_id)
        ForgetPasswordOTP.objects.filter(user=user).delete()
        ForgetPasswordOTP.objects.create(user=user, otp=otp)

        # user.set_password(otp)
        # user.save()


        subject = 'আপনার পাসওয়ার্ড রিসেট কোড'
        to_email = user.email
        context = {'user': user, 'otp': otp}

        text_content = f"আপনার নতুন পাসওয়ার্ড হলো: {otp}"
        html_content = render_to_string('emails/otp_email.html', context)

        msg = EmailMultiAlternatives(subject, text_content, '', [to_email])
        msg.attach_alternative(html_content, "text/html")
        msg.send()

    except Exception as e:
        print("Error sending email:", e)
