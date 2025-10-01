from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
import traceback
from ..models import Unidad


@api_view(['POST'])
def crear_unidad(request):
    try:
        print("=== INICIANDO CREACIÓN DE UNIDAD ===")
        print("Datos recibidos:", request.data)

        nro_modulo = request.data.get("nro_modulo")
        nro_piso = request.data.get("nro_piso")
        nro_habitacion = request.data.get("nro_habitacion")
        valor_mensual = request.data.get("valor_mensual")
        capacidad = request.data.get("capacidad")
        estado = request.data.get("estado", "disponible")

        # ✅ Validaciones mínimas
        if not nro_modulo or not nro_habitacion or not valor_mensual:
            return Response(
                {"error": "Faltan datos obligatorios (nro_modulo, nro_habitacion, valor_mensual)"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # ✅ Crear la unidad sin propietario ni contrato
        unidad = Unidad.objects.create(
            nro_modulo=nro_modulo,
            nro_piso=nro_piso,
            nro_habitacion=nro_habitacion,
            valor_mensual=valor_mensual,
            capacidad=capacidad,
            nro_contrato=None,
            propietario=None,
            estado=estado
        )

        print("✅ UNIDAD CREADA EXITOSAMENTE")

        return Response(
            {
                "message": "Unidad creada exitosamente",
                "unidad": {
                    "id": unidad.id,
                    "nro_modulo": unidad.nro_modulo,
                    "nro_piso": unidad.nro_piso,
                    "nro_habitacion": unidad.nro_habitacion,
                    "valor_mensual": str(unidad.valor_mensual),
                    "capacidad": unidad.capacidad,
                    "estado": unidad.estado
                }
            },
            status=status.HTTP_201_CREATED
        )

    except Exception as e:
        print("❌ ERROR:", str(e))
        print(traceback.format_exc())
        return Response(
            {"error": "Ocurrió un error al crear la unidad"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
