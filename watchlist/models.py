from django.db import models
from myapi.models import Movie
from django.contrib.auth.models import User

class WatchList(models.Model):
    movies = models.ManyToManyField(Movie,through='WatchTracking')
    user = models.ForeignKey(User,on_delete=models.CASCADE)


class WatchTracking(models.Model):
    movie = models.ForeignKey(Movie,on_delete=models.CASCADE)
    watch_list = models.ForeignKey(WatchList,on_delete=models.CASCADE)
    watched = models.BooleanField(null=False,blank=False)