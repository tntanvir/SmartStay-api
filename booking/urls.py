from django.urls import path
from . import views

urlpatterns = [
    path('booking', views.BookingViews.as_view(), name='booking'),
    path('booking/<str:pk>', views.BookingViews.as_view(), name='details'),
   
]
