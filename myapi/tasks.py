from celery.decorators import task
from socket import gaierror
from django.core.mail import send_mail
from django.conf import settings
from project.celery.celery import app
from celery.exceptions import SoftTimeLimitExceeded
from django.core.exceptions import BadRequest

@app.task(name="send_email",autoretry_for=(BadRequest,SoftTimeLimitExceeded),default_retry_delay=10)
def send_movie_email(title,description):

    print('Here!')
    raise SoftTimeLimitExceeded('Task has encountered a timeout. Try again.')

    try:
        send_mail(
            'A new movie is added to the system!',
            'Movie added to movie database: \n Title: {} \n Description: {}'.format(title,description),
            settings.EMAIL_HOST_USER,
            settings.EMAIL_RECIEVERS,
            fail_silently=False,
        )
        print('Email has been sent!')

    except Exception:
        print('Error! Unable to send movie confirmation email!')