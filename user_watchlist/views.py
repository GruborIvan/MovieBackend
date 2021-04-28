from django.shortcuts import render
from rest_framework import status,generics
from user_watchlist.serializers import WatchListSerializer,WatchListSerializer2
from user_watchlist.models import UserWatchList as WatchList

class MovieListView(generics.ListCreateAPIView):
    pagination_class = None

    def get_queryset(self):
        return WatchList.objects.filter(user=self.request.user)

    def perform_create(self,serializer):
        serializer.save(user=self.request.user)

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return WatchListSerializer
        if self.request.method == 'POST':
            return WatchListSerializer2
        else:
            return WatchListSerializer


class MovieListRemoveView(generics.DestroyAPIView):

    queryset = WatchList.objects.all()
    serializer_class = WatchListSerializer