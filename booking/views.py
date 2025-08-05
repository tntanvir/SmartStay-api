from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework.views import APIView
from rest_framework import status
from .serializers import BookingSerializers
from .models import BookingModel
from rest_framework.generics import get_object_or_404
from datetime import date
from django.db.models import Q

class CustomPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100

class BookingViews(APIView):
 
    def get(self, request, pk=None):
        username = request.query_params.get('username')

        try:
            if pk is not None:
                booking = BookingModel.objects.get(pk=pk)
                serializer = BookingSerializers(booking)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
               
                filters = Q()

                if username:
                    filters &= Q(user__username__icontains=username)

                bookings = BookingModel.objects.filter(filters).order_by('-created_at')

                paginator = CustomPagination()
                paginated_data = paginator.paginate_queryset(bookings, request)
                serializer = BookingSerializers(paginated_data, many=True)
                return paginator.get_paginated_response(serializer.data)

        except BookingModel.DoesNotExist:
            return Response({'error': 'Booking not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self,request):
        serializer=BookingSerializers(data=request.data)
        if serializer.is_valid():
            start_date = serializer.validated_data.get('start_date')
            if start_date < date.today():
                return Response({"error": "Start date is in the past."}, status=status.HTTP_400_BAD_REQUEST)
            serializer.save(user=request.user)
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self,request,pk=None):
        try:
            if pk is not None:
                data = BookingModel.objects.get(pk=pk)
                if request.user == data.user:
                    data.delete()
                    Response({"message": "Room deleted successfully"}, status=status.HTTP_200_OK)
                else:
                    return Response({'error':'You can not delete this data'},status=status.HTTP_400_BAD_REQUEST)
        except :
            return Response({'error':'not Found'},status=status.HTTP_404_NOT_FOUND)
        
