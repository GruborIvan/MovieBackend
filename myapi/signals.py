from django.db.models.signals import post_save,pre_save
from django.dispatch import receiver
from .models import Movie
from .tasks import *

@receiver(post_save,sender=Movie)
def send_email_confirmation(sender,instance,created,**kwargs):
    if created:
        send_movie_email.delay(instance.title,instance.description)