# colegio/logica/condominio.py
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
import traceback
from ..models import Persona, Pais

@api_view(['POST'])
def condominio(request):
    try:
        print("=== INICIANDO CREACIÓN DE USUARIO ===")
        print("Datos recibidos:", request.data)
        
        # Usar los nombres correctos de los campos del modelo
        nombre = request.data.get('nombre', '').strip()
        apellido_paterno = request.data.get('paterno', '').strip()  # Cambiado a apellido_paterno
        apellido_materno = request.data.get('materno', '').strip()  # Cambiado a apellido_materno
        telefono = request.data.get('telefono', '').strip()
        pais_id = request.data.get('pais', '').strip()
        ci = request.data.get('ci', '').strip()  # Nuevo campo
        email = request.data.get('email', '').strip()  # Nuevo campo
        clave = request.data.get('clave', '').strip()  # Nuevo campo

        print(f"Datos procesados: nombre='{nombre}', apellido_paterno='{apellido_paterno}', apellido_materno='{apellido_materno}', telefono='{telefono}', pais_id='{pais_id}'")

        # Validación simple
        if not nombre or not apellido_paterno or not telefono:
            error_msg = "Faltan datos obligatorios (nombre, apellido_paterno, telefono)"
            print(f"VALIDACIÓN FALLIDA: {error_msg}")
            return Response(
                {"error": error_msg},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Obtener la instancia de Pais si se proporcionó un ID
        pais_instance = None
        if pais_id:
            try:
                pais_instance = Pais.objects.get(id=pais_id)
                print(f"✅ PAIS ENCONTRADO: {pais_instance.nombre}")
            except Pais.DoesNotExist:
                print(f"❌ PAIS NO ENCONTRADO con ID: {pais_id}")
                return Response(
                    {"error": f"País con ID {pais_id} no existe"},
                    status=status.HTTP_400_BAD_REQUEST
                )

        print("Intentando crear persona en la base de datos...")
        
        # Insertar en la base de datos con los nombres correctos de campos
        persona = Persona.objects.create(
            nombre=nombre,
            apellido_paterno=apellido_paterno,  # Nombre correcto
            apellido_materno=apellido_materno,  # Nombre correcto
            telefono=telefono,
            pais=pais_instance,
            ci=ci or None,  # Opcional
            email=email or None,  # Opcional
            clave=clave or None  # Opcional
        )

        print(f"✅ PERSONA CREADA EXITOSAMENTE: ID={persona.id}")

        # Preparar respuesta
        response_data = {
            "id": persona.id,
            "nombre": persona.nombre,
            "apellido_paterno": persona.apellido_paterno,
            "apellido_materno": persona.apellido_materno,
            "telefono": persona.telefono,
            "ci": persona.ci,
            "email": persona.email,
            "fecha_creada": persona.fecha_creada.isoformat() if persona.fecha_creada else None,
        }
        
        # Incluir país solo si existe
        if persona.pais:
            response_data["pais"] = {
                "id": persona.pais.id,
                "nombre": persona.pais.nombre
            }

        return Response(
            response_data,
            status=status.HTTP_201_CREATED
        )

    except Exception as e:
        print("❌ ERROR CAPTURADO:")
        print(f"Tipo de error: {type(e).__name__}")
        print(f"Mensaje de error: {str(e)}")
        print("Traceback completo:")
        print(traceback.format_exc())
        return Response(
            {"error": f"Error interno: {str(e)}"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )