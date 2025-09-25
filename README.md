# Service de Gestion des Prêts de Bibliothèque 

## Guide d'Installation

### Prérequis
- Python 3.12+
- pip (gestionnaire de paquets Python)
- Docker (optionnel)
- PostgreSQL (production) / SQLite (développement)

### Installation Standard
```bash
# 1. Cloner le dépôt
git clone <repository-url>
cd lending-service-master

# 2. Créer un environnement virtuel
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
.\venv\Scripts\activate   # Windows

# 3. Installer les dépendances
pip install -r requirements.txt

# 4. Configurer l'environnement
cp .env.example .env
# Éditer .env avec vos configurations

# 5. Initialiser la base de données
python manage.py migrate

# 6. Lancer le serveur
python manage.py runserver
```

### Installation avec Docker
```bash
# Construction et lancement des conteneurs
docker-compose up --build
```

## API Reference

### 1. Gestion des Emprunts

#### Créer un nouvel emprunt
```http
POST /api/lendings/
Content-Type: application/json

{
    "user_email": "user@example.com",
    "book_id": 123,
    "due_date": "2024-02-01"
}
```

#### Lister tous les emprunts
```http
GET /api/lendings/
```

#### Détails d'un emprunt
```http
GET /api/lendings/{id}/
```

#### Retourner un livre
```http
PUT /api/lendings/{id}/return/
Content-Type: application/json

{
    "return_date": "2024-01-15",
    "condition": "good"
}
```

### 2. Gestion des Retards

#### Liste des emprunts en retard
```http
GET /api/lendings/overdue/
```

## Structure du Projet
```
lending-service/
├── lending/
│   ├── models.py          # Modèles de données
│   ├── views.py           # Vues et endpoints API
│   ├── services.py        # Logique métier
│   └── tests.py          # Tests unitaires
├── projet/               # Configuration Django
├── docker/              # Fichiers Docker
├── k8s/                 # Configs Kubernetes
└── mocks/               # Mocks pour tests
```

## Configuration

### Base de Données
Supports multiples bases de données :
- SQLite (développement)
- PostgreSQL (production recommandée)
- MySQL (supporté)

## Déploiement

### Docker
Le projet inclut un `Dockerfile` optimisé et un `docker-compose.yml` pour :
- Build multi-stage
- Mise en cache des dépendances
- Configuration production-ready

### Kubernetes
Fichiers de déploiement K8s disponibles dans `/k8s` :
- Deployments
- Services
- ConfigMaps
- Secrets
- HPA (Horizontal Pod Autoscaling)

## Tests et Qualité

### Tests Unitaires
```bash
# Lancer tous les tests
pytest

# Avec couverture de code
pytest --cov=lending
```

### Tests d'Intégration
```bash
# Tests avec bases de données
pytest tests/integration

# Tests avec services mockés
pytest tests/integration --use-mocks
```

### Qualité du Code
- Configuration SonarQube incluse
- Hooks pre-commit configurés
- Formatage automatique avec black

## Monitoring

- Métriques Prometheus : `/metrics/`
- Logs structurés (JSON)
- Traçage distribué avec OpenTelemetry

## Contribution
1. Forker le projet
2. Créer une branche (`git checkout -b feature/AmazingFeature`)
3. Commiter les changements (`git commit -m 'Add AmazingFeature'`)
4. Pusher la branche (`git push origin feature/AmazingFeature`)
5. Ouvrir une Pull Request

