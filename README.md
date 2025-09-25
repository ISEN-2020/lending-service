# Service de Gestion des Prêts - Lending Management

Ce microservice fait partie d'un système de bibliothèque distribué et gère les opérations d'emprunt et de retour de livres.

##  Architecture

Le service s'intègre dans une architecture microservices comprenant :
- **Book Management** : Gestion des livres et de leur disponibilité
- **User Management** : Gestion des utilisateurs
- **Notification System** : Envoi de notifications
- **Lending Management** : Gestion des prêts (ce service)

##  Fonctionnalités

### Endpoints Principaux

- `POST /lendBook/` - Emprunter un livre
- `POST /returnBook/` - Retourner un livre
- `GET /getExpiredBooks/` - Récupérer les livres en retard
- `GET /health/` - Vérification de santé du service

### Fonctionnalités Avancées

-  Communication inter-microservices via HTTP
-  Gestion des transactions pour la cohérence des données
-  Notifications automatiques lors des emprunts/retours
-  Suivi des livres en retard
-  Health checks pour Kubernetes
-  Logging structuré
-  Configuration via variables d'environnement

## Technologies Utilisées

- **Framework** : Django + Django REST Framework
- **Base de données** : SQLite (dev) / PostgreSQL (prod)
- **Containerisation** : Docker
- **Orchestration** : Kubernetes
- **Client HTTP** : Requests
- **Serveur WSGI** : Gunicorn

## Installation et Configuration

### Développement Local

1. **Cloner le repository**
```bash
git clone <repository-url>
cd lending-service-master
```

2. **Installation avec Docker Compose**
```bash
docker-compose up --build
```

3. **Installation manuelle**
```bash
# Créer un environnement virtuel
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate     # Windows

# Installer les dépendances
pip install -r requirements.txt

# Appliquer les migrations
python manage.py makemigrations
python manage.py migrate

# Lancer le serveur
python manage.py runserver
```

### Déploiement avec Kubernetes

1. **Construire l'image Docker**
```bash
docker build -t lending-service:latest .
```

2. **Déployer sur Kubernetes**
```bash
cd k8s
chmod +x deploy.sh
./deploy.sh
```

## Configuration

### Variables d'Environnement

| Variable | Description | Défaut |
|----------|-------------|--------|
| `DJANGO_SECRET_KEY` | Clé secrète Django | - |
| `DJANGO_DEBUG` | Mode debug | `True` |
| `DJANGO_ALLOWED_HOSTS` | Hôtes autorisés | `localhost,127.0.0.1` |
| `DATABASE_ENGINE` | Moteur de base de données | `django.db.backends.sqlite3` |
| `DATABASE_NAME` | Nom de la base de données | `db.sqlite3` |
| `DATABASE_USER` | Utilisateur de la base | - |
| `DATABASE_PASSWORD` | Mot de passe de la base | - |
| `DATABASE_HOST` | Hôte de la base | `localhost` |
| `DATABASE_PORT` | Port de la base | `5432` |
| `BOOK_MANAGEMENT_URL` | URL du service Book Management | `http://localhost:8001` |
| `USER_MANAGEMENT_URL` | URL du service User Management | `http://localhost:8002` |
| `NOTIFICATION_SERVICE_URL` | URL du service de notifications | `http://localhost:8003` |
| `LOG_LEVEL` | Niveau de log | `INFO` |

## API Documentation

### Emprunter un livre

```http
POST /lendBook/
Content-Type: application/json

{
    "user_email": "user@example.com",
    "book_id": 123
}
```

**Réponse :**
```json
{
    "id": 1,
    "user_email": "user@example.com",
    "book_id": 123,
    "date_borrowed": "2024-01-15T10:00:00Z",
    "date_due": "2024-03-15T10:00:00Z",
    "date_returned": null,
    "status": "ACTIVE"
}
```

### Retourner un livre

```http
POST /returnBook/
Content-Type: application/json

{
    "user_email": "user@example.com",
    "book_id": 123
}
```

### Récupérer les livres en retard

```http
GET /getExpiredBooks/
```

