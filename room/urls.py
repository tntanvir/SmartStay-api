
from django.urls import path
from . import views

urlpatterns = [
    path('rooms/', views.RoomViews.as_view(), name='room'),
    path('rooms/latest', views.LatestRoom.as_view(), name='latest'),
    path('rooms/most-booked', views.MostBooking.as_view(), name='most_booked'),
    path('rooms/<str:pk>', views.RoomViews.as_view(), name='room'),
    path('rooms/<uuid:pk>/check-availability/', views.RoomAvailabilityCheck.as_view()),
   
]
