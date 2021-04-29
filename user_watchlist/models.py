from django.db import models
from myapi.models import Movie
from django.contrib.auth.models import User

class UserWatchList(models.Model):
    movie = models.ForeignKey(Movie,on_delete=models.CASCADE,default=None)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    watched = models.BooleanField(null=False,blank=False,default=False)

    class Meta:
        unique_together = ('movie','user')