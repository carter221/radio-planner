# scheduler/models.py
from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

class Song(models.Model):
    title = models.CharField(max_length=255, verbose_name="Titre de la chanson")
    artist = models.CharField(max_length=255, verbose_name="Artiste", blank=True, null=True)
    file_path = models.FileField(upload_to='songs/', verbose_name="Fichier audio")  # Stocke les chansons dans /media/songs/
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} - {self.artist if self.artist else 'Artiste inconnu'}"


class Schedule(models.Model):
    song = models.ForeignKey(Song, on_delete=models.CASCADE, related_name="schedules", verbose_name="Chanson associée")
    scheduled_date = models.DateField(verbose_name="Date prévue")
    start_time = models.TimeField(verbose_name="Heure de début")
    end_time = models.TimeField(verbose_name="Heure de fin")
    mount_url = models.CharField(max_length=255, verbose_name="URL du Mount", blank=True, null=True)
    mount_state = models.CharField(
        max_length=50,
        choices=[('automatic', 'Automatique'),('live', 'En direct')],
        default='live',
        verbose_name="État du Mount"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def duration(self):
        """Calcule la durée en minutes."""
        start = datetime.combine(self.scheduled_date, self.start_time)
        end = datetime.combine(self.scheduled_date, self.end_time)
        return (end - start).total_seconds() / 60  # Durée en minutes

    def clean(self):
        super().clean()
        overlapping_schedules = Schedule.objects.filter(
            scheduled_date=self.scheduled_date,
            start_time__lt=self.end_time,
            end_time__gt=self.start_time
        ).exclude(id=self.id)

        if overlapping_schedules.exists():
            raise ValidationError(_('Le programme chevauche un autre programme existant.'))


    def __str__(self):
        return f"Programme : {self.song.title} ({self.scheduled_date} {self.start_time} - {self.end_time})"
