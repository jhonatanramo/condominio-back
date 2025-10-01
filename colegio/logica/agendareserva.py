from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
import traceback
from ..models import Reserva

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
#[
#  {
#    "id": 1,
#    "fecha": "2025-09-27",
#    "horario_inicio": "10:00:00",
#    "horario_fin": "12:00:00",
#    "estado": "confirmada",
#    "cantidad_gente": 15,
#    "persona__id": 3,
#    "persona__nombre": "Juan",
#    "persona__apellido_paterno": "Pérez",
#    "persona__telefono": "77777777",
#    "area_social__id": 2,
#    "area_social__nombre": "Piscina",
#  }
#]

