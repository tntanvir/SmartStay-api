from django.contrib import admin
from .models import RoomModel

# Register your models here.

@admin.register(RoomModel)
class RoomAdmin(admin.ModelAdmin):
    list_display=('user','location','price','is_booking')
    search_fields = ('user', 'location')
    list_filter = (['types'])
