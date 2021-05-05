from django.shortcuts import render
from rest_framework import generics
from myapi.models import Movie
from reactions.models import Reactions
from popular_movies.serializers import MovieSerializer
from django.http import HttpResponse

class PopularMoviesView(generics.ListAPIView):
    queryset = Movie.objects.filter()
    ordering_fields = ['likes']
    serializer_class = MovieSerializer
    pagination_class = None