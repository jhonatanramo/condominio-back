# colegio/logica/agendavisita.py
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
import traceback
from ..models import Visita, Reserva,Pagos
from django.utils import timezone


@api_view(['GET'])
def visita(request):
    try:
        visitas = Visita.objects.select_related(
            'autorizado', 'area_social', 'unidad'
        )
        
        # Transformar los datos para tener nombres de campos más limpios
        visitas_data = []
        for visita_obj in visitas:  # Cambiado el nombre para evitar conflicto
            visitas_data.append({
                # Datos de la visita
                "id": visita_obj.id,
                "nombre_visitante": visita_obj.nombre_visitante,
                "apellido_paterno": visita_obj.apellido_paterno,
                "apellido_materno": visita_obj.apellido_materno,
                "telefono": visita_obj.telefono,
                "fecha_ingreso": visita_obj.fecha_ingreso,
                "hora_ingreso": visita_obj.hora_ingreso,
                "fecha_salida": visita_obj.fecha_salida,
                "hora_salida": visita_obj.hora_salida,
                "motivo": visita_obj.motivo,
                
                # Datos del autorizado
                "autorizado": {
                    "id": visita_obj.autorizado.id if visita_obj.autorizado else None,
                    "nombre": visita_obj.autorizado.nombre if visita_obj.autorizado else None,
                    "apellido_paterno": visita_obj.autorizado.apellido_paterno if visita_obj.autorizado else None,
                    "apellido_materno": visita_obj.autorizado.apellido_materno if visita_obj.autorizado else None,
                    "ci": visita_obj.autorizado.ci if visita_obj.autorizado else None,
                    "telefono": visita_obj.autorizado.telefono if visita_obj.autorizado else None,
                    "email": visita_obj.autorizado.email if visita_obj.autorizado else None,
                } if visita_obj.autorizado else None,
                
                # Datos del área social
                "area_social": {
                    "id": visita_obj.area_social.id if visita_obj.area_social else None,
                    "nombre": visita_obj.area_social.nombre if visita_obj.area_social else None,
                    "ubicacion": visita_obj.area_social.ubicacion if visita_obj.area_social else None,
                    "hora_inicio_permitido": visita_obj.area_social.hora_inicio_permitido if visita_obj.area_social else None,
                    "hora_fin_permitido": visita_obj.area_social.hora_fin_permitido if visita_obj.area_social else None,
                    "capacidad_maxima": visita_obj.area_social.capacidad_maxima if visita_obj.area_social else None,
                } if visita_obj.area_social else None,
                
                # Datos de la unidad
                "unidad": {
                    "id": visita_obj.unidad.id if visita_obj.unidad else None,
                    "nro_modulo": visita_obj.unidad.nro_modulo if visita_obj.unidad else None,
                    "nro_piso": visita_obj.unidad.nro_piso if visita_obj.unidad else None,
                    "nro_habitacion": visita_obj.unidad.nro_habitacion if visita_obj.unidad else None,
                    "valor_mensual": float(visita_obj.unidad.valor_mensual) if visita_obj.unidad and visita_obj.unidad.valor_mensual else 0.00,
                    "capacidad": visita_obj.unidad.capacidad if visita_obj.unidad else None,
                    "nro_contrato": visita_obj.unidad.nro_contrato if visita_obj.unidad else None,
                    "estado": visita_obj.unidad.estado if visita_obj.unidad else None,
                } if visita_obj.unidad else None
            })

        return Response(visitas_data, status=status.HTTP_200_OK)

    except Exception as e:
        print(traceback.format_exc())
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
def reserva(request):
    try:
        # JOIN implícito con Persona y ÁreaSocial
        reservas = Reserva.objects.select_related('persona', 'area_social').values(
            "id",
            "fecha",
            "horario_inicio",
            "horario_fin",
            "estado",
            "cantidad_gente",
            # Persona
            "persona__id",
            "persona__nombre",
            "persona__apellido_paterno",
            "persona__telefono",
            # Área social
            "area_social__id",
            "area_social__nombre",
        )

        return Response(list(reservas), status=status.HTTP_200_OK)

    except Exception as e:
        print(traceback.format_exc())
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
