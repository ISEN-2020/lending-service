from django.urls import path
from .views import create_lending, expired_lendings

urlpatterns = [
    path('create-lending/', create_lending, name='create_lending'),
    path('expired-lendings/', expired_lendings, name='expired_lendings'),
]
