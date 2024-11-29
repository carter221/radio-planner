# Utiliser une image légère de Python
FROM python:3.10-slim

# Installer les dépendances système, y compris cron et supervisor
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    cron \
    supervisor

# Définir le dossier de travail
WORKDIR /usr/src/app

# Copier le code de l'application
COPY . /usr/src/app

# Installer les dépendances Python
RUN pip install --no-cache-dir -r requirements.txt

# Créer un dossier pour les fichiers médias
VOLUME /usr/src/app/media

# Ajouter le fichier cron
COPY django-cron /etc/cron.d/django-cron

# Donner les permissions correctes au fichier cron
RUN chmod 0644 /etc/cron.d/django-cron

# Installer la crontab
RUN crontab /etc/cron.d/django-cron

# Créer un fichier de log pour cron
RUN touch /var/log/cron.log

# Copier le fichier de configuration de supervisor
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

# Exposer le port 3000
EXPOSE 3000

# Commande pour démarrer supervisor
CMD ["/usr/bin/supervisord"]