from django.shortcuts import render
from rest_framework import status,generics
from user_watchlist.serializers import WatchListSerializer,WatchListCreateSerializer
from user_watchlist.models import UserWatchList as WatchList

class MovieListView(generics.ListCreateAPIView):
    pagination_class = None

    def get_queryset(self):
        return WatchList.objects.filter(user=self.request.user)

    def perform_create(self,serializer):
        try:
            serializer.save(user=self.request.user)
        except:
            upd_movie = WatchList.objects.filter(user=self.request.user).filter(movie=self.request.data.get("movie")).first()
            if upd_movie.watched != self.request.data.get('watched'):
                upd_movie.watched = self.request.data.get('watched')
                upd_movie.save()

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return WatchListSerializer
        if self.request.method == 'POST':
            return WatchListCreateSerializer
        else:
            return WatchListSerializer


class MovieListRemoveView(generics.RetrieveUpdateDestroyAPIView):

    queryset = WatchList.objects.all()
    serializer_class = WatchListCreateSerializer