from rest_framework import serializers
from .models import Lending

class LendingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lending
        fields = ['id', 'user_email', 'book_id', 'date_borrowed', 'date_due', 'date_returned', 'status']
        read_only_fields = ['id', 'date_borrowed']

class LendBookSerializer(serializers.Serializer):
    """Serializer pour l'endpoint lendBook"""
    user_email = serializers.EmailField()
    book_id = serializers.IntegerField(min_value=1)

class ReturnBookSerializer(serializers.Serializer):
    """Serializer pour l'endpoint returnBook"""
    user_email = serializers.EmailField()
    book_id = serializers.IntegerField(min_value=1)
