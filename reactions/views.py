from reactions.models import Reactions
from myapi.models import Movie,MovieGenre
from django.contrib.auth.models import User
from reactions.serializers import ReactionsSerializer,CommentSerializer
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
        movie_id = request.data.get("movieId")
        reaction = request.data.get("reaction")

        # Provera da li je like ili dislike..
        if (reaction == 'like'):
            reaction = True
        elif (reaction == 'dislike'):
            reaction = False
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        reactions = Reactions.objects.filter(movie_id=movie_id).filter(user_id = user).first()

        # Update reakcije..
        if reactions:
            reactions.reaction = reaction
            reactions.save()
            serializer_class = ReactionsSerializer(reactions)
            return Response(serializer_class.data,status=status.HTTP_200_OK)
        
        data = {
            "movie" : movie_id,
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
        

class CommentsView(generics.ListCreateAPIView):

    def get(self,request):
        movie_id = request.GET["movie_id"]
        print(movie_id)
        return HttpResponse(movie_id,status=status.HTTP_200_OK)

    # Za kreiranje komentara treba: movie_id, content, 
    def post(self,request):
        user = self.request.user
        movie_id = request.data.get("movieId")
        content = request.data.get("content")

        data = {
            "user" : user.id,
            "movie" : movie_id,
            "content" : content,
        }

        serializer = CommentSerializer(data=data)

        if (serializer.is_valid()):
            serializer.save()
            return HttpResponse(status=status.HTTP_200_OK)
        else:
            return HttpResponse(status=status.HTTP_400_BAD_REQUEST)