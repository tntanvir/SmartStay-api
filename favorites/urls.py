from django.urls import path
from . import views

urlpatterns = [
    path('favorites/', views.FavoriteView.as_view(), name='favorites'),
    path('favorites/<int:pk>/', views.FavoriteView.as_view(), name='favorite_detail'),
]
