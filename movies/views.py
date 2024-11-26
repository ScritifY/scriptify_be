from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .models import Movie, Genre
from .serializers import MovieSerializer


# 1. 전체 영화 리스트 조회
@api_view(['GET'])
def movie_list(request):
    movies = Movie.objects.all()
    serializer = MovieSerializer(movies, many=True)
    data = {
        'statusCode': 200,
        'data': {
            'movies': serializer.data
        }
    }
    return Response(data, status=status.HTTP_200_OK)


# 2. 특정 장르의 영화 조회
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def movies_by_genre(request, genre_pk):
    genre = Genre.objects.get(pk=genre_pk)
    # Memo: 3~5개만 보내줄지?
    movies = Movie.objects.filter(genre=genre)
    serializer = MovieSerializer(movies, many=True)
    data = {
        'statusCode': 200,
        'data': {
            'movies': serializer.data
        }
    }
    return Response(data, status=status.HTTP_200_OK)
