from django.contrib import admin
from .models import BookingModel

# Register your models here.

@admin.register(BookingModel)
class BookingAdmin(admin.ModelAdmin):
    list_display =['user__username','room__id','start_date','end_date','is_available']
