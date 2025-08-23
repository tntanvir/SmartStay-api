from django.contrib import admin
from .models import Favorite
# Register your models here.

@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ['user', 'room']
    search_fields = ['user__username', 'room__name']
