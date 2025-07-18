import random
from django.core.mail import send_mail
from .models import EmailOTP
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

def generate_otp():
    return str(random.randint(100000, 999999))

def send_otp_to_email(user):
    otp = generate_otp()
    EmailOTP.objects.filter(user=user).delete()
    EmailOTP.objects.create(user=user, otp=otp)

    # HTML ও Plain টেক্সট রেন্ডার করুন
    subject = 'আপনার  OTP কোড'
    # from_email = 'tntanvir2382018@gmail.com'
    to_email = user.email

    context = {
        'user': user,
        'otp': otp,
    }

    text_content = f"আপনার OTP কোড হলো: {otp}"
    html_content = render_to_string('emails/otp_email.html', context)

    # ইমেইল তৈরি করুন
    msg = EmailMultiAlternatives(subject, text_content, '', [to_email])
    msg.attach_alternative(html_content, "text/html")
    msg.send()