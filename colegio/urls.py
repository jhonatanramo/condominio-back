# colegio/urls.py
from django.urls import path, include
from rest_framework import routers
from .api import (
    PaisViewSet, RolViewSet, PersonaViewSet, RolPersonaViewSet,
    CondominioViewSet, UnidadViewSet, AreaSocialViewSet,
    RestriccionViewSet, RestriccionAreaViewSet, ReservaViewSet,
    IncumplimientoViewSet, PagosViewSet, VisitaViewSet
)

router = routers.DefaultRouter()

# Registrar CADA ViewSet con su ruta correspondiente
router.register(r'paises', PaisViewSet)
router.register(r'roles', RolViewSet)
router.register(r'personas', PersonaViewSet)
router.register(r'rol-personas', RolPersonaViewSet)
router.register(r'condominios', CondominioViewSet)
router.register(r'unidades', UnidadViewSet)
router.register(r'areas-sociales', AreaSocialViewSet)
router.register(r'restricciones', RestriccionViewSet)
router.register(r'restriccion-areas', RestriccionAreaViewSet)
router.register(r'reservas', ReservaViewSet)
router.register(r'incumplimientos', IncumplimientoViewSet)
router.register(r'pagos', PagosViewSet)
router.register(r'visitas', VisitaViewSet)

urlpatterns = [
    path('', include(router.urls)),  # Todas las rutas empezarán con /api/
]