**Réponse :**
```json
[
    {
        "id": 1,
        "user_email": "user@example.com",
        "book_id": 123,
        "date_borrowed": "2023-11-15T10:00:00Z",
        "date_due": "2024-01-15T10:00:00Z",
        "date_returned": null,
        "status": "OVERDUE"
    }
]
```

## Communication Inter-Microservices

Le service communique avec :

### Book Management Service
- `GET /getBooks/{book_id}` - Récupérer les détails d'un livre
- `PUT /updateBook/{book_id}` - Mettre à jour la disponibilité

### User Management Service  
- `GET /users/{email}` - Vérifier l'existence et le statut d'un utilisateur

### Notification Service
- `POST /send-notification` - Envoyer des notifications par email

## Docker

### Dockerfile Optimisé

Le Dockerfile inclut :
- Image Python slim pour réduire la taille
- Utilisateur non-root pour la sécurité
- Health checks intégrés
- Support multi-stage (si nécessaire)

### Docker Compose

Le fichier `docker-compose.yml` inclut :
- Service principal lending-service
- Services mock pour le développement
- Réseau isolé
- Volumes persistants

## Kubernetes

### Ressources Déployées

- **ConfigMap** : Configuration non-sensible
- **Secret** : Informations sensibles (clés, mots de passe)
- **Deployment** : Déploiement de l'application avec 3 réplicas
- **Service** : Exposition interne du service
- **HPA** : Autoscaling horizontal basé sur CPU/mémoire
- **NetworkPolicy** : Sécurité réseau

### Monitoring et Health Checks

- **Liveness Probe** : Vérifie que le service répond
- **Readiness Probe** : Vérifie que le service est prêt
- **Startup Probe** : Vérifie le démarrage initial

## Logging

Les logs sont configurés avec plusieurs niveaux :
- **ERROR** : Erreurs critiques
- **WARNING** : Avertissements
- **INFO** : Informations générales
- **DEBUG** : Débogage détaillé

Les logs sont envoyés vers :
- Console (pour Kubernetes)
- Fichiers rotatifs (pour persistance)

## Sécurité

- Variables d'environnement pour les secrets
- Utilisateur non-root dans Docker
- NetworkPolicies Kubernetes pour l'isolation réseau
- HTTPS forcé en production
- Headers de sécurité configurés

## Tests

```bash
# Tests unitaires
python manage.py test

# Tests d'intégration avec Docker Compose
docker-compose -f docker-compose.test.yml up --abort-on-container-exit
```

## Déploiement en Production

1. **Construire l'image pour la production**
```bash
docker build -t lending-service:v1.0.0 .
docker tag lending-service:v1.0.0 your-registry/lending-service:v1.0.0
docker push your-registry/lending-service:v1.0.0
```

2. **Mettre à jour les manifestes Kubernetes**
```bash
# Éditer k8s/deployment.yaml pour changer l'image
sed -i 's/lending-service:latest/your-registry\/lending-service:v1.0.0/g' k8s/deployment.yaml
```

3. **Déployer**
```bash
./k8s/deploy.sh
```

## Monitoring

Le service expose des métriques pour :
- Prometheus (endpoint `/metrics` si configuré)
- Health checks (`/health/`)
- Logs structurés pour aggregation

## Contribution

1. Fork le projet
2. Créer une branche feature (`git checkout -b feature/AmazingFeature`)
3. Commit les changements (`git commit -m 'Add some AmazingFeature'`)
4. Push vers la branche (`git push origin feature/AmazingFeature`)
5. Ouvrir une Pull Request

## Licence

Ce projet est sous licence MIT. Voir le fichier `LICENSE` pour plus de détails.

Etape 3 : Créer la structure du projet

Etape 4 : Dockerisation
Création du dockerfile en fonction de notre projet.
Cela va permettre de conteneuriser notre appli

Etape 5 : Deploiement sur Kubernetes
Creation du fichier deployment.yaml pour déployer notre microservice sur Kubernetes

Etape 6 : Tests unitaires

Etape 7 : Documentation

    1. Deploiement de notre application:
Pour executer l'application...

    2. Configuration des variables d'environnement
Exemple de comment configurer la connexion de notre BDD

    3. Utilisation des endpoints API
Exemple de requete pour chaque endpoint


