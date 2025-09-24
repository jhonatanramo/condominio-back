from django.contrib import admin
from .models import Pais  # Solo los modelos que realmente existen

admin.site.register(Pais)
