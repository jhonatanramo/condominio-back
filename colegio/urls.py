# colegio/urls.py
from django.urls import path, include
from rest_framework import routers
from .api import ProyectoVistas

router = routers.DefaultRouter()
#router.register(r'personas', ProyectoVistas, basename='personas')

#urlpatterns = [
 #   path("/new", include(router.urls)),
#    path("", ProyectoVistas)
#]
router.register('/',ProyectoVistas,'persona')
urlpatterns=router.urls