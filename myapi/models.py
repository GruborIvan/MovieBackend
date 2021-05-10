from django.db import models

class MovieGenre(models.Model):
    genre_name = models.CharField(max_length=24)

class Movie(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(max_length=1000)
    imageurl = models.TextField(max_length=1000)
    genre = models.ManyToManyField(MovieGenre,related_name='genres')
    number_of_page_visits = models.IntegerField(default=0)