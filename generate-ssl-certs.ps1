# Script PowerShell pour générer des certificats SSL auto-signés
Write-Host "Generation des certificats SSL pour le developpement..." -ForegroundColor Green

# Créer le répertoire SSL
$sslDir = "nginx\ssl"
if (!(Test-Path $sslDir)) {
    New-Item -ItemType Directory -Path $sslDir -Force
    Write-Host "Repertoire $sslDir cree" -ForegroundColor Blue
}

# Vérifier si OpenSSL est disponible
$openssl = Get-Command openssl -ErrorAction SilentlyContinue
if (!$openssl) {
    Write-Host "OpenSSL n'est pas installe ou pas dans le PATH" -ForegroundColor Red
    Write-Host "Veuillez installer OpenSSL ou utiliser Git Bash" -ForegroundColor Yellow
    exit 1
}

# Générer avec OpenSSL
try {
    # Générer la clé privée
    & openssl genrsa -out "$sslDir\nginx.key" 2048
    
    # Générer le certificat auto-signé
    & openssl req -new -x509 -key "$sslDir\nginx.key" -out "$sslDir\nginx.crt" -days 365 -subj "/C=FR/ST=France/L=Paris/O=ISEN/OU=Lending Service/CN=localhost/emailAddress=admin@lending-service.local"
    
    Write-Host "Certificats SSL generes avec succes !" -ForegroundColor Green
    Write-Host "Fichiers crees :" -ForegroundColor Blue
    Write-Host "   - nginx\ssl\nginx.key (cle privee)" -ForegroundColor White
    Write-Host "   - nginx\ssl\nginx.crt (certificat)" -ForegroundColor White
    Write-Host "ATTENTION: Ces certificats sont auto-signes" -ForegroundColor Yellow
    
} catch {
    Write-Host "Erreur lors de la generation des certificats: $_" -ForegroundColor Red
}