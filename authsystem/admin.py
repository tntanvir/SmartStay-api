from django.contrib import admin
from .models import CustomUser, EmailOTP
# Register your models here.
@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'name', 'phone', 'address', 'profile','role')
    search_fields = ('username', 'email', 'name')
    list_filter = ('is_staff', 'is_active','role')
    
    
admin.site.register(EmailOTP)

