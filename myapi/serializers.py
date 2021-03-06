from myapi.models import Movie,MovieGenre,MovieImageThumbnail
from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password
from reactions.serializers import MovieLikesCountSerializer
from reactions.models import Reactions
from user_watchlist.models import UserWatchList

class RegisterSerializer(serializers.ModelSerializer):
    username = serializers.EmailField(required=True,validators=[UniqueValidator(queryset=User.objects.all())])
    password = serializers.CharField(write_only=True,required=True,validators=[validate_password])
    password2 = serializers.CharField(write_only=True,required=True)

    class Meta:
        model = User
        fields = ('username','password','password2')
    
    def validate(self,attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password":"Password fields dont match!"})
        return attrs
    
    def create(self,validated_data):
        user = User.objects.create(username = validated_data['username'])
        user.set_password(validated_data['password'])
        user.save()
        return user

class MovieGenreSerializer(serializers.ModelSerializer):
    class Meta:
        ordering = ['-id']
        model = MovieGenre
        fields = '__all__'

class MovieImageThumbnailSerializer(serializers.ModelSerializer):

    class Meta:
        model = MovieImageThumbnail
        fields = '__all__' 

class MovieSerializer(serializers.ModelSerializer):

    likes = serializers.SerializerMethodField()
    dislikes = serializers.SerializerMethodField()
    watched = serializers.SerializerMethodField()
    is_in_watchlist = serializers.SerializerMethodField()
    #image = MovieImageThumbnailSerializer()
    #genre = MovieGenreSerializer()

    class Meta:
        model = Movie
        fields = '__all__'
        depth = 2

    def create(self,validated_data):
        img = self.context['request'].data.get('image')
        image = MovieImageThumbnail(movie_thumbnail=img,movie_full_img=img)
        image.save()

        movie = Movie(title=validated_data.pop('title'), description=validated_data.pop('description'),image=image)
        movie.save()

        for gen in self.context['request'].data.get('genre'):
            print(gen)
            MovieGenre.objects.get(pk=gen)
            movie.genre.add(gen)
        movie.save()
        return movie

    def get_likes(self,obj):
        return Reactions.objects.filter(movie=obj.id).filter(reaction=True).count()

    def get_dislikes(self,obj):
        return Reactions.objects.filter(movie=obj.id).filter(reaction=False).count()

    def get_is_in_watchlist(self,obj):
        entry = UserWatchList.objects.filter(user = self.context['request'].user.id).filter(movie=obj.id).first()
        if entry == None:
            return False
        else:
            return True

    def get_watched(self,obj):
        obj = UserWatchList.objects.filter(movie = obj.id).filter(user = self.context['request'].user.id).first()
        if obj is None:
            return False
        return obj.watched


class PopularMoviesSerializer(serializers.ModelSerializer):

    likes = serializers.SerializerMethodField()

    class Meta: 
        model = Movie
        fields = "__all__"

    def get_likes(self,obj):
        return Reactions.objects.filter(movie=obj.id).filter(reaction=True).count()