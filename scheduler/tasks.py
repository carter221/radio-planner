from django.utils.timezone import localtime, now
from scheduler.models import Schedule
import os
import hashlib


# Chemin du fichier temporaire pour garder une trace de l'état
STATE_FILE = '/usr/src/app/media/last_program.state'


def get_last_program_state():
    """
    Récupère le hash du dernier programme enregistré dans le fichier d'état.
    """
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, 'r') as f:
            return f.read().strip()
    return None


def save_program_state(state):
    """
    Sauvegarde le hash du programme actuel dans le fichier d'état.
    """
    with open(STATE_FILE, 'w') as f:
        f.write(state)


def generate_liquidsoap_config():
    """
    Génère le fichier de configuration Liquidsoap uniquement si le programme actif change.
    """
    current_time = localtime().time()
    current_date = localtime().date()
    current_schedule = Schedule.objects.filter(
        scheduled_date=current_date,
        start_time__lte=current_time,
        end_time__gt=current_time
    ).first()

    config_path = '/usr/src/app/media/playlist.liq'  # Fichier de configuration Liquidsoap
    base_path = '/home/mediauser/songs/'  # Chemin des chansons

    if current_schedule and current_schedule.song.file_path:
        song_file_name = os.path.basename(current_schedule.song.file_path.name)
        absolute_song_path = os.path.join(base_path, song_file_name)

        config = f'{absolute_song_path}\n'
        program_identifier = absolute_song_path
    else:
        # Si aucun programme actif, utilisez une chanson par défaut
        config = '/home/mediauser/songs/song.mp3'
        program_identifier = "default"

    # Générer un hash unique pour le programme actuel
    current_program_hash = hashlib.md5(program_identifier.encode('utf-8')).hexdigest()

    # Charger le dernier état enregistré
    last_program_hash = get_last_program_state()

    # Si le programme n'a pas changé, ne rien faire
    if last_program_hash == current_program_hash:
        print("Le programme n'a pas changé. Aucun changement dans le fichier radio.liq.")
        return

    # Si le programme a changé, mettre à jour le fichier et sauvegarder l'état
    try:
        with open(config_path, 'w') as f:
            f.write(config)
        save_program_state(current_program_hash)
        print(f"Fichier {config_path} mis à jour avec succès.")
    except Exception as e:
        print(f"Erreur lors de la mise à jour de {config_path} : {e}")