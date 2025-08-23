from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
import stripe.error
from .serializers import PaymentSerializer
from .models import PaymentModel
from django.conf import settings
import stripe
from booking.models import BookingModel
from django.db.models import Sum
from rest_framework.pagination import PageNumberPagination

stripe.api_key = settings.STRIPE_TEST_SECRET_KEY


class PaymentViews(APIView):
    def get(self, request):
        payments = PaymentModel.objects.all()

        # Calculate total transaction amount from all payments
        total_amount = payments.aggregate(total=Sum('amount'))['total'] or 0
        

        # Pagination
        paginator = PageNumberPagination()
        paginator.page_size = 10  # Change page size as needed
        result_page = paginator.paginate_queryset(payments, request)
        serializer = PaymentSerializer(result_page, many=True)

        return paginator.get_paginated_response({
            'total_transactions': total_amount,
            'payments': serializer.data
        })

    def post(self, request):
        currency = request.data.get('currency')
        user_email = request.data.get('user_email')
        booking_id = request.data.get('booking_id')

        # Validate required fields
        if not currency or not user_email or not booking_id:
            return Response({'error': 'currency, user_email, and booking_id are required.'},
                            status=status.HTTP_400_BAD_REQUEST)

        # Get booking
        try:
            booking = BookingModel.objects.get(id=booking_id)
        except BookingModel.DoesNotExist:
            return Response({'error': 'Booking not found'}, status=status.HTTP_400_BAD_REQUEST)

        # Get total price (works for both field & method)
        amount_value = booking.total_price() if callable(booking.total_price) else booking.total_price

        if not isinstance(amount_value, (int, float)):
            return Response({'error': 'Invalid amount value.'}, status=status.HTTP_400_BAD_REQUEST)

        # Stripe expects smallest currency unit (e.g., cents for USD)
        amount_for_stripe = int(amount_value * 100)

        try:
            # Create Stripe payment intent
            intent = stripe.PaymentIntent.create(
                amount=amount_for_stripe,
                currency=currency
            )

            # Save payment in DB
            payment_data = {
                'amount': amount_value,  
                'currency': currency,
                'user_email': user_email,
                'booking_id': booking_id,
                'stripe_payment_id': intent['id']
            }
            serializer = PaymentSerializer(data=payment_data)

            if serializer.is_valid():
                serializer.save()

                # Mark booking as paid
                booking.payment_status = 'paid'
                booking.save()

                return Response({
                    'client_secret': intent['client_secret'],
                    'payment': serializer.data
                }, status=status.HTTP_201_CREATED)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except stripe.error.StripeError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
