from reactions.models import Reactions
from myapi.models import Movie,MovieGenre
from django.contrib.auth.models import User
from reactions.serializers import ReactionsSerializer
from django.shortcuts import render
from rest_framework import status,generics
from rest_framework.response import Response
from django.core.serializers import serialize
from django.http import HttpResponse

# Create your views here.
class ReactionsView(generics.ListCreateAPIView):

    def get(self,request):
        user = request.user
        queryset = Reactions.objects.filter(user=user)
        data = ReactionsSerializer(queryset)
        return HttpResponse(data)


    def post(self,request):
        user = self.request.user
        movieId = request.data.get("movieId")
        reaction = request.data.get("reaction")

        # Provera da li je like ili dislike..
        if (reaction == 'like'):
            reaction = True
        elif (reaction == 'dislike'):
            reaction = False
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        reactions = Reactions.objects.filter(movie_id=movieId).filter(user_id = user).first()

        # Update reakcije..
        if reactions:
            reactions.reaction = reaction
            reactions.save()
            serializer_class = ReactionsSerializer(reactions)
            return Response(serializer_class.data,status=status.HTTP_200_OK)
        
        data = {
            "movie" : movieId,
            "user" : user.id,
            "reaction" : reaction,
        }

        serializer = ReactionsSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            return Response(data,status=status.HTTP_200_OK)
        else:
            print(serializer.errors)
            return Response(status=status.HTTP_404_NOT_FOUND)
        


class ReactionsView2(generics.ListCreateAPIView):
    queryset = Reactions.objects.all()
    serializer_class = ReactionsSerializer