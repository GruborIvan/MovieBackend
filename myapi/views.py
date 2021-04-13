from django.shortcuts import render
from rest_framework import status,generics
from myapi.serializers import MovieSerializer
from myapi.models import Movie

# Create your views here.

class MovieView(generics.ListCreateAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer


class MovieViewByIndex(generics.RetrieveUpdateDestroyAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer