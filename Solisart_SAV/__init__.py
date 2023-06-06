from .celery import app as celery_app

__all__ = ('celery_app',)
celery_app.conf.broker_url = "redis://localhost:6379"
