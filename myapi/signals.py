from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Movie
from socket import gaierror
from django.core.mail import send_mail
from django.conf import settings

@receiver(post_save,sender=Movie)
def send_email_confirmation(sender,instance,created,**kwargs):
    if created:
        try:
            send_mail(
                'A new movie is added to the system!',
                'Movie added to movie database: \n Title: {} \n Description: {}'.format(instance.title,instance.description),
                settings.EMAIL_HOST_USER,
                settings.EMAIL_RECIEVERS,
                fail_silently=False,
            )
            print('Email has been sent!')
        except (gaierror,ConnectionRefusedError):
            print('Failed to connect to server! Probably bad connection settings.')
        except:
            print('Error! Unable to send movie confirmation email!')
