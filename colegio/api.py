# colegio/api.py
from .models import (
    Pais, Rol, Persona, RolPersona, Unidad, AreaSocial,
    Restriccion, RestriccionArea, Reserva, Incumplimiento, Pagos, Visita
)

from rest_framework import viewsets, permissions
from .serializer import (  # Cambié "serializer" por "serializers" (más común)
    PaisSerializer, RolSerializer, PersonaSerializer, RolPersonaSerializer, 
    UnidadSerializer, AreaSocialSerializer,
    RestriccionSerializer, RestriccionAreaSerializer, ReservaSerializer, 
    IncumplimientoSerializer, PagosSerializer, VisitaSerializer
)  # Corregí los nombres de las clases del serializer

class PaisViewSet(viewsets.ModelViewSet):  # Cambié el nombre por claridad
    queryset = Pais.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = PaisSerializer

# Debes crear ViewSets para todos tus modelos, por ejemplo:
class RolViewSet(viewsets.ModelViewSet):
    queryset = Rol.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = RolSerializer

class PersonaViewSet(viewsets.ModelViewSet):
    queryset = Persona.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = PersonaSerializer

class RolPersonaViewSet(viewsets.ModelViewSet):
    queryset = RolPersona.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = RolPersonaSerializer


class UnidadViewSet(viewsets.ModelViewSet):
    queryset = Unidad.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = UnidadSerializer

class AreaSocialViewSet(viewsets.ModelViewSet):
    queryset = AreaSocial.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = AreaSocialSerializer

class RestriccionViewSet(viewsets.ModelViewSet):
    queryset = Restriccion.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = RestriccionSerializer

class RestriccionAreaViewSet(viewsets.ModelViewSet):
    queryset = RestriccionArea.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = RestriccionAreaSerializer

class ReservaViewSet(viewsets.ModelViewSet):
    queryset = Reserva.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = ReservaSerializer

class IncumplimientoViewSet(viewsets.ModelViewSet):
    queryset = Incumplimiento.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = IncumplimientoSerializer

class PagosViewSet(viewsets.ModelViewSet):
    queryset = Pagos.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = PagosSerializer

class VisitaViewSet(viewsets.ModelViewSet):
    queryset = Visita.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = VisitaSerializer