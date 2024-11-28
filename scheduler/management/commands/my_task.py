from django.core.management.base import BaseCommand
from scheduler.tasks import generate_liquidsoap_config

class Command(BaseCommand):
    help = 'Génère le fichier radio.liq à partir des tâches planifiées'

    def handle(self, *args, **kwargs):
        try:
            generate_liquidsoap_config()
            self.stdout.write(self.style.SUCCESS('Tâche exécutée avec succès.'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Erreur lors de l\'exécution de la tâche : {str(e)}'))