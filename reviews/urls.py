from django.urls import path
from . import views

urlpatterns = [
    path('reviews', views.RoomReviewViews.as_view(), name='reviews'),
    path('reviews/<str:pk>', views.RoomReviewViews.as_view(), name='roomdetails'),
   
]
