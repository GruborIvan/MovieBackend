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
        #data = serialize("json",queryset)
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


        reactions = Reactions.objects.filter(movie_id=movieId).filter(user_id = user)
        print(reaction)

        # Update reakcije..
        if reactions:
            upd_reaction = reactions[0]
            upd_reaction = ReactionsSerializer(data=upd_reaction)
            upd_reaction = reaction
            print(upd_reaction)
            upd_reaction.save()
            return Response(upd_reaction,status=status.HTTP_200_OK)

        # Get movie by Id..
        mov = Movie.objects.filter(id=movieId)[0]
        
        data = {
            "movie" : mov.id,
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