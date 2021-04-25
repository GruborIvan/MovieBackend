from reactions.models import Reactions
from myapi.models import Movie,MovieGenre
from django.contrib.auth.models import User
from rest_framework import serializers

class MovieLikesCountSerializer(serializers.ModelSerializer):
    likeCount = 2
    dislikeCount = 4

class ReactionsSerializer(serializers.ModelSerializer):

    #movie = Movie.objects.get(pk=)

    class Meta:
        model = Reactions
        fields = [
            'movie',
            'user',
            'reaction'
        ]
    
    # def validate_reaction(self,reaction):
    #     if (reaction == 'like'):
    #         return true
    #     elif (reaction == 'dislike'):
    #         return false