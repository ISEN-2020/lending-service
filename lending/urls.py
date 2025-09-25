from django.urls import path
from .views import lend_book, return_book, get_expired_books, health_check

urlpatterns = [
    # Health check pour Kubernetes
    path('health/', health_check, name='health_check'),
    
    # Endpoints principaux de l'API
    path('lendBook/', lend_book, name='lend_book'),
    path('returnBook/', return_book, name='return_book'),
    path('getExpiredBooks/', get_expired_books, name='get_expired_books'),
]
