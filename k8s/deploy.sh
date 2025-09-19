#!/bin/bash

# Script de déploiement pour le service Lending Management
# Ce script déploie tous les composants Kubernetes nécessaires

set -e

echo "🚀 Déploiement du service Lending Management..."

# Variables
NAMESPACE="library-system"
IMAGE_TAG="${IMAGE_TAG:-latest}"

# Créer le namespace s'il n'existe pas
echo "📁 Création du namespace $NAMESPACE..."
kubectl create namespace $NAMESPACE --dry-run=client -o yaml | kubectl apply -f -

# Labeliser le namespace pour les NetworkPolicies
kubectl label namespace $NAMESPACE name=$NAMESPACE --overwrite

# Déployer les ressources dans l'ordre
echo "📋 Déploiement du ConfigMap..."
kubectl apply -f configmap.yaml

echo "🔐 Déploiement du Secret..."
kubectl apply -f secret.yaml

echo "🌐 Déploiement des NetworkPolicies..."
kubectl apply -f networkpolicy.yaml

echo "🚢 Déploiement du Service..."
kubectl apply -f service.yaml

echo "🖥️  Déploiement du Deployment..."
kubectl apply -f deployment.yaml

echo "📈 Déploiement du HPA..."
kubectl apply -f hpa.yaml

# Attendre que le déploiement soit prêt
echo "⏳ Attente que le déploiement soit prêt..."
kubectl rollout status deployment/lending-service -n $NAMESPACE --timeout=300s

# Vérifier la santé du service
echo "🏥 Vérification de la santé du service..."
kubectl wait --for=condition=ready pod -l app=lending-service -n $NAMESPACE --timeout=120s

echo "✅ Déploiement terminé avec succès!"

# Afficher l'état des ressources
echo ""
echo "📊 État des ressources déployées:"
kubectl get all -l app=lending-service -n $NAMESPACE

# Afficher les logs des pods
echo ""
echo "📝 Derniers logs:"
kubectl logs -l app=lending-service -n $NAMESPACE --tail=10