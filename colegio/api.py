from .models import Persona
from rest_framework import viewsets, permissions
from .serializer import PersonaSerializer  # Import the specific serializer

class ProyectoVistas(viewsets.ModelViewSet):
    queryset = Persona.objects.all()
    permission_classes = [permissions.AllowAny]  # Fixed typo and correct attribute name
    serializer_class = PersonaSerializer  # Use the actual serializer class