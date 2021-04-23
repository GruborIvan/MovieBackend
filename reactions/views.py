from reactions.models import Reactions
from myapi.models import Movie,MovieGenre
from django.contrib.auth.models import User
from reactions.serializers import ReactionsSerializer
from django.shortcuts import render
from rest_framework import status,generics
from rest_framework.response import Response

# Create your views here.
class ReactionsView(generics.ListCreateAPIView):
    def get(self,request):
        user = request.user
        queryset = Reactions.objects.filter(user=user)
        return Response(reactions)