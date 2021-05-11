from django.core.management.base import BaseCommand
from django_celery_results.models import TaskResult
from myapi.tasks import *
import re

class Command(BaseCommand):
    help = '-Run this command to retry all failed jobs in database-'

    def handle(self,*args,**kwargs):
        failed_tasks = TaskResult.objects.filter(status='FAILURE')
        for task in failed_tasks:
            arguments = re.findall("'([^']*)'",task.task_args)
            TaskResult.objects.filter(task_id=task.task_id).delete()
            send_movie_email.delay(arguments[0],arguments[1])