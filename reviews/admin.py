from django.contrib import admin
from .models import RoomReviews
# Register your models here.

@admin.register(RoomReviews)
class RoomReviewsAdmin(admin.ModelAdmin):
    list_display =['id','user__username','room__id','rating','reviews']
    search_fields =['user__username']
