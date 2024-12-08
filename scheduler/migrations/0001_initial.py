# Generated by Django 3.2.12 on 2024-11-26 14:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Song',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='Titre de la chanson')),
                ('artist', models.CharField(blank=True, max_length=255, null=True, verbose_name='Artiste')),
                ('file_path', models.FileField(upload_to='songs/', verbose_name='Fichier audio')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Schedule',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('scheduled_date', models.DateField(verbose_name='Date prévue')),
                ('start_time', models.TimeField(verbose_name='Heure de début')),
                ('end_time', models.TimeField(verbose_name='Heure de fin')),
                ('mount_url', models.CharField(blank=True, max_length=255, null=True, verbose_name='URL du Mount')),
                ('mount_state', models.CharField(choices=[('live', 'En direct'), ('automatic', 'Automatique')], default='live', max_length=50, verbose_name='État du Mount')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('song', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='schedules', to='scheduler.song', verbose_name='Chanson associée')),
            ],
        ),
    ]
