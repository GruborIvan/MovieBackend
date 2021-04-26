from django.db import models
from myapi.models import Movie
from django.contrib.auth.models import User
from django.conf import settings

# Create your models here.
class Reactions(models.Model):
    movie = models.ForeignKey(Movie,on_delete=models.CASCADE)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    reaction = models.BooleanField(null=False)

class Comments(models.Model):
    movie = models.ForeignKey(Movie,on_delete=models.CASCADE,default=1)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    content = models.TextField(blank=False,null=False)
    timestamp = models.DateTimeField(auto_now_add=True)