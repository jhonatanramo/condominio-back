
#------------------------
# colegio/logica/agendavisita.py
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
import traceback
from ..models import Visita, Reserva,Pagos
from django.utils import timezone



# colegio/logica/agendavisita.py

@api_view(["POST"])
def crear_R(request):
    try:
        # Obtener datos
        inicio = request.data.get("inicio")
        fin = request.data.get("fin")
        monto = request.data.get("monto")
        idareasocial = request.data.get("idareasocial")
        cant_gente = request.data.get("cant_gente")
        fecha = request.data.get("fecha")

        if not inicio or not fin or not idareasocial or not monto:
            return Response({"error": "Faltan datos obligatorios"}, status=status.HTTP_400_BAD_REQUEST)

        if not fecha:
            fecha = timezone.now().date()

        # Crear reserva - REMOVE `estado=None` OR SET A VALID VALUE
        reserva = Reserva.objects.create(
            horario_inicio=inicio,
            horario_fin=fin,
            fecha=fecha,
            # The 'estado' field will now use its default value of 'pendiente'
            cantidad_gente=cant_gente,
            area_social_id=8,
            persona_id=100, # Consider making this dynamic based on the logged-in user
        )

        # Crear pago
        pago = Pagos.objects.create(
            monto=100,
            fecha=timezone.now().date(),
            duracion_meses=0,
            url_foto=None,
            persona_id=100, # Consider making this dynamic
            unidad_id=None,
            reserva_id=reserva.id,
        )
        
        # 🔥 IMPORTANT: You MUST return a response
        return Response({"mensaje": "Reserva y pago creados exitosamente", "reserva_id": reserva.id}, status=status.HTTP_201_CREATED)
        
    except Exception as e:
        print("❌ ERROR:", str(e))
        print(traceback.format_exc())
        return Response({"error": "Ocurrió un error al crear la reserva"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)