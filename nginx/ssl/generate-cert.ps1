# Générer un certificat auto-signé pour développement
$cert = New-SelfSignedCertificate -DnsName "localhost", "127.0.0.1" -CertStoreLocation "cert:\CurrentUser\My" -NotAfter (Get-Date).AddYears(1) -KeyAlgorithm RSA -KeyLength 2048

# Exporter le certificat (.crt)
$certPath = Join-Path -Path $PSScriptRoot -ChildPath "nginx.crt"
Export-Certificate -Cert $cert -FilePath $certPath -Type CERT

# Exporter la clé privée (.key) - Nécessite une conversion
$keyPath = Join-Path -Path $PSScriptRoot -ChildPath "nginx.key"

# Exporter le certificat avec clé privée au format PFX temporaire
$pfxPath = Join-Path -Path $PSScriptRoot -ChildPath "temp.pfx"
$password = ConvertTo-SecureString -String "temp123" -Force -AsPlainText
Export-PfxCertificate -Cert $cert -FilePath $pfxPath -Password $password

Write-Host "Certificat créé: $certPath"
Write-Host "Pour la clé privée, utilisez Docker avec OpenSSL à l'intérieur"
Write-Host "Fichier PFX temporaire créé: $pfxPath (mot de passe: temp123)"

# Instructions pour extraire la clé avec Docker
Write-Host ""
Write-Host "Pour extraire la clé privée, exécutez:"
Write-Host "docker run --rm -v ${PWD}:/work -w /work alpine/openssl pkcs12 -in temp.pfx -out nginx.key -nodes -nocerts -passin pass:temp123"