from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.hashers import check_password
from rest_framework_simplejwt.tokens import RefreshToken  # Si usas JWT
from ..models import Persona  # Import relativo corregido
from django.shortcuts import render, redirect

@api_view(['POST'])
def login(request):
    try:
        username = request.data.get('username', '').strip()
        password = request.data.get('password', '').strip()    
        if not username or not password:
            return Response(
                {"error": "Cédula y contraseña son requeridos"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        usuario = Persona.objects.filter(ci=username).first()
        if not usuario:
            return Response(
                {"error": "Usuario no encontrado"}, 
                status=status.HTTP_401_UNAUTHORIZED
            )
        if password == usuario.clave:
            refresh = RefreshToken.for_user(usuario)
            request.session['usuario'] = {
                'nombre': usuario.nombre,
                'apellido_1': usuario.apellido_paterno,
                'apellido_2': usuario.apellido_materno,
                'id': usuario.id,
                'ci': usuario.ci
            }
            return Response({
                "access": str(refresh.access_token),
                "refresh": str(refresh)
            })

        else:
            return Response(
                {"error": "Contraseña incorrecta"}, 
                status=status.HTTP_401_UNAUTHORIZED
            )
            
    except Exception as e:
        return Response(
            {"error": "Error interno del servidor"}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )