from django.urls import path, include
from rest_framework import routers
from .logica.login import login
from .logica.condominio import condominio
from .logica.agendavisita import visita, reserva
from .logica.Reporte import Reporte
from .logica.crear_unidad import crear_unidad
from .logica.agendareserva import Reserva

from .logica.crearReserva import crear_R

from .views import create_payment
from . import views


from .api import (
    PaisViewSet, RolViewSet, PersonaViewSet, RolPersonaViewSet,
    UnidadViewSet, AreaSocialViewSet,
    RestriccionViewSet, RestriccionAreaViewSet, ReservaViewSet,
    IncumplimientoViewSet, PagosViewSet, VisitaViewSet
)

router = routers.DefaultRouter()

# Registrar ViewSets...
router.register(r'paises', PaisViewSet)
router.register(r'roles', RolViewSet)
router.register(r'personas', PersonaViewSet)
router.register(r'rol-personas', RolPersonaViewSet)
router.register(r'unidades', UnidadViewSet)
router.register(r'areas-sociales', AreaSocialViewSet)
router.register(r'restricciones', RestriccionViewSet)
router.register(r'restriccion-areas', RestriccionAreaViewSet)
router.register(r'reservas', ReservaViewSet)
router.register(r'incumplimientos', IncumplimientoViewSet)
router.register(r'pagos', PagosViewSet)
router.register(r'visitas', VisitaViewSet)

urlpatterns = [
    path('data/', include(router.urls)),
    path('login/', login, name='procesar_login'),
    path('usuario/crear/', condominio, name='condominio_crear_usuario'),  
    path('agenda/visita/', visita, name='visita'),
    path('agenda/reserva/', reserva, name='reserva'),

    path('agenda/reserva/crear/', crear_R, name="crear_R"),
        # This should now work
    path("create-payment/", create_payment, name="create_payment"),
    path('analizar-placa/', views.analizar_placa, name='analizar_placa'),
    path("crear-unidad/", crear_unidad, name="crear-unidad"),
    path('dashboard/stats/', Reporte.dashboard_stats, name='dashboard_stats'),
    path('dashboard/ultimas-visitas/', Reporte.ultimas_visitas, name='ultimas_visitas'),
    path('dashboard/proximas-reservas/', Reporte.proximas_reservas, name='proximas_reservas'),
    path('dashboard/metricas-financieras/', Reporte.metricas_financieras, name='metricas_financieras'),
    path('dashboard/ingresos-por-mes/', Reporte.ingresos_por_mes, name='ingresos_por_mes'),
    path('dashboard/pagos-pendientes/', Reporte.pagos_pendientes, name='pagos_pendientes'),

path('datos/personales', views.usuario, name='usuario'),
]
