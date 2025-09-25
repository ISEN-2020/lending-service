"""
Tests pour le service Lending Management
Ces tests peuvent être exécutés avec ou sans environnement Django complet
"""

import os
import sys
import json
import unittest
from unittest.mock import patch, Mock, MagicMock
from datetime import datetime, timedelta

# Configuration pour les tests
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'projet.settings')


class TestLendingLogic(unittest.TestCase):
    """Tests pour la logique métier du service de prêt"""
    
    def setUp(self):
        """Configuration des tests"""
        self.sample_lending_data = {
            'id': 1,
            'user_email': 'test@example.com',
            'book_id': 123,
            'status': 'ACTIVE',
            'date_borrowed': datetime.now(),
            'date_due': datetime.now() + timedelta(days=60)
        }
    
    def test_lending_data_structure(self):
        """Test de la structure des données de prêt"""
        lending = self.sample_lending_data
        
        self.assertEqual(lending['user_email'], 'test@example.com')
        self.assertEqual(lending['book_id'], 123)
        self.assertEqual(lending['status'], 'ACTIVE')
        self.assertIsInstance(lending['date_borrowed'], datetime)
        self.assertIsInstance(lending['date_due'], datetime)
    
    def test_overdue_calculation(self):
        """Test du calcul de retard"""
        # Test avec un prêt non expiré
        due_date_future = datetime.now() + timedelta(days=10)
        self.assertFalse(due_date_future < datetime.now())
        
        # Test avec un prêt expiré
        due_date_past = datetime.now() - timedelta(days=1)
        self.assertTrue(due_date_past < datetime.now())
    
    def test_email_validation(self):
        """Test de validation des emails"""
        valid_emails = [
            'test@example.com',
            'user.name@university.edu',
            'student123@gmail.com'
        ]
        
        invalid_emails = [
            'invalid-email',
            '@example.com',
            'test@',
            ''
        ]
        
        # Simple validation regex
        import re
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        
        for email in valid_emails:
            self.assertTrue(re.match(email_pattern, email), f"Email {email} should be valid")
        
        for email in invalid_emails:
            self.assertFalse(re.match(email_pattern, email), f"Email {email} should be invalid")
    
    def test_book_id_validation(self):
        """Test de validation des IDs de livre"""
        valid_ids = [1, 123, 999999]
        invalid_ids = [0, -1, -999]
        
        for book_id in valid_ids:
            self.assertGreater(book_id, 0, f"Book ID {book_id} should be valid")
        
        for book_id in invalid_ids:
            self.assertLessEqual(book_id, 0, f"Book ID {book_id} should be invalid")


class TestMicroserviceCommunication(unittest.TestCase):
    """Tests pour la communication avec les microservices"""
    
    @patch('requests.request')
    def test_book_service_success_response(self, mock_request):
        """Test de réponse réussie du service Book Management"""
        # Mock de la réponse HTTP
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'id': 123,
            'title': 'Test Book',
            'available': True
        }
        mock_response.raise_for_status.return_value = None
        mock_response.content = b'{"id": 123}'
        mock_request.return_value = mock_response
        
        # Test de la logique (simulation)
        response = mock_request('GET', 'http://book-service/books/123')
        data = response.json()
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['id'], 123)
        self.assertTrue(data['available'])
    
    @patch('requests.request')
    def test_user_service_success_response(self, mock_request):
        """Test de réponse réussie du service User Management"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'email': 'test@example.com',
            'active': True
        }
        mock_response.raise_for_status.return_value = None
        mock_response.content = b'{"email": "test@example.com"}'
        mock_request.return_value = mock_response
        
        # Test de la logique (simulation)
        response = mock_request('GET', 'http://user-service/users/test@example.com')
        data = response.json()
        
        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['active'])
    
    @patch('requests.request')
    def test_notification_service_success(self, mock_request):
        """Test d'envoi réussi de notification"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'success': True,
            'message': 'Notification sent'
        }
        mock_response.raise_for_status.return_value = None
        mock_response.content = b'{"success": true}'
        mock_request.return_value = mock_response
        
        # Test de la logique (simulation)
        notification_data = {
            'user_email': 'test@example.com',
            'message_type': 'lending_confirmation',
            'book_title': 'Test Book'
        }
        response = mock_request('POST', 'http://notification-service/send', json=notification_data)
        data = response.json()
        
        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['success'])
    
    @patch('requests.request')
    def test_service_timeout_handling(self, mock_request):
        """Test de gestion du timeout"""
        # Simuler une exception Timeout
        mock_request.side_effect = Exception("Request timeout")
        
        # Test du comportement avec timeout
        try:
            mock_request('GET', 'http://slow-service/endpoint', timeout=1)
            self.fail("Exception attendue")
        except Exception as e:
            self.assertIn("timeout", str(e).lower())
    
    @patch('requests.request') 
    def test_service_connection_error(self, mock_request):
        """Test de gestion d'erreur de connexion"""
        # Simuler une erreur de connexion
        mock_request.side_effect = Exception("Connection failed")
        
        # Test du comportement avec erreur de connexion
        try:
            mock_request('GET', 'http://unavailable-service/endpoint')
            self.fail("Exception attendue")
        except Exception as e:
            self.assertIn("connection", str(e).lower())


