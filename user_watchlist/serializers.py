from django.contrib.auth.models import User
from rest_framework import serializers
from user_watchlist.models import UserWatchList as WatchList
from reactions.serializers import UserSerializer
from myapi.models import Movie
from myapi.serializers import MovieSerializer
from reactions.serializers import UserSerializer

class WatchListSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    movie = MovieSerializer()

    class Meta:
        model = WatchList
        fields = "__all__"


class WatchListCreateSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = WatchList
        fields = "__all__"