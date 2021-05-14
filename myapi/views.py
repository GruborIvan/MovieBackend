from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework import status,generics
from myapi.serializers import MovieSerializer,MovieGenreSerializer, RegisterSerializer, PopularMoviesSerializer, MovieImageThumbnailSerializer
from myapi.models import Movie,MovieGenre,MovieImageThumbnail
from rest_framework.decorators import authentication_classes, permission_classes
from django_filters import rest_framework as filters
from reactions.models import Reactions
from django.http import HttpResponse
from rest_framework import pagination
from django.db.models import Count
from .search import MovieIndex
from django.forms.models import model_to_dict
import json
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from .renderers import JPEGRenderer,PNGRenderer

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

class ImageRetrieve(generics.ListCreateAPIView):
    queryset = MovieImageThumbnail.objects.all()
    renderer_classes = [PNGRenderer,JPEGRenderer]
    serializer_class = MovieImageThumbnailSerializer
    parser_classes = [MultiPartParser]

class MovieView(generics.ListCreateAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    filterset_class = MovieFilter
    parser_classes = [MultiPartParser]

    def post(self, request, format=None):

        mov = Movie(title=request.data.get('title'),description=request.data.get('description'))

        if request.data.get('imageurl') != '':
            
            mov.imageurl = request.data.get('title')
            mov.save()
            for gen in request.data.get('genre'):
                MovieGenre.objects.get(pk=gen)
                mov.genre.add(gen)
            mov.save()
            return HttpResponse(status.HTTP_201_CREATED)

        else:
            img = self.request.data.get('image')

            print('Recieved image: {0}'.format(str(img)))
            movie_image = MovieImageThumbnail(movie_thumbnail = img, movie_full_img = img)
            movie_image.save()
            mov.image = movie_image
            mov.save()
            
            for gen in request.data.get('genre'):
                MovieGenre.objects.get(pk=gen)
                mov.genre.add(gen)
            mov.save()

            return HttpResponse(status=status.HTTP_201_CREATED)        


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