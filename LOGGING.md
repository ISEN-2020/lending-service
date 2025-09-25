# 📋 Guide de Gestion des Logs - Lending Management Service

## 🔍 Types de Logs

Le service génère plusieurs types de logs :

### 1. **Logs Applicatifs** (Module `lending`)
- **INFO** : Opérations normales (emprunts, retours)
- **WARNING** : Situations inhabituelles mais gérées
- **ERROR** : Erreurs de communication avec microservices
- **DEBUG** : Détails pour le débogage

### 2. **Logs Django** (Framework)
- Requêtes HTTP
- Erreurs de base de données
- Middleware et authentification

### 3. **Logs d'Infrastructure** (Kubernetes)
- Health checks
- Démarrage/arrêt des conteneurs
- Ressources système

## 📖 Comment Lire les Logs

### En Développement Local

```bash
# Logs en temps réel avec Docker Compose
docker-compose logs -f lending-service

# Logs des dernières 100 lignes
docker-compose logs --tail=100 lending-service

# Filtrer par niveau
docker-compose logs lending-service | grep ERROR
```

### En Production Kubernetes

```bash
# Logs en temps réel de tous les pods
kubectl logs -f deployment/lending-service -n library-system

# Logs d'un pod spécifique
kubectl logs -f <pod-name> -n library-system

# Logs des 1000 dernières lignes
kubectl logs --tail=1000 deployment/lending-service -n library-system

# Filtrer par niveau d'erreur
kubectl logs deployment/lending-service -n library-system | grep '"level": "ERROR"'

# Logs depuis une période
kubectl logs --since=1h deployment/lending-service -n library-system
```

## 🔧 Configuration des Logs

### Variables d'Environnement

```env
LOG_LEVEL=INFO          # DEBUG, INFO, WARNING, ERROR
DJANGO_DEBUG=False      # True pour plus de détails
```

### Niveaux de Log par Contexte

| Contexte | Niveau Recommandé | Description |
|----------|-------------------|-------------|
| Développement | DEBUG | Tous les détails |
| Staging | INFO | Opérations normales + erreurs |
| Production | WARNING | Uniquement problèmes et erreurs |

## 📊 Format des Logs

### Format JSON (Production)
```json
{
  "timestamp": "2024-01-15T10:30:00.123Z",
  "level": "INFO",
  "service": "lending-management",
  "module": "views",
  "message": "Book 123 lent to user@example.com",
  "process": 1,
  "thread": 140234567890
}
```

### Format Text (Développement)
```
INFO 2024-01-15 10:30:00,123 views 1 140234567890 Book 123 lent to user@example.com
```

## 🎯 Logs Importants à Surveiller

### ✅ **Succès d'Opérations**
```json
{"level": "INFO", "message": "Book lent successfully", "book_id": 123, "user_email": "user@example.com"}
```

### ⚠️ **Avertissements**
```json
{"level": "WARNING", "message": "Unable to send notification", "service": "notification"}
```

### ❌ **Erreurs Critiques**
```json
{"level": "ERROR", "message": "Database connection failed", "error": "connection timeout"}
```

## 🔍 Commandes de Diagnostic

### Vérifier la Santé du Service
```bash
# Health check
curl http://service-url:8000/health/

# Ou via Kubernetes
kubectl exec -it <pod-name> -n library-system -- curl localhost:8000/health/
```

### Analyser les Performances
```bash
# Requêtes les plus lentes
kubectl logs deployment/lending-service -n library-system | grep "slow_query"

# Erreurs de timeout
kubectl logs deployment/lending-service -n library-system | grep "timeout"

# Statut des microservices
kubectl logs deployment/lending-service -n library-system | grep "microservice_status"
```

## 📈 Monitoring et Alertes

### Métriques Clés à Surveiller

1. **Taux d'Erreur** : % de requêtes en erreur
2. **Latence** : Temps de réponse moyen
3. **Disponibilité** : Uptime du service
4. **Throughput** : Nombre de requêtes/sec

### Requêtes Utiles (Prometheus/Grafana)

```promql
# Taux d'erreur
rate(http_requests_total{status=~"5.."}[5m]) / rate(http_requests_total[5m])

# Latence P95
histogram_quantile(0.95, rate(http_request_duration_seconds_bucket[5m]))
```

## 🚨 Alertes Recommandées

### Alertes Critiques
- Taux d'erreur > 5%
- Latence P95 > 5s
- Service indisponible > 1min

### Alertes d'Avertissement
- Taux d'erreur > 1%
- Latence P95 > 2s
- Communications inter-services en échec

## 🛠️ Dépannage Courant

### Problème : Service ne démarre pas
```bash
# Vérifier les logs de démarrage
kubectl logs deployment/lending-service -n library-system --previous

# Vérifier la configuration
kubectl describe configmap lending-service-config -n library-system
```

### Problème : Erreurs de base de données
```bash
# Vérifier la connectivité
kubectl exec -it <pod-name> -n library-system -- python manage.py dbshell

# Logs spécifiques à la DB
kubectl logs deployment/lending-service -n library-system | grep "database"
```

### Problème : Communication inter-services
```bash
# Tester la connectivité réseau
kubectl exec -it <pod-name> -n library-system -- curl http://book-management-service:8001/health/

# Logs de communication
kubectl logs deployment/lending-service -n library-system | grep "microservice"
```

## 📁 Rotation et Archivage

### Configuration (Production)
- **Taille maximale par fichier** : 10MB
- **Nombre de fichiers** : 5 (50MB total)
- **Rotation** : Automatique quand taille atteinte

### Commandes d'Archivage
```bash
# Archiver les anciens logs
find /app/logs -name "*.log.*" -older-than 7d -exec gzip {} \;

# Nettoyer les logs trop anciens
find /app/logs -name "*.gz" -older-than 30d -delete
```

## 🔐 Sécurité des Logs

### Données Sensibles
- ❌ Ne jamais logger : mots de passe, tokens, données personnelles complètes
- ✅ Logger : IDs, emails (partiels), statuts, erreurs génériques

### Exemple Sécurisé
```python
# ❌ Mauvais
logger.info(f"User password: {password}")

# ✅ Bon  
logger.info(f"User authenticated: {email[:3]}***@{domain}")
```

## 📞 Support

En cas de problème avec les logs :
1. Vérifier le niveau de log configuré
2. S'assurer que le service a les permissions d'écriture
3. Vérifier l'espace disque disponible
4. Consulter la documentation Kubernetes pour les logs