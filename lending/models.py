from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta

# Fonction qui renvoie la date actuelle + 2 mois
def two_months_from_now():
    return timezone.now() + timedelta(days=60)  # Approximativement 2 mois

class Lending(models.Model):
    STATUS_CHOICES = [
        ('ACTIVE', 'Active'),
        ('RETURNED', 'Returned'),
        ('OVERDUE', 'Overdue'),
    ]
    
    user_email = models.EmailField()  # Champ pour stocker l'adresse e-mail de l'utilisateur
    book_id = models.PositiveIntegerField()  # ID du livre dans le microservice Book Management
    date_borrowed = models.DateTimeField(default=timezone.now)  # date d'emprunt
    date_due = models.DateTimeField(default=two_months_from_now)  # date d'échéance
    date_returned = models.DateTimeField(null=True, blank=True)  # date de retour
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='ACTIVE')
    
    class Meta:
        # Empêcher qu'un utilisateur emprunte plusieurs fois le même livre
        unique_together = [['user_email', 'book_id', 'status']]
        indexes = [
            models.Index(fields=['status']),
            models.Index(fields=['date_due']),
            models.Index(fields=['user_email']),
        ]

    def __str__(self):
        return f"Lending {self.id} - User: {self.user_email}, Book ID: {self.book_id}, Status: {self.status}"
    
    def is_overdue(self):
        """Vérifie si le prêt est en retard"""
        if self.status == 'ACTIVE' and self.date_due < timezone.now():
            return True
        return False
