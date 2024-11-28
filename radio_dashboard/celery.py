from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

# Définit le module des paramètres Django pour Celery
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'radio_dashboard.settings')

# Initialise l'application Celery
app = Celery('radio_dashboard')

# Configure Celery avec les paramètres de Django
app.config_from_object('django.conf:settings', namespace='CELERY')

# Auto-découverte des tâches définies dans les applications
app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
