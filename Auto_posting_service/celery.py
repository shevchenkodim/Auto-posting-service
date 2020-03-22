import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Auto_posting_service.settings')

app = Celery('Auto_posting_service')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.conf.update(
     enable_utc=True,
     timezone='Europe/Kiev',
)
app.autodiscover_tasks()
