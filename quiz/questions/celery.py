from __future__ import absolute_import
import os
from celery import Celery
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'quiz.settings')


app = Celery('quiz',
             broker="redis://localhost",
             backend="redis://localhost")


app.conf.update({
    "beat_schedule":{
    	'add-every-10-seconds': {
        	'task': 'questions.tasks.add',
        	'schedule': 10.0,
        	'args': (16, 16)
        },
    }
})

# app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
	print('Request: {0!r}'.format(self.request))
