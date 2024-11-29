from django.apps import AppConfig

class CronManagerConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'cron_manager'

    def ready(self):
        import cron_manager.signals
