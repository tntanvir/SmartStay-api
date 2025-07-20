from rest_framework.response import Response

from rest_framework.views import APIView
from rest_framework import status
from .serializers import ReviewSerializer
from .models import RoomReviews
from rest_framework.generics import get_object_or_404


class RoomReviewViews(APIView):
    def get(self,request,pk=None):
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