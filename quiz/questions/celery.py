from __future__ import absolute_import
import os
from celery import Celery
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'quiz.settings')

app = Celery('quiz',
             broker="amqp://redis:6379/",
             backend="amqp://redis:6379/")

app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
	print('Request: {0!r}'.format(self.request))
