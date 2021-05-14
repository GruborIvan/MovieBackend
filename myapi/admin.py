from django.contrib import admin
from .models import Movie,MovieGenre,MovieImageThumbnail
from . import models

# Register your models here.
admin.site.register(Movie)

@admin.register(models.MovieImageThumbnail)
class MovieImage(admin.ModelAdmin):
    list_display = ('movie_thumbnail','movie_full_img')