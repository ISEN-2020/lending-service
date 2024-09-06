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
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def expired_lendings(request):
    now = timezone.now()
    expired_lendings = Lending.objects.filter(date_due__lt=now)  # Filtrer tous les objets où la date_due est passée
    serializer = LendingSerializer(expired_lendings, many=True)  # Sérialiser les objets filtrés
    return Response(serializer.data)  # Retourner la liste des objets sérialisés
