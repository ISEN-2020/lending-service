#!/bin/bash

# Script CI/CD pour SonarQube avec couverture de code
echo "🚀 Lancement de l'analyse de qualité de code..."

# 1. Installer les dépendances de test
echo "📦 Installation des dépendances..."
pip install -r requirements.txt
pip install coverage pytest pytest-cov pytest-django

# 2. Exécuter les tests avec couverture
echo "🧪 Exécution des tests avec couverture..."
python -m coverage run --source=. --omit="*/venv/*,*/migrations/*,manage.py,check_compliance.py" -m unittest discover -s lending -p "test_*.py" -v

# 3. Générer le rapport XML pour SonarQube
echo "📊 Génération du rapport de couverture..."
python -m coverage xml

# 4. Afficher les résultats
echo "📈 Résultats de couverture:"
python -m coverage report -m

# 5. Lancer SonarQube Scanner (si disponible)
if command -v sonar-scanner &> /dev/null; then
    echo "🔍 Lancement de SonarQube Scanner..."
    sonar-scanner \
        -Dsonar.projectKey=ISEN-2020_lending-service \
        -Dsonar.organization=isen-2020 \
        -Dsonar.sources=lending,projet \
        -Dsonar.exclusions="**/*test*/**,**/migrations/**,**/venv/**" \
        -Dsonar.tests=lending \
        -Dsonar.test.inclusions="**/test_*.py" \
        -Dsonar.python.coverage.reportPaths=coverage.xml \
        -Dsonar.host.url=https://sonarcloud.io
else
    echo "⚠️ SonarQube Scanner non trouvé. Veuillez l'installer pour l'analyse automatique."
fi

echo "✅ Analyse terminée !"