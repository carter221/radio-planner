from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import CronTask
from django.core.management import call_command

@receiver([post_save, post_delete], sender=CronTask)
def update_crontab(sender, **kwargs):
    # Synchroniser les tâches cron
    call_command('update_crontab')
