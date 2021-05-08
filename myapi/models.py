from django.db import models

class MovieGenre(models.Model):
    genre_name = models.CharField(max_length=24)

class Movie(models.Model):
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=200)
    imageurl = models.TextField(max_length=1000)
    genre = models.ManyToManyField(MovieGenre,related_name='genres')
    number_of_page_visits = models.IntegerField(default=0)

    def __str__(self):
        return 'Title: {}  genre: {}'.format(self.title,self.genre)