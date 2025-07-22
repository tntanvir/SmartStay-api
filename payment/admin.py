from django.contrib import admin
from .models import PaymentModel

# Register your models here.

@admin.register(PaymentModel)
class PaymentAdmin(admin.ModelAdmin):
    list_display =['amount','currency','stripe_payment_id','user_email','created_at']
