from django.urls import path
from .views import create_lending, expired_lendings, lend_book, return_book, get_expired_books, health_check

urlpatterns = [
    # Health check pour Kubernetes
    path('health/', health_check, name='health_check'),
    
    # Nouveaux endpoints principaux selon l'architecture
    path('lendBook/', lend_book, name='lend_book'),
    path('returnBook/', return_book, name='return_book'),
    path('getExpiredBooks/', get_expired_books, name='get_expired_books'),
    
    # Endpoints existants maintenus pour compatibilité
    path('create-lending/', create_lending, name='create_lending'),
    path('expired-lendings/', expired_lendings, name='expired_lendings'),
]
