from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework import status,generics
from myapi.serializers import MovieSerializer,MovieGenreSerializer, RegisterSerializer
from myapi.models import Movie,MovieGenre
from rest_framework.decorators import authentication_classes, permission_classes
from django_filters import rest_framework as filters
from reactions.models import Reactions
from django.http import HttpResponse
from django.db.models import Count

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

    def get(self,request):
        movie_id = request.GET["movId"]
        view_number = Movie.objects.get(id=movie_id).numberOfPageVisits
        return HttpResponse(view_number,status = status.HTTP_200_OK)
    
    def post(self,request):
        movie_id = request.data.get("movId")
        the_movie = Movie.objects.get(id=movie_id)
        views = the_movie.number_of_page_visits
        the_movie.number_of_page_visits = views + 1
        the_movie.save()
        return HttpResponse(the_movie.number_of_page_visits,status = status.HTTP_200_OK)