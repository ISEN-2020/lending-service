from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta

# Fonction qui renvoie la date actuelle + 2 mois
def two_months_from_now():
    return timezone.now() + timedelta(days=60)  # Approximativement 2 mois

class Lending(models.Model):
    user_email = models.EmailField()  # Champ pour stocker l'adresse e-mail de l'utilisateur
    book_id = models.PositiveIntegerField()  # Assuming book_id is an integer. Adjust type if necessary.
    date_borrowed = models.DateTimeField(default=timezone.now)  # date d'emprunt
    date_due = models.DateTimeField(default=two_months_from_now)  # date d'échéance

    def __str__(self):
        return f"Lending {self.id} - User: {self.user_email}, Book ID: {self.book_id}"
