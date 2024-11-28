
        # Charger la chanson et la faire tourner en boucle manuellement
        backup = fallback([single("/home/mediauser/songs/Deborah_LUKALU_-_TU_ES_LE_PAPA_LE_PLUS_RESPONSABLE_AliB51S.wav"), fallback([])])

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
        