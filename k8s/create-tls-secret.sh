#!/bin/bash

# Script pour créer le secret TLS dans Kubernetes
# À exécuter après avoir généré les certificats SSL

echo "🔒 Création du secret TLS pour Kubernetes..."

# Vérifier que les certificats existent
if [ ! -f "nginx/ssl/nginx.crt" ] || [ ! -f "nginx/ssl/nginx.key" ]; then
    echo "❌ Certificats SSL non trouvés. Exécutez d'abord ./generate-ssl-certs.sh"
    exit 1
fi

# Créer le namespace s'il n'existe pas
kubectl create namespace library-system --dry-run=client -o yaml | kubectl apply -f -

# Créer le secret TLS
kubectl create secret tls lending-service-tls-secret \
    --cert=nginx/ssl/nginx.crt \
    --key=nginx/ssl/nginx.key \
    --namespace=library-system \
    --dry-run=client -o yaml | kubectl apply -f -

echo "✅ Secret TLS créé avec succès !"
echo "📋 Vérification :"
kubectl get secret lending-service-tls-secret -n library-system