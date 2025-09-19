"""
URL configuration for projet project.
"""
from django.urls import path, include

urlpatterns = [
    path('api/', include('lending.urls')),
]
