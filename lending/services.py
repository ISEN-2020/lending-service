import requests
import logging
from django.conf import settings
from typing import Optional, Dict, Any

logger = logging.getLogger(__name__)

class MicroserviceClient:
    """Client de base pour communiquer avec les microservices"""
    
    def __init__(self, base_url: str, timeout: int = 30):
        self.base_url = base_url.rstrip('/')
        self.timeout = timeout
    
    def _make_request(self, method: str, endpoint: str, data: Optional[Dict] = None, params: Optional[Dict] = None) -> Optional[Dict[str, Any]]:
        """Effectue une requête HTTP vers le microservice"""
        url = f"{self.base_url}{endpoint}"
        
        try:
            response = requests.request(
                method=method,
                url=url,
                json=data,
                params=params,
                timeout=self.timeout,
                headers={'Content-Type': 'application/json'}
            )
            response.raise_for_status()
            return response.json() if response.content else None
        except requests.exceptions.Timeout:
            logger.error(f"Timeout lors de la requête vers {url}")
            return None
        except requests.exceptions.ConnectionError:
            logger.error(f"Erreur de connexion vers {url}")
            return None
        except requests.exceptions.HTTPError as e:
            logger.error(f"Erreur HTTP {e.response.status_code} vers {url}: {e.response.text}")
            return None
        except Exception as e:
            logger.error(f"Erreur inattendue lors de la requête vers {url}: {str(e)}")
            return None

class BookManagementService(MicroserviceClient):
    """Service pour communiquer avec le microservice Book Management"""
    
    def __init__(self):
        base_url = getattr(settings, 'BOOK_MANAGEMENT_URL', 'http://book-management-service:8001')
        super().__init__(base_url)
    
    def get_book_details(self, book_id: int) -> Optional[Dict[str, Any]]:
        """Récupère les détails d'un livre"""
        return self._make_request('GET', f'/getBooks/{book_id}')
    
    def check_book_availability(self, book_id: int) -> bool:
        """Vérifie si un livre est disponible pour emprunt"""
        book_details = self.get_book_details(book_id)
        if book_details:
            return book_details.get('available', False)
        return False
    
    def update_book_availability(self, book_id: int, available: bool) -> bool:
        """Met à jour la disponibilité d'un livre"""
        data = {'available': available}
        result = self._make_request('PUT', f'/updateBook/{book_id}', data=data)
        return result is not None

class UserManagementService(MicroserviceClient):
    """Service pour communiquer avec le microservice User Management"""
    
    def __init__(self):
        base_url = getattr(settings, 'USER_MANAGEMENT_URL', 'http://user-management-service:8002')
        super().__init__(base_url)
    
    def verify_user(self, user_email: str) -> bool:
        """Vérifie si l'utilisateur existe et est actif"""
        user_details = self._make_request('GET', f'/users/{user_email}')
        if user_details:
            return user_details.get('active', False)
        return False
    
    def get_user_details(self, user_email: str) -> Optional[Dict[str, Any]]:
        """Récupère les détails d'un utilisateur"""
        return self._make_request('GET', f'/users/{user_email}')

class NotificationService(MicroserviceClient):
    """Service pour communiquer avec le système de notification"""
    
    def __init__(self):
        base_url = getattr(settings, 'NOTIFICATION_SERVICE_URL', 'http://notification-service:8003')
        super().__init__(base_url)
    
    def send_lending_confirmation(self, user_email: str, book_title: str, due_date: str) -> bool:
        """Envoie une notification de confirmation d'emprunt"""
        data = {
            'user_email': user_email,
            'message_type': 'lending_confirmation',
            'book_title': book_title,
            'due_date': due_date
        }
        result = self._make_request('POST', '/send-notification', data=data)
        return result is not None
    
    def send_return_confirmation(self, user_email: str, book_title: str) -> bool:
        """Envoie une notification de confirmation de retour"""
        data = {
            'user_email': user_email,
            'message_type': 'return_confirmation',
            'book_title': book_title
        }
        result = self._make_request('POST', '/send-notification', data=data)
        return result is not None

# Instances globales des services
book_service = BookManagementService()
user_service = UserManagementService()
notification_service = NotificationService()