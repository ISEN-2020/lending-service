#!/bin/bash

# Script pour générer des certificats SSL auto-signés pour le développement
# NE PAS UTILISER EN PRODUCTION - Utiliser Let's Encrypt ou des certificats valides

echo "🔒 Génération des certificats SSL pour le développement..."

# Créer le répertoire SSL s'il n'existe pas
mkdir -p nginx/ssl

# Générer la clé privée
openssl genrsa -out nginx/ssl/nginx.key 2048

# Générer le certificat auto-signé
openssl req -new -x509 -key nginx/ssl/nginx.key -out nginx/ssl/nginx.crt -days 365 \
    -subj "/C=FR/ST=France/L=Paris/O=ISEN/OU=Lending Service/CN=localhost/emailAddress=admin@lending-service.local"

# Définir les bonnes permissions
chmod 600 nginx/ssl/nginx.key
chmod 644 nginx/ssl/nginx.crt

echo "✅ Certificats SSL générés avec succès !"
echo "📁 Fichiers créés :"
echo "   - nginx/ssl/nginx.key (clé privée)"
echo "   - nginx/ssl/nginx.crt (certificat)"
echo ""
echo "⚠️  ATTENTION: Ces certificats sont auto-signés et destinés au développement uniquement."
echo "📖 Pour la production, utilisez Let's Encrypt ou des certificats valides."