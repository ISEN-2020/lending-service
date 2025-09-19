from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.utils import timezone
from django.db import transaction
import logging

from .models import Lending
from .serializers import LendingSerializer, LendBookSerializer, ReturnBookSerializer
from .services import book_service, user_service, notification_service
from .utils import get_book_title, handle_api_errors, NotificationHelper, update_book_availability_safe

logger = logging.getLogger(__name__)

@api_view(['POST'])
@handle_api_errors("la création du prêt")
def lend_book(request):
    """Endpoint pour emprunter un livre - /lendBook"""
    serializer = LendBookSerializer(data=request.data)
    
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    user_email = serializer.validated_data['user_email']
    book_id = serializer.validated_data['book_id']
    
    # Vérifier si l'utilisateur existe et est actif
    if not user_service.verify_user(user_email):
        return Response(
            {'error': 'Utilisateur non trouvé ou inactif'}, 
            status=status.HTTP_404_NOT_FOUND
        )
    
    # Vérifier si le livre existe et est disponible
    if not book_service.check_book_availability(book_id):
        return Response(
            {'error': 'Livre non disponible pour l\'emprunt'}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # Vérifier si l'utilisateur n'a pas déjà emprunté ce livre
    existing_lending = Lending.objects.filter(
        user_email=user_email, 
        book_id=book_id, 
        status='ACTIVE'
    ).exists()
    
    if existing_lending:
        return Response(
            {'error': 'Ce livre est déjà emprunté par cet utilisateur'}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # Transaction pour créer le prêt et marquer le livre comme indisponible
    with transaction.atomic():
        # Créer le prêt
        lending = Lending.objects.create(
            user_email=user_email,
            book_id=book_id,
            status='ACTIVE'
        )
        
        # Marquer le livre comme indisponible
        update_book_availability_safe(book_service, book_id, False)
    
    # Envoyer notification
    NotificationHelper.send_lending_notification(
        notification_service, book_service, user_email, book_id, lending.date_due
    )
    
    # Retourner les détails du prêt
    response_serializer = LendingSerializer(lending)
    return Response(response_serializer.data, status=status.HTTP_201_CREATED)

@api_view(['POST'])
@handle_api_errors("le retour du livre")
def return_book(request):
    """Endpoint pour retourner un livre - /returnBook"""
    serializer = ReturnBookSerializer(data=request.data)
    
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    user_email = serializer.validated_data['user_email']
    book_id = serializer.validated_data['book_id']
    
    # Trouver le prêt actif
    lending = Lending.objects.filter(
        user_email=user_email,
        book_id=book_id,
        status='ACTIVE'
    ).first()
    
    if not lending:
        return Response(
            {'error': 'Aucun prêt actif trouvé pour ce livre et cet utilisateur'}, 
            status=status.HTTP_404_NOT_FOUND
        )
    
    # Transaction pour marquer le prêt comme retourné et le livre comme disponible
    with transaction.atomic():
        # Marquer le prêt comme retourné
        lending.status = 'RETURNED'
        lending.date_returned = timezone.now()
        lending.save()
        
        # Marquer le livre comme disponible
        update_book_availability_safe(book_service, book_id, True)
    
    # Envoyer notification de retour
    NotificationHelper.send_return_notification(
        notification_service, book_service, user_email, book_id
    )
    
    # Retourner les détails du retour
    response_serializer = LendingSerializer(lending)
    return Response(response_serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
@handle_api_errors("la récupération des livres expirés")
def get_expired_books(request):
    """Endpoint pour récupérer les livres expirés - /getExpiredBooks"""
    now = timezone.now()
    expired_lendings = Lending.objects.filter(
        date_due__lt=now,
        status='ACTIVE'  # Seulement les prêts actifs
    ).order_by('date_due')
    
    # Marquer automatiquement comme en retard
    expired_lendings.update(status='OVERDUE')
    
    # Récupérer les objets mis à jour
    expired_lendings = Lending.objects.filter(
        date_due__lt=now,
        status='OVERDUE'
    ).order_by('date_due')
    
    serializer = LendingSerializer(expired_lendings, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['POST'])
def create_lending(request):
    """Endpoint existant maintenu pour compatibilité"""
    serializer = LendingSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def expired_lendings(request):
    """Endpoint existant maintenu pour compatibilité - redirige vers get_expired_books"""
    return get_expired_books(request)

@api_view(['GET'])
def health_check(request):
    """Endpoint de vérification de santé pour Kubernetes"""
    try:
        # Vérifier la connexion à la base de données
        from django.db import connection
        cursor = connection.cursor()
        cursor.execute("SELECT 1")
        cursor.fetchone()
        
        return Response({
            'status': 'healthy',
            'service': 'lending-management',
            'timestamp': timezone.now().isoformat()
        }, status=status.HTTP_200_OK)
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        return Response({
            'status': 'unhealthy',
            'service': 'lending-management',
            'timestamp': timezone.now().isoformat(),
            'error': str(e)
        }, status=status.HTTP_503_SERVICE_UNAVAILABLE)
