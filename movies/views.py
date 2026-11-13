from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Movie
from .serializers import MovieSerializer


@api_view(['GET', 'POST'])
def movie_list(request):
    if request.method == 'GET':
        movies = Movie.objects.all()
        return Response(MovieSerializer(movies, many=True).data)

    serializer = MovieSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['GET'])
def top_movies(request):
    movies = Movie.objects.filter(rating__gte=8).order_by('-rating')
    return Response(MovieSerializer(movies, many=True).data)


@api_view(['GET', 'DELETE'])
def movie_detail(request, pk):
    movie = get_object_or_404(Movie, pk=pk)

    if request.method == 'GET':
        return Response(MovieSerializer(movie).data)

    movie.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)
