from django.shortcuts import render
from rest_framework import viewsets
from .serializer import TaskSerializer
from .models import Persona


#crea el crud
class taskView(viewsets.ModelViewSet):
    serializer_class=TaskSerializer
    queryset = Persona.objects.all()