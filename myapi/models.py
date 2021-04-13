from django.db import models

# Create your models here.

class Movie(models.Model):
    title = models.CharField(max_length=15)
    description = models.CharField(max_length=200)
    imageurl = models.CharField(max_length=240)
    genre = models.CharField(max_length=15)