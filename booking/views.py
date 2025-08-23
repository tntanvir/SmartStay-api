from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework.views import APIView
from rest_framework import status
from .serializers import BookingSerializers,BookingCreateSerializer,BookingUpdateSerializer
from .models import BookingModel
from rest_framework.generics import get_object_or_404
from datetime import date
from django.utils import timezone
from django.db.models import Q
from room.models import RoomModel
from rest_framework.permissions import IsAuthenticated



    
class CustomPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100

class BookingViews(APIView):
    # permission_classes = [IsAuthenticated]

    def get(self, request, pk=None):
        user = request.user
        

        if not user or not user.is_authenticated:
            return Response({"error": "Authentication required."}, status=status.HTTP_401_UNAUTHORIZED)

        username = request.query_params.get('username')
        paid = request.query_params.get('paid')
        unpaid = request.query_params.get('unpaid')
        checkout = request.query_params.get('checkout')

        try:
            # Get single booking
            if pk is not None:
                booking = BookingModel.objects.get(pk=pk)
                # Only allow access if admin, hotel owner of that room, or the user who made the booking
                if user.is_superuser or booking.user == user or booking.room.user == user:
                    serializer = BookingSerializers(booking)
                    return Response(serializer.data, status=status.HTTP_200_OK)
                return Response({"error": "You are not authorized to view this booking."}, status=status.HTTP_403_FORBIDDEN)

            # Filters
            filters = Q()
            if paid and paid.lower() == 'true':
                filters &= Q(payment_status='paid')
            if unpaid and unpaid.lower() == 'true':
                filters &= Q(payment_status='unpaid')
            if checkout and checkout.lower() == 'true':
                filters &= Q(end_date__lt=timezone.now().date(), status='confirmed')
            if username:
                filters &= Q(user__username__icontains=username)

            # Role-based booking access
            if user.is_superuser:
                # Admin: see all
                bookings = BookingModel.objects.filter(filters)
            elif RoomModel.objects.filter(user=user).exists():
                # Hotel owner: only bookings for their rooms
                owner_rooms = RoomModel.objects.filter(user=user)
                bookings = BookingModel.objects.filter(filters, room__in=owner_rooms)
            else:
                # Normal user: only own bookings
                bookings = BookingModel.objects.filter(filters, user=user)

            bookings = bookings.order_by('-created_at')

            # Counters (for dashboard cards)
            checkout_count = BookingModel.objects.filter(end_date__lt=timezone.now().date(), status='confirmed').count()
            unpaid_count = BookingModel.objects.filter(payment_status='unpaid').count()
            paid_count = BookingModel.objects.filter(payment_status='paid').count()
            book_count = BookingModel.objects.all().count()

            # Paginate
            paginator = CustomPagination()
            paginated_data = paginator.paginate_queryset(bookings, request)
            serializer = BookingSerializers(paginated_data, many=True)

            response_data = {
                "bookings": serializer.data,
                "checkout_count": checkout_count,
                "unpaid_count": unpaid_count,
                "paid_count": paid_count,
                "total_bookings": book_count
                
            }

            return paginator.get_paginated_response(response_data)

        except BookingModel.DoesNotExist:
            return Response({'error': 'Booking not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self,request):
        if not request.user.activity:
            return Response({"error": "Your account is not active. Please contact support."}, status=status.HTTP_403_FORBIDDEN)

        serializer=BookingCreateSerializer(data=request.data)
        if serializer.is_valid():
            start_date = serializer.validated_data.get('start_date')
            if start_date < date.today():
                return Response({"error": "Start date is in the past."}, status=status.HTTP_400_BAD_REQUEST)
            serializer.save(user=request.user)
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    def patch(self,request,pk=None):
        try:
            if pk is not None:
                data = get_object_or_404(BookingModel, pk=pk)
                if request.user == data.user or request.user.role == 'hotel owner':
                    serializer = BookingUpdateSerializer(data, data=request.data, partial=True)
                    if serializer.is_valid():
                        serializer.save()
                        return Response(serializer.data, status=status.HTTP_200_OK)
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                else:
                    return Response({'error': 'You can not update this data'}, status=status.HTTP_400_BAD_REQUEST)
        except BookingModel.DoesNotExist:
            return Response({'error': 'Booking not found'}, status=status.HTTP_404_NOT_FOUND)
    
    def delete(self,request,pk=None):
        try:
            if pk is not None:
                data = BookingModel.objects.get(pk=pk)
                if request.user == data.user and request.user.role == 'hotel owner':
                    data.delete()
                    return Response({"message": "Room deleted successfully"}, status=status.HTTP_200_OK)
                else:
                    return Response({'error':'You can not delete this data'},status=status.HTTP_400_BAD_REQUEST)
        except :
            return Response({'error':'not Found'},status=status.HTTP_404_NOT_FOUND)
        
