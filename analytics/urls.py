from django.urls import path
from . import views

urlpatterns = [
   path('analytics/', views.AnaliticsView.as_view(), name='analytics_view'),
]