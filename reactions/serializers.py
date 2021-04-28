from reactions.models import Reactions,Comments
from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username']


class MovieLikesCountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reactions
        queryset = Reactions.objects.count()
        fields = '__all__'


class ReactionsSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source="user.id")

    class Meta:
        model = Reactions
        fields = [
            'movie',
            'user',
            'reaction'
        ]


class CommentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Comments
        fields = [
            'movie',
            'user',
            'content',
            'timestamp'
        ]