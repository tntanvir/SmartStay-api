from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework.views import APIView
from rest_framework import status
from .serializers import RoomSerializers
from .models import RoomModel
from rest_framework.generics import get_object_or_404

# Create your views here.
class CustomRoomPagination(PageNumberPagination):
    page_size = 12  
    page_size_query_param = 'page_size'
    max_page_size = 20

class RoomViews(APIView):
    def get(self, request, pk=None):
        if pk:
            try:
                room = RoomModel.objects.get(pk=pk)
                serializer = RoomSerializers(room)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except RoomModel.DoesNotExist:
                return Response({"detail": "Data not found."}, status=status.HTTP_404_NOT_FOUND)
        else:
            room = RoomModel.objects.all()
            paginate = CustomRoomPagination()
            result_page = paginate.paginate_queryset(room,request)
            serializers = RoomSerializers(result_page,many=True)
            return paginate.get_paginated_response(serializers.data)
    
    def post(self,request):
        if request.user.role not in ['admin', 'hotel_owner']:
            return Response({"error": "You do not have permission to create a room."}, status=status.HTTP_403_FORBIDDEN)
        serializers = RoomSerializers(data=request.data)
        if serializers.is_valid():
            serializers.save(user=request.user)
            return Response(serializers.data,status=status.HTTP_201_CREATED)
        return Response({'error':serializers.errors},status=status.HTTP_400_BAD_REQUEST)
    
    def patch(self,request,pk=None):
        try:
            room = get_object_or_404(RoomModel, pk=pk)
        except RoomModel.DoesNotExist():
            return Response({"detail": "Data not found."}, status=status.HTTP_404_NOT_FOUND)
        if room.user != request.user:
            return Response({"error": "You are not allowed to edit this room."}, status=status.HTTP_403_FORBIDDEN)
        serializers = RoomSerializers(room,data=request.data,partial=True)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data,status=status.HTTP_200_OK)
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self,request,pk=None):
        try:
            room = get_object_or_404(RoomModel, pk=pk)
        except RoomModel.DoesNotExist():
            return Response({"detail": "Data not found."}, status=status.HTTP_404_NOT_FOUND)
        if room.user != request.user:
            return Response({"error": "You are not allowed to delete this room."}, status=status.HTTP_403_FORBIDDEN)
        room.delete()
        return Response({"message": "Room deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
