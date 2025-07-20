
from django.urls import path
from . import views

urlpatterns = [
    path('rooms', views.RoomViews.as_view(), name='room'),
    path('rooms/<str:pk>', views.RoomViews.as_view(), name='room'),
   
]
