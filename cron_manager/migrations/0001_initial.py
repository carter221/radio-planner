# Generated by Django 3.2.25 on 2024-11-28 15:59

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CronTask',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Nom de la tâche')),
                ('schedule', models.CharField(max_length=255, verbose_name='Planification (format cron)')),
                ('command', models.TextField(verbose_name='Commande à exécuter')),
                ('enabled', models.BooleanField(default=True, verbose_name='Activée')),
            ],
            options={
                'verbose_name': 'Tâche Cron',
                'verbose_name_plural': 'Tâches Cron',
            },
        ),
    ]
