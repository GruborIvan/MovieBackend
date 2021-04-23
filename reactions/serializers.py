from reactions.models import Reactions
from myapi.models import Movie,MovieGenre
from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class ReactionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reactions
        fields = "__all__"