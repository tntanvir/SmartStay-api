from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework.views import APIView
from rest_framework import status
from .serializers import BookingSerializers
from .models import BookingModel
from rest_framework.generics import get_object_or_404
from datetime import date

class BookingViews(APIView):
    def get(self,request,pk=None):
        try:
            if pk is not None:
                data = BookingModel.objects.get(pk=pk)
                serializers= BookingSerializers(data)
            else:
                data = BookingModel.objects.all()
                serializers= BookingSerializers(data,many=True)
            return Response(serializers.data,status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error':e})
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
        
