from django.db import models

class CronTask(models.Model):
    name = models.CharField(max_length=255, verbose_name="Nom de la tâche")
    schedule = models.CharField(max_length=255, verbose_name="Planification (format cron)")
    command = models.TextField(verbose_name="Commande à exécuter")
    enabled = models.BooleanField(default=True, verbose_name="Activée")

    def __str__(self):
        return f"{self.name} - {'Activée' if self.enabled else 'Désactivée'}"

    class Meta:
        verbose_name = "Tâche Cron"
        verbose_name_plural = "Tâches Cron"
