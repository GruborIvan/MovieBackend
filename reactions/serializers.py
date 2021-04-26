from reactions.models import Reactions,Comments
from myapi.models import Movie,MovieGenre
from django.contrib.auth.models import User
from rest_framework import serializers

class MovieLikesCountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reactions
        queryset = Reactions.objects.count()
        fields = '__all__'
    
    def getNumberOfLikes(self):
        return Reactions.objects.all().count()

class ReactionsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Reactions
        fields = [
            'movie',
            'user',
            'reaction'
        ]

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comments
        fields = [
            'movie',
            'user',
            'content',
            'timestamp'
        ]