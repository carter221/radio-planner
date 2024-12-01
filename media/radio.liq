# Fichier de playlist temporaire
playlist_file = "/home/mediauser/playlist.liq"

# Fonction pour charger la playlist dynamiquement
def load_playlist()
  # Lire le contenu du fichier de playlist
  content = process.read.lines("cat " ^ playlist_file)
  if list.length(content) > 0 then
    # Retourner une liste de requêtes basées sur le contenu du fichier
    [request.create(list.hd(content))]
  else
    log("La playlist est vide ou inaccessible.")
    []
  end
end

# Source dynamique pour recharger la playlist
dynamic_playlist = mksafe(request.dynamic.list(load_playlist))

# Configurer la sortie vers Icecast
output.icecast(
  %mp3,
  host="radio.eglisecdau.com",
  port=8000,
  password="601Blaise@",
  mount="/stream",
  dynamic_playlist
)
