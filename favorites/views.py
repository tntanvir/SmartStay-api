from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from .models import Favorite
from .serializers import FavoriteSerializer
from rest_framework.permissions import IsAuthenticated
# Create your views here.

class FavoriteView(APIView):
    # permission_classes = [IsAuthenticated]

    def get(self, request):
        # favorites = Favorite.objects.filter(user=request.user)
        favorites = Favorite.objects.all()
        serializer = FavoriteSerializer(favorites, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = FavoriteSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def delete(self, request, pk):
        try:
            favorite = Favorite.objects.get(pk=pk, user=request.user)
            favorite.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Favorite.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)