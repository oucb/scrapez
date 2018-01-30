from celery import Celery

app = Celery(__name__, broker='redis://', backend='redis://localhost')
app.config_from_object(__name__)
task_track_started = True
result_backend = 'redis://'
from scrape import *
from tasks.youtube import *
print app.conf
