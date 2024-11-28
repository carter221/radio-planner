import os
from django.core.management.base import BaseCommand
from cron_manager.models import CronTask

class Command(BaseCommand):
    help = 'Synchronise les tâches cron depuis le modèle avec le fichier crontab'

    def handle(self, *args, **kwargs):
        # Récupérer toutes les tâches activées
        tasks = CronTask.objects.filter(enabled=True)

        # Créer un fichier temporaire pour le crontab
        cron_file = '/tmp/crontab'
        with open(cron_file, 'w') as f:
            for task in tasks:
                f.write(f"{task.schedule} {task.command}\n")

        # Appliquer le crontab
        os.system(f"crontab {cron_file}")

        self.stdout.write(self.style.SUCCESS(f"Synchronized {tasks.count()} cron tasks."))
