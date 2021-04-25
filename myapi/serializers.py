from myapi.models import Movie,MovieGenre
from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password
from reactions.serializers import MovieLikesCountSerializer

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
        fields = ('id','genre_name')


class MovieSerializer(serializers.ModelSerializer):

    #genre = MovieGenreSerializer(many=True)
    #reactions = MovieLikesCountSerializer(many=True)

    class Meta:
        ordering = ['-id']
        model = Movie
        #fields = ['id','title','description','imageurl','genre']
        fields = "__all__"