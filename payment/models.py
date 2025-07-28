from django.db import models

# Create your models here.
class PaymentModel(models.Model):
    amount = models.DecimalField(max_digits=10,decimal_places=2)
    currency = models.CharField(max_length=10,default='usd')
    stripe_payment_id = models.CharField(max_length=250,blank=True,null=True)
    user_email = models.EmailField()
    created_at = models.DateTimeField(auto_now_add=True)
    booking_id = models.CharField(blank=True,null=True)
