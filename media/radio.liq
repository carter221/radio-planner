# Fichier de configuration temporaire
config_file = "/home/mediauser/playlist.liq"

# Fonction pour charger la configuration dynamiquement
def load_config()
  # Lire le contenu du fichier de configuration
  content = process.read.lines("cat " ^ config_file)
  if list.length(content) > 0 then
    # Retourner une liste de requêtes basées sur le contenu du fichier
    [request.create(list.hd(content))]
  else
    log("La configuration est vide ou inaccessible.")
    []
  end
end

# Source dynamique pour recharger la configuration
dynamic_config = mksafe(request.dynamic.list(load_config))

# Source en direct depuis Icecast
live = mksafe(fallback(track_sensitive=false, [input.http("http://radio.eglisecdau.com:8000/live"), dynamic_config]))

# Créer un fallback entre la source live et la source dynamique
radio = fallback(track_sensitive=false, [live, dynamic_config])

# Configurer la sortie vers Icecast
output.icecast(
  %mp3,
  host="radio.eglisecdau.com",
  port=8000,
  password="601Blaise@",
  mount="/stream",
  radio
)

# Activer le serveur Telnet
set("server.telnet", true)                   # Activer Telnet
set("server.telnet.bind_addr", "0.0.0.0")    # Autoriser toutes les adresses (utile dans un conteneur)
set("server.telnet.port", 1234)              # Définir le port (par défaut : 1234)
set("server.telnet.password", "pass")  # Définir un mot de passe
