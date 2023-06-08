import os
from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Solisart_SAV.settings")
app = Celery("Solisart_SAV" )
app.config_from_object("django.conf:settings", namespace='CELERY')
app.autodiscover_tasks()
app.conf.timezone = 'UTC'

import sav

# @app.on_after_configure.connect
# def setup_periodic_tasks(sender, **kwargs):
#
#     sender.add_periodic_task(
#         10.0,
#         sav.tasks.refresh_mailbox(),
#     )


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))

@app.task(bind=True)
def hello_world(self):
    print('Hello world!')