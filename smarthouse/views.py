from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status



@api_view(['GET'])
def Home(request):
    return Response({"message": "Welcome to the Smart House API!"}, status=status.HTTP_200_OK)


@api_view(['GET'])
def Custom_Endpoint(request):
    return Response({"message": "This custom endpoint not match"}, status=status.HTTP_400_BAD_REQUEST)