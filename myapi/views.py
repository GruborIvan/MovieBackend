from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework import status,generics
from myapi.serializers import MovieSerializer,MovieGenreSerializer, RegisterSerializer
from myapi.models import Movie,MovieGenre
from rest_framework.decorators import authentication_classes, permission_classes

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

class MovieView(generics.ListCreateAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer

class MovieViewByIndex(generics.RetrieveUpdateDestroyAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer