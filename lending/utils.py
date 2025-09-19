"""
Utilitaires pour le service Lending Management
"""
import logging
from functools import wraps
from rest_framework import status
from rest_framework.response import Response

logger = logging.getLogger(__name__)


def get_book_title(book_service, book_id):
    """
    Récupère le titre d'un livre ou retourne un ID formaté
    
    Args:
        book_service: Service de gestion des livres
        book_id: ID du livre
    
    Returns:
        str: Titre du livre ou "Livre ID {book_id}"
    """
    book_details = book_service.get_book_details(book_id)
    return book_details.get('title', f'Livre ID {book_id}') if book_details else f'Livre ID {book_id}'


def handle_api_errors(operation_name):
    """
    Décorateur pour gérer les erreurs d'API de manière standardisée
    
    Args:
        operation_name: Nom de l'opération pour les logs
    
    Returns:
        Décorateur fonction
    """
    def decorator(func):
        @wraps(func)
        def wrapper(request, *args, **kwargs):
            try:
                return func(request, *args, **kwargs)
            except Exception as e:
                logger.error(f"Erreur lors de {operation_name}: {str(e)}")
                return Response(
                    {'error': 'Erreur interne du serveur'}, 
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
        return wrapper
    return decorator


class NotificationHelper:
    """
    Classe utilitaire pour gérer les notifications
    """
    
    @staticmethod
    def send_lending_notification(notification_service, book_service, user_email, book_id, date_due):
        """
        Envoie une notification de confirmation d'emprunt
        
        Args:
            notification_service: Service de notification
            book_service: Service de gestion des livres
            user_email: Email de l'utilisateur
            book_id: ID du livre
            date_due: Date d'échéance
        """
        try:
            book_title = get_book_title(book_service, book_id)
            notification_service.send_lending_confirmation(
                user_email, 
                book_title, 
                date_due.strftime('%Y-%m-%d')
            )
        except Exception as e:
            logger.warning(f"Impossible d'envoyer la notification d'emprunt: {str(e)}")
    
    @staticmethod
    def send_return_notification(notification_service, book_service, user_email, book_id):
        """
        Envoie une notification de confirmation de retour
        
        Args:
            notification_service: Service de notification
            book_service: Service de gestion des livres  
            user_email: Email de l'utilisateur
            book_id: ID du livre
        """
        try:
            book_title = get_book_title(book_service, book_id)
            notification_service.send_return_confirmation(user_email, book_title)
        except Exception as e:
            logger.warning(f"Impossible d'envoyer la notification de retour: {str(e)}")


def update_book_availability_safe(book_service, book_id, availability):
    """
    Met à jour la disponibilité d'un livre avec gestion d'erreur
    
    Args:
        book_service: Service de gestion des livres
        book_id: ID du livre
        availability: True pour disponible, False pour non disponible
        
    Returns:
        bool: True si succès, False sinon
    """
    try:
        result = book_service.update_book_availability(book_id, availability)
        if not result:
            status_text = "disponible" if availability else "indisponible"
            logger.warning(f"Impossible de marquer le livre {book_id} comme {status_text}")
        return result
    except Exception as e:
        logger.error(f"Erreur lors de la mise à jour de disponibilité du livre {book_id}: {str(e)}")
        return False