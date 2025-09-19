# Utiliser une image Python officielle avec Nginx
FROM python:3.12.5-slim

# Définir les variables d'environnement
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV DJANGO_SETTINGS_MODULE=projet.settings

# Définir le répertoire de travail
WORKDIR /app

# Installer les dépendances système including Nginx
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        postgresql-client \
        nginx \
        supervisor \
        gettext \
    && rm -rf /var/lib/apt/lists/*

# Copier et installer les dépendances Python
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt \
    && pip install --no-cache-dir gunicorn

# Copier le code de l'application
COPY . .

# Copier la configuration Nginx
COPY nginx/nginx.conf /etc/nginx/sites-available/default
RUN rm -f /etc/nginx/sites-enabled/default \
    && ln -s /etc/nginx/sites-available/default /etc/nginx/sites-enabled/

# Créer les répertoires nécessaires
RUN mkdir -p /var/log/nginx /app/static /app/media /etc/nginx/ssl

# Copier les certificats SSL (si ils existent)
COPY nginx/ssl/ /etc/nginx/ssl/

# Copier la configuration supervisor
COPY docker/supervisord.conf /etc/supervisor/conf.d/supervisord.conf

# Créer un utilisateur non-root
RUN adduser --disabled-password --gecos '' appuser \
    && chown -R appuser:appuser /app \
    && chown -R appuser:appuser /var/log/nginx \
    && mkdir -p /var/log/supervisor \
    && chown -R appuser:appuser /var/log/supervisor

# Script de démarrage
COPY docker/start.sh /start.sh
RUN chmod +x /start.sh

# Changer vers l'utilisateur non-root pour les services applicatifs
# Note: Supervisor et Nginx ont besoin de root pour certaines opérations
USER root

# Exposer les ports HTTP et HTTPS
EXPOSE 80 443

# Script de santé pour HTTPS
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f -k https://localhost/health/ || curl -f http://localhost/health/ || exit 1

# Commande de démarrage avec Supervisor
CMD ["/usr/bin/supervisord", "-c", "/etc/supervisor/conf.d/supervisord.conf"]
