from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django.contrib.auth import get_user_model
from .models import Review
from .serializers import ReviewSerializer

User = get_user_model()

@api_view(['GET', 'POST', 'PUT', 'DELETE'])
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
            review = serializer.save(user=request.user)
            response_serializer = ReviewSerializer(review)
            data = {
              'statusCode': 201,
              'data': response_serializer.data
            }
            return Response(data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'PUT':
        review_id = request.data.get('reviewId')
        content = request.data.get('content')
        rank = request.data.get('rank')

        if not review_id or not content or not rank:
            return Response({'error': 'reviewId, content, and rank are required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            review = Review.objects.get(id=review_id, user=request.user)
        except Review.DoesNotExist:
            return Response({'error': 'Review not found or unauthorized'}, status=status.HTTP_404_NOT_FOUND)

        review.content = content
        review.rank = rank
        review.save()

        serializer = ReviewSerializer(review)
        data = {
            'statusCode': 200,
            'data': serializer.data
        }
        return Response(data, status=status.HTTP_200_OK)

    elif request.method == 'DELETE':
        review_id = request.data.get('reviewId')

        if not review_id:
            return Response({'error': 'reviewId is required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            review = Review.objects.get(id=review_id, user=request.user)
        except Review.DoesNotExist:
            return Response({'error': 'Review not found or unauthorized'}, status=status.HTTP_404_NOT_FOUND)

        review.delete()
        return Response({'statusCode': 204, 'message': 'Review deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
