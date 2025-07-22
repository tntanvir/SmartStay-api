from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
import stripe.error
from .serializers import PaymentSerializer
from .models import PaymentModel
from django.conf import settings
import stripe
from booking.models import BookingModel

stripe.api_key=settings.STRIPE_TEST_SECRET_KEY

class PaymentViews(APIView):
    def get(self,request):
        data = PaymentModel.objects.all()
        serializer = PaymentSerializer(data,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)

    
    def post(self, request):
    
        amount = self.request.data.get('amount')
        currency = self.request.data.get('currency')
        user_email = self.request.data.get('user_email')
        booking_id = self.request.data.get('booking_id')
        try:
            booking = BookingModel.objects.get(id=booking_id)
            amount = booking.total_price
        except BookingModel.DoesNotExist:
                return Response({'error': 'Booking not found'}, status=status.HTTP_400_BAD_REQUEST)
        
        if not amount or not currency or not user_email:
            return Response({'error': 'Missing required fields.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            intent = stripe.PaymentIntent.create(
                amount=int(amount),  
                currency=currency
            )
            data = {
                'amount': amount,
                'currency': currency,
                'user_email': user_email,
                'stripe_payment_id': intent['id']
            }
            serializer = PaymentSerializer(data=data)

            if serializer.is_valid():
                serializer.save()
                try:
                    booking = BookingModel.objects.get(id=booking_id)
                    booking.payment_status = 'paid'
                    booking.save()
                except BookingModel.DoesNotExist:
                    return Response({'error': 'Booking not found'}, status=status.HTTP_400_BAD_REQUEST)
                return Response({
                    'client_url': intent['client_secret'],
                    'payment': serializer.data
                }, status=status.HTTP_201_CREATED)
            
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except stripe.error.StripeError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
