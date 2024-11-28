from django.utils.timezone import localtime
from scheduler.models import Schedule
import os

import logging

logger = logging.getLogger('django')
def generate_liquidsoap_config():
    print("La tâche est exécutée")
    try:
        # Log pour vérifier l'existence du fichier
        liquidsoap_path = '/usr/src/app/media/radio.liq'
        if not os.path.exists(liquidsoap_path):
            print(f"Fichier {liquidsoap_path} introuvable.")
            return

        # Log pour indiquer que l'écriture commence
        print("Écriture dans le fichier en cours...")
        with open(liquidsoap_path, 'w') as f:
            f.write("Test de mise à jour depuis Django Q\n")
        print(f"Fichier {liquidsoap_path} mis à jour avec succès.")
    except Exception as e:
        print(f"Erreur pendant la mise à jour du fichier : {e}")
    """
    Génère le fichier de configuration Liquidsoap en fonction du programme actif.
    Met à jour le fichier si nécessaire.
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

    if current_schedule and current_schedule.song.file_path:
        # Si un programme actif existe, créez la configuration appropriée
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
        print(f"Programme actif trouvé : {absolute_song_path}")

    # Écriture dans le fichier Liquidsoap
    try:
        with open(liquidsoap_path, 'w') as f:
            f.write(config)
        print(f"Fichier {liquidsoap_path} mis à jour avec succès.")
    except Exception as e:
        print(f"Erreur lors de la mise à jour de {liquidsoap_path} : {e}")
