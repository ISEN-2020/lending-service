# Script CI/CD PowerShell pour SonarQube avec couverture de code
Write-Host "Lancement de l'analyse de qualite de code..." -ForegroundColor Green

# 1. Installer les dependances de test
Write-Host "Installation des dependances..." -ForegroundColor Blue
pip install coverage pytest pytest-cov pytest-django

# 2. Executer les tests avec couverture
Write-Host "Execution des tests avec couverture..." -ForegroundColor Blue
python -m coverage run --source=. --omit="*/venv/*,*/migrations/*,manage.py,check_compliance.py" -m unittest discover -s lending -p "test_*.py"

# 3. Generer le rapport XML pour SonarQube
Write-Host "Generation du rapport de couverture..." -ForegroundColor Blue
python -m coverage xml

# 4. Afficher les resultats
Write-Host "Resultats de couverture:" -ForegroundColor Yellow
python -m coverage report -m

# 5. Verifier si SonarQube Scanner est disponible
$sonarScanner = Get-Command sonar-scanner -ErrorAction SilentlyContinue
if ($sonarScanner) {
    Write-Host "Lancement de SonarQube Scanner..." -ForegroundColor Blue
    sonar-scanner `
        "-Dsonar.projectKey=ISEN-2020_lending-service" `
        "-Dsonar.organization=isen-2020" `
        "-Dsonar.sources=lending,projet" `
        "-Dsonar.exclusions=**/*test*/**,**/migrations/**,**/venv/**" `
        "-Dsonar.tests=lending" `
        "-Dsonar.test.inclusions=**/test_*.py" `
        "-Dsonar.python.coverage.reportPaths=coverage.xml" `
        "-Dsonar.host.url=https://sonarcloud.io"
} else {
    Write-Host "SonarQube Scanner non trouve. Veuillez l'installer pour l'analyse automatique." -ForegroundColor Yellow
    Write-Host "Vous pouvez telecharger SonarQube Scanner depuis: https://docs.sonarqube.org/latest/analysis/scan/sonarscanner/" -ForegroundColor Cyan
}

Write-Host "Analyse terminee !" -ForegroundColor Green

# Affichage d'un resume
Write-Host "`nRESUME:" -ForegroundColor Cyan
Write-Host "- Tests executes avec couverture" -ForegroundColor White
Write-Host "- Rapport XML genere pour SonarQube" -ForegroundColor White
Write-Host "- Fichier coverage.xml cree" -ForegroundColor White
if (Test-Path "coverage.xml") {
    Write-Host "- Rapport de couverture disponible" -ForegroundColor Green
} else {
    Write-Host "- Erreur lors de la generation du rapport" -ForegroundColor Red
}