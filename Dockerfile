FROM python:3.12.5

WORKDIR /app

# Installer les dépendances Python
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copier le code de l'application
COPY . .

EXPOSE 8000

# Lancer les migrations puis le serveur
CMD ["sh", "-c", "python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]
