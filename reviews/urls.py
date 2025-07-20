from django.urls import path
from . import views

urlpatterns = [
    path('reviews', views.RoomReviewViews.as_view(), name='reviews'),
    # path('rooms/<str:pk>', views.RoomViews.as_view(), name='room'),
   
]
