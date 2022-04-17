from __future__ import absolute_import, unicode_literals
import os
import celery
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', "main.settings")

app = celery.Celery('dgs', config_source=settings.CELERY)
app.autodiscover_tasks()
