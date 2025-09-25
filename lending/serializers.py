from rest_framework import serializers
from .models import Lending

class LendingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lending
        fields = ['user_email', 'book_id']  # Inclure les champs nécessaires
