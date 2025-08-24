from rest_framework.response import Response

from rest_framework.views import APIView
from rest_framework import status
from .serializers import ReviewSerializer
from .models import RoomReviews
from rest_framework.generics import get_object_or_404
import time
from celery import shared_task

@shared_task
def test_task():
    for i in range(10):
        print(f"Test task: {i}")
        time.sleep(1)
    return "Test task completed."
class RoomReviewViews(APIView):
    def get(self,request,pk=None):
        
        # test_task()
        test_task.delay()    
        try:
            if pk is not None:
                review =get_object_or_404(RoomReviews,pk=pk)
                serializer = ReviewSerializer(review)
            else:
                review =RoomReviews.objects.all()
                serializer = ReviewSerializer(review,many=True)
            return Response(serializer.data,status=status.HTTP_200_OK)
        except:
            return Response({"error": "server error"}, status=status.HTTP_404_NOT_FOUND)
    def post(self,request):
        serializer = ReviewSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response({'error':serializer.errors},status=status.HTTP_400_BAD_REQUEST)
    def patch(self,request,pk=None):
        try:
            review =get_object_or_404(RoomReviews,pk=pk)
        except RoomReviews.DoesNotExist:
            return Response({"detail": "Data not found."}, status=status.HTTP_404_NOT_FOUND)
        if review.user != request.user:
            return Response({"error": "You are not allowed to edit this room."}, status=status.HTTP_403_FORBIDDEN)
        serializer = ReviewSerializer(review,data=request.data,partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def delete(self,request,pk=None):
        try:
            review =get_object_or_404(RoomReviews,pk=pk)
        except RoomReviews.DoesNotExist:
            return Response({"detail": "Data not found."}, status=status.HTTP_404_NOT_FOUND)
        if review.user != request.user:
            return Response({"error": "You are not allowed to delete this room."}, status=status.HTTP_403_FORBIDDEN)
        review.delete()
        return Response({"message": "Room deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
