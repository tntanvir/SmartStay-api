from django.urls import path
from . import views

urlpatterns = [
    path('payment', views.PaymentViews.as_view(), name='payment'),
    
   
]