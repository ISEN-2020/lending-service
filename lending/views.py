from django.shortcuts import render

# Create your views here.
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Lending
from .serializers import LendingSerializer
from django.utils import timezone


@api_view(['POST'])
def create_lending(request):
    serializer = LendingSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    # Log des erreurs de validation pour faciliter le debug
    print("[create_lending] validation errors:", serializer.errors)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def expired_lendings(request):
    now = timezone.now()
    expired_lendings = Lending.objects.filter(date_due__lt=now)  # Filtrer tous les objets où la date_due est passée
    serializer = LendingSerializer(expired_lendings, many=True)  # Sérialiser les objets filtrés
    return Response(serializer.data)  # Retourner la liste des objets sérialisés


@api_view(['GET'])
def user_borrowings(request):
    user_email = request.query_params.get('user_email')
    if not user_email:
        return Response({'error': 'Le paramètre user_email est requis'}, status=status.HTTP_400_BAD_REQUEST)
    borrowings = Lending.objects.filter(user_email=user_email).order_by('-date_borrowed')
    serializer = LendingSerializer(borrowings, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)
