from reactions.models import Reactions
from myapi.models import Movie
from django.contrib.auth.models import User
from rest_framework import serializers

class MovieSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source="user.id")
    likes = serializers.SerializerMethodField()
    likes_num = serializers.IntegerField(read_only=True)

    class Meta:
        ordering = ['-likes']
        model = Movie
        fields = "__all__"

    def get_likes(self,obj):
        return Reactions.objects.filter(movie=obj.id).count()