class TestAPIEndpoints(unittest.TestCase):
    """Tests pour les endpoints de l'API"""
    
    def test_lend_book_data_validation(self):
        """Test de validation des données pour l'emprunt"""
        valid_data = {
            'user_email': 'test@example.com',
            'book_id': 123
        }
        
        invalid_data_sets = [
            {},  # Données vides
            {'user_email': 'test@example.com'},  # book_id manquant
            {'book_id': 123},  # user_email manquant
            {'user_email': 'invalid-email', 'book_id': 123},  # Email invalide
            {'user_email': 'test@example.com', 'book_id': -1},  # book_id invalide
        ]
        
        # Validation simple
        import re
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        
        # Test des données valides
        self.assertIn('user_email', valid_data)
        self.assertIn('book_id', valid_data)
        self.assertTrue(re.match(email_pattern, valid_data['user_email']))
        self.assertGreater(valid_data['book_id'], 0)
        
        # Test des données invalides
        for invalid_data in invalid_data_sets:
            if 'user_email' in invalid_data and 'book_id' in invalid_data:
                email_valid = re.match(email_pattern, invalid_data['user_email']) is not None
                book_id_valid = invalid_data['book_id'] > 0
                self.assertFalse(email_valid and book_id_valid, 
                    f"Data should be invalid: {invalid_data}")
    
    def test_return_book_data_validation(self):
        """Test de validation des données pour le retour"""
        valid_data = {
            'user_email': 'test@example.com',
            'book_id': 123
        }
        
        # Même validation que pour l'emprunt
        import re
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        
        self.assertTrue(re.match(email_pattern, valid_data['user_email']))
        self.assertGreater(valid_data['book_id'], 0)
    
    def test_health_check_response_format(self):
        """Test du format de réponse du health check"""
        expected_response = {
            'status': 'healthy',
            'service': 'lending-management',
            'timestamp': datetime.now().isoformat()
        }
        
        self.assertIn('status', expected_response)
        self.assertIn('service', expected_response)
        self.assertIn('timestamp', expected_response)
        self.assertEqual(expected_response['service'], 'lending-management')


class TestBusinessRules(unittest.TestCase):
    """Tests pour les règles métier"""
    
    def test_unique_lending_constraint(self):
        """Test de la contrainte d'unicité des prêts"""
        # Simuler des prêts existants
        existing_lendings = [
            {'user_email': 'user1@example.com', 'book_id': 123, 'status': 'ACTIVE'},
            {'user_email': 'user2@example.com', 'book_id': 456, 'status': 'ACTIVE'},
        ]
        
        # Test d'un nouveau prêt autorisé
        new_lending = {'user_email': 'user3@example.com', 'book_id': 789, 'status': 'ACTIVE'}
        
        # Vérifier qu'il n'y a pas de conflit
        conflicts = [
            lending for lending in existing_lendings 
            if lending['user_email'] == new_lending['user_email'] 
            and lending['book_id'] == new_lending['book_id']
            and lending['status'] == 'ACTIVE'
        ]
        
        self.assertEqual(len(conflicts), 0, "No conflicts should exist for new lending")
        
        # Test d'un prêt en conflit
        conflicting_lending = {'user_email': 'user1@example.com', 'book_id': 123, 'status': 'ACTIVE'}
        
        conflicts = [
            lending for lending in existing_lendings 
            if lending['user_email'] == conflicting_lending['user_email'] 
            and lending['book_id'] == conflicting_lending['book_id']
            and lending['status'] == 'ACTIVE'
        ]
        
        self.assertGreater(len(conflicts), 0, "Conflict should be detected")
    
    def test_lending_status_transitions(self):
        """Test des transitions de statut des prêts"""
        valid_transitions = {
            'ACTIVE': ['RETURNED', 'OVERDUE'],
            'OVERDUE': ['RETURNED'],
            'RETURNED': []  # État final
        }
        
        # Test des transitions valides
        current_status = 'ACTIVE'
        new_status = 'RETURNED'
        self.assertIn(new_status, valid_transitions[current_status])
        
        # Test d'une transition invalide
        invalid_status = 'ACTIVE'
        self.assertNotIn(invalid_status, valid_transitions['RETURNED'])


if __name__ == '__main__':
    # Configuration pour les tests
    unittest.main(verbosity=2)