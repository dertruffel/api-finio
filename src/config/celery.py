import os
import sys
from celery import Celery



os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


app = Celery('config')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.conf.event_serializer = 'pickle' # this event_serializer is optional. somehow i missed this when writing this solution and it still worked without.
app.conf.task_serializer = 'pickle'
app.conf.result_serializer = 'pickle'
app.conf.accept_content = ['application/json', 'application/x-python-serialize']
app.autodiscover_tasks()

@app.task(bind=True, ignore_result=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))