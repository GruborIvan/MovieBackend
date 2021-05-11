from django.core.management.base import BaseCommand
from django_celery_results.models import TaskResult

class Command(BaseCommand):
    help = '-Run this command to delete all failed jobs from database-'

    def handle(self,*args,**kwargs):
        TaskResult.objects.filter(status='FAILURE').delete()