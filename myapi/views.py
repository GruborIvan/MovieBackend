from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework import status,generics
from myapi.serializers import MovieSerializer,MovieGenreSerializer, RegisterSerializer, PopularMoviesSerializer
from myapi.models import Movie,MovieGenre
from rest_framework.decorators import authentication_classes, permission_classes
from django_filters import rest_framework as filters
from reactions.models import Reactions
from django.http import HttpResponse
from rest_framework import pagination
from django.db.models import Count
from .search import MovieIndex
from django.forms.models import model_to_dict
import json
from django.core.mail import send_mail
from django.conf import settings
from rest_framework.response import Response
from socket import gaierror

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

    def perform_create(self,serializer):
        try:
            serializer.save()
            send_mail(
                'A new movie is added to the system!',
                'Movie added to movie database: \n Title: {} \n Description: {}'.format(self.request.data.get('title'),self.request.data.get('description')),
                settings.EMAIL_HOST_USER,
                settings.EMAIL_RECIEVERS,
                fail_silently=False,
            )
            print('Email has been sent!')
        except (gaierror,ConnectionRefusedError):
            print('Failed to connect to server! Probably bad connection settings.')
        except:
            print('Error! Unable to send movie confirmation email!')


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
        context = {'request':request}

        if q:
            movies = MovieIndex.search().query('match_phrase_prefix',title=q)
            movies = movies.to_queryset()
        else:
            movies = Movie.objects.all()
        
        ser_movies = MovieSerializer(movies,many=True,context=context)
        return Response(ser_movies.data, status = status.HTTP_200_OK)