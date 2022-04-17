from django.core.management import call_command
from main.celery import app


@app.task(name='Import events')
def import_events(*args, **kwargs):
    return call_command('import_events', '--timed', verbosity=0)
