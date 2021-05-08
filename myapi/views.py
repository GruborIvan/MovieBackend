from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework import status,generics
from myapi.serializers import MovieSerializer,MovieGenreSerializer, RegisterSerializer, PopularMoviesSerializer, BasicMovieSerializer
from myapi.models import Movie,MovieGenre
from rest_framework.decorators import authentication_classes, permission_classes
from django_filters import rest_framework as filters
from reactions.models import Reactions
from django.http import HttpResponse
from rest_framework import pagination
from django.db.models import Count
import json
from .search import MovieIndex
from elasticsearch_dsl.query import MultiMatch
from elasticsearch_dsl.query import SimpleQueryString
from rest_framework import serializers
from django.forms.models import model_to_dict

@authentication_classes([])
@permission_classes([])
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer

class MovieGenreView(generics.ListAPIView):
    queryset = MovieGenre.objects.all()
    serializer_class = MovieGenreSerializer
    pagination_class = None

class MovieFilter(filters.FilterSet):
    title = filters.CharFilter(lookup_expr='icontains')
    class Meta:
        model = Movie
        fields = ('title','genre')


class MovieView(generics.ListCreateAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    filterset_class = MovieFilter

class MovieViewByIndex(generics.RetrieveUpdateDestroyAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer

class VisitNumberCount(generics.ListCreateAPIView):
    
    def post(self,request):
        movie_id = request.data.get("movId")
        the_movie = Movie.objects.get(id=movie_id)
        the_movie.number_of_page_visits = the_movie.number_of_page_visits + 1
        the_movie.save()
        return HttpResponse(the_movie.number_of_page_visits,status = status.HTTP_200_OK)

class CommentPagination(pagination.PageNumberPagination):
    page_size = 2

class PopularMovies(generics.ListAPIView):
    
    serializer_class = PopularMoviesSerializer
    queryset = Movie.objects.all()
    pagination_class = None

    def get(self,request):
        movies = Movie.objects.annotate(likes=Count('reactions__reaction')).order_by('-likes').filter(reactions__reaction=True)
        serializer = PopularMoviesSerializer(movies,many=True)
        return HttpResponse(json.dumps(serializer.data),status = status.HTTP_200_OK)

class ElasticSearchView(generics.ListAPIView):

    def get(self,request):
        
        q = self.request.GET['q']
        upd_movies = []

        if q:
            movies = MovieIndex.search().query('match_phrase_prefix',title=q)
            movies = movies.to_queryset()
        else:
            movies = Movie.objects.all()

        for movie in movies:
            movie = model_to_dict(movie)
            genre_values = []

            for key,value in movie.items():
                if key == 'genre':
                    for gen in value:
                        genre_values.append(gen.id)
                
            id = movie['id']
            movie['genre'] = genre_values

            serialized_movie = MovieSerializer(data=movie)
            if serialized_movie.is_valid():
                serialized_movie.validated_data['id'] = id
                serialized_movie.validated_data['genre'] = genre_values
                    
            upd_movies.append(serialized_movie.validated_data)
            
        movies = json.dumps(list(upd_movies))
        return HttpResponse(movies, status = status.HTTP_200_OK)