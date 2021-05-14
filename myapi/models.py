from django.db import models
from easy_thumbnails.fields import ThumbnailerImageField
from project import settings

def thumbnail_path(instance,filename):
    return 'thumbnails/{0}'.format(filename)

def full_picture_path(instance,fielname):
    return 'full-pics/{0}'.format(fielname)

class MovieGenre(models.Model):
    genre_name = models.CharField(max_length=24)

class MovieImageThumbnail(models.Model):
    movie_thumbnail = ThumbnailerImageField(upload_to=thumbnail_path,default='posts/default.jpg',resize_source=settings.THUMBNAIL_ALIASES['thumbnail'])
    movie_full_img = ThumbnailerImageField(upload_to=full_picture_path,default='posts/default.jpg',resize_source=settings.THUMBNAIL_ALIASES['full-size'])

class Movie(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(max_length=1000)
    imageurl = models.TextField(max_length=1000,blank=True,null=True)
    genre = models.ManyToManyField(MovieGenre,related_name='genres')
    number_of_page_visits = models.IntegerField(default=0)
    image = models.OneToOneField(MovieImageThumbnail,blank=True,null=True,on_delete=models.CASCADE) 