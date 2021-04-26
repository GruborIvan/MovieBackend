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

# Create your views here.

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
        movieId = request.GET["movId"]
        viewNumber = Movie.objects.get(id=movieId).numberOfPageVisits
        return HttpResponse(viewNumber,status = status.HTTP_200_OK)
    
    def post(self,request):
        movieId = request.data.get("movId")
        theMovie = Movie.objects.get(id=movieId)
        views = theMovie.numberOfPageVisits
        theMovie.numberOfPageVisits = views + 1
        theMovie.save()
        return HttpResponse(theMovie.numberOfPageVisits,status = status.HTTP_200_OK)