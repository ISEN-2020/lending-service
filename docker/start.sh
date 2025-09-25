#!/bin/bash

# Script de démarrage pour le conteneur avec Nginx + Django
set -e

echo "🚀 Démarrage du service Lending Management avec Nginx + HTTPS..."

# Générer les certificats SSL s'ils n'existent pas
if [ ! -f "/etc/nginx/ssl/nginx.crt" ] || [ ! -f "/etc/nginx/ssl/nginx.key" ]; then
    echo "🔒 Génération des certificats SSL auto-signés..."
    mkdir -p /etc/nginx/ssl
    
    openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
        -keyout /etc/nginx/ssl/nginx.key \
        -out /etc/nginx/ssl/nginx.crt \
        -subj "/C=FR/ST=France/L=Paris/O=ISEN/OU=Lending Service/CN=localhost"
    
    echo "✅ Certificats SSL générés"
fi

# Collecter les fichiers statiques Django
echo "📦 Collection des fichiers statiques..."
python manage.py collectstatic --noinput --clear

# Appliquer les migrations
echo "🔄 Application des migrations Django..."
python manage.py migrate --noinput

# Démarrer supervisor
echo "▶️  Démarrage de Supervisor (Nginx + Gunicorn)..."
exec /usr/bin/supervisord -c /etc/supervisor/conf.d/supervisord.conf