from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django.contrib.auth import get_user_model
from .models import Review
from .serializers import ReviewSerializer

User = get_user_model()

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticatedOrReadOnly])
def review(request):
    if request.method == 'GET':
        reviews = Review.objects.all().order_by('-created_at')
        serializer = ReviewSerializer(reviews, many=True)
        data = {
            'statusCode': 200,
            'data': {
                'reviews': serializer.data
            }
        }
        return Response(data, status=status.HTTP_200_OK)
    
    elif request.method == 'POST':
        serializer = ReviewSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            data = {
                'statusCode': 201,
                **serializer.data
            }
            return Response(data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
