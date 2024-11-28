from django.utils.timezone import localtime
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
    now = localtime().time()
    current_schedule = Schedule.objects.filter(
        start_time__lte=now,
        end_time__gt=now
    ).first()

    liquidsoap_path = '/usr/src/app/media/radio.liq'  # Fichier Liquidsoap
    base_path = '/home/mediauser/songs/'  # Chemin des chansons

    # Configuration par défaut (aucun programme actif)
    config = '''
    # Charger la chanson et la faire tourner en boucle manuellement
    backup = fallback([single("/home/mediauser/songs/song.mp3"), fallback([])])

    # Configurer la source en direct depuis Icecast
    live = mksafe(fallback(track_sensitive = false, [input.http("http://radio.eglisecdau.com:8000/live"), backup]))

    # Créer un fallback entre la source live et le backup
    radio = fallback(track_sensitive=false, [live, backup])

    # Configurer la sortie vers Icecast
    output.icecast(
    %mp3,
    host="radio.eglisecdau.com",
    port=8000,
    password="601Blaise@",
    mount="/stream",
    radio
    )
    '''

    # Si un programme actif existe, créez la configuration appropriée
    if current_schedule and current_schedule.song.file_path:
        song_file_name = os.path.basename(current_schedule.song.file_path.name)
        absolute_song_path = os.path.join(base_path, song_file_name)

        config = f'''
        # Charger la chanson et la faire tourner en boucle manuellement
        backup = fallback([single("{absolute_song_path}"), fallback([])])

        # Configurer la source en direct depuis Icecast
        live = mksafe(fallback(track_sensitive = false, [input.http("http://radio.eglisecdau.com:8000/live"), backup]))

        # Créer un fallback entre la source live et le backup
        radio = fallback(track_sensitive=false, [live, backup])

        # Configurer la sortie vers Icecast
        output.icecast(
        %mp3,
        host="radio.eglisecdau.com",
        port=8000,
        password="601Blaise@",
        mount="/stream",
        radio
        )
        '''
        program_identifier = absolute_song_path
    else:
        # Si aucun programme actif, utilisez une chaîne fixe
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
        with open(liquidsoap_path, 'w') as f:
            f.write(config)
        save_program_state(current_program_hash)
        print(f"Fichier {liquidsoap_path} mis à jour avec succès.")
    except Exception as e:
        print(f"Erreur lors de la mise à jour de {liquidsoap_path} : {e}